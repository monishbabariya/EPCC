# M01 — Project Registry
## v1.4 Cascade Note
**Status:** Cascade Patch
**Type:** Reference propagation + role canonicalisation (no field add/remove, no BR change)
**Author:** Monish (with Claude assist)
**Created:** 2026-05-04
**Last Audited:** v1.4 on 2026-05-04 (Round 29 medium-cleanup — Format B field backfill, M29)
**Trigger:** Round 29 audit findings H13 (X8 ENUM section refs missing) + H16 (Block 4a permission matrix uses truncated role names + missing canonical roles)
**Parent Spec:** M01_ProjectRegistry_Spec_v1_0.md
**Reference Standards:** X8_GlossaryENUMs_v0_6.md (v0.6a), X9_VisualisationStandards_Spec_v0_4.md, M34_SystemAdminRBAC_Spec_v1_0.md (Block 3 — canonical 17-role taxonomy), .claude/rules/cross-cutting-standards.md
**Folder:** SystemAdmin/Modules/

---

## CHANGE LOG

| Version | Date | Change Summary |
|---|---|---|
| v1.0 | 2026-05-03 | Initial standalone consolidated spec (Round 6) |
| v1.1 | 2026-05-03 (backfilled Round 18 audit) | `Project.min_wbs_depth` field addition per M02 OQ-1.1=B. See `M01_ProjectRegistry_v1_1_CascadeNote.md`. |
| v1.2 | 2026-05-03 | `Project.reporting_period_type` field REMOVED. Ownership → M03 LookAheadConfig. See `M01_ProjectRegistry_v1_2_CascadeNote.md`. |
| v1.3 | 2026-05-04 | `Contract.dlp_retention_split_pct` field ADDED + BR-01-036. Driven by M06 OQ-1.8=C. See `M01_ProjectRegistry_v1_3_CascadeNote.md`. |
| **v1.4** | **2026-05-04** | **H13: X8 §section refs added to 8 M01-owned ENUM fields in Block 3b. H16: Block 4a permission matrix role names canonicalised (3 truncated labels) + ANALYST + EXTERNAL_AUDITOR rows added. No field, BR, or entity change.** |

---

## NATURE OF v1.4 CHANGE

Two finding-class fixes bundled into one cascade note because both are non-substantive reference propagation — neither adds a field, removes a field, or changes any locked decision. Per spec-protocol §Cascade-vs-Re-issue, this is the cascade-note vehicle (not re-issue).

---

## H13 — ENUM Field X8 Reference Propagation

The following 8 fields in M01 Spec v1.0 Block 3b use ENUM types but lack the canonical `→ X8 §section` reference per the X8 anti-drift rule. **No ENUM values changed — references only.**

X8 §section numbers verified against `SystemAdmin/Cross-link files/X8_GlossaryENUMs_v0_2.md` (the version that introduced these M01-owned ENUMs).

| # | Field | Entity | ENUM Name | X8 Reference |
|---|---|---|---|---|
| 1 | `party_type` | ProjectParty | `PartyType` | → X8 §3.19 |
| 2 | `party_role` | ProjectParty | `PartyRole` | → X8 §3.20 |
| 3 | `contract_role` | ContractParty | `ContractRole` | → X8 §3.21 |
| 4 | `contract_type` | Contract | `ContractType` | → X8 §3.22 |
| 5 | `scenario_active` | ProjectScenario | `ScenarioActive` | → X8 §3.23 |
| 6 | `kpi_name` | ProjectKPI | `KPIName` | → X8 §3.24 |
| 7 | `kpi_direction` | ProjectKPI | `KPIDirection` | → X8 §3.25 |
| 8 | `region` | Project _(via PincodeMaster)_ | `Region` | → X8 §3.26 |

**Application:** when reading M01 Spec v1.0 Block 3b, apply these references to the corresponding field rows. Field types, constraints, and ENUM values are unchanged.

**Already-referenced ENUMs (no patch required):** `Phase` (§3.9), `ProjectStatus` (§3.8), `SectorTopLevel` (§3.16a), `DeliveryModel` (§3.18). These were introduced with X8 references in v1.0 and remain accurate.

---

## H16 — Block 4a Permission Matrix Canonicalisation + Missing Roles

M01 Spec v1.0 Block 4a permission matrix (line 422) uses **truncated** role names that do not match the canonical UPPER_SNAKE_CASE 17-role taxonomy (M34 Spec Block 3, also indexed in `.claude/rules/cross-cutting-standards.md`).

### Substitution Table — Apply When Reading Block 4a

| Block 4a label (line 422) | Canonical name (M34 Block 3) | Notes |
|---|---|---|
| `PORTFOLIO_MGR` | `PORTFOLIO_MANAGER` | Truncated — name only, semantics unchanged |
| `PROJECT_DIR` | `PROJECT_DIRECTOR` | Truncated — name only, semantics unchanged |
| `OTHERS` | _(context-dependent — see below)_ | Bucket — collapses 6 internal roles |

**`OTHERS` bucket — composition (per M34 Block 3 + `cross-cutting-standards.md` §17 Canonical Roles):**

The `OTHERS` column collapses these 6 canonical roles, all with the same default M01 permission posture as represented:
- `PLANNING_ENGINEER`
- `QS_MANAGER`
- `PROCUREMENT_OFFICER`
- `SITE_MANAGER`
- `COMPLIANCE_MANAGER`
- `ANALYST` _(applied here per H16 — see row addition below)_

When reading Block 4a, treat each `OTHERS` cell as applying uniformly to all 6 of the above. Where a specific role needs a different value (e.g., `PROCUREMENT_OFFICER` having explicit contract-read privilege per Brief §6), the existing `OTHERS = ✗ except contract read` annotations in Block 4a apply.

### Missing Canonical Roles — Row Additions

M01 Spec v1.0 Block 4a omits two canonical roles. Both are read-only consumers of M01 data and do not appear in the existing matrix at all. Append these rows:

| Role | All M01 Actions | Notes |
|---|---|---|
| `ANALYST` | View only (read + filter + export — same posture as `READ_ONLY`); ✗ on all CRUD | Added Round 18 audit; canonical 17-role list. Mirrors `READ_ONLY` but with explicit data-export privilege per `cross-cutting-standards.md` Spike Formula Role Mapping. |
| `EXTERNAL_AUDITOR` | View only on project metadata + stage gate history; ✗ on all CRUD | Added Round 18 audit; canonical 17-role list. MFA-required per M34 Block 3. Phase-2-gated by PF03 ExternalPartyPortal for cross-tenant access; in-tenant audit access available in v1.0. |

**No existing row permissions changed.** No BR-01-* changed. Block 4a's column structure (SYSTEM_ADMIN | PMO_DIRECTOR | PORTFOLIO_MGR | PROJECT_DIR | FINANCE_LEAD | OTHERS | READ_ONLY) is preserved verbatim — the two new rows extend the role inventory beneath it.

---

## DOWNSTREAM IMPACT

- **No M02/M03/M04/M06 cascade required.** Their RBAC matrices reference roles by name; this cascade does not change role names, only adds canonical references for two roles that already exist in M34's source-of-truth ENUM.
- **No code impact** (Phase 1 spec-only; no implementation yet).
- **VersionLog §3.4 M01 row** should reference v1.4 cascade note when the medium-cleanup branch lands (deferred to `audit/round-29-medium-cleanup`).

---

*Cascade note v1.4 — LOCKED 2026-05-04 — Round 29 audit. No re-issue required (per spec-protocol.md §Cascade-vs-Re-issue: 0 fields added, 0 BRs changed, scope unchanged).*
