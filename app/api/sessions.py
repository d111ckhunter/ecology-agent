# -*- coding: utf-8 -*-
"""
会话与聊天路由（SSE）。

- POST   /api/sessions           创建会话
- GET    /api/sessions           会话列表（最新在前）
- GET    /api/sessions/{id}      会话详情
- GET    /api/sessions/{id}/messages   历史消息
- POST   /api/sessions/{id}/chat 提问（SSE 流式返回）
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session as OrmSession

from app.core.database import get_db
from app.schemas.api import ChatRequest, MessageOut, SessionCreate, SessionListOut, SessionOut
from app.services.agent_service import create_session, sse_format, stream_chat
from app.services.mysql_session_store import MySQLSessionStore
from app.services.session_store import SessionStore

router = APIRouter(prefix="/api", tags=["agent"])


def _store(db: OrmSession) -> SessionStore:
    return MySQLSessionStore(db)


@router.post("/sessions", response_model=SessionOut, status_code=201)
def api_create_session(payload: SessionCreate, db: OrmSession = Depends(get_db)):
    return create_session(_store(db), title=payload.title)


@router.get("/sessions", response_model=SessionListOut)
def api_list_sessions(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: OrmSession = Depends(get_db),
):
    items = _store(db).list_sessions(limit=limit, offset=offset)
    return SessionListOut(total=len(items), items=[SessionOut(**s) for s in items])


@router.get("/sessions/{session_id}", response_model=SessionOut)
def api_get_session(session_id: str, db: OrmSession = Depends(get_db)):
    s = _store(db).get_session(session_id)
    if s is None:
        raise HTTPException(404, "会话不存在")
    return SessionOut(**s)


@router.delete("/sessions/{session_id}", status_code=204)
def api_delete_session(session_id: str, db: OrmSession = Depends(get_db)):
    deleted = _store(db).delete_session(session_id)
    if not deleted:
        raise HTTPException(404, "会话不存在")
    return None


@router.get("/sessions/{session_id}/messages", response_model=list[MessageOut])
def api_list_messages(session_id: str, db: OrmSession = Depends(get_db)):
    store = _store(db)
    if store.get_session(session_id) is None:
        raise HTTPException(404, "会话不存在")
    msgs = store.list_messages(session_id)
    return [MessageOut(**m) for m in msgs]


@router.post("/sessions/{session_id}/chat")
def api_chat(session_id: str, payload: ChatRequest, db: OrmSession = Depends(get_db)):
    store = _store(db)
    if store.get_session(session_id) is None:
        raise HTTPException(404, "会话不存在")

    def _events():
        for ev in stream_chat(store, session_id, payload.question):
            yield sse_format(ev)

    # 同步生成器由 Starlette 放入线程池迭代，避免阻塞事件循环
    return StreamingResponse(
        _events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 代理层不缓冲
        },
    )
