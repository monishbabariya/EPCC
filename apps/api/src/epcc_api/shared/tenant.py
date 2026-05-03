"""Tenant_id middleware + RLS session-variable setter.

Round 25 scaffold: signature only. Real implementation lands in Round 27.
Per `EPCC_BuildArchitecture_Spec_v1_0.md` §4.3, RLS policy on every
tenant-scoped table reads `current_setting('epcc.tenant_id')::uuid`.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession


async def set_tenant_for_session(session: AsyncSession, tenant_id: UUID) -> None:
    """Set per-request tenant_id on the Postgres session.

    Stub: replaced in Round 27.
    """
    raise NotImplementedError(
        "set_tenant_for_session is implemented in Round 27 (M34 thin slice)"
    )
