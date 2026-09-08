# -*- coding: utf-8 -*-
"""Application configuration (read from .env / environment, with demo defaults)."""

import os
from functools import lru_cache

try:
    from dotenv import load_dotenv

    load_dotenv()  # 读取项目根目录 .env（若存在）；缺失时使用下方默认值
except ImportError:  # 未安装 python-dotenv 时静默降级
    pass

# demo 默认直连本地 MySQL（3307）；部署/协作时用 .env 或环境变量覆盖
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


@lru_cache
def get_settings() -> dict:
    return {
        "db_host": DB_HOST,
        "db_port": DB_PORT,
        "db_user": DB_USER,
        "db_name": DB_NAME,
        "sqlalchemy_database_url": SQLALCHEMY_DATABASE_URL,
        "server_database_url": SERVER_DATABASE_URL,
    }
