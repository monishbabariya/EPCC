# M01 — Project Registry
## v1.2 Cascade Note
**Status:** Cascade Patch
**Type:** Minor version bump (field removal only)
**Author:** PMO Director / System Architect
**Created:** 2026-05-03
**Trigger:** M03 spec lock OQ-1.8=A (reporting_period_type ownership shifts to M03)
**Reference Standards:** X8_GlossaryENUMs_v0_4.md, M03_PlanningMilestones_Spec_v1_0.md
**Folder:** /02_L1_Command/

---

## CHANGE LOG

| Version | Date | Change Summary |
|---|---|---|
| v1.0 | 2026-05-03 | Initial standalone consolidated spec (Round 6) |
| v1.1 | (deferred) | `Project.min_wbs_depth` field addition per M02 OQ-1.1=B |
| **v1.2** | **2026-05-03** | **`Project.reporting_period_type` field REMOVED. Ownership shifts to M03 LookAheadConfig.reporting_period_type. M01 reads via API per Single-Owner rule (F-005).** |

---

## NATURE OF v1.2 CHANGE

This is a **field removal cascade** — minor bump triggered by M03 spec lock decision OQ-1.8=A.

### What Changes

| Aspect | Before (v1.1) | After (v1.2) |
|---|---|---|
| Field location | `Project.reporting_period_type` (M01) | `LookAheadConfig.reporting_period_type` (M03) |
| Ownership module | M01 | **M03** |
| API access | Direct field read on Project entity | Read via M03 internal API |
| ENUM ownership | M01 (legacy ambiguity) | **M03** (X8 §3.43 reassigned) |

### What Stays the Same

- ENUM values: `Monthly`, `Weekly`, `Daily`, `Event_Driven` (4 values, X8 §3.43 unchanged)
- Default value: `Monthly`
- Project staleness calculation logic (still uses reporting_period_type, but reads from M03)
- All other M01 fields and behaviour
- All other M01 BRs

---

## CASCADE EXECUTION

### Schema Migration

```sql
-- Migration: 20260503_0032_m01_v1_2_remove_reporting_period.py

-- 1. Backfill LookAheadConfig with current Project.reporting_period_type values
INSERT INTO look_ahead_config (
    config_id, tenant_id, project_id, look_ahead_weeks, reporting_period_type,
    created_at, updated_at
)
SELECT
    gen_random_uuid(),
    tenant_id,
    project_id,
    4,  -- Default look-ahead 4 weeks
    reporting_period_type,
    NOW(),
    NOW()
FROM project
WHERE NOT EXISTS (
    SELECT 1 FROM look_ahead_config WHERE look_ahead_config.project_id = project.project_id
);

-- 2. Drop the column from Project
ALTER TABLE project DROP COLUMN reporting_period_type;
```

### API Changes

| Endpoint | Before | After |
|---|---|---|
| `GET /api/v1/projects/:id` | Returns `reporting_period_type` field in response | Field removed; client must call M03 endpoint |
| `GET /internal/v1/m03/projects/:id/reporting-period` | (new) | Returns `reporting_period_type` from LookAheadConfig |
| `PATCH /api/v1/projects/:id` | Could update `reporting_period_type` | Cannot — must use M03 endpoint |
| `PATCH /api/v1/projects/:id/look-ahead-config` (M03 endpoint) | (new in M03 spec) | Updates reporting_period_type with audit trail |

### M01 Spec References Updated

The full M01 spec v1.0 (locked Round 6) requires the following minor edits when next re-issued:

| Block | Change |
|---|---|
| Block 3 — Entity: Project | Remove `reporting_period_type` field row |
| Block 6 — Business Rules | BR referencing project staleness now reads via M03 API call |
| Block 7 — Integration Points | Add: RECEIVES FROM M03 — reporting_period_type (project staleness calc) |
| Block 9 — Explicit Exclusions | Add: "reporting_period_type ownership → M03 LookAheadConfig" |

**These edits are documented here as patch notes**; the M01 spec file v1.0 remains in place as the canonical pre-cascade reference. A consolidated M01 v1.2 spec re-issue can be done in a future round if needed (low priority — patch notes are sufficient for build).

---

## RATIONALE FOR CASCADE NOTE FORMAT

Re-issuing the entire 700-line M01 spec for a single field removal would be wasteful. This cascade note follows the same pattern as Anthropic engineering practice for surgical schema changes:

- **Single source of truth:** This document describes the v1.0 → v1.2 delta exactly
- **Audit trail:** Migration script + before/after fields + API impact documented
- **Build-ready:** Engineers implementing v1.2 read M01 v1.0 + this cascade note
- **Future re-issue option:** When M01 v2.0 is needed (major changes), v1.2 changes will be incorporated

---

## DOWNSTREAM EFFECTS

| Module | Effect |
|---|---|
| M02 | None — never read reporting_period_type |
| M03 | Now owns the field (LookAheadConfig.reporting_period_type) |
| M04 | Reads reporting_period_type via M03 API for progress reporting cadence |
| M05 | Reads via M03 API for VO impact periodisation |
| M06 | Reads via M03 API for cashflow forecast period boundaries |
| M07 | Reads via M03 API for EVM period boundaries |
| M08 | Reads via M03 API for gate review cadence |
| M10 | Reads via M03 API for dashboard refresh |

All downstream modules query M03's internal API endpoint:

```
GET /internal/v1/m03/projects/:id/reporting-period
Response: { reporting_period_type: "Monthly", look_ahead_weeks: 4, ... }
```

---

## VERIFICATION CHECKLIST

```
[ ] Migration script tested on staging environment
[ ] Backfill of LookAheadConfig populates correctly from Project values
[ ] Project.reporting_period_type column dropped successfully
[ ] M03 internal API endpoint returns expected payload
[ ] Existing API consumers updated to query M03 endpoint
[ ] M01 spec v1.0 referenced + this cascade note attached
[ ] X8 §3.43 ownership clarified (M03 owns)
[ ] Audit log: SCHEMA_MIGRATION_M01_V1_2_REPORTING_PERIOD_REMOVED
```

---

## PENDING M01 CASCADES

For tracking — pending M01 cascades that should be consolidated into M01 v2.0 when re-issued:

| Pending | Source | Status |
|---|---|---|
| Add `Project.min_wbs_depth` field | M02 OQ-1.1=B | Deferred (cascade note exists) |
| Remove `Project.reporting_period_type` | M03 OQ-1.8=A | **This document** |

When 2-3+ cascades accumulate, M01 v2.0 re-issue becomes worthwhile. For now, cascade notes are the contained, auditable approach.

---

*v1.2 — Cascade note locked. Schema migration ready for build phase.*
