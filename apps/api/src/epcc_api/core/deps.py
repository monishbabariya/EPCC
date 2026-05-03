"""Reusable FastAPI dependencies.

Round 25 scaffold: stubs only. `get_current_user` + `get_current_tenant`
become real in Round 27.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from epcc_api.core.db import get_session


async def db_session() -> AsyncIterator[AsyncSession]:
    async for session in get_session():
        yield session


SessionDep = Depends(db_session)
