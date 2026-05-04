# EPCC Naming Conventions & Folder Structure — LOCKED

> **Purpose:** Single source of truth for file naming, identifier conventions, and folder hierarchy. Authoritative reference: `System Specs/EPCC_NamingConvention_v1_0.md` and `System Specs/EPCC_FolderIndex_v1_0.md`.

---

## File Naming Convention

```
{Prefix}_{ShortName}_{ArtefactType}_v{Major}_{Minor}.{ext}

Examples:
- M01_ProjectRegistry_Spec_v1_0.md
- M02_StructureWBS_Wireframes_v1_0.html
- X8_GlossaryENUMs_v0_3.md
```

---

## Naming Rules (X8 §2)

| Concept | Convention | Example |
|---|---|---|
| ENUM type name | PascalCase | `BACIntegrityStatus` |
| ENUM values (system) | UPPER_SNAKE_CASE | `SYSTEM_ADMIN` |
| ENUM values (status) | Pascal_Snake_Case | `Stale_Pending_VO` |
| Severity / RAG | Pascal single word | `Critical` / `Green` |
| Permission codes | lower_snake_case | `view_project` |
| Role codes | UPPER_SNAKE_CASE | `PMO_DIRECTOR` |
| Field names | lower_snake_case | `user_id` |
| BR codes | `BR-{module}-{seq}` | `BR-01-010` |
| Decision Queue triggers | UPPER_SNAKE_CASE | `BAC_VS_CONTRACT_DEVIATION` |
| Audit event types | UPPER_SNAKE_CASE | `LOGIN_SUCCESS` |

---

## Reserved Fields (X8 §6)

Every entity (except append-only logs and junction tables) MUST include:

```
tenant_id, created_by, created_at, updated_by, updated_at, is_active
```

### Append-only exemptions (no soft delete, no `updated_*`)

- `BACIntegrityLedger` (M02) — DB-level UPDATE/DELETE forbidden
- `IDGovernanceLog` (M02)
- `CSVImportRecord` (M02)
- `ProjectPhaseHistory` (M01)
- `ProjectStatusHistory` (M01)
- `LoginAttempt` (M34)
- `SystemAuditLog` (M34)
- `Baseline` (M03) — sealed at SG-6; immutable after lock
- `BaselineExtension` (M03) — append-only after approval
- `PVProfileSnapshot` (M03) — historical snapshots immutable
- `ProgressEntryAudit` (M04) — every state transition; UPDATE/DELETE forbidden at DB level
- `NCRStatusLog` (M04) — every NCR transition + severity change
- `MaterialReceiptLedger` (M04) — every QC decision + receipt event
- `ContractorPerformanceScoreLog` (M04) — every score recompute / override
- `CostLedgerEntry` (M06) — 4-state transitions Budgeted→Committed→Accrued→Paid; reversals via compensating entries only
- `RABillAuditLog` (M06) — every RA Bill state change
- `PaymentEvidenceLedger` (M06) — every PaymentEvidence packet event
- `ForexRateLog` (M06) — every rate entry + lock event; per-tier (RBI_Reference / Bank_Transaction)

> **Source of truth:** X8 §6 (current v0.6). This list mirrors X8 — when X8 §6 grows, update here in the same cascade.

---

## Folder Placement — Canonical (locked Round 18 audit)

**Active artefacts (Phase 1 build):**

```
SystemAdmin/
  M34_SystemAdminRBAC_Spec_v1_0.md          # M34 Spec sits one level up (legacy artefact placement)
  M34_SystemAdminRBAC_Wireframes_v1_0.html
  Modules/                                   # all module Briefs / Specs / Wireframes / Workflows for M01+
    M0X_*.{md,html}
    M0X_*_v1_X_CascadeNote.md                # cascade notes co-located with their source module
  Cross-link files/                          # X-series living docs
    X8_GlossaryENUMs_v0_X.md
    X9_VisualisationStandards_*_v0_X.md
System Specs/                                # governance, naming, version log, audits
  EPCC_*.md
  AUDIT_*.md
ZEPCC_Legacy/                                # frozen prior-version artefacts (read-only reference)
  M0X_*.md
```

**Convention:**
- Active modules (M01+) live in `SystemAdmin/Modules/`
- M34 was authored before this convention; its Spec stays at `SystemAdmin/` (no rename — would break references)
- Cascade notes (`_v1_X_CascadeNote.md`) sit beside their source module
- Cross-cutting living docs go in `SystemAdmin/Cross-link files/`
- Governance + audits go in `System Specs/`
- Legacy is `ZEPCC_Legacy/` — frozen, read-only, naming-convention-exempt

## 13-Folder Hierarchy — Aspirational (deferred)

The original plan called for a layered 13-folder hierarchy:

```
00_Governance/, 01_Strategic/, 02_L1_Command/, 03_L2_Planning/, 04_L2_Execution/,
05_L2_RiskCommercial/, 06_L2_Compliance/, 07_L2_Performance/, 08_L3_Intelligence/,
09_Platform_Features/, 10_CrossCutting/, 11_System_Utilities/, 12_Audits/
```

**Status:** Aspirational. Not enforced. The Round 18 audit confirmed actual placement is `SystemAdmin/{Modules,Cross-link files}/` + `System Specs/` (above), not the 13-folder structure. The 13-folder hierarchy is retained here as a possible future migration target — not as a current rule. Migration would require renaming ~25 files + updating every internal reference; deferred indefinitely until a strong reason emerges.

## Round Folder Convention (Outputs)

Round folders are **logical / metadata-only**, not physical. No `Round{NN}/` directories exist on disk; round membership is captured via the audit stamp's `round:` field, the EPCC_VersionLog, and CLAUDE.md §3 status table.
