# M03 — Planning & Milestones
## Spec v1.1a
**Status:** LOCKED
**Locked:** Yes
**Author:** PMO Director / System Architect _(grandfathered)_
**Created:** 2026-05-03 | **Last Updated:** 2026-05-04 (v1.1a in-place patch — Round 29 audit, H7 forward-pointer)
**Last Audited:** v1.1a on 2026-05-04
**Reference Standards:** EPCC_NamingConvention_v1_0.md, X8_GlossaryENUMs_v0_4.md, X9_VisualisationStandards_Spec_v0_2.md, M34_SystemAdminRBAC_Spec_v1_0.md, M01_ProjectRegistry_Spec_v1_0.md (+ v1_1_CascadeNote + v1_2_CascadeNote), M02_StructureWBS_Spec_v1_0.md
**Cascade Notes Issued:** M03_PlanningMilestones_v1_2_CascadeNote.md — adds BR-03-035 + `MILESTONE_ACHIEVED_FINANCIAL` emit hook to M06 (X8 v0.6a §4.12). v1.1 stamp values above are historical (X8 v0.4 / X9 v0.2 at lock); current cross-cutting versions are X8 v0.6a / X9 v0.4.
**Layer:** L2 Control — Planning
**Phase:** 1 — Foundational
**Build Priority:** 🔴 Critical (precedes M04, M05, M06, M07, M08)
**Folder:** /03_L2_Planning/
**Re-Issue Of:** Legacy `M03_Planning_Milestones_v2.3.md` — consolidated standalone

---

## CHANGE LOG

| Version | Date | Author | Change Summary |
|---|---|---|---|
| v1.1a | 2026-05-04 | Monish (with Claude assist) | H7 in-place patch (Round 29 audit): added forward-pointer to M03_PlanningMilestones_v1_2_CascadeNote.md in audit stamp (BR-03-035 + `MILESTONE_ACHIEVED_FINANCIAL` emit hook). Reference Standards versions unchanged — v1.1 lock state preserved historically; current X8 v0.6a / X9 v0.4 noted as context. No scope, BR, entity, or field change. |
| v1.0 | 2026-05-03 | PMO Director / System Architect | Initial standalone consolidated spec. Re-issued from legacy v2.3 amendment chain. All 11 OQ-1 decisions locked. 12 entities, ~32 BRs. ResourceType extended to 4 values (incl. Vendor_Resource). reporting_period_type ownership shifted to M03 (M01 v1.2 cascade). Procurement vendor identity owned by M06. Float visibility role-tiered. Role-default views per X9 v0.2 §13.3.3 (PROJECT_DIRECTOR + PV S-curve secondary; PLANNING_ENGINEER + PV roll-up shape). |
| v1.1 | 2026-05-03 | PMO Director / System Architect | Round 18 cascade from Workflows lock. (1) New **Appendix C — Audit Events Catalogue** locks 28 UPPER_SNAKE_CASE event names (2 pre-existing in v1.0 + 26 surfaced by Workflows v1.0). Source of truth for M03 audit events until X3 Audit Event Catalogue lands. (2) New **BR-03-033** — critical-path recomputation MUST execute within the same DB transaction as `ScheduleEntry` persist (anti-stale-read invariant for BR-03-018). (3) New **BR-03-034** — `reporting_period_type` change + full PV regeneration MUST execute as a single atomic transaction; PV regen failure rolls back the reporting_period_type itself; emit `REPORTING_PERIOD_CHANGE_FAILED` (data integrity rule strengthening BR-03-028). |

---

## BLOCK 1 — IDENTITY

```
Module ID                : M03
Module Name              : Planning & Milestones
Layer                    : L2 Control — Planning
Decision It Enables      : Is the project executing within its approved time
                           baseline, and where it is not — is the variance
                           attributable to client (billable), contractor
                           (LD-applicable), neutral event (governed
                           classification), or approved scope extension —
                           such that schedule control, performance
                           measurement, and commercial recovery are all
                           grounded in a single authoritative baseline?

Primary User             : PLANNING_ENGINEER
Secondary Users          : PMO_DIRECTOR (baseline lock + extension approval),
                           PROJECT_DIRECTOR (raise extensions, milestones),
                           PROCUREMENT_OFFICER (procurement schedule),
                           QS_MANAGER, FINANCE_LEAD (PV reads),
                           SITE_MANAGER (look-ahead Gantt only)
Module Icon              : Calendar (Lucide)
Navigation Section       : L2 Control — Planning
```

---

## BLOCK 2 — SCOPE BOUNDARY

### INCLUDES

| Capability | Description |
|---|---|
| Master schedule | `ScheduleEntry` per WBS — planned/baseline/extended dates, float, critical path |
| Baseline (single immutable) | `Baseline` snapshot at SG-6; sealed forever |
| Approved Extensions | `BaselineExtension` — cause-classified additions; commercially tracked |
| Extension cause classification | 6 categories per `BaselineExtensionCause` (X8 §3.40) |
| Auto-classification rules | Billable + vendor-counts flags auto-set per cause; PMO override |
| Neutral_Event auto-reclassification | Blank contract clause → reclassify to Contractor_Delay (BR-03-008) |
| Milestones | `Milestone` — key dates, status, predecessor, gate links, delay tracking |
| Planned Value (PV) | `PVProfile` — time-phased S-curve per WBS per period; foundation of EVM |
| Loading Profiles | `LoadingProfile` — distribution rules per activity_category; 5 types |
| Resource Allocation | `ResourceAllocation` — role mandatory + named optional |
| Resource Master | `ResourceMaster` — 4 types: Internal/Contractor/Consultant/Vendor |
| Procurement Schedule | `ProcurementScheduleItem` — lead time + dates (vendor identity in M06) |
| Weather/Monsoon Config | `WeatherWindowConfig` — region-default + project override |
| Look-ahead Window | `LookAheadConfig` — window weeks + reporting period type |
| Float / Slack | Schedule-calculated, not user-entered |
| Critical Path | Schedule-calculated via inbuilt CPM algorithm |
| Schedule Import | `ScheduleImport` — Primavera P6 / MSP import (modal-gated) |
| Decision Queue triggers | 5 trigger types feeding M11 |

### EXCLUDES

| Excluded | Where It Lives |
|---|---|
| WBS structure and hierarchy | M02 |
| BOQ items + package structure | M02 |
| Actual progress % complete | M04 |
| Actual cost transactions | M06 |
| EVM calculations (CPI, SPI, EAC) | M07 |
| Stage gate approvals | M08 |
| Risk register + variation orders | M05 |
| **Vendor identity for procurement (vendor_id, name, terms)** | **M06** |
| Vendor PO value + payment terms | M06 |
| Regulatory compliance tracking | M09 |
| Document storage | MinIO + M12 |
| Contractor performance scoring | M04 |
| Sub-contract financial terms | M06 |
| Gate entry/exit criteria | M08 |
| BIM model integration | PF02 (Phase 4) |
| Schedule re-baselining (versioned baselines) | NOT SUPPORTED in v1.0 |

---

## BLOCK 3 — DATA ARCHITECTURE

### 3a. Entity Overview

