---
artefact: M04_ExecutionCapture_Spec_v1_0a
round: 20 (patched Round 29)
date: 2026-05-04
author: Monish (with Claude assist)
x8_version: v0.6a
x9_version: v0.4
status: LOCKED
prior_version: M04_ExecutionCapture_Brief_v1_0 (Round 19)
reference_standards: EPCC_NamingConvention_v1_0.md, X8_GlossaryENUMs_v0_6a.md, X9_VisualisationStandards_Spec_v0_4.md, M34_SystemAdminRBAC_Spec_v1_0.md, M01_ProjectRegistry_Spec_v1_0.md (+ v1_1_CascadeNote + v1_2_CascadeNote + v1_3_CascadeNote), M02_StructureWBS_Spec_v1_0.md, M03_PlanningMilestones_Spec_v1_1.md (+ v1_2_CascadeNote)
re_issue_of: ZEPCC_Legacy/M04_Execution_Capture_v2_2.md (amendment-only — base v2.0/v2.1 not in legacy)
---

# M04 — Execution Capture — Spec v1.0

## CHANGE LOG

| Version | Date | Author | Change Summary |
|---|---|---|---|
| v1.0a  | 2026-05-04 | Monish (with Claude assist) | M19 in-place patch (Round 29 audit): X8 stamp v0.4→v0.6a, X9 stamp v0.2→v0.4, all "cascade pending" annotations cleared (X8 v0.5 M04 ENUMs + X9 v0.3 §13.3.3 row both LOCKED); reference_standards refreshed with M01 v1_3_CascadeNote + M03 v1_2_CascadeNote forward-pointers. No scope, BR, entity, or field change. |
| v1.0 | 2026-05-03 | Monish (with Claude assist) | Initial standalone consolidated spec (Round 20). All 13 OQ items from Brief v1.0 (Round 19) carried as locked. Slim-core scope — DLP→M15, HSE→M31, BOQ-grain→M14, docs→M12, daily diary→M16. Three-state ProgressEntry approval (Draft → Submitted → Approved/Rejected). 4-tier ConstructionNCR severity (reuse X8 Severity ENUM). Dual sign-off above ₹50L threshold (default; configurable via M04-owned `ProjectExecutionConfig` per OQ-2.6 resolution below). Photo storage stubbed (MinIO direct URLs) until M12 lands; migration path documented. 9 entities including 4 append-only ledgers with DB-level UPDATE/DELETE forbidden. 39 BRs. Audit Events Catalogue locked from authoring (Appendix A — 22 events) per Round 18 cascade-pattern discipline. |

---

## BLOCK 1 — IDENTITY

```
Module ID                : M04
Module Name              : Execution Capture
Layer                    : L2 — Execution
Decision It Enables      : Is what's actually happening on site matching what
                           was planned, and where it isn't, what is the
                           commercial and schedule consequence?
Primary User             : SITE_MANAGER (data entry)
Secondary Users          : QS_MANAGER (single & dual approvals),
                           PROJECT_DIRECTOR (escalations + dual-signoff above ₹50L),
                           PMO_DIRECTOR (NCR pipeline + contractor scoring oversight),
                           PROCUREMENT_OFFICER (material receipts + GRN signal)
Build Priority           : 🔴 Critical (precedes M05, M06, M07, M14)
Folder                   : SystemAdmin/Modules/ (per Round 18 audit canonical placement)
Re-Issue Of              : Legacy `M04_Execution_Capture_v2_2.md` (amendment file; base v2.0/v2.1 not in legacy — full scope reverse-engineered from v2.2 + cross-references)
```

---

## BLOCK 2 — SCOPE BOUNDARY

