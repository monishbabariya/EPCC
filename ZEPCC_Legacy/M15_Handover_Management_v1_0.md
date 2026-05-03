# M15 — Handover Management
## Module Specification v1.0
**Status:** Draft — Pending PMO Director Review | **Locked:** No
**Spec Author:** PMO Director | **Date:** 2026-05-02
**Reference Standards:** EPCC_Engineering_Standards_v1_2.md
**Layer:** L2 Control
**Navigation Section:** Control (between M09 Compliance and M10 EPCC Command)
**Build Priority:** Phase 1 — Critical (must be complete before first project reaches SG-8)

---

## CHANGE LOG

| Version | Date | Change Summary |
|---------|------|----------------|
| v1.0 | 2026-05-02 | Initial specification. Addresses the complete absence of any pre-handover, commissioning, and handover certificate workflow in EPCC M01–M14. |

---

## WHY THIS MODULE EXISTS

The current system has a critical gap between SG-8 (gate where construction is substantially complete and commissioning begins) and SG-11 (formal project closure/handover). The existing modules handle:
- Construction quality: M04 NCRs
- Post-handover defects: M04 DLPRegister (activated by SG-11)
- Regulatory compliance: M09

But nobody owns:
- Punch list creation and resolution before handover
- System-level commissioning tests and certificates
- O&M documentation assembly and handover
- Client staff training records
- The Handover Certificate itself (the contractual document that defines practical completion)
- The transition from "construction defects" to "DLP defects"

Without M15, the SG-11 gate has nothing to certify. The DLP period starts without a defined baseline of outstanding items. The client has no formal record of what was handed over, what O&M manuals exist, or what warranty commitments were made at handover.

For hospital EPC specifically, the handover to a healthcare operator is not a single event. It spans 3–6 months of pre-commissioning, system commissioning, NABH gap assessment, integrated testing, and finally the formal ceremony with a Taking Over Certificate. EPCC must govern this entire phase.

---

## BLOCK 1 — Identity

```
Module ID             : M15
Module Name           : Handover Management
Layer                 : L2 Control
Decision It Enables   : Has every system been commissioned to specification,
                        every document assembled and transferred, every A-list
                        punch item resolved, every statutory approval received,
                        and every contractual obligation met — such that the
                        Handover Certificate can be issued without legal exposure
                        and the DLP period can begin with a defined, agreed
                        baseline of outstanding items?
Primary User          : PMO Director / Project Director
Secondary Users       : Site Manager, QS Manager, Compliance Manager (M09),
                        Finance Lead
```

### Module Icon: `PackageCheck` (Lucide)

### Users

| Role | Access Level |
|---|---|
| PMO Director | Full — create, edit, approve, issue Handover Certificate |
| Portfolio Manager | Full read, view all projects |
| Project Director | Full — create, edit all records within own project |
| Planning Engineer | Read + update commissioning test records |
| QS Manager | Read + manage O&M document register, punch list items |
| Site Manager | Create punch list items, record commissioning tests, mark training delivered |
| Finance Lead | Read only (Handover Certificate triggers M06 final account) |
| Read-Only | View only |

---

## BLOCK 2 — Scope Boundary

### INCLUDES

| Capability | Description |
|---|---|
| `HandoverPlan` master record | Per-project handover governance record activated at SG-8 |
| Punch List (A-list and B-list) | All pre-handover defects and outstanding items, categorised by commercial significance |
| Commissioning System register | Building systems being tested (HVAC, Fire Alarm, Medical Gas, etc.) |
| Commissioning Test records | Individual tests per system, results, certificates, snagging |
| O&M Document register | Master checklist of all O&M manuals, warranties, certificates to be handed over |
| Client Staff Training register | Training sessions delivered to client operating staff |
| Statutory Document register | All NOCs, completion certificates, licences required at handover |
| Access & Keys handover register | Physical and digital access items transferred at handover |
| Handover Certificate workflow | Drafting, review, joint signing (PMO + client), issuance |
| Handover Readiness Score | CALC: composite % across all handover categories, feeds M08 + M10 |
| B-list → DLP transition | On SG-11 passage, all unclosed B-list items auto-transfer to M04 DLPDefect register |
| Training readiness score | % of mandatory client training sessions delivered |

### EXCLUDES

| Excluded | Where It Lives |
|---|---|
| DLP defect tracking after handover | M04 DLPRegister / DLPDefect |
| NABH accreditation tracking | M09 Compliance Tracker |
| Financial final account, retention release | M06 Financial Control |
| As-built drawing storage and revision control | M12 Document Control + MinIO |
| Equipment calibration during O&M period | Outside EPCC scope |
| O&M period operational management | Outside EPCC scope |
| Warranty claim management post-DLP | Outside EPCC scope |
| Procurement of O&M contracts | Outside EPCC scope |
| Gate passage authority and approval | M08 Gate Control — M15 provides readiness data; M08 owns the decision |

---

## BLOCK 3 — Data Architecture

### 3a. Entity Overview

| Entity | Description | Cardinality |
|---|---|---|
| `HandoverPlan` | Master handover governance record per project. Activated at SG-8. | 1 per project |
| `PunchListItem` | Individual item on the pre-handover punch list. A-list or B-list. | Many per project |
| `CommissioningSystem` | A building/MEP/medical system being commissioned (e.g., HVAC_Block_A, Medical_Gas_ICU) | Many per project |
| `CommissioningTest` | A specific test within a commissioning system | Many per CommissioningSystem |
| `HandoverDocument` | An O&M manual, warranty certificate, or drawing set to be handed over | Many per project |
| `ClientTrainingRecord` | A training session delivered to client staff | Many per project |
| `StatutoryDocument` | A licence, NOC, or completion certificate required at handover | Many per project |
| `AccessHandoverItem` | A key, access card, password, or system credential to be transferred | Many per project |
| `HandoverCertificate` | The formal Taking Over / Completion Certificate | 1 per project |
| `HandoverReadinessSnapshot` | Daily snapshot of readiness score per category | Many per project |

