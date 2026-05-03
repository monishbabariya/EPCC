# M01 — Project Registry
## Module Specification v2.1
**Status:** Draft — Pending Review | **Locked:** No
**Spec Author:** PMO Director | **Date:** 2026-04-30
**Reference Standards:** EPCC_Standards_Memory.md v2.0

---

## CHANGE LOG

| Version | Date | Change Summary |
|---------|------|---------------|
| v1.0 | 2026-04-29 | Initial draft |
| v2.0 | 2026-04-30 | Full retrofit — all Block 10 resolved |
| v2.1 | 2026-04-30 | Block 7 updated: M05 reads ld_rate_per_week + ld_cap_pct + risk_buffer_pct from Contract for LD and contingency calculations |; multi-contract; multi-portfolio; global party table; report date cascade; speed tiers; SLA escalation; decision queue integration; all Block 10 questions resolved |

---

## BLOCK 1 — Identity

```
Module ID             : M01
Module Name           : Project Registry
Layer                 : L1 Command
Decision It Enables   : Is this project authorized to exist in the portfolio,
                        and are its foundational parameters — identity, contract,
                        parties, dates, value, thresholds — correctly established
                        as the master reference for all downstream modules?
Primary User          : PMO Director
Secondary Users       : Portfolio Manager, Project Director, Finance Lead
```

---

## BLOCK 2 — Scope Boundary

| INCLUDES | EXCLUDES |
|----------|---------|
| Portfolio, Program, Project identity and classification | WBS / work breakdown structure → M02 |
| Project code, name, sector, delivery model | BOQ and cost items → M02 |
| Contract parties (client, contractor, PMC) and roles | Milestone schedule → M03 |
| Contract value, type, and financial terms | Actual cost transactions → M06 |
| Project dates, duration, and phase tracking | EVM calculations (CPI, SPI, EAC) → M07 |
| Geography via pincode | Stage gate approvals → M08 |
| Portfolio and program grouping hierarchy | Risk and issue register → M05 |
| KPI thresholds and RAG status (auto-calculated) | Compliance and regulatory tracking → M09 |
| Scenario configuration (Base / Best / Worst) | Document storage → Data Lake |
| Party master (global shared table) | Sub-contract management → M06 |
| Project-party assignment and exclusivity tracking | Billing and payment processing → M06 |
| Model version and report date | Execution data entry → M04 |

---

## BLOCK 3 — Data Architecture

### 3a. Entities

| Entity | Description | Cardinality |
|--------|-------------|-------------|
| `Portfolio` | Top-level grouping of programs and projects | Many per organization |
| `Program` | Group of related projects under one strategic objective | Many per portfolio |
| `Project` | A single capital project | Many per program |
| `Contract` | A contract governing a project | Many per project (role-typed) |
| `Party` | Global master of all external entities — clients, contractors, consultants, vendors | Global shared — many projects |
| `ProjectPartyAssignment` | Links a Party to a Project with a defined role | Many per project, many per party |
| `ProjectPhase` | Tracks lifecycle phase transitions for a project | Many per project over time |
| `ScenarioConfig` | Scenario parameters (Base/Best/Worst) for a project | 1 active set per project |
| `KPIThreshold` | Green/Amber/Red thresholds per KPI per project | 1 set per KPI per project |
| `PincodeMaster` | Lookup table: pincode → state, city, district | System table — loaded once |

---

### 3b. Key Fields

#### Entity: `Portfolio`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `portfolio_id` | UUID | Y | Auto-generated, immutable | SYSTEM |
| `portfolio_code` | VARCHAR(20) | Y | Unique across system | INPUT |
| `portfolio_name` | VARCHAR(200) | Y | Non-empty | INPUT |
| `description` | TEXT | N | — | INPUT |
| `owner_user_id` | UUID | Y | Must exist in Users | LINK → Users |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |

---

#### Entity: `Program`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `program_id` | UUID | Y | Auto-generated, immutable | SYSTEM |
| `portfolio_id` | UUID | Y | Must exist in Portfolio | LINK → Portfolio |
| `program_code` | VARCHAR(20) | Y | Unique within portfolio | INPUT |
| `program_name` | VARCHAR(200) | Y | Non-empty | INPUT |
| `strategic_objective` | TEXT | N | — | INPUT |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |

---

