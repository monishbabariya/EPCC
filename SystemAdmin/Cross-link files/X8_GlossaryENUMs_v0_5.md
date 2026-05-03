# X8 — Glossary & ENUMs
## Cross-Cutting Document v0.5 (LIVING)
**Owner:** PMO Director / System Architect
**Created:** 2026-05-03 (v0.1) | **Updated:** 2026-05-03 (v0.5)
**Status:** Living — appended on every module spec lock
**Source modules locked into this version:** M34, M01, M02, M03, **M04**
**Folder:** SystemAdmin/Cross-link files/ (per Round 18 audit canonical placement)

---

## CHANGES IN v0.5

| # | Change | Driven By |
|---|---|---|
| 1 | Added `ProgressMeasurementMethod` ENUM (§3.52) — 4 values | M04 Brief OQ-1.2 |
| 2 | Added `ProgressApprovalStatus` ENUM (§3.53) — 4 values incl. Rejected | M04 Brief OQ-1.3 |
| 3 | Added `EVConfidence` ENUM (§3.54) — 4 values; carried forward from M07 v3.0 legacy for forward-traceability | M04 Spec BR-04-013 |
| 4 | Added `NCRStatus` ENUM (§3.55) — 7-state lifecycle | M04 Spec |
| 5 | Added `NCRRootCauseCategory` ENUM (§3.56) — 5 values | M04 Spec |
| 6 | Added `MaterialReceiptStatus` ENUM (§3.57) — 6-state lifecycle | M04 Spec |
| 7 | Added `MaterialQCStatus` ENUM (§3.58) — 3 values | M04 Spec |
| 8 | Added `MaterialQCDecision` ENUM (§3.59) — 3 values | M04 Spec |
| 9 | M04-owned audit event types (22) added to AuditEventType extension (§4.12) | M04 Spec Appendix A |
| 10 | M04-owned Decision Queue trigger types (8) catalogued (§4.16) | M04 Spec Appendix A |
| 11 | M04 append-only entities (4) added to reserved-fields exemption list (§6) | M04 Spec Block 8b |

**Cascade note:** M04 also introduces `ProjectExecutionConfig` (resolves OQ-2.6 — execution-tunables live in M04, not M01) — this is an entity, not an ENUM, so no v0.5 ENUM impact. Documented in M04 Spec Block 3k.

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

### 3.52 `ProgressMeasurementMethod` (M04-owned) — **NEW v0.5**

Per M04 Brief OQ-1.2=C — locked at 4 methods. Method choice is captured per WBS node in `ProgressMeasurementConfig` and locked after the first ProgressEntry persists (BR-04-002).

```
ENUM ProgressMeasurementMethod {
  Units                  // Quantity-of-output units (e.g., m³, tonnes, each).
                         // pct = units_completed / units_total
  Steps                  // Discrete sub-steps with equal weight.
                         // pct = len(steps_completed) / steps_total_count
  Milestone              // Weighted milestones; weights sum to 1.0.
                         // pct = sum(weights of milestones_achieved)
  Subjective_Estimate    // Free-form % with required basis text (≥100 chars
                         // when declared > config.subjective_basis_threshold_pct,
                         // default 25%). EV consumed by M07 with confidence=Low.
}
```

**Default:** None. Selected per WBS node by PLANNING_ENGINEER at WBS authoring; no system default.

---

### 3.53 `ProgressApprovalStatus` (M04-owned) — **NEW v0.5**

Per M04 Brief OQ-1.3=B — three-state lifecycle (Draft → Submitted → Approved/Rejected). The fourth value `Rejected` re-opens the cycle by routing the entry back to contractor for re-Draft.

```
ENUM ProgressApprovalStatus {
  Draft        // Contractor declared, not yet submitted to EPCC for approval
  Submitted    // Handed off to QS_MANAGER (and PROJECT_DIRECTOR if dual-signoff)
  Approved     // Final approval — consumed by M07 (EV) and M06 (billing)
  Rejected     // QS or PD rejected with reason ≥ 50 chars; re-Draft permitted
}
```

