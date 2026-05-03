# EPCC — Engineering Standards
## Version 1.2 — Micro-Amendment (Changed Section Only)
**Owner:** System Architect / PMO Director
**Base Version:** EPCC_Engineering_Standards_v1_1.md
**Amendment Date:** 2026-05-02
**Scope:** ES-DR-002 updated — per-tenant schema backup added to daily backup procedure.
           Single change only. All other standards from v1.0 and v1.1 unchanged.
**Status:** Draft — Pending PMO Director Review | Locked: No

---

## CHANGE LOG

| Version | Date | Change Summary |
|---------|------|----------------|
| v1.0 | 2026-05-02 | Initial engineering standards locked. |
| v1.1 | 2026-05-02 | Gap analysis resolution — observability, DR, Alembic, CI/CD, DLQ, HDI staging, DPDPA 2023. |
| v1.2 | 2026-05-02 | **ES-DR-002 amended:** Per-tenant schema-level backup added to daily backup procedure. Closes the per-tenant restore gap identified in multi-EPC deployment analysis. ES-DB-001 (schema-per-tenant) confirmed and held. |

---

## SECTION 8 — DISASTER RECOVERY STANDARDS (Amendment)

### ES-DR-001: Recovery Objectives (Unchanged from v1.1)

*No change. RPO = 24hr, RTO = 4hr for Phase 1. See v1.1.*

---

### ES-DR-002: Backup Procedure (Updated — v1.2)

**Daily automated backup (Celery Beat — 2am IST):**

Two backup operations run in sequence every night:

```
OPERATION 1 — Full Instance Backup (unchanged from v1.1)
  1. pg_dump entire PostgreSQL instance (all schemas)
  2. Compress with gzip
  3. Upload to MinIO: backups/full/{date}/epcc_full_{timestamp}.sql.gz
  4. Verify checksum
  5. Delete full backups older than 30 days
  6. Log completion to SystemLog

OPERATION 2 — Per-Tenant Schema Backup (NEW — v1.2)
  For each active tenant in TenantMaster (is_active = true):
    1. pg_dump --schema=tenant_{slug} (single schema only)
    2. Compress with gzip
    3. Upload to MinIO: backups/tenants/{tenant_slug}/{date}/
                        {tenant_slug}_{timestamp}.sql.gz
    4. Verify checksum
    5. Delete per-tenant backups older than 90 days (longer retention
       than full backup — enables selective restore across 3 billing months)
    6. Log completion per tenant to SystemLog
  Alert System Admin if any per-tenant backup fails (even if full backup succeeded)
```

**Why two operations, not one:**

| Scenario | Full Instance Backup | Per-Tenant Schema Backup |
|---|---|---|
| Full system restore (catastrophic failure) | ✅ Use this — fastest full recovery | ❌ Too many files to reassemble |
| Single tenant data corruption or accidental deletion | ❌ Restoring full instance to fix one tenant's data affects all tenants | ✅ Use this — surgical restore of one schema |
| Tenant contractual right to their own data export | ❌ Cannot extract one tenant cleanly | ✅ Hand per-tenant file directly to client |
| Audit / legal hold for one tenant | ❌ Over-broad | ✅ Isolate one tenant's data without touching others |

**Per-Tenant Restore Procedure:**

```
Scenario: tenant_kdmc data corrupted. All other tenants unaffected.

1. Identify the correct per-tenant backup file from MinIO:
   backups/tenants/kdmc/{date}/kdmc_{timestamp}.sql.gz

2. Stop API + Worker containers (prevents further writes during restore)

3. Drop the corrupted schema:
   DROP SCHEMA tenant_kdmc CASCADE;

4. Create fresh empty schema:
   CREATE SCHEMA tenant_kdmc;

5. Restore from per-tenant backup:
   pg_restore --schema=tenant_kdmc kdmc_{timestamp}.sql.gz

6. Run Alembic migrate --schema=tenant_kdmc to bring schema to current
   migration head (if backup is behind HEAD)

7. Validate: run tenant health check script for tenant_kdmc only

8. Restart containers

9. Notify KDMC users: "System restored. Please verify your last 24hr
   of data entries."

10. Other tenants: ZERO impact. No downtime for other EPC firms.
```

**MinIO bucket structure (updated):**

```
epcc-backups/
├── full/
│   ├── 2026-05-01/
│   │   └── epcc_full_20260501_0200.sql.gz
│   └── 2026-05-02/
│       └── epcc_full_20260502_0200.sql.gz
└── tenants/
    ├── kdmc/
    │   ├── 2026-05-01/
    │   │   └── kdmc_20260501_0215.sql.gz
    │   └── 2026-05-02/
    │       └── kdmc_20260502_0215.sql.gz
    ├── apollohc/
    │   └── ...
    └── lginfra/
        └── ...
```

**Per-tenant backup timing:** Stagger starts by 5 minutes per tenant to avoid I/O contention.
First tenant starts at 2:10am IST (10 minutes after full backup starts).
With ≤50 tenants and staggered starts, all per-tenant backups complete before 5am IST.

**Retention policy:**

| Backup Type | Retention | Rationale |
|---|---|---|
| Full instance | 30 days | Covers one billing month. Operational recovery. |
| Per-tenant schema | 90 days | Covers one financial quarter. Contractual disputes may surface weeks after an event. |
| Weekly offsite (full) | 12 months | Annual audit and compliance. |

---

*All other sections from v1.0 and v1.1 remain fully in force.*
*This amendment adds one backup operation. It does not change ES-DB-001 (schema-per-tenant).*
*ES-DB-001 is confirmed, held, and closed.*