| Entity | Description | Cardinality | Schema Owner |
|---|---|---|---|
| `ScheduleEntry` | Time dimension for each WBS node | 1 per WBSNode | M03 |
| `Baseline` | Original approved schedule snapshot | 1 per project | M03 (immutable) |
| `BaselineExtension` | Approved baseline addition | Many per project | M03 (append-only after approval) |
| `PVProfile` | Time-phased PV per WBS per period | 1 per (WBS × period) | M03 |
| `PVProfileSnapshot` | Historical PV snapshot at report dates | Many per project | M03 (append-only) |
| `LoadingProfile` | S-curve distribution rules | Global per tenant | M03 |
| `Milestone` | Key project milestone | Many per project | M03 |
| `ResourceAllocation` | Role + named per WBS | Many per WBS | M03 |
| `ResourceMaster` | 4-type unified repository | Global per tenant | M03 |
| `ProcurementScheduleItem` | Lead time + dates per item | Many per project | M03 |
| `WeatherWindowConfig` | Region-default + project override | Many per project | M03 |
| `LookAheadConfig` | Window weeks + reporting period type | 1 per project | M03 |
| `ScheduleImport` | Import session metadata | Many per project | M03 |
| `ScheduleImportRecord` | Per-row audit | Many per session | M03 (append-only) |

**Total entities: 14** (including append-only audit entities).

### 3b. Entity: `ScheduleEntry`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `schedule_entry_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | FK → M34.Tenant | LINK → M34 |
| `project_id` | UUID | Y | FK → M01.Project | LINK → M01 |
| `wbs_id` | UUID | Y | FK → M02.WBSNode; UNIQUE within project | LINK → M02 |
| `planned_start` | DATE | Y | < `planned_finish`; within Project planned dates | INPUT |
| `planned_finish` | DATE | Y | > `planned_start`; within Project planned dates | INPUT |
| `baseline_start` | DATE | N | Set at baseline lock; immutable thereafter | SYSTEM (snapshot at SG-6) |
| `baseline_finish` | DATE | N | Set at baseline lock; immutable thereafter | SYSTEM (snapshot at SG-6) |
| `extended_baseline_start` | DATE | N | Auto = baseline_start + sum(approved_extensions for this WBS) | CALC |
| `extended_baseline_finish` | DATE | N | Auto = baseline_finish + sum(approved_extensions for this WBS) | CALC |
| `actual_start` | DATE | N | From M04 progress capture | LINK → M04 |
| `actual_finish` | DATE | N | From M04 progress capture | LINK → M04 |
| `forecast_finish` | DATE | N | Best estimate; updated by Planning Engineer | INPUT |
| `is_baseline_locked` | BOOLEAN | Y | Default false; true after BR-03-005 | SYSTEM |
| `total_float_days` | INTEGER | N | Auto-calculated by CPM algorithm | CALC |
| `free_float_days` | INTEGER | N | Auto-calculated by CPM algorithm | CALC |
| `is_on_critical_path` | BOOLEAN | Y | Auto = (total_float_days ≤ 0) | CALC |
| `schedule_variance_days` | INTEGER | N | Auto = today − extended_baseline_finish (if not complete) | CALC |
| `loading_profile_id` | UUID | N | FK → LoadingProfile | LINK → LoadingProfile |
| `entry_status` | ENUM | Y | Per X8 §3.46 `ScheduleEntryStatus` | CALC |
| `created_by` | UUID | Y | — | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_by` | UUID | Y | Auto | LINK → M34.User |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |

**Composite uniqueness:** (`tenant_id`, `project_id`, `wbs_id`).

---

### 3c. Entity: `Baseline` (immutable after lock)

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `baseline_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34 |
| `project_id` | UUID | Y | UNIQUE — exactly one Baseline per project | LINK → M01 |
| `baseline_snapshot` | JSONB | Y | Full schedule state at lock time | SYSTEM (auto-built from ScheduleEntry) |
| `pv_snapshot` | JSONB | Y | Full PVProfile state at lock time | SYSTEM |
| `milestone_snapshot` | JSONB | Y | Full milestone state at lock time | SYSTEM |
| `total_baseline_duration_days` | INTEGER | Y | Project planned_end − planned_start | CALC |
| `total_pv_at_baseline` | DECIMAL(15,2) | Y | Sum of all PVProfile values | CALC |
| `locked_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `locked_by` | UUID | Y | PMO_DIRECTOR | LINK → M34.User |
| `gate_passage_id` | UUID | Y | FK → M08 SG-6 gate passage record | LINK → M08 |

**IMMUTABILITY ENFORCED AT DB LEVEL:**
- `REVOKE UPDATE, DELETE ON baseline FROM app_role`
- INSERT only at baseline lock
- Subsequent changes go through BaselineExtension entity

---

### 3d. Entity: `BaselineExtension` (append-only after approval)

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `extension_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34 |
| `project_id` | UUID | Y | — | LINK → M01 |
| `extension_code` | VARCHAR(30) | Y | Format: `EXT-{seq}` auto; unique within project | SYSTEM |
| `wbs_id` | UUID | Y | Primary affected WBS | LINK → M02 |
| `additional_wbs_ids` | JSONB | N | Array of UUIDs if multi-WBS impact | INPUT |
| `is_project_level_exception` | BOOLEAN | Y | Default false; true requires PMO_DIR + 100-char justification | INPUT |
| `project_level_justification` | TEXT | N | Required if is_project_level_exception=true; min 100 chars | INPUT |
| `cause_category` | ENUM | Y | Per X8 §3.40 `BaselineExtensionCause` | INPUT |
| `cause_description` | TEXT | Y | Min 50 chars | INPUT |
| `extension_days` | INTEGER | Y | > 0 | INPUT |
| `contract_clause_ref` | VARCHAR(200) | N | If blank + Neutral_Event → auto-reclassify (BR-03-008) | INPUT |
| `is_billable_to_client` | BOOLEAN | Y | Auto-set by cause_category; PMO override | CALC + OVERRIDE |
| `counts_against_vendor` | BOOLEAN | Y | Auto-set by cause_category; PMO override | CALC + OVERRIDE |
| `variation_order_id` | UUID | N | Required if is_billable_to_client=true | LINK → M05 |
| `supporting_evidence_url` | VARCHAR(500) | N | Required for Neutral_Event + Force_Majeure | INPUT |
| `submitted_by` | UUID | Y | Submitter user | LINK → M34.User |
| `submitted_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `approval_status` | ENUM | Y | Per X8 §3.49 `BaselineExtensionStatus` | SYSTEM |
| `approved_by` | UUID | N | PMO_DIRECTOR; required if approval_status=Approved | LINK → M34.User |
| `approved_at` | TIMESTAMP | N | Auto on approval | SYSTEM |
| `rejection_reason` | TEXT | N | Required if approval_status=Rejected | INPUT |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |

**Composite uniqueness:** (`tenant_id`, `project_id`, `extension_code`).

**Append-only after approval:** Once approval_status=Approved, no field changes permitted. Force new extension if correction needed.

---

### 3e. Entity: `PVProfile`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `pv_profile_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34 |
| `project_id` | UUID | Y | — | LINK → M01 |
| `wbs_id` | UUID | Y | — | LINK → M02 |
| `period_start_date` | DATE | Y | Aligned to project reporting_period_type | SYSTEM |
| `period_end_date` | DATE | Y | period_start_date + period_length | SYSTEM |
| `period_pv_amount` | DECIMAL(15,2) | Y | Auto from BAC × loading_profile distribution_curve | CALC |
| `cumulative_pv_amount` | DECIMAL(15,2) | Y | Auto = SUM all prior periods + current | CALC |
| `pv_pct_of_bac` | DECIMAL(5,4) | Y | Auto = period_pv / package_BAC | CALC |
| `is_overridden` | BOOLEAN | Y | Default false | INPUT |
| `override_reason` | TEXT | N | Required if is_overridden=true | INPUT |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

