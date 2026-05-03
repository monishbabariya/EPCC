# X8 — Glossary & ENUMs
## Cross-Cutting Document v0.2 (LIVING)
**Owner:** PMO Director / System Architect
**Created:** 2026-05-03 (v0.1) | **Updated:** 2026-05-03 (v0.2)
**Status:** Living — appended on every module spec lock
**Source modules locked into this version:** M34, M01
**Folder:** /10_CrossCutting/

---

## CHANGES IN v0.2

| # | Change | Driven By |
|---|---|---|
| 1 | Added `SectorTopLevel` ENUM (§3.16a) | M01 spec OQ-1.2=C |
| 2 | Added `PartyType` ENUM (§3.19) | M01 spec |
| 3 | Added `PartyRole` ENUM (§3.20) | M01 spec |
| 4 | Added `ContractRole` ENUM (§3.21) | M01 spec |
| 5 | Added `ContractType` ENUM (§3.22) | M01 spec |
| 6 | Added `ScenarioActive` ENUM (§3.23) | M01 spec |
| 7 | Added `KPIName` ENUM (§3.24) | M01 spec |
| 8 | Added `KPIDirection` ENUM (§3.25) | M01 spec |
| 9 | Added `Region` ENUM (§3.26) | M01 PincodeMaster |
| 10 | Phase enum locked migration note added (§3.9) | M01 OQ-1.1=A |
| 11 | DeliveryModel: "Hybrid" formally retired (§3.18) | M01 OQ-1.3=A |
| 12 | M01-owned Decision Queue trigger types catalogued (§4.13) | M01 spec |
| 13 | M01 audit event types added to AuditEventType extension (§4.12) | M01 spec |

---

## 1. PURPOSE

[unchanged from v0.1 — see source]

Single canonical reference for:
- Every ENUM type used across EPCC modules
- Every system-wide vocabulary term
- Every reserved keyword that a module spec must NOT redefine

**Rule:** When writing any module spec, look up here FIRST.

---

## 2. NAMING CONVENTIONS — LOCKED

[unchanged from v0.1]

| Concept | Convention | Example |
|---|---|---|
| ENUM type name | PascalCase | `UserStatus`, `RoleFamily` |
| ENUM values (system identifiers) | `UPPER_SNAKE_CASE` | `SYSTEM_ADMIN` |
| ENUM values (status states) | `Pascal_Snake_Case` | `Draft`, `Stale_Pending_VO` |
| Severity / RAG | Pascal single word | `Critical`, `Green` |
| Permission codes | `lower_snake_case` | `view_project` |
| Role codes | `UPPER_SNAKE_CASE` | `PMO_DIRECTOR` |
| Field names | `lower_snake_case` | `user_id` |
| BR codes | `BR-{module_id}-{seq}` | `BR-01-010` |
| Decision Queue triggers | `UPPER_SNAKE_CASE` | `BAC_VS_CONTRACT_DEVIATION` |
| Audit event types | `UPPER_SNAKE_CASE` | `LOGIN_SUCCESS` |

---

## 3. SYSTEM-WIDE ENUMS

### 3.1 `Severity` — *unchanged from v0.1*

```
ENUM Severity { Critical / High / Medium / Low / Info }
```

### 3.2 `RAGStatus` — *unchanged*

```
ENUM RAGStatus { Green / Amber / Red }
```

### 3.3 `HealthBand` — *unchanged*

```
ENUM HealthBand { Excellent / Good / Watch / At_Risk / Critical }
```

### 3.4 `SpeedTier` — *unchanged*

```
ENUM SpeedTier { Realtime / NearRealtime / Batch / Link }
```

### 3.5 `RecordStatus` — *unchanged*

```
ENUM RecordStatus { Draft / Active / Suspended / Archived / Deleted }
```

### 3.6 `LockState` — *unchanged*

```
ENUM LockState { Unlocked / Pending_Review / Locked / Archived }
```

### 3.7 `UserStatus` (M34-owned) — *unchanged*

