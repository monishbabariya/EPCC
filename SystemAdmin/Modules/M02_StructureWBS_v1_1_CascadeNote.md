# M02 — Structure & WBS
## v1.1 Cascade Note
**Status:** Cascade Patch
**Type:** Reference propagation (H12) + role row addition to rate-display matrix (H14, also extends BR-02-008)
**Author:** Monish (with Claude assist)
**Created:** 2026-05-04
**Trigger:** Round 29 audit findings H12 (X8 ENUM section refs missing on 11 fields) + H14 (ANALYST missing from rate-display matrix; canonical role since R18 audit)
**Parent Spec:** M02_StructureWBS_Spec_v1_0.md
**Reference Standards:** X8_GlossaryENUMs_v0_6.md (v0.6a), X9_VisualisationStandards_Spec_v0_4.md, M34_SystemAdminRBAC_Spec_v1_0.md (Block 3), .claude/rules/cross-cutting-standards.md (§Spike Formula Role Mapping)
**Folder:** SystemAdmin/Modules/

---

## CHANGE LOG

| Version | Date | Change Summary |
|---|---|---|
| v1.0 | 2026-05-03 | Initial standalone consolidated spec (Round 10). 11 entities, BAC integrity ledger (append-only, DB-level UPDATE/DELETE forbidden), 3-tier rate spike formula matrix per role, three-tier package templates (copy-down only). |
| **v1.1** | **2026-05-04** | **H12: X8 §section refs added to 11 M02-owned ENUM fields in Block 3b. H14: ANALYST row added to Block 5 rate-display matrix and BR-02-008. No field, entity, or invariant change.** |

---

## NATURE OF v1.1 CHANGE

Two non-substantive fixes bundled into one cascade note:
- **H12** — pure reference propagation (no ENUM values, no field types, no constraints changed)
- **H14** — extends an existing matrix and one BR with one new role row; no existing role permission changed

Per spec-protocol §Cascade-vs-Re-issue: this is the cascade-note vehicle (not re-issue) — 0 fields added/removed, 0 entities changed, only matrix row addition + BR-02-008 single-row extension.

---

## H12 — ENUM Field X8 Reference Propagation

The following 11 fields in M02 Spec v1.0 Block 3b use ENUM types but lack the canonical `→ X8 §section` reference per the X8 anti-drift rule. **No ENUM values changed — references only.**

X8 §section numbers verified against `SystemAdmin/Cross-link files/X8_GlossaryENUMs_v0_3.md` (the version that introduced these M02-owned ENUMs).

| # | Field | Entity | ENUM Name | X8 Reference |
|---|---|---|---|---|
| 1 | `bac_integrity_status` | BACIntegrityLedger | `BACIntegrityStatus` | → X8 §3.27 |
| 2 | `boq_origin` | BOQLineItem | `BOQOrigin` | → X8 §3.28 |
| 3 | `bac_change_type` | BACChangeRecord | `BACChangeType` | → X8 §3.31 |
| 4 | `unit_tier` | RateCard / Unit | `UnitTier` | → X8 §3.32 |
| 5 | `unit_category` | RateCard / Unit | `UnitCategory` | → X8 §3.33 |
| 6 | `unit_system` | RateCard / Unit | `UnitSystem` | → X8 §3.34 |
| 7 | `package_type` | PackageTemplate | `PackageType` | → X8 §3.35 |
| 8 | `chain_validation_status` | WBSNode | `ChainValidationStatus` | → X8 §3.36 |
| 9 | `csv_import_mode` | CSVImportRecord | `CSVImportMode` | → X8 §3.37 |
| 10 | `csv_import_target` | CSVImportRecord | `CSVImportTarget` | → X8 §3.38 |
| 11 | `csv_import_record_action` | CSVImportRecord | `CSVImportRecordAction` | → X8 §3.39 |

**Already-referenced ENUMs (no patch required):** `BOQRateSpikeFormula` (§3.29), `PackageTemplateTier` (§3.30). These were introduced with X8 references in v1.0 and remain accurate.

**Application:** when reading M02 Spec v1.0 Block 3b, apply these references to the corresponding field rows. Field types, constraints, and ENUM values are unchanged.

---

## H14 — ANALYST Row Added to Rate-Display Matrix + BR-02-008

ANALYST was added to the canonical 17-role list in the R18 audit but was not propagated to M02 Spec v1.0 Block 5 spike formula role matrix (line 461-466) or BR-02-008 (rate spike formula enforcement at API serialiser).

### Block 5 Rate-Display Matrix — Row Addition

Append the following row to M02 Spec v1.0 Block 5 spike formula matrix (after line 465 `PLANNING_ENGINEER, QS_MANAGER` row, before line 466 `SITE_MANAGER, READ_ONLY` row, to keep the Indexed-tier rows grouped):

| Role | Formula | Display Result |
|---|---|---|
| `ANALYST` | `Indexed` | Rate × indexing factor (CPI-style; tenant-configurable, default +8% via `M02_INDEXED_FACTOR` feature flag) |

**Rationale:** ANALYST is an analytical / planning-adjacent role (closer to `PLANNING_ENGINEER` than to `SITE_MANAGER` or `READ_ONLY`). The Indexed formula is consistent with `cross-cutting-standards.md` §Spike Formula Role Mapping, where `PLANNING_ENGINEER` and `QS_MANAGER` already share `Indexed × 1.08`. This grouping reflects the role's data-trend orientation: ANALYST sees indexed (CPI-adjusted) rates for trend analysis, not the raw actual rates that finance roles need.

**No existing rows changed.** The matrix grows from 4 rows to 5 rows.

### BR-02-008 Extension

BR-02-008 governs rate spike formula enforcement by role at the API serialiser layer (per M02 OQ-2.11 lock). Append `ANALYST | Indexed | × 1.08 (default)` to the BR-02-008 rule table.

**Enforcement mechanism unchanged:** API serialiser applies the per-role formula before returning rate data; client never sees raw rate for non-`None` formula roles. Tenant override of indexed factor remains via `M02_INDEXED_FACTOR` feature flag (M34-owned).

---

## DOWNSTREAM IMPACT

- **`cross-cutting-standards.md` §Spike Formula Role Mapping** — already accurate (does not list ANALYST). No edit required in this round; the table is descriptive, not prescriptive. Would benefit from an ANALYST row addition in `audit/round-29-medium-cleanup` for parity, but not blocking.
- **No M01/M03/M04/M06 cascade required.** Other modules don't redefine M02's rate-display logic.
- **No code impact** (Phase 1 spec-only).
- **VersionLog §3.5 M02 row** should reference v1.1 cascade note when medium-cleanup branch lands (deferred).

---

*Cascade note v1.1 — LOCKED 2026-05-04 — Round 29 audit. No re-issue required (per spec-protocol.md §Cascade-vs-Re-issue: 0 fields added, 0 BRs newly created, scope unchanged — single existing BR's role table extended).*