**Composite uniqueness:** (`tenant_id`, `project_id`, `wbs_id`, `period_start_date`).

---

### 3f. Entity: `LoadingProfile`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `profile_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | N | NULL = system default | LINK → M34 |
| `profile_name` | VARCHAR(100) | Y | e.g., `Civil_Front_Loaded` | INPUT |
| `activity_category` | ENUM | Y | Per X8 Discipline (M02 §3.32 reference) | INPUT |
| `distribution_type` | ENUM | Y | Per X8 §3.41 `LoadingProfileType` | INPUT |
| `distribution_curve` | JSONB | Y | Array of (period_pct, value_pct) pairs; sum=100% | INPUT |
| `is_system_default` | BOOLEAN | Y | True = shipped with EPCC; cannot delete | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

**System defaults:** Civil→Front_Loaded, MEP/HVAC→Bell, Commissioning→Back_Loaded, Indirect→Linear (per X8 §3.41).

---

### 3g. Entity: `Milestone`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `milestone_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34 |
| `project_id` | UUID | Y | — | LINK → M01 |
| `milestone_code` | VARCHAR(20) | Y | Unique within project; e.g., `MS-001` | INPUT |
| `wbs_id` | UUID | N | If maps to WBS milestone-type node | LINK → M02 |
| `package_id` | UUID | N | Package milestone governs | LINK → M02 |
| `milestone_name` | VARCHAR(200) | Y | Non-empty | INPUT |
| `milestone_type` | ENUM | Y | Per X8 §3.45 `MilestoneType` | INPUT |
| `phase_id` | ENUM | Y | Per X8 §3.9 Phase | INPUT |
| `planned_date` | DATE | Y | Within project dates | INPUT |
| `baseline_date` | DATE | N | Set at baseline lock | SYSTEM (snapshot) |
| `extended_baseline_date` | DATE | N | Auto = baseline_date + extensions | CALC |
| `forecast_date` | DATE | N | Updated by Planning Engineer weekly | INPUT |
| `actual_date` | DATE | N | From M04 (or M09 for compliance grants) | LINK → M04 / M09 |
| `status` | ENUM | Y | Per X8 §3.44 `MilestoneStatus` | CALC |
| `delay_days` | INTEGER | N | Auto-calculated | CALC |
| `delay_cause_category` | ENUM | N | Per X8 §3.40 if delayed | LINK → BaselineExtensionCause |
| `is_gate_linked` | BOOLEAN | Y | True = prerequisite for stage gate (M08) | INPUT |
| `gate_id` | VARCHAR(10) | N | Required if is_gate_linked=true | LINK → M08 |
| `predecessor_milestone_id` | UUID | N | Self-reference; same project | LINK → Milestone |
| `is_client_visible` | BOOLEAN | Y | True = in client progress report | INPUT |
| `created_by` | UUID | Y | — | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |

---

### 3h. Entity: `ResourceMaster` (4 types per OQ-1.5)

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `resource_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34 |
| `resource_name` | VARCHAR(200) | Y | Person/team name | INPUT |
| `resource_type` | ENUM | Y | Per X8 §3.42 `ResourceType` (4 values incl. **Vendor_Resource**) | INPUT |
| `role_default` | VARCHAR(100) | N | Default role for allocations | INPUT |
| `party_id` | UUID | C | Required if type=Contractor/Consultant/Vendor | LINK → M01.Party |
| `contract_id` | UUID | C | Required if type=Contractor/Consultant; optional for Vendor | LINK → M01.Contract |
| `engagement_start` | DATE | C | Required for external resources | INPUT |
| `engagement_end` | DATE | C | Required for external resources | INPUT |
| `max_allocation_pct` | DECIMAL(5,2) | Y | Default 100; e.g., 80 for shared resource | INPUT |
| `cost_rate_per_day` | DECIMAL(10,2) | N | Reference rate; full PO terms in M06 | INPUT |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

---

### 3i. Entity: `ResourceAllocation`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `allocation_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34 |
| `project_id` | UUID | Y | — | LINK → M01 |
| `wbs_id` | UUID | Y | — | LINK → M02 |
| `role_name` | VARCHAR(100) | Y | e.g., Site Manager, MEP Coordinator | INPUT |
| `resource_id` | UUID | N | Optional named resource | LINK → ResourceMaster |
| `allocation_pct` | DECIMAL(5,2) | Y | 0-100; default 100 | INPUT |
| `allocation_start` | DATE | Y | Aligned to wbs planned_start | INPUT |
| `allocation_end` | DATE | Y | Aligned to wbs planned_finish | INPUT |
| `is_confirmed` | BOOLEAN | Y | True only when resource_id populated | CALC |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |

---

### 3j. Entity: `ProcurementScheduleItem`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `procurement_item_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34 |
| `project_id` | UUID | Y | — | LINK → M01 |
| `package_id` | UUID | Y | — | LINK → M02 |
| `item_name` | VARCHAR(200) | Y | e.g., "LINAC", "MRI 1.5T" | INPUT |
| `item_code` | VARCHAR(30) | Y | Unique within project | INPUT |
| `lead_time_days` | INTEGER | Y | Manufacturing + transit | INPUT |
| `is_long_lead` | BOOLEAN | Y | True if lead_time_days ≥ 90 | CALC |
| `gate_id` | VARCHAR(10) | N | Required if is_long_lead=true (early gate assignment) | LINK → M08 |
| `latest_order_date` | DATE | Y | Auto = required_at_site − lead_time_days | CALC |
| `actual_order_date` | DATE | N | From M06 PO creation | LINK → M06 |
| `planned_delivery_date` | DATE | Y | Auto = actual_order_date + lead_time_days (or planned) | CALC |
| `actual_delivery_date` | DATE | N | From M04 MaterialReceipt | LINK → M04 |
| `installation_target_date` | DATE | Y | Aligned to WBS install activity | INPUT |
| `actual_installation_date` | DATE | N | From M04 progress | LINK → M04 |
| `m06_po_id` | UUID | N | FK to M06 PurchaseOrder when issued | LINK → M06 |
| `status` | ENUM | Y | Per X8 §3.47 `ProcurementItemStatus` | CALC |
| `order_delay_days` | INTEGER | N | Auto = actual_order_date − latest_order_date | CALC |
| `delivery_delay_days` | INTEGER | N | Auto = actual_delivery_date − planned_delivery_date | CALC |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |

**Vendor identity NOT stored here** — read via M06 API using `m06_po_id` (per OQ-1.9).

---