#### Entity: `Project`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `project_id` | UUID | Y | Auto-generated, immutable, never shown in UI | SYSTEM |
| `project_code` | VARCHAR(20) | Y | Unique across system. Format: `[CLIENT]-[SEQ]-[TYPE]` | INPUT |
| `project_name` | VARCHAR(200) | Y | Non-empty | INPUT |
| `portfolio_id` | UUID | Y | Must exist in Portfolio | LINK → Portfolio |
| `program_id` | UUID | Y | Must exist in Program under same Portfolio | LINK → Program |
| `sector` | ENUM | Y | `Healthcare / Infrastructure / Residential / Commercial / Industrial` | INPUT (dropdown) |
| `delivery_model` | ENUM | Y | `EPC / DBOT / PPP / Hybrid` | INPUT (dropdown) |
| `pincode` | CHAR(6) | Y | Must exist in PincodeMaster. Numeric only. | INPUT |
| `state` | VARCHAR(50) | Y | Auto-resolved from PincodeMaster | CALC |
| `city` | VARCHAR(100) | Y | Auto-resolved from PincodeMaster | CALC |
| `district` | VARCHAR(100) | Y | Auto-resolved from PincodeMaster | CALC |
| `planned_start_date` | DATE | Y | Cannot precede today by > 365 days | INPUT |
| `planned_end_date` | DATE | Y | Must be > planned_start_date | INPUT |
| `planned_duration_days` | INTEGER | Y | Auto = planned_end_date − planned_start_date | CALC |
| `report_date` | DATE | Y | Must be between planned_start_date and planned_end_date | INPUT |
| `project_month` | INTEGER | Y | Auto = months elapsed from planned_start_date to report_date | CALC |
| `pct_time_elapsed` | DECIMAL(5,4) | Y | Auto = elapsed_days / planned_duration_days | CALC |
| `current_phase` | ENUM | Y | `DEV / DES / EPC / COM / OAM` | INPUT (dropdown) |
| `project_status` | ENUM | Y | `Active / On Hold / Closed / Cancelled` | INPUT (dropdown) |
| `rag_status` | ENUM | Y | Auto-computed from KPI thresholds after EVM run | CALC |
| `created_by` | UUID | Y | User who created the record | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto on every edit | SYSTEM |
| `is_active` | BOOLEAN | Y | Soft delete flag. Default true. | SYSTEM |

---

#### Entity: `Contract`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `contract_id` | UUID | Y | Auto-generated | SYSTEM |
| `contract_code` | VARCHAR(30) | Y | Unique within project. Format: `[PROJECT_CODE]-[ROLE]-[SEQ]` | INPUT |
| `project_id` | UUID | Y | Must exist in Project | LINK → Project |
| `contract_role` | ENUM | Y | `Primary / Secondary / Specialist` | INPUT (dropdown) |
| `contract_type` | ENUM | Y | `DBOT / EPC / Lump Sum / Item Rate / PPP` | INPUT (dropdown) |
| `contract_value_basic` | DECIMAL(15,2) | Y | > 0, in INR | INPUT |
| `gst_rate` | DECIMAL(5,4) | Y | Default 0.18. Range 0.00–0.28. | INPUT |
| `contract_value_incl_gst` | DECIMAL(15,2) | Y | Auto = contract_value_basic × (1 + gst_rate) | CALC |
| `total_boq_cost` | DECIMAL(15,2) | Y | > 0. Warning if > contract_value_basic. | INPUT |
| `consultancy_pct` | DECIMAL(5,4) | Y | Default 0.035 | INPUT |
| `overhead_pct` | DECIMAL(5,4) | Y | Default 0.08 | INPUT |
| `risk_buffer_pct` | DECIMAL(5,4) | Y | Default 0.05 | INPUT |
| `profit_margin_pct` | DECIMAL(5,4) | Y | > 0 | INPUT |
| `retention_pct` | DECIMAL(5,4) | Y | Default 0.02 | INPUT |
| `advance_pct` | DECIMAL(5,4) | Y | Default 0.05 | INPUT |
| `payment_terms_days` | INTEGER | Y | > 0. Default 15. | INPUT |
| `ld_rate_per_week` | DECIMAL(5,4) | Y | Default 0.005 | INPUT |
| `ld_cap_pct` | DECIMAL(5,4) | Y | Default 0.10 | INPUT |
| `dlp_months` | INTEGER | Y | Default 12. Range 6–24. | INPUT |
| `delay_interest_pct_month` | DECIMAL(5,4) | Y | Default 0.02 | INPUT |
| `tds_subcon_pct` | DECIMAL(5,4) | Y | Default 0.01 (Sec 194C) | INPUT |
| `tds_professional_pct` | DECIMAL(5,4) | Y | Default 0.10 (Sec 194J) | INPUT |
| `is_active` | BOOLEAN | Y | Soft delete flag | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |

---

#### Entity: `Party`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `party_id` | UUID | Y | Auto-generated, global | SYSTEM |
| `party_code` | VARCHAR(20) | Y | Unique across system | INPUT |
| `party_name` | VARCHAR(200) | Y | Non-empty | INPUT |
| `party_type` | ENUM | Y | `Client / Contractor / Consultant / PMC / Vendor / Specialist` | INPUT (dropdown) |
| `gstin` | VARCHAR(15) | N | Valid GSTIN format if provided | INPUT |
| `pan` | VARCHAR(10) | N | Valid PAN format if provided | INPUT |
| `contact_name` | VARCHAR(100) | N | — | INPUT |
| `contact_email` | VARCHAR(150) | N | Valid email format | INPUT |
| `contact_phone` | VARCHAR(15) | N | Valid Indian mobile format | INPUT |
| `pincode` | CHAR(6) | N | Must exist in PincodeMaster if provided | INPUT |
| `state` | VARCHAR(50) | N | Auto-resolved from pincode | CALC |
| `is_active` | BOOLEAN | Y | Soft delete flag | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |

---

#### Entity: `ProjectPartyAssignment`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `assignment_id` | UUID | Y | Auto-generated | SYSTEM |
| `project_id` | UUID | Y | Must exist in Project | LINK → Project |
| `party_id` | UUID | Y | Must exist in Party | LINK → Party |
| `assignment_role` | ENUM | Y | `Client / EPC Contractor / PMC / Design Consultant / Specialist` | INPUT (dropdown) |
| `effective_from` | DATE | Y | Must be within project dates | INPUT |
| `effective_to` | DATE | N | Must be > effective_from if provided | INPUT |
| `is_primary` | BOOLEAN | Y | Default false. Only one primary per role per project. | INPUT |
| `assigned_by` | UUID | Y | User who made the assignment | SYSTEM |
| `assigned_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `exclusivity_override_approved` | BOOLEAN | N | Required if party is active on another project in same category | SYSTEM |
| `exclusivity_override_approver` | UUID | N | PMO Director user ID | LINK → Users |
| `is_active` | BOOLEAN | Y | Soft delete flag | SYSTEM |

---

#### Entity: `ScenarioConfig`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `config_id` | UUID | Y | Auto-generated | SYSTEM |
| `project_id` | UUID | Y | Unique per project | LINK → Project |
| `active_scenario` | ENUM | Y | `Base / Best / Worst` | INPUT (dropdown) |
| `base_escalation_pct` | DECIMAL(5,4) | Y | Default 0.05 | INPUT |
| `best_escalation_pct` | DECIMAL(5,4) | Y | Must be ≤ base_escalation_pct | INPUT |
| `worst_escalation_pct` | DECIMAL(5,4) | Y | Must be ≥ base_escalation_pct | INPUT |
| `base_delay_months` | INTEGER | Y | Default 2 | INPUT |
| `best_delay_months` | INTEGER | Y | Must be ≤ base_delay_months | INPUT |
| `worst_delay_months` | INTEGER | Y | Must be ≥ base_delay_months | INPUT |
| `monsoon_delay_months` | INTEGER | Y | Default 2. Range 0–4. | INPUT |
| `payment_delay_risk_days` | INTEGER | Y | Default 15 | INPUT |
| `material_escalation_pct` | DECIMAL(5,4) | Y | Auto-selected from active_scenario | CALC |
| `last_updated_by` | UUID | Y | User who last changed scenario | SYSTEM |
| `last_updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

---

