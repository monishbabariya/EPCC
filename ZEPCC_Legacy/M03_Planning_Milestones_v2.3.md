# M03 — Planning & Milestones
## Module Specification v2.3
**Status:** Draft — Pending Review | **Locked:** No
**Spec Author:** PMO Director | **Date:** 2026-04-30
**Reference Standards:** EPCC_Standards_Memory.md v2.1
**Depends On:** M01 locked (project_id, contract_id) + M02 locked (wbs_id, package_id, boq_id)

---

## CHANGE LOG

| Version | Date | Change Summary |
|---------|------|---------------|
| v1.0 | 2026-04-30 | Initial draft |
| v2.0 | 2026-04-30 | Block 10 resolved: CPM inbuilt + import; flexible period; WBS-attributed extensions; unified ResourceMaster |
| v2.1 | 2026-04-30 | Block 7: material receipt integration precision |
| v2.2 | 2026-04-30 | Block 7: EOT VO + contractor_delay_days |
| v2.3 | 2026-04-30 | Block 7 updated: M09 compliance grant dates auto-populate milestone actual_date + auto-create milestones for mandatory compliance items | approval in M05 auto-creates BaselineExtension in M03 (cause_category=Client_Delay); M05 reads contractor_delay_days for LD calculation | integration precision — actual_delivery_date now populated via MaterialReceipt.received_date through material_receipt_id FK |: CPM inbuilt + import; flexible reporting period; WBS-attributed extensions with controlled project-level exceptions; unified ResourceMaster with type classification |

---

## BLOCK 1 — Identity

```
Module ID             : M03
Module Name           : Planning & Milestones
Layer                 : L2 Control
Decision It Enables   : Is the project executing within its approved time baseline,
                        and where it is not — is the variance attributable to the
                        client (billable), the contractor (LD-applicable), a neutral
                        event (governed classification), or an approved scope extension
                        — such that schedule control, performance measurement, and
                        commercial recovery are all grounded in a single authoritative
                        baseline?
Primary User          : Planning Engineer
Secondary Users       : PMO Director, Project Director, Procurement Officer,
                        QS Manager, Finance Lead (procurement schedule read)
```

---

## BLOCK 2 — Scope Boundary

| INCLUDES | EXCLUDES |
|----------|---------|
| Master schedule — planned start/finish per WBS node | WBS structure and hierarchy → M02 |
| Baseline schedule (original) + Approved Extensions | BOQ items and package structure → M02 |
| Baseline extension classification and governance | Actual progress % complete → M04 |
| Planned Value (PV) — time-phased, S-curve distributed | Actual cost transactions → M06 |
| S-curve loading profiles per activity category | EVM calculations (CPI, SPI, EAC) → M07 |
| Milestone master — key dates, status, delay tracking | Stage gate approvals → M08 |
| Look-ahead schedule — filtered view (not separate entity) | Risk and variation register → M05 |
| Resource allocation — role (mandatory) + named (optional) | Vendor PO value and payment terms → M06 |
| Resource loading and utilisation summary | Regulatory compliance tracking → M09 |
| Procurement schedule — item, lead time, order/delivery dates | Vendor selection and PO financial details → M06 |
| Float / slack per WBS node | Document storage → Data Lake |
| Critical path (schedule-calculated — not structural flag) | Contractor performance scoring → M04 |
| Monsoon / weather window configuration | Sub-contract financial terms → M06 |
| Look-ahead window configuration (default 4 weeks) | Gate entry/exit criteria → M08 |

---

## BLOCK 3 — Data Architecture

### 3a. Entities

| Entity | Description | Cardinality |
|--------|-------------|-------------|
| `ScheduleEntry` | Time dimension for each WBS node — planned dates, baseline dates, float | 1 per WBS node |
| `Baseline` | Original approved schedule snapshot — immutable after lock | 1 per project |
| `BaselineExtension` | Approved addition to baseline — cause-classified, commercially tracked | Many per project |
| `PVProfile` | Time-phased planned value distribution per WBS node (S-curve) | 1 per WBS node per reporting period |
| `LoadingProfile` | S-curve distribution rule per activity category | Global shared — system defaults + user overrides |
| `Milestone` | Key project milestone — date, status, predecessor, delay tracking | Many per project |
| `ResourceAllocation` | Role + optional named person assignment per WBS node | Many per WBS node |
| `ResourceMaster` | Unified type-classified repository — internal staff, contractor, consultant. Differentiated governance and contract linkage. | Global shared |
| `ScheduleImport` | Tracks imports from Primavera / MSP — version, source file, import log, conflict resolution | Many per project |
| `ProcurementScheduleItem` | Schedule-layer of procurement — lead time, order date, delivery date, installation date | Many per project |
| `WeatherWindowConfig` | Monsoon / seasonal working restriction per project | 1–many per project |
| `LookAheadConfig` | Rolling look-ahead window setting per project | 1 per project |

---

### 3b. Key Fields

#### Entity: `ScheduleEntry`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `schedule_id` | UUID | Y | Auto-generated | SYSTEM |
| `wbs_id` | UUID | Y | Must exist in WBSNode (M02) | LINK → M02 WBSNode |
| `project_id` | UUID | Y | Must match WBSNode project | LINK → M01 Project |
| `planned_start` | DATE | Y | Must be within project dates | INPUT |
| `planned_finish` | DATE | Y | Must be > planned_start | INPUT |
| `duration_days` | INTEGER | Y | Auto = planned_finish − planned_start | CALC |
| `baseline_start` | DATE | Y | Locked at SG-6. Copied from planned_start at baseline lock. | SYSTEM |
| `baseline_finish` | DATE | Y | Locked at SG-6. Copied from planned_finish at baseline lock. | SYSTEM |
| `baseline_duration_days` | INTEGER | Y | Auto = baseline_finish − baseline_start | CALC |
| `extended_baseline_finish` | DATE | N | Auto = baseline_finish + sum of approved extensions for this node | CALC |
| `actual_start` | DATE | N | Received from M04. Read-only here. | LINK → M04 |
| `actual_finish` | DATE | N | Received from M04. Read-only here. | LINK → M04 |
| `total_float_days` | INTEGER | N | Auto-calculated by schedule engine | CALC |
| `free_float_days` | INTEGER | N | Auto-calculated by schedule engine | CALC |
| `is_on_critical_path` | BOOLEAN | Y | Auto = total_float_days = 0 | CALC |
| `schedule_variance_days` | INTEGER | N | Auto = planned_finish − extended_baseline_finish (as of report date) | CALC |
| `delay_cause_category` | ENUM | N | `Scope_Addition / Design_Change / Force_Majeure / Client_Delay / Contractor_Delay / Neutral_Event` | LINK → BaselineExtension |
| `loading_profile_id` | UUID | Y | Must exist in LoadingProfile | LINK → LoadingProfile |
| `pv_total` | DECIMAL(15,2) | Y | Auto = BAC for this WBS node (from M02 BOQ) | CALC |
| `is_baseline_locked` | BOOLEAN | Y | True after SG-6 | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

