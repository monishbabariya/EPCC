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

---

## 13-Folder Hierarchy

```
00_Governance/        → standards, naming, version log
01_Strategic/         → L0 modules
02_L1_Command/        → M34, M01, M23, M24, M28
03_L2_Planning/       → M02, M03
04_L2_Execution/      → M04, M14, M27, M12, M13
05_L2_RiskCommercial/ → M05, M06, M22
06_L2_Compliance/     → M09, M25, M30, M31
07_L2_Performance/    → M07, M26, M32
08_L3_Intelligence/   → M08, M10, M11, M15, M29, M33
09_Platform_Features/ → PF01-PF06
10_CrossCutting/      → X1-X8 living docs
11_System_Utilities/  → HDI
12_Audits/            → audit reports per round
```

---

## Round Folder Convention (Outputs)

```
Round{NN}/
  {Module}_{ShortName}_{ArtefactType}_v{Major}_{Minor}.{ext}
  [+ X8 / X9 version bump file if any]
  [+ cascade notes if any]
```

Example: `Round17/M03_PlanningMilestones_Wireframes_v1_0.html`
