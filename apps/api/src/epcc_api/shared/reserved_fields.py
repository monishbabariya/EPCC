"""Reserved-fields mixin per X8 §6 + naming-folders.md.

The 6 reserved columns: tenant_id, created_by, created_at, updated_by,
updated_at, is_active.

Append-only ledgers (BACIntegrityLedger, IDGovernanceLog, CSVImportRecord,
ProjectPhaseHistory, ProjectStatusHistory, LoginAttempt, SystemAuditLog,
M04 4 ledgers) are exempt and use a different mixin pattern (Round 27+).

Round 25 scaffold: stub. Implementation lands in Round 27 once Postgres
extensions + Base are exercised by the first M34 migration.
"""

from __future__ import annotations