**Note:** Reporting period granularity (Monthly / Weekly / Daily) is controlled at project level via `PVPeriodConfig` — see PVProfile entity.

---

#### Entity: `Baseline`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `baseline_id` | UUID | Y | Auto-generated | SYSTEM |
| `project_id` | UUID | Y | One baseline per project | LINK → M01 Project |
| `baseline_label` | VARCHAR(50) | Y | e.g., `Baseline_v1.0` | SYSTEM |
| `locked_at` | TIMESTAMP | Y | Timestamp of SG-6 approval | SYSTEM |
| `locked_by` | UUID | Y | PMO Director who approved SG-6 | SYSTEM |
| `total_planned_duration_days` | INTEGER | Y | Auto = project end − start at lock | CALC |
| `total_bac` | DECIMAL(15,2) | Y | Auto = sum of all WBS node PV totals at lock | CALC |
| `schedule_snapshot` | JSONB | Y | Full ScheduleEntry state for all WBS nodes at lock | SYSTEM |
| `is_immutable` | BOOLEAN | Y | Always true. System-enforced. No field in Baseline is ever editable post-lock. | SYSTEM |

---

#### Entity: `BaselineExtension`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `extension_id` | UUID | Y | Auto-generated | SYSTEM |
| `project_id` | UUID | Y | Must exist in Project | LINK → M01 Project |
| `wbs_id` | UUID | N | Primary WBS node. Default: must be populated. Null only if `is_project_level_exception = true` (requires PMO Director approval). | LINK → M02 WBSNode |
| `additional_wbs_ids` | JSONB | N | Array of secondary WBS node UUIDs also impacted by this extension. Multi-WBS impact mapping. | INPUT |
| `is_project_level_exception` | BOOLEAN | Y | Default false. True = extension affects entire project, not specific WBS. Requires PMO Director explicit approval + documented justification. | INPUT |
| `project_level_justification` | TEXT | N | Required if `is_project_level_exception = true`. Min 100 characters. | INPUT |
| `extension_days` | INTEGER | Y | > 0 | INPUT |
| `extension_start_date` | DATE | Y | Date from which extension applies | INPUT |
| `cause_category` | ENUM | Y | `Scope_Addition / Design_Change / Force_Majeure / Client_Delay / Contractor_Delay / Neutral_Event` | INPUT (dropdown) |
| `cause_description` | TEXT | Y | Min 50 characters. Detailed explanation mandatory. | INPUT |
| `contract_clause_ref` | VARCHAR(100) | N | Required for `Neutral_Event`. If blank + Neutral_Event → auto-reclassify to `Contractor_Delay`. | INPUT |
| `is_billable_to_client` | BOOLEAN | Y | Auto-set by cause_category. Overridable by PMO Director only with reason. | CALC + OVERRIDE |
| `counts_against_vendor` | BOOLEAN | Y | Auto-set by cause_category. Overridable by PMO Director only with reason. | CALC + OVERRIDE |
| `variation_order_id` | UUID | N | Required if `is_billable_to_client = true`. Links to M05 Variation Order. | LINK → M05 |
| `supporting_evidence_url` | VARCHAR(500) | N | Required for `Neutral_Event` and `Force_Majeure`. Data Lake URL. | INPUT |
| `approved_by` | UUID | Y | PMO Director user ID | LINK → Users |
| `approved_at` | TIMESTAMP | Y | Auto on approval | SYSTEM |
| `status` | ENUM | Y | `Pending / Approved / Rejected` | SYSTEM |
| `rejection_reason` | TEXT | N | Required if status = Rejected | INPUT |
| `created_by` | UUID | Y | Auto | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |

**Cause Category — Auto-Classification Rules:**

| Cause Category | `is_billable_to_client` | `counts_against_vendor` | Contract Clause Required |
|---------------|------------------------|------------------------|--------------------------|
| `Scope_Addition` | true | false | Yes — VO mandatory |
| `Design_Change` | true (if client-initiated) | false | Yes |
| `Force_Majeure` | Case by case — PMO override | false | Yes |
| `Client_Delay` | true | false | Yes |
| `Contractor_Delay` | false | true | No |
| `Neutral_Event` | false (default) | false | Yes — if blank → reclassify to `Contractor_Delay` |

---

#### Entity: `LoadingProfile`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `profile_id` | UUID | Y | Auto-generated | SYSTEM |
| `profile_name` | VARCHAR(100) | Y | e.g., `Civil_Front_Loaded`, `MEP_Bell`, `Commissioning_Back_Loaded` | INPUT / SYSTEM |
| `activity_category` | ENUM | Y | `Civil / MEP / Medical / Interior / PM_Design / Commissioning / Specialist` | INPUT (dropdown) |
| `distribution_type` | ENUM | Y | `Front_Loaded / Bell / Back_Loaded / Linear / Custom` | INPUT (dropdown) |
| `distribution_curve` | JSONB | Y | Array of (period_pct, value_pct) pairs. Must sum to 100%. | INPUT |
| `is_system_default` | BOOLEAN | Y | True = shipped with EPCC. Cannot delete. | SYSTEM |
| `created_by` | UUID | Y | PMO Director only for non-default profiles | SYSTEM |
| `is_active` | BOOLEAN | Y | Soft delete flag | SYSTEM |

