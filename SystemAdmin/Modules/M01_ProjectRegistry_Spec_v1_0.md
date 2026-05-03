# M01 — Project Registry
## Spec v1.0
**Status:** Locked
**Locked:** Yes
**Author:** PMO Director / System Architect
**Created:** 2026-05-03 | **Last Updated:** 2026-05-03
**Last Audited:** v1.0 on 2026-05-03
**Reference Standards:** EPCC_NamingConvention_v1_0.md, X8_GlossaryENUMs_v0_2.md, M34_SystemAdminRBAC_Spec_v1_0.md
**Layer:** L1 Command
**Phase:** 1 — Foundational
**Build Priority:** 🔴 Critical (precedes all execution modules)
**Folder:** /02_L1_Command/
**Re-Issue Of:** Legacy M01_Project_Registry_v2.1.md (consolidated standalone)

---

## CHANGE LOG

| Version | Date | Change Summary |
|---|---|---|
| v1.0 | 2026-05-03 | Initial standalone spec. Re-issued from legacy v2.1 with audit fixes (F-001, F-003, F-004, F-005, F-007, F-013, F-014). All 10 OQ-1 decisions locked. Phase enum aligned with X8 v0.2. Sector split into SectorTopLevel enum + sub-type CodeMaster. DeliveryModel "Hybrid" dropped. ProjectStatus "Draft" added. |

---

## BLOCK 1 — IDENTITY

```
Module ID                : M01
Module Name              : Project Registry
Layer                    : L1 Command
Decision It Enables      : Is this project authorised to exist in the portfolio,
                           and are its foundational parameters — identity,
                           contract, parties, dates, value, thresholds — correctly
                           established as the master reference for all downstream
                           modules?

Primary User             : PMO_DIRECTOR
Secondary Users          : PORTFOLIO_MANAGER, PROJECT_DIRECTOR, FINANCE_LEAD
Module Icon              : Briefcase (Lucide)
Navigation Section       : L1 Command (between M34 SystemAdmin and M23 BG/Insurance)
```

---

## BLOCK 2 — SCOPE BOUNDARY

### INCLUDES

| Capability | Description |
|---|---|
| Portfolio / Program / Project hierarchy | 3-level mandatory hierarchy. Multi-portfolio supported. |
| Project identity | code, name, sector (top-level + sub-type), delivery model, geography (pincode), dates, phase, status |
| Multiple contracts per project | Primary / Secondary / Specialist roles. Soft cap 3 Primary. |
| Contract financial terms | value (basic + GST), retention, advance, LD, DLP, escalation, risk_buffer_pct |
| Party master (global shared) | Single source-of-truth for external organisations (clients, contractors, consultants, vendors) |
| Project-Party assignment | Many-to-many via `ProjectPartyAssignment` |
| Party exclusivity tracking | Detect and govern same-role overlap across active projects |
| Pincode → geography resolution | Embedded `PincodeMaster` (static snapshot, annual refresh by SYSTEM_ADMIN) |
| Scenario configuration | Base / Best / Worst — escalation %, delay months, monsoon, payment delays |
| KPI threshold configuration | Green / Amber / Red bands per KPI per project |
| Project lifecycle phase tracking | Per X8 §3.9 Phase enum (10 values aligned with stage gates) |
| Report date | Authoritative "current as-of" date — drives full recalculation cascade |
| Project activation governance | BR-01-010: at least one Primary contract, both Client and EPC Contractor parties assigned |
| Soft delete with cascade guard | Block if child records exist (per OQ-1.10) |

### EXCLUDES

| Excluded | Where It Lives |
|---|---|
| WBS, packages, BOQ items | M02 Structure & WBS |
| Schedule, milestones, baselines, S-curves | M03 Planning & Milestones |
| Site progress, NCRs, HSE incidents, DLP defects | M04 Execution Capture |
| Risk register, variation orders, EOTs | M05 Risk & Change Control |
| Actual cost ledger, billing, sub-contracts, retention release | M06 Financial Control |
| EVM (CPI/SPI/EAC) calculations | M07 EVM Engine |
| Stage gate criteria + decisions | M08 Gate Control |
| Compliance (NABH, statutory, AERB) | M09 Compliance Tracker |
| Portfolio dashboard aggregation | M10 EPCC Command |
| Action items, decision queue resolution | M11 Action Register |
| Tendering / award workflow | M29 Tendering & Award |
| Vendor PQ, scorecards, blacklist | M30 Vendor Master & PQ |
| BG / insurance certificate tracking | M23 (Phase 2 sub-module) |
| User accounts, roles, permissions | M34 System Administration & RBAC |
| Document storage | MinIO + per-module references |

---

## BLOCK 3 — DATA ARCHITECTURE

### 3a. Entity Overview

| Entity | Description | Cardinality | Schema Owner |
|---|---|---|---|
| `Portfolio` | Top-level grouping of programs and projects | Many per tenant | M01 |
| `Program` | Group of related projects under a strategic objective | Many per portfolio | M01 |
| `Project` | A single capital project | Many per program | M01 |
| `Contract` | Commercial instrument governing the project | Many per project | M01 |
| `Party` | Global master: external organisations across all projects | Many per tenant | M01 |
| `ProjectPartyAssignment` | Many-to-many: party × project × role | Many per project | M01 |
| `ProjectPhaseHistory` | Phase transition log per project | Many per project | M01 |
| `ProjectStatusHistory` | Status transition log per project | Many per project | M01 |
| `ScenarioConfig` | Per-project scenario parameters | 1 active per project | M01 |
| `KPIThreshold` | Per-project KPI bands per KPI | 5 per project (one per KPI) | M01 |
| `PincodeMaster` | Pincode → state/city/district lookup | System seed | M01 |

---