---

### 3b. Entity: `HandoverPlan`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `handover_plan_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | FK → M01 Project. Unique per project. | LINK → M01 Project |
| `contract_id` | UUID | Y | FK → M01 Contract (primary). | LINK → M01 Contract |
| `sg8_passage_id` | UUID | Y | FK → M08 GatePassage (SG-8). Source of plan activation date. Immutable. | LINK → M08 GatePassage |
| `plan_activation_date` | DATE | Y | = SG-8 GatePassage.actual_passage_date. Populated on M08 signal. | LINK → M08 GatePassage |
| `target_handover_date` | DATE | Y | Target date for Handover Certificate issuance. Must be ≥ plan_activation_date + 30 days. PMO Director sets. | INPUT |
| `revised_target_handover_date` | DATE | N | Updated if target slips. Each revision requires 50-char reason. Change logged. | INPUT |
| `contractual_completion_date` | DATE | Y | LINK from M01 Contract / M03 milestone. The date by which practical completion is contractually required. | LINK → M03 |
| `completion_delay_days` | INTEGER | N | CALC: `target_handover_date − contractual_completion_date`. Negative = ahead of schedule. | CALC |
| `handover_readiness_score` | DECIMAL(5,2) | Y | CALC: composite readiness % (see BR-15 rules). Range 0.00–100.00. | CALC |
| `punch_a_total` | INTEGER | Y | CALC: count of PunchListItem where list_type = A | CALC |
| `punch_a_open` | INTEGER | Y | CALC: count of PunchListItem where list_type = A AND status ≠ Closed | CALC |
| `punch_b_total` | INTEGER | Y | CALC: count of PunchListItem where list_type = B | CALC |
| `punch_b_open` | INTEGER | Y | CALC: count of PunchListItem where list_type = B AND status ≠ Closed | CALC |
| `commissioning_systems_total` | INTEGER | Y | CALC: count of CommissioningSystem records | CALC |
| `commissioning_systems_complete` | INTEGER | Y | CALC: count where commissioning_status = Complete | CALC |
| `om_docs_total` | INTEGER | Y | CALC: count of HandoverDocument records | CALC |
| `om_docs_received` | INTEGER | Y | CALC: count where status = Received | CALC |
| `statutory_docs_total` | INTEGER | Y | CALC: count of StatutoryDocument | CALC |
| `statutory_docs_received` | INTEGER | Y | CALC: count where status = Received | CALC |
| `training_sessions_planned` | INTEGER | Y | CALC: count of ClientTrainingRecord | CALC |
| `training_sessions_delivered` | INTEGER | Y | CALC: count where status = Delivered | CALC |
| `handover_certificate_id` | UUID | N | LINK → HandoverCertificate on issuance | LINK → HandoverCertificate |
| `status` | ENUM | Y | `Not_Started / Active / Certificate_Drafted / Certificate_Issued / Closed` | SYSTEM |
| `activated_by` | UUID | N | PMO Director | LINK → M08 GatePassage |
| `activated_at` | TIMESTAMP | N | Auto on SG-8 signal | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

---

### 3c. Entity: `PunchListItem`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `punch_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | LINK → M01 Project |
| `handover_plan_id` | UUID | Y | FK → HandoverPlan | LINK → HandoverPlan |
| `punch_code` | VARCHAR(20) | Y | CALC: `PL-{list_type}-{seq_pad3}`. e.g., PL-A-042, PL-B-018. | CALC |
| `list_type` | ENUM | Y | `A / B`. A = must resolve before Handover Certificate. B = accepted at handover, resolve within DLP. | INPUT |
| `discipline` | ENUM | Y | `Civil / Architectural / MEP_HVAC / MEP_Electrical / MEP_Plumbing / MEP_Fire / Medical_Gas / Medical_Equipment / IT_BMS / Landscaping / Other` | INPUT |
| `wbs_id` | UUID | Y | Location reference. FK → M02 WBSNode. | LINK → M02 WBSNode |
| `package_id` | UUID | Y | FK → M02 Package. | LINK → M02 Package |
| `contract_id` | UUID | Y | Responsible contractor. FK → M01 Contract. | INPUT |
| `description` | TEXT | Y | Min 30 chars. Specific description of the outstanding item. | INPUT |
| `severity` | ENUM | Y | `Critical / High / Medium / Low`. Severity determines resolution SLA. | INPUT |
| `raised_by` | UUID | Y | User who raised it. | SYSTEM |
| `raised_date` | DATE | Y | Date of inspection. Must be ≥ plan_activation_date. | INPUT |
| `photographic_evidence_url` | JSONB | N | MinIO URL array. Mandatory for Critical/High severity. | INPUT |
| `resolution_required` | TEXT | Y | Min 20 chars. What needs to be done to close this item. | INPUT |
| `contractor_response_due` | DATE | Y | CALC: Critical = +3 days, High = +5 days, Medium = +10 days, Low = +15 days from raised_date. | CALC |
| `contractor_response` | TEXT | N | Contractor's proposed resolution. Required before status → In_Progress. | INPUT |
| `resolution_date_planned` | DATE | N | Contractor's planned resolution date. | INPUT |
| `resolution_date_actual` | DATE | N | Actual date item was resolved. | INPUT |
| `reinspection_required` | BOOLEAN | Y | Default true. PMO Director can set false for administrative items only. | INPUT |
| `reinspection_date` | DATE | N | Date of reinspection by PMO team. | INPUT |
| `reinspection_result` | ENUM | N | `Pass / Fail / Partial` | INPUT |
| `reinspection_notes` | TEXT | N | Required if Fail/Partial (min 30 chars). | INPUT |
| `status` | ENUM | Y | `Open / Response_Pending / In_Progress / Reinspection_Pending / Closed / Waived` | SYSTEM |
| `waiver_reason` | TEXT | N | Min 100 chars. Required if status → Waived. PMO Director only. | INPUT |
| `dlp_defect_id` | UUID | N | LINK → M04 DLPDefect. Populated when B-list item transfers to DLP register on SG-11. Immutable once set. | LINK → M04 DLPDefect |
| `transferred_to_dlp` | BOOLEAN | Y | CALC: true if dlp_defect_id is populated. | CALC |
| `closed_at` | TIMESTAMP | N | Auto on status → Closed | SYSTEM |
| `closed_by` | UUID | N | FK → Users | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true. Soft delete on Waived. | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

