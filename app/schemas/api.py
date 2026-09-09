# -*- coding: utf-8 -*-
"""API 请求/响应模型（会话与聊天，独立于自动生成的数据表 schemas）。"""

from typing import Optional

from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    title: str = Field(default="", max_length=255, description="会话标题（可空，空则后端用首问生成）")


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000, description="用户提问")


class MessageOut(BaseModel):
    id: int
    session_id: str
    role: str
    content: Optional[str] = None
    sql: Optional[str] = None
    result_summary: Optional[str] = None
    error: Optional[str] = None
    created_at: str


class SessionOut(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str


class SessionListOut(BaseModel):
    total: int
    items: list[SessionOut]
