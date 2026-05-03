# EPCC — Historical Data Import (HDI) System
## Specification v1.0
**Status:** Draft — Pending Review | **Locked:** No
**Spec Author:** PMO Director | **Date:** 2026-05-02
**Reference Standards:** EPCC_Standards_Memory_v5_2.md §7.109–§7.114
**Classification:** System-Level Utility (not a module — no M-number assigned)
**Purpose:** Enable EPCC deployment on in-progress projects by loading structured historical
data. Activates M07 statistical engine from day one of deployment.

---

## CHANGE LOG

| Version | Date | Change Summary |
|---------|------|---------------|
| v1.0 | 2026-05-02 | Initial spec. GAP-08 resolution. Covers governance, entities, CSV templates, validation, M07 activation, and cross-module data_source standard. |

---

## SECTION 1 — Problem Statement

EPCC is frequently deployed on projects that are already in progress. KDMC, the pilot project, is at Month 13 of 35 at time of EPCC deployment.

Without historical data, four critical failures occur:

**Failure 1 — M07 statistical engine cannot activate.** Holt's ES and OLS require ≥6 periods. On day one of a fresh deployment, the system has zero periods. Predictive alerts are silent for 6 months. PMO trust in the dashboard collapses before it is established.

**Failure 2 — EVM baselines are wrong.** Without historical PV, EV, and AC, the CPI and SPI are calculated from an artificial "month 1" starting point — even though the project is in month 13. Every EVM metric is misleading.

**Failure 3 — Decision Queue history is blank.** No historical gate passages, no prior VOs, no prior risks. The system appears to have no institutional memory.

**Failure 4 — Trend analysis produces false positives.** Predictive alerts built on 1–2 periods of data generate noise, not signal. PMO dismisses the feature.

The HDI system resolves all four failures by loading pre-EPCC historical data in a single, governed, one-time import event.

---

## SECTION 2 — Scope

### WHAT HDI DOES
- Loads structured historical project data from prior Excel or manual tracking sources
- Creates authentic EPCC records marked as `data_source = Historical_Seed`
- Activates M07 statistical engine immediately upon import of ≥6 periods
- Preserves full audit integrity — every seed record is distinguishable from live data
- Provides retroactive EVM snapshots, gate history, and VO register

### WHAT HDI DOES NOT DO
- It does NOT modify or backfill M01 Project Registry (project is already created in EPCC)
- It does NOT import BOQ items or WBS structure (M02 — must be set up in EPCC before HDI runs)
- It does NOT replace ongoing live data capture — HDI is a one-time historical seed only
- It does NOT guarantee the accuracy of imported data — that is the PMO Director's responsibility
- It does NOT allow corrections after Confirmed status (except via 7-day error window with System Admin)

---

## SECTION 3 — Pre-Conditions (must be met before HDI session can be created)

| Pre-Condition | Module | Verification |
|--------------|--------|-------------|
| Project created and active in M01 | M01 | project_status = Active |
| WBS structure and packages created | M02 | At least 1 active Package + WBS nodes |
| BOQ items created with actual_rate | M02 | bac_amount > 0 for at least 1 package |
| Reporting period granularity set | M03 | reporting_period_type confirmed |
| No prior HDI session (Confirmed) | System | HistoricalDataImportSession.status ≠ Confirmed |
| PMO Director role | RBAC | User.role = PMO_Director |

---

## SECTION 4 — Entities