### 3b. Entity: `Portfolio`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `portfolio_id` | UUID | Y | Auto-generated, immutable | SYSTEM |
| `tenant_id` | UUID | Y | FK → M34.Tenant | LINK → M34.Tenant |
| `portfolio_code` | VARCHAR(20) | Y | Unique within tenant. Uppercase, 3–20 chars. | INPUT |
| `portfolio_name` | VARCHAR(200) | Y | Min 3 chars | INPUT |
| `description` | TEXT | N | Max 2000 chars | INPUT |
| `owner_user_id` | UUID | Y | FK → M34.User. Must hold PMO_DIRECTOR or PORTFOLIO_MANAGER role. | LINK → M34.User |
| `created_by` | UUID | Y | FK → M34.User | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_by` | UUID | Y | Auto | LINK → M34.User |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true (soft delete per X8 §6) | SYSTEM |

---

### 3c. Entity: `Program`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `program_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | FK → M34.Tenant | LINK → M34.Tenant |
| `portfolio_id` | UUID | Y | FK → Portfolio. Must be active. | LINK → Portfolio |
| `program_code` | VARCHAR(20) | Y | Unique within portfolio | INPUT |
| `program_name` | VARCHAR(200) | Y | Min 3 chars | INPUT |
| `strategic_objective` | TEXT | N | Max 2000 chars | INPUT |
| `created_by` | UUID | Y | — | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_by` | UUID | Y | Auto | LINK → M34.User |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |

**Composite uniqueness:** (`tenant_id`, `portfolio_id`, `program_code`)

---

### 3d. Entity: `Project`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `project_id` | UUID | Y | Auto-generated, immutable, never user-facing | SYSTEM |
| `tenant_id` | UUID | Y | FK → M34.Tenant | LINK → M34.Tenant |
| `project_code` | VARCHAR(20) | Y | Unique within tenant. Format: `[CLIENT]-[SEQ]-[TYPE]` (e.g., `KDMC-001-DBOT`). Uppercase. | INPUT |
| `project_name` | VARCHAR(200) | Y | Unique within program (case-insensitive). Min 3 chars. | INPUT |
| `portfolio_id` | UUID | Y | FK → Portfolio | LINK → Portfolio |
| `program_id` | UUID | Y | FK → Program (must be under same portfolio) | LINK → Program |
| `sector_top_level` | ENUM | Y | Per X8 §3.16a `SectorTopLevel`: `Healthcare / Infrastructure / Residential / Commercial / Industrial` | INPUT (dropdown) |
| `sector_sub_type_code` | VARCHAR(50) | Y | FK → CodeMaster where category=`SectorSubType` and parent matches sector_top_level. e.g., `Hospital_DBOT`, `Hospital_PPP`, `Highway`. | LINK → M34.CodeMaster |
| `delivery_model` | ENUM | Y | Per X8 §3.18 `DeliveryModel`: `EPC / EPCM / DBOT / PPP / Turnkey / Construction_Management`. **No "Hybrid".** | INPUT (dropdown) |
| `delivery_model_notes` | TEXT | N | Max 500 chars. Use to capture hybrid arrangements. | INPUT |
| `pincode` | CHAR(6) | Y | Numeric. Must exist in PincodeMaster. | INPUT |
| `state` | VARCHAR(50) | Y | Auto-resolved from PincodeMaster. Locked from edit. | CALC |
| `city` | VARCHAR(100) | Y | Auto-resolved | CALC |
| `district` | VARCHAR(100) | Y | Auto-resolved | CALC |
| `planned_start_date` | DATE | Y | Cannot precede today by > 365 days | INPUT |
| `planned_end_date` | DATE | Y | Must be > planned_start_date | INPUT |
| `planned_duration_days` | INTEGER | Y | Auto = planned_end_date − planned_start_date | CALC |
| `report_date` | DATE | Y | Must be ≥ planned_start_date and ≤ planned_end_date | INPUT |
| `project_month` | INTEGER | Y | Auto = months elapsed from planned_start_date to report_date | CALC |
| `pct_time_elapsed` | DECIMAL(5,4) | Y | Auto = elapsed_days / planned_duration_days. Range 0.0000–1.0000. | CALC |
| `current_phase` | ENUM | Y | Per X8 §3.9 `Phase`: `Pre_Investment / Design / Pre_Construction / Construction / Equipment / Commissioning / Empanelment / Handover / DLP / Closed` | INPUT (dropdown) |
| `project_status` | ENUM | Y | Per X8 §3.8 `ProjectStatus`: `Draft / Active / On_Hold / Closed / Cancelled` | SYSTEM (state machine) |
| `rag_status` | ENUM | Y | Per X8 §3.2 `RAGStatus`. Auto-computed from KPI thresholds after EVM run. | CALC |
| `accounting_system` | VARCHAR(50) | N | Free-text stub: `Tally / Zoho / SAP / Other / None`. Agnostic — no integration in v1.0. | INPUT |
| `report_date_staleness_threshold_days` | INTEGER | Y | Auto-set from M03 reporting_period_type (Monthly→35, Weekly→10, Daily→2). PMO_DIRECTOR override allowed. | CALC + override |
| `created_by` | UUID | Y | — | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_by` | UUID | Y | Auto | LINK → M34.User |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true. Soft delete blocked if child records exist (BR-01-019). | SYSTEM |

**State machine (project_status):**
```
Draft → Active     (on BR-01-010 pass — at least 1 Primary contract + Client + EPC Contractor parties)
Active → On_Hold   (PMO_DIRECTOR action; preserves all data; downstream modules read-only)
On_Hold → Active   (PMO_DIRECTOR action)
Active → Closed    (normal completion; downstream modules read-only)
Active → Cancelled (abnormal termination; downstream modules read-only)
On_Hold → Closed/Cancelled
Draft → Cancelled  (project never activated)
```

**Forbidden transitions:** Closed → Active, Cancelled → Active, Closed → Cancelled (and vice versa). Any reactivation requires PMO_DIRECTOR + reason ≥ 100 chars + new ProjectStatusHistory entry.

---