#### Entity: `KPIThreshold`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `threshold_id` | UUID | Y | Auto-generated | SYSTEM |
| `project_id` | UUID | Y | Linked to project | LINK → Project |
| `kpi_name` | ENUM | Y | `CPI / SPI / Gross_Margin / Open_High_Risks / Pending_Clearances` | SYSTEM |
| `green_threshold` | DECIMAL(8,4) | Y | Green ≥ this value | INPUT |
| `amber_threshold` | DECIMAL(8,4) | Y | Amber ≥ this value. Must be < green_threshold. | INPUT |
| `red_threshold` | DECIMAL(8,4) | Y | Auto = below amber_threshold | CALC |
| `default_applied` | BOOLEAN | Y | True if system defaults were used without user edit | SYSTEM |

**Default KPI thresholds (pre-populated on project creation):**

| KPI | Green | Amber | Red |
|-----|-------|-------|-----|
| CPI | ≥ 1.0 | ≥ 0.95 | < 0.95 |
| SPI | ≥ 1.0 | ≥ 0.95 | < 0.95 |
| Gross Margin % | ≥ 20% | ≥ 10% | < 10% |
| Open High Risks | ≤ 5 | ≤ 8 | > 8 |
| Pending Clearances | ≤ 3 | ≤ 6 | > 6 |

---

### 3c. Decision Queue Integration

M01 generates two decision-triggering conditions that create formal Decision records:

| Trigger Condition | Decision Type | Owner | SLA | Escalation |
|-----------------|--------------|-------|-----|-----------|
| BAC total (from M07) deviates from contract value by > ₹1 Cr | Financial Review | Finance Lead + PMO Director | 24 hrs | 36 hrs → PMO Director auto-notified + governance breach logged |
| Party being assigned to second active project in same category | Exclusivity Exception Approval | PMO Director | 12 hrs | 24 hrs → Portfolio Manager escalated |

---

## BLOCK 4 — Data Population Rules

### 4a. Role Permission Matrix

| Action | PMO Director | Portfolio Manager | Project Director | Finance Lead | Site Manager | Read-Only |
|--------|-------------|------------------|-----------------|-------------|-------------|----------|
| Create Portfolio / Program | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Create Project | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Edit project identity fields | ✅ | ✅ | ✅ (own) | ❌ | ❌ | ❌ |
| Edit contract financial terms | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Edit KPI thresholds | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Edit scenario config | ✅ | ✅ (own program) | ❌ | ❌ | ❌ | ❌ |
| Assign party to project | ✅ | ✅ | ✅ (own) | ❌ | ❌ | ❌ |
| Approve exclusivity override | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Change project status | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Soft delete | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| View all projects | ✅ | ✅ | ✅ (own) | ✅ | ✅ (own) | ✅ |

---

### 4b. Entry Method Per Entity / Field Group

| Entity / Field Group | Entry Method |
|---------------------|-------------|
| Portfolio, Program creation | Structured form — sequential (Portfolio first, then Program) |
| Project identity | Structured form — all mandatory fields on single screen |
| Sector, delivery model, phase, status | Dropdown — controlled list, no free text |
| Pincode | Text input (6 digits) → auto-resolves state, city, district on validation |
| Dates | Date picker — with real-time validation feedback |
| Party (new) | Form — creates global Party record; then auto-creates ProjectPartyAssignment |
| Party (existing) | Search and select from global Party master |
| Contract financial terms | Form — numeric fields with system defaults pre-populated |
| KPI thresholds | Form — pre-populated with EPCC standard defaults; user confirms or edits before save |
| Scenario config | Dropdown for active scenario + numeric fields for parameters |
| All CALC fields | Locked display — never editable |
| All SYSTEM fields | Not shown in UI — backend only |

---

### 4c. Mandatory vs Optional

| Field Group | Mandatory | System Behaviour if Empty |
|------------|-----------|--------------------------|
| Portfolio and Program | Yes — must exist before project creation | Blocks project creation |
| Project identity (name, code, sector, model) | Yes | Blocks save |
| Pincode | Yes | Blocks save. Invalid pincode blocks save. |
| Project dates (start + end) | Yes | Blocks save |
| Report date | Yes | Blocks save |
| Current phase | Yes | Blocks save |
| Client party assignment | Yes | Blocks project activation |
| EPC Contractor party assignment | Yes | Blocks project activation |
| PMC party assignment | No | Flagged as incomplete in audit. Project can be saved. |
| Primary contract (at least one) | Yes | Blocks project activation |
| Contract financial terms | All mandatory | Blocks contract save |
| KPI thresholds | Yes — defaults applied | User must confirm (click accept) before save — cannot silently bypass |
| Scenario config — active scenario | Yes | Defaults to Base if not selected |
| Scenario config — parameters | Yes — defaults applied | Defaults used with flag in audit log |