| INCLUDES | EXCLUDES |
|---|---|
| ProgressEntry capture per WBS node × period (M03's `reporting_period_type`) | DLP register + DLP defects → **M15 HandoverManagement** (per Brief OQ-1.1=B) |
| Three-state ProgressEntry approval flow with dual-signoff threshold | HSE incident capture → **M31 HSESafetyManagement** (per OQ-1.1=B) |
| ProgressMeasurementConfig — locks the method (Units / Steps / Milestone / Subjective_Estimate) per WBS node | BOQ-line-grain measurement → **M14 QSMeasurementBook** (per OQ-1.2=C — single-owner) |
| Auto-derive `actual_start` / `actual_finish` per WBS to feed M03 (first/last Approved entry) | Document/photo storage internals → **M12 DocumentControl** (M04 stores `document_id` references; MinIO direct-URL stub until M12 lands) |
| ConstructionNCR — 4-tier severity, contractor-attributable | Daily site diary → **M16 SiteDiary** |
| NCRStatusLog — append-only state-transition audit | Stage-gate decisions → **M08 GateControl** (M04 reports state; M08 reads to gate-block) |
| MaterialReceipt — site goods receipt → feeds M03 procurement timing + M06 GRN trigger | Commercial LD logic — **M05 Risk & Change** owns LD-eligibility (per OQ-1.6=B — separation of duties) |
| MaterialReceiptLedger — append-only QC decision audit | Vendor identity / PO terms → **M06 FinancialControl** (M04 only references via M03's `procurement_schedule_item_id`) |
| ContractorPerformanceScore (Phase 1) — quarterly weighted score; cascades to M01 `Party.long_term_rating` | Vendor master + pre-qualification → **M30 VendorMasterPQ** (Phase 2 takeover from M04) |
| ContractorPerformanceScoreLog — append-only score-change audit | Risk register / Monte Carlo / VOs → **M05** |
| ProjectExecutionConfig — per-project tunables (dual-signoff threshold, response SLAs, photo minimums) | EVM computation (CPI/SPI/EAC) → **M07 EVMEngine** |
| Decision Queue triggers (NCR overdue, approval pending, QC fail, contractor score decline) | Billing milestones / cashflow → **M06** |
| Photo evidence stub (MinIO URLs in `photo_urls` JSONB until M12 lands) — with planned migration | Schedule / PV / baseline → **M03** |
| Audit-events emission per Appendix A (22 events) | Stage gates SG-0 to SG-11 / Gate criteria → **M08** |

---

## BLOCK 3 — DATA ARCHITECTURE

### 3a. Entities

| Entity | Description | Cardinality | Append-only? |
|---|---|---|---|
| `ProgressEntry` | The single source of truth for "% of this WBS work declared/approved this period." Three-state lifecycle. | Many per WBS node per period | No (mutable until Approved) |
| `ProgressEntryAudit` | Every state transition recorded. Provenance for M07 EV computation + M06 billing trigger + dispute defence. | Many per ProgressEntry | **Yes** |
| `ProgressMeasurementConfig` | Locks the measurement method for a WBS node. Cannot change after first ProgressEntry persists (per BR-04-002). | 1 per WBS node | No (locked-state, not append-only) |
| `ConstructionNCR` | Non-conformance during construction (pre-SG-11). 4-tier severity. M04 reports faithfully — no LD logic inside. | Many per WBS node | No |
| `NCRStatusLog` | Every NCR state transition + severity change. | Many per NCR | **Yes** |
| `MaterialReceipt` | Site goods receipt event. Triggers M03 `actual_delivery_date` populate + M06 GRN signal. | Many per ProcurementScheduleItem | No |
| `MaterialReceiptLedger` | Every QC decision and receipt event. | Many per receipt | **Yes** |
| `ContractorPerformanceScore` | Quarterly weighted score per contractor per project. Phase 1 implementation. M30 takeover Phase 2. | 1 per Contract per quarter | No (one row per quarter — quarter is the immutable axis) |
| `ContractorPerformanceScoreLog` | Every score recomputation / manual override. | Many per score | **Yes** |
| `ProjectExecutionConfig` | Per-project tunables. Resolves OQ-2.6 — threshold + SLA homes live in M04, not M01. | 1 per project | No (audited via standard `updated_*` fields + edit BR) |

**Append-only DB-level enforcement (per OQ-2.2 + Round 18 anti-drift discipline — same pattern as M02 BACIntegrityLedger):**

```sql
-- For each append-only ledger:
REVOKE UPDATE, DELETE ON {ledger_table} FROM app_role;
GRANT INSERT, SELECT ON {ledger_table} TO app_role;
```

Append-only entities have NO `updated_at`, NO `updated_by`, NO `is_active` (no soft-delete).

---

### 3b. Entity: `ProgressEntry`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `entry_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → TenantMaster |
| `project_id` | UUID | Y | — | LINK → M01 Project |
| `wbs_id` | UUID | Y | Must have ProgressMeasurementConfig (BR-04-001) | LINK → M02 WBSNode |
| `package_id` | UUID | Y | Inherited from WBS node | LINK → M02 Package |
| `contract_id` | UUID | Y | Responsible contractor | LINK → M01 Contract |
| `period_start` | DATE | Y | Reporting period start; derived from M03 `reporting_period_type` | CALC |
| `period_end` | DATE | Y | Period end | CALC |
| `measurement_method` | ENUM | Y | `Units / Steps / Milestone / Subjective_Estimate` (X8 `ProgressMeasurementMethod`, locked v0.5). Read from ProgressMeasurementConfig at create. | LINK → ProgressMeasurementConfig |
| `pct_complete_declared` | DECIMAL(5,4) | Y | Range [0.0000, 1.0000]. The contractor's declared %. | INPUT (SITE_MANAGER) |
| `pct_complete_approved` | DECIMAL(5,4) | N | Set on Approved transition. May differ from declared (QS verification). Range [0.0000, 1.0000]. | INPUT (QS_MANAGER on approve) |
| `units_completed` | INTEGER | N | Required if measurement_method=Units; else null | INPUT |
| `units_total` | INTEGER | N | Required if measurement_method=Units; from ProgressMeasurementConfig | LINK → ProgressMeasurementConfig |
| `steps_completed` | JSONB | N | Required if measurement_method=Steps; ordered list of step indices marked complete | INPUT |
| `steps_total_count` | INTEGER | N | Required if measurement_method=Steps | LINK → ProgressMeasurementConfig |
| `milestones_achieved` | JSONB | N | Required if measurement_method=Milestone; list of milestone keys (M03 milestone_id refs) achieved this period | INPUT |
| `subjective_estimate_basis` | TEXT | N | Required (min 100 chars) if measurement_method=Subjective_Estimate; describes the basis for the estimate (BR-04-004d) | INPUT |
| `notes` | TEXT | N | Max 2000 chars | INPUT |
| `photo_document_ids` | JSONB | N | M12 references (target). Until M12 lands: empty array. | LINK → M12 (when built) |
| `photo_urls` | JSONB | N | **STUB FIELD** — array of MinIO URLs. Deprecated when M12 v1.0 lands; migration script: `20260XXX_M12_absorb_M04_photo_urls.py` (drafted Appendix C) | INPUT (stub period) |
| `status` | ENUM | Y | `Draft / Submitted / Approved / Rejected` (X8 `ProgressApprovalStatus`, locked v0.5) | SYSTEM |
| `approval_path` | ENUM | N | `Single_QS / Dual_QS_PD` — determined at Submit by BR-04-006 based on entry_value_inr × dual_signoff_threshold | CALC |
| `entry_value_inr` | DECIMAL(15,2) | Y | CALC = pct_complete_declared × WBSNode.bac_per_node (read from M02). Used for dual-signoff routing. | CALC |
| `declared_by` | UUID | Y | Site rep who declared. | LINK → M34 User |
| `declared_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `submitted_by` | UUID | N | SITE_MANAGER or PROJECT_DIRECTOR | LINK → M34 User |
| `submitted_at` | TIMESTAMP | N | Set on Draft → Submitted | SYSTEM |
| `approved_by_qs` | UUID | N | QS_MANAGER. Required on Approved (single OR dual path). | LINK → M34 User |
| `approved_at_qs` | TIMESTAMP | N | Set when QS approves | SYSTEM |
| `approved_by_pd` | UUID | N | PROJECT_DIRECTOR. Required only when approval_path=Dual_QS_PD AND status=Approved. | LINK → M34 User |
| `approved_at_pd` | TIMESTAMP | N | Set when PD approves (after QS) | SYSTEM |
| `approved_at` | TIMESTAMP | N | Final approved timestamp = max(approved_at_qs, approved_at_pd). The "consume" timestamp for M07/M06. | CALC |
| `rejected_by` | UUID | N | QS_MANAGER or PROJECT_DIRECTOR | LINK → M34 User |
| `rejected_at` | TIMESTAMP | N | Set on Rejected | SYSTEM |
| `rejection_reason` | TEXT | N | Min 50 chars (BR-04-008). Required if status=Rejected | INPUT |
| `ev_confidence` | ENUM | Y | `High / Low / Fallback / Derived` (X8 `EVConfidence`, locked v0.5). CALC from method + status. See BR-04-013. | CALC |
| `recalc_job_id_emitted` | UUID | N | FK → M07 RecalcQueue (when M07 built). Tracks the EV recalc this approval triggered. | LINK → M07 (when built) |
| `tenant_id, created_by, created_at, updated_by, updated_at, is_active` | reserved | Y | Standard reserved fields (X8 §6) | SYSTEM |

**Method-specific consistency check (BR-04-004 a–d):**

| Method | Required derivation |
|---|---|
| `Units` | `pct_complete_declared = units_completed / units_total` (must agree to 4 decimal places) |
| `Steps` | `pct_complete_declared = len(steps_completed) / steps_total_count` (must agree) |
| `Milestone` | `pct_complete_declared = sum(milestone.weight for milestone in milestones_achieved) / 1.0` |
| `Subjective_Estimate` | `pct_complete_declared` is free-form; `subjective_estimate_basis` text required ≥ 100 chars |

---

### 3c. Entity: `ProgressEntryAudit` (APPEND-ONLY)

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `audit_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | SYSTEM |
| `entry_id` | UUID | Y | FK → ProgressEntry | LINK |
| `prior_status` | ENUM | N | Null if INSERT (initial Draft). Else ProgressApprovalStatus value before. | SYSTEM |
| `new_status` | ENUM | Y | ProgressApprovalStatus value after. | SYSTEM |
| `transition_reason` | TEXT | N | For Reject: rejection_reason. For Approve: optional verification note. | INPUT |
| `actor_id` | UUID | Y | FK → M34 User | LINK |
| `actor_role` | VARCHAR(40) | Y | Snapshot of role at time of action (UPPER_SNAKE_CASE) | SYSTEM |
| `event_type` | VARCHAR(60) | Y | UPPER_SNAKE_CASE per X8 §2 (e.g., `PROGRESS_ENTRY_DECLARED`, `PROGRESS_ENTRY_SUBMITTED`, `PROGRESS_ENTRY_APPROVED_QS`, `PROGRESS_ENTRY_APPROVED_PD`, `PROGRESS_ENTRY_REJECTED`) | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `tenant_id, created_by` | reserved | Y | Standard | SYSTEM |

**No `updated_*` / `is_active`. DB-level UPDATE/DELETE forbidden.**

---

### 3d. Entity: `ProgressMeasurementConfig`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `config_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | LINK → M01 |
| `wbs_id` | UUID | Y | Unique per project (1:1 with WBS node) | LINK → M02 WBSNode |
| `measurement_method` | ENUM | Y | ProgressMeasurementMethod (X8 v0.5) | INPUT (PLANNING_ENGINEER) |
| `units_total` | INTEGER | N | Required if method=Units; > 0 | INPUT |
| `unit_of_measure` | VARCHAR(20) | N | Required if method=Units (e.g., 'm³', 'tonnes', 'each') | INPUT |
| `steps_total_count` | INTEGER | N | Required if method=Steps; > 0 | INPUT |
| `steps_definition` | JSONB | N | Required if method=Steps; ordered list of step labels | INPUT |
| `milestone_definitions` | JSONB | N | Required if method=Milestone; list of {milestone_id, weight}; weights sum to 1.0 | INPUT |
| `subjective_basis_required_above_pct` | DECIMAL(5,4) | N | If method=Subjective_Estimate, optional threshold above which an additional PMO-attached basis document is required (default 0.25 per OQ-2.7 below). | INPUT |
| `is_locked` | BOOLEAN | Y | Default false. Set true after first ProgressEntry persists (BR-04-002) | SYSTEM |
| `locked_at` | TIMESTAMP | N | Set when is_locked=true | SYSTEM |
| `tenant_id, created_by, created_at, updated_by, updated_at, is_active` | reserved | Y | Standard | SYSTEM |

---

### 3e. Entity: `ConstructionNCR`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `ncr_id` | UUID | Y | Auto-generated | SYSTEM |
| `ncr_code` | VARCHAR(20) | Y | Auto-generated. Format: `NCR-{project_seq_pad4}` (e.g., NCR-0001) | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | LINK → M01 |
| `wbs_id` | UUID | Y | Location of NCR | LINK → M02 WBSNode |
| `package_id` | UUID | Y | Inherited from WBS | LINK → M02 Package |
| `contract_id` | UUID | Y | Responsible contractor | LINK → M01 Contract |
| `severity` | ENUM | Y | X8 `Severity` ENUM = `Critical / High / Medium / Low` (4-tier per OQ-1.5=A; X8 system ENUM, locked since v0.1) | INPUT |
| `description` | TEXT | Y | Min 50 chars | INPUT |
| `root_cause_category` | ENUM | Y | `Workmanship / Material / Design / Procedure / Other` (X8 `NCRRootCauseCategory`, locked v0.5) | INPUT |
| `identified_by` | UUID | Y | FK → M34 User | LINK |
| `identified_at` | DATE | Y | Cannot be < project planned_start (BR-04-015) | INPUT |
| `response_due` | DATE | Y | CALC by BR-04-017 — Critical = +24hr; High = +48hr; Medium/Low = +72hr (configurable via ProjectExecutionConfig) | CALC |
| `contractor_response` | TEXT | N | Min 30 chars when populated; required for Response_Received transition | INPUT |
| `contractor_response_date` | DATE | N | Set when contractor responds | INPUT |
| `remediation_planned_start` | DATE | N | Contractor's planned start | INPUT |
| `remediation_actual_start` | DATE | N | Actual start | INPUT |
| `remediation_completion_declared` | DATE | N | Contractor declares done | INPUT |
| `reinspection_required` | BOOLEAN | Y | Default true. PROJECT_DIRECTOR may override only for Low severity (BR-04-019) | INPUT |
| `reinspection_scheduled` | DATE | N | When PMO/QS team will inspect | INPUT |
| `reinspection_date` | DATE | N | Actual inspection date | INPUT |
| `reinspection_result` | ENUM | N | `Pass / Fail / Partial` | INPUT |
| `reinspection_notes` | TEXT | N | Min 30 chars if reinspection_result in (Fail, Partial) | INPUT |
| `status` | ENUM | Y | `Open / Response_Pending / Response_Received / Remediation_In_Progress / Reinspection_Pending / Closed / Disputed` (X8 v0.5 — `NCRStatus`) | SYSTEM |
| `closed_at` | TIMESTAMP | N | Auto on status → Closed (reinspection_result=Pass OR PMO override) | SYSTEM |
| `closed_by` | UUID | N | PROJECT_DIRECTOR or PMO_DIRECTOR | LINK → M34 User |
| `is_disputed` | BOOLEAN | Y | Default false. Set true on contractor liability dispute. | INPUT |
| `dispute_resolution_note` | TEXT | N | Min 100 chars; required if is_disputed=true | INPUT |
| `ld_eligibility_flag` | BOOLEAN | Y | Default false. **Only M05 may toggle true** (per OQ-1.6=B — separation of duties; M04 has zero LD logic) | LINK → M05 (when built) |
| `photo_document_ids` | JSONB | N | M12 references when built | LINK → M12 |
| `photo_urls` | JSONB | N | STUB until M12 lands | INPUT |
| `tenant_id, created_by, created_at, updated_by, updated_at, is_active` | reserved | Y | Standard | SYSTEM |

---

### 3f. Entity: `NCRStatusLog` (APPEND-ONLY)

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `log_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | SYSTEM |
| `ncr_id` | UUID | Y | FK → ConstructionNCR | LINK |
| `prior_status` | ENUM | N | NCRStatus or null on initial INSERT | SYSTEM |
| `new_status` | ENUM | Y | NCRStatus | SYSTEM |
| `prior_severity` | ENUM | N | If severity changed; else null | SYSTEM |
| `new_severity` | ENUM | N | If severity changed; else null | SYSTEM |
| `transition_reason` | TEXT | N | Optional context | INPUT |
| `actor_id` | UUID | Y | FK → M34 User | LINK |
| `actor_role` | VARCHAR(40) | Y | Snapshot | SYSTEM |
| `event_type` | VARCHAR(60) | Y | UPPER_SNAKE_CASE (e.g., `NCR_RAISED`, `NCR_RESPONSE_RECEIVED`, `NCR_REINSPECTION_FAIL`, `NCR_CLOSED`) | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `tenant_id, created_by` | reserved | Y | Standard | SYSTEM |

**No `updated_*` / `is_active`. DB-level UPDATE/DELETE forbidden.**

---

### 3g. Entity: `MaterialReceipt`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `receipt_id` | UUID | Y | Auto-generated | SYSTEM |
| `receipt_code` | VARCHAR(20) | Y | Auto. Format: `RCPT-{project_seq_pad5}` | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | LINK → M01 |
| `procurement_schedule_item_id` | UUID | Y | FK → M03 ProcurementScheduleItem (mandatory link per BR-04-024) | LINK → M03 |
| `package_id` | UUID | Y | Inherited via M03 link | LINK → M02 |
| `wbs_id` | UUID | N | Where the material will be installed (optional at receipt; required at consumption) | LINK → M02 WBSNode |
| `contract_id` | UUID | Y | Vendor contract (responsible vendor) | LINK → M01 Contract |
| `quantity_received` | DECIMAL(15,4) | Y | > 0 | INPUT |
| `unit_of_measure` | VARCHAR(20) | Y | From procurement_schedule_item.unit_of_measure | LINK → M03 |
| `unit_value_inr` | DECIMAL(15,2) | Y | CALC = quantity_received × procurement_schedule_item.unit_rate (from M03) | CALC |
| `received_at` | TIMESTAMP | Y | Auto on creation | SYSTEM |
| `received_by` | UUID | Y | FK → M34 User (typically SITE_MANAGER) | LINK |
| `qc_status` | ENUM | Y | `Pending_QC / In_QC / QC_Complete` (X8 v0.5 — `MaterialQCStatus`) | SYSTEM |
| `qc_decision` | ENUM | N | `Accepted / Rejected / Conditional_Acceptance` (X8 v0.5 — `MaterialQCDecision`); set on QC_Complete | INPUT (PROCUREMENT_OFFICER or PROJECT_DIRECTOR) |
| `qc_decided_by` | UUID | N | FK → M34 User | LINK |
| `qc_decided_at` | TIMESTAMP | N | Auto | SYSTEM |
| `qc_notes` | TEXT | N | Min 100 chars if qc_decision=Conditional_Acceptance (BR-04-030) | INPUT |
| `qc_rejection_reason` | TEXT | N | Min 50 chars if qc_decision=Rejected | INPUT |
| `return_to_vendor_status` | ENUM | N | `Not_Required / Pending / Returned / Replacement_Received` if qc_decision=Rejected | INPUT |
| `grn_signal_emitted_at` | TIMESTAMP | N | Set when GRN_SIGNAL emitted to M06 (Accepted only) | SYSTEM |
| `m03_actual_delivery_emitted_at` | TIMESTAMP | N | Set when actual_delivery_date emitted to M03 (Accepted only) | SYSTEM |
| `status` | ENUM | Y | `Received / In_QC / Accepted / Rejected / Conditional_Accepted / Closed` (X8 v0.5 — `MaterialReceiptStatus`) | SYSTEM |
| `photo_document_ids` | JSONB | N | M12 refs when built; required (≥1) if unit_value_inr ≥ ProjectExecutionConfig.high_value_material_threshold_inr (default ₹10L per OQ-2.3) | LINK → M12 |
| `photo_urls` | JSONB | N | STUB until M12 | INPUT |
| `tenant_id, created_by, created_at, updated_by, updated_at, is_active` | reserved | Y | Standard | SYSTEM |

---

### 3h. Entity: `MaterialReceiptLedger` (APPEND-ONLY)

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `ledger_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | SYSTEM |
| `receipt_id` | UUID | Y | FK → MaterialReceipt | LINK |
| `prior_status` | ENUM | N | MaterialReceiptStatus or null on INSERT | SYSTEM |
| `new_status` | ENUM | Y | MaterialReceiptStatus | SYSTEM |
| `qc_decision_at_event` | ENUM | N | If event was QC decision | SYSTEM |
| `actor_id` | UUID | Y | FK → M34 User | LINK |
| `actor_role` | VARCHAR(40) | Y | Snapshot | SYSTEM |
| `event_type` | VARCHAR(60) | Y | UPPER_SNAKE_CASE (e.g., `MATERIAL_RECEIVED`, `MATERIAL_QC_ACCEPTED`, `MATERIAL_QC_REJECTED`, `MATERIAL_GRN_EMITTED`) | SYSTEM |
| `transition_reason` | TEXT | N | Optional context | INPUT |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `tenant_id, created_by` | reserved | Y | Standard | SYSTEM |

**No `updated_*` / `is_active`. DB-level UPDATE/DELETE forbidden.**

---

### 3i. Entity: `ContractorPerformanceScore`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `score_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | LINK → M01 |
| `contract_id` | UUID | Y | The contractor whose work is being scored | LINK → M01 Contract |
| `period_start` | DATE | Y | Quarter start | SYSTEM |
| `period_end` | DATE | Y | Quarter end | SYSTEM |
| `progress_adherence_score` | DECIMAL(5,2) | Y | Range [0.00, 100.00]. CALC by BR-04-032. | CALC |
| `ncr_rate_score` | DECIMAL(5,2) | Y | Range [0.00, 100.00]. CALC by BR-04-032. | CALC |
| `material_acceptance_score` | DECIMAL(5,2) | Y | Range [0.00, 100.00]. CALC by BR-04-032. | CALC |
| `weighted_total` | DECIMAL(5,2) | Y | CALC = progress×0.40 + ncr×0.35 + material×0.25 (BR-04-032 formula) | CALC |
| `score_basis_payload` | JSONB | Y | Transparent breakdown — counts, periods, formula intermediates. Allows audit reproduction. | CALC |
| `prior_quarter_score` | DECIMAL(5,2) | N | Previous quarter's weighted_total for trend | LINK |
| `score_delta` | DECIMAL(5,2) | N | CALC = weighted_total - prior_quarter_score | CALC |
| `is_decline_alert` | BOOLEAN | Y | true if score_delta < -10.00 (BR-04-034) | CALC |
| `manual_override_applied` | BOOLEAN | Y | Default false. Set true if PMO_DIRECTOR overrode (BR-04-035) | SYSTEM |
| `manual_override_value` | DECIMAL(5,2) | N | Override value if applied | INPUT (PMO_DIRECTOR) |
| `manual_override_justification` | TEXT | N | Min 200 chars if override applied | INPUT |
| `manual_override_by` | UUID | N | FK → PMO_DIRECTOR user | LINK |
| `manual_override_at` | TIMESTAMP | N | Auto | SYSTEM |
| `applied_to_party_at` | TIMESTAMP | N | Set when M01 cascade emits Party.long_term_rating update | SYSTEM |
| `computed_at` | TIMESTAMP | Y | Auto on quarterly batch run | SYSTEM |
| `tenant_id, created_by, created_at, updated_by, updated_at, is_active` | reserved | Y | Standard | SYSTEM |

**Uniqueness:** (project_id, contract_id, period_start) — one score row per contractor per project per quarter.

---

### 3j. Entity: `ContractorPerformanceScoreLog` (APPEND-ONLY)

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `log_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | SYSTEM |
| `score_id` | UUID | Y | FK → ContractorPerformanceScore | LINK |
| `event_type` | VARCHAR(60) | Y | UPPER_SNAKE_CASE (`SCORE_COMPUTED`, `SCORE_OVERRIDDEN`, `SCORE_APPLIED_TO_PARTY`) | SYSTEM |
| `prior_value` | DECIMAL(5,2) | N | Previous weighted_total | SYSTEM |
| `new_value` | DECIMAL(5,2) | Y | New weighted_total | SYSTEM |
| `actor_id` | UUID | Y | System or PMO_DIRECTOR | LINK |
| `actor_role` | VARCHAR(40) | Y | Snapshot | SYSTEM |
| `change_reason` | TEXT | N | For overrides; required ≥ 200 chars | INPUT |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `tenant_id, created_by` | reserved | Y | Standard | SYSTEM |

**No `updated_*` / `is_active`. DB-level UPDATE/DELETE forbidden.**

---

### 3k. Entity: `ProjectExecutionConfig` (resolves OQ-2.6)

> **Why M04 owns this, not M01:** Per OQ-2.6 resolution — keeping execution-tunables out of the M01 Project entity avoids further M01 cascade churn. M04 owns the lifecycle of these settings; PMO_DIRECTOR-only edits with audit; defaults seeded at project Active state.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `config_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | Unique (1:1 with Project) | LINK → M01 |
| `dual_signoff_threshold_inr` | DECIMAL(15,2) | Y | Default 5000000 (₹50L per Brief OQ-1.4=C) | INPUT (PMO_DIRECTOR) |
| `response_time_critical_hours` | INTEGER | Y | Default 24 (per Brief OQ-2.4 + OQ-2.5) | INPUT |
| `response_time_high_hours` | INTEGER | Y | Default 48 | INPUT |
| `response_time_medium_low_hours` | INTEGER | Y | Default 72 | INPUT |
| `photo_min_critical_ncr` | INTEGER | Y | Default 2 (per Brief OQ-2.3) | INPUT |
| `photo_min_high_ncr` | INTEGER | Y | Default 1 | INPUT |
| `high_value_material_threshold_inr` | DECIMAL(15,2) | Y | Default 1000000 (₹10L) — receipts above this need ≥ 1 photo | INPUT |
| `subjective_basis_threshold_pct` | DECIMAL(5,4) | Y | Default 0.2500 (25% — per OQ-2.7 below) | INPUT |
| `last_edited_by` | UUID | N | FK → PMO_DIRECTOR | LINK |
| `last_edit_justification` | TEXT | N | Min 100 chars on every edit (BR-04-037) | INPUT |
| `tenant_id, created_by, created_at, updated_by, updated_at, is_active` | reserved | Y | Standard | SYSTEM |

---

## BLOCK 4 — DATA POPULATION RULES

| Rule | Trigger | Action |
|---|---|---|
| Auto-create ProjectExecutionConfig | Project transitions to Active (M01 BR-01-007) | Insert ProjectExecutionConfig row with all defaults; emit `EXEC_CONFIG_CREATED` audit |
| Auto-generate `ncr_code` | NCR INSERT | Format: `NCR-{project.project_code}-{seq_pad4}` where seq is per-project monotonic |
| Auto-generate `receipt_code` | MaterialReceipt INSERT | Format: `RCPT-{project.project_code}-{seq_pad5}` |
| Derive `period_start` / `period_end` | ProgressEntry INSERT | Read M03 LookAheadConfig.reporting_period_type via M03 internal API; compute period bounds from declared_at |
| Derive `entry_value_inr` | ProgressEntry INSERT or pct_complete_declared change | CALC = pct_complete_declared × M02 WBSNode.bac_per_node (read via M02 internal API per F-005) |
| Derive `approval_path` | Submit transition | If entry_value_inr ≤ ProjectExecutionConfig.dual_signoff_threshold_inr → `Single_QS`; else `Dual_QS_PD` |
| Derive `ev_confidence` | On Approve | See BR-04-013 mapping |
| Cascade ContractorPerformanceScore → M01 | Quarterly batch (1st of month after quarter close) | BR-04-031 → BR-04-033; emit SCORE_APPLIED_TO_PARTY |
| Photo migration to M12 | M12 v1.0 lock | One-shot script `20260XXX_M12_absorb_M04_photo_urls.py`; emit `PHOTO_MIGRATED_TO_M12` per row; deprecate `photo_urls` JSONB |

---

## BLOCK 5 — FILTERS AND VIEWS

### Common filters across views

- `project_id` (mandatory — RBAC scope)
- `wbs_id` (optional drill)
- `package_id` (optional drill)
- `period_start` / `period_end` (date range)
- `status` (entity-specific status enums)
- `severity` (NCR only)
- `contract_id` (contractor filter)
- `qc_decision` (MaterialReceipt only)

### Role-default views (per OQ-1.8 — locked from Brief; X9 §13.3.3 row locked v0.3)

| Role | Primary view | Secondary view |
|---|---|---|
| `SITE_MANAGER` | **Today's progress entries** (data-entry surface; declared & in-Draft list with quick-Submit) | 4-week look-ahead Gantt with site-relevant WBS slice (link → M03) |
| `PROJECT_DIRECTOR` | Project progress dashboard — **% complete heatmap by WBS** (with status badges) | NCR pipeline funnel (X9 §11 flagship pattern — 8th instance) |
| `QS_MANAGER` ⭐ | **Pending approvals queue** — Submitted ProgressEntries awaiting QS review, sortable by entry_value_inr | Measurement variance — declared vs approved % delta per period |
| `PMO_DIRECTOR` | NCR pipeline funnel (X9 §11) | Material receipts vs procurement schedule variance (link → M03) |
| `PROCUREMENT_OFFICER` | Material receipts log + receipt-vs-PO variance | Long-lead item tracking (link → M03 ProcurementScheduleItem) |
| `ANALYST` | Progress trend curves (S-curve actual vs planned by package) | NCR rate trend |
| `READ_ONLY` | Project progress card (status badges only; no approval actions) | — |

⭐ = X9 v0.3 added this row to §13.3.3 (locked).

### Mandatory-input fields per entity (M03 pattern)

| Field | Required at | Block save if blank? |
|---|---|---|
| `pct_complete_declared` | ProgressEntry create | Y (BR-04-003) |
| `subjective_estimate_basis` | ProgressEntry create where method=Subjective_Estimate | Y if pct_declared > config.subjective_basis_threshold_pct (BR-04-004d) |
| `rejection_reason` | Reject transition | Y (BR-04-008) |
| `description` | NCR create | Y (min 50 chars) |
| `contractor_response` | Response_Received transition | Y (min 30 chars) |
| `qc_notes` | qc_decision=Conditional_Acceptance | Y (BR-04-030, min 100 chars) |
| `manual_override_justification` | ContractorScore override | Y (BR-04-035, min 200 chars) |
| `last_edit_justification` | ProjectExecutionConfig edit | Y (BR-04-037, min 100 chars) |

---

## BLOCK 6 — BUSINESS RULES

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---|---|---|---|---|
| BR-04-001 | ProgressEntry create | wbs_id must have ProgressMeasurementConfig row | Block save with reason=`MEASUREMENT_METHOD_NOT_CONFIGURED` | 🔴 Real-time |
| BR-04-002 | First ProgressEntry persists for a wbs_id | Set ProgressMeasurementConfig.is_locked=true; record locked_at | Method cannot change retroactively. Future edits to method Block. | 🔴 Real-time |
| BR-04-003 | ProgressEntry create | pct_complete_declared in [0.0000, 1.0000] | Block save if out of range | 🔴 Real-time |
| BR-04-004a | ProgressEntry create where method=Units | units_completed ≤ units_total AND pct = units_completed/units_total (4-dec agreement) | Block save if mismatch | 🔴 Real-time |
| BR-04-004b | ProgressEntry create where method=Steps | All steps_completed indices ∈ [0, steps_total_count); pct = len/total | Block save if mismatch | 🔴 Real-time |
| BR-04-004c | ProgressEntry create where method=Milestone | milestones_achieved ⊂ milestone_definitions; pct = sum(weights) | Block save if mismatch | 🔴 Real-time |
| BR-04-004d | ProgressEntry create where method=Subjective_Estimate AND pct_declared > config.subjective_basis_threshold_pct | subjective_estimate_basis required ≥ 100 chars | Block save | 🔴 Real-time |
| BR-04-005 | Submit transition (Draft → Submitted) | Caller role ∈ {SITE_MANAGER, PROJECT_DIRECTOR} AND on own project (RBAC) | Allow; emit `PROGRESS_ENTRY_SUBMITTED`; compute approval_path via BR-04-006 | 🔴 Real-time |
| BR-04-006 | On Submit | If entry_value_inr ≤ ProjectExecutionConfig.dual_signoff_threshold_inr → approval_path=Single_QS; else Dual_QS_PD | Persist approval_path; route to Decision Queue if Dual | 🔴 Real-time |
| BR-04-007 | Approve transition | If Single_QS: caller=QS_MANAGER → status=Approved. If Dual_QS_PD: first QS_MANAGER then PROJECT_DIRECTOR (sequential) → status=Approved only when both signed. | Allow; emit appropriate audit events; on final Approved trigger BR-04-013/014 cascade | 🔴 Real-time |
| BR-04-008 | Reject transition | Caller ∈ {QS_MANAGER, PROJECT_DIRECTOR} on own project; rejection_reason ≥ 50 chars | Allow; emit `PROGRESS_ENTRY_REJECTED`; entry returns to contractor for re-Draft (cycle limited per BR-04-009) | 🔴 Real-time |
| BR-04-009 | Rejected → Draft re-cycle | Count of (Submitted → Rejected) transitions for this entry > 3 | Decision Queue: `PROGRESS_ENTRY_REPEATED_REJECTION` severity=High; PROJECT_DIRECTOR review | 🟡 2-4hr |
| BR-04-010 | M07 EV computation reads | Filter ProgressEntry WHERE status=Approved (Draft / Submitted / Rejected NOT consumed by M07 — confirms M07 v3.0 BR-07-027 contract for the 3-state model) | M07 reads pct_complete_approved + ev_confidence | 🔴 Real-time |
| BR-04-011 | M07 EV computation reads where method=Subjective_Estimate AND status=Approved | M07 sees ev_confidence=Low | EV consumed but flagged Low-confidence | 🔴 Real-time |
| BR-04-012 | Approved transition | Emit `BILLING_TRIGGER_READY` to M06 (when built) with entry_id, entry_value_inr, approved_at | Persist; M06 internal API endpoint receives | 🔴 Real-time |
| BR-04-013 | Approved transition | Compute ev_confidence: method=Units/Steps/Milestone → `High`; method=Subjective_Estimate → `Low`; (Fallback / Derived computed by M07-side, not M04) | Persist on ProgressEntry | 🔴 Real-time |
| BR-04-014 | Approved transition (first or last for a wbs_id) | If first Approved entry for wbs_id: emit `actual_start = period_start` to M03 ScheduleEntry. If pct_complete_approved=1.0000: emit `actual_finish = period_end` to M03 | M03 ScheduleEntry receives | 🔴 Real-time |
| BR-04-015 | NCR create | identified_at ≥ M01 Project.planned_start_date | Block save with reason=`IDENTIFIED_BEFORE_PROJECT_START` | 🔴 Real-time |
| BR-04-016 | NCR create where severity ∈ {Critical, High} | photo_document_ids count ≥ ProjectExecutionConfig.photo_min_critical_ncr (or _high) per severity | Block save if photo count below minimum | 🔴 Real-time |
| BR-04-017 | NCR create | response_due CALC = identified_at + ProjectExecutionConfig.response_time_{severity}_hours | Persist response_due | 🔴 Real-time |
| BR-04-018 | NCR daily sweep (🟢 24hr) where status ∈ {Open, Response_Pending} AND response_due < today | Generate Decision Queue: `NCR_OPEN_CRITICAL` (severity=Critical → CRITICAL) or `NCR_OPEN_HIGH` (severity=High → HIGH); SLA per OQ-2.4 | Decision created; PROJECT_DIRECTOR notified | 🟢 24hr (sweep) — emits Decision in 🔴 |
| BR-04-019 | NCR create where reinspection_required=false | Allowed only if severity=Low AND PROJECT_DIRECTOR is the caller (not contractor) | Block save with reason=`REINSPECTION_OVERRIDE_NOT_PERMITTED` for higher severities or non-PD callers | 🔴 Real-time |
| BR-04-020 | reinspection_result populated | If Pass: status → Closed; closed_at = now. If Fail: status → Remediation_In_Progress; new response_due = today + severity SLA. If Partial: status → Remediation_In_Progress; reinspection_notes required ≥ 30 chars | Persist; emit `NCR_REINSPECTION_{result}` | 🔴 Real-time |
| BR-04-021 | NCR create OR status change | Emit `NCR_RAISED` (on create) or `NCR_STATUS_CHANGED` (on transition) to M05 (when built) with full payload | M05 internal API endpoint receives | 🔴 Real-time |
| BR-04-022 | NCR ld_eligibility_flag write attempt | Caller must be M05 internal API (system-to-system); UI cannot toggle | Block UI write; allow M05 system call. Audit log every flip. | 🔴 Real-time |
| BR-04-023 | NCR soft-delete (is_active → false) | status must be in {Closed, Disputed} | Block soft-delete if open; force closure first | 🔴 Real-time |
| BR-04-024 | MaterialReceipt create | procurement_schedule_item_id must exist + resolve in M03 (active row) | Block save with reason=`PROC_ITEM_NOT_FOUND` | 🔴 Real-time |
| BR-04-025 | MaterialReceipt create | quantity_received > 0 AND ≤ procurement_schedule_item.ordered_quantity (no over-delivery without QC) | Block save (over-delivery routes to Conditional_Acceptance flow on QC) | 🔴 Real-time |
| BR-04-026 | MaterialReceipt create where unit_value_inr ≥ ProjectExecutionConfig.high_value_material_threshold_inr | photo_document_ids count ≥ 1 | Block save if zero photos | 🔴 Real-time |
| BR-04-027 | qc_decision write | Value ∈ {Accepted, Rejected, Conditional_Acceptance} | Block save outside ENUM | 🔴 Real-time |
| BR-04-028 | qc_decision = Accepted | Emit `MATERIAL_GRN_EMITTED` to M06 (when built) AND `actual_delivery_date = received_at` to M03 ProcurementScheduleItem | Persist; both signals | 🔴 Real-time |
| BR-04-029 | qc_decision = Rejected | DO NOT emit GRN OR actual_delivery_date. Set return_to_vendor_status=Pending. | Persist | 🔴 Real-time |
| BR-04-030 | qc_decision = Conditional_Acceptance | qc_notes ≥ 100 chars | Block save if blank | 🔴 Real-time |
| BR-04-031 | Quarterly batch — 1st of month following quarter close | For each (project_id, contract_id): compute progress_adherence + ncr_rate + material_acceptance scores per BR-04-032 formula; insert ContractorPerformanceScore | Persist; emit `SCORE_COMPUTED` per row | 🟢 24hr (batch) |
| BR-04-032 | ContractorPerformanceScore compute | weighted_total = (progress_adherence × 0.40) + (ncr_rate × 0.35) + (material_acceptance × 0.25). Components: progress_adherence = % of declared % complete that was approved without rejection in the quarter (range 0–100). ncr_rate = 100 − (open_critical_ncrs × 10 + open_high_ncrs × 5 + open_medium_low_ncrs × 1), floored at 0. material_acceptance = % of MaterialReceipt rows with qc_decision=Accepted. Capture full intermediates in score_basis_payload JSONB. | Score row created | 🟢 24hr |
| BR-04-033 | ContractorPerformanceScore created where applied_to_party_at IS NULL | Cascade to M01: PATCH `Party.long_term_rating` via M01 internal API with new weighted_total. M01 BR (existing) handles the receipt + audit. Set applied_to_party_at = now. | M01 cascade | 🟢 24hr (within batch window) |
| BR-04-034 | ContractorPerformanceScore created where score_delta < -10.00 | Generate Decision Queue: `CONTRACTOR_SCORE_DECLINE` severity=Medium; owner=PMO_DIRECTOR; SLA=7 days | Decision created | 🟢 24hr |
| BR-04-035 | Manual override of ContractorPerformanceScore | Caller=PMO_DIRECTOR; manual_override_justification ≥ 200 chars; new manual_override_value in [0, 100] | Persist override; emit `SCORE_OVERRIDDEN`; cascade BR-04-033 | 🔴 Real-time |
| BR-04-036 | M01 Project transitions to Active | Auto-create ProjectExecutionConfig with all defaults; emit `EXEC_CONFIG_CREATED` | Persist; PMO_DIRECTOR notified | 🔴 Real-time |
| BR-04-037 | ProjectExecutionConfig edit | Caller=PMO_DIRECTOR; last_edit_justification ≥ 100 chars; numeric values within sane bounds (e.g., dual_signoff_threshold_inr in [10000, 100000000]) | Persist; emit `EXEC_CONFIG_EDITED` | 🔴 Real-time |
| BR-04-038 | Photo upload (stub mode pre-M12) | photo_urls JSONB; per URL validate: MinIO domain + content-type prefix image/* (validated client-side; trust at API for stub period) | Persist; emit `PHOTO_ATTACHED` | 🔴 Real-time |
| BR-04-039 | M12 v1.0 lock detected | One-shot migration: for each ProgressEntry/NCR/MaterialReceipt with non-empty photo_urls: create M12 Document records; populate photo_document_ids; clear photo_urls (or leave for one-cycle redundancy then drop in v1.1) | One-shot script run | 🟢 24hr (one-time) |

---

## BLOCK 7 — INTEGRATION POINTS

| Direction | Module | Data Exchanged | Trigger | Speed Tier |
|---|---|---|---|---|
| RECEIVES FROM | M34 | Auth, role, project scope, photo permissions per role | Every API call | 🔴 |
| RECEIVES FROM | M01 | `project_id`, `current_phase`, `report_date`, `contract_id`, `Party` (contractor identity), `Project.planned_start_date` (for BR-04-015), `Project.min_wbs_depth` (for WBS validation context only — read-only) | On project state change | 🔴 |
| RECEIVES FROM | M02 | `wbs_id`, `package_id`, `bac_per_node`, `bac_integrity_status` | On WBS create/update + BAC change | 🔴 |
| RECEIVES FROM | M03 | `wbs_id` planned dates, `procurement_schedule_item_id`, `unit_rate`, `look_ahead_window_weeks`, LookAheadConfig.reporting_period_type (per M01 v1.2 cascade — ownership shifted to M03) | On schedule create + look-ahead refresh + period config change | 🔴 |
| SENDS TO | M03 | `MaterialReceipt.received_at` → ProcurementScheduleItem.actual_delivery_date (Accepted only — BR-04-028) | On qc_decision=Accepted | 🔴 |
| SENDS TO | M03 | First Approved ProgressEntry.period_start → ScheduleEntry.actual_start; pct_complete_approved=1.0 → ScheduleEntry.actual_finish | On Approved transition (BR-04-014) | 🔴 |
| SENDS TO | M07 (when built) | Approved ProgressEntry payload: pct_complete_approved, ev_confidence, approved_at; also pct_complete_declared + status for Draft/Submitted (M07 displays as "approval pending" badge) | On every Approved (BR-04-013); on every Submit/Reject for the badge counter | 🔴 |
| SENDS TO | M05 (when built) | `NCR_RAISED` + `NCR_STATUS_CHANGED` events with full ConstructionNCR payload | On NCR create + status change | 🔴 |
| SENDS TO | M05 (when built) | `ld_eligibility_flag` is **read** by M05; M05 sets it back. M04 never sets true. | On M05 LD-eligibility decision | 🔴 |
| SENDS TO | M06 (when built) | `BILLING_TRIGGER_READY` on Approved progress entries (BR-04-012); `MATERIAL_GRN_EMITTED` on Accepted material receipts (BR-04-028) | On Approved + Accepted | 🔴 |
| SENDS TO | M01 | `Party.long_term_rating` cascade from quarterly ContractorPerformanceScore (BR-04-033) | Quarterly batch | 🟢 |
| SENDS TO | M11 ActionRegister (when built) | Decision Queue items: NCR_OPEN_CRITICAL, NCR_OPEN_HIGH, PROGRESS_APPROVAL_PENDING, MATERIAL_RECEIPT_QC_FAIL, DUAL_SIGNOFF_PENDING, CONTRACTOR_SCORE_DECLINE, PROGRESS_ENTRY_REPEATED_REJECTION | On condition match | 🔴 / 🟢 per trigger |
| SENDS TO | M10 EPCC Command (when built) | Project progress dashboard data, NCR pipeline funnel data, material receipts log | On any change | 🟡 |

---

## BLOCK 8 — GOVERNANCE AND AUDIT

### 8a. Logged Events (action-level — full names locked in Appendix A)

| Action | Logged | Field-Level Detail | Visible To | Retention |
|---|---|---|---|---|
| ProgressEntry create / Submit / Approve / Reject | Yes | All fields, before/after | QS_MANAGER, PROJECT_DIRECTOR, PMO_DIRECTOR | Project lifetime |
| ProgressMeasurementConfig create / lock | Yes | Method choice, units/steps/milestone definitions | PLANNING_ENGINEER, PMO_DIRECTOR | **Permanent** |
| NCR create / status change / closure | Yes | All fields incl. severity changes | PMO_DIRECTOR, PROJECT_DIRECTOR | **Permanent** |
| ld_eligibility_flag toggle (by M05) | Yes | Old/new, M05 source job | PMO_DIRECTOR, FINANCE_LEAD | **Permanent** |
| MaterialReceipt create / QC decision | Yes | All fields, photos, qc_notes | PROCUREMENT_OFFICER, PMO_DIRECTOR, PROJECT_DIRECTOR | Project lifetime |
| GRN_SIGNAL emitted to M06 | Yes | receipt_id, m06 ack | FINANCE_LEAD, PMO_DIRECTOR | **Permanent** |
| ContractorPerformanceScore compute | Yes | All component scores + payload | PMO_DIRECTOR | **Permanent** |
| ContractorPerformanceScore manual override | Yes | Old/new, justification, PMO actor | PMO_DIRECTOR, FINANCE_LEAD | **Permanent** |
| ProjectExecutionConfig create / edit | Yes | All fields, justification | PMO_DIRECTOR | **Permanent** |
| Photo migration to M12 (one-shot) | Yes | Pre/post counts, M12 doc IDs | SYSTEM_ADMIN, PMO_DIRECTOR | **Permanent** |

### 8b. Immutability Rules (DB-level)

- **`ProgressEntryAudit`** — DB-level UPDATE/DELETE forbidden; INSERT only
- **`NCRStatusLog`** — DB-level UPDATE/DELETE forbidden; INSERT only
- **`MaterialReceiptLedger`** — DB-level UPDATE/DELETE forbidden; INSERT only
- **`ContractorPerformanceScoreLog`** — DB-level UPDATE/DELETE forbidden; INSERT only
- **`ProgressEntry`** — Mutable until status=Approved. After Approved: only `photo_document_ids` may be appended (post-approval evidence supplementation per Brief OQ-1.7 stub period).
- **`ConstructionNCR`** — Mutable until status=Closed; Closed records may have `is_disputed` toggled with audit but no other field changes.

### 8c. Privacy / Role Visibility

- `pct_complete_declared` vs `pct_complete_approved` divergence visible to QS_MANAGER + PROJECT_DIRECTOR + PMO_DIRECTOR; not exposed to SITE_MANAGER (declarations remain visible only as "what I declared", not the approval delta)
- ContractorPerformanceScore visible to PMO_DIRECTOR + PROJECT_DIRECTOR (own project) + FINANCE_LEAD; **not** visible to the contractor's own PORTAL roles in v1.0 (Phase 2 PF03 may expose with redaction)
- Photo evidence access mediated by M12 RBAC (when built); during stub period, MinIO URLs gated by M34 role + project scope
- Manual override justifications visible only to PMO_DIRECTOR + FINANCE_LEAD + EXTERNAL_AUDITOR

---

## BLOCK 9 — EXPLICIT EXCLUSIONS

```
This module does NOT:
─────────────────────────────────────────────────────────────────────
[ ] Track DLP register or DLP defects                          → M15 HandoverManagement
[ ] Capture HSE incidents                                       → M31 HSESafetyManagement
[ ] Measure progress at BOQ-line grain                          → M14 QSMeasurementBook
[ ] Store documents / photos / drawings (long-term)             → M12 DocumentControl
[ ] Maintain daily site diary                                   → M16 SiteDiary
[ ] Decide LD-eligibility from NCRs                             → M05 Risk & Change (separation of duties — OQ-1.6=B)
[ ] Trigger or own variation orders                             → M05
[ ] Calculate EVM (CPI / SPI / EAC / EV)                        → M07 EVMEngine
[ ] Process billing or cashflow                                 → M06 FinancialControl
[ ] Define stage-gate criteria                                  → M08 GateControl
[ ] Authenticate users / manage roles                           → M34
[ ] Define BOQ items / WBS structure / BAC                      → M02
[ ] Define schedule / planned dates / PV                        → M03
[ ] Run Monte Carlo / risk-adjusted EAC                         → M05
[ ] Manage vendor master / pre-qualification                    → M30 VendorMasterPQ (Phase 2)
[ ] Compute long-term party rating beyond Phase 1 contractor scoring → M30 takes over Phase 2
[ ] Auto-create gate review or warning on NCR severity          → M08 reads M04 state; M04 doesn't push to gate
[ ] Track regulatory NABH compliance                            → M09
[ ] Override M03 reporting_period_type                          → M03 owns (per M01 v1.2 cascade)
```

---

## BLOCK 10 — OPEN QUESTIONS

**All questions resolved. Zero open questions.**

| # | Question | Resolution |
|---|---|---|
| 1 | OQ-2.6 — Where does the dual-signoff threshold live? M01 v1.3 cascade or M04-owned config? | **M04-owned `ProjectExecutionConfig` (LOCKED).** Avoids further M01 cascade churn. PMO_DIRECTOR-only edits with audit (BR-04-037). Houses all execution-tunables (thresholds + SLAs + photo minimums) in one place. |
| 2 | OQ-2.7 — Subjective_Estimate basis-document escalation threshold? | **Default 25% of WBS-node BAC slice (LOCKED).** Configurable via `ProjectExecutionConfig.subjective_basis_threshold_pct`. BR-04-004d enforces basis text ≥ 100 chars when declared > threshold. |
| 3 | M07 contract — does M07 v3.0 legacy 2-state (Draft/Approved) consume the new 3-state cleanly? | **Yes.** Submitted is invisible to M07 for EV computation (treated as Draft from M07's perspective). When M07 is specced (Round 31+), its `progress_approval_status` filter is `WHERE status = 'Approved'` — same semantics, new state machine transparent to it. |
| 4 | Photo migration to M12 — destructive (drop photo_urls) or additive (keep both for one cycle)? | **Additive for one cycle (LOCKED).** M04 v1.1 cascade (post-M12 v1.0 lock) drops `photo_urls`. Keeps a one-version safety window. |
| 5 | Approver authority for Subjective_Estimate vs measurable methods — same approval path? | **Same path (LOCKED).** Single_QS or Dual_QS_PD per OQ-1.4=C, regardless of method. Subjective_Estimate's risk is captured by `ev_confidence=Low` (M07 reads), not by approval routing. |
| 6 | NCR re-open after Closed — supported? | **No (LOCKED).** A Closed NCR cannot be re-opened. If the same physical issue recurs, raise a new NCR with cross-reference in `description`. Maintains immutable NCRStatusLog without re-open ambiguity. (Same pattern as legacy v2.2 OQ #2 for DLP — consistent across v1.0 era.) |

---

## APPENDIX A — Audit Events Catalogue (LOCKED from authoring per OQ-2.1)

> **Status:** LOCKED. Source of truth for M04 audit event names until X3 Audit Event Catalogue is built. When X3 lands, names migrate to X3 unchanged. Naming follows X8 §2 — UPPER_SNAKE_CASE. Authored alongside Spec per Round 18 cascade-pattern decision (avoids retro-cascade like M03 Round 18 had to do).

### Event registry (22 events)

| Event Name | Source BR | Severity | Trigger Description |
|---|---|---|---|
| `PROGRESS_ENTRY_DECLARED` | BR-04-001..004 | Info | Initial Draft insert |
| `PROGRESS_ENTRY_SUBMITTED` | BR-04-005, BR-04-006 | Info | Draft → Submitted; approval_path computed |
| `PROGRESS_ENTRY_APPROVED_QS` | BR-04-007 | Info | QS_MANAGER signs (intermediate in Dual path; final in Single path) |
| `PROGRESS_ENTRY_APPROVED_PD` | BR-04-007 | Info | PROJECT_DIRECTOR signs (only in Dual path) |
| `PROGRESS_ENTRY_APPROVED` | BR-04-007, BR-04-013, BR-04-014 | Info | Final Approved transition; cascades to M07 + M06 + M03 fire |
| `PROGRESS_ENTRY_REJECTED` | BR-04-008 | Medium | QS_MANAGER or PROJECT_DIRECTOR rejects; rejection_reason captured |
| `PROGRESS_ENTRY_REPEATED_REJECTION` | BR-04-009 | High | **Decision Queue trigger** — same entry rejected > 3 times |
| `MEASUREMENT_CONFIG_LOCKED` | BR-04-002 | Info | First ProgressEntry triggers permanent lock of method choice |
| `NCR_RAISED` | BR-04-015..017, BR-04-021 | Medium (severity-dependent: Critical=High event-severity; Low=Info) | NCR created |
| `NCR_RESPONSE_RECEIVED` | BR-04-021 | Info | Contractor response captured |
| `NCR_REINSPECTION_PASS` | BR-04-020 | Info | Reinspection passed; status → Closed |
| `NCR_REINSPECTION_FAIL` | BR-04-020 | High | **Decision Queue trigger** (via BR-04-018 next sweep) — reinspection failed; new response_due |
| `NCR_REINSPECTION_PARTIAL` | BR-04-020 | Medium | Partial pass; reinspection_notes required |
| `NCR_CLOSED` | BR-04-020 | Info | Final closure |
| `NCR_DISPUTED` | (NCR is_disputed flip) | Medium | Contractor disputes liability |
| `NCR_LD_ELIGIBILITY_TOGGLED` | BR-04-022 | High | M05 sets ld_eligibility_flag true |
| `NCR_OPEN_CRITICAL` | BR-04-018 | **Critical** | **Decision Queue trigger** — Critical NCR overdue |
| `NCR_OPEN_HIGH` | BR-04-018 | High | **Decision Queue trigger** — High NCR overdue |
| `MATERIAL_RECEIVED` | BR-04-024..026 | Info | Receipt event created |
| `MATERIAL_QC_ACCEPTED` | BR-04-027, BR-04-028 | Info | QC pass; GRN + actual_delivery_date emitted |
| `MATERIAL_QC_REJECTED` | BR-04-027, BR-04-029 | Medium | QC fail; return-to-vendor flow |
| `MATERIAL_QC_CONDITIONAL` | BR-04-027, BR-04-030 | Medium | Conditional acceptance; qc_notes ≥ 100 chars |
| `MATERIAL_GRN_EMITTED` | BR-04-028 | Info | GRN signal sent to M06 |
| `MATERIAL_RECEIPT_QC_FAIL` | BR-04-029 | High | **Decision Queue trigger** — QC fail surfaces to PROCUREMENT_OFFICER |
| `SCORE_COMPUTED` | BR-04-031, BR-04-032 | Info | Quarterly score row created |
| `SCORE_OVERRIDDEN` | BR-04-035 | High | PMO manual override applied |
| `SCORE_APPLIED_TO_PARTY` | BR-04-033 | Info | M01 cascade fired; Party.long_term_rating updated |
| `CONTRACTOR_SCORE_DECLINE` | BR-04-034 | Medium | **Decision Queue trigger** — quarterly decline > 10 points |
| `EXEC_CONFIG_CREATED` | BR-04-036 | Info | Auto-create on Project Active |
| `EXEC_CONFIG_EDITED` | BR-04-037 | Medium | PMO edit with justification |
| `PHOTO_ATTACHED` | BR-04-038 | Info | Stub-period photo URL added |
| `PHOTO_MIGRATED_TO_M12` | BR-04-039 | Info | Migration cascade event (one-time when M12 lands) |
| `DUAL_SIGNOFF_PENDING` | BR-04-006 | Medium | **Decision Queue trigger** — Dual_QS_PD path awaiting PD signature |
| `PROGRESS_APPROVAL_PENDING` | (sweep) | Medium | **Decision Queue trigger** — Submitted entries awaiting QS > 48hr |

### Decision Queue triggers (8): summary

`PROGRESS_ENTRY_REPEATED_REJECTION`, `PROGRESS_APPROVAL_PENDING`, `DUAL_SIGNOFF_PENDING`, `NCR_OPEN_CRITICAL`, `NCR_OPEN_HIGH`, `NCR_REINSPECTION_FAIL` (via sweep), `MATERIAL_RECEIPT_QC_FAIL`, `CONTRACTOR_SCORE_DECLINE`.

Confirms Brief OQ-2.4 SLA defaults; M11 ActionRegister (when built) absorbs.

### Notes

- `NCR_RAISED` event severity varies with NCR severity (Critical NCR → High event-severity; Low NCR → Info event-severity) — pattern: event severity is one tier below NCR severity, capping at Info on Low/Medium NCRs. Allows audit log prioritisation without flooding.
- `ld_eligibility_flag` toggles emit `NCR_LD_ELIGIBILITY_TOGGLED` regardless of direction — true→false and false→true both audit. Source actor is M05 (system-to-system).
- Photo migration is a one-time event per row; the catalogue keeps `PHOTO_MIGRATED_TO_M12` named for forward-traceability when the migration cascade actually runs.

---

## APPENDIX B — KDMC Reference Data Mapping

| KDMC Excel Source | M04 Entity | Notes |
|---|---|---|
| `04_Progress_Entries` (legacy sheet) | ProgressEntry | 438 WBS nodes × N periods. Period-cadence inherited from M03 LookAheadConfig. |
| `04_NCR_Register` | ConstructionNCR | KDMC has ~3-4 active NCR categories — Workmanship dominates per pilot data |
| `04_Material_Receipts` | MaterialReceipt | LINAC, MRI, CT — high-value items (>₹1Cr each) — all ≥1 photo per OQ-2.3 |
| `04_Contractor_Scorecard` (manual quarterly) | ContractorPerformanceScore | L&T as primary contractor; quarterly batch generates KDMC's first scorecard at Q1 close |
| (none — new) | ProjectExecutionConfig | Seeded at KDMC project Active state with defaults; PMO can tune dual_signoff_threshold per project sensitivity |

**KDMC Specifics:**
```
Primary contractor:       L&T Construction (contract_id from M01)
Project value:            ₹68.4 Cr
Dual-signoff default:     ₹50L threshold = 0.73% of project value
                          → most progress entries below threshold (Single_QS path)
                          → high-value milestones (LINAC install, MRI commissioning) trigger Dual_QS_PD
NCR categories expected:  Workmanship (60%), Material (20%), Procedure (10%), Design (5%), Other (5%)
                          (estimated from typical Indian healthcare DBOT projects)
High-value materials:     LINAC ~₹15Cr, MRI ~₹8Cr, CT ~₹4Cr, Cath Lab ~₹6Cr
                          → all far above ₹10L photo threshold
```

---

## APPENDIX C — Photo Migration Script (Drafted)

> **Status:** Drafted only — executes when M12 v1.0 lands.

```python
# 20260XXX_M12_absorb_M04_photo_urls.py
# One-shot migration from M04 photo_urls JSONB stub to M12 Document references.

# Pseudo-code:
for table in ['progress_entry', 'construction_ncr', 'material_receipt']:
    for row in select_where(f"{table}.photo_urls IS NOT NULL AND jsonb_array_length(photo_urls) > 0"):
        document_ids = []
        for url in row.photo_urls:
            doc = m12.create_document(
                source_module='M04',
                source_entity=table,
                source_id=row.pk,
                minio_url=url,
                uploaded_by=row.created_by,
                uploaded_at=row.created_at,  # preserve original timestamp
            )
            document_ids.append(doc.id)
        update_row(table, row.pk, photo_document_ids=document_ids)
        emit_audit('PHOTO_MIGRATED_TO_M12', row.pk, count=len(document_ids))
    # Drop photo_urls column in M04 v1.1 cascade — one cycle later (additive safety per Open Question #4)
```

---

*v1.0 — Spec LOCKED. Zero open questions. M04 ExecutionCapture ready for Round 21 (Wireframes). Cascade pending: X8 v0.5 (6 new ENUMs) + X9 v0.3 (M04 row in §13.3.3) — to be authored as Round 20 sub-deliverables.*