### 3e. Entity: `Contract`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `contract_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `contract_code` | VARCHAR(30) | Y | Unique within project. Format: `[PROJECT_CODE]-[ROLE]-[SEQ]` | INPUT |
| `project_id` | UUID | Y | FK → Project | LINK → Project |
| `contract_role` | ENUM | Y | `Primary / Secondary / Specialist` | INPUT (dropdown) |
| `contract_type` | ENUM | Y | `DBOT / EPC / EPCM / Lump_Sum / Item_Rate / PPP / Turnkey / Construction_Management` | INPUT (dropdown) |
| `contract_value_basic` | DECIMAL(15,2) | Y | > 0. INR. | INPUT |
| `gst_rate` | DECIMAL(5,4) | Y | Default 0.18. Range 0.00–0.28. | INPUT |
| `contract_value_incl_gst` | DECIMAL(15,2) | Y | Auto = contract_value_basic × (1 + gst_rate) | CALC |
| `total_boq_cost` | DECIMAL(15,2) | N | Optional at contract creation. Reconciled with M02 BAC after WBS lock. Warning flag if > contract_value_basic. | INPUT |
| `signing_date` | DATE | Y | ≤ today | INPUT |
| `effective_date` | DATE | Y | ≥ signing_date | INPUT |
| `contract_term_months` | INTEGER | Y | > 0 | INPUT |
| `mobilisation_advance_pct` | DECIMAL(5,4) | Y | Default 0.10. Range 0–0.20. | INPUT |
| `material_advance_pct` | DECIMAL(5,4) | Y | Default 0.05. Range 0–0.10. | INPUT |
| `retention_pct` | DECIMAL(5,4) | Y | Default 0.05. Range 0–0.10. | INPUT |
| `retention_release_after_dlp` | BOOLEAN | Y | Default true | INPUT |
| `dlp_term_days` | INTEGER | Y | Default 365. Range 90–1825. | INPUT |
| `ld_rate_per_week` | DECIMAL(5,4) | Y | Default 0.005 (0.5%). Read by M05 for LD calc. | INPUT |
| `ld_cap_pct` | DECIMAL(5,4) | Y | Default 0.10 (10% of contract value). Read by M05. | INPUT |
| `risk_buffer_pct` | DECIMAL(5,4) | Y | Default 0.05 (5% of contract value). Read by M05 for contingency init. | INPUT |
| `warranty_period_years` | INTEGER | N | Default 1. Read by M15 Handover. | INPUT |
| `payment_credit_days` | INTEGER | Y | Default 30. Range 0–90. | INPUT |
| `escalation_clause_enabled` | BOOLEAN | Y | Default false | INPUT |
| `created_by` | UUID | Y | — | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_by` | UUID | Y | Auto | LINK → M34.User |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |

**Composite uniqueness:** (`tenant_id`, `project_id`, `contract_code`)

---

### 3f. Entity: `Party`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `party_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | FK → M34.Tenant. Party master is global within tenant. | LINK → M34.Tenant |
| `party_code` | VARCHAR(20) | Y | Unique within tenant. Uppercase. | INPUT |
| `party_legal_name` | VARCHAR(300) | Y | Full legal name | INPUT |
| `party_short_name` | VARCHAR(100) | N | Display name | INPUT |
| `party_type` | ENUM | Y | `Client / EPC_Contractor / PMC / Consultant / Specialist_Subcontractor / Vendor / Lender / Auditor / Authority` | INPUT |
| `pan_number` | VARCHAR(10) | N | Indian PAN format `[A-Z]{5}[0-9]{4}[A-Z]{1}` | INPUT |
| `gst_number` | VARCHAR(15) | N | Indian GSTIN format | INPUT |
| `cin_number` | VARCHAR(21) | N | Indian Corporate Identity Number | INPUT |
| `registered_address` | TEXT | N | Max 1000 chars | INPUT |
| `pincode` | CHAR(6) | N | Must exist in PincodeMaster if provided | INPUT |
| `contact_person_name` | VARCHAR(200) | N | — | INPUT |
| `contact_email` | VARCHAR(150) | N | Valid email format | INPUT |
| `contact_phone` | VARCHAR(15) | N | Indian format | INPUT |
| `long_term_rating` | DECIMAL(4,2) | N | 0.00–100.00. Updated by M04 contractor performance scoring (Phase 1) and M30 vendor scorecards (Phase 2). | LINK → M04 / M30 |
| `created_by` | UUID | Y | — | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_by` | UUID | Y | Auto | LINK → M34.User |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |

**Note:** `User.party_id` (M34) provides one-way link from User to Party. M01 does NOT maintain Party.linked_users back-reference (per OQ-1.8). Query "users for party" via JOIN.

---

### 3g. Entity: `ProjectPartyAssignment`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `assignment_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | FK → Project | LINK → Project |
| `party_id` | UUID | Y | FK → Party (must be active in tenant) | LINK → Party |
| `party_role` | ENUM | Y | `Primary_Client / Co_Client / EPC_Contractor / PMC / Design_Consultant / MEP_Consultant / Structural_Consultant / Specialist_Subcontractor / Vendor / Lender / NABH_Auditor / Other` | INPUT |
| `role_seq` | INTEGER | Y | 1, 2, 3... within same role within same project. Auto-assigned. | SYSTEM |
| `is_primary_for_role` | BOOLEAN | Y | True for the lead party in that role. Only one primary per role per project. | INPUT |
| `engagement_start` | DATE | Y | Defaults to project planned_start_date | INPUT |
| `engagement_end` | DATE | N | NULL = indefinite | INPUT |
| `assigned_by` | UUID | Y | FK → M34.User | LINK → M34.User |
| `assigned_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `exclusivity_override_required` | BOOLEAN | Y | CALC: true if party already active on another project in same party_role | CALC |
| `exclusivity_override_approved` | BOOLEAN | Y | Default false. Required true if override flag set. | SYSTEM |
| `exclusivity_override_approver_user_id` | UUID | N | FK → M34.User. Must hold PMO_DIRECTOR role. | LINK → M34.User |
| `exclusivity_override_reason` | TEXT | N | Required if override approved. Min 100 chars. | INPUT |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |

**Composite uniqueness:** (`tenant_id`, `project_id`, `party_id`, `party_role`) — same party can be on same project in different roles, but not same role twice.

---

### 3h. Entity: `ProjectPhaseHistory`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `phase_history_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | FK → Project | LINK → Project |
| `from_phase` | ENUM | N | Per X8 §3.9 `Phase`. NULL only on initial creation entry. | SYSTEM |
| `to_phase` | ENUM | Y | Per X8 §3.9 `Phase` | SYSTEM |
| `transitioned_by` | UUID | Y | FK → M34.User | LINK → M34.User |
| `transitioned_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `gate_passage_id` | UUID | N | FK → M08.GatePassage if phase change was triggered by gate passage | LINK → M08.GatePassage |
| `transition_reason` | TEXT | N | Min 30 chars if not gate-triggered | INPUT |

**Append-only.** No updates. No soft delete.

---

### 3i. Entity: `ProjectStatusHistory`

Same shape as ProjectPhaseHistory but for project_status transitions. Append-only.

| Field | Type | Required | Notes |
|---|---|---|---|
| `status_history_id` | UUID | Y | — |
| `tenant_id` | UUID | Y | — |
| `project_id` | UUID | Y | — |
| `from_status` | ENUM | N | NULL on initial Draft creation |
| `to_status` | ENUM | Y | Per X8 §3.8 |
| `transitioned_by` | UUID | Y | — |
| `transitioned_at` | TIMESTAMP | Y | — |
| `transition_reason` | TEXT | N | Min 100 chars for reactivations (Closed/Cancelled → Active forbidden anyway; for On_Hold → Active also required) |

---

### 3j. Entity: `ScenarioConfig`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `config_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | FK → Project. Unique. | LINK → Project |
| `active_scenario` | ENUM | Y | `Base / Best / Worst`. Default `Base`. | INPUT |
| `base_escalation_pct` | DECIMAL(5,4) | Y | Default 0.05 | INPUT |
| `best_escalation_pct` | DECIMAL(5,4) | Y | Must be ≤ base_escalation_pct | INPUT |
| `worst_escalation_pct` | DECIMAL(5,4) | Y | Must be ≥ base_escalation_pct | INPUT |
| `base_delay_months` | INTEGER | Y | Default 2 | INPUT |
| `best_delay_months` | INTEGER | Y | Must be ≤ base_delay_months | INPUT |
| `worst_delay_months` | INTEGER | Y | Must be ≥ base_delay_months | INPUT |
| `monsoon_delay_months` | INTEGER | Y | Default 2. Range 0–4. | INPUT |
| `payment_delay_risk_days` | INTEGER | Y | Default 15 | INPUT |
| `material_escalation_pct` | DECIMAL(5,4) | Y | Auto-selected from active_scenario.escalation_pct | CALC |
| `last_updated_by` | UUID | Y | — | LINK → M34.User |
| `last_updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |

---

### 3k. Entity: `KPIThreshold`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `threshold_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | FK → Project | LINK → Project |
| `kpi_name` | ENUM | Y | `CPI / SPI / Gross_Margin / Open_High_Risks / Pending_Clearances` | SYSTEM |
| `green_threshold` | DECIMAL(8,4) | Y | Green ≥ this value (or ≤ for inverted KPIs like Open_Risks) | INPUT |
| `amber_threshold` | DECIMAL(8,4) | Y | Amber ≥ amber, < green (inverse for inverted KPIs). Must be different from green_threshold. | INPUT |
| `red_threshold` | DECIMAL(8,4) | Y | Auto = "below amber" | CALC |
| `kpi_direction` | ENUM | Y | `Higher_Is_Better / Lower_Is_Better` | SYSTEM |
| `default_applied` | BOOLEAN | Y | True if system defaults used without user edit | SYSTEM |
| `updated_by` | UUID | Y | — | LINK → M34.User |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