---

### 3d. Entity: `CommissioningSystem`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `commissioning_system_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | LINK |
| `handover_plan_id` | UUID | Y | FK → HandoverPlan | LINK |
| `system_code` | VARCHAR(30) | Y | CALC: `CS-{discipline_prefix}-{seq_pad3}`. e.g., CS-HVAC-001, CS-MG-002 | CALC |
| `system_name` | VARCHAR(200) | Y | Descriptive name. e.g., "HVAC — OT Suite Block C" | INPUT |
| `discipline` | ENUM | Y | Same as PunchListItem.discipline ENUM | INPUT |
| `wbs_id` | UUID | N | Area/zone reference | LINK → M02 WBSNode |
| `package_id` | UUID | Y | FK → M02 Package | LINK → M02 Package |
| `contract_id` | UUID | Y | Commissioning contractor | INPUT |
| `commissioning_authority` | ENUM | Y | `Contractor_Self / PMC_Witnessed / Third_Party_Agency / OEM_Engineer / Regulatory_Body` | INPUT |
| `commissioning_agency_name` | VARCHAR(200) | N | Required if commissioning_authority = Third_Party_Agency or Regulatory_Body | INPUT |
| `planned_start_date` | DATE | Y | Must be ≥ plan_activation_date | INPUT |
| `planned_completion_date` | DATE | Y | Must be > planned_start_date | INPUT |
| `actual_start_date` | DATE | N | Actual start | INPUT |
| `actual_completion_date` | DATE | N | Actual completion | INPUT |
| `test_protocol_document_id` | UUID | N | FK → M12 DrawingRegister or M15 HandoverDocument (test protocol reference) | LINK → M12 |
| `total_tests` | INTEGER | Y | CALC: count of CommissioningTest records for this system | CALC |
| `tests_passed` | INTEGER | Y | CALC: count where test_result = Pass | CALC |
| `tests_failed` | INTEGER | Y | CALC: count where test_result = Fail | CALC |
| `tests_pending` | INTEGER | Y | CALC: count where test_result = Pending | CALC |
| `commissioning_certificate_url` | VARCHAR(500) | N | MinIO URL. Required before commissioning_status → Complete. | INPUT |
| `commissioning_status` | ENUM | Y | `Not_Started / Pre_Commissioning / Testing_In_Progress / Snag_Clearance / Complete / Failed` | SYSTEM |
| `nabh_relevance` | BOOLEAN | Y | True if this system is a NABH inspection item (HVAC, Medical Gas, Sterilisation). Feeds M09. | INPUT |
| `nabh_compliance_item_id` | UUID | N | FK → M09 ComplianceItem if nabh_relevance = true. | LINK → M09 |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

---

### 3e. Entity: `CommissioningTest`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `test_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `commissioning_system_id` | UUID | Y | FK → CommissioningSystem | LINK |
| `project_id` | UUID | Y | — | LINK |
| `test_code` | VARCHAR(30) | Y | CALC: `{system_code}-T{seq_pad3}`. e.g., CS-HVAC-001-T001 | CALC |
| `test_name` | VARCHAR(200) | Y | e.g., "Air Change Rate Measurement — ICU Zone", "Medical Gas Purity Test — ICU Manifold" | INPUT |
| `test_type` | ENUM | Y | `Pre_Commissioning / Performance / Integrated / Acceptance / Regulatory` | INPUT |
| `test_date` | DATE | N | Date test was conducted | INPUT |
| `tested_by` | UUID | N | FK → Users or text for external agency | INPUT |
| `test_parameters` | JSONB | N | Key-value pairs of measured values vs. specifications. e.g., {"air_change_rate_measured": 22, "specification_min": 20} | INPUT |
| `test_result` | ENUM | Y | `Pending / Pass / Fail / Partial_Pass` | INPUT |
| `snag_list` | TEXT | N | Any deficiencies observed during testing. | INPUT |
| `snag_resolution_date` | DATE | N | When snags from this test were resolved | INPUT |
| `retest_required` | BOOLEAN | Y | CALC: true if test_result = Fail or Partial_Pass | CALC |
| `retest_date` | DATE | N | Date of retest | INPUT |
| `retest_result` | ENUM | N | `Pass / Fail` | INPUT |
| `certificate_issued` | BOOLEAN | Y | Default false. Set true when commissioning certificate is issued for this test. | INPUT |
| `certificate_url` | VARCHAR(500) | N | MinIO URL of test certificate. Required if certificate_issued = true. | INPUT |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

---

### 3f. Entity: `HandoverDocument`