**System-Shipped Default Profiles:**

| Category | Profile | Logic |
|----------|---------|-------|
| Civil | Front_Loaded | 60% value in first 40% of duration |
| MEP | Bell | 20% / 60% / 20% across thirds of duration |
| Medical | Bell | Same as MEP |
| Interior | Bell | Same as MEP |
| Commissioning | Back_Loaded | 60% value in last 40% of duration |
| PM_Design | Linear | Even distribution across duration |
| Specialist | Linear | Default — user overrides per activity |

---

#### Entity: `PVProfile`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `pv_profile_id` | UUID | Y | Auto-generated | SYSTEM |
| `wbs_id` | UUID | Y | Must exist in ScheduleEntry | LINK → WBSNode |
| `project_id` | UUID | Y | — | LINK → M01 Project |
| `reporting_period` | DATE | Y | First day of reporting month | INPUT |
| `pv_period` | DECIMAL(15,2) | Y | Planned value for this period only | CALC |
| `pv_cumulative` | DECIMAL(15,2) | Y | Running total PV to end of this period | CALC |
| `pv_pct_cumulative` | DECIMAL(5,4) | Y | pv_cumulative / pv_total | CALC |
| `loading_profile_id` | UUID | Y | Profile used to generate this distribution | LINK → LoadingProfile |
| `is_overridden` | BOOLEAN | Y | True if user manually adjusted this period's PV | INPUT |
| `override_reason` | TEXT | N | Required if is_overridden = true | INPUT |
| `generated_at` | TIMESTAMP | Y | Auto | SYSTEM |

**Reporting Period Granularity:**
PV distribution supports Monthly (default), Weekly, Daily, or Event-driven (milestone-triggered).
Granularity set per project via `reporting_period_type` field in `LookAheadConfig` (reused as project period config).
Finer granularity = more PVProfile records but higher schedule visibility.
Granularity can be changed pre-baseline. Post-baseline change requires PMO Director approval + full PV regeneration.

---

#### Entity: `Milestone`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `milestone_id` | UUID | Y | Auto-generated | SYSTEM |
| `milestone_code` | VARCHAR(20) | Y | Unique within project. e.g., `MS-001` | INPUT |
| `project_id` | UUID | Y | Must exist in Project | LINK → M01 Project |
| `wbs_id` | UUID | N | Linked WBS node — if milestone maps to a WBS Milestone type node | LINK → M02 WBSNode |
| `package_id` | UUID | N | Package this milestone governs | LINK → M02 Package |
| `milestone_name` | VARCHAR(200) | Y | Non-empty | INPUT |
| `milestone_type` | ENUM | Y | `Design / Procurement / Construction / Commissioning / Regulatory / Financial / Handover` | INPUT (dropdown) |
| `phase_id` | ENUM | Y | `DEV / DES / EPC / COM / OAM` | INPUT (dropdown) |
| `planned_date` | DATE | Y | Must be within project dates | INPUT |
| `baseline_date` | DATE | Y | Locked at SG-6. Copied from planned_date. | SYSTEM |
| `extended_baseline_date` | DATE | N | Auto = baseline_date + approved extensions for this milestone | CALC |
| `forecast_date` | DATE | N | Current best estimate. Updated by Planning Engineer. | INPUT |
| `actual_date` | DATE | N | Date milestone was achieved. From M04. | LINK → M04 |
| `status` | ENUM | Y | `Not_Started / In_Progress / Achieved / Delayed / At_Risk` | CALC |
| `delay_days` | INTEGER | N | Auto = actual_date − extended_baseline_date (if achieved) OR forecast_date − extended_baseline_date (if not) | CALC |
| `delay_cause_category` | ENUM | N | Same categories as BaselineExtension | LINK → BaselineExtension |
| `is_gate_linked` | BOOLEAN | Y | True if this milestone is a prerequisite for a stage gate (M08) | INPUT |
| `gate_id` | VARCHAR(10) | N | Required if is_gate_linked = true. e.g., `SG-6` | LINK → M08 |
| `predecessor_milestone_id` | UUID | N | Must exist in Milestone within same project | LINK → Milestone (self) |
| `is_client_visible` | BOOLEAN | Y | True = included in client progress report | INPUT |
| `created_by` | UUID | Y | Auto | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

---

#### Entity: `ResourceAllocation`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `allocation_id` | UUID | Y | Auto-generated | SYSTEM |
| `wbs_id` | UUID | Y | Must exist in WBSNode | LINK → M02 WBSNode |
| `project_id` | UUID | Y | — | LINK → M01 Project |
| `role_name` | VARCHAR(100) | Y | e.g., Structural Engineer, Site Manager, MEP Coordinator | INPUT |
| `resource_id` | UUID | N | Optional. Must exist in ResourceMaster if provided. | LINK → ResourceMaster |
| `allocation_pct` | DECIMAL(5,2) | Y | % of resource time on this activity. Range 0–100. | INPUT |
| `planned_start` | DATE | Y | Must match or fall within ScheduleEntry planned dates | LINK → ScheduleEntry |
| `planned_finish` | DATE | Y | Must match or fall within ScheduleEntry planned dates | LINK → ScheduleEntry |
| `is_confirmed` | BOOLEAN | Y | False = planned role only. True = named person confirmed. | INPUT |
| `created_by` | UUID | Y | Auto | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |

---