**Composite uniqueness:** (`tenant_id`, `project_id`, `kpi_name`).

**Default KPI thresholds (pre-populated on project creation per OQ-2.1):**

| KPI | Direction | Green | Amber | Red |
|---|---|---|---|---|
| CPI | Higher_Is_Better | ≥ 1.00 | ≥ 0.95 | < 0.95 |
| SPI | Higher_Is_Better | ≥ 1.00 | ≥ 0.95 | < 0.95 |
| Gross_Margin | Higher_Is_Better | ≥ 0.20 | ≥ 0.10 | < 0.10 |
| Open_High_Risks | Lower_Is_Better | ≤ 5 | ≤ 8 | > 8 |
| Pending_Clearances | Lower_Is_Better | ≤ 3 | ≤ 6 | > 6 |

---

### 3l. Entity: `PincodeMaster`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `pincode` | CHAR(6) | Y | Numeric. Primary key. | SYSTEM (seed) |
| `state_code` | VARCHAR(2) | Y | ISO state code (e.g., MH, DL, KA) | SYSTEM (seed) |
| `state_name` | VARCHAR(50) | Y | — | SYSTEM (seed) |
| `district_name` | VARCHAR(100) | Y | — | SYSTEM (seed) |
| `city_name` | VARCHAR(100) | Y | — | SYSTEM (seed) |
| `region` | ENUM | Y | `North / South / East / West / Northeast / Central` | SYSTEM (seed) |
| `dataset_version` | VARCHAR(20) | Y | e.g., `IndiaPost_2026_Q1`. Refreshed annually by SYSTEM_ADMIN. | SYSTEM |
| `loaded_at` | TIMESTAMP | Y | When last refreshed | SYSTEM |

**Note:** Static snapshot per OQ-1.9. ~155k records, ~2 MB. SYSTEM_ADMIN refreshes annually via dataset import.

---

### 3m. Decision Queue Integrations

M01 generates Decision Queue items per X8 trigger naming convention (UPPER_SNAKE_CASE):

| Trigger Type | Owner | SLA | Severity | Source BR |
|---|---|---|---|---|
| `BAC_VS_CONTRACT_DEVIATION` | FINANCE_LEAD + PMO_DIRECTOR | 24 hr | High | BR-01-013 |
| `EXCLUSIVITY_EXCEPTION_APPROVAL` | PMO_DIRECTOR | 12 hr | Medium | BR-01-011 |
| `PROJECT_REPORT_DATE_STALE` | PROJECT_DIRECTOR | None (informational amber) | Low | BR-01-017 |
| `MULTIPLE_PRIMARY_CONTRACTS_FLAG` | PMO_DIRECTOR | 24 hr | Medium | BR-01-018 |
| `SCENARIO_CHANGE_APPROVAL` | PMO_DIRECTOR | 24 hr | High | BR-01-016 |

**SLA escalation table** (applies to all M01 Decision Queue items):

| Time Since Created | Action |
|---|---|
| 0–12 hr | Normal — no action |
| 12–24 hr | Reminder notification to owner |
| 24–36 hr | Escalate to next level (PMO_DIRECTOR if not already) |
| 36+ hr | Auto-escalate + log governance breach + amber on M10 |

---

## BLOCK 4 — DATA POPULATION RULES

### 4a. Role × Action Permission Matrix

References M34 canonical role names. Cross-reference X1 RBAC Matrix (when populated).

| Action | SYSTEM_ADMIN | PMO_DIRECTOR | PORTFOLIO_MGR | PROJECT_DIR | FINANCE_LEAD | OTHERS | READ_ONLY |
|---|---|---|---|---|---|---|---|
| Create Portfolio | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Create Program | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Create Project | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Edit Project identity (name, sector, dates) | ❌ | ✅ | ✅ | ✅ (own) | ❌ | ❌ | ❌ |
| Edit Contract financial terms | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Create Contract | ❌ | ✅ | ❌ | ✅ (own, non-Primary) | ✅ | ❌ | ❌ |
| Edit KPI thresholds | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Edit ScenarioConfig | ❌ | ✅ | ✅ (own program) | ❌ | ❌ | ❌ | ❌ |
| Change active_scenario | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Create Party (global master) | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Edit Party | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Assign Party to Project | ❌ | ✅ | ✅ | ✅ (own) | ❌ | ❌ | ❌ |
| Approve exclusivity override | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Approve multiple-Primary justification | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Change project_status (to On_Hold/Closed/Cancelled) | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Change current_phase manually (override gate-triggered) | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Update report_date | ❌ | ✅ | ✅ | ✅ (own) | ❌ | ❌ | ❌ |
| Soft delete Project | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Refresh PincodeMaster dataset | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| View Portfolio/Program/Project list | ✅ | ✅ | ✅ | ✅ (own) | ✅ | ✅ (own) | ✅ |
| View Contract financial details | ✅ | ✅ | ❌ | ✅ (own, summary) | ✅ | ❌ | ❌ |
| View Party master | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |

### 4b. Mandatory Fields at Creation

**Project (status=Draft):**
```
project_code, project_name, portfolio_id, program_id, sector_top_level,
sector_sub_type_code, delivery_model, pincode, planned_start_date,
planned_end_date, report_date, current_phase
```

**Project (transition to Active per BR-01-010):**
```
+ at least 1 Contract with contract_role=Primary
+ ProjectPartyAssignment with party_role=Primary_Client
+ ProjectPartyAssignment with party_role=EPC_Contractor (or contract-role-equivalent)
+ ScenarioConfig set
+ KPIThreshold set (default values explicitly confirmed by user)
```

