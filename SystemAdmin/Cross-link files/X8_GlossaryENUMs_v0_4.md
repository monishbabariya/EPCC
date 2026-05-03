# X8 — Glossary & ENUMs
## Cross-Cutting Document v0.4 (LIVING)
**Owner:** PMO Director / System Architect
**Created:** 2026-05-03 (v0.1) | **Updated:** 2026-05-03 (v0.4)
**Status:** Living — appended on every module spec lock
**Source modules locked into this version:** M34, M01, M02, **M03**
**Folder:** /10_CrossCutting/

---

## CHANGES IN v0.4

| # | Change | Driven By |
|---|---|---|
| 1 | Added `BaselineExtensionCause` ENUM (§3.40) | M03 OQ-1.2 |
| 2 | Added `LoadingProfileType` ENUM (§3.41) | M03 OQ-1.4 |
| 3 | Added `ResourceType` ENUM (§3.42) — 4 values incl. Vendor_Resource | M03 OQ-1.5 |
| 4 | Added `ReportingPeriodType` ENUM (§3.43) | M03 OQ-1.6 |
| 5 | Added `MilestoneStatus` ENUM (§3.44) | M03 spec |
| 6 | Added `MilestoneType` ENUM (§3.45) | M03 spec |
| 7 | Added `ScheduleEntryStatus` ENUM (§3.46) | M03 spec |
| 8 | Added `ProcurementItemStatus` ENUM (§3.47) | M03 spec |
| 9 | Added `WeatherWindowSeverity` ENUM (§3.48) | M03 spec |
| 10 | Added `BaselineExtensionStatus` ENUM (§3.49) | M03 spec |
| 11 | Added `ScheduleImportSource` ENUM (§3.50) | M03 spec |
| 12 | Added `ScheduleImportMode` ENUM (§3.51) | M03 spec (matches M02 pattern) |
| 13 | M03-owned audit event types added to AuditEventType extension (§4.12) | M03 spec |
| 14 | M03-owned Decision Queue trigger types catalogued (§4.15) | M03 spec |

**Cascade note:** M01 v1.2 (issued same round) removes `Project.reporting_period_type` field. ENUM ownership shifts to M03 (`LookAheadConfig.reporting_period_type`). M01 v1.2 reads via API.

---

## 1. PURPOSE

[unchanged from v0.3]

Single canonical reference for:
- Every ENUM type used across EPCC modules
- Every system-wide vocabulary term
- Every reserved keyword that a module spec must NOT redefine

**Rule:** When writing any module spec, look up here FIRST.

---

## 2. NAMING CONVENTIONS — LOCKED

[unchanged from v0.3]

| Concept | Convention | Example |
|---|---|---|
| ENUM type name | PascalCase | `UserStatus`, `BaselineExtensionCause` |
| ENUM values (system identifiers) | `UPPER_SNAKE_CASE` | `SYSTEM_ADMIN` |
| ENUM values (status states) | `Pascal_Snake_Case` | `Stale_Pending_VO`, `Force_Majeure` |
| Severity / RAG | Pascal single word | `Critical`, `Green` |
| Permission codes | `lower_snake_case` | `view_project` |
| Role codes | `UPPER_SNAKE_CASE` | `PMO_DIRECTOR` |
| Field names | `lower_snake_case` | `user_id` |
| BR codes | `BR-{module_id}-{seq}` | `BR-03-008` |
| Decision Queue triggers | `UPPER_SNAKE_CASE` | `CRITICAL_PATH_DELAY` |
| Audit event types | `UPPER_SNAKE_CASE` | `BASELINE_LOCKED` |

---

## 3. SYSTEM-WIDE ENUMS

### 3.1 — 3.39 *Unchanged from v0.3.*

[Severity, RAGStatus, HealthBand, SpeedTier, RecordStatus, LockState, UserStatus, ProjectStatus, Phase, StageGate, GatePassageOutcome, DataSource, Currency, Unit, BillableState, Discipline, Sector→DEPRECATED, SectorTopLevel, DeliveryModel, PartyType, PartyRole, ContractRole, ContractType, ScenarioActive, KPIName, KPIDirection, Region, BACIntegrityStatus, BOQOrigin, BOQRateSpikeFormula, PackageTemplateTier, BACChangeType, UnitTier, UnitCategory, UnitSystem, PackageType, ChainValidationStatus, CSVImportMode, CSVImportTarget, CSVImportRecordAction — see v0.3.]

