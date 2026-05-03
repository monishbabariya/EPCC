# X8 — Glossary & ENUMs
## Cross-Cutting Document v0.3 (LIVING)
**Owner:** PMO Director / System Architect
**Created:** 2026-05-03 (v0.1) | **Updated:** 2026-05-03 (v0.3)
**Status:** Living — appended on every module spec lock
**Source modules locked into this version:** M34, M01, **M02**
**Folder:** /10_CrossCutting/

---

## CHANGES IN v0.3

| # | Change | Driven By |
|---|---|---|
| 1 | Added `BACIntegrityStatus` ENUM (§3.27) | M02 spec OQ-1.2 |
| 2 | Added `BOQOrigin` ENUM (§3.28) | M02 spec OQ-1.7 |
| 3 | Added `BOQRateSpikeFormula` ENUM (§3.29) | M02 spec OQ-1.3 |
| 4 | Added `PackageTemplateTier` ENUM (§3.30) | M02 spec OQ-1.5 (refined) |
| 5 | Added `BACChangeType` ENUM (§3.31) | M02 BACIntegrityLedger |
| 6 | Added `UnitTier` ENUM (§3.32) | M02 UnitMaster |
| 7 | Added `UnitCategory` ENUM (§3.33) | M02 UnitMaster |
| 8 | Added `UnitSystem` ENUM (§3.34) | M02 UnitMaster (future-proof for OQ-1.9) |
| 9 | Added `PackageType` ENUM (§3.35) | M02 Package |
| 10 | Added `ChainValidationStatus` ENUM (§3.36) | M02 IDGovernanceLog |
| 11 | Added `CSVImportMode` ENUM (§3.37) | M02 CSVImportSession |
| 12 | Added `CSVImportTarget` ENUM (§3.38) | M02 CSVImportSession |
| 13 | Added `CSVImportRecordAction` ENUM (§3.39) | M02 CSVImportRecord |
| 14 | M02-owned audit event types added to AuditEventType extension (§4.12) | M02 spec |
| 15 | M02-owned Decision Queue trigger types catalogued (§4.14) | M02 spec |

---

## 1. PURPOSE

[unchanged from v0.2]

Single canonical reference for:
- Every ENUM type used across EPCC modules
- Every system-wide vocabulary term
- Every reserved keyword that a module spec must NOT redefine

**Rule:** When writing any module spec, look up here FIRST.

---

## 2. NAMING CONVENTIONS — LOCKED

[unchanged from v0.2]

| Concept | Convention | Example |
|---|---|---|
| ENUM type name | PascalCase | `UserStatus`, `RoleFamily`, `BACIntegrityStatus` |
| ENUM values (system identifiers) | `UPPER_SNAKE_CASE` | `SYSTEM_ADMIN` |
| ENUM values (status states) | `Pascal_Snake_Case` | `Stale_Pending_VO`, `System_Default` |
| Severity / RAG | Pascal single word | `Critical`, `Green` |
| Permission codes | `lower_snake_case` | `view_project` |
| Role codes | `UPPER_SNAKE_CASE` | `PMO_DIRECTOR` |
| Field names | `lower_snake_case` | `user_id` |
| BR codes | `BR-{module_id}-{seq}` | `BR-02-014` |
| Decision Queue triggers | `UPPER_SNAKE_CASE` | `BAC_INTEGRITY_STALE_DETECTED` |
| Audit event types | `UPPER_SNAKE_CASE` | `BAC_LEDGER_ENTRY` |

---

## 3. SYSTEM-WIDE ENUMS

### 3.1 — 3.18 *Unchanged from v0.2.*
[Severity, RAGStatus, HealthBand, SpeedTier, RecordStatus, LockState, UserStatus, ProjectStatus, Phase, StageGate, GatePassageOutcome, DataSource, Currency, Unit (CodeMaster), BillableState, Discipline, Sector→DEPRECATED, SectorTopLevel, DeliveryModel — see v0.2.]

### 3.19 — 3.26 *Unchanged from v0.2.*
[PartyType, PartyRole, ContractRole, ContractType, ScenarioActive, KPIName, KPIDirection, Region — see v0.2.]