### 4c. Entry Methods

| Field group | Method |
|---|---|
| Portfolio / Program | Sequential structured forms (Portfolio first) |
| Project identity | Single form, multi-section (Identity / Geography / Dates / Phase / Contracts / Parties / Scenario / KPIs) |
| sector_top_level | Dropdown (5 values) |
| sector_sub_type_code | Dependent dropdown (filtered by sector_top_level via parent_code_id) |
| delivery_model | Dropdown (6 values) |
| Pincode | Text input (6 digits) → real-time validation → auto-resolve state/city/district |
| Dates | Date picker with cross-field validation |
| Party (new) | Form: creates Party global record, then auto-creates ProjectPartyAssignment |
| Party (existing) | Search-and-select from global Party master |
| Contract | Sub-form within Project create wizard; multiple contracts addable |
| KPI thresholds | Pre-populated with defaults; user must explicitly confirm before save |
| ScenarioConfig | Form with system defaults; tabbed Base/Best/Worst editor |

### 4d. Default Values (per OQ-2)

| Field | Default | Source |
|---|---|---|
| GST rate | 0.18 | OQ-2.2 |
| Project code format | `[CLIENT]-[SEQ]-[TYPE]` | OQ-2.3 |
| Active scenario | `Base` | OQ-2.9 |
| Mobilisation advance | 10% | Industry standard |
| Material advance | 5% | Industry standard |
| Retention | 5% | Industry standard |
| DLP term | 365 days | Industry standard |
| LD rate | 0.5%/week | Industry standard |
| LD cap | 10% | Industry standard |
| Risk buffer | 5% | Industry standard |
| Payment credit | 30 days | Industry standard |
| Warranty | 1 year | Industry standard |
| Report date staleness threshold | Tier by reporting period (35/10/2 days) | OQ-1.7 |

---

## BLOCK 5 — FILTERS AND VIEWS

### 5a. Portfolio Summary (PMO_DIRECTOR / PORTFOLIO_MANAGER)

```
Card grid layout. One card per project.
Filter: portfolio | program | sector_top_level | delivery_model | rag_status | project_status | current_phase
Sort: rag_status DESC (Red first) → project_code ASC

Card:
  [project_code]                          [RAG badge]
  [project_name]
  Client: [name] · Contractor: [name]
  Phase: [current_phase] · Month [N] / [M] · [Z]% time elapsed
  Contract: ₹[value]Cr · [contract_type]
  CPI: [value] · SPI: [value]
  [Decision Queue badge: N pending] [if > 0]
```

### 5b. Project List (tabular)

```
Columns: project_code | name | portfolio | program | sector | model | phase | status | RAG | start | end | contract_value | client | contractor
Filters: as above + multi-select on phase, party search
Export: CSV
```

### 5c. Project Detail (PROJECT_DIRECTOR own / PMO_DIRECTOR all)

Tabbed:
- Identity & Geography
- Dates & Phase (incl. ProjectPhaseHistory)
- Contracts (table of contracts)
- Parties (ProjectPartyAssignments grouped by role)
- Scenario Configuration
- KPI Thresholds
- Status History
- Audit (read-only)

### 5d. Exception View (PMO_DIRECTOR)

```
Show only projects where:
  rag_status = Red OR Amber, OR
  Decision Queue items pending, OR
  report_date stale, OR
  BAC vs contract deviation > ₹1 Cr
Sort: severity DESC
```

### 5e. Contract Summary (FINANCE_LEAD)

```
Tabular view across all projects:
  project_code | contract_code | role | type | value_basic | value_incl_gst | retention | LD_cap | DLP_days
Filters: project | role | type | signing_date range
```

### 5f. Party Assignment View (PMO_DIRECTOR)

```
Two views:
  Party-centric: party → all active project assignments (with role + dates)
  Project-centric: project → all party assignments by role
Highlight: parties with > 1 same-role active assignment (amber)
```

---