---

### 3.40 `BaselineExtensionCause` (M03-owned) — **NEW v0.4**

Per M03 spec OQ-1.2 — locked at 6 values.

```
ENUM BaselineExtensionCause {
  Scope_Addition       // Client adds new scope
  Design_Change        // Design changes during execution
  Force_Majeure        // Acts of God, war, regulatory action beyond control
  Client_Delay         // Client-caused delay (decisions, approvals)
  Contractor_Delay     // Contractor-caused delay (manpower, supply chain, productivity)
  Neutral_Event        // Mutually agreed neutral cause; requires contract clause + evidence
}
```

**Auto-classification rules:**

| Cause | is_billable_to_client (default) | counts_against_vendor (default) | Contract clause required |
|---|---|---|---|
| Scope_Addition | true | false | Yes — VO mandatory |
| Design_Change | true (if client-initiated) | false | Yes |
| Force_Majeure | Case-by-case PMO override | false | Yes |
| Client_Delay | true | false | Yes |
| Contractor_Delay | false | true | No |
| Neutral_Event | false | false | **Yes — if blank → reclassify to Contractor_Delay** |

**Lock rule:** New cause categories require formal trigger specification + X8 version bump. No speculative additions.

---

### 3.41 `LoadingProfileType` (M03-owned) — **NEW v0.4**

Per M03 spec OQ-1.4 — locked at 5 values.

```
ENUM LoadingProfileType {
  Front_Loaded     // Civil works — heavy mobilisation upfront
  Bell             // MEP — distributed effort with mid-project peak
  Back_Loaded      // Commissioning — heavy at end
  Linear           // Indirect costs, ongoing services
  Custom           // User-defined curve via JSONB distribution_curve field
}
```

**System defaults by activity_category:**
- Civil → Front_Loaded
- Structural → Front_Loaded
- MEP → Bell
- HVAC → Bell
- Electrical → Bell
- Plumbing → Bell
- Medical_Equipment → Back_Loaded
- Commissioning → Back_Loaded
- Indirect → Linear
- Other → Linear (user override expected)

---

### 3.42 `ResourceType` (M03-owned) — **NEW v0.4**

Per M03 spec OQ-1.5 — **4 values** including Vendor_Resource.

```
ENUM ResourceType {
  Internal              // Direct employee of tenant organisation
  Contractor_Resource   // General contractor's field staff (party_id + contract_id required)
  Consultant_Resource   // Engineering/QS consultant (party_id + contract_id required)
  Vendor_Resource       // Equipment vendor field engineer (LINAC/MRI/CT vendors etc.)
                        // Distinct from contractors: shorter engagements, equipment-specific
}
```

**Governance per type:**
- `Internal` — Standard governance via M34
- `Contractor_Resource`, `Consultant_Resource` — Contract_Governed; require party_id + contract_id from M01
- `Vendor_Resource` — Agreement_Governed; party_id required; contract_id optional (may be PO-based)

---

### 3.43 `ReportingPeriodType` (M03-owned) — **NEW v0.4**

Per M03 spec OQ-1.6 — locked at 4 values.

```
ENUM ReportingPeriodType {
  Monthly       // Default; KDMC pilot; most Indian capital projects
  Weekly        // Fast-cycle projects; high-control phases
  Daily         // Critical phases (commissioning, gate windows)
  Event_Driven  // Irregular pace projects (post-monsoon catch-up)
}
```

**Default:** `Monthly`.

**Ownership cascade:** Field stored on `LookAheadConfig.reporting_period_type` (M03-owned). M01 reads via API. **M01 v1.2 (Round 16 cascade) removes `Project.reporting_period_type` field.**

---

### 3.44 `MilestoneStatus` (M03-owned) — **NEW v0.4**

Per M03 spec.

```
ENUM MilestoneStatus {
  Not_Started     // Default; before planned_date passes
  In_Progress     // Activities underway toward milestone
  Achieved        // actual_date populated; milestone met
  Delayed         // extended_baseline_date passed; not yet achieved
  At_Risk         // Forecast > extended_baseline_date by significant margin
}
```