#### Entity: `ResourceMaster`
*(Unified repository — internal + contractor + consultant, type-differentiated)*

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `resource_id` | UUID | Y | Auto-generated | SYSTEM |
| `resource_code` | VARCHAR(20) | Y | Unique globally. Auto-generated. e.g., `RES-001` | SYSTEM |
| `full_name` | VARCHAR(150) | Y | Non-empty | INPUT |
| `resource_type` | ENUM | Y | `Internal / Contractor / Consultant` | INPUT (dropdown) |
| `primary_role` | VARCHAR(100) | Y | e.g., Structural Engineer, Site Manager, MEP Coordinator | INPUT |
| `department` | VARCHAR(100) | N | Applicable for Internal type | INPUT |
| `party_id` | UUID | N | Required for Contractor and Consultant types. Links to Party master (M01). | LINK → M01 Party |
| `contract_id` | UUID | N | For Contractor / Consultant — links to the contract governing their engagement (M01) | LINK → M01 Contract |
| `engagement_start` | DATE | N | Required for Contractor / Consultant | INPUT |
| `engagement_end` | DATE | N | Must be > engagement_start if provided | INPUT |
| `max_allocation_pct` | DECIMAL(5,2) | Y | Default 100. Max % this resource can be allocated across all activities simultaneously. | INPUT |
| `email` | VARCHAR(150) | N | Valid format | INPUT |
| `phone` | VARCHAR(15) | N | Valid Indian format | INPUT |
| `governance_level` | ENUM | Y | Auto-set by resource_type: Internal → Standard; Contractor → Contract_Governed; Consultant → Agreement_Governed | CALC |
| `is_active` | BOOLEAN | Y | Soft delete flag | SYSTEM |
| `created_by` | UUID | Y | Auto | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |

**Resource Type Governance Rules:**
| Type | party_id Required | contract_id Required | Engagement Dates | Conflict Detection |
|------|------------------|---------------------|-----------------|-------------------|
| Internal | No | No | Optional | Against max_allocation_pct |
| Contractor | Yes | Yes | Mandatory | Against engagement_end + max_allocation_pct |
| Consultant | Yes | Yes | Mandatory | Against engagement_end + max_allocation_pct |

---

#### Entity: `ProcurementScheduleItem`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `proc_schedule_id` | UUID | Y | Auto-generated | SYSTEM |
| `project_id` | UUID | Y | Must exist in Project | LINK → M01 Project |
| `package_id` | UUID | Y | Must exist in Package (M02) | LINK → M02 Package |
| `boq_id` | UUID | N | Links to specific BOQ item if applicable | LINK → M02 BOQItem |
| `item_description` | VARCHAR(300) | Y | Non-empty | INPUT |
| `item_category` | ENUM | Y | `Civil_Material / MEP_Equipment / Medical_Equipment / Specialist / Consumable` | INPUT (dropdown) |
| `is_long_lead` | BOOLEAN | Y | True = lead time > 90 days. Triggers early procurement flag. | INPUT |
| `lead_time_days` | INTEGER | Y | > 0 | INPUT |
| `latest_order_date` | DATE | Y | Auto = planned_installation_date − lead_time_days | CALC |
| `planned_order_date` | DATE | Y | Must be ≤ latest_order_date | INPUT |
| `planned_delivery_date` | DATE | Y | Must be > planned_order_date | INPUT |
| `planned_installation_date` | DATE | Y | Must be > planned_delivery_date. Must align with WBS planned dates. | INPUT |
| `baseline_order_date` | DATE | Y | Locked at SG-6 | SYSTEM |
| `baseline_delivery_date` | DATE | Y | Locked at SG-6 | SYSTEM |
| `baseline_installation_date` | DATE | Y | Locked at SG-6 | SYSTEM |
| `actual_order_date` | DATE | N | From M06 PO creation date. Read-only here. | LINK → M06 |
| `actual_delivery_date` | DATE | N | From M04 site receipt confirmation. Read-only here. | LINK → M04 |
| `actual_installation_date` | DATE | N | From M04 progress entry. Read-only here. | LINK → M04 |
| `order_delay_days` | INTEGER | N | Auto = actual_order_date − baseline_order_date | CALC |
| `delivery_delay_days` | INTEGER | N | Auto = actual_delivery_date − baseline_delivery_date | CALC |
| `gate_id` | VARCHAR(10) | N | Gate by which procurement must be complete (e.g., SG-5 for long-lead items) | LINK → M08 |
| `status` | ENUM | Y | `Not_Started / Order_Placed / Delivered / Installed / Delayed` | CALC |
| `created_by` | UUID | Y | Auto | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

---


---

#### Entity: `ScheduleImport`
*(Tracks external schedule imports from Primavera P6 / Microsoft Project)*

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `import_id` | UUID | Y | Auto-generated | SYSTEM |
| `project_id` | UUID | Y | Must exist in Project | LINK → M01 Project |
| `import_source` | ENUM | Y | `Primavera_P6 / MSP / EPCC_Native / CSV` | INPUT (dropdown) |
| `source_file_name` | VARCHAR(200) | Y | Original filename | SYSTEM |
| `source_file_url` | VARCHAR(500) | Y | Data Lake URL of uploaded file | SYSTEM |
| `import_mode` | ENUM | Y | `Create_Only / Create_And_Update` | INPUT (modal per session) |
| `import_version` | INTEGER | Y | Auto-increment per project | SYSTEM |
| `imported_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `imported_by` | UUID | Y | User who triggered import | SYSTEM |
| `total_activities` | INTEGER | Y | Count from source file | CALC |
| `matched_activities` | INTEGER | N | Count matched to existing WBS nodes by code | CALC |
| `new_activities` | INTEGER | N | Count of net-new WBS nodes to create | CALC |
| `conflict_count` | INTEGER | N | Count of activities with date conflicts vs existing schedule | CALC |
| `conflict_log` | JSONB | N | Detail of each conflict — activity, field, existing value, import value | CALC |
| `user_resolution` | ENUM | N | `Accept_Import / Keep_Existing / Manual_Per_Conflict` | INPUT |
| `status` | ENUM | Y | `Pending_Review / Committed / Rejected` | SYSTEM |
| `commit_notes` | TEXT | N | Free text — what was accepted / overridden | INPUT |

**Import Conflict Resolution Rules:**
```
On import, EPCC compares source file activities to existing WBSNodes by wbs_code.