One record per document (O&M manual, warranty, as-built drawing set, test report) to be formally handed over to the client.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `doc_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | LINK |
| `handover_plan_id` | UUID | Y | FK → HandoverPlan | LINK |
| `doc_code` | VARCHAR(20) | Y | CALC: `HD-{seq_pad3}` | CALC |
| `document_title` | VARCHAR(300) | Y | Min 10 chars | INPUT |
| `document_type` | ENUM | Y | `OM_Manual / Warranty_Certificate / As_Built_Drawing_Set / Test_Certificate / Training_Material / Statutory_Licence / Insurance_Certificate / Equipment_Manual / Other` | INPUT |
| `discipline` | ENUM | Y | See PunchListItem.discipline ENUM | INPUT |
| `package_id` | UUID | N | FK → M02 Package (if package-specific) | LINK → M02 |
| `responsible_party` | UUID | Y | FK → M01 Contract. Party responsible for providing this document. | INPUT |
| `required_by_nabh` | BOOLEAN | Y | Default false. If true, M09 is notified. | INPUT |
| `due_date` | DATE | Y | Date by which the document must be received. Must be ≤ target_handover_date. | INPUT |
| `status` | ENUM | Y | `Not_Submitted / Submitted_For_Review / Under_Review / Rejected / Received` | SYSTEM |
| `submitted_date` | DATE | N | Date document was submitted by responsible party | INPUT |
| `review_notes` | TEXT | N | PMO review notes on the submission | INPUT |
| `rejection_reason` | TEXT | N | Min 30 chars. Required if status → Rejected. | INPUT |
| `document_url` | VARCHAR(500) | N | MinIO URL of received document. Required when status → Received. | INPUT |
| `m12_drawing_id` | UUID | N | FK → M12 DrawingRecord if document is an as-built drawing. | LINK → M12 |
| `hard_copy_required` | BOOLEAN | Y | Default false. Some statutory bodies require original hard copies. | INPUT |
| `hard_copy_received` | BOOLEAN | Y | Default false. Set true when hard copy confirmed received. | INPUT |
| `received_date` | DATE | N | Date document confirmed received | INPUT |
| `received_by` | UUID | N | FK → User who confirmed receipt | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

---

### 3g. Entity: `StatutoryDocument`

Licences, NOCs, and completion certificates required from government authorities before handover is legally valid.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `statutory_doc_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | LINK |
| `handover_plan_id` | UUID | Y | FK → HandoverPlan | LINK |
| `doc_code` | VARCHAR(20) | Y | CALC: `SD-{seq_pad3}` | CALC |
| `document_title` | VARCHAR(300) | Y | e.g., "Occupancy Certificate", "Fire NOC (Final)", "Lift Inspection Certificate", "AERB Regulatory Approval" | INPUT |
| `issuing_authority` | VARCHAR(200) | Y | e.g., "KDMC", "Fire Department", "AERB", "Electrical Inspector" | INPUT |
| `regulatory_reference` | VARCHAR(200) | N | Act/Rule reference. e.g., "Maharashtra Regional and Town Planning Act 1966 — Section 45" | INPUT |
| `is_mandatory_for_occupancy` | BOOLEAN | Y | True if the building cannot be occupied without this document. These are SG-10/SG-11 gate blockers. | INPUT |
| `application_submitted_date` | DATE | N | Date application was submitted to the authority | INPUT |
| `application_reference` | VARCHAR(100) | N | Application number from the authority | INPUT |
| `expected_receipt_date` | DATE | N | Expected date of receipt based on authority timelines | INPUT |
| `status` | ENUM | Y | `Not_Applied / Applied / Under_Review / Additional_Info_Requested / Received / Rejected` | SYSTEM |
| `document_url` | VARCHAR(500) | N | MinIO URL. Required when status → Received. | INPUT |
| `received_date` | DATE | N | Date document received | INPUT |
| `expiry_date` | DATE | N | If the document has an expiry (some NOCs have 1-year validity) | INPUT |
| `m09_compliance_item_id` | UUID | N | FK → M09 ComplianceItem if this mirrors a tracked compliance item | LINK → M09 |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

**System-shipped statutory documents (pre-loaded on healthcare project creation, mirrors M09 compliance items):**
- Occupancy Certificate (KDMC/Local Authority)
- Fire NOC — Final Certificate
- Lift Inspection Certificate (Electrical Inspectorate)
- Electrical Inspector NOC — Final
- AERB Regulatory Approval (if radiation equipment present)
- PCB Consent to Operate (CTO)
- MSEDCL Permanent Connection
- BOCW Registration Closure
- Water Connection Final Certificate

---

### 3h. Entity: `ClientTrainingRecord`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `training_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | LINK |
| `handover_plan_id` | UUID | Y | FK → HandoverPlan | LINK |
| `training_code` | VARCHAR(20) | Y | CALC: `TR-{seq_pad3}` | CALC |
| `training_title` | VARCHAR(200) | Y | e.g., "HVAC BMS Operations Training", "Medical Gas Safety Training", "Fire Alarm Panel Operations" | INPUT |
| `system_reference` | UUID | N | FK → CommissioningSystem if training covers a commissioned system | LINK → CommissioningSystem |
| `trainer_name` | VARCHAR(200) | Y | Name and organisation of trainer (often OEM/contractor engineer) | INPUT |
| `trainer_type` | ENUM | Y | `OEM_Engineer / Contractor / PMC_Staff / External_Agency` | INPUT |
| `planned_date` | DATE | Y | Must be before target_handover_date | INPUT |
| `actual_date` | DATE | N | Actual delivery date | INPUT |
| `duration_hours` | DECIMAL(4,1) | Y | Min 0.5 hours | INPUT |
| `participants_count` | INTEGER | N | Number of client staff trained | INPUT |
| `attendance_sheet_url` | VARCHAR(500) | N | MinIO URL of signed attendance sheet | INPUT |
| `training_material_url` | VARCHAR(500) | N | MinIO URL of training material | INPUT |
| `status` | ENUM | Y | `Planned / Delivered / Client_Signed_Off / Cancelled` | SYSTEM |
| `client_signoff_by` | VARCHAR(200) | N | Name of client representative who signed off | INPUT |
| `client_signoff_date` | DATE | N | Date of client sign-off | INPUT |
| `is_nabh_required` | BOOLEAN | Y | True if NABH requires this training (e.g., infection control, medical gas safety). Links to M09. | INPUT |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