```
ENUM UserStatus { Active / Suspended / Locked / Archived }
```

### 3.8 `ProjectStatus` (M01-owned) — *locked v0.2*

```
ENUM ProjectStatus {
  Draft        // initial state until activation per BR-01-010
  Active       // operational
  On_Hold      // paused; downstream modules read-only; reactivable
  Closed       // normal completion; not reactivable
  Cancelled    // abnormal termination; not reactivable
}
```

**State machine:** Draft → Active | Cancelled. Active ↔ On_Hold. Active → Closed | Cancelled. On_Hold → Closed | Cancelled. **Forbidden:** Closed/Cancelled → anything.

### 3.9 `Phase` (M01-owned) — *locked v0.2*

```
ENUM Phase {
  Pre_Investment       // pre SG-3 (idea, concept, DPR, capital sanction)
  Design               // SG-4 (detailed design)
  Pre_Construction     // SG-5 to SG-6 (clearances, procurement, award)
  Construction         // SG-7 (execution)
  Equipment            // SG-8 (equipment install + integration)
  Commissioning        // SG-9 (clinical commissioning)
  Empanelment          // SG-10 (insurance empanelment + go-live)
  Handover             // SG-11 (operations handover)
  DLP                  // post-SG-11 (Defects Liability Period)
  Closed               // post-DLP
}
```

**Migration note (v0.2):** Legacy 5-value Phase enum (`DEV / DES / EPC / COM / OAM`) replaced. KDMC pilot migration: `EPC` → `Construction`. Module specs that reference Phase must adopt this 10-value enum.

### 3.10 `StageGate` — *unchanged*

```
ENUM StageGate { SG_0 / SG_1 / SG_2 / SG_3 / SG_4 / SG_5 / SG_6 / SG_7 / SG_8 / SG_9 / SG_10 / SG_11 }
```

### 3.11 `GatePassageOutcome` — *unchanged*

```
ENUM GatePassageOutcome { Passed / Conditional_Pass / Stopped / Reopened / Skipped }
```

### 3.12 `DataSource` (HDI cross-cutting) — *unchanged*

```
ENUM DataSource { Live_EPCC / Historical_Seed / Mixed_Seed / Manual_Adjustment }
```

### 3.13 `Currency` — *unchanged*

```
ENUM Currency { INR / USD / EUR / GBP / AED / SGD / JPY / CHF }
```

### 3.14 `Unit` — see CodeMaster (M34 §3o) — *unchanged*

### 3.15 `BillableState` — *unchanged*

```
ENUM BillableState { Billable / Non_Billable / Disputed / Not_Yet_Determined }
```

### 3.16 `Discipline` — see CodeMaster — *unchanged*

### 3.16a `SectorTopLevel` (M01-owned) — **NEW v0.2**

Top-level project sector classification. Stable list (changes require release).

```
ENUM SectorTopLevel {
  Healthcare      // hospitals, diagnostics, clinics
  Infrastructure  // highways, metros, railways, ports, airports
  Residential     // apartments, townships
  Commercial      // offices, malls, hotels
  Industrial      // factories, warehouses, data centers
}
```

**Sub-types** are managed via `CodeMaster` with `code_category = 'SectorSubType'`. Each sub-type record's `parent_code_id` references the parent SectorTopLevel CodeMaster row. Examples:

| sector_top_level | sector_sub_type_code (CodeMaster) |
|---|---|
| Healthcare | Hospital_DBOT, Hospital_PPP, Hospital_EPC, Diagnostics_Center, Specialty_Clinic |
| Infrastructure | Highway, Metro, Railway, Port, Airport, Bridge |
| Residential | Apartment_Highrise, Township_Integrated, Affordable_Housing |
| Commercial | Office_Commercial, Mall_Retail, Hotel_Hospitality |
| Industrial | Warehouse_Industrial, Factory_Industrial, Data_Center |