If match found AND dates differ:
  → Show conflict in conflict_log
  → User must choose: Accept_Import (overwrite) / Keep_Existing / Manual_Per_Conflict
  → No silent overwrites permitted

If baseline is locked:
  → Any date change from import creates a BaselineExtension request (not a direct overwrite)
  → User must classify cause_category before commit

If no match found:
  → New WBSNode created (subject to post-baseline rules if applicable)

All imports are all-or-nothing per resolution decision.
Partial commits not permitted.
```

#### Entity: `WeatherWindowConfig`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `config_id` | UUID | Y | Auto-generated | SYSTEM |
| `project_id` | UUID | Y | Must exist in Project | LINK → M01 Project |
| `window_name` | VARCHAR(100) | Y | e.g., `Monsoon 2026`, `Summer Shutdown 2027` | INPUT |
| `window_type` | ENUM | Y | `Monsoon / Extreme_Heat / Holiday_Shutdown / Regulatory_Closure` | INPUT (dropdown) |
| `start_date` | DATE | Y | — | INPUT |
| `end_date` | DATE | Y | Must be > start_date | INPUT |
| `productivity_factor` | DECIMAL(4,3) | Y | 0.0 = full stop; 1.0 = no impact; 0.5 = 50% productivity | INPUT |
| `affected_categories` | JSONB | Y | Array of activity categories affected. e.g., `["Civil", "External"]` | INPUT |
| `is_factored_into_schedule` | BOOLEAN | Y | True = schedule engine accounts for this window in float and PV calculations | INPUT |
| `created_by` | UUID | Y | Auto | SYSTEM |

---

#### Entity: `LookAheadConfig`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `config_id` | UUID | Y | Auto-generated | SYSTEM |
| `project_id` | UUID | Y | One config per project | LINK → M01 Project |
| `window_weeks` | INTEGER | Y | Default 4. Range 2–12. | INPUT |
| `reporting_period_type` | ENUM | Y | `Monthly / Weekly / Daily / Event_Driven`. Default Monthly. | INPUT (dropdown) |
| `updated_by` | UUID | Y | Planning Engineer or Project Director | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

---

### 3c. Decision Queue Integration

M03 generates five decision-triggering conditions:

| Trigger Condition | Decision Type | Owner | SLA | Escalation |
|-----------------|--------------|-------|-----|-----------|
| Milestone delay > 7 days on gate-linked milestone | Schedule Recovery Required | Project Director | 24 hrs | 36 hrs → PMO Director + governance breach |
| Long-lead item order date missed | Procurement Escalation | Procurement Officer | 12 hrs | 24 hrs → Project Director |
| `Neutral_Event` extension requested | Neutral Event Classification Review | PMO Director | 24 hrs | 36 hrs → Portfolio Manager |
| Any extension where `Neutral_Event` has no contract clause | Auto-reclassification to `Contractor_Delay` | System (auto) | Immediate | No SLA — auto-executed |
| Critical path activity delayed > 5 days | Critical Path Alert | Project Director + PMO Director | 12 hrs | 24 hrs → Portfolio Manager |

---

## BLOCK 4 — Data Population Rules

### 4a. Role Permission Matrix

| Action | PMO Director | Project Director | Planning Engineer | Procurement Officer | QS Manager | Finance Lead | Site Manager | Read-Only |
|--------|-------------|-----------------|-------------------|--------------------|-----------|-----------|-----------| ------|
| Create / edit schedule entries (pre-baseline) | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Edit schedule entries (post-baseline) | ✅ (with decision) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Lock baseline (SG-6) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Create baseline extension | ✅ | ✅ (raise request) | ✅ (raise request) | ❌ | ❌ | ❌ | ❌ | ❌ |
| Approve baseline extension | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Classify `Neutral_Event` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Override billable / vendor flags | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Create / edit milestones | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Update milestone forecast date | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Create / edit procurement schedule | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Configure loading profiles | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Override PV period (manual adjustment) | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Allocate resources (role) | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Assign named resource | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Configure weather windows | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Configure look-ahead window | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| View all schedule data | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (own pkg) | ✅ |

---

### 4b. Entry Method

| Entity / Field Group | Entry Method |
|---------------------|-------------|
| Schedule dates per WBS | Inline date entry within WBS tree view (M02 tree, dates added in M03 column) |
| Baseline lock | Single action button — PMO Director only — triggered by SG-6 gate approval in M08 |
| Baseline extension | Form — cause category dropdown + description + contract clause + evidence upload |
| Neutral_Event evidence | File upload to Data Lake — URL auto-populated in extension record |
| Milestones | Form — linked to WBS node or standalone. Gate link selected from dropdown. |
| Milestone forecast date | Inline update — Planning Engineer updates weekly |
| Loading profile | Dropdown per WBS node — defaults auto-applied by category |
| PV override | Inline per period — reason mandatory |
| Resource allocation | Role: dropdown from controlled list. Named resource: search from ResourceMaster. |
| Procurement schedule | Form per item — long-lead flag triggers early gate assignment |
| Weather windows | Date range form — productivity factor slider (0.0–1.0) |
| Look-ahead window | Single integer input (weeks) per project |

---

### 4c. Mandatory vs Optional

| Field / Group | Mandatory | System Behaviour if Empty |
|--------------|-----------|--------------------------|
| Planned start + finish per WBS node | Yes — before baseline | Blocks baseline lock |
| Loading profile per WBS node | Yes — defaults auto-applied | System applies category default. User may override. |
| Milestone planned date | Yes | Blocks milestone save |
| Milestone type + phase | Yes | Blocks milestone save |
| Gate-linked milestones (SG-4 to SG-11) | Yes — must exist before gate can be activated | M08 blocks gate if no linked milestone found |
| Resource role per WBS node | Yes — for Level 3 tasks | Warning if missing. Does not block save. |
| Named resource | No | Allocation marked as unconfirmed |
| Procurement item — lead time + order date | Yes — for long-lead items | Blocks long-lead flag if empty |
| Baseline extension cause description | Yes (min 50 chars) | Blocks extension save |
| Contract clause for Neutral_Event | Yes — or auto-reclassify | System reclassifies to Contractor_Delay if blank |
| Weather window productivity factor | Yes | Blocks weather config save |
| PV override reason | Yes — if override = true | Blocks override save |

---

## BLOCK 5 — Filters & Views

### 5a. Standard Filters

| Filter | Type | Options |
|--------|------|---------|
| Project | Single-select | All projects user has access to |
| Phase | Multi-select | DEV / DES / EPC / COM / OAM |
| Package | Multi-select | All packages in selected project |
| Activity Category | Multi-select | Civil / MEP / Medical / Interior / PM_Design / Commissioning |
| Milestone Type | Multi-select | Design / Procurement / Construction / Commissioning / Regulatory / Financial / Handover |
| Baseline Status | Single-select | Pre-baseline / Baseline locked |
| Date Range | Date range picker | Filter by planned start within window |

### 5b. Module-Specific Filters

| Filter | Type | Purpose |
|--------|------|---------|
| Critical Path Only | Toggle | Show only is_on_critical_path = true nodes |
| Delayed Activities | Toggle | Show activities where schedule_variance_days > 0 |
| Look-Ahead Window | Auto-applied | Shows activities with planned_start within next N weeks (from LookAheadConfig) |
| Long-Lead Items | Toggle | Show procurement items with is_long_lead = true |
| Overdue Procurement | Toggle | latest_order_date < today AND actual_order_date is null |
| Extension Cause | Multi-select | Filter baseline extensions by cause_category |
| Unconfirmed Resources | Toggle | ResourceAllocation where is_confirmed = false |
| Milestone Status | Multi-select | Not_Started / In_Progress / Achieved / Delayed / At_Risk |

### 5c. Views

| View | Format | Default For | Who Sees |
|------|--------|------------|---------|
| Gantt Chart | Horizontal bar chart — WBS hierarchy, baseline vs planned vs actual bars | Planning Engineer, Project Director | All with access |
| Schedule Table | Sortable table — all WBS nodes with dates, float, variance | Planning Engineer | All |
| Milestone Tracker | Table — all milestones, status badges, delay days, gate links | PMO Director, Project Director | All |
| Look-Ahead View | Filtered Gantt — next N weeks only | Site Manager, Planning Engineer | All |
| S-Curve View | Chart — cumulative PV over time, with EV and AC overlay (from M07) | PMO Director, Finance Lead | All |
| Procurement Schedule | Table — all items, order/delivery/install dates, delay flags | Procurement Officer, Planning Engineer | All |
| Resource Loading | Bar chart — utilisation % per resource per period | Project Director, Planning Engineer | PMO, Project Director, Planning |
| Extension Log | Table — all baseline extensions, cause, days, billable flag, approval | PMO Director, Finance Lead | PMO, Finance |
| Critical Path View | Highlighted Gantt — critical path nodes only | Project Director, Planning Engineer | All |

---

## BLOCK 6 — Business Rules (Enhanced)

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---------|---------|-------|--------|------------|
| BR-03-001 | Schedule entry created | `planned_finish` must be > `planned_start` | Block save | 🔴 Real-time |
| BR-03-002 | Schedule entry created | Dates must fall within project `planned_start_date` and `planned_end_date` (M01) | Block save | 🔴 Real-time |
| BR-03-003 | Baseline lock triggered | All WBS Level 3 task nodes must have planned_start and planned_finish populated | Block baseline lock if any Level 3 task has null dates | 🔴 Real-time |
| BR-03-004 | Baseline lock triggered | All gate-linked milestones (SG-4 to SG-11) must exist and have planned_dates | Block baseline lock if any gate milestone missing | 🔴 Real-time |
| BR-03-005 | Baseline lock triggered | `baseline_start`, `baseline_finish` copied from `planned_start`, `planned_finish` for all nodes | Immutable copy created. `is_baseline_locked` = true. | 🔴 Real-time |
| BR-03-006 | Baseline lock triggered | `Baseline` snapshot (JSONB) created with full schedule state | Baseline record created and sealed | 🔴 Real-time |
| BR-03-007 | Schedule edit post-baseline | Any direct edit to `planned_start` or `planned_finish` after lock | Block edit. Require BaselineExtension instead. | 🔴 Real-time |
| BR-03-008 | BaselineExtension created | `cause_category` = `Neutral_Event` AND `contract_clause_ref` is blank | Auto-reclassify to `Contractor_Delay`. Log reclassification in audit. Notify submitter. | 🔴 Real-time |
| BR-03-009 | BaselineExtension created | `cause_category` = `Neutral_Event` AND `supporting_evidence_url` is blank | Block extension save. Evidence mandatory for Neutral_Event. | 🔴 Real-time |
| BR-03-010 | BaselineExtension created | `is_billable_to_client` = true AND `variation_order_id` is null | Block approval. VO must exist in M05 before billable extension can be approved. | 🔴 Real-time |
| BR-03-011 | BaselineExtension approved | `extended_baseline_finish` recalculated for affected WBS nodes and milestones | Cascade update to all downstream schedule_variance_days | 🔴 Real-time |
| BR-03-012 | LoadingProfile assigned | PVProfile records auto-generated for all reporting periods of WBS node | Generate time-phased PV distribution. Notify M07. | 🔴 Real-time |
| BR-03-013 | PVProfile override | `is_overridden` = true but `override_reason` is blank | Block save | 🔴 Real-time |
| BR-03-014 | Report date updated (from M01) | All `schedule_variance_days` recalculated as of new report date | Full PV recalculation cascade triggered | 🔴 Real-time |
| BR-03-015 | Milestone status update | `forecast_date` > `extended_baseline_date` by > 7 days AND `is_gate_linked` = true | Generate Decision record (Schedule Recovery Required). Notify Project Director. | 🔴 Real-time |
| BR-03-016 | Procurement check | `latest_order_date` < today AND `actual_order_date` is null | Generate Decision record (Procurement Escalation). Notify Procurement Officer. | 🟡 2-4hr |
| BR-03-017 | Long-lead item flagged | `is_long_lead` = true AND `gate_id` is null | Warning — long-lead item without gate assignment. Notify Planning Engineer. | 🟡 2-4hr |
| BR-03-018 | Critical path activity delayed | `is_on_critical_path` = true AND `schedule_variance_days` > 5 | Generate Decision record (Critical Path Alert). Notify Project Director + PMO Director. | 🔴 Real-time |
| BR-03-019 | Resource conflict | Same named resource allocated > 100% across all activities in same period | Flag conflict. Notify Planning Engineer. Block confirmation of over-allocated resource. | 🟡 2-4hr |
| BR-03-020 | Weather window active | `WeatherWindowConfig` period overlaps with WBS planned dates AND `is_factored_into_schedule` = true | Adjust effective float calculation. Reduce productivity in PV distribution for affected categories. | 🟢 24hr |
| BR-03-021 | Daily schedule check | Any milestone with status = `Not_Started` or `In_Progress` AND `extended_baseline_date` < today | Auto-update status to `Delayed`. Notify Planning Engineer. | 🟢 24hr |
| BR-03-022 | Procurement order placed (from M06) | `actual_order_date` populated from M06 PO creation | `order_delay_days` calculated. Status → `Order_Placed`. | 🔴 Real-time |

| BR-03-023 | Schedule import initiated | `ScheduleImport` record created. Import mode modal presented — no default. | User must select Create_Only or Create_And_Update before file is processed. | 🔴 Real-time |
| BR-03-024 | Schedule import — conflict detected | Existing WBS date differs from import value | Show conflict in conflict_log. Block commit until user resolves all conflicts. | 🔴 Real-time |
| BR-03-025 | Schedule import — post-baseline | Any date change from import after baseline is locked | Block direct overwrite. Route to BaselineExtension workflow. User must classify cause_category. | 🔴 Real-time |
| BR-03-026 | Project-level extension requested | `is_project_level_exception = true` AND `project_level_justification` < 100 chars | Block save. Justification mandatory and must meet minimum length. | 🔴 Real-time |
| BR-03-027 | Project-level extension requested | `is_project_level_exception = true` | Requires PMO Director approval. Block until approved. Generate Decision record. | 🔴 Real-time |
| BR-03-028 | Reporting period granularity changed post-baseline | `reporting_period_type` changed after baseline lock | Requires PMO Director approval. Full PV regeneration triggered on approval. Log old + new granularity. | 🔴 Real-time |
| BR-03-029 | Contractor / Consultant resource allocated | `resource_type` = Contractor or Consultant AND `engagement_end` < activity `planned_finish` | Warning — resource engagement ends before activity finishes. Block confirmation. | 🔴 Real-time |
| BR-03-030 | Resource over-allocated | Named resource total allocation_pct > `max_allocation_pct` in any period | Flag conflict. Block confirmation of allocation. Generate Decision record. Notify Planning Engineer. | 🟡 2-4hr |
### SLA Escalation Table

Applies to: BR-03-015 (Schedule Recovery), BR-03-016 (Procurement Escalation), BR-03-018 (Critical Path Alert)

| Time Since Decision Created | Status | System Action |
|----------------------------|--------|--------------|
| 0–12 hrs | Normal | No action |
| 12–24 hrs | Attention | Reminder to decision owner |
| 24–36 hrs | Risk | Escalate to PMO Director |
| 36+ hrs | Critical | Auto-escalate to Portfolio Manager + governance breach logged |

---

## BLOCK 7 — Integration Points

| Direction | Module | Data Exchanged | Trigger | Speed Tier |
|-----------|--------|---------------|---------|------------|
| RECEIVES FROM | M01 Project Registry | `project_id`, `planned_start_date`, `planned_end_date`, `report_date`, `current_phase`, `monsoon_delay_months` | On project activation + report date change | 🔴 Real-time |
| RECEIVES FROM | M02 Structure & WBS | `wbs_id`, `wbs_code`, `activity_type`, `phase_id`, `package_id`, `predecessor_wbs_id`, `is_baseline_locked` signal | On WBS node create/edit + SG-6 lock | 🔴 Real-time |
| RECEIVES FROM | M04 Execution | `actual_start`, `actual_finish` per WBS node; `actual_delivery_date` populated via `MaterialReceipt.received_date` (linked by `material_receipt_id` FK) when M06 confirms GRN | On progress entry (🟢 24hr) + GRN confirmation from M06 (🔴 Real-time) | 🟢 24hr |
| RECEIVES FROM | M09 Compliance | Compliance grant dates → auto-populate `actual_date` on linked milestones. Compliance items auto-create milestones if not yet linked. Schedule_impact signal when grant_date delayed. | On compliance grant date entry | 🔴 Real-time |
| RECEIVES FROM | M05 Risk & Change | `variation_order_id` for billable extensions; EOT VO approval auto-creates `BaselineExtension` record (cause_category=Client_Delay, extension_days=approved_time_days) | On VO creation + EOT VO approval | 🔴 Real-time |
| SENDS TO | M05 Risk & Change | `contractor_delay_days` per package (sum of delay days attributable to Contractor_Delay cause) | On schedule update — feeds LD auto-calculation | 🟡 2-4hr |
| RECEIVES FROM | M06 Financial | `actual_order_date` from PO creation | On PO raised in M06 | 🔴 Real-time |
| RECEIVES FROM | M08 Gate Control | SG-6 approval signal → triggers baseline lock | On SG-6 gate approval | 🔴 Real-time |
| SENDS TO | M07 EVM Engine | `pv_period`, `pv_cumulative` per WBS node per reporting period | On PVProfile generation + report date change | 🔴 Real-time |
| SENDS TO | M07 EVM Engine | `extended_baseline_finish` per WBS node | On baseline extension approval | 🔴 Real-time |
| SENDS TO | M06 Financial | `planned_delivery_date`, `planned_installation_date` per procurement item | On procurement schedule save | 🟢 24hr |
| SENDS TO | M08 Gate Control | Milestone status per gate-linked milestone | On milestone update | 🔴 Real-time |
| SENDS TO | M08 Gate Control | Procurement gate readiness (long-lead items vs gate date) | On procurement status change | 🟡 2-4hr |
| SENDS TO | M05 Risk & Change | Schedule variance data — delay days per WBS node | On schedule update | 🟡 2-4hr |
| SENDS TO | M10 EPCC Command | Overall schedule health, critical path status, milestone summary, S-curve data | On any schedule update | 🟡 2-4hr |

---

## BLOCK 8 — Governance & Audit

| Action | Logged | Field-Level Detail | Visible To | Retention |
|--------|--------|--------------------|-----------|-----------|
| Schedule entry created | Yes | All fields | PMO Director, Project Director | Project lifetime |
| Schedule dates edited (pre-baseline) | Yes | Old + new dates, user, timestamp | PMO Director | Project lifetime |
| Baseline locked | Yes | Timestamp, gate reference, approver | All | Permanent |
| BaselineExtension submitted | Yes | All fields, submitter | PMO Director, Project Director | Permanent |
| BaselineExtension approved / rejected | Yes | Decision, approver, reason | All | Permanent |
| Neutral_Event reclassified to Contractor_Delay | Yes | Original submission, auto-reclassification reason | PMO Director, Finance Lead | Permanent |
| Billable flag overridden | Yes | Old value, new value, reason, PMO Director | PMO Director, Finance Lead | Permanent |
| Vendor performance flag overridden | Yes | Old value, new value, reason, PMO Director | PMO Director | Permanent |
| PV override applied | Yes | Period, old PV, new PV, reason, user | PMO Director | Project lifetime |
| Milestone status changed | Yes | Old + new status, user, timestamp | All | Project lifetime |
| Milestone forecast date updated | Yes | Old + new date, user, timestamp | PMO Director, Project Director | Project lifetime |
| Resource allocated | Yes | WBS node, role, resource, allocation % | PMO Director, Project Director | Project lifetime |
| Procurement item created / edited | Yes | All fields | PMO Director, Procurement Officer | Project lifetime |
| Critical path alert generated | Yes | WBS node, delay days, decision ID | All | Permanent |
| Soft delete | Yes | Deleted by, timestamp, reason | PMO Director + System Admin | Permanent |

---

## BLOCK 9 — Explicit Exclusions

```
This module does NOT:
────────────────────────────────────────────────────────────────────────
[ ] Store WBS structure, hierarchy, or BOQ items               → M02
[ ] Calculate or store actual cost (AC)                        → M06
[ ] Calculate CPI, SPI, EAC, VAC, TCPI                        → M07
[ ] Manage stage gate approvals or STOP/GO logic               → M08
[ ] Store variation orders or formal claims                    → M05
[ ] Track site daily progress or QA inspections                → M04
[ ] Store vendor PO values or payment terms                    → M06
[ ] Track regulatory permits or NABH compliance                → M09
[ ] Store contractor performance scores                        → M04
[ ] Manage sub-contract financial terms                        → M06
[ ] Store project documents or drawings                        → Data Lake
[ ] Perform schedule optimization or resource levelling        → Future module (scheduler engine)
```

---

## BLOCK 10 — Open Questions

**All questions resolved. Zero open questions.**

| # | Question | Resolution |
|---|----------|-----------|
| 1 | CPM inbuilt or external import? | Both. EPCC has inbuilt CPM engine (calculates float, critical path, schedule variance). Also supports import from Primavera P6 and MSP via `ScheduleImport` entity. Import conflicts are user-resolved — no silent overwrites. Post-baseline imports trigger BaselineExtension workflow. |
| 2 | Reporting period granularity? | User-configurable per project: Monthly (default), Weekly, Daily, or Event-driven (milestone-triggered). Granularity change post-baseline requires PMO Director approval + full PV regeneration. |
| 3 | Project-level baseline extensions? | WBS-attributed by default (`wbs_id` mandatory). Project-level exceptions allowed (`is_project_level_exception = true`) but require PMO Director explicit approval + 100-character justification. Multi-WBS impact mapped via `additional_wbs_ids` JSONB array. |
| 4 | ResourceMaster scope? | Unified type-classified repository: Internal / Contractor / Consultant. Contractor and Consultant require `party_id` (M01 Party) and `contract_id` (M01 Contract). Differentiated governance: Internal = Standard; Contractor/Consultant = Contract_Governed or Agreement_Governed. Engagement dates mandatory for external types. |

---

## APPENDIX — KDMC Reference Mapping

| KDMC Excel | M03 Entity | Notes |
|-----------|-----------|-------|
| 03_Milestones | Milestone | Key dates, delay tracking |
| 03_Phase_Gate_Tracker | Milestone (gate-linked) + M08 | Gate entry/exit criteria feed M08 |
| 03_Resource_Allocation | ResourceAllocation | Role-level. Named resources optional. |
| 03_Procurement_Control | ProcurementScheduleItem | Long-lead: LINAC (18–24m), MRI (14–16m) at SG-5 |
| 02_WBS date columns | ScheduleEntry | 438 WBS nodes — all need schedule entries |
| 01_ASSUMPTIONS monsoon_delay | WeatherWindowConfig | Default 2 months monsoon window |
| 01_MODEL_INPUTS report_date | Cascade trigger | Report date drives full PV recalculation |

**KDMC Critical Procurement Items (Long-Lead — SG-5):**
```
LINAC           18–24 months    latest_order_date = SG-5 date
MRI             14–16 months    latest_order_date = SG-5 date
CT Scanner      10–12 months    latest_order_date = SG-5 date
Cath Lab        12–14 months    latest_order_date = SG-5 date
OT Equipment     8–10 months    latest_order_date = SG-6 date
MGPS             6–8 months     latest_order_date = SG-6 date
```

---

*Spec complete when Block 10 shows zero open questions.*
*Status: Draft. Four open questions require resolution before lock.*
