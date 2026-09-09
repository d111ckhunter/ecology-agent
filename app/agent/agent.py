# -*- coding: utf-8 -*-
"""
Agent orchestration: 中文问题 -> SQL -> 只读执行 -> 自然语言回答。
（v2 增加多轮对话记忆：SQL 演进式 —— 追问基于最近成功的 SQL 改写）

流程:
  1) 组装系统提示词（身份规则 + schema 字典 + 最近对话回顾(5轮滑动窗口)）
  2) 请求 LLM 产出 {"sql": "...", "thinking": "..."}
  3) 经 ReadonlyDBTool 执行（含护栏）
  4) SQL 失败 -> 将错误回喂 LLM 修正，最多 MAX_RETRIES 次
  5) 成功 -> 将结果交给 LLM 组织为中文回答

记忆输入 history 约定（与 SessionStore.list_messages 返回结构兼容）：
  [{"role": "user", "content": 问题},
   {"role": "assistant", "content": 回答, "sql": "...", "result_summary": "..."}, ...]
"""

from dataclasses import dataclass, field

from app.agent.db_tool import ReadonlyDBTool, SQLExecutionResult
from app.agent.schema import build_schema_text
from app.agent.llm import get_llm, MockLLM

MAX_RETRIES = 2  # SQL 生成失败后的纠错次数（首次 + 2 次重试）
SQL_ROW_PREVIEW = 30  # 回喂 LLM 组织回答时最多预览的行数
MEMORY_WINDOW = 5  # 多轮记忆滑动窗口（保留最近 N 个“问题+成功SQL”对）
RESULT_SUMMARY_ROWS = 10  # 写入会话存储的结果摘要保留前 N 行


def build_memory_text(history: list[dict] | None) -> str:
    """
    从 history 中提取最近 MEMORY_WINDOW 个“成功问答对”渲染为回顾文本。

    只有 assistant 消息且带 sql（执行成功）的轮次才进入记忆；
    单独的提问或失败轮不进入（避免误导下一轮改写）。
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
6. 若用户问题无法由现有表/列回答（例如查询不存在字段），不要编造，回复 {{"sql": null, "reason": "..."}}。
7. 不要假设表中有你未在字典里看到的列。
8. 若“最近对话回顾”与本问题相关，应尽量基于回顾中最近的成功 SQL 做局部改写（换时间/加列/改分组等），保持列名风格一致。

输出格式（严格 JSON，不要夹杂其他文字）：
{{"sql": "你的 SQL", "thinking": "一句简短说明"}}
若无法回答：{{"sql": null, "reason": "说明原因"}}

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

SYSTEM_ANSWER_TEMPLATE = """你是生态环境监测数据分析助手。根据用户的提问、执行的 SQL 和查询结果，用中文给出清晰、准确、简洁的回答。

要求：
- 直接回答用户问题，引用关键数值。
- 结果为空时如实说明“未查询到相关记录”，不要编造数据。
- 可对数字做必要的归纳（最大值、趋势、排名），但不得超出查询结果凭空补充。
- 如 SQL 最终未能执行成功，请说明失败原因。

原始问题：{question}

执行的 SQL：
{sql}

查询结果（列: {columns}）：
{rows}
"""


@dataclass
class AgentAnswer:
    question: str
    sql: str | None = None
    thinking: str = ""
    answer_text: str = ""
    ok: bool = False
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

    def _system_prompt(self, history: list[dict] | None = None) -> str:
        memory = build_memory_text(history)
        return SYSTEM_TEMPLATE.format(schema_text=self.schema_text) + memory

    def ask(self, question: str, history: list[dict] | None = None) -> AgentAnswer:
        ans = AgentAnswer(question=question)
        # ---- 1. 生成 SQL（携带记忆上下文）----
        messages = [
            {"role": "system", "content": self._system_prompt(history)},
            {"role": "user", "content": question},
        ]
        gen = self.llm.chat_json(messages)
        sql, thinking, reason = self._extract_sql(gen)
        if sql is None:
            ans.error = reason or "LLM 未给出 SQL"
            ans.thinking = thinking
            ans.answer_text = self._no_answer_text(ans.error)
            return ans
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
                ans.error = reason2 or "修正后仍无 SQL"
                ans.answer_text = self._no_answer_text(ans.error)
                return ans
            ans.sql = sql2
            ans.thinking = thinking2
            ans.trace.append("修正 SQL(%d): %s" % (attempt, sql2))
            result = self.tool.execute(sql2)
            ans.execution = result

        if not result.ok:
            ans.error = result.error
            ans.answer_text = "查询执行失败：%s（已重试 %d 次）" % (result.error[:300], ans.retries)
            return ans

        ans.ok = True
        # ---- 3. 结果 -> 自然语言 ----
        rows_txt = self._format_rows(result)
        answer_msgs = [
            {"role": "system", "content": SYSTEM_ANSWER_TEMPLATE.format(
                question=question, sql=ans.sql,
                columns=", ".join(result.columns), rows=rows_txt)},
            {"role": "user", "content": "请组织回答。"},
        ]
        final = self.llm.chat(answer_msgs)
        ans.answer_text = final.strip() or "（查询成功，未生成回答文本）"
        return ans

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

    @staticmethod
    def _no_answer_text(error: str) -> str:
        return "未能生成可执行的查询：%s" % error


def build_agent(force_mock: bool = False) -> EcologyAgent:
    return EcologyAgent(llm=get_llm(force_mock=force_mock))


if __name__ == "__main__":  # 自检（mock 模式，不联网）
    agent = build_agent(force_mock=True)
    # 模拟两轮：第二轮带第一轮的历史，验证记忆渲染不报错
    ans1 = agent.ask("列出各测站监测记录数，从多到少排序")
    history = [
        {"role": "user", "content": ans1.question},
        {"role": "assistant", "content": ans1.answer_text, "sql": ans1.sql,
         "result_summary": make_result_summary(ans1.execution)},
    ]
    ans2 = agent.ask("只看水文站的？", history=history)
    print("round1 ok:", ans1.ok)
    print("round2 ok:", ans2.ok)
    print("memory sample:\n", build_memory_text(history)[:300])