---

## BLOCK 5 — Filters & Views

### 5a. Standard Filters (Present on all list and table views)

| Filter | Type | Options |
|--------|------|---------|
| Portfolio | Single-select | All portfolios the user has access to |
| Program | Multi-select | Programs within selected portfolio |
| Sector | Multi-select | Healthcare / Infrastructure / Residential / Commercial / Industrial |
| Delivery Model | Multi-select | EPC / DBOT / PPP / Hybrid |
| Phase | Multi-select | DEV / DES / EPC / COM / OAM |
| Project Status | Multi-select | Active / On Hold / Closed / Cancelled |
| RAG Status | Multi-select | Green / Amber / Red |
| State | Multi-select | Auto-populated from pincode data — all states present in system |
| Planned Start Range | Date range picker | Filter by planned start date window |

### 5b. Module-Specific Filters

| Filter | Type | Options | Purpose |
|--------|------|---------|---------|
| Contract Role | Multi-select | Primary / Secondary / Specialist | View projects with specific contract types |
| Party | Search + select | All parties in global master | Find all projects linked to a specific party |
| Time Elapsed % | Range slider | 0–100% | Identify projects at risk by time consumption |
| Scenario | Single-select | Base / Best / Worst | Filter by active scenario |
| BAC Deviation | Toggle | > ₹1Cr deviation only | Show projects with financial integrity flag |

### 5c. Views

| View | Format | Default For | Who Sees |
|------|--------|------------|---------|
| Portfolio Summary | Card grid — one card per project, RAG colour badge, 6 key metrics | PMO Director, Portfolio Manager | All |
| Project List | Sortable, filterable table — all projects in scope | — | All |
| Project Detail | Single project — all blocks expanded with full field detail | Project Director | Own project |
| Exception View | Red and Amber projects only — sorted by severity | PMO Director | PMO Director |
| Contract Summary | Financial terms table — all contracts across projects | Finance Lead | Finance Lead |
| Party Assignment View | Party → all active projects map | PMO Director | PMO Director |

**Portfolio Summary Card (per project):**
```
[Project Code]                    [RAG Badge: GREEN / AMBER / RED]
[Project Name]
Client: [name] | Contractor: [name]
Phase: [phase] | Month [X] of [Y] | [Z]% time elapsed
Contract: ₹[value]Cr | Type: [DBOT/EPC/etc]
CPI: [value] [✅/⚠/🔴]  |  SPI: [value] [✅/⚠/🔴]
[Decision Queue Badge: X decisions pending]
```

---

## BLOCK 6 — Business Rules (Enhanced)

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---------|---------|-------|--------|------------|
| BR-01-001 | Project creation | `project_code` must be unique across entire system | Block save if duplicate | 🔴 Real-time |
| BR-01-002 | Date entry | `planned_end_date` must be > `planned_start_date` | Block save | 🔴 Real-time |
| BR-01-003 | Date entry | `report_date` must be between `planned_start_date` and `planned_end_date` | Block save | 🔴 Real-time |
| BR-01-004 | Pincode entry | Pincode must exist in PincodeMaster | Block save if not found. Show error: "Invalid pincode" | 🔴 Real-time |
| BR-01-005 | Pincode validation | State, city, district auto-resolve on pincode confirmation | Populate CALC fields. Lock from editing. | 🔴 Real-time |
| BR-01-006 | Contract creation | `total_boq_cost` > `contract_value_basic` | Warning flag — allow save with amber flag on contract | 🔴 Real-time |
| BR-01-007 | Scenario config | `best_escalation_pct` ≤ `base_escalation_pct` ≤ `worst_escalation_pct` | Block save if order violated | 🔴 Real-time |
| BR-01-008 | Scenario config | `best_delay_months` ≤ `base_delay_months` ≤ `worst_delay_months` | Block save if order violated | 🔴 Real-time |
| BR-01-009 | KPI threshold entry | `green_threshold` > `amber_threshold` | Block save if violated | 🔴 Real-time |
| BR-01-010 | Project activation | At least one Primary contract must exist | Block activation. Status cannot move from Draft to Active. | 🔴 Real-time |
| BR-01-011 | Party assignment | Party already active on another project in same `party_type` category | Generate Decision record (type: Exclusivity Exception). Block assignment until PMO Director approves. | 🔴 Real-time |
| BR-01-012 | Report date updated | Any change to `report_date` | Trigger full recalculation cascade (sequence: project_month → pct_time_elapsed → M03 PV → M07 EVM → M01 RAG → M10 cards) | 🔴 Real-time |
| BR-01-013 | BAC deviation received from M07 | BAC total deviates from `contract_value_basic` by > ₹1 Cr | Generate Decision record (type: Financial Review). Amber flag on project card. | 🟡 2-4hr |
| BR-01-014 | Project status → Closed | Status changed to Closed or Cancelled | All downstream modules (M02–M09) set to read-only for this project. Lock enforced at API level. | 🔴 Real-time |
| BR-01-015 | Project creation | KPI thresholds auto-populated with EPCC standard defaults | User must explicitly confirm or edit before project activates | 🔴 Real-time |
| BR-01-016 | Scenario active change | `active_scenario` changed (e.g., Base → Worst) | Requires PMO Director approval. Logged in audit. Triggers cascade: `material_escalation_pct` recalculated → M06 and M07 notified. | 🔴 Real-time |
| BR-01-017 | Daily system check | Projects where `report_date` has not been updated in > 35 days | Flag as stale. Amber badge on project card. Notification to Project Director. | 🟢 24hr |

