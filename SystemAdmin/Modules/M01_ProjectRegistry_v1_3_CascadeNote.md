# M01 — Project Registry
## v1.3 Cascade Note
**Status:** Cascade Patch
**Type:** Minor version bump (field addition + 1 BR)
**Author:** Monish (with Claude assist)
**Created:** 2026-05-04
**Trigger:** M06 spec lock OQ-1.8=C (tranched retention release at SG-9 + SG-11; per-contract split percentage required)
**Reference Standards:** X8_GlossaryENUMs_v0_6.md, M06_FinancialControl_Spec_v1_0.md (v1.0a), M06_FinancialControl_Workflows_v1_0.md
**Folder:** SystemAdmin/Modules/

---

## CHANGE LOG

| Version | Date | Change Summary |
|---|---|---|
| v1.0 | 2026-05-03 | Initial standalone consolidated spec (Round 6) |
| v1.1 | 2026-05-03 (backfilled in Round 18 audit) | `Project.min_wbs_depth` field addition per M02 OQ-1.1=B. See `M01_ProjectRegistry_v1_1_CascadeNote.md`. |
| v1.2 | 2026-05-03 | `Project.reporting_period_type` field REMOVED. Ownership shifts to M03 LookAheadConfig.reporting_period_type. See `M01_ProjectRegistry_v1_2_CascadeNote.md`. |
| **v1.3** | **2026-05-04** | **`Contract.dlp_retention_split_pct DECIMAL(5,4) DEFAULT 0.5000` field ADDED + new `BR-01-036` (PMO_DIRECTOR-edit only with justification ≥100 chars). Required by M06 BR-06-027 + BR-06-045 to compute tranche-1 retention release at SG-9 passage.** |

---

## NATURE OF v1.3 CHANGE

This is a **field addition + 1 BR cascade** — minor bump triggered by M06 Brief OQ-1.8=C (tranched retention release).

### What Changes

| Aspect | Before (v1.2) | After (v1.3) |
|---|---|---|
| Contract entity | No retention split field — M06 must hardcode 50/50 default per project | New field `dlp_retention_split_pct DECIMAL(5,4) DEFAULT 0.5000` (range 0.0001–0.9999) |
| Tranche-1 release amount | Implicit (M06-derived) | Explicit on M01 Contract — single-owner read |
| Edit governance | n/a | New BR-01-036 — only `PMO_DIRECTOR` may edit; justification text ≥ 100 chars; emit `CONTRACT_DLP_SPLIT_EDITED` audit event |

### What Stays the Same

- All other Contract fields and behaviour
- All other M01 BRs (BR-01-001 through BR-01-035)
- API surface — only adds `dlp_retention_split_pct` to existing GET response shapes; no new endpoints required
- Reserved fields (Contract is NOT append-only — already includes `tenant_id, created_by, created_at, updated_by, updated_at, is_active` per X8 §6)

---

## CASCADE EXECUTION

### Schema Migration

```sql
-- Migration: 20260504_0001_m01_v1_3_add_dlp_retention_split.py

-- 1. Add column with default 0.5000 (50% split — common DBOT default)
ALTER TABLE contract
  ADD COLUMN dlp_retention_split_pct DECIMAL(5,4) NOT NULL DEFAULT 0.5000
    CHECK (dlp_retention_split_pct > 0.0000 AND dlp_retention_split_pct < 1.0000);

-- 2. Backfill existing contracts with 0.5000 (default split)
-- (handled by DEFAULT clause on row insert; no explicit UPDATE needed)

-- 3. Add audit trigger for edits (BR-01-036 enforcement at app layer; trigger emits log row)
-- Application layer enforces:
--   * RBAC: only PMO_DIRECTOR may UPDATE this column
--   * Justification: edit_reason TEXT ≥ 100 chars required in same transaction
--   * Audit emit: CONTRACT_DLP_SPLIT_EDITED with old/new values
```

### New Business Rule — BR-01-036

**Rule:** `Contract.dlp_retention_split_pct` is editable only by `PMO_DIRECTOR`. Edit requires `edit_reason ≥ 100 chars` captured in the same API transaction. On commit, emit `CONTRACT_DLP_SPLIT_EDITED` audit event with `{contract_id, old_value, new_value, edited_by, edit_reason, edited_at}` payload.

**Trigger:** PATCH `/api/v1/contracts/:id` with `dlp_retention_split_pct` in request body.

**Validation chain:**
1. Caller role must be `PMO_DIRECTOR` (else `403 FORBIDDEN`)
2. `dlp_retention_split_pct` ∈ (0.0000, 1.0000) exclusive (else `400 VALIDATION_ERROR`)
3. `edit_reason` length ≥ 100 chars (else `400 JUSTIFICATION_TOO_SHORT`)
4. On success: emit audit event + return updated Contract DTO

**Cascade impact:** M06 BR-06-027 reads this value to compute `tranche_1_release_amount = retention_accumulated × dlp_retention_split_pct`. M06 BR-06-028 derives `tranche_2_release_amount = retention_accumulated − tranche_1_release_amount`.