### 3k. Entity: `WeatherWindowConfig`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `weather_config_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34 |
| `project_id` | UUID | Y | — | LINK → M01 |
| `window_name` | VARCHAR(100) | Y | e.g., "Monsoon 2026" | INPUT |
| `start_date` | DATE | Y | Within project dates | INPUT |
| `end_date` | DATE | Y | > start_date | INPUT |
| `severity` | ENUM | Y | Per X8 §3.48 `WeatherWindowSeverity` | INPUT |
| `productivity_factor` | DECIMAL(3,2) | Y | 0.00-1.00; aligns to severity band | INPUT |
| `affected_categories` | JSONB | Y | Array of activity_category values | INPUT |
| `is_factored_into_schedule` | BOOLEAN | Y | If true, BR-03-020 adjusts float | INPUT |
| `region_default` | VARCHAR(100) | N | If sourced from region template | INPUT |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |

---

### 3l. Entity: `LookAheadConfig`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `config_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34 |
| `project_id` | UUID | Y | UNIQUE — exactly one per project | LINK → M01 |
| `look_ahead_weeks` | INTEGER | Y | Range 2-12; default 4 | INPUT |
| `reporting_period_type` | ENUM | Y | Per X8 §3.43 `ReportingPeriodType`; default Monthly | INPUT |
| `last_period_change_at` | TIMESTAMP | N | Auto on reporting_period_type change | SYSTEM |
| `last_period_change_by` | UUID | N | Auto | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

**Ownership:** This entity owns `reporting_period_type`. M01 v1.2 (cascade in this round) reads via API; no longer stores on Project.

---

### 3m. Entity: `ScheduleImport`

Schedule import session metadata for Primavera/MSP imports. Pattern matches M02 CSVImportSession.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `import_session_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34 |
| `project_id` | UUID | Y | — | LINK → M01 |
| `import_source` | ENUM | Y | Per X8 §3.50 `ScheduleImportSource` | INPUT |
| `import_mode` | ENUM | Y | Per X8 §3.51 `ScheduleImportMode`; **no default** | INPUT |
| `source_file_name` | VARCHAR(300) | Y | Original filename | SYSTEM |
| `source_file_size_bytes` | BIGINT | Y | Max 20 MB | SYSTEM |
| `total_activities` | INTEGER | Y | After parse; max 10,000 | SYSTEM |
| `validation_status` | ENUM | Y | Pending/Valid/Invalid | SYSTEM |
| `validation_report` | JSONB | N | Per-activity pass/fail | SYSTEM |
| `conflict_log` | JSONB | N | Conflicts with existing data | SYSTEM |
| `commit_status` | ENUM | Y | Not_Committed/Committed/Rolled_Back | SYSTEM |
| `committed_at` | TIMESTAMP | N | Auto on commit | SYSTEM |
| `committed_by` | UUID | N | — | LINK → M34.User |
| `created_by` | UUID | Y | — | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |

---

### 3n. Entity: `ScheduleImportRecord` (append-only)

Per-activity import audit. Pattern matches M02 CSVImportRecord.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `record_id` | UUID | Y | Auto-generated | SYSTEM |
| `import_session_id` | UUID | Y | FK → ScheduleImport | LINK → ScheduleImport |
| `source_activity_id` | VARCHAR(50) | Y | From source file | SYSTEM |
| `target_wbs_id` | UUID | N | Resolved match in M02 | SYSTEM |
| `action` | ENUM | Y | Created/Updated/Failed/Skipped_Duplicate | SYSTEM |
| `failure_reason` | TEXT | N | Required if Failed | SYSTEM |
| `changed_fields` | JSONB | N | If Updated | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |

**Append-only.**

---

## BLOCK 4 — DATA POPULATION RULES

### 4a. Role × Action Permission Matrix

| Action | SYS_ADMIN | PMO_DIR | PORTFOLIO | PROJ_DIR | PLAN_ENG | QS_MGR | FIN_LEAD | PROC | SITE_MGR | COMP_MGR | READ_ONLY |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Create/edit schedule (pre-baseline) | ❌ | ✅ | ❌ | ✅ (own) | ✅ (own) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Edit schedule (post-baseline) | ❌ | ✅ (via ext.) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Lock baseline | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Submit baseline extension | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Approve baseline extension | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Override billable/vendor flags | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Create/edit milestones | ❌ | ✅ | ❌ | ✅ (own) | ✅ (own) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Update milestone forecast | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Configure loading profiles | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Override PV period | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Allocate resources (role) | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Assign named resource | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Manage ResourceMaster | ❌ | ✅ | ❌ | ✅ (own type) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Create/edit procurement schedule | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Configure weather windows | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Configure look-ahead window | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Schedule import | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **View float values** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ (status only) |
| View all schedule | ✅ | ✅ | ✅ | ✅ (own) | ✅ (own) | ✅ (own) | ✅ | ✅ (own) | ✅ (own pkg) | ✅ (own) | ✅ (own) |

**Float visibility (BR-03-031, OQ-1.10):** All editing roles see float values; READ_ONLY sees only schedule status badges (no float numerics).

---

### 4b. Mandatory vs Optional

| Field / Group | Mandatory | System Behaviour if Empty |
|---|---|---|
| ScheduleEntry planned_start + planned_finish | Y (before baseline) | Blocks baseline lock (BR-03-003) |
| Loading profile per WBS | Y (defaults auto-applied) | System applies category default; user override allowed |
| Milestone planned_date | Y | Blocks save |
| Milestone type + phase | Y | Blocks save |
| Gate-linked milestones (SG-4 to SG-11) | Y (before gate active) | M08 blocks gate if missing (BR-03-004) |
| Resource role per Level 3 task | Y | Warning if missing; doesn't block save |
| Named resource | N | Allocation marked unconfirmed |
| Procurement lead time + order date (long-lead) | Y | Blocks long-lead flag if empty |
| BaselineExtension cause description | Y (min 50 chars) | Blocks save |
| Contract clause for Neutral_Event | Y or auto-reclassify | System reclassifies to Contractor_Delay (BR-03-008) |
| Supporting evidence URL for Neutral_Event/Force_Majeure | Y | Blocks save (BR-03-009) |
| VO link for billable extension | Y | Blocks approval (BR-03-010) |
| Project-level extension justification | Y (min 100 chars) if exception=true | Blocks save (BR-03-026) |
| Weather window productivity factor | Y | Blocks save |
| PV override reason | Y (if override=true) | Blocks save (BR-03-013) |

---

### 4c. Default Values

| Field | Default | Source |
|---|---|---|
| `LookAheadConfig.look_ahead_weeks` | 4 | OQ-1.7 |
| `LookAheadConfig.reporting_period_type` | Monthly | OQ-2.8 |
| `BaselineExtension.is_billable_to_client` | Per cause auto-classification | X8 §3.40 |
| `BaselineExtension.counts_against_vendor` | Per cause auto-classification | X8 §3.40 |
| `Milestone.is_client_visible` | true | — |
| `Milestone.is_gate_linked` | false | — |
| `ResourceAllocation.allocation_pct` | 100 | — |
| `ResourceMaster.max_allocation_pct` | 100 | — |
| `LoadingProfile` defaults | Civil→Front_Loaded, MEP→Bell, Commissioning→Back_Loaded, Indirect→Linear | X8 §3.41 |
| `WeatherWindowConfig.is_factored_into_schedule` | true | — |
| Schedule import file size | 20 MB / 10,000 activities | OQ-2.11 |

---

## BLOCK 5 — FILTERS AND VIEWS

### 5a. Default Role-Based Views

**See X9 §13.3.3 (v0.2)** — Locked role-default views per role for M03. Reproduced from X9 for reference (full canonical specification in X9):

| Role | Primary View | Secondary Widgets |
|---|---|---|
| PMO_DIRECTOR | Master Gantt with baseline + critical path | Milestone timeline, S-curve variance, RAG status |
| PORTFOLIO_MANAGER | Schedule variance summary (multi-project) | Cross-project critical path comparison |
| **PROJECT_DIRECTOR** | **Master Gantt (own) + variance bar** | **Look-ahead Gantt, milestone timeline, PV S-curve (cost overlay)** ⭐ |
| **PLANNING_ENGINEER** | **WBS Gantt builder + float histogram** | **Critical path DAG, baseline lock state, PV roll-up shape** ⭐ |
| SITE_MANAGER | 4-week Look-ahead Gantt | Today's milestones, resource roster |
| QS_MANAGER | Master Gantt (read) + procurement schedule | BOQ progress |
| FINANCE_LEAD | PV S-curve + procurement Gantt | Financial milestones, schedule variance ₹ impact |
| PROCUREMENT_OFFICER | Procurement Gantt | Long-lead-time alerts, vendor schedule |
| COMPLIANCE_MANAGER | Permit Gantt + milestone timeline | Compliance events on schedule |
| READ_ONLY | Master Gantt (read-only, no float) | — |
| EXTERNAL_AUDITOR | Schedule + extension log (forensic) | Audit trail |

⭐ = Updates from X9 v0.1 → v0.2 per OQ-1.11 (PROJECT_DIRECTOR + PV S-curve secondary; PLANNING_ENGINEER + PV roll-up shape).

### 5b. Chart Specifications

**See X9 §8.3 (v0.2)** — Locked chart matrix per M03. Charts:

| Chart | Type (X9) | Decision Answered |
|---|---|---|
| Master Gantt with Baseline + Critical Path | gantt_with_overlay | Is the project on schedule? |
| Variance Bar | bar_horizontal | What's the variance to baseline by WBS? |
| Look-ahead Gantt | gantt_filtered | What needs to happen in next 4 weeks? |
| Critical Path DAG | network_dag | Are critical path activities healthy? |
| Milestone Timeline | timeline | Are milestones being hit? |
| Schedule S-curve | line_multi_series | Is planned vs actual progress tracking? |
| Resource Histogram | bar_stacked_time | Are resources over/under-loaded? |
| Procurement Gantt | gantt | Are long-lead items ordered in time? |
| Float Histogram | histogram | Float distribution — close to critical? |
| PV S-curve | line_simple | Cumulative planned value over time? |

All chart components implement X9 §14 contracts.

### 5c. Filter Patterns

Standard filters per view per X9 conventions: activity_category, status, baseline lock state, period range, role-scoped project list.

### 5d. Schedule Import Wizard

5-step modal-gated wizard following M02 CSV import pattern:

```
Step 1: Source selection (Primavera_P6_XML / Primavera_P6_XER / MSP_XML)
Step 2: Mode selection — REQUIRED, no default:
  [ ] Create_Only — fail on duplicate
  [ ] Create_And_Update — sparse update on match
