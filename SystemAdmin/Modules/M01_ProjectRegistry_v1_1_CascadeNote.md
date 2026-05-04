# M01 — Project Registry
## v1.1 Cascade Note
**Status:** Cascade Patch
**Type:** Minor version bump (field addition only)
**Author:** Monish (with Claude assist)
**Created:** 2026-05-03 (Round 18 audit-driven backfill)
**Last Audited:** v1.1 on 2026-05-04 (Round 29 medium-cleanup — Format B field backfill, M29)
**Trigger:** M02 spec lock OQ-1.1=B — per-project, sector-driven minimum WBS depth
**Reference Standards:** X8_GlossaryENUMs_v0_4.md, M02_StructureWBS_Spec_v1_0.md
**Folder:** /02_L1_Command/

---

## CHANGE LOG

| Version | Date | Change Summary |
|---|---|---|
| v1.0 | 2026-05-03 | Initial standalone consolidated spec (Round 6) |
| **v1.1** | **2026-05-03** | **`Project.min_wbs_depth` field ADDED. Per-project, sector-driven minimum WBS depth per M02 OQ-1.1=B. Healthcare default = 4. PMO_DIRECTOR-only edit with justification ≥ 100 chars. Read by M02 BR-02-001 (depth validation on WBS create) and BR-02-032 (PMO edit + audit).** |

---

## NATURE OF v1.1 CHANGE

This is a **field addition cascade** — minor bump triggered by M02 spec lock decision OQ-1.1=B (locked Round 10).

**Why it surfaced now:** The audit pass following Round 18 lock identified that M02 BR-02-001 + BR-02-032 + Block 7 already reference `Project.min_wbs_depth` as if it exists, but M01 Spec v1.0 never defined it. This cascade note closes that architectural gap — M02 was treating an unsaid contract as locked. CLAUDE.md §3 had this listed as a pending cascade since Round 10; never executed until now.

### What Changes

| Aspect | Before (v1.0) | After (v1.1) |
|---|---|---|
| Field on `Project` entity | _(absent)_ | **`min_wbs_depth INTEGER NOT NULL DEFAULT 4`** |
| Validation | (none — M02 BR-02-001 had no field to read) | M02 BR-02-001 reads via M01 internal API on every WBS save |
| Edit authority | _(n/a)_ | PMO_DIRECTOR only (BR-01-035 added) |
| Justification | _(n/a)_ | ≥ 100 chars on edit (per M02 OQ-1.1=B lock) |
| Default at project create | _(n/a)_ | Sector-driven: `Hospital_DBOT` → 4; other sectors → CodeMaster lookup, fallback 3 |

### What Stays the Same

- All v1.0 fields and behaviour
- All v1.0 BRs
- M01 single-owner role unchanged

---

## CASCADE EXECUTION

### Schema Migration

```sql
-- Migration: 20260503_0034_m01_v1_1_add_min_wbs_depth.py

-- 1. Add column with sector-driven default
ALTER TABLE project
  ADD COLUMN min_wbs_depth INTEGER NOT NULL DEFAULT 4;

-- 2. Backfill non-healthcare projects from CodeMaster sector defaults
UPDATE project p
SET min_wbs_depth = COALESCE(
  (SELECT default_min_wbs_depth FROM code_master_sector
   WHERE code_master_sector.sector_code = p.sector_top_level),
  3  -- system-wide fallback if sector has no default
)
WHERE p.sector_top_level <> 'Hospital_DBOT';

-- 3. Add CHECK constraint (depth must be > 0; cap at 8 for sanity)
ALTER TABLE project
  ADD CONSTRAINT project_min_wbs_depth_range
  CHECK (min_wbs_depth BETWEEN 1 AND 8);
```

### New BR

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---|---|---|---|---|
| BR-01-035 | `Project.min_wbs_depth` edit | Caller role = PMO_DIRECTOR AND justification ≥ 100 chars AND M02 validates change does not violate existing WBS structure (delegated check via M02 internal API per F-005); audit log entry | Persist + audit; reject with reason if any check fails | 🔴 Real-time |

### API Changes

| Endpoint | Before | After |
|---|---|---|
| `GET /api/v1/projects/:id` | Response excludes `min_wbs_depth` | Response includes `min_wbs_depth` |
| `PATCH /api/v1/projects/:id` | Could not update min_wbs_depth (didn't exist) | PMO_DIRECTOR only; requires `min_wbs_depth_change_justification` (≥100 chars); validates with M02 |
| `GET /internal/v1/m01/projects/:id/min-wbs-depth` _(new)_ | _(n/a)_ | Returns current value for M02 BR-02-001 reads (single-owner F-005) |

### M01 Spec References Updated

The full M01 spec v1.0 (locked Round 6) requires the following minor edits when next re-issued (M01 v2.0):

| Block | Change |
|---|---|
| Block 3 — Entity: Project | Add `min_wbs_depth INT NOT NULL DEFAULT 4` field row with full data-architecture metadata |
| Block 4 — Data Population Rules | Add row: sector-driven default lookup at project create |
| Block 6 — Business Rules | Insert BR-01-035 (specified above) |
| Block 7 — Integration Points | Add: SENDS TO M02 — `min_wbs_depth` (WBS depth validation); already implicit via BR-02-001 reads |
| Block 8 — Governance and Audit | Add audit event row: `MIN_WBS_DEPTH_CHANGED` (Permanent retention; visible to PMO_DIR + PROJECT_DIR) |

**These edits are documented here as patch notes**; the M01 spec file v1.0 remains in place as the canonical pre-cascade reference. Build engineers read M01 v1.0 + this cascade note (+ v1.2 cascade note for `reporting_period_type` removal) for the current contract.

---

## DOWNSTREAM EFFECTS

| Module | Effect |
|---|---|
| M02 | **Already references** `Project.min_wbs_depth` in BR-02-001 + BR-02-032 + Block 7. No M02 spec change needed — this cascade note is the M01 side of an already-established contract. |
| M03 | None — schedule entries don't validate against WBS depth |
| M04 | None |
| M07 | None |
| All others | None |

---

## VERIFICATION CHECKLIST

```
[ ] Migration script tested on staging environment
[ ] Backfill from CodeMaster sector defaults populates correctly
[ ] CHECK constraint rejects out-of-range values
[ ] M01 internal API endpoint returns expected payload
[ ] M02 BR-02-001 successfully reads from M01 API
[ ] M02 BR-02-032 successfully PATCHes M01 with justification
[ ] PMO_DIRECTOR-only authorization enforced on edit
[ ] Audit event MIN_WBS_DEPTH_CHANGED emitted on edit
[ ] M01 spec v1.0 referenced + this cascade note attached
```

---

## RATIONALE FOR CASCADE NOTE FORMAT

Same as v1.2 cascade note: re-issuing the 700-line M01 spec for a single field addition is wasteful. This pattern matches the established practice (see `M01_ProjectRegistry_v1_2_CascadeNote.md`).

When 2–3+ cascades accumulate, M01 v2.0 re-issue becomes worthwhile. As of Round 18, M01 has v1.1 (this note, field addition) + v1.2 (cascade note, field removal) — both surgical, cascade-note-appropriate. M01 v2.0 deferred until further pressure.

---

*v1.1 — Cascade note locked. Closes the M02→M01 architectural gap surfaced in the Round 18 audit. Schema migration ready for build phase.*
