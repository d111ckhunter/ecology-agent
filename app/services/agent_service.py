# -*- coding: utf-8 -*-
"""
会话化 Agent 服务：把 SessionStore + EcologyAgent 编排为可流式输出的
事件生成器，供 SSE 路由消费。

SSE 事件协议（每项为一个 dict，路由层负责序列化）:
  {"type": "status",        "stage": "generating_sql|composing|chat_fallback"}
  {"type": "sql",           "sql": "...", "thinking": "..."}
  {"type": "table",         "columns": [...], "rows": [...], "truncated": bool}
  {"type": "answer_delta",  "delta": "..."}        # 回答文本逐块（token 级打字机）
  {"type": "error",         "message": "..."}
  {"type": "done",          "message_id": ..., "session_id": ..., "ok": bool, "kind": "sql|chat"}
"""

import json
import uuid

from app.agent.agent import AgentAnswer, EcologyAgent, make_result_summary
from app.agent.llm import LLMConfigError
from app.services.session_store import SessionStore

# 取最近多少条消息作为记忆候选（足够覆盖 MEMORY_WINDOW 轮）
HISTORY_FETCH = 30

_agent: EcologyAgent | None = None


def _get_agent() -> EcologyAgent:
    """进程内单例 agent；构造可能因缺 LLM_API_KEY 抛 LLMConfigError。"""
    global _agent
    if _agent is None:
        _agent = EcologyAgent()
    return _agent


def new_session_id() -> str:
    return str(uuid.uuid4())


def create_session(store: SessionStore, title: str = "") -> dict:
    return store.create_session(new_session_id(), title=title)


def stream_chat(store: SessionStore, session_id: str, question: str):
    """
    生成 SSE 事件（generator）。先校验会话与 LLM 配置，再执行一轮问答，
    并把 user/assistant 消息持久化。
    """
    # ---- 前置校验 ----
    session = store.get_session(session_id)
    if session is None:
        yield {"type": "error", "message": "会话不存在: %s" % session_id}
        return
    try:
        agent = _get_agent()
    except LLMConfigError as e:
        yield {"type": "error", "message": "LLM 未配置: %s" % e}
        return

    # ---- 持久化 user 消息（先入库再回答，保证提问不丢）----
    user_msg = store.add_message(session_id, role="user", content=question)

    # ---- 取历史记忆（不含本轮 user 消息——它在 add_message 后才入 recent）----
    history = store.recent_messages(session_id, n=HISTORY_FETCH)
    if history and history[-1].get("id") == user_msg.get("id"):
        history = history[:-1]  # 移除刚写入的本轮 user，避免自问自答

    # ---- 消费 run_events：转发前端事件并聚合完整答案用于落库 ----
    answer_parts: list[str] = []
    ans: AgentAnswer | None = None

    for ev in agent.run_events(question, history=history):
        etype = ev.get("type")
        if etype == "_final":
            ans = ev["answer"]
            continue
        if etype == "answer_delta":
            answer_parts.append(ev["delta"])
        # 其余事件（status/sql/table/error）原样转发
        yield ev

    # 若无内部 _final（理论上不会），构造兜底对象
    if ans is None:
        ans = AgentAnswer(question=question, ok=False,
                          answer_text="".join(answer_parts), error="agent 未返回结果")

    # ---- 持久化 assistant 消息（含 sql 与结果摘要，供下轮记忆）----
    asst_msg = store.add_message(
        session_id,
        role="assistant",
        content=ans.answer_text or (ans.error if not ans.ok else ""),
        sql=ans.sql,
        result_summary=(make_result_summary(ans.execution)
                        if ans.execution is not None else None),
        error=ans.error if not ans.ok else None,
    )
    yield {
        "type": "done",
        "session_id": session_id,
        "message_id": asst_msg.get("id"),
        "ok": ans.ok,
        "kind": ans.kind,
    }


def sse_format(event: dict) -> str:
    """把一个事件 dict 序列化为一条 SSE 消息（event: xxx / data: json）。"""
    etype = event.get("type", "message")
    data = json.dumps(event, ensure_ascii=False, default=str)
    return "event: %s\ndata: %s\n\n" % (etype, data)
