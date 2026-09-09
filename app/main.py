# -*- coding: utf-8 -*-
"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.sessions import router as agent_router
from app.core.config import get_settings

app = FastAPI(
    title="ecology-agent API",
    description="生态环境监测数据查询 Agent 后端（demo：水环境 + 水生生态）",
    version="0.2.0",
)

app.include_router(agent_router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "settings": {k: v for k, v in get_settings().items() if "url" not in k}}
