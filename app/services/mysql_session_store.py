# -*- coding: utf-8 -*-
"""MySQL 会话存储实现（基于 SQLAlchemy ORM 会话表）。"""

from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.session import AgentMessage, AgentSession
from app.services.session_store import SessionStore, _to_dict


class MySQLSessionStore(SessionStore):
    """用 ecology_demo 库中的 agent_sessions / agent_messages 表存取。"""

    def __init__(self, db: Session):
        self.db = db

    # ---------------- sessions ----------------
    def create_session(self, session_id: str, title: str = "") -> dict:
        obj = AgentSession(id=session_id, title=title)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return _to_dict(obj)

    def get_session(self, session_id: str) -> dict | None:
        obj = self.db.get(AgentSession, session_id)
        return _to_dict(obj) if obj else None

    def list_sessions(self, limit: int = 50, offset: int = 0) -> list[dict]:
        objs = (
            self.db.execute(
                select(AgentSession)
                .order_by(AgentSession.updated_at.desc())
                .limit(limit)
                .offset(offset)
            )
            .scalars()
            .all()
        )
        return [_to_dict(o) for o in objs]

    def touch_session(self, session_id: str) -> None:
        obj = self.db.get(AgentSession, session_id)
        if obj:
            obj.updated_at = datetime.utcnow()
            self.db.commit()

    def delete_session(self, session_id: str) -> bool:
        obj = self.db.get(AgentSession, session_id)
        if obj is None:
            return False
        # ORM cascade="all, delete-orphan" 级联删除消息（DB 外键另有 ON DELETE CASCADE）
        self.db.delete(obj)
        self.db.commit()
        return True

    # ---------------- messages ----------------
    def add_message(self, session_id: str, *, role: str, content: str | None = None,
                    sql: str | None = None, result_summary: str | None = None,
                    error: str | None = None) -> dict:
        msg = AgentMessage(
            session_id=session_id, role=role, content=content, sql=sql,
            result_summary=result_summary, error=error,
        )
        self.db.add(msg)
        obj = self.db.get(AgentSession, session_id)
        if obj:
            obj.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(msg)
        return _to_dict(msg)

    def list_messages(self, session_id: str, limit: int = 200) -> list[dict]:
        objs = (
            self.db.execute(
                select(AgentMessage)
                .where(AgentMessage.session_id == session_id)
                .order_by(AgentMessage.id.asc())
                .limit(limit)
            )
            .scalars()
            .all()
        )
        return [_to_dict(o) for o in objs]

    def recent_messages(self, session_id: str, n: int = 5) -> list[dict]:
        """取最近 n 条（按 id 倒序取再反转为正序）。"""
        objs = (
            self.db.execute(
                select(AgentMessage)
                .where(AgentMessage.session_id == session_id)
                .order_by(AgentMessage.id.desc())
                .limit(n)
            )
            .scalars()
            .all()
        )
        return [_to_dict(o) for o in reversed(objs)]