### API Changes

| Endpoint | Before | After |
|---|---|---|
| `GET /api/v1/contracts/:id` | Returns Contract DTO without retention split | Returns Contract DTO **with** `dlp_retention_split_pct` field |
| `PATCH /api/v1/contracts/:id` | Allowed any contract field PATCH per existing RBAC | New: `dlp_retention_split_pct` editable by `PMO_DIRECTOR` only with `edit_reason` ≥ 100 chars |
| `GET /internal/v1/m01/contracts/:id` | Internal read (M02–M07 consumers) | Same response now includes `dlp_retention_split_pct` |

### M01 Spec References Updated

The full M01 spec v1.0 (locked Round 6) requires the following minor edits when next re-issued:

| Block | Change |
|---|---|
| Block 3 — Entity: Contract | Add `dlp_retention_split_pct` field row (DECIMAL(5,4) NOT NULL DEFAULT 0.5000, CHECK > 0 AND < 1) |
| Block 6 — Business Rules | Add BR-01-036 — PMO-only edit with justification ≥ 100 chars |
| Block 7 — Integration Points | Add: SENDS TO M06 — `dlp_retention_split_pct` (consumed by BR-06-027 + BR-06-045) |
| Block 8 — Audit catalogue | Add: `CONTRACT_DLP_SPLIT_EDITED` audit event |
| Appendix A (audit events) | Append `CONTRACT_DLP_SPLIT_EDITED` |

**These edits are documented here as patch notes**; the M01 spec file v1.0 remains in place as the canonical pre-cascade reference. A consolidated M01 v2.0 spec re-issue can be done in a future round if needed (low priority — patch notes sufficient for build).

---

## RATIONALE FOR CASCADE NOTE FORMAT

Per `spec-protocol.md` Round 18 audit cascade-vs-re-issue rule:

- **1 small change (1 field add + 1 BR addition, scope unchanged)** → cascade note (this document)
- **NOT a substantive change** (no new appendix, no new entity, no scope shift)

Pattern precedent: `M01_ProjectRegistry_v1_1_CascadeNote.md` (`min_wbs_depth` field add) + `M01_ProjectRegistry_v1_2_CascadeNote.md` (`reporting_period_type` field remove). v1.3 follows the same surgical-cascade pattern.

---

## DOWNSTREAM EFFECTS

| Module | Effect |
|---|---|
| M02 | None — never reads `dlp_retention_split_pct` |
| M03 | None |
| M04 | None |
| M05 | None — VO impact unchanged (split only affects retention release timing) |
| **M06** | **Consumes `dlp_retention_split_pct` via internal API for BR-06-027 (tranche-1 amount at SG-9) and BR-06-045 (consistency check on tranche-2 amount at SG-11)** |
| M07 | None — EVM unaffected |
| M08 | Reads at gate review (informational only — confirms split percentage at SG-9 / SG-11 readiness checks) |
| M23 | (Phase 2) — BG migration consumes for retention-substitute BG sizing |

All downstream modules query M01's internal API:

```
GET /internal/v1/m01/contracts/:id
Response: { contract_id, ..., dlp_retention_split_pct: 0.5000, ... }
```

---

## VERIFICATION CHECKLIST

```
[ ] Migration script tested on staging environment
[ ] DEFAULT 0.5000 backfills correctly on row insert
[ ] CHECK constraint rejects 0.0000 and 1.0000 (must be exclusive)
[ ] Application layer enforces PMO_DIRECTOR-only edit
[ ] Application layer enforces edit_reason ≥ 100 chars
[ ] CONTRACT_DLP_SPLIT_EDITED audit event emits with correct payload
[ ] M01 spec v1.0 referenced + this cascade note attached
[ ] X8 §3.10 SG_9/SG_11 description refresh consumed (v0.6)
[ ] M06 BR-06-027 reads from M01 API (not hardcoded)
[ ] M06 BR-06-045 cross-validates tranche-2 amount via API call
```

---

## PENDING M01 CASCADES

For tracking — pending M01 cascades that should be consolidated into M01 v2.0 when re-issued:

| Pending | Source | Status |
|---|---|---|
| Add `Project.min_wbs_depth` field | M02 OQ-1.1=B | **DONE** — `M01_ProjectRegistry_v1_1_CascadeNote.md` (Round 18 audit backfill) |
| Remove `Project.reporting_period_type` | M03 OQ-1.8=A | **DONE** — `M01_ProjectRegistry_v1_2_CascadeNote.md` |
| Add `Contract.dlp_retention_split_pct` + BR-01-036 | M06 OQ-1.8=C | **This document** |

3 cascades now accumulated. M01 v2.0 re-issue threshold approaching. For now, cascade notes remain the contained, auditable approach.

---

*v1.3 — Cascade note locked. Schema migration ready for build phase. M06 v1.0 consumption pre-wired (BR-06-027, BR-06-045).*
