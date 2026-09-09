# -*- coding: utf-8 -*-
"""
会话与消息持久化模型（多轮对话记忆用）。

挂在 app.models.Base 下，运行 scripts/init_db.py 时会一并建表。
存储层预留 SessionStore 抽象，未来可替换为 Redis 实现而不影响 API。
"""

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.models.base import Base


class AgentSession(Base):
    """一次对话会话（= 一个会话上下文）。"""

    __tablename__ = "agent_sessions"
    __table_args__ = {"comment": "Agent 对话会话表"}

    id = Column(String(36), primary_key=True, nullable=False, comment="会话ID(UUID)")
    title = Column(String(255), nullable=False, default="", comment="会话标题(取首问前若干字)")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow,
                        comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow,
                        onupdate=datetime.utcnow, comment="最后更新时间")

    messages = relationship(
        "AgentMessage",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="AgentMessage.created_at",
    )


class AgentMessage(Base):
    """会话内的一条消息。"""

    __tablename__ = "agent_messages"
    __table_args__ = (
        Index("ix_agent_messages_session", "session_id", "created_at"),
        {"comment": "Agent 对话消息表"},
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True,
                nullable=False, comment="消息ID")
    session_id = Column(
        String(36),
        ForeignKey("agent_sessions.id", ondelete="CASCADE"),
        nullable=False,
        comment="所属会话ID",
    )
    role = Column(String(16), nullable=False, comment="user / assistant")
    content = Column(Text, nullable=True, comment="消息正文(问题或回答文本)")
    sql = Column(Text, nullable=True, comment="该轮生成的SQL(assistant)")
    result_summary = Column(Text, nullable=True,
                            comment="查询结果摘要(列名+前N行+行数, 供下轮记忆)")
    error = Column(Text, nullable=True, comment="该轮错误信息(若有)")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow,
                        comment="消息时间")

    session = relationship("AgentSession", back_populates="messages")