### SLA Escalation Table (Decision-Generating Rules)

Applies to: BR-01-011 (Exclusivity Exception), BR-01-013 (BAC Deviation)

| Time Since Decision Created | Status | System Action |
|----------------------------|--------|--------------|
| 0–12 hrs | Normal | No action |
| 12–24 hrs | Attention | Reminder notification to decision owner |
| 24–36 hrs | Risk | Escalate to next level in role hierarchy |
| 36+ hrs | Critical | Auto-escalate to PMO Director + log as governance breach in audit |

---

## BLOCK 7 — Integration Points

| Direction | Module | Data Exchanged | Trigger | Speed Tier |
|-----------|--------|---------------|---------|------------|
| SENDS TO | M02 Structure & WBS | `project_id`, `contract_id`(s), phase list, `planned_start_date`, `planned_end_date` | On project activation | 🔴 Real-time |
| SENDS TO | M03 Planning | `project_id`, `planned_start_date`, `planned_end_date`, `current_phase`, `report_date` | On project activation + report date change | 🔴 Real-time |
| SENDS TO | M06 Financial | `contract_id`, all financial terms (retention, advance, LD, DLP), `scenario_config` | On project activation + any contract edit | 🔴 Real-time |
| SENDS TO | M07 EVM Engine | `contract_value_basic` per contract, `kpi_thresholds`, `active_scenario`, `report_date` | On activation + threshold/scenario/report date change | 🔴 Real-time |
| SENDS TO | M08 Gate Control | `project_id`, `current_phase`, `contract_type`, `project_status` | On phase change or status change | 🔴 Real-time |
| SENDS TO | M10 EPCC Command | All summary fields for portfolio card | On any project update | 🟡 2-4hr |
| RECEIVES FROM | M07 EVM Engine | `rag_status`, `cpi`, `spi`, `bac_total`, `eac`, `vac` | After each EVM recalculation run | 🟡 2-4hr |
| RECEIVES FROM | M08 Gate Control | `gate_health` indicator (% gates cleared) | After each gate update | 🟡 2-4hr |
| SENDS TO | M05 Risk & Change | `ld_rate_per_week`, `ld_cap_pct`, `risk_buffer_pct`, `contract_value_basic` per contract | On project activation — M05 reads for LD auto-calculation and contingency initialisation | 🔴 Real-time |
| RECEIVES FROM | M09 Compliance | `pending_clearances_count` | After compliance update | 🟢 24hr |

---

## BLOCK 8 — Governance & Audit