**Auto-transitions:**
- `Not_Started` → `In_Progress` when any linked WBS activity status = In_Progress
- Any → `Achieved` when actual_date populated (from M04 progress capture or M09 compliance grant)
- Any → `Delayed` when extended_baseline_date < today AND status ≠ Achieved (BR-03-021 daily check)
- `In_Progress` → `At_Risk` when forecast_date > extended_baseline_date + 7 days AND is_gate_linked = true

---

### 3.45 `MilestoneType` (M03-owned) — **NEW v0.4**

Per M03 spec.

```
ENUM MilestoneType {
  Design          // Design package release, drawing approvals
  Procurement     // PO awarded, equipment received
  Construction    // Civil/structural completion stages
  Commissioning   // Testing, integrated commissioning, handover prep
  Regulatory      // Permits, NABH, AERB, EC, Fire NOC milestones
  Financial       // Funding tranches, payment milestones
  Handover        // Substantial completion, final handover
}
```

---

### 3.46 `ScheduleEntryStatus` (M03-owned) — **NEW v0.4**

Per M03 spec.

```
ENUM ScheduleEntryStatus {
  Not_Started     // planned_start in future; no progress
  In_Progress     // Activities underway (from M04)
  Completed       // 100% complete (from M04)
  Delayed         // extended_baseline_finish < today AND not Completed
}
```

---

### 3.47 `ProcurementItemStatus` (M03-owned) — **NEW v0.4**

Per M03 spec.

```
ENUM ProcurementItemStatus {
  Planned          // Identified in procurement schedule; no action yet
  RFQ_Issued       // Vendor inquiries sent
  Order_Placed     // PO created in M06
  Manufactured     // Vendor confirms manufacture complete
  In_Transit       // Shipment underway
  Delivered        // Received on site (linked to M04 MaterialReceipt)
  Installed        // Installation complete (per M04)
}
```

---

### 3.48 `WeatherWindowSeverity` (M03-owned) — **NEW v0.4**

Per M03 spec.

```
ENUM WeatherWindowSeverity {
  Low       // Productivity factor 0.85-1.00 (minor impact)
  Medium    // Productivity factor 0.60-0.84 (moderate impact)
  High      // Productivity factor 0.30-0.59 (severe impact, e.g., monsoon civil works)
  Severe    // Productivity factor 0.00-0.29 (work suspension, e.g., severe monsoon weeks)
}
```

---

### 3.49 `BaselineExtensionStatus` (M03-owned) — **NEW v0.4**

Per M03 spec.

```
ENUM BaselineExtensionStatus {
  Pending           // Submitted; awaiting PMO_DIRECTOR review
  Approved          // PMO_DIRECTOR approved; cascades to schedule
  Rejected          // PMO_DIRECTOR rejected with reason
}
```

---

### 3.50 `ScheduleImportSource` (M03-owned) — **NEW v0.4**

Per M03 spec.

```
ENUM ScheduleImportSource {
  Primavera_P6_XML
  Primavera_P6_XER
  MSP_XML
}
```

---

### 3.51 `ScheduleImportMode` (M03-owned) — **NEW v0.4**

Per M03 spec — matches M02 CSVImportMode pattern.

```
ENUM ScheduleImportMode {
  Create_Only            // Fail on duplicate; only new entries allowed
  Create_And_Update      // Sparse update on match; new entries on no-match
}
```

**No default.** User must explicitly select per import session.

---

## 4. M34-OWNED ENUMS

[§4.1 through §4.11 unchanged from v0.3]

### 4.12 `AuditEventType` (extended in v0.4)

**M03-owned event types added:**

```
SCHEDULE_ENTRY_CREATED
SCHEDULE_ENTRY_UPDATED
SCHEDULE_ENTRY_DELETED
BASELINE_LOCKED
BASELINE_LOCK_BLOCKED
BASELINE_EXTENSION_SUBMITTED
BASELINE_EXTENSION_APPROVED
BASELINE_EXTENSION_REJECTED
NEUTRAL_EVENT_RECLASSIFIED       // Auto-reclassification per BR-03-008
BILLABLE_FLAG_OVERRIDDEN
VENDOR_FLAG_OVERRIDDEN
MILESTONE_CREATED
MILESTONE_STATUS_CHANGED
MILESTONE_FORECAST_UPDATED
PV_OVERRIDE_APPLIED
LOADING_PROFILE_CREATED
LOADING_PROFILE_ASSIGNED
RESOURCE_ALLOCATED
RESOURCE_OVER_ALLOCATED
PROCUREMENT_ITEM_CREATED
PROCUREMENT_ORDER_PLACED
PROCUREMENT_ITEM_DELIVERED
WEATHER_WINDOW_CONFIGURED
LOOK_AHEAD_WINDOW_CHANGED
REPORTING_PERIOD_TYPE_CHANGED
SCHEDULE_IMPORT_SESSION_CREATED
SCHEDULE_IMPORT_PREVIEW_GENERATED
SCHEDULE_IMPORT_COMMITTED
SCHEDULE_IMPORT_ROLLED_BACK
PV_RECALCULATION_TRIGGERED       // Cascade event from report_date change
CRITICAL_PATH_RECALCULATED
```