### 3.27 `BACIntegrityStatus` (M02-owned) — **NEW v0.3**

Per M02 spec OQ-1.2 — locked at 2 values.

```
ENUM BACIntegrityStatus {
  Confirmed         // BAC current; M07 may compute EVM
  Stale_Pending_VO  // BAC suspended pending VO materialisation; M07 must not compute EAC during this
}
```

**Lock rule:** New states require formal trigger specification in spec + X8 version bump. No speculative additions.

---

### 3.28 `BOQOrigin` (M02-owned) — **NEW v0.3**

Per M02 spec OQ-1.7 — 5 values including HDI_Seed.

```
ENUM BOQOrigin {
  Manual               // user-typed in UI
  CSV_Import           // imported via CSVImportSession
  VO_Materialisation   // created via M05 VO materialisation Option B/C
  Template_Applied     // copied from PackageTemplate during apply
  HDI_Seed             // historical seed via HDI utility
}
```

**Immutability:** `BOQItem.boq_origin` is immutable post-creation per M02 BR audit-integrity guarantee.

---

### 3.29 `BOQRateSpikeFormula` (M02-owned) — **NEW v0.3**

Per M02 spec OQ-1.3 — legacy names retained.

```
ENUM BOQRateSpikeFormula {
  Loaded          // actual_rate × loaded factor (default 1.15)
  Indexed         // actual_rate × indexed factor (default 1.08)
  Flat_Redacted   // display literal "[RESTRICTED]"
}
```

**Role mapping** (locked in M02 Block 4a):
- `SYSTEM_ADMIN`, `PMO_DIRECTOR`, `FINANCE_LEAD`, `EXTERNAL_AUDITOR` → none (actual rate)
- `PORTFOLIO_MANAGER`, `PROJECT_DIRECTOR`, `PROCUREMENT_OFFICER`, `COMPLIANCE_MANAGER` → `Loaded`
- `PLANNING_ENGINEER`, `QS_MANAGER` → `Indexed`
- `SITE_MANAGER`, `READ_ONLY` → `Flat_Redacted`

**Spike factors** stored in tenant feature flags (M34): `M02_LOADED_FACTOR`, `M02_INDEXED_FACTOR`.

---

### 3.30 `PackageTemplateTier` (M02-owned) — **NEW v0.3**

Per M02 spec OQ-1.5 (refined) — three-tier copy-down model.

```
ENUM PackageTemplateTier {
  System_Default       // Anthropic ships via Alembic seed; read-only; visible to all tenants
  Tenant_Standard      // PMO_DIRECTOR creates (typically by copying System_Default); validates; visible across tenant
  Project_Template     // PROJECT_DIRECTOR creates on own project; project-scoped only
}
```

**Promotion direction (locked, BR-02-035):**
- Copy direction: `System_Default → Tenant_Standard → Project_Template` ✅
- **Forbidden:** Tenant_Standard.parent_template_id → Project_Template (upward)
- **Forbidden:** Project_Template.parent_template_id → System_Default (skipping tier)

**Quality gate:** Tenant_Standard must have `pmo_validated=true` before any project can apply it.

---

### 3.31 `BACChangeType` (M02-owned) — **NEW v0.3**

Used by `BACIntegrityLedger.change_type`.

```
ENUM BACChangeType {
  Initial_BAC          // First BAC value at package creation
  VO_Materialisation   // BAC change due to M05 VO materialisation
  Baseline_Revision    // BAC change due to M03 baseline extension
  Correction           // SYSTEM_ADMIN correction (e.g., HDI 7-day window)
  Template_Applied     // BAC change due to template apply (initial)
  CSV_Import           // BAC change due to CSV import
  HDI_Seed             // Initial BAC from HDI seed import
}
```

---

### 3.32 `UnitTier` (M02-owned) — **NEW v0.3**

```
ENUM UnitTier {
  Standard_Core        // System-wide locked; SYSTEM_ADMIN edits only via release
  Domain_Specific      // Tenant-scoped; PMO_DIRECTOR manages
  Custom               // Project-scoped; PROJECT_DIRECTOR manages on own project
}
```