## BLOCK 6 — BUSINESS RULES

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---|---|---|---|---|
| BR-01-001 | Project create | project_code unique within tenant; format matches `[A-Z0-9]+-[0-9]+-[A-Z]+` | Block save if duplicate or format invalid | 🔴 Real-time |
| BR-01-002 | Date entry | planned_end_date > planned_start_date | Block save | 🔴 Real-time |
| BR-01-003 | Date entry | report_date ∈ [planned_start_date, planned_end_date] | Block save | 🔴 Real-time |
| BR-01-004 | Pincode entry | Pincode exists in PincodeMaster | Block save with error "Invalid pincode" | 🔴 Real-time |
| BR-01-005 | Pincode validated | state, city, district auto-populate from PincodeMaster; lock from edit | Populate CALC fields | 🔴 Real-time |
| BR-01-006 | Contract create | total_boq_cost (if provided) > contract_value_basic | Save with amber warning flag on contract | 🔴 Real-time |
| BR-01-007 | ScenarioConfig save | best_escalation_pct ≤ base_escalation_pct ≤ worst_escalation_pct | Block save if order violated | 🔴 Real-time |
| BR-01-008 | ScenarioConfig save | best_delay_months ≤ base_delay_months ≤ worst_delay_months | Block save if order violated | 🔴 Real-time |
| BR-01-009 | KPIThreshold save | For Higher_Is_Better: green > amber. For Lower_Is_Better: green < amber. | Block save if violated | 🔴 Real-time |
| BR-01-010 | Project status transition Draft → Active | Validate: at least 1 Contract role=Primary; ProjectPartyAssignment with role=Primary_Client; ProjectPartyAssignment with role=EPC_Contractor; ScenarioConfig present; KPIThreshold present (5 KPIs) | Block transition with specific failure list | 🔴 Real-time |
| BR-01-011 | ProjectPartyAssignment create | Same Party already on another active Project with same party_role AND is_primary_for_role=true | Set exclusivity_override_required=true. Generate Decision Queue: `EXCLUSIVITY_EXCEPTION_APPROVAL`. Block status of new assignment until approved. | 🔴 Real-time |
| BR-01-012 | Project.report_date updated | Any change | 🔴 Real-time cascade: project_month → pct_time_elapsed → M03 PV recalc → M07 EVM recalc → M01 rag_status → M10 cards. Audit log entry. | 🔴 Real-time |
| BR-01-013 | M07 sends BAC update | abs(BAC_total − sum(Contract.contract_value_basic)) > ₹1,00,00,000 (1 Cr) | Generate Decision Queue: `BAC_VS_CONTRACT_DEVIATION`, severity=High, owner=FINANCE_LEAD + PMO_DIRECTOR, SLA=24hr | 🟡 2-4hr |
| BR-01-014 | Project.project_status → Closed/Cancelled | Status change | All downstream modules (M02–M09) become read-only for this project (enforced at API gate via M34 permission check). ProjectStatusHistory entry. | 🔴 Real-time |
| BR-01-015 | Project create | KPIThreshold rows auto-populated with default values per 4d defaults table; default_applied=true | User must edit or explicitly confirm-as-default before transition to Active | 🔴 Real-time |
| BR-01-016 | ScenarioConfig.active_scenario change | Any change | Generate Decision Queue: `SCENARIO_CHANGE_APPROVAL`, owner=PMO_DIRECTOR, SLA=24hr. Block scenario change until approved. On approval: cascade material_escalation_pct → M06 + M07. | 🔴 Real-time |
| BR-01-017 | Daily Celery Beat | Project.report_date < today − Project.report_date_staleness_threshold_days | Set amber flag on project card. Generate Decision Queue: `PROJECT_REPORT_DATE_STALE`, owner=PROJECT_DIRECTOR. Notify. | 🟢 24hr |
| BR-01-018 | Contract create OR edit role=Primary | Count Primary contracts on project | If count > 3: BLOCK save with hard error. If count > 1: amber flag + require justification ≥ 100 chars. Generate Decision Queue: `MULTIPLE_PRIMARY_CONTRACTS_FLAG`, owner=PMO_DIRECTOR. | 🔴 Real-time |
| BR-01-019 | Project soft delete attempt | Check existence of dependent records: M02 WBS, M03 Schedule, M04 Progress, M06 Cost entries, etc. | BLOCK if any child records exist. Error: "Cannot delete project with N child records. Use Cancelled status instead." | 🔴 Real-time |
| BR-01-020 | Project create | reporting_period_type from M03 NOT yet set (M03 not initialised) | Set Project.report_date_staleness_threshold_days = 35 (Monthly default). Recalc when M03 initialises with actual reporting_period_type. | 🔴 Real-time |
| BR-01-021 | M03 reporting_period_type set/changed | Any change | Recalculate Project.report_date_staleness_threshold_days: Monthly→35, Weekly→10, Daily→2. PMO_DIRECTOR override preserved if set. | 🔴 Real-time |
| BR-01-022 | Phase transition (current_phase change) | Any change | Append ProjectPhaseHistory entry. Set transitioned_by, transitioned_at, gate_passage_id (if from M08). Audit log. | 🔴 Real-time |
| BR-01-023 | Status transition (project_status change) | Any change | Validate transition is permitted by state machine. Append ProjectStatusHistory. Audit log. Notify PORTFOLIO_MANAGER and PROJECT_DIRECTOR. | 🔴 Real-time |
| BR-01-024 | Reactivation attempt: Closed/Cancelled → any | Any attempt | BLOCK at state machine. Error: "Closed/Cancelled projects cannot be reactivated. Create a new project if work resumes." | 🔴 Real-time |
| BR-01-025 | Reactivation attempt: On_Hold → Active | Status change | Allow, but require transition_reason ≥ 100 chars. Audit log entry with reason. | 🔴 Real-time |
| BR-01-026 | Sector top-level change | Project.sector_top_level edited after creation | BLOCK. Error: "Sector cannot be changed after project creation. Cancel project and create new if reclassification needed." | 🔴 Real-time |
| BR-01-027 | Sector sub-type code change | Project.sector_sub_type_code edited | Validate new sub-type's parent_code_id matches Project.sector_top_level. Block if mismatch. | 🔴 Real-time |
| BR-01-028 | Pincode dataset refresh | SYSTEM_ADMIN initiates PincodeMaster bulk import | Validate all CSV rows. All-or-nothing transaction. Update dataset_version. SystemAuditLog: PINCODE_DATASET_REFRESHED, severity=Info, privileged=true. | 🔴 Real-time |
| BR-01-029 | Multi-Primary justification | Decision queue MULTIPLE_PRIMARY_CONTRACTS_FLAG approved | Persist justification on Contract record. Clear amber flag. | 🔴 Real-time |
| BR-01-030 | Status change Active → On_Hold | PMO_DIRECTOR action | Optionally specify "Hold reason" + "Expected resume date". Notify all parties on assignment. Downstream modules read-only. | 🔴 Real-time |

---

## BLOCK 7 — INTEGRATION POINTS

| Direction | Module | Data Exchanged | Trigger | Speed Tier |
|---|---|---|---|---|
| RECEIVES FROM | M34 | Authenticated user_id, tenant_id, role, project_scope on every API call | Every request | 🔴 Real-time |
| RECEIVES FROM | M34 | Permission check `can(user, action, entity, scope)` | Every state-changing request | 🔴 Real-time |
| RECEIVES FROM | M34 | CodeMaster reference data (SectorSubType, etc.) | Form rendering | 🔴 Real-time |
| SENDS TO | M02 Structure & WBS | project_id, contract_id(s), planned_start/end, current_phase | On project Activation | 🔴 Real-time |
| SENDS TO | M03 Planning | project_id, planned dates, current_phase, report_date, active_scenario | On Activation + report_date change + scenario change | 🔴 Real-time |
| SENDS TO | M05 Risk & Change | Contract.ld_rate_per_week, ld_cap_pct, risk_buffer_pct, contract_value_basic | On Activation + Contract edit | 🔴 Real-time |
| SENDS TO | M06 Financial | contract_id, all financial terms, scenario_config.material_escalation_pct | On Activation + Contract edit + scenario change | 🔴 Real-time |
| SENDS TO | M07 EVM | contract_value_basic per Contract, KPI thresholds, active_scenario, report_date | On Activation + threshold/scenario/date change | 🔴 Real-time |
| SENDS TO | M08 Gate Control | project_id, current_phase, contract_type, project_status | On phase/status change | 🔴 Real-time |
| SENDS TO | M09 Compliance | project_id, sector_top_level, sector_sub_type_code, current_phase | On Activation (drives compliance template selection) | 🔴 Real-time |
| SENDS TO | M10 EPCC Command | All project summary fields for portfolio cards | On any project update | 🟡 2-4hr (snapshot) |
| SENDS TO | M11 Action Register | Decision Queue items per BR-01-011, 013, 016, 017, 018 | When triggered | 🔴 Real-time |
| RECEIVES FROM | M07 EVM | BAC_total per project for BR-01-013 | After EVM recalc | 🟡 2-4hr |
| RECEIVES FROM | M08 Gate Control | gate_passage_id for ProjectPhaseHistory linkage | On gate passage | 🔴 Real-time |
| RECEIVES FROM | M09 Compliance | pending_clearances_count for KPI | After compliance update | 🟢 24hr |
| RECEIVES FROM | M04 + M30 | Party.long_term_rating updates from contractor performance | Quarterly batch (Phase 1) / Real-time (Phase 2) | 🟢 24hr |
| RECEIVES FROM | M03 Planning | reporting_period_type for staleness threshold tier | On M03 init + reporting period change | 🔴 Real-time |
| LINKS TO | M34.User | User.party_id back-reference (M34 owns; M01 reads via JOIN) | On user list query for party | LINK |