### Entity: `HistoricalDataImportSession`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `session_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | FK → M01 Project. Unique non-failed session per project enforced. | LINK → M01 |
| `session_code` | VARCHAR(20) | Y | Format: `HDI-{project_code}-01`. e.g., `HDI-KDMC001-01`. | SYSTEM |
| `import_description` | TEXT | Y | Min 50 chars. PMO Director describes the import scope. | INPUT |
| `source_description` | TEXT | Y | Min 30 chars. Description of data source: "KDMC Monthly EVM Excel v3.2, PMO tracking file". | INPUT |
| `periods_start` | DATE | Y | Earliest reporting period being imported. Format YYYY-MM-01. | INPUT |
| `periods_end` | DATE | Y | Latest reporting period. Must be < today. Must be ≥ periods_start. | INPUT |
| `periods_count` | INTEGER | Y | CALC: months between periods_start and periods_end inclusive. | CALC |
| `status` | ENUM | Y | `Draft / Validated / Confirmed / Failed` | SYSTEM |
| `authorised_by` | UUID | N | FK → Users (PMO Director). Set on Confirmed. | INPUT |
| `authorised_at` | TIMESTAMP | N | Auto on Confirmed | SYSTEM |
| `files_uploaded` | JSONB | Y | Array: `[{type: "TYPE_A", filename: "...", row_count: N, upload_status: "Uploaded/Error"}]` | SYSTEM |
| `validation_errors` | INTEGER | Y | Total validation errors across all files. Must = 0 to proceed to Confirmed. | CALC |
| `validation_warnings` | INTEGER | Y | Total warnings (non-blocking). PMO Director reviews before confirming. | CALC |
| `validation_report` | JSONB | Y | Full per-file validation results. | SYSTEM |
| `records_imported` | JSONB | N | Populated on Confirmed. `{pv_profiles: N, progress: N, costs: N, gates: N, vos: N}` | SYSTEM |
| `statistical_engine_activated` | BOOLEAN | N | CALC after import: true if periods_count ≥ 6 | CALC |
| `recalc_job_id` | UUID | N | FK → RecalcQueue (Historical_Seed_Import job created on Confirmed) | LINK → RecalcQueue |
| `error_window_expires_at` | TIMESTAMP | N | CALC = authorised_at + 7 days. Error correction window. | CALC |

---

### Entity: `HistoricalImportRecord`

One record per imported row — the granular audit trail.

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `record_id` | UUID | Y | Auto-generated | SYSTEM |
| `session_id` | UUID | Y | FK → HistoricalDataImportSession | LINK |
| `import_type` | ENUM | Y | `TYPE_A / TYPE_B / TYPE_C / TYPE_D / TYPE_E` | SYSTEM |
| `source_row_number` | INTEGER | Y | Row number in original CSV | SYSTEM |
| `target_entity` | VARCHAR(50) | Y | e.g., "PVProfile", "ProgressEntry", "CostLedgerEntry" | SYSTEM |
| `target_record_id` | UUID | N | FK → created record. Null if record creation failed. | SYSTEM |
| `reporting_period` | DATE | Y | Period this record covers | SYSTEM |
| `status` | ENUM | Y | `Created / Failed / Skipped_Duplicate` | SYSTEM |
| `failure_reason` | TEXT | N | Populated if status = Failed | SYSTEM |

---

## SECTION 5 — CSV Templates (Full Field Specification)

### TYPE A — Historical PV Profile (MANDATORY)
**Target entity:** M03 PVProfile | **data_source:** Historical_Seed

| CSV Column | Type | Required | Notes |
|-----------|------|----------|-------|
| `wbs_code` | VARCHAR | Y | Must resolve to active WBSNode in M02. e.g., `3.1.2` |
| `reporting_period` | DATE | Y | Format: YYYY-MM. e.g., `2025-04` |
| `pv_this_period` | DECIMAL | Y | Planned value for this period only (INR). ≥ 0. |
| `pv_cumulative` | DECIMAL | Y | Cumulative PV through this period (INR). Non-decreasing across periods for same WBS. |
| `loading_profile` | ENUM | Y | `Front_Loaded / Bell / Back_Loaded / Linear`. Must match system ENUM. |
| `is_baseline_period` | BOOLEAN | Y | `TRUE` for all imported periods (all are baseline-locked historical data). |

**Validation checks:**
- wbs_code resolves to active WBSNode
- No gaps in reporting_period sequence per wbs_code
- pv_cumulative non-decreasing across periods per wbs_code
- pv_this_period = pv_cumulative(period) − pv_cumulative(period−1) ± 1% tolerance
- Sum of all wbs pv_this_period for a period = project-level PV for that period ± 5% tolerance (warning, not error)