**Resolution at BOQ creation:** Custom (project) → Domain_Specific (tenant) → Standard_Core. First match wins.

---

### 3.33 `UnitCategory` (M02-owned) — **NEW v0.3**

```
ENUM UnitCategory {
  Mass        // kg, g, mt, ton
  Volume      // m3, l, ml
  Length      // m, cm, mm
  Area        // m2, sqm
  Count       // nos, set, lot, doz
  Time        // hr, day, month
  Currency    // INR, etc.
  LumpSum     // LS
  Other       // catch-all
}
```

---

### 3.34 `UnitSystem` (M02-owned) — **NEW v0.3**

Future-proofing per M02 OQ-1.9.

```
ENUM UnitSystem {
  Metric      // v1.0 default and only supported value
  Imperial    // Reserved for future Phase 3+ expansion
}
```

**v1.0 lock:** All Standard_Core units ship Metric. Imperial reserved.

---

### 3.35 `PackageType` (M02-owned) — **NEW v0.3**

```
ENUM PackageType {
  Civil
  Structural
  MEP
  HVAC
  Electrical
  Plumbing
  Medical_Equipment
  Specialist
  Indirect
  Mixed
  Other
}
```

**Note:** Distinct from `Discipline` (CodeMaster, M02 WBSNode.activity_type). PackageType is contract-grouping; Discipline is technical category. Module specs may extend via X8 version bump.

---

### 3.36 `ChainValidationStatus` (M02-owned) — **NEW v0.3**

```
ENUM ChainValidationStatus {
  Passed
  Failed
}
```

Used by `IDGovernanceLog.chain_validation_status`.

---

### 3.37 `CSVImportMode` (M02-owned) — **NEW v0.3**

Per M02 spec OQ-1.6 — sparse update on Create_And_Update.

```
ENUM CSVImportMode {
  Create_Only            // Fail on duplicate; only new rows allowed
  Create_And_Update      // Sparse update on match; new rows on no-match
}
```

**No default.** User must explicitly select per import session.

---

### 3.38 `CSVImportTarget` (M02-owned) — **NEW v0.3**

```
ENUM CSVImportTarget {
  BOQItem
  WBSNode
  Package
}
```

Module specs may extend (e.g., M03 may add `Milestone`, M06 may add `RABill`).

---

### 3.39 `CSVImportRecordAction` (M02-owned) — **NEW v0.3**

```
ENUM CSVImportRecordAction {
  Created             // New row inserted
  Updated             // Existing row sparse-updated (Create_And_Update mode)
  Failed              // Validation failed; row rejected
  Skipped_Duplicate   // Create_Only mode; duplicate detected
}
```

---

## 4. M34-OWNED ENUMS

[§4.1 through §4.11 unchanged from v0.2]

### 4.12 `AuditEventType` (extended in v0.3)

**M02-owned event types added:**

```
WBS_CREATED
WBS_REORDERED
WBS_SOFT_DELETED
PACKAGE_CREATED
PACKAGE_UPDATED
PACKAGE_SOFT_DELETED
BOQ_CREATED
BOQ_RATE_CHANGED
BOQ_QUANTITY_CHANGED
BOQ_SOFT_DELETED
BOQ_WBS_MAPPING_CHANGED
RATE_ACCESSED_PRIVILEGED         // Audit log when actual_rate viewed by privileged role
UNIT_STANDARD_CORE_CHANGED        // Forwarded to M34 SystemAuditLog as privileged
UNIT_DOMAIN_SPECIFIC_CHANGED
UNIT_CUSTOM_CHANGED
UNAUTHORISED_STANDARD_CORE_EDIT_ATTEMPT
TEMPLATE_TENANT_STANDARD_CREATED
TEMPLATE_TENANT_STANDARD_VALIDATED
TEMPLATE_VERSION_LOCKED
TEMPLATE_APPLIED_TO_PACKAGE
CSV_IMPORT_SESSION_CREATED
CSV_IMPORT_PREVIEW_GENERATED
CSV_IMPORT_COMMITTED
CSV_IMPORT_ROLLED_BACK
BAC_LEDGER_ENTRY                  // Append-only ledger writes
ID_CHAIN_VALIDATION_PASSED
ID_CHAIN_VALIDATION_FAILED
BASELINE_LOCKED                   // From M08 SG-6 signal
BAC_INTEGRITY_STALE_DETECTED
BAC_INTEGRITY_RESTORED
VO_MATERIALISATION_RECEIVED       // From M05
VO_MATERIALISATION_COMPLETED       // M02 → M05/M06/M07 confirmation
```

