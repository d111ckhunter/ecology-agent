# -*- coding: utf-8 -*-
"""
Agent orchestration: 中文问题 -> SQL -> 只读执行 -> 自然语言回答。
（v2 多轮记忆：SQL 演进式；v3：回答文本 token 级流式 + 自然语言兜底）

编排核心是事件生成器 run_events()：
  * 数据类问题：生成 SQL -> 只读执行(护栏) -> 失败回喂修正(≤MAX_RETRIES)
    -> 成功则依次产出 sql/table 事件与 answer_delta 流式块
  * 兜底（轻量版）：LLM 判定问题不涉及库内数据(返回 sql:null)，或 SQL 反复执行失败，
    则走"生态助手纯聊天"prompt 直接生成自然语言回答（不带全量 schema，防编造数值）
  * ask() 是 run_events() 的聚合封装（供 CLI / 既有调用兼容）

run_events 产出的事件 dict（type 前缀 "_" 为内部事件，不直接发往前端）：
  {"type":"status",  "stage": "generating_sql|composing|chat_fallback"}
  {"type":"sql",     "sql","thinking"}
  {"type":"table",   "columns","rows","truncated","elapsed"}
  {"type":"answer_delta","delta"}          # 回答文本逐块
  {"type":"error",   "message"}
  {"type":"_final",  "answer": AgentAnswer}  # 内部：收尾携带完整结果供持久化
"""

from dataclasses import dataclass, field

from app.agent.db_tool import ReadonlyDBTool, SQLExecutionResult
from app.agent.schema import build_schema_text, compact_tables
from app.agent.llm import get_llm, MockLLM, LLMError

MAX_RETRIES = 2  # SQL 生成失败后的纠错次数（首次 + 2 次重试）
SQL_ROW_PREVIEW = 30  # 回喂 LLM 组织回答时最多预览的行数
MEMORY_WINDOW = 5  # 多轮记忆滑动窗口（保留最近 N 个“问题+成功SQL”对）
RESULT_SUMMARY_ROWS = 10  # 写入会话存储的结果摘要保留前 N 行


def build_memory_text(history: list[dict] | None) -> str:
    """
    从 history 中提取最近 MEMORY_WINDOW 个“成功问答对”渲染为回顾文本。

    只有 assistant 消息且带 sql（执行成功）的轮次才进入记忆；
    单独的提问、兜底聊天(无 sql)轮不进入（避免误导下一轮改写）。
    """
    if not history:
        return ""
    pairs = []
    pending_q = None
    for m in history:
        role = m.get("role")
        if role == "user":
            pending_q = (m.get("content") or "").strip()
        elif role == "assistant" and pending_q is not None and m.get("sql"):
            pairs.append({
                "q": pending_q,
                "sql": m["sql"],
                "summary": (m.get("result_summary") or "").strip(),
            })
            pending_q = None  # 该问题已配对，避免一条历史复用多次
    if not pairs:
        return ""
    lines = ["\n===== 最近对话回顾（判断是否追问；追问可改写最近成功的 SQL）====="]
    for i, p in enumerate(pairs[-MEMORY_WINDOW:], start=1):
        lines.append("[%d] 用户: %s" % (i, p["q"]))
        lines.append("    SQL: %s" % p["sql"])
        if p["summary"]:
            lines.append("    结果摘要: %s" % p["summary"])
    lines.append("说明：若本次问题是对上面某轮的追问/引用，请基于对应 SQL 改写；若属全新主题，忽略回顾直接编写新 SQL。")
    return "\n".join(lines)


def make_result_summary(result: SQLExecutionResult, max_rows: int = RESULT_SUMMARY_ROWS) -> str:
    """把一次成功执行的结果压缩为文本摘要，供会话存储/下轮记忆使用。"""
    if not result.ok:
        return "执行失败: %s" % result.error
    if not result.columns:
        return "(空结果)"
    rows_txt = []
    for row in result.rows[:max_rows]:
        rows_txt.append(" | ".join(str(v) for v in row))
    txt = "列: %s\n" % ", ".join(result.columns)
    txt += "行数: %d%s\n" % (len(result.rows), "（已截断）" if result.truncated else "")
    if rows_txt:
        txt += "前 %d 行:\n%s" % (min(len(rows_txt), max_rows), "\n".join(rows_txt))
    return txt


