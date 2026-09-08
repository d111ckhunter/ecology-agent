# -*- coding: utf-8 -*-
"""SQLAlchemy engine / session wiring."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import SQLALCHEMY_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    """FastAPI dependency: yield a session, always close it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