**Why hybrid (ENUM + CodeMaster):**
- Top-level list is stable (5 values cover all of Indian construction)
- Sub-types proliferate and need PMO_DIRECTOR runtime control
- M09 Compliance template selection keys off sector_top_level (stability needed)

### 3.17 `Sector` — DEPRECATED → see §3.16a + CodeMaster

### 3.18 `DeliveryModel` — *updated v0.2*

```
ENUM DeliveryModel {
  EPC                       // Engineering, Procurement, Construction
  EPCM                      // EPC + Management
  DBOT                      // Design-Build-Operate-Transfer
  PPP                       // Public-Private Partnership
  Turnkey                   // single-vendor end-to-end
  Construction_Management   // CM at risk / agency
}
```

**Retired in v0.2:**
- ~~`Hybrid`~~ — replaced by `delivery_model_notes` free-text field on Project entity. If a project is genuinely between models, capture the specific arrangement in notes.

### 3.19 `PartyType` (M01-owned) — **NEW v0.2**

```
ENUM PartyType {
  Client                    // primary client / employer
  EPC_Contractor            // main works contractor
  PMC                       // project management consultant
  Consultant                // design / engineering consultant
  Specialist_Subcontractor  // specialist trades (lifts, MEP, BMS)
  Vendor                    // material/equipment supplier
  Lender                    // bank / financial institution
  Auditor                   // external auditor (NABH, financial, lender)
  Authority                 // statutory authority (NMC, AERB, fire, PCB)
}
```

### 3.20 `PartyRole` (M01-owned) — **NEW v0.2**

Role assigned to a party on a specific project (via ProjectPartyAssignment).

```
ENUM PartyRole {
  Primary_Client
  Co_Client
  EPC_Contractor
  PMC
  Design_Consultant
  MEP_Consultant
  Structural_Consultant
  Specialist_Subcontractor
  Vendor
  Lender
  NABH_Auditor
  Other
}
```

**Note:** PartyRole is the project-context role. A Party has a global `party_type` (§3.19) and may serve different `party_role`s on different projects.

### 3.21 `ContractRole` (M01-owned) — **NEW v0.2**

```
ENUM ContractRole {
  Primary       // main commercial instrument; project requires ≥ 1; soft cap 3 (BR-01-018)
  Secondary     // supplementary contracts (e.g., Owner's Engineer)
  Specialist    // specialist subcontracts (lifts, BMS, medical equipment)
}
```

### 3.22 `ContractType` (M01-owned) — **NEW v0.2**

```
ENUM ContractType {
  DBOT
  EPC
  EPCM
  Lump_Sum
  Item_Rate
  PPP
  Turnkey
  Construction_Management
}
```

**Note:** ContractType ≠ DeliveryModel. DeliveryModel is project-level; ContractType is per-contract. A DBOT project may have a Lump_Sum primary contract + Item_Rate specialist contracts.

### 3.23 `ScenarioActive` (M01-owned) — **NEW v0.2**

```
ENUM ScenarioActive { Base / Best / Worst }
```

Default: `Base`. Change requires `SCENARIO_CHANGE_APPROVAL` Decision Queue (BR-01-016).

### 3.24 `KPIName` (M01-owned) — **NEW v0.2**

```
ENUM KPIName {
  CPI                  // Cost Performance Index (M07)
  SPI                  // Schedule Performance Index (M07)
  Gross_Margin         // % gross margin (M06)
  Open_High_Risks      // count from M05
  Pending_Clearances   // count from M09
}
```

**Module specs may extend this enum** via X8 version bump as new KPIs are introduced (e.g., M10 may add health composite KPIs).

### 3.25 `KPIDirection` (M01-owned) — **NEW v0.2**

```
ENUM KPIDirection {
  Higher_Is_Better     // CPI, SPI, Gross_Margin
  Lower_Is_Better      // Open_High_Risks, Pending_Clearances
}
```

Drives RAG threshold semantics in KPIThreshold validation (BR-01-009).

### 3.26 `Region` (M01 PincodeMaster) — **NEW v0.2**