SYSTEM_TEMPLATE = """你是一名生态环境监测数据库的 SQL 专家。根据用户的中文问题编写 MySQL 查询。

规则：
1. 只能输出只读查询：SELECT / WITH（可用于聚合、联表、子查询）。
2. 不得使用任何写入/管理语句（DELETE/UPDATE/INSERT/DDL/DROP...），不得使用分号拼接多条语句。
3. 表名、列名一律使用反引号包裹（例如 `hydro_data`.`water_level`），因为存在 `as`、`class` 等保留字列名。
4. 结合给出的表结构字典判断用哪些表；表间通过外键（station_code / heduan_code / fish_code）关联。
5. 时间类条件优先用 `monitor_time` 列；涉及年份/月份用 MySQL 日期函数。
6. 若用户问题不涉及对数据库做查询（闲聊、概念询问、方法论等），或现有表/列无法回答，
   不要编造，回复 {{"sql": null, "reason": "说明原因"}}。
7. 不要假设表中有你未在字典里看到的列。
8. 若“最近对话回顾”与本问题相关，应尽量基于回顾中最近的成功 SQL 做局部改写（换时间/加列/改分组等），保持列名风格一致。

输出格式（严格 JSON，不要夹杂其他文字）：
{{"sql": "你的 SQL", "thinking": "一句简短说明"}}
若无需查询即可回答：{{"sql": null, "reason": "说明原因"}}

===== 表结构字典 =====
{schema_text}
"""

SYSTEM_REFINE_TEMPLATE = """上一次生成的 SQL 执行失败，错误信息如下：
{error}

原始用户问题：{question}

请根据错误修正 SQL。仍只允许只读查询。再次输出严格 JSON：
{{"sql": "修正后的 SQL", "thinking": "修正说明"}}
若确认无法回答：{{"sql": null, "reason": "说明原因"}}
"""

SYSTEM_ANSWER_TEMPLATE = """你是生态环境监测数据分析助手。基于下面的查询结果回答用户，要求自然、口语化、准确：

要求：
- 用自然的中文组织回答，像专业助手对话一样，避免“根据查询结果如下”之类的模板腔。
- 直接给出结论与关键数值；可用 Markdown（如 **加粗** 关键数字、- 列表归纳）让回答易读。
- 结果为空时自然说明“目前没有查到相关记录”，不要编造数据。
- 涉及对比/趋势/排名时做简要归纳。
- 不得编造查询结果之外的数值。

原始问题：{question}

执行的 SQL：
{sql}

查询结果（列: {columns}）：
{rows}
"""

SYSTEM_FALLBACK_TEMPLATE = """你是“生态监测数据助手”。用户当前的问题没有走数据库查询（可能是闲聊、询问概念，
或是数据库暂时无法满足）。请用自然、口语化的中文回答。

要求：
1. 不要编造 ecology_demo 数据库中的具体监测数值或记录。
2. 如果用户想要的数据必须来自数据库，请如实说明“目前无法从数据库查询到该数据”，并简要说明原因。
3. 闲聊、生态/水质概念解释、方法论咨询等可以正常给出有价值的回答。
4. 可用简短 Markdown 增强可读性（如加粗、列表），但不要过度。

当前数据库包含以下数据表（共 {n} 张，可据此判断哪些问题能查）：
{tables}
"""


@dataclass
class AgentAnswer:
    question: str
    sql: str | None = None
    thinking: str = ""
    answer_text: str = ""
    ok: bool = False
    kind: str = "sql"  # sql: 数据查询回答 / chat: 自然语言兜底回答
    retries: int = 0
    execution: SQLExecutionResult | None = None
    error: str = ""
    trace: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "sql": self.sql,
            "thinking": self.thinking,
            "answer": self.answer_text,
            "ok": self.ok,
            "kind": self.kind,
            "retries": self.retries,
            "error": self.error,
            "execution": None if not self.execution else {
                "ok": self.execution.ok,
                "columns": self.execution.columns,
                "row_count": len(self.execution.rows),
                "truncated": self.execution.truncated,
                "elapsed": self.execution.elapsed,
            },
            "result_summary": None if not self.execution else make_result_summary(self.execution),
            "trace": self.trace,
        }