| Action | Logged | Field-Level Detail | Visible To | Retention |
|--------|--------|--------------------|-----------|-----------|
| Portfolio / Program created | Yes | — | PMO Director + System Admin | Permanent |
| Project created | Yes | All initial field values | PMO Director + System Admin | Permanent |
| Any field edited | Yes | Field name, old value, new value, user, timestamp | PMO Director | Project lifetime |
| Contract terms edited | Yes | Old + new values per field | PMO Director + Finance Lead | Permanent |
| Party assigned | Yes | Party, role, project, assigned by | PMO Director | Project lifetime |
| Exclusivity override approved | Yes | Party, projects involved, approver, reason | PMO Director | Permanent |
| Scenario changed | Yes | Old scenario, new scenario, user, timestamp | PMO Director | Permanent |
| KPI threshold changed | Yes | KPI name, old threshold, new threshold, user | PMO Director | Permanent |
| Project status changed | Yes | Old status, new status, user, timestamp | All | Permanent |
| Report date updated | Yes | Old date, new date, cascade triggered | PMO Director | Project lifetime |
| Soft delete | Yes | Deleted by, timestamp, reason | PMO Director + System Admin | Permanent |
| Decision created | Yes | Trigger type, owner, SLA | PMO Director | Permanent |
| Decision resolved | Yes | Resolution, decided by, time taken vs SLA | PMO Director | Permanent |
| SLA breach | Yes | Decision ID, breach duration | PMO Director | Permanent |

---

## BLOCK 9 — Explicit Exclusions

```
This module does NOT:
──────────────────────────────────────────────────────────────────
[ ] Store WBS, work packages, or BOQ items                  → M02
[ ] Define or track milestones or baselines                 → M03
[ ] Capture site progress or execution data                 → M04
[ ] Store risk, issue, or variation records                 → M05
[ ] Record actual cost transactions or billing              → M06
[ ] Calculate CPI, SPI, EAC, VAC, or TCPI                  → M07
[ ] Manage stage gate approvals or STOP/GO logic            → M08
[ ] Track regulatory permits, NOCs, or NABH compliance      → M09
[ ] Aggregate portfolio-level command views                 → M10
[ ] Manage sub-contractor agreements                        → M06
[ ] Store or manage project documents                       → Data Lake
[ ] Process payments or invoices                            → M06
```

---

## BLOCK 10 — Open Questions

**All questions from v1.0 resolved. Zero open questions.**

| # | Question | Resolution |
|---|----------|-----------|
| 1 | Can one project have multiple primary contracts? | Yes. `contract_role` ENUM supports multiple Primary contracts. |
| 2 | Is Portfolio single or multi? | Multi-portfolio supported. Portfolio is a full entity. |
| 3 | Is Party global or project-scoped? | Global shared table. Assignment tracked via `ProjectPartyAssignment`. Exclusivity rule enforced via BR-01-011. |
| 4 | Does report date trigger full cascade? | Yes. BR-01-012. Speed tier: 🔴 Real-time. Cascade sequence fully defined. |
| 5 | Pincode: embedded or external API? | Embedded PincodeMaster table. No external API dependency. |

---

## APPENDIX — KDMC Reference Data (Pilot Project)

*How KDMC maps to M01 entities:*

| M01 Entity | KDMC Value |
|-----------|-----------|
| Portfolio | KDMC Healthcare Portfolio |
| Program | KDMC Municipal Hospitals Program |
| Project Code | `KDMC-001-DBOT` |
| Project Name | KDMC 150-Bed Maternity, Cancer & Cardiology Hospital |
| Sector | Healthcare |
| Delivery Model | DBOT |
| Pincode | (Kalyan-Dombivli area — to be confirmed) |
| Planned Start | 01-Apr-2025 |
| Planned End | 28-Feb-2028 |
| Duration | 1,063 days |
| Report Date | 23-Apr-2026 |
| Project Month | 13 of 35 |
| % Time Elapsed | 36.4% |
| Current Phase | EPC |
| Client | KDMC (Kalyan-Dombivli Municipal Corporation) |
| EPC Contractor | M/s. Built Together |
| Contract Value (basic) | ₹161.02 Cr |
| GST Rate | 18% |
| Contract Value (incl. GST) | ₹190.00 Cr |
| BOQ Cost | ₹127.24 Cr |
| Retention | 2% |
| Advance | 5% |
| Payment Terms | 15 days |
| DLP | 12 months |
| Active Scenario | Base |
| RAG Status | YELLOW — Watch |

---

*This spec is complete when all 10 blocks are filled and Block 10 shows zero open questions.*
*Status: Ready for review. Lock requires explicit PMO Director confirmation.*
