# -*- coding: utf-8 -*-
"""Application configuration (read from .env / environment, with demo defaults)."""

import os
from functools import lru_cache

try:
    from dotenv import load_dotenv

    load_dotenv()  # 读取项目根目录 .env（若存在）；缺失时使用下方默认值
except ImportError:  # 未安装 python-dotenv 时静默降级
    pass

# ---------------------------------------------------------------------------
# 主连接（建库/建表/mock 灌数，需写权限）
# ---------------------------------------------------------------------------
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3307"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")
DB_NAME = os.getenv("DB_NAME", "ecology_demo")

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?charset=utf8mb4"
)

# 建库时使用的服务级连接（不带库名）
SERVER_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
    "?charset=utf8mb4"
)

# ---------------------------------------------------------------------------
# 只读连接（Agent 查询用；账号 ecology_ro 仅授予 SELECT）
# ---------------------------------------------------------------------------
DB_RO_HOST = os.getenv("DB_RO_HOST", DB_HOST)
DB_RO_PORT = int(os.getenv("DB_RO_PORT", str(DB_PORT)))
DB_RO_USER = os.getenv("DB_RO_USER", "ecology_ro")
DB_RO_PASSWORD = os.getenv("DB_RO_PASSWORD", "")
DB_RO_NAME = os.getenv("DB_RO_NAME", DB_NAME)

READONLY_DATABASE_URL = (
    f"mysql+pymysql://{DB_RO_USER}:{DB_RO_PASSWORD}@{DB_RO_HOST}:{DB_RO_PORT}/{DB_RO_NAME}"
    "?charset=utf8mb4"
)

# ---------------------------------------------------------------------------
# LLM（DeepSeek，OpenAI 兼容接口）
# ---------------------------------------------------------------------------
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-v4-flash")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))

# Agent 查询护栏
SQL_MAX_ROWS = int(os.getenv("SQL_MAX_ROWS", "200"))   # 强制 LIMIT 上限
SQL_TIMEOUT_SECONDS = int(os.getenv("SQL_TIMEOUT_SECONDS", "10"))


@lru_cache
def get_settings() -> dict:
    return {
        "db_host": DB_HOST,
        "db_port": DB_PORT,
        "db_user": DB_USER,
        "db_name": DB_NAME,
        "sqlalchemy_database_url": SQLALCHEMY_DATABASE_URL,
        "server_database_url": SERVER_DATABASE_URL,
        "readonly_database_url": READONLY_DATABASE_URL,
        "llm_api_key": "***" if LLM_API_KEY else "",
        "llm_base_url": LLM_BASE_URL,
        "llm_model": LLM_MODEL,
        "sql_max_rows": SQL_MAX_ROWS,
        "sql_timeout_seconds": SQL_TIMEOUT_SECONDS,
    }