---

### TYPE B — Historical Progress (MANDATORY)
**Target entity:** M04 ProgressEntry | **data_source:** Historical_Seed

| CSV Column | Type | Required | Notes |
|-----------|------|----------|-------|
| `wbs_code` | VARCHAR | Y | Must resolve to active WBSNode in M02. |
| `reporting_period` | DATE | Y | Format: YYYY-MM. |
| `pct_complete_reported` | DECIMAL | Y | Range 0.000 to 1.000 (e.g., 0.450 = 45%). |
| `measurement_method` | ENUM | Y | Must be valid M04 ENUM. Historical seed: `Subjective_Estimate` permitted — auto-set to Approved. |
| `progress_note` | TEXT | N | Optional context. |

**Validation checks:**
- wbs_code resolves to active WBSNode
- pct_complete_reported range 0–1
- No regression: pct_complete_reported(period N) ≥ pct_complete_reported(period N-1) for same wbs_code
- All seed ProgressEntry records: progress_approval_status = Approved (historical data auto-approved — no supervisor required)

---

### TYPE C — Historical Actual Costs (MANDATORY)
**Target entity:** M06 CostLedgerEntry | **data_source:** Historical_Seed

| CSV Column | Type | Required | Notes |
|-----------|------|----------|-------|
| `package_code` | VARCHAR | Y | Must resolve to active Package in M02. e.g., `PKG-01`. |
| `reporting_period` | DATE | Y | Format: YYYY-MM. |
| `ac_this_period` | DECIMAL | Y | Actual cost incurred in this period only (INR). ≥ 0. |
| `ac_cumulative` | DECIMAL | Y | Cumulative actual cost through this period (INR). Non-decreasing. |
| `cost_category` | ENUM | Y | `Civil / MEP / Medical / Consultant / PMC / Indirect / Other`. |

**Validation checks:**
- package_code resolves to active Package
- ac_cumulative non-decreasing across periods per package_code
- ac_this_period = ac_cumulative(period) − ac_cumulative(period−1) ± 1% tolerance
- Sum of all package ac_cumulative for latest period = project-level AC ± 5% tolerance (warning)

---

### TYPE D — Historical Gate Passages (OPTIONAL)
**Target entity:** M08 GatePassage | **data_source:** Historical_Seed

| CSV Column | Type | Required | Notes |
|-----------|------|----------|-------|
| `gate_code` | ENUM | Y | `SG-0` to `SG-11`. Must be valid gate for this project. |
| `actual_passage_date` | DATE | Y | Date gate was formally passed. Must be < today. |
| `passage_type` | ENUM | Y | `GO / Conditional_GO`. |
| `approver_name` | VARCHAR | Y | Free text. Historical approver may not be in EPCC Users table. |
| `approver_role` | VARCHAR | N | e.g., "PMO Director", "Project Director". |
| `passage_note` | TEXT | N | Any notes on the gate passage. |

**Validation checks:**
- gate_code is valid for this project's sector and template
- Gates must be in sequence: cannot import SG-7 passage without SG-6 passage
- actual_passage_date must be < today
- No duplicate gate_code entries (one passage record per gate)

---

### TYPE E — Historical VO Register (OPTIONAL)
**Target entity:** M05 VariationOrder | **data_source:** Historical_Seed

| CSV Column | Type | Required | Notes |
|-----------|------|----------|-------|
| `vo_code` | VARCHAR | Y | e.g., `VO-001`. Must be unique within project. |
| `vo_type` | ENUM | Y | `Cost_Variation / EOT / Combined`. |
| `description` | TEXT | Y | Min 30 chars. |
| `submitted_date` | DATE | Y | Date VO was formally submitted. |
| `status` | ENUM | Y | `Approved / Partially_Approved / Rejected / Disputed / Settled`. |
| `cost_impact` | DECIMAL | N | Approved cost impact (INR). 0 for time-only VOs. |
| `time_impact_days` | INTEGER | N | Approved time extension in days. 0 for cost-only VOs. |
| `cause_category` | ENUM | N | `Scope_Addition / Design_Change / Client_Delay / Force_Majeure / Other`. |

