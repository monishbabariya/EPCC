"""Async SQLAlchemy engine + session factory.

Round 25 scaffold: engine wired to DATABASE_URL, no models registered yet.
RLS enforcement and reserved-fields mixin land in Round 27 with M34.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from epcc_api.core.config import settings

engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    echo=settings.env == "dev" and settings.api_log_level == "debug",
)

SessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all EPCC models."""


async def get_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency: yields an async session per request."""
    async with SessionLocal() as session:
        yield session
