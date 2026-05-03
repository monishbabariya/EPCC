"""Audit-log emission helper.

Round 25 scaffold: signature only. Real implementation lands in Round 27
when M34 SystemAuditLog table is created via Alembic.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID


async def emit(
    *,
    event_type: str,
    actor_user_id: UUID,
    tenant_id: UUID,
    entity_type: str,
    entity_id: UUID,
    before_value: dict[str, Any] | None = None,
    after_value: dict[str, Any] | None = None,
    request_id: str | None = None,
    ip: str | None = None,
    user_agent: str | None = None,
) -> UUID:
    """Append a row to system_audit_log; return the audit row id.

    Stub: replaced in Round 27 with the M34 implementation.
    """
    raise NotImplementedError("audit.emit is implemented in Round 27 (M34 thin slice)")