```
ENUM Region { North / South / East / West / Northeast / Central }
```

Used for regional analytics + regulatory clustering.

---

## 4. M34-OWNED ENUMS

[§4.1 through §4.11 unchanged from v0.1]

### 4.12 `AuditEventType` (extended in v0.2)

**M01-owned event types added (§ extension):**

```
PROJECT_CREATED
PROJECT_UPDATED
PROJECT_STATUS_CHANGED
PROJECT_PHASE_CHANGED
PROJECT_REPORT_DATE_UPDATED
PROJECT_SOFT_DELETED
PROJECT_SOFT_DELETE_BLOCKED
PORTFOLIO_CREATED
PROGRAM_CREATED
CONTRACT_CREATED
CONTRACT_FINANCIAL_TERMS_CHANGED
PARTY_CREATED
PARTY_UPDATED
PARTY_ASSIGNED_TO_PROJECT
PARTY_ASSIGNMENT_REVOKED
EXCLUSIVITY_OVERRIDE_APPROVED
MULTI_PRIMARY_JUSTIFICATION_APPROVED
KPI_THRESHOLD_CHANGED
SCENARIO_CHANGED
PINCODE_DATASET_REFRESHED
```

### 4.13 `M01_DecisionQueueTriggerType` — **NEW v0.2**

```
BAC_VS_CONTRACT_DEVIATION
EXCLUSIVITY_EXCEPTION_APPROVAL
PROJECT_REPORT_DATE_STALE
MULTIPLE_PRIMARY_CONTRACTS_FLAG
SCENARIO_CHANGE_APPROVAL
```

All UPPER_SNAKE_CASE per F-013 lock.

---

## 5. CODEMASTER CATEGORIES — *updated v0.2*

| Category | Tier | Owned By | Notes |
|---|---|---|---|
| Unit | Standard_Core | SYSTEM_ADMIN | kg, m, m², m³, hr, etc. |
| DocumentType | Domain_Specific | PMO_DIRECTOR | RFI, Submittal, Drawing |
| **SectorSubType** | **Domain_Specific** | **PMO_DIRECTOR** | **NEW v0.2 — sub-types under SectorTopLevel** |
| Discipline | Custom | PROJECT_DIRECTOR | CIV, STR, MEP, etc. |
| Currency | Standard_Core | SYSTEM_ADMIN | INR, USD, etc. |

---

## 6. RESERVED FIELDS — *unchanged*

Every entity (except append-only logs and junction tables) MUST include:

```
tenant_id, created_by, created_at, updated_by, updated_at, is_active
```

---

## 7. NAMING DICTIONARY — *unchanged from v0.1*

[full table preserved — see v0.1]

---

## 8. EXTENSION PROTOCOL — *unchanged*

When writing a new spec:
- ENUM exists in §3 or §4 → reference it
- Need new value → append here, version bump
- New concept → new section here, version bump
- Reserved field → inherit from §6

---

## 9. CHANGE LOG

| Version | Date | Change |
|---|---|---|
| v0.1 | 2026-05-03 | Initial. M34 ENUMs locked. System-wide ENUMs locked. |
| **v0.2** | **2026-05-03** | **M01 lock. SectorTopLevel ENUM added. PartyType, PartyRole, ContractRole, ContractType, ScenarioActive, KPIName, KPIDirection, Region added. Phase enum migration note. DeliveryModel "Hybrid" retired. SectorSubType CodeMaster category added. M01 audit event types and Decision Queue triggers catalogued.** |

**Future bumps:**
- v0.3 — after M02/M03 spec lock (will likely add WBSNodeType, PVProfile-related enums, etc.)
- v0.4 — after M04/M05/M06 lock (NCR-related, VO-related, financial-state enums)
- v0.5 — after M07/M08/M09 lock
- v1.0 — after all Phase 1 specs locked

---

## 10. ENFORCEMENT — *unchanged*

[unchanged from v0.1]

---

*v0.2 — Living document. M01 ENUMs locked. Next bump on M02 spec lock.*