**M07 contract (Round 31+ when M07 specced):** filter `WHERE status='Approved'` — Submitted is invisible to EV computation, so the new 3-state model is transparently consumed by M07's existing 2-state expectation.

---

### 3.54 `EVConfidence` (M04-owned, M07-consumed) — **NEW v0.5**

Carried forward from M07 v3.0 legacy for forward-traceability per Round 18 cascade-pattern discipline. M04 sets this on every Approved ProgressEntry (BR-04-013); M07 reads when computing EV.

```
ENUM EVConfidence {
  High        // Method ∈ {Units, Steps, Milestone} — verifiable
  Low         // Method = Subjective_Estimate — qualitative
  Fallback    // M07-side: previous-period value used because current is Draft
              // (M04 doesn't write Fallback — set by M07 BR-07-027)
  Derived     // M07-side: rolled up from children (parent has no own entry)
}
```

**M04 writes only `High` or `Low`.** `Fallback` and `Derived` are set by M07 during EV computation.

---

### 3.55 `NCRStatus` (M04-owned) — **NEW v0.5**

Per M04 Spec Block 3e + state-machine diagram. 7-state lifecycle. NCR cannot be re-opened after Closed (per M04 Spec Block 10 OQ #6 — recurrence requires new NCR with cross-reference).

```
ENUM NCRStatus {
  Open                       // Just raised; no contractor response yet
  Response_Pending           // Awaiting contractor response (response_due may have passed)
  Response_Received          // Contractor responded; remediation plan submitted
  Remediation_In_Progress    // Contractor working on fix
  Reinspection_Pending       // Remediation declared complete; awaiting EPCC inspection
  Closed                     // reinspection_result=Pass OR PMO override (Low only)
  Disputed                   // Contractor disputes liability; is_disputed=true
}
```

---

### 3.56 `NCRRootCauseCategory` (M04-owned) — **NEW v0.5**

Per M04 Spec Block 3e. Captured at NCR creation; allows trend analysis on root-cause patterns per contractor / per project.

```
ENUM NCRRootCauseCategory {
  Workmanship    // Quality of execution (most common in healthcare construction)
  Material       // Defective or non-spec material
  Design         // Design intent vs constructability gap
  Procedure      // Procedural / process failure
  Other          // Free-form; description must clarify
}
```

---

### 3.57 `MaterialReceiptStatus` (M04-owned) — **NEW v0.5**

Per M04 Spec Block 3g + state-machine diagram. 6-state lifecycle covering the receipt-to-GRN-emission flow.

```
ENUM MaterialReceiptStatus {
  Received                // Material arrived on site
  In_QC                   // Quality control inspection underway
  Accepted                // qc_decision=Accepted; GRN_SIGNAL emitted to M06; actual_delivery_date emitted to M03
  Rejected                // qc_decision=Rejected; return-to-vendor flow
  Conditional_Accepted    // qc_decision=Conditional_Acceptance; qc_notes ≥ 100 chars required
  Closed                  // Final state — M06 has acknowledged GRN OR return-to-vendor complete
}
```

---

### 3.58 `MaterialQCStatus` (M04-owned) — **NEW v0.5**

Per M04 Spec Block 3g. Captures the QC inspection lifecycle within the broader receipt status. Distinct from `MaterialReceiptStatus` — this tracks "is QC inspection complete" while ReceiptStatus tracks "has the receipt closed."

```
ENUM MaterialQCStatus {
  Pending_QC      // Receipt created; QC not yet started
  In_QC           // Inspection underway
  QC_Complete     // Inspection done; qc_decision populated
}
```

---

### 3.59 `MaterialQCDecision` (M04-owned) — **NEW v0.5**

Per M04 Spec Block 3g + BR-04-027. Three terminal QC outcomes. `Conditional_Acceptance` requires `qc_notes ≥ 100 chars` (BR-04-030).

```
ENUM MaterialQCDecision {
  Accepted                  // Material passes QC; full acceptance
  Rejected                  // Material fails QC; return to vendor; M06 GRN NOT emitted
  Conditional_Acceptance    // Material accepted with caveats (e.g., minor defect, partial use);
                            // qc_notes ≥ 100 chars required; GRN emitted with conditional flag
}
```

---

## 4. M34-OWNED ENUMS

[§4.1 through §4.11 unchanged from v0.3]

### 4.12 `AuditEventType` (extended in v0.4 + **v0.5**)

**M03-owned event types (locked v0.4):**

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

**M04-owned event types — NEW v0.5** (sourced from `M04_ExecutionCapture_Spec_v1_0.md` Appendix A — 22 events; locked from authoring per Round 18 cascade-pattern discipline):

```
PROGRESS_ENTRY_DECLARED          // Initial Draft insert
PROGRESS_ENTRY_SUBMITTED         // Draft → Submitted; approval_path computed
PROGRESS_ENTRY_APPROVED_QS       // QS_MANAGER signs (intermediate Dual / final Single)
PROGRESS_ENTRY_APPROVED_PD       // PROJECT_DIRECTOR signs (Dual_QS_PD path only)
PROGRESS_ENTRY_APPROVED          // Final Approved; M07/M06/M03 cascades fire
PROGRESS_ENTRY_REJECTED          // QS or PD rejects with reason ≥ 50 chars
PROGRESS_ENTRY_REPEATED_REJECTION  // Decision Queue trigger — > 3 rejections on same entry
MEASUREMENT_CONFIG_LOCKED        // ProgressMeasurementConfig.is_locked=true after first entry
NCR_RAISED                       // ConstructionNCR created
NCR_RESPONSE_RECEIVED            // Contractor response captured
NCR_REINSPECTION_PASS            // Reinspection passed; status → Closed
NCR_REINSPECTION_FAIL            // Decision Queue trigger via daily sweep
NCR_REINSPECTION_PARTIAL         // Partial pass; reinspection_notes required
NCR_CLOSED                       // Final closure
NCR_DISPUTED                     // Contractor disputes liability
NCR_LD_ELIGIBILITY_TOGGLED       // M05 sets ld_eligibility_flag (system-to-system only)
NCR_OPEN_CRITICAL                // Decision Queue trigger — Critical NCR overdue
NCR_OPEN_HIGH                    // Decision Queue trigger — High NCR overdue
MATERIAL_RECEIVED                // MaterialReceipt created
MATERIAL_QC_ACCEPTED             // qc_decision=Accepted; GRN + delivery emit
MATERIAL_QC_REJECTED             // qc_decision=Rejected; return-to-vendor
MATERIAL_QC_CONDITIONAL          // qc_decision=Conditional_Acceptance
MATERIAL_GRN_EMITTED             // GRN signal sent to M06
MATERIAL_RECEIPT_QC_FAIL         // Decision Queue trigger
SCORE_COMPUTED                   // Quarterly ContractorPerformanceScore created
SCORE_OVERRIDDEN                 // PMO manual override
SCORE_APPLIED_TO_PARTY           // M01 cascade fired; Party.long_term_rating updated
CONTRACTOR_SCORE_DECLINE         // Decision Queue trigger — quarterly decline > 10 points
EXEC_CONFIG_CREATED              // ProjectExecutionConfig auto-create on Project Active
EXEC_CONFIG_EDITED               // PMO edit with justification ≥ 100 chars
PHOTO_ATTACHED                   // Stub-period photo URL added
PHOTO_MIGRATED_TO_M12            // One-time migration cascade event when M12 lands
DUAL_SIGNOFF_PENDING             // Decision Queue trigger — awaiting PD signature
PROGRESS_APPROVAL_PENDING        // Decision Queue trigger — Submitted > 48hr
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

### 4.16 `M04_DecisionQueueTriggerType` — **NEW v0.5**

```
PROGRESS_ENTRY_REPEATED_REJECTION    // BR-04-009: same entry rejected > 3 times
PROGRESS_APPROVAL_PENDING            // Submitted entries awaiting QS > 48hr (sweep)
DUAL_SIGNOFF_PENDING                 // BR-04-006: Dual_QS_PD path awaiting PD after QS sign
NCR_OPEN_CRITICAL                    // BR-04-018: Critical NCR past response_due
NCR_OPEN_HIGH                        // BR-04-018: High NCR past response_due
NCR_REINSPECTION_FAIL                // BR-04-020: reinspection_result=Fail; new response_due
MATERIAL_RECEIPT_QC_FAIL             // BR-04-029: qc_decision=Rejected
CONTRACTOR_SCORE_DECLINE             // BR-04-034: quarterly weighted_total decline > 10 pts
```

All UPPER_SNAKE_CASE per F-013 lock. Confirms M04 Spec Appendix A summary count of 8 Decision Queue triggers.

---

## 5. CODEMASTER CATEGORIES — *unchanged from v0.3*

[unchanged]

---

## 6. RESERVED FIELDS — *updated v0.5*

Every entity (except append-only logs and junction tables) MUST include:

```
tenant_id, created_by, created_at, updated_by, updated_at, is_active
```

**Append-only entity exemption (v0.5 explicit list — extended with M04):**
- `BACIntegrityLedger` (M02) — UPDATE/DELETE forbidden at DB level
- `IDGovernanceLog` (M02)
- `CSVImportRecord` (M02)
- `ProjectPhaseHistory` (M01)
- `ProjectStatusHistory` (M01)
- `LoginAttempt` (M34)
- `SystemAuditLog` (M34)
- `Baseline` (M03) — sealed at SG-6; immutable after lock
- `BaselineExtension` (M03) — append-only after approval (no edits to approved extensions)
- `PVProfileSnapshot` (M03) — historical snapshots immutable
- **`ProgressEntryAudit` (M04)** — every state transition; UPDATE/DELETE forbidden at DB level
- **`NCRStatusLog` (M04)** — every NCR transition + severity change; UPDATE/DELETE forbidden
- **`MaterialReceiptLedger` (M04)** — every QC decision + receipt event; UPDATE/DELETE forbidden
- **`ContractorPerformanceScoreLog` (M04)** — every score recompute / override; UPDATE/DELETE forbidden

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
| v0.4 | 2026-05-03 | M03 lock. 12 new M03 ENUMs added (BaselineExtensionCause, LoadingProfileType, ResourceType (4 values incl. Vendor_Resource), ReportingPeriodType, MilestoneStatus, MilestoneType, ScheduleEntryStatus, ProcurementItemStatus, WeatherWindowSeverity, BaselineExtensionStatus, ScheduleImportSource, ScheduleImportMode). M03 audit event types (28) and Decision Queue triggers (5) catalogued. Append-only entity exemption list extended with Baseline + BaselineExtension + PVProfileSnapshot. Cascade: M01 v1.2 removes reporting_period_type; M03 owns. |
| **v0.5** | **2026-05-03** | **M04 lock (Round 20). 8 new M04 ENUMs added (ProgressMeasurementMethod, ProgressApprovalStatus, EVConfidence, NCRStatus, NCRRootCauseCategory, MaterialReceiptStatus, MaterialQCStatus, MaterialQCDecision). M04 audit event types (22 — locked from authoring per Round 18 cascade-pattern) and Decision Queue triggers (8) catalogued. Append-only entity exemption list extended with M04 ledgers (ProgressEntryAudit, NCRStatusLog, MaterialReceiptLedger, ContractorPerformanceScoreLog). EVConfidence carried forward from M07 v3.0 legacy for forward-traceability — M04 writes High/Low; M07 will write Fallback/Derived when built.** |

**Future bumps:**
- v0.6 — after M05 / M06 spec lock
- v0.7 — after M07 / M08 lock
- v0.8 — after M09 / M10 lock
- v1.0 — after all Phase 1 specs locked

---

## 10. ENFORCEMENT — *unchanged*

[unchanged from v0.3]

---

*v0.5 — Living document. M04 ENUMs locked. Next bump on M05 spec lock (or M06 — sequencing TBD).*