**Validation checks:**
- vo_code unique within project
- If status = Approved and cost_impact > 0: NO materialisation triggered (historical VOs assumed resolved in BOQ already)
- Imported VOs do NOT trigger VOBOQMaterialisation workflow — the flag `is_historical_seed = true` bypasses this

---

## SECTION 6 — Validation Protocol

### Validation Levels

| Level | Description | Blocking? |
|-------|-------------|----------|
| ERROR | Schema violation, unresolvable reference, constraint breach | YES — must fix before Confirmed |
| WARNING | Data quality concern, reconciliation variance > 5%, missing optional fields | NO — PMO Director reviews and acknowledges |
| INFO | Row count confirmation, period coverage, records created | NO — informational only |

### Validation Report Structure (returned to UI after upload)

```json
{
  "session_id": "uuid",
  "files": [
    {
      "type": "TYPE_A",
      "filename": "KDMC_PV_History.csv",
      "rows_parsed": 182,
      "errors": [
        {"row": 45, "column": "wbs_code", "message": "WBS code '3.1.9' not found in M02"}
      ],
      "warnings": [
        {"row": 0, "column": "summary", "message": "PV total variance 3.2% — within 5% tolerance"}
      ],
      "info": {"periods_found": 13, "wbs_nodes_covered": 14}
    }
  ],
  "cross_file_checks": [
    {"check": "TYPE_A_TYPE_B_period_alignment", "result": "PASS", "note": "All 13 periods present in both files"},
    {"check": "TYPE_B_TYPE_C_period_alignment", "result": "PASS", "note": "All 13 periods present in both files"},
    {"check": "TYPE_A_pv_total_vs_project_bac", "result": "WARNING", "message": "Latest period cumulative PV (₹42.3 Cr) is 4.8% below project BAC (₹127.24 Cr). Expected at 33.3% of duration. Confirm this is correct."}
  ],
  "overall": {
    "total_errors": 1,
    "total_warnings": 2,
    "can_confirm": false,
    "minimum_periods_met": true
  }
}
```

---

## SECTION 7 — Import Execution Sequence

After PMO Director clicks "Confirm Import":

```
Step 1: System sets HistoricalDataImportSession.status = Confirmed
        Locks session — no further file uploads permitted

Step 2: System writes all validated records to database
        Each record:
          data_source = Historical_Seed
          created_by = session_id (system action, not user)
          created_at = current timestamp (time of import, not historical date)
          is_active = true
          version_number = 1

Step 3: M07 RecalcQueue
        Creates RecalcQueue job:
          job_type = Historical_Seed_Import
          priority = STANDARD
          trigger_source = "HDI_Session_{session_id}"
          process_periods_in_sequence: periods_start to periods_end (oldest first)

Step 4: RecalcQueue processes each period
        For each imported period (oldest to newest):
          Reads: PVProfile (M03), ProgressEntry (M04), CostLedgerEntry (M06)
          Calculates: EVMSnapshot for every WBS node + PackageEVMRollup + ProjectEVMSummary
          Sets: EVMSnapshot.data_source = Historical_Seed (or Mixed_Seed if some live data exists)

Step 5: Statistical engine activation check
        After all periods processed:
          Count confirmed EVM periods (including seed)
          Update ProjectEVMSummary.statistical_engine_status
          If ≥ 6: Holt's + OLS activate
          If ≥ 8: SPC activates
          NarrativeGeneration: queued for all seed periods + current period

Step 6: Session completion record
        HistoricalDataImportSession.records_imported populated
        HistoricalDataImportSession.statistical_engine_activated populated
        PMO Director notification: "HDI complete. {N} periods imported.
        Statistical engine: {status}. Review EVM dashboard to verify."
```

---