---

### 3i. Entity: `AccessHandoverItem`

Physical keys, access cards, digital credentials, and system accounts transferred to the client at handover.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `access_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | LINK |
| `handover_plan_id` | UUID | Y | FK → HandoverPlan | LINK |
| `item_code` | VARCHAR(20) | Y | CALC: `AH-{seq_pad3}` | CALC |
| `item_description` | VARCHAR(300) | Y | e.g., "Main entrance master keys (3 sets)", "BMS supervisor login credentials", "DG set control panel key" | INPUT |
| `item_type` | ENUM | Y | `Physical_Key / Access_Card / Digital_Credential / System_Account / Manual_Password / Other` | INPUT |
| `quantity` | INTEGER | Y | Min 1 | INPUT |
| `location_description` | VARCHAR(200) | Y | Where this provides access | INPUT |
| `received_by_name` | VARCHAR(200) | N | Name of client representative who received. Required when status → Handed_Over. | INPUT |
| `received_by_designation` | VARCHAR(200) | N | Designation of client representative | INPUT |
| `handover_date` | DATE | N | Date of handover | INPUT |
| `receipt_document_url` | VARCHAR(500) | N | MinIO URL of signed receipt | INPUT |
| `status` | ENUM | Y | `Pending / Handed_Over` | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

---

### 3j. Entity: `HandoverCertificate`

The formal Taking Over Certificate / Practical Completion Certificate. The contractually significant document that defines the start of the DLP period and releases certain financial obligations.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `certificate_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | LINK → M01 Project |
| `handover_plan_id` | UUID | Y | FK → HandoverPlan. One certificate per plan. | LINK → HandoverPlan |
| `certificate_code` | VARCHAR(30) | Y | CALC: `HOC-{project_code}-{year}`. e.g., HOC-KDMC-001-DBOT-2026. | CALC |
| `draft_prepared_by` | UUID | Y | PMO Director or Project Director | SYSTEM |
| `draft_prepared_at` | TIMESTAMP | Y | Auto on draft creation | SYSTEM |
| `practical_completion_date` | DATE | Y | The contractual date of practical completion. This is the DLP start date. Must match HandoverPlan readiness criteria. | INPUT (PMO Director) |
| `scope_included` | TEXT | Y | Min 100 chars. Narrative of what is included in the handover scope. | INPUT |
| `scope_excluded` | TEXT | N | Items explicitly excluded from this handover (e.g., Phase 2 equipment). | INPUT |
| `punch_b_items_count` | INTEGER | Y | CALC: count of PunchListItem where list_type = B AND status ≠ Closed at certificate issue date. These items transfer to DLP. | CALC |
| `punch_b_completion_commitment` | TEXT | N | Contractor's commitment for B-list item resolution (dates, resources). Required if punch_b_items_count > 0. Min 50 chars. | INPUT |
| `warranty_period_years` | INTEGER | Y | LINK from M01 Contract.warranty_period_years (if defined). | LINK → M01 |
| `dlp_start_date` | DATE | Y | = practical_completion_date | CALC |
| `dlp_end_date` | DATE | Y | CALC = dlp_start_date + M01 Contract.dlp_term_days | CALC |
| `pmc_signatory_name` | VARCHAR(200) | Y | Full name of PMO authorised signatory | INPUT |
| `pmc_signed_at` | TIMESTAMP | N | Timestamp of PMO signature | SYSTEM |
| `client_signatory_name` | VARCHAR(200) | N | Full name of client authorised signatory | INPUT |
| `client_signatory_designation` | VARCHAR(200) | N | Designation of client signatory | INPUT |
| `client_signed_at` | TIMESTAMP | N | Timestamp of client signature | SYSTEM |
| `contractor_signatory_name` | VARCHAR(200) | N | Full name of main contractor signatory | INPUT |
| `contractor_signed_at` | TIMESTAMP | N | Timestamp of contractor signature | SYSTEM |
| `certificate_document_url` | VARCHAR(500) | N | MinIO URL of executed certificate (scanned signed document). Required for status → Executed. | INPUT |
| `status` | ENUM | Y | `Draft / Under_Review / PMC_Signed / All_Signed / Executed` | SYSTEM |
| `sg11_passage_triggered` | BOOLEAN | Y | CALC: true when status → All_Signed. Triggers SG-11 gate signal to M08. | CALC |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

---

### 3k. Entity: `HandoverReadinessSnapshot`

Daily snapshot of handover readiness, per category, used for M10 trending and M08 gate criterion verification.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `snapshot_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | LINK |
| `snapshot_date` | DATE | Y | Date of snapshot | SYSTEM |
| `overall_readiness_score` | DECIMAL(5,2) | Y | Weighted composite (see scoring formula) | CALC |
| `punch_a_score` | DECIMAL(5,2) | Y | % A-list items closed. Weight: 35%. | CALC |
| `commissioning_score` | DECIMAL(5,2) | Y | % systems commissioned (Complete status). Weight: 25%. | CALC |
| `om_docs_score` | DECIMAL(5,2) | Y | % O&M documents received. Weight: 20%. | CALC |
| `statutory_docs_score` | DECIMAL(5,2) | Y | % statutory documents received. Weight: 15%. | CALC |
| `training_score` | DECIMAL(5,2) | Y | % client training sessions delivered. Weight: 5%. | CALC |
| `days_to_target` | INTEGER | Y | CALC: HandoverPlan.target_handover_date − snapshot_date | CALC |
| `is_sg10_eligible` | BOOLEAN | Y | CALC: overall_readiness_score ≥ 80.00 AND punch_a_open ≤ 5 | CALC |
| `is_sg11_eligible` | BOOLEAN | Y | CALC: overall_readiness_score ≥ 95.00 AND punch_a_open = 0 AND HandoverCertificate.status ∈ (All_Signed, Executed) | CALC |

**Readiness Scoring Formula:**
```
overall_readiness_score =
  (punch_a_closed / punch_a_total × 100) × 0.35
  + (commissioning_complete / commissioning_total × 100) × 0.25
  + (om_docs_received / om_docs_total × 100) × 0.20
  + (statutory_docs_received / statutory_docs_total × 100) × 0.15
  + (training_delivered / training_planned × 100) × 0.05