---

## BLOCK 8 — GOVERNANCE AND AUDIT

### 8a. Logged Events (M01-owned audit log; cross-cutting events forwarded to M34 SystemAuditLog)

| Action | Logged | Detail | Visible To | Retention |
|---|---|---|---|---|
| Portfolio created | Yes | All fields | SYSTEM_ADMIN, PMO_DIRECTOR | Permanent |
| Program created | Yes | All fields | SYSTEM_ADMIN, PMO_DIRECTOR | Permanent |
| Project created | Yes | All initial field values | PMO_DIRECTOR, PORTFOLIO_MANAGER | Permanent |
| Project field edited | Yes | Field name, from/to values, user, timestamp | PMO_DIRECTOR, PROJECT_DIRECTOR (own) | Project lifetime |
| Project status changed | Yes | from/to status, reason, user | All on project | Permanent |
| Project phase changed | Yes | from/to phase, source (manual / gate-triggered), user | All on project | Permanent |
| Contract created | Yes | All fields | PMO_DIRECTOR, FINANCE_LEAD | Permanent |
| Contract financial terms edited | Yes | from/to per field | PMO_DIRECTOR, FINANCE_LEAD | Permanent |
| Party created | Yes | All fields | PMO_DIRECTOR, PORTFOLIO_MANAGER | Permanent |
| Party assigned to project | Yes | party_id, project_id, role, by whom | PMO_DIRECTOR | Project lifetime |
| Exclusivity override approved | Yes | party, projects, approver, reason | PMO_DIRECTOR | Permanent |
| Multi-Primary justification | Yes | contracts, reason, approver | PMO_DIRECTOR | Permanent |
| Scenario active changed | Yes | from/to scenario, approver | PMO_DIRECTOR | Permanent |
| KPI threshold edited | Yes | KPI, from/to, user | PMO_DIRECTOR | Permanent |
| Report date updated | Yes | old/new, cascade triggered | PMO_DIRECTOR | Project lifetime |
| Pincode dataset refreshed | Yes (forwarded to M34 SystemAuditLog: PINCODE_DATASET_REFRESHED) | Old version, new version, row counts | SYSTEM_ADMIN | Permanent |
| Soft delete attempt blocked | Yes | Reason (child records present) | PMO_DIRECTOR | Permanent |
| Soft delete executed | Yes | by whom, timestamp | PMO_DIRECTOR + SYSTEM_ADMIN | Permanent |
| Decision queue item created | Yes | trigger_type, owner, SLA | PMO_DIRECTOR | Permanent |
| Decision queue item resolved | Yes | resolution, time taken vs SLA | PMO_DIRECTOR | Permanent |
| SLA breach | Yes | item_id, breach duration | PMO_DIRECTOR | Permanent |

### 8b. Immutability Rules

- `ProjectPhaseHistory` and `ProjectStatusHistory` are append-only. No updates.
- `Contract.contract_value_basic` once set on Active project requires variation order workflow (M05) to change — cannot be edited directly.
- `project_code` immutable after creation.
- `project_name` editable but every edit logged.
- `sector_top_level` immutable after creation (BR-01-026).
- `tenant_id` always immutable.

### 8c. Privacy

- Party PAN, GST, CIN treated as sensitive PII. Display masked in non-Finance views (e.g., "ABCDE****1F").
- Per-tenant `dpdp_data_fiduciary_name` (M34 Tenant) referenced in any PII export.
- User can request data export of their own party_id linkage; PMO_DIRECTOR-initiated for others.

---

## BLOCK 9 — EXPLICIT EXCLUSIONS

```
This module does NOT:
─────────────────────────────────────────────────────────────────────
[ ] Store WBS, work packages, or BOQ items                  → M02
[ ] Define or track milestones, schedules, baselines        → M03
[ ] Capture site progress, NCRs, HSE, DLP defects           → M04
[ ] Store risk, issue, variation orders, EOTs               → M05
[ ] Record actual cost transactions, RA bills, retention    → M06
[ ] Calculate CPI, SPI, EAC, VAC, TCPI                     → M07
[ ] Manage stage gate criteria or STOP/GO logic             → M08
[ ] Track regulatory permits, NABH, AERB                    → M09
[ ] Aggregate portfolio-level command views                 → M10
[ ] Drive action items / decision queue resolution          → M11
[ ] Process tendering or contract award                     → M29
[ ] Manage vendor PQ, scorecards, blacklist                 → M30
[ ] Track BG / insurance certificate validity               → M23 (Phase 2)
[ ] Authenticate users or manage roles                      → M34
[ ] Issue or revoke permissions                              → M34
[ ] Store project documents                                 → MinIO + per-module
[ ] Process payments or invoices                            → M06
[ ] Compute long-term party rating from execution metrics   → M04 (Phase 1) + M30 (Phase 2)
[ ] Manage external party portal users                      → PF03 (Phase 3)
```

---

## BLOCK 10 — OPEN QUESTIONS

**All questions resolved. Zero open questions.**

| # | Question | Resolution |
|---|---|---|
| 1 | Phase enum: legacy 5-value vs X8 10-value? | **Adopt X8 10-value (OQ-1.1=A).** Phase enum aligned with stage gates. KDMC migration: `EPC` → `Construction`. |
| 2 | Sector as ENUM or CodeMaster? | **Hybrid (OQ-1.2=C).** SectorTopLevel ENUM (5 values: Healthcare/Infrastructure/Residential/Commercial/Industrial) + CodeMaster sub-types (Hospital_DBOT, Highway, etc.). X8 v0.2 adds SectorTopLevel. |
| 3 | DeliveryModel "Hybrid"? | **Dropped (OQ-1.3=A).** Hybrid arrangements captured in delivery_model_notes free text. |
| 4 | ProjectStatus "Draft" state? | **Added (OQ-1.4=A).** Initial state until BR-01-010 passes. |
| 5 | Party exclusivity rule: type or role? | **Same party_role overlap (OQ-1.5=B).** is_primary_for_role=true on both projects triggers exception. |
| 6 | Multiple Primary contracts permitted? | **Soft cap 3 (OQ-1.6=C).** Amber + justification > 1; hard block > 3. |
| 7 | Report date staleness threshold? | **Tier by reporting_period_type (OQ-1.7=C).** Monthly→35d, Weekly→10d, Daily→2d. |
| 8 | User-Party linkage direction? | **One-way, M34 owns (OQ-1.8=A).** User.party_id only. M01 doesn't maintain back-reference. |
| 9 | Pincode dataset strategy? | **Static snapshot (OQ-1.9=A).** ~155k records, ~2 MB. Annual refresh by SYSTEM_ADMIN. |
| 10 | Soft delete cascade rules? | **Block if child records exist (OQ-1.10=C).** Cancelled/Closed status used instead. |
| 11 | OQ-2.1 KPI threshold defaults | **Legacy values retained.** CPI/SPI ≥1.0/0.95, Gross Margin 20%/10%, Open High Risks ≤5/8, Pending Clearances ≤3/6. |
| 12 | OQ-2.2 GST default | **18%** |
| 13 | OQ-2.3 Project code format | **`[CLIENT]-[SEQ]-[TYPE]`** |
| 14 | OQ-2.4 Reserved fields | **Per X8 §6.** Standard pattern. |
| 15 | OQ-2.6 Project name uniqueness | **Within program, case-insensitive.** project_code unique system-wide. |
| 16 | OQ-2.7 SLA escalation table | **Legacy retained.** 12hr/24hr/36hr breach pattern. |
| 17 | OQ-2.8 Speed tier on report_date cascade | **🔴 Real-time.** Cascade sequence locked. |
| 18 | OQ-2.9 Default scenario | **Base.** |
| 19 | OQ-2.10 Pincode validation timing | **On-blur during entry.** Real-time. |
| 20 | OQ-2.11 Activation gating | **At least 1 Primary contract required (BR-01-010).** |
| 21 | OQ-2.12 Audit retention | **Permanent for create/financial/status/party events; 7 years for routine field edits.** |