class EcologyAgent:
    def __init__(self, llm=None, tool: ReadonlyDBTool | None = None):
        self.llm = llm if llm is not None else get_llm()
        self.tool = tool if tool is not None else ReadonlyDBTool()
        self.schema_text = build_schema_text()
        self.is_mock = isinstance(self.llm, MockLLM)

    # ---------------- prompt builders ----------------
    def _system_prompt(self, history: list[dict] | None = None) -> str:
        memory = build_memory_text(history)
        return SYSTEM_TEMPLATE.format(schema_text=self.schema_text) + memory

    def _fallback_messages(self, question: str, reason: str) -> list[dict]:
        tables = compact_tables()
        names = "、".join("[%s]%s" % (t["table"], t["chinese"]) for t in tables)
        sys_prompt = SYSTEM_FALLBACK_TEMPLATE.format(
            n=len(tables), tables=names,
        )
        if reason:
            sys_prompt += "\n\n（参考：SQL 生成阶段说明：%s）" % reason[:300]
        return [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": question},
        ]

    # ---------------- orchestration ----------------
    def run_events(self, question: str, history: list[dict] | None = None):
        """
        事件生成器：yield 编排过程中的逐步事件（见模块 docstring）。
        调用方（SSE 服务/聚合 ask）据此渲染与持久化。
        """
        ans = AgentAnswer(question=question)

        # ---- 1. 生成 SQL（携带记忆上下文）----
        yield {"type": "status", "stage": "generating_sql"}
        messages = [
            {"role": "system", "content": self._system_prompt(history)},
            {"role": "user", "content": question},
        ]
        gen = self.llm.chat_json(messages)
        sql, thinking, reason = self._extract_sql(gen)

        if sql is None:
            # ---- 兜底：无需查询，直接自然语言回答 ----
            ans.kind = "chat"
            ans.error = reason or "LLM 未给出 SQL"
            yield {"type": "status", "stage": "chat_fallback"}
            yield from self._stream_fallback(ans, question, reason)
            yield {"type": "_final", "answer": ans}
            return

        ans.sql = sql
        ans.thinking = thinking
        ans.trace.append("生成 SQL: %s" % sql)

        # ---- 2. 执行 + 纠错重试 ----
        result = self.tool.execute(sql)
        ans.execution = result
        attempt = 0
        while not result.ok and attempt < MAX_RETRIES:
            attempt += 1
            ans.retries = attempt
            ans.trace.append("执行失败(%d): %s" % (attempt, result.error[:200]))
            refine_msgs = [
                {"role": "system", "content": SYSTEM_REFINE_TEMPLATE.format(
                    error=result.error[:1000], question=question)},
                {"role": "user", "content": question},
            ]
            gen = self.llm.chat_json(refine_msgs)
            sql2, thinking2, reason2 = self._extract_sql(gen)
            if sql2 is None:
                # 修正时 LLM 也放弃 → 兜底自然语言
                ans.kind = "chat"
                ans.error = reason2 or "修正后仍无 SQL"
                yield {"type": "status", "stage": "chat_fallback"}
                yield from self._stream_fallback(ans, question, reason2)
                yield {"type": "_final", "answer": ans}
                return
            ans.sql = sql2
            ans.thinking = thinking2
            ans.trace.append("修正 SQL(%d): %s" % (attempt, sql2))
            result = self.tool.execute(sql2)
            ans.execution = result

        if not result.ok:
            # ---- 兜底：SQL 反复执行失败 → 自然语言说明 ----
            ans.kind = "chat"
            ans.error = result.error
            yield {"type": "status", "stage": "chat_fallback"}
            yield from self._stream_fallback(ans, question,
                                             "查询执行失败: %s" % result.error[:300])
            yield {"type": "_final", "answer": ans}
            return

        # ---- 3. 成功：先发 sql/table，再流式组织自然语言回答 ----
        ans.ok = True
        yield {"type": "sql", "sql": ans.sql, "thinking": ans.thinking}
        yield {
            "type": "table",
            "columns": result.columns,
            "rows": result.rows,
            "truncated": result.truncated,
            "elapsed": result.elapsed,
        }
        yield {"type": "status", "stage": "composing"}

        rows_txt = self._format_rows(result)
        answer_msgs = [
            {"role": "system", "content": SYSTEM_ANSWER_TEMPLATE.format(
                question=question, sql=ans.sql,
                columns=", ".join(result.columns), rows=rows_txt)},
            {"role": "user", "content": "请组织回答。"},
        ]
        try:
            for delta in self.llm.chat_stream(answer_msgs):
                if delta:
                    ans.answer_text += delta
                    yield {"type": "answer_delta", "delta": delta}
        except LLMError as e:
            ans.error = str(e)
            yield {"type": "error", "message": str(e)}
        if not ans.answer_text.strip():
            ans.answer_text = "（查询执行成功，但未能生成回答文本）"
        yield {"type": "_final", "answer": ans}

    def _stream_fallback(self, ans: AgentAnswer, question: str, reason: str | None):
        """兜底聊天：流式产出自然语言文本，写入 ans.answer_text。"""
        msgs = self._fallback_messages(question, reason or "")
        try:
            for delta in self.llm.chat_stream(msgs):
                if delta:
                    ans.answer_text += delta
                    yield {"type": "answer_delta", "delta": delta}
        except LLMError as e:
            ans.error = str(e)
            yield {"type": "error", "message": str(e)}
        if ans.answer_text.strip():
            ans.ok = True

    def ask(self, question: str, history: list[dict] | None = None) -> AgentAnswer:
        """聚合版：消费 run_events，返回完整 AgentAnswer（兼容 CLI/旧调用）。"""
        ans: AgentAnswer | None = None
        for ev in self.run_events(question, history=history):
            if ev["type"] == "_final":
                ans = ev["answer"]
        return ans if ans is not None else AgentAnswer(question=question)

    # ---- helpers ----
    @staticmethod
    def _extract_sql(gen: dict | None):
        if not gen:
            return None, "", "LLM 输出无法解析为 JSON"
        if gen.get("sql") is None:
            return None, gen.get("thinking", ""), gen.get("reason", "无法回答")
        return gen["sql"], gen.get("thinking", ""), ""

    @staticmethod
    def _format_rows(result: SQLExecutionResult, max_chars: int = 3000) -> str:
        if not result.columns:
            return "(空)"
        lines = []
        for row in result.rows[:SQL_ROW_PREVIEW]:
            cell = ", ".join(str(v) for v in row)
            lines.append(cell)
        txt = "\n".join(lines)
        truncated = len(result.rows) > SQL_ROW_PREVIEW or len(txt) > max_chars
        if len(txt) > max_chars:
            txt = txt[:max_chars] + " ..."
        if truncated:
            txt += "\n[结果已截断]"
        return txt


def build_agent(force_mock: bool = False) -> EcologyAgent:
    return EcologyAgent(llm=get_llm(force_mock=force_mock))


if __name__ == "__main__":  # 自检（mock 模式，不联网）
    agent = build_agent(force_mock=True)

    # 数据类问题：确认事件序列（含 answer_delta）
    evs = list(agent.run_events("列出各测站监测记录数"))
    types = [e["type"] for e in evs]
    print("data-events:", types)
    assert "sql" in types and "table" in types and "answer_delta" in types

    # 闲聊类问题：应走 chat_fallback（无 sql/table）
    evs2 = list(agent.run_events("你好，介绍一下你们监测什么？"))
    types2 = [e["type"] for e in evs2]
    print("chat-events:", types2)
    ans2 = evs2[-1]["answer"]
    assert ans2.kind == "chat" and ans2.ok and not ans2.sql
    print("chat-ok:", ans2.ok, "| text head:", ans2.answer_text[:60])
