# -*- coding: utf-8 -*-
"""
初始化 MySQL 数据库与全部表结构（demo：水环境 + 水生生态）。

用法（fastapi conda 环境）:
    python scripts/init_db.py            # 建库(若不存在) + 建表
    python scripts/init_db.py --drop     # 先 DROP 已有表再重建（危险，仅演示）
"""

import os
import sys

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Engine

# 把项目根目录加入 sys.path（无论从哪里执行都可用），根目录 = 本文件上两级
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from app.core.config import DB_NAME, SERVER_DATABASE_URL, SQLALCHEMY_DATABASE_URL  # noqa: E402
import app.models  # noqa: F401,E402  (注册全部模型)
from app.models.base import Base  # noqa: E402


def ensure_database() -> None:
    """connect without db and CREATE DATABASE ... if missing."""
    server = create_engine(SERVER_DATABASE_URL, isolation_level="AUTOCOMMIT")
    with server.connect() as conn:
        conn.execute(
            text(
                f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        )
        print(f"[ok] database `{DB_NAME}` ensured")
    server.dispose()


def create_tables(drop: bool = False) -> None:
    engine: Engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    if drop:
        print("[warn] dropping all tables ...")
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                "SELECT table_name, table_comment FROM information_schema.tables "
                "WHERE table_schema = :db ORDER BY table_name"
            ),
            {"db": DB_NAME},
        ).fetchall()
    print(f"[ok] {len(rows)} tables ready:")
    for name, comment in rows:
        print(f"   - {name}\t{comment}")
    engine.dispose()


if __name__ == "__main__":
    drop = "--drop" in sys.argv[1:]
    try:
        ensure_database()
        create_tables(drop=drop)
    except SQLAlchemyError as e:
        print(f"[fail] {e}")
        raise