---

## APPENDIX A — KDMC Reference Data Migration (Pilot Project)

Legacy KDMC data must be migrated when this spec is implemented:

| Legacy Field | Legacy Value | New Value | Source |
|---|---|---|---|
| Phase | `EPC` | `Construction` | OQ-1.1 |
| Sector | `Healthcare` | sector_top_level=`Healthcare`, sector_sub_type_code=`Hospital_DBOT` | OQ-1.2 |
| DeliveryModel | `DBOT` | `DBOT` | unchanged |
| ProjectStatus | `Active` | `Active` | unchanged |

| M01 Entity | KDMC Value |
|---|---|
| Portfolio | KDMC Healthcare Portfolio |
| Program | KDMC Municipal Hospitals Program |
| project_code | `KDMC-001-DBOT` |
| project_name | KDMC 150-Bed Maternity, Cancer & Cardiology Hospital |
| sector_top_level | `Healthcare` |
| sector_sub_type_code | `Hospital_DBOT` |
| delivery_model | `DBOT` |
| pincode | (Kalyan-Dombivli area; resolved from PincodeMaster) |
| planned_start_date | 2025-04-01 |
| planned_end_date | 2028-02-28 |
| planned_duration_days | 1063 |
| report_date | 2026-04-23 |
| project_month | 13 |
| pct_time_elapsed | 0.3640 |
| current_phase | `Construction` |
| project_status | `Active` |
| Primary client | KDMC (Kalyan-Dombivli Municipal Corporation) |
| EPC contractor | (to be confirmed in pilot) |

---

## APPENDIX B — Migration Notes

```
Migration: 20260503_0010_m01_initial_schema.py
  - Creates Portfolio, Program, Project, Contract, Party, ProjectPartyAssignment,
    ProjectPhaseHistory, ProjectStatusHistory, ScenarioConfig, KPIThreshold,
    PincodeMaster
  - All tables tenant-scoped per ES-DB-001
  - Composite uniqueness constraints
  - FK constraints to M34.Tenant, M34.User

Migration: 20260503_0011_m01_seed_pincodes.py
  - Bulk-load PincodeMaster from IndiaPost_2026_Q1 dataset (~155k rows)

Migration: 20260503_0012_m01_seed_codemaster_sector_subtypes.py
  - Seed CodeMaster with SectorSubType entries:
      Hospital_DBOT, Hospital_PPP, Hospital_EPC,
      Highway, Metro, Railway,
      Office_Commercial, Mall_Retail, Apartment_Residential,
      Warehouse_Industrial, Factory_Industrial
  - Each linked to parent SectorTopLevel via parent_code_id

Migration: 20260503_0013_m01_seed_default_kpi_thresholds.py
  - Define system-wide default KPI thresholds (used as starting values for new projects)
```

---

## APPENDIX C — API Surface (sketch)

```
Portfolio:
  GET    /api/v1/portfolios
  POST   /api/v1/portfolios
  GET    /api/v1/portfolios/{id}
  PATCH  /api/v1/portfolios/{id}
  DELETE /api/v1/portfolios/{id}                  (soft-delete; PMO_DIRECTOR)

Program:
  GET    /api/v1/portfolios/{p_id}/programs
  POST   /api/v1/portfolios/{p_id}/programs
  GET    /api/v1/programs/{id}
  PATCH  /api/v1/programs/{id}

Project:
  GET    /api/v1/projects                          ?portfolio_id&program_id&status&phase&rag
  POST   /api/v1/projects
  GET    /api/v1/projects/{id}
  PATCH  /api/v1/projects/{id}
  POST   /api/v1/projects/{id}/activate            (BR-01-010 gate)
  POST   /api/v1/projects/{id}/status              { to_status, reason }
  POST   /api/v1/projects/{id}/phase               { to_phase, reason }
  PATCH  /api/v1/projects/{id}/report-date         { report_date }   (triggers cascade)
  DELETE /api/v1/projects/{id}                     (soft-delete; BR-01-019)

Contract:
  GET    /api/v1/projects/{p_id}/contracts
  POST   /api/v1/projects/{p_id}/contracts
  PATCH  /api/v1/contracts/{id}

Party:
  GET    /api/v1/parties                           ?type&search
  POST   /api/v1/parties
  PATCH  /api/v1/parties/{id}

ProjectPartyAssignment:
  GET    /api/v1/projects/{p_id}/parties
  POST   /api/v1/projects/{p_id}/parties
  POST   /api/v1/assignments/{id}/exclusivity-override   { reason }   (PMO_DIRECTOR)
  DELETE /api/v1/assignments/{id}

ScenarioConfig:
  GET    /api/v1/projects/{p_id}/scenario
  PATCH  /api/v1/projects/{p_id}/scenario
  POST   /api/v1/projects/{p_id}/scenario/activate     { scenario }   (Decision Queue gated)

KPIThreshold:
  GET    /api/v1/projects/{p_id}/kpi-thresholds
  PATCH  /api/v1/projects/{p_id}/kpi-thresholds/{kpi_name}

Pincode:
  GET    /api/v1/pincodes/{pincode}                    (resolution)
  POST   /api/v1/admin/pincodes/refresh                (SYSTEM_ADMIN; CSV import)
```

---

*v1.0 — Spec locked. Zero open questions. Ready for Round 7 (Wireframes).*