Edge cases:
  If any denominator = 0: that category scores 100% (no items = fully met by absence).
  B-list punch items excluded from punch_a score entirely (they are accepted deficiencies).
  Waived punch items count as Closed for scoring purposes.
```

---

## BLOCK 4 — Data Population Rules

### 4a. Role Permission Matrix

| Action | PMO Dir | Project Dir | Planning Eng | QS Mgr | Site Mgr | Finance Lead | Read-Only |
|---|---|---|---|---|---|---|---|
| Create PunchListItem | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ |
| Change list_type A↔B | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Close PunchListItem | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Waive PunchListItem | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Create CommissioningSystem | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Record CommissioningTest | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Mark system Complete | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Manage HandoverDocument | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Manage StatutoryDocument | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Record ClientTraining | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Record AccessHandover | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Draft HandoverCertificate | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Sign HandoverCertificate (PMC) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Set target_handover_date | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## BLOCK 5 — Filters and Views

### 5a. Handover Dashboard (M15 Home — per project)

```
Header row (KPIs):
  [Overall Readiness Score] [Days to Target] [A-List Open] [Systems Complete] [Docs Received]

Readiness breakdown panel:
  Horizontal gauge per category:
    Punch List A:     [████████░░] 82%
    Commissioning:    [███████░░░] 74%
    O&M Documents:    [█████░░░░░] 51%
    Statutory Docs:   [████████░░] 80%
    Client Training:  [███░░░░░░░] 35%
    OVERALL:          [████████░░] 73%

Two-panel below:
  Left: Punch List filtered view (default: A-list open, sorted by severity)
  Right: Commissioning Systems filtered view (default: In Progress, sorted by planned_completion)
```

### 5b. Punch List View

```
Filter bar: list_type | severity | discipline | status | contractor | overdue (toggle)
Table: PL Code | Description | Type | Severity | Discipline | Contractor | Status | Due Date | Overdue?
Sort default: A-list Critical → A-list High → A-list Medium → B-list (collapsed)
RAG row: Overdue A-list → red. Near-overdue (< 3 days) → amber.
```

### 5c. Commissioning Tracker View

```
Group by: CommissioningSystem (expandable)
Per system header: System Code | Name | Discipline | Status | Tests n/m | % complete
Per test row (expanded): Test Code | Test Name | Date | Result | Certificate | Retest?
```

### 5d. M10 Integration Surface

```
On M10 project detail panel (post-SG-8):
  Handover Readiness: [██████░░░░] 61%
  A-List Open: 14 items  ·  Days to Target: 43
  [View Handover Plan →] → navigates to M15

On M10 portfolio grid (post-SG-8):
  Project card secondary badge: "HANDOVER: 61%" — amber below 80%, red below 60%