### 4.13 `M01_DecisionQueueTriggerType` — *unchanged from v0.2*

### 4.14 `M02_DecisionQueueTriggerType` — **NEW v0.3**

```
BAC_DELTA_VARIANCE_EXCEEDED        // BR-02-037: VO BAC actual diverges from approved cost > ₹10K
TEMPLATE_VERSION_LOCK_REQUESTED    // PMO requests version lock
CSV_IMPORT_ANOMALY                 // Validation report flags >5% rows
WBS_DEPTH_OVERRIDE_REQUESTED       // PROJECT_DIRECTOR requests min_wbs_depth waiver (escalates to PMO)
```

All UPPER_SNAKE_CASE per F-013 lock.

---

## 5. CODEMASTER CATEGORIES — *updated v0.3*

| Category | Tier | Owned By | Notes |
|---|---|---|---|
| Unit | Standard_Core | SYSTEM_ADMIN | Now formalised in §3.32–3.34. M02 owns governance. |
| DocumentType | Domain_Specific | PMO_DIRECTOR | RFI, Submittal, Drawing |
| SectorSubType | Domain_Specific | PMO_DIRECTOR | Hospital_DBOT, etc. |
| **Discipline** | **Custom** | **PROJECT_DIRECTOR** | **Used by M02 WBSNode.activity_type — clarified in v0.3** |
| Currency | Standard_Core | SYSTEM_ADMIN | INR, USD, etc. |

---

## 6. RESERVED FIELDS — *unchanged*

Every entity (except append-only logs and junction tables) MUST include:

```
tenant_id, created_by, created_at, updated_by, updated_at, is_active
```

**Append-only entity exemption (v0.3 explicit list):**
- `BACIntegrityLedger` (M02) — UPDATE/DELETE forbidden at DB level
- `IDGovernanceLog` (M02)
- `CSVImportRecord` (M02)
- `ProjectPhaseHistory` (M01)
- `ProjectStatusHistory` (M01)
- `LoginAttempt` (M34)
- `SystemAuditLog` (M34)

---

## 7. NAMING DICTIONARY — *unchanged from v0.2*

[full table preserved — see v0.2]

---

## 8. EXTENSION PROTOCOL — *unchanged*

[unchanged from v0.2]

---

## 9. CHANGE LOG

| Version | Date | Change |
|---|---|---|
| v0.1 | 2026-05-03 | Initial. M34 ENUMs locked. System-wide ENUMs locked. |
| v0.2 | 2026-05-03 | M01 lock. SectorTopLevel + 8 other M01 ENUMs added. Phase enum migration note. DeliveryModel "Hybrid" retired. |
| **v0.3** | **2026-05-03** | **M02 lock. 13 new M02 ENUMs added (BACIntegrityStatus, BOQOrigin, BOQRateSpikeFormula, PackageTemplateTier, BACChangeType, UnitTier, UnitCategory, UnitSystem, PackageType, ChainValidationStatus, CSVImportMode, CSVImportTarget, CSVImportRecordAction). M02 audit event types and Decision Queue triggers catalogued. CodeMaster Discipline ownership clarified. Append-only entity exemption list explicit.** |

**Future bumps:**
- v0.4 — after M03 / M04 spec lock
- v0.5 — after M05 / M06 lock
- v0.6 — after M07 / M08 / M09 lock
- v1.0 — after all Phase 1 specs locked

---

## 10. ENFORCEMENT — *unchanged*

[unchanged from v0.2]

---

*v0.3 — Living document. M02 ENUMs locked. Next bump on M03 spec lock.*