Step 3: File upload (max 20 MB / 10,000 activities)
Step 4: Preview validation + conflict log
Step 5: Confirm commit (all-or-nothing)
```

---

## BLOCK 6 — BUSINESS RULES

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---|---|---|---|---|
| BR-03-001 | Schedule entry create | planned_finish > planned_start | Block save | 🔴 Real-time |
| BR-03-002 | Schedule entry create | Dates within project planned dates (M01) | Block save | 🔴 Real-time |
| BR-03-003 | Baseline lock attempt | All Level 3+ WBS task nodes have planned_start + planned_finish | Block lock if any null | 🔴 Real-time |
| BR-03-004 | Baseline lock attempt | All gate-linked milestones (SG-4 to SG-11) exist with planned_dates | Block lock if any missing | 🔴 Real-time |
| BR-03-005 | Baseline lock execute | Copy planned_start/finish → baseline_start/finish for all entries; create Baseline JSONB snapshot; set is_baseline_locked=true | Immutable snapshot persisted | 🔴 Real-time |
| BR-03-006 | Baseline lock execute | Insert Baseline record with full pv_snapshot + milestone_snapshot | Sealed forever | 🔴 Real-time |
| BR-03-007 | Schedule edit attempt post-baseline | Direct edit of planned_start/planned_finish | Block edit; force BaselineExtension workflow | 🔴 Real-time |
| BR-03-008 | BaselineExtension save | cause_category=Neutral_Event AND contract_clause_ref blank | Auto-reclassify to Contractor_Delay; log NEUTRAL_EVENT_RECLASSIFIED; notify submitter | 🔴 Real-time |
| BR-03-009 | BaselineExtension save | cause_category in (Neutral_Event, Force_Majeure) AND supporting_evidence_url blank | Block save | 🔴 Real-time |
| BR-03-010 | BaselineExtension approval | is_billable_to_client=true AND variation_order_id is null | Block approval; VO must exist in M05 first | 🔴 Real-time |
| BR-03-011 | BaselineExtension approval execute | Recalc extended_baseline_finish for affected WBS + milestones; cascade schedule_variance_days update | Persist; notify M07 | 🔴 Real-time |
| BR-03-012 | LoadingProfile assigned to WBS | Generate PVProfile records for all reporting periods of WBS | Persist; notify M07 | 🔴 Real-time |
| BR-03-013 | PVProfile override | is_overridden=true AND override_reason blank | Block save | 🔴 Real-time |
| BR-03-014 | report_date update (from M01) | Recalc all schedule_variance_days; trigger PV recalc cascade | Cascade update | 🔴 Real-time |
| BR-03-015 | Milestone forecast update | forecast_date > extended_baseline_date by > 7 days AND is_gate_linked=true | Generate Decision SCHEDULE_RECOVERY_REQUIRED; notify Project Director | 🔴 Real-time |
| BR-03-016 | Daily procurement check | latest_order_date < today AND actual_order_date is null | Generate Decision PROCUREMENT_ESCALATION; notify Procurement Officer | 🟡 2-4hr |
| BR-03-017 | Long-lead item save | is_long_lead=true AND gate_id is null | Warning to Planning Engineer | 🟡 2-4hr |
| BR-03-018 | Critical path activity update | is_on_critical_path=true AND schedule_variance_days > 5 | Generate Decision CRITICAL_PATH_DELAY; notify Project Director + PMO | 🔴 Real-time |
| BR-03-019 | Resource conflict detection | Same named resource > max_allocation_pct in any period | Flag conflict; block confirmation | 🟡 2-4hr |
| BR-03-020 | Weather window active | Window overlaps WBS dates AND is_factored_into_schedule=true | Adjust effective float; reduce productivity in PV distribution | 🟢 24hr |
| BR-03-021 | Daily milestone check | Milestone in (Not_Started, In_Progress) AND extended_baseline_date < today | Auto-update status to Delayed; notify Planning Engineer | 🟢 24hr |
| BR-03-022 | M06 PO created | M06 sends actual_order_date | Populate ProcurementScheduleItem.actual_order_date; calc order_delay_days; status → Order_Placed | 🔴 Real-time |
| BR-03-023 | Schedule import session create | Import mode must be explicitly selected | Block if mode unselected | 🔴 Real-time |
| BR-03-024 | Schedule import preview | Conflict detection — imported date differs from existing | Show in conflict_log; block commit until resolved | 🔴 Real-time |
| BR-03-025 | Schedule import — post-baseline | Date change after baseline lock | Block direct overwrite; route to BaselineExtension workflow | 🔴 Real-time |
| BR-03-026 | Project-level extension save | is_project_level_exception=true AND project_level_justification < 100 chars | Block save | 🔴 Real-time |
| BR-03-027 | Project-level extension approval | is_project_level_exception=true | Requires PMO_DIRECTOR; generate Decision record | 🔴 Real-time |
| BR-03-028 | reporting_period_type change post-baseline | Change after baseline lock | Requires PMO_DIRECTOR; trigger full PV regeneration; log REPORTING_PERIOD_TYPE_CHANGED | 🔴 Real-time |
| BR-03-029 | External resource allocation | resource_type in (Contractor_Resource, Consultant_Resource, Vendor_Resource) AND engagement_end < activity planned_finish | Warning; block confirmation | 🔴 Real-time |
| BR-03-030 | Resource over-allocation | Named resource total allocation_pct > max_allocation_pct in any period | Flag conflict; generate Decision RESOURCE_OVER_ALLOCATION_CONFLICT | 🔴 Real-time |
| BR-03-031 | Float read by READ_ONLY | API request for float value | Return null/redacted; show status badge only | 🔴 Real-time |
| BR-03-032 | M09 compliance grant date received | Compliance permit grant_date populated | Auto-populate linked Milestone.actual_date; status → Achieved | 🔴 Real-time |
| BR-03-033 | ScheduleEntry persist (BR-03-018 dependency) | Critical-path recomputation must execute within the same DB transaction as the ScheduleEntry persist | If recompute fails, rollback persist; no stale-read for BR-03-018 firing | 🔴 Real-time |
| BR-03-034 | reporting_period_type change post-baseline (BR-03-028 strengthening) | Atomic transaction: change reporting_period_type AND full PV regeneration in single commit | If PV regen fails, rollback reporting_period_type; emit REPORTING_PERIOD_CHANGE_FAILED; never leave project in mixed-period state | 🔴 Real-time |

---

## BLOCK 7 — INTEGRATION POINTS

| Direction | Module | Data Exchanged | Trigger | Speed Tier |
|---|---|---|---|---|
| RECEIVES FROM | M34 | Auth, role, scope | Every API call | 🔴 |
| RECEIVES FROM | M01 | project_id, current_phase, planned dates, report_date, contract_id | On project state change | 🔴 |
| RECEIVES FROM | M02 | wbs_id list, package_id list, BAC per package, WBS hierarchy | On WBS create/update | 🔴 |
| RECEIVES FROM | M05 | variation_order_id (linkage); EOT VO triggers BaselineExtension | On VO approval (cost_impact > 0) | 🔴 |
| RECEIVES FROM | M08 | SG-6 gate passage signal → triggers baseline lock | On gate passage | 🔴 |
| RECEIVES FROM | M09 | Compliance permit grant_date → auto-populate Milestone.actual_date | On permit grant | 🔴 |
| RECEIVES FROM | M04 | MaterialReceipt date → ProcurementScheduleItem.actual_delivery_date | On material receipt | 🔴 |
| RECEIVES FROM | M06 | PO created → ProcurementScheduleItem.actual_order_date | On PO create | 🔴 |
| SENDS TO | M01 | reporting_period_type via API (M01 v1.2 reads) | On config change | LINK |
| SENDS TO | M04 | wbs_id list with planned dates | On schedule create/update | 🔴 |
| SENDS TO | M05 | Schedule context for VO impact assessment | On query | LINK |
| SENDS TO | M06 | Procurement schedule (PO timing); PV per period (cashflow forecast) | On schedule create + period | 🔴 |
| SENDS TO | M07 | **PV per period per WBS — foundation of EVM** | On any PV change | 🔴 |
| SENDS TO | M08 | Baseline state + gate-linked milestones | On baseline lock + milestone update | 🔴 |
| SENDS TO | M09 | Schedule for permit timeline overlay | On query | LINK |
| SENDS TO | M10 | Schedule health, critical path, milestone summary, S-curve | On any change | 🟡 2-4hr |
| SENDS TO | M11 | 5 Decision Queue triggers | When triggered | 🔴 |

---

## BLOCK 8 — GOVERNANCE AND AUDIT

### 8a. Logged Events

| Action | Logged | Detail | Visible To | Retention |
|---|---|---|---|---|
| Schedule entry create/update | Yes | All fields, before/after | PMO_DIR, PROJECT_DIR | Project lifetime |
| Baseline lock | Yes | Timestamp, gate ref, locker | All | **Permanent** |
| BaselineExtension submit | Yes | All fields, submitter | PMO_DIR, PROJECT_DIR | Permanent |
| BaselineExtension approve/reject | Yes | Decision, approver, reason | All | Permanent |
| Neutral_Event reclassified | Yes | Original + reclassification reason | PMO_DIR, FIN_LEAD | Permanent |
| Billable flag override | Yes | Old/new, reason, PMO | PMO_DIR, FIN_LEAD | Permanent |
| Vendor flag override | Yes | Old/new, reason, PMO | PMO_DIR | Permanent |
| PV override | Yes | Period, old/new PV, reason | PMO_DIR | Project lifetime |
| Milestone status change | Yes | Old/new status | All | Project lifetime |
| Milestone forecast update | Yes | Old/new date | PMO_DIR, PROJECT_DIR | Project lifetime |
| Procurement schedule edit | Yes | Old/new fields | PMO_DIR, PROC_OFF, PROJECT_DIR | Project lifetime |
| Long-lead delay alert | Yes | Item, days late | PMO_DIR, PROC_OFF | Permanent |
| Loading profile assign | Yes | WBS, profile, user | PMO_DIR, PLAN_ENG | Project lifetime |
| Resource allocation conflict | Yes | Resource, periods, conflict detail | PMO_DIR, PROJECT_DIR | Project lifetime |
| Critical path delay alert | Yes | Activity, variance days | All | Permanent |
| Weather window config | Yes | Window, factor, user | PMO_DIR | Permanent |
| Look-ahead window change | Yes | Old/new weeks | PMO_DIR | Project lifetime |
| Reporting period change | Yes | Old/new type, regen trigger | PMO_DIR | **Permanent** |
| Schedule import session | Yes | Source, mode, file, commit | PMO_DIR + initiator | Permanent |
| PV recalc cascade | Yes | Trigger, scope, duration | PMO_DIR | Project lifetime |
| Critical path recalc | Yes | Trigger, affected WBS | PMO_DIR | Project lifetime |

### 8b. Immutability Rules

- **`Baseline`** — DB-level UPDATE/DELETE forbidden; INSERT only at SG-6 lock
- **`BaselineExtension`** — Append-only after approval (status=Approved); no field changes permitted
- **`PVProfileSnapshot`** — Append-only at report_date changes
- **`ScheduleImportRecord`** — Append-only

### 8c. Privacy

- Float values are role-tiered; READ_ONLY and external portal users see status badges only (BR-03-031)
- Baseline extensions and reasons are auditable but not exposed to external roles in v1.0
- PV values inherit M02 BR-02-008 rate display tiering

---

## BLOCK 9 — EXPLICIT EXCLUSIONS

```
This module does NOT:
─────────────────────────────────────────────────────────────────────
[ ] Define WBS structure or hierarchy                          → M02
[ ] Store BOQ items or package master                          → M02
[ ] Capture actual progress (% complete)                       → M04
[ ] Track actual cost transactions                             → M06
[ ] Compute EVM (CPI, SPI, EAC, ETC, VAC, TCPI)               → M07
[ ] Approve stage gates                                        → M08
[ ] Manage risk register or variation orders                   → M05
[ ] Store vendor identity (vendor_id, name, terms)             → M06
[ ] Manage vendor PO value or payment terms                    → M06
[ ] Track regulatory compliance status                         → M09
[ ] Store project documents                                    → MinIO + M12
[ ] Score contractor performance                               → M04
[ ] Manage sub-contract financial terms                        → M06
[ ] Define gate entry/exit criteria                            → M08
[ ] Integrate with BIM models                                  → PF02 (Phase 4)
[ ] Support schedule re-baselining (versioned baselines)       → NOT SUPPORTED v1.0
[ ] Authenticate users / manage roles                          → M34
```

---

## BLOCK 10 — OPEN QUESTIONS

**All questions resolved. Zero open questions.**

| # | Question | Resolution |
|---|---|---|
| 1.1 | Baseline model? | **Single immutable + Approved Extensions (OQ-1.1=A).** Audit-clean; forces governance. |
| 1.2 | Cause categories? | **Lock 6 (OQ-1.2=A).** Healthcare reality covered. X8 §3.40. |
| 1.3 | Neutral_Event auto-reclassify? | **Keep legacy auto-reclassify to Contractor_Delay (OQ-1.3=A).** Contract clause omission = contractor risk. BR-03-008. |
| 1.4 | LoadingProfile types? | **Lock 5 (OQ-1.4=A).** Custom covers any non-standard. X8 §3.41. |
| 1.5 | ResourceType taxonomy? | **4 types incl. Vendor_Resource (OQ-1.5=B).** KDMC MEP vendor reality. X8 §3.42. |
| 1.6 | ReportingPeriodType? | **Lock 4 (OQ-1.6=A).** X8 §3.43. |
| 1.7 | Look-ahead window? | **Default 4w, range 2-12 (OQ-1.7=A).** Legacy proven. |
| 1.8 | reporting_period_type owner? | **M03 owns (OQ-1.8=A).** M01 v1.2 cascade removes field. |
| 1.9 | Procurement vendor identity? | **M06 owns (OQ-1.9=B).** Single-Owner rule; vendor identity = financial. |
| 1.10 | Float visibility? | **All editing roles see; READ_ONLY status only (OQ-1.10=A).** BR-03-031. |
| 1.11 | Role-default views? | **B with adjustments 1.11.a + 1.11.b (OQ-1.11=B).** PROJECT_DIRECTOR + PV S-curve secondary; PLANNING_ENGINEER + PV roll-up shape. X9 v0.2 cascade. |
| OQ-2 | All pattern defaults | **ACCEPT ALL.** |

---

## APPENDIX A — Migration Plan

```
Migration: 20260503_0030_m03_initial_schema.py
  - Creates: ScheduleEntry, Baseline, BaselineExtension, PVProfile,
    PVProfileSnapshot, LoadingProfile, Milestone, ResourceAllocation,
    ResourceMaster, ProcurementScheduleItem, WeatherWindowConfig,
    LookAheadConfig, ScheduleImport, ScheduleImportRecord
  - Enforces UPDATE/DELETE revocation on baseline + baseline_extension (post-approval)
  - Composite uniqueness on entity codes within scope
  - FK constraints to M01 + M02 + M34

