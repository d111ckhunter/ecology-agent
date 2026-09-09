# -*- coding: utf-8 -*-
"""
会话存储抽象层。

API 层只依赖 SessionStore 协议（不感知 MySQL/Redis 实现细节），
未来加 Redis 实现时新增一个类并在工厂函数切换即可。

协议中传输的是普通 dict（非 ORM 对象），方便替换实现与序列化。
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class SessionStore(ABC):
    """对话会话与消息的读写接口。所有方法返回普通 dict。"""

    # ---------------- sessions ----------------
    @abstractmethod
    def create_session(self, session_id: str, title: str = "") -> dict:
        """创建会话，返回 session dict。"""

    @abstractmethod
    def get_session(self, session_id: str) -> dict | None:
        """按 id 查会话，不存在返回 None。"""

    @abstractmethod
    def list_sessions(self, limit: int = 50, offset: int = 0) -> list[dict]:
        """按更新时间倒序列出会话（最新在前）。"""

    @abstractmethod
    def touch_session(self, session_id: str) -> None:
        """更新会话 updated_at（有新消息时调用）。"""

    @abstractmethod
    def delete_session(self, session_id: str) -> bool:
        """删除会话及其全部消息；存在并删除返回 True，不存在返回 False。"""

    # ---------------- messages ----------------
    @abstractmethod
    def add_message(self, session_id: str, *, role: str, content: str | None = None,
                    sql: str | None = None, result_summary: str | None = None,
                    error: str | None = None) -> dict:
        """追加一条消息并 touch 会话；返回消息 dict（含 id/created_at）。"""

    @abstractmethod
    def list_messages(self, session_id: str, limit: int = 200) -> list[dict]:
        """按时间正序列出会话内消息。"""

    def recent_messages(self, session_id: str, n: int = 5) -> list[dict]:
        """取最近 n 条消息（正序返回，供 Agent 上下文记忆）。"""
        msgs = self.list_messages(session_id, limit=n)
        return msgs[-n:]


def _to_dict(obj) -> dict[str, Any]:
    d = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    # 规范时间类型：datetime -> isoformat 字符串（JSON 友好）
    for k, v in d.items():
        if isinstance(v, datetime):
            d[k] = v.isoformat()
    return d