```

---

## BLOCK 6 — Business Rules

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---|---|---|---|---|
| BR-15-001 | M08 SG-8 gate passage signal received | Validate: SG-8 passage confirmed. | Create HandoverPlan (status → Active). Send M08 confirmation. PMO Director notification: "Handover Plan activated for {project_code}. Target handover: {target_handover_date} — not yet set. Set target date within 48hr." | 🔴 Real-time |
| BR-15-002 | HandoverPlan created without target_handover_date | On creation (SG-8 signal auto-creates without date) | Create ActionItem (M11): "Set target handover date for {project_code}. Required within 48hr of SG-8 passage." Priority = High. Assigned to PMO Director. | 🔴 Real-time |
| BR-15-003 | PunchListItem created with severity = Critical or High | On creation | Validate: photographic_evidence_url must have ≥ 1 entry. Block save if missing. Error: "Critical/High punch items require photographic evidence." | 🔴 Real-time |
| BR-15-004 | PunchListItem.contractor_response_due passes with status still Open | Daily check | Status auto-transitions to Response_Pending. Decision Queue item: type = PUNCH_LIST_RESPONSE_OVERDUE, severity = HIGH (A-list Critical/High) or MEDIUM (A-list Medium/Low, B-list), owner = Project Director, SLA = 24hr. | 🟢 24hr |
| BR-15-005 | CommissioningTest.test_result set to Fail | On save | Set CommissioningTest.retest_required = true. Alert to Site Manager and Project Director: "Commissioning test failed: {system_name} — {test_name}. Snag resolution and retest required." | 🔴 Real-time |
| BR-15-006 | CommissioningSystem — all tests Passed or Fail_Accepted | CALC when test results update | Validate: at least one CommissioningTest exists, all test_results ≠ Pending. Set commissioning_status = Complete. If nabh_relevance = true: signal to M09 ComplianceItem update. | 🔴 Real-time |
| BR-15-007 | HandoverReadinessSnapshot daily calculation | Celery Beat 7am IST | For all active HandoverPlans: calculate per-category scores and overall_readiness_score. Write HandoverReadinessSnapshot. Update HandoverPlan readiness fields. Signal to M10 for dashboard badge update. | 🟢 24hr |
| BR-15-008 | overall_readiness_score drops below 80% with ≤ 21 days to target | On BR-15-007 completion | Decision Queue item: type = HANDOVER_READINESS_AT_RISK, severity = HIGH, owner = PMO Director, SLA = 24hr, context = {score, days_to_target, lowest_category}. | 🟢 24hr |
| BR-15-009 | HandoverDocument.due_date passes with status ≠ Received | Daily check | Status → Not_Submitted or remains current. Decision Queue: type = HANDOVER_DOCUMENT_OVERDUE, severity = HIGH (mandatory_for_occupancy = true) or MEDIUM, owner = QS Manager, SLA = 48hr. | 🟢 24hr |
| BR-15-010 | StatutoryDocument is_mandatory_for_occupancy = true AND status ≠ Received | When target_handover_date is ≤ 30 days away | Decision Queue: type = STATUTORY_DOC_CRITICAL, severity = CRITICAL, owner = PMO Director, SLA = 24hr. Badge on M10: "STATUTORY DOC OUTSTANDING — {doc_title}". | 🟡 2-4hr |
| BR-15-011 | HandoverCertificate creation attempted | On create | Validate: (1) HandoverPlan.punch_a_open = 0 (no A-list items unresolved) OR PMO Director explicit override with 200-char reason. (2) HandoverPlan.overall_readiness_score ≥ 90%. (3) All is_mandatory_for_occupancy StatutoryDocuments have status = Received. If any fail: block. Return specific failures. | 🔴 Real-time |
| BR-15-012 | HandoverCertificate.status → All_Signed | On contractor signature | (1) Trigger SG-11 gate passage signal to M08. (2) Trigger B-list transfer: create M04 DLPDefect for each open B-list PunchListItem. (3) Set HandoverPlan.status → Certificate_Issued. (4) Signal M06: practical_completion_date confirmed → DLP retention period starts. (5) Notify Finance Lead, PMO Director, Portfolio Manager. (6) PMO Director notification: "Handover Certificate executed for {project_code}. DLP period starts {practical_completion_date}. {punch_b_items_count} B-list items transferred to DLP." | 🔴 Real-time |
| BR-15-013 | B-list PunchListItem transferred to DLP (on BR-15-012) | For each open B-list item on certificate execution | Create M04 DLPDefect with: project_id, dlp_id (from newly created DLPRegister), description from PunchListItem.description, defect_type mapped from discipline, defect_severity = PunchListItem.severity, date_observed = HandoverCertificate.practical_completion_date, rectification_required = PunchListItem.resolution_required. Set PunchListItem.dlp_defect_id = new DLPDefect.defect_id. Set PunchListItem.transferred_to_dlp = true. | 🔴 Real-time |
| BR-15-014 | CommissioningSystem.nabh_relevance = true AND commissioning_status → Complete | On commissioning complete | Signal M09: update linked ComplianceItem.document_received_date = ActualCompletionDate. | 🔴 Real-time |
| BR-15-015 | target_handover_date revised (delayed) | On HandoverPlan.revised_target_handover_date saved | CALC new completion_delay_days. If delay > 7 days: Decision Queue item: HANDOVER_DATE_SLIPPAGE, severity = HIGH, owner = PMO Director. If delay pushes past contractual_completion_date: severity = CRITICAL. Auto-create M05 Schedule_Event risk entry for the delay. | 🔴 Real-time |
| BR-15-016 | PunchListItem.list_type changed from A to B | On update | Validate: only PMO Director can change list type. Require 100-char reason. AuditLog entry with from/to values and justification. Alert Finance Lead: "Punch list item reclassified A→B: {punch_code}. {description}. This item will transfer to DLP on handover." | 🔴 Real-time |

---

## BLOCK 7 — Integration Points

| Direction | Module | Data Exchanged | Trigger | Speed Tier |
|---|---|---|---|---|
| RECEIVES FROM | M08 Gate Control | SG-8 gate passage signal: project_id, sg8_passage_id, actual_passage_date | On SG-8 gate passage | 🔴 Real-time |
| SENDS TO | M08 Gate Control | Handover readiness score + is_sg10_eligible + is_sg11_eligible flags | Daily (BR-15-007) + on certificate execution | 🟢 24hr + 🔴 RT |
| SENDS TO | M08 Gate Control | SG-11 gate passage trigger on HandoverCertificate All_Signed (BR-15-012) | On certificate execution | 🔴 Real-time |
| SENDS TO | M04 Execution Capture | B-list PunchListItem transfer: create DLPDefect records (BR-15-013) | On HandoverCertificate All_Signed | 🔴 Real-time |
| SENDS TO | M06 Financial Control | practical_completion_date + dlp_start_date + dlp_end_date confirmation | On HandoverCertificate All_Signed | 🔴 Real-time |
| SENDS TO | M09 Compliance Tracker | Commissioning completion signals for NABH-linked systems (BR-15-014) | On CommissioningSystem Complete | 🔴 Real-time |
| RECEIVES FROM | M09 Compliance Tracker | NABH compliance readiness signals for commissioning-relevant items | On M09 ComplianceItem status change | 🟡 2-4hr |
| SENDS TO | M10 EPCC Command | Handover readiness score, A-list open count, days to target | Daily snapshot (BR-15-007) | 🟢 24hr |
| SENDS TO | M11 Action Register | Auto-created ActionItems for overdue documents, readiness risks | On BR-15-002, BR-15-008 | 🔴 Real-time |
| LINKS TO | M12 Document Control | As-built drawing reference via HandoverDocument.m12_drawing_id | On as-built drawing received | 🔴 Real-time |
| RECEIVES FROM | M03 Planning | contractual_completion_date via milestone link | On M03 milestone reference | LINK |

---

## BLOCK 8 — Governance and Audit

| Action | Logged | Detail Level | Visible To | Retention |
|---|---|---|---|---|
| PunchListItem created | Yes | All fields | PMO Director, Project Director | Project lifetime |
| list_type changed A↔B | Yes | Old value, new value, reason, PMO Director | PMO Director, Finance Lead | Permanent |
| PunchListItem Waived | Yes | reason, waiver approver | PMO Director | Permanent |
| CommissioningTest result recorded | Yes | All test parameters | PMO Director, Project Director, Site Manager | Project lifetime |
| CommissioningSystem marked Complete | Yes | Approver, date, certificate reference | All | Project lifetime |
| HandoverDocument received | Yes | Document URL, received by, date | All | Permanent |
| StatutoryDocument received | Yes | Document URL, received by, date | All | Permanent |
| HandoverCertificate created | Yes | All fields, drafter | PMO Director, Portfolio Manager | Permanent |
| HandoverCertificate signed (each party) | Yes | Signatory name, designation, timestamp | All | Permanent |
| HandoverCertificate executed | Yes | All three parties, practical_completion_date | All | Permanent |
| B-list transfer to DLP | Yes | Each PunchListItem → DLPDefect mapping | PMO Director, Finance Lead | Permanent |
| target_handover_date revised | Yes | Old date, new date, reason, delay_days | PMO Director, Portfolio Manager | Project lifetime |

**Immutability rules:**
- HandoverCertificate once at `Executed` status cannot be edited. It is a permanent legal record.
- The `practical_completion_date` on an Executed certificate cannot be changed without PMO Director override + 200-char reason + ViolationLog entry.
- DLP transfer records (PunchListItem.dlp_defect_id mapping) are immutable once set.

---

## BLOCK 9 — Explicit Exclusions

```
This module does NOT:
────────────────────────────────────────────────────────────────────────
[ ] Manage DLP defects after handover                         → M04 DLPRegister / DLPDefect
[ ] Track NABH accreditation compliance                       → M09 Compliance Tracker
[ ] Issue financial certificates or release retention         → M06 Financial Control
[ ] Store as-built drawings or manage drawing revisions       → M12 Document Control
[ ] Manage the DLP period or retention release                → M04 + M06
[ ] Own gate passage decisions (SG-8, SG-10, SG-11)          → M08 Gate Control
[ ] Calculate LD during the handover period                   → M05 / M06 (LD calculation is pre-handover)
[ ] Manage O&M contracts during operations                    → Outside EPCC scope
[ ] Track equipment calibration or maintenance after handover → Outside EPCC scope (OAM phase)
[ ] Manage warranty claims post-DLP expiry                    → Outside EPCC scope
[ ] Calculate practical completion date independently         → PMO Director inputs; contractual_completion_date from M03
[ ] Commission individual equipment (handled by OEM)          → OEM-specific process; M15 records the outcome
```

---

## BLOCK 10 — Open Questions

**All v1.0 questions resolved. Zero open questions.**

| # | Question | Resolution |
|---|----------|-----------|
| 1 | When does M15 activate — SG-8 or earlier? | SG-8. Pre-commissioning work (creating the punch list, identifying commissioning systems) should begin as soon as construction is substantially complete, which is what SG-8 signifies. Starting earlier risks tracking incomplete systems. Starting later compresses the handover timeline. SG-8 is the correct trigger. |
| 2 | Who owns the Handover Certificate — the PMC or the contractor? | The PMC (EPCC system user) issues the Taking Over Certificate on behalf of the employer/client. The contractor receives and countersigns it. The PMO Director is the PMC signatory. Client and contractor countersign. All three signatures are tracked. |
| 3 | Can a Handover Certificate be issued with A-list items still open? | No, by default. BR-15-011 blocks creation. However, PMO Director can override with a 200-char written justification (e.g., non-critical administrative items). This is logged permanently and is the PMO Director's personal accountability. |
| 4 | What happens to A-list items that are waived? | They count as closed for readiness scoring (waiver = accepted, resolved by governance decision). The waiver reason is permanently logged. The item does NOT transfer to DLP. |
| 5 | Should B-list items all auto-transfer to DLP, or only unclosed ones? | Only unclosed B-list items transfer. B-list items closed before certificate execution are legitimate pre-handover resolutions — no DLP record needed. Only items outstanding at the moment of certificate execution transfer to M04 DLPDefect. |
| 6 | What if the client refuses to sign the Handover Certificate? | This is a contractual dispute. M15 records the PMC and contractor signatures. A separate `HandoverCertificateDispute` entity (added in v1.1 if needed) can track the formal dispute. The PMO Director can proceed with a unilateral certificate (signed by PMC and contractor only) in some contracts — this should be governed by the contract terms in M01 and documented with a ViolationLog note. |
| 7 | Where do AERB and other radiation-specific commissioning tests sit? | CommissioningSystem with discipline = Medical_Equipment and nabh_relevance = true (or a separate aerb_relevance flag in v1.1). The commissioning certificate from AERB is tracked as a StatutoryDocument (is_mandatory_for_occupancy = true for LINAC). |
| 8 | How does M15 know which O&M manuals are required? | The initial HandoverDocument checklist is system-shipped per sector template (Healthcare_NABH_DBOT), similar to M09's compliance checklist. The PMO Director reviews and adds project-specific items. The template ensures no critical O&M document (HVAC manual, medical gas safety manual, fire alarm programming guide) is missed. |

---

*Spec complete. Zero open questions.*
*M15 activates on SG-8 passage. Executes the Handover Certificate. Triggers SG-11 and DLP on certificate execution.*
*Memory file update required: §7.139 — M15 Handover Management v1.0.*
