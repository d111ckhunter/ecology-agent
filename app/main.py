# -*- coding: utf-8 -*-
"""
FastAPI application entry point.

直接启动（无需命令行参数）:
    python -m app.main

可选覆盖（均有默认值，不传即用默认）:
    python -m app.main --host 0.0.0.0 --port 9000
    python -m app.main --no-reload

供 uvicorn 以模块方式加载（旧方式，仍可用）:
    uvicorn app.main:app --reload --port 8000
"""

import argparse
import os

import uvicorn
from fastapi import FastAPI

from app.api.sessions import router as agent_router
from app.core.config import get_settings

# ---- 启动默认值（集中在此，命令行可不传）----
DEFAULT_HOST = os.getenv("AGENT_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.getenv("AGENT_PORT", "8000"))
DEFAULT_RELOAD = os.getenv("AGENT_RELOAD", "1") == "1"  # 开发默认热重载

app = FastAPI(
    title="ecology-agent API",
    description="生态环境监测数据查询 Agent 后端（demo：水环境 + 水生生态）",
    version="0.2.0",
)

app.include_router(agent_router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "settings": {k: v for k, v in get_settings().items() if "url" not in k}}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="启动 ecology-agent API 服务")
    p.add_argument("--host", default=DEFAULT_HOST, help="监听地址（默认 %s）" % DEFAULT_HOST)
    p.add_argument("--port", type=int, default=DEFAULT_PORT, help="监听端口（默认 %d）" % DEFAULT_PORT)
    p.add_argument("--reload", dest="reload", action="store_true", default=True,
                   help="开发热重载（默认开）")
    p.add_argument("--no-reload", dest="reload", action="store_false", help="关闭热重载")
    return p


def run() -> None:
    args = build_parser().parse_args()
    print("ecology-agent API 启动: http://%s:%d  (reload=%s)"
          % (args.host, args.port, args.reload))
    # app="app.main:app" 供 --reload 正确找到入口（reload 需要字符串导入）
    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info",
    )


if __name__ == "__main__":
    run()