### 4.13 `M01_DecisionQueueTriggerType` — *unchanged from v0.3*

### 4.14 `M02_DecisionQueueTriggerType` — *unchanged from v0.3*

### 4.15 `M03_DecisionQueueTriggerType` — **NEW v0.4**

```
SCHEDULE_RECOVERY_REQUIRED         // BR-03-015: gate-linked milestone delay > 7 days
PROCUREMENT_ESCALATION             // BR-03-016: long-lead order date missed
NEUTRAL_EVENT_CLASSIFICATION_REVIEW // BR-03-008 trigger before auto-reclassify
CRITICAL_PATH_DELAY                // BR-03-018: critical path activity delayed > 5 days
RESOURCE_OVER_ALLOCATION_CONFLICT   // BR-03-030: same resource > 100% in period
```

All UPPER_SNAKE_CASE per F-013 lock.

---

## 5. CODEMASTER CATEGORIES — *unchanged from v0.3*

[unchanged]

---

## 6. RESERVED FIELDS — *updated v0.4*

Every entity (except append-only logs and junction tables) MUST include:

```
tenant_id, created_by, created_at, updated_by, updated_at, is_active
```

**Append-only entity exemption (v0.4 explicit list — extended):**
- `BACIntegrityLedger` (M02) — UPDATE/DELETE forbidden at DB level
- `IDGovernanceLog` (M02)
- `CSVImportRecord` (M02)
- `ProjectPhaseHistory` (M01)
- `ProjectStatusHistory` (M01)
- `LoginAttempt` (M34)
- `SystemAuditLog` (M34)
- **`Baseline` (M03)** — sealed at SG-6; immutable after lock
- **`BaselineExtension` (M03)** — append-only after approval (no edits to approved extensions)
- **`PVProfileSnapshot` (M03)** — historical snapshots immutable

---

## 7. NAMING DICTIONARY — *unchanged from v0.3*

[unchanged]

---

## 8. EXTENSION PROTOCOL — *unchanged*

[unchanged from v0.3]

---

## 9. CHANGE LOG

| Version | Date | Change |
|---|---|---|
| v0.1 | 2026-05-03 | Initial. M34 ENUMs locked. System-wide ENUMs locked. |
| v0.2 | 2026-05-03 | M01 lock. SectorTopLevel + 8 other M01 ENUMs added. Phase enum migration note. DeliveryModel "Hybrid" retired. |
| v0.3 | 2026-05-03 | M02 lock. 13 new M02 ENUMs added. M02 audit event types and Decision Queue triggers catalogued. CodeMaster Discipline ownership clarified. Append-only entity exemption list explicit. |
| **v0.4** | **2026-05-03** | **M03 lock. 12 new M03 ENUMs added (BaselineExtensionCause, LoadingProfileType, ResourceType (4 values incl. Vendor_Resource), ReportingPeriodType, MilestoneStatus, MilestoneType, ScheduleEntryStatus, ProcurementItemStatus, WeatherWindowSeverity, BaselineExtensionStatus, ScheduleImportSource, ScheduleImportMode). M03 audit event types (28) and Decision Queue triggers (5) catalogued. Append-only entity exemption list extended with Baseline + BaselineExtension + PVProfileSnapshot. Cascade: M01 v1.2 removes reporting_period_type; M03 owns.** |

**Future bumps:**
- v0.5 — after M04 / M05 spec lock
- v0.6 — after M06 / M07 lock
- v0.7 — after M08 / M09 lock
- v1.0 — after all Phase 1 specs locked

---

## 10. ENFORCEMENT — *unchanged*

[unchanged from v0.3]

---

*v0.4 — Living document. M03 ENUMs locked. Next bump on M04 spec lock.*