## SECTION 8 — Post-Import Behaviour

### Data Visibility

- Seed records appear in all EPCC views identically to live records
- They are visually distinguished by a badge: `📂 SEED` (or similar indicator) in data tables
- EVM trend charts show seed periods in a lighter shade with a legend note
- All metrics derived from seed periods carry the "Includes historical seed data" disclaimer per §7.110

### Correction Protocol (Within 7-Day Error Window)

If PMO Director identifies errors in imported data within 7 days of import:

```
1. PMO Director reports error to System Admin with specific records
2. System Admin creates a correction batch:
   - Soft-deletes the incorrect seed records (is_active = false)
   - Creates replacement records (data_source = Historical_Seed, correction = true)
   - Logs every correction in AuditLog with business_event = "HDI_CORRECTION"
3. RecalcQueue: STANDARD job for affected periods
4. PMO Director confirms corrections are accurate
```

After 7 days: corrections require a formal Governance Change Request (PMO Director + System Admin joint approval).

### Statistical Engine After Import

| Periods Imported | Engine Status | Predictive Capability |
|-----------------|---------------|----------------------|
| 1–5 periods | Insufficient_Data | No predictive alerts. Trend charts shown but labeled "insufficient history". |
| 6–7 periods | Tier1_Active | Holt's ES + OLS active. Predictive alerts on. SPC pending 2+ more periods. |
| ≥ 8 periods | Full_Active | All three tiers. Full predictive capability. Alerts use normal confidence levels. |
| 13 periods (KDMC example) | Full_Active | Holt's auto-optimised. OLS high confidence (R² meaningful). SPC limits meaningful. |

---

## SECTION 9 — Cross-Module data_source Field Implementation

Every entity that can receive HDI data must have `data_source` added to its schema:

| Module | Entity | Field Added |
|--------|--------|------------|
| M03 | PVProfile | `data_source ENUM(Live_EPCC, Historical_Seed)` DEFAULT Live_EPCC |
| M04 | ProgressEntry | `data_source ENUM(Live_EPCC, Historical_Seed)` DEFAULT Live_EPCC |
| M06 | CostLedgerEntry | `data_source ENUM(Live_EPCC, Historical_Seed)` DEFAULT Live_EPCC |
| M07 | EVMSnapshot | `data_source ENUM(Live_EPCC, Historical_Seed, Mixed_Seed)` CALC |
| M08 | GatePassage | `data_source ENUM(Live_EPCC, Historical_Seed)` DEFAULT Live_EPCC |
| M05 | VariationOrder | `data_source ENUM(Live_EPCC, Historical_Seed)` DEFAULT Live_EPCC |

**Migration requirement:** These fields are added via Alembic migration before HDI feature is activated. Default = Live_EPCC ensures all existing records are correctly classified without data modification.

---

## SECTION 10 — Open Questions

**All questions resolved. Zero open questions.**

| # | Question | Resolution |
|---|----------|-----------|
| 1 | Should HDI support weekly/daily granularity or monthly only? | Monthly only for v1.0. The statistical engine is designed for monthly periods (KDMC standard). Weekly granularity HDI is Phase 2 enhancement when a project uses weekly reporting. |
| 2 | What if WBS structure changes between historical period and current? | HDI validates against the current M02 WBS structure. If historical WBS codes don't match current codes, they fail validation. PMO Director must either: (a) create the historical WBS nodes in M02 before import, or (b) map historical codes to current codes manually in the CSV. |
| 3 | Can HDI be used to load data for a project that just started (no prior history)? | No. If the project has no prior history outside EPCC, HDI is not needed or useful. HDI is specifically for projects migrating to EPCC from prior manual tracking. |
| 4 | What if the imported data contradicts data already in EPCC? | Pre-import validation detects conflicts with existing live records. If live records exist for a period being imported: validation returns ERROR — "Live EPCC record exists for period {YYYY-MM} for WBS {code}. Cannot seed over live data." PMO Director must delete the conflicting live records first (with approval). |