Migration: 20260503_0031_m03_seed_loading_profiles.py
  - Seeds system default LoadingProfiles per X8 §3.41 mapping

Migration: 20260503_0032_m01_v1_2_remove_reporting_period.py
  - Drops Project.reporting_period_type column
  - LookAheadConfig becomes single source

Migration: 20260503_0033_m03_seed_kdmc_baselines.py
  - Seeds KDMC pilot procurement long-lead items:
    LINAC, MRI, CT Scanner, Cath Lab, OT Equipment, MGPS
  - Default monsoon WeatherWindowConfig for KDMC region
```

---

## APPENDIX B — KDMC Reference Data Mapping

| KDMC Excel Source | M03 Entity | Notes |
|---|---|---|
| 03_Milestones | Milestone | Key dates, delay tracking |
| 03_Phase_Gate_Tracker | Milestone (gate-linked) + M08 | Gate criteria feed M08 |
| 03_Resource_Allocation | ResourceAllocation | Role-level; named optional |
| 03_Procurement_Control | ProcurementScheduleItem | Long-lead: LINAC (18-24m), MRI (14-16m) |
| 02_WBS date columns | ScheduleEntry | 438 WBS nodes |
| 01_ASSUMPTIONS monsoon | WeatherWindowConfig | Default 2-month monsoon window |
| 01_MODEL_INPUTS report_date | report_date cascade | Drives PV recalc |

**KDMC Long-Lead Items:**
```
LINAC           18-24 months    latest_order_date = SG-5 date
MRI             14-16 months    latest_order_date = SG-5 date
CT Scanner      10-12 months    latest_order_date = SG-5 date
Cath Lab        12-14 months    latest_order_date = SG-5 date
OT Equipment     8-10 months    latest_order_date = SG-6 date
MGPS             6-8 months     latest_order_date = SG-6 date
```

---

## APPENDIX C — Audit Events Catalogue (Spec v1.1, Round 18 cascade)

> **Status:** LOCKED. Source of truth for M03 audit event names until X3 Audit Event Catalogue is built. When X3 lands, these names migrate to X3 unchanged (forward-traceability commitment). Naming follows X8 §2 — UPPER_SNAKE_CASE.
>
> **Scope:** Twenty-eight events surfaced across M03 v1.0 BRs and Workflows v1.0. Listed alphabetically below.

### Event registry

| Event Name | Source BR(s) | Workflow | Severity | Trigger Description |
|---|---|---|---|---|
| `AUTHZ_DENIED` | M34 RBAC | WF-03-001 | Medium | RBAC fail at API entry (proxy-emitted; M34-owned, listed for closure) |
| `BASELINE_EXTENSION_BLOCKED` | BR-03-009, BR-03-010 | WF-03-003 | Medium | Evidence URL missing OR billable extension without VO |
| `BASELINE_EXTENSION_RAISED` | BR-03-008..011 | WF-03-003 | Info | Pending extension row inserted |
| `BASELINE_LOCKED` | BR-03-005, BR-03-006 | WF-03-002 | High | Atomic transaction commits — irreversible |
| `BASELINE_LOCK_BLOCKED` | BR-03-003, BR-03-004 | WF-03-002 | Medium | Pre-check fail (missing dates or gate milestones); `reason` enum |
| `BASELINE_LOCK_FAILED` | BR-03-005, BR-03-006 | WF-03-002 | Critical | Atomic transaction rolled back |
| `BASELINE_LOCK_INITIATED` | BR-03-003, BR-03-004 | WF-03-002 | Info | Pre-checks passed; routed to PMO_DIRECTOR |
| `BASELINE_LOCK_REJECTED` | BR-03-005, BR-03-006 | WF-03-002 | High | PMO_DIRECTOR declined |
| `CRITICAL_PATH_DELAY` | BR-03-018 | WF-03-007 | High | **Decision Queue trigger** — critical-path activity variance > 5d |
| `EXTENSION_APPROVED` | BR-03-011 | WF-03-003 | High | PMO approves; cascade to M07 complete |
| `EXTENSION_REJECTED` | BR-03-011 | WF-03-003 | Medium | PMO declines |
| `LONG_LEAD_NO_GATE_LINK` | BR-03-017 | WF-03-006 | Low | Warning — long-lead item saved without gate link |
| `M09_GRANT_ORPHANED` | BR-03-032 | WF-03-005 | Medium | M09 grant_date received with no linked milestone |
| `MILESTONE_AUTO_ACHIEVED` | BR-03-032 | WF-03-005 | Info | M09 cascade flips status to Achieved |
| `MILESTONE_AUTO_DELAYED` | BR-03-021 | WF-03-005 | Medium | Daily sweep flips status to Delayed |
| `MILESTONE_FORECAST_UPDATED` | BR-03-015 | WF-03-005 | Info | Forecast date persisted |
| `NEUTRAL_EVENT_RECLASSIFIED` | BR-03-008 | WF-03-003 | Medium | Pre-existing in v1.0; auto-reclassify Neutral_Event → Contractor_Delay |
| `POST_BASELINE_EDIT_BLOCKED` | BR-03-007 | WF-03-001 | Medium | Direct date edit attempted post-baseline |
| `PO_LINKED_TO_SCHEDULE` | BR-03-022 | WF-03-006 | Info | M06 PO event populates actual_order_date |
| `PROCUREMENT_ESCALATION` | BR-03-016 | WF-03-006 | High | **Decision Queue trigger** — daily sweep finds late order |
| `PROJECT_LEVEL_EXCEPTION_APPROVED` | BR-03-027 | WF-03-009 | High | PMO approves project-level extension |
| `PROJECT_LEVEL_EXCEPTION_BLOCKED` | BR-03-026 | WF-03-009 | Medium | Justification < 100 chars |
| `PROJECT_LEVEL_EXCEPTION_RAISED` | BR-03-027 | WF-03-009 | High | Flagged extension persisted; PMO Decision generated |
| `PROJECT_LEVEL_EXCEPTION_REJECTED` | BR-03-027 | WF-03-009 | Medium | PMO declines |
| `PV_PROFILE_GENERATED` | BR-03-012 | WF-03-004 | Info | LoadingProfile assignment generates PV rows |
| `PV_PROFILE_OVERRIDDEN` | BR-03-013 | WF-03-004 | Medium | Manual override persisted with reason |
| `PV_PROFILE_OVERRIDE_BLOCKED` | BR-03-013 | WF-03-004 | Low | Blank override_reason |
| `REPORT_DATE_PV_RECALCULATED` | BR-03-014 | WF-03-004 | Info | M01 report_date update triggers cascade |
| `REPORTING_PERIOD_CHANGE_FAILED` | BR-03-034 | WF-03-009 | Critical | Atomic rollback fired during reporting_period_type change |
| `REPORTING_PERIOD_TYPE_CHANGED` | BR-03-028, BR-03-034 | WF-03-009 | High | Pre-existing in v1.0; atomic change with PV regen committed |
| `RESOURCE_CONFLICT_FLAGGED` | BR-03-019 | WF-03-007 | Medium | Over-allocation detected; confirmation blocked |
| `RESOURCE_EXTERNAL_ENGAGEMENT_GAP` | BR-03-029 | WF-03-007 | Medium | External resource engagement_end < activity planned_finish |
| `RESOURCE_OVER_ALLOCATION_CONFLICT` | BR-03-030 | WF-03-007 | High | **Decision Queue trigger** — same trigger as BR-019, generates Decision |
| `SCHEDULE_ENTRY_CREATED` | BR-03-001, BR-03-002 | WF-03-001 | Info | ScheduleEntry insert |
| `SCHEDULE_ENTRY_UPDATED` | BR-03-001, BR-03-002 | WF-03-001 | Info | ScheduleEntry update |
| `SCHEDULE_ENTRY_VALIDATION_FAILED` | BR-03-001, BR-03-002 | WF-03-001 | Low | Date logic OR project bounds reject; `reason` enum |
| `SCHEDULE_IMPORT_COMMITTED` | BR-03-023..025 | WF-03-008 | Info | Final commit with row counts |
| `SCHEDULE_IMPORT_INITIATED` | BR-03-023 | WF-03-008 | Info | Import session created |
| `SCHEDULE_IMPORT_MODE_MISSING` | BR-03-023 | WF-03-008 | Low | Mode unselected |
| `SCHEDULE_IMPORT_PREVIEW_BLOCKED` | BR-03-024 | WF-03-008 | Medium | Conflicts unresolved at preview |
| `SCHEDULE_RECOVERY_REQUIRED` | BR-03-015 | WF-03-005 | High | **Decision Queue trigger** — gate-linked milestone forecast > baseline + 7d |
| `WEATHER_WINDOW_APPLIED` | BR-03-020 | WF-03-007 | Info | Factored window adjusts float / productivity |
| `WEATHER_WINDOW_REVERSED` | BR-03-020 | WF-03-007 | Info | Factored flag toggled false; adjustment reversed |

### Notes

- **Pre-existing in v1.0 (2 events):** `NEUTRAL_EVENT_RECLASSIFIED`, `REPORTING_PERIOD_TYPE_CHANGED`. Confirmed unchanged here.
- **Newly locked in v1.1 (26 events + 1 sibling):** all others. `REPORTING_PERIOD_TYPE_CHANGED` gains a sibling `REPORTING_PERIOD_CHANGE_FAILED` for the BR-03-034 rollback path.
- **Decision Queue triggers (5):** `CRITICAL_PATH_DELAY`, `PROCUREMENT_ESCALATION`, `RESOURCE_OVER_ALLOCATION_CONFLICT`, `SCHEDULE_RECOVERY_REQUIRED`, plus `PROJECT_LEVEL_EXCEPTION_RAISED` (PMO routing). Matches the "5 Decision Queue triggers" line in BLOCK 7 integration to M11.
- **Out-of-scope events listed for closure:** `AUTHZ_DENIED` is M34-owned but emitted on the M03 path; included for traceability only.
- **BR-03-031 (READ_ONLY float redaction):** No event emitted. Redaction is a serialiser-layer rule logged at API gateway access logs only.
- **Cross-reference:** BLOCK 8a "Logged Events" describes *what* is logged (action-level, retention-tagged); Appendix C names the *event constants* (machine-level). Complementary, not duplicate.

---

*v1.1 — Spec re-locked. Round 18 cascade absorbed. Zero open questions. M03 module COMPLETE pending Workflows v1.0 lock.*
