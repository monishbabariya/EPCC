# M04 — Execution Capture
## Module Specification v2.2
## AMENDMENT — Changed Blocks Only
**Status:** Draft — Pending Review | **Locked:** No
**Spec Author:** PMO Director | **Date:** 2026-05-02
**Reference Standards:** EPCC_Standards_Memory_v5_1.md
**Base Version:** M04_Execution_Capture_v2.1
**Amendment Scope:** GAP-07: DLPRegister entity. DLPDefect entity.
                     DLP NCR sub-type distinction from construction NCRs.
                     SG-11 activation signal receipt. DLP retention signal to M06.

---

## CHANGE LOG

| Version | Date | Change Summary |
|---------|------|---------------|
| v2.0 | 2026-04-30 | Full spec |
| v2.1 | 2026-05-02 | GAP-03: ProgressEntryApproval two-state model |
| v2.2 | 2026-05-02 | GAP-07: DLPRegister + DLPDefect entities. BR-04-038 through BR-04-046 added. SG-11 signal reception. Open defect count signal to M06. |

---

## BLOCK 2 — Scope Boundary (Updated)

**ADDITIONS to INCLUDES:**

| INCLUDES (New) | Rationale |
|----------------|-----------|
| `DLPRegister` — DLP period tracking per project, activated at SG-11 | GAP-07: No dedicated DLP tracking existed |
| `DLPDefect` — individual defect records during DLP period, sub-type of NCR concept | GAP-07 |
| DLP defect rectification workflow — response, rectification, reinspection, closure | GAP-07 |
| Open defect count signal to M06 — blocks DLP retention release when defects unresolved | GAP-07 |
| DLP activation signal receipt from M08 SG-11 passage | GAP-07 |

**ADDITION to EXCLUDES:**

| EXCLUDES (Clarification) |
|--------------------------|
| DLP retention release decision → M06 owns retention. M04 provides open_defect_count signal only. |
| NABH compliance observations during DLP → M09 owns DLPComplianceObservation |
| DLP start date authority → M08 SG-11 passage is the sole trigger. M04 cannot self-activate. |

---

## BLOCK 3 — Data Architecture (Amendment)

### 3a. New Entities

| Entity | Description | Cardinality |
|--------|-------------|-------------|
| `DLPRegister` | **(NEW v2.2)** DLP period master record per project. Activated by SG-11 passage signal from M08. Tracks DLP period dates, total and open defect counts, and retention release eligibility. | 1 per project |
| `DLPDefect` | **(NEW v2.2)** Individual defect identified during DLP period. Sub-type of the NCR concept with different commercial rules: no LD, contractor's own cost, no gate blocking, but blocks retention release. | Many per project |

---

### 3b. New Entity Fields — `DLPRegister`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `dlp_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | FK → M01 Project. Unique per project. | LINK → M01 Project |
| `contract_id` | UUID | Y | FK → M01 Contract (primary contract). | LINK → M01 Contract |
| `sg11_passage_id` | UUID | Y | FK → M08 GatePassage (SG-11). Immutable. Source of dlp_start_date. | LINK → M08 GatePassage |
| `dlp_start_date` | DATE | Y | = SG-11 GatePassage.actual_passage_date. Populated on M08 activation signal. | LINK → M08 GatePassage |
| `dlp_term_days` | INTEGER | Y | LINK → M01 Contract.dlp_term_days. Copied at activation — immutable on DLPRegister. | LINK → M01 Contract |
| `dlp_end_date` | DATE | Y | CALC = dlp_start_date + dlp_term_days | CALC |
| `status` | ENUM | Y | `Not_Started / Active / Closed` | SYSTEM |
| `total_defects_raised` | INTEGER | Y | CALC — count of all DLPDefect records for this project | CALC |
| `open_defect_count` | INTEGER | Y | CALC — count where defect_status ≠ Closed | CALC |
| `critical_open_count` | INTEGER | Y | CALC — count where defect_severity = Critical AND defect_status ≠ Closed | CALC |
| `high_open_count` | INTEGER | Y | CALC — count where defect_severity = High AND defect_status ≠ Closed | CALC |
| `retention_release_eligible` | BOOLEAN | Y | CALC = (open_defect_count = 0 AND today ≥ dlp_end_date) | CALC |
| `activated_by` | UUID | N | FK → Users. Auto-populated from M08 gate passage approver. | LINK → M08 GatePassage |
| `activated_at` | TIMESTAMP | N | Populated when status → Active | SYSTEM |
| `closed_at` | TIMESTAMP | N | Populated when status → Closed | SYSTEM |
| `closed_by` | UUID | N | FK → Users. PMO Director on closure. | INPUT (PMO Director) |
| `closure_note` | TEXT | N | Required if closed_by populated and open_defect_count > 0 (override closure). Min 200 chars. | INPUT |

**Activation Rule:**
```
DLPRegister.status = Not_Started until SG-11 GatePassage signal received from M08.
M04 CANNOT self-activate DLPRegister.
On SG-11 signal: status → Active, dates populated, M06 notified.
PMO Director cannot manually activate — only SG-11 gate passage triggers it.
```

---

### 3b. New Entity Fields — `DLPDefect`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `defect_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | LINK → M01 Project |
| `dlp_id` | UUID | Y | FK → DLPRegister. Cannot create DLPDefect if DLPRegister.status ≠ Active. | LINK → DLPRegister |
| `defect_code` | VARCHAR(20) | Y | System-generated. Format: DLP-{project_seq_pad3}. e.g., DLP-001. | SYSTEM |
| `wbs_id` | UUID | Y | Location of defect. FK → M02 WBSNode. | LINK → M02 WBSNode |
| `package_id` | UUID | Y | FK → M02 Package. | LINK → M02 Package |
| `contract_id` | UUID | Y | Which contractor is responsible. FK → M01 Contract. | INPUT (dropdown) |
| `description` | TEXT | Y | Min 50 chars. Specific description of the defect. | INPUT |
| `defect_type` | ENUM | Y | `Structural / Architectural / MEP_Mechanical / MEP_Electrical / MEP_Plumbing / Medical_Gas / Fire_Safety / Finishes / Equipment / Other` | INPUT (dropdown) |
| `defect_severity` | ENUM | Y | `Critical / High / Medium / Low` | INPUT (dropdown) |
| `date_observed` | DATE | Y | Date defect was found. Cannot be before dlp_start_date. | INPUT |
| `observed_by` | UUID | Y | FK → Users. Who identified the defect. | INPUT |
| `photographic_evidence_url` | VARCHAR(500) | N | Data Lake URL(s) — JSONB array of photo URLs. Mandatory for Critical/High. | INPUT |
| `rectification_required` | TEXT | Y | Min 30 chars. Description of required fix. | INPUT |
| `contractor_response_due` | DATE | Y | CALC: Critical/High = date_observed + 3 days. Medium/Low = date_observed + 7 days. | CALC |
| `contractor_response` | TEXT | N | Contractor's proposed rectification method. Required before defect_status → Rectification_In_Progress. | INPUT |
| `contractor_response_date` | DATE | N | Date contractor submitted response | INPUT |
| `rectification_planned_start` | DATE | N | Contractor's planned start of rectification work | INPUT |
| `rectification_actual_start` | DATE | N | Actual date rectification began | INPUT |
| `rectification_completion_declared` | DATE | N | Date contractor declares rectification done | INPUT |
| `reinspection_required` | BOOLEAN | Y | Default true. Can only be false for very minor cosmetic items — PMO Director override required. | INPUT |
| `reinspection_scheduled_date` | DATE | N | Date PMO/QA team will inspect. Required before status → Reinspection_Pending. | INPUT |
| `reinspection_date` | DATE | N | Actual reinspection date | INPUT |
| `reinspection_result` | ENUM | N | `Pass / Fail / Partial` | INPUT (Project Director or QA) |
| `reinspection_notes` | TEXT | N | Mandatory if reinspection_result = Fail or Partial (min 30 chars). | INPUT |
| `defect_status` | ENUM | Y | `Open / Response_Pending / Rectification_In_Progress / Reinspection_Pending / Closed / Disputed` | SYSTEM |
| `closed_at` | TIMESTAMP | N | Auto on status → Closed (reinspection_result = Pass) | SYSTEM |
| `closed_by` | UUID | N | FK → Users (Project Director or PMO Director who confirmed closure) | INPUT |
| `nabh_observation_link` | UUID | N | FK → M09 DLPComplianceObservation if this defect is also an NABH non-compliance. | LINK → M09 |
| `is_disputed` | BOOLEAN | Y | Default false. Set true when contractor disputes liability. | INPUT |
| `dispute_resolution_note` | TEXT | N | Min 50 chars. Required if is_disputed = true. | INPUT |

**Commercial Difference from Construction NCR (explicit):**
```
CONSTRUCTION NCR (existing NCR entity in M04):
  Period:        During construction (pre-SG-11)
  LD impact:     Yes — critical NCRs contribute to LD calculation in M05
  Gate blocking: Yes — critical/high NCRs block assigned gate in M08
  Cost:          Contractor remediation cost tracked in M06 CostLedgerEntry
  Lifecycle:     Open → Response → Remediation → Re_Inspection → Closed

DLP DEFECT (DLPDefect entity — this v2.2 addition):
  Period:        During DLP period (post-SG-11, pre-DLP end date)
  LD impact:     NO — LD period ended at SG-11
  Gate blocking: NO — all gates already passed at SG-11
  Cost:          Contractor's own liability (no M06 cost entry from contractor)
                 Exceptional case: if contractor refuses → EPCC tracks dispute only
  Retention:     YES — unresolved defects block DLP retention release in M06
  Lifecycle:     Open → Response_Pending → Rectification_In_Progress →
                 Reinspection_Pending → Closed (or Disputed)
```

---

## BLOCK 6 — Business Rules (Amendment — new rules v2.2)

*All existing rules BR-04-001 through BR-04-037 from v2.1 remain in force.*

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---------|---------|-------|--------|------------|
| BR-04-038 | M08 SG-11 gate passage signal received | DLP activation signal: {project_id, sg11_passage_id, dlp_start_date} | Create DLPRegister (status → Active). Populate dlp_start_date, dlp_end_date, dlp_term_days. Send M06 activation signal: {project_id, dlp_start_date, dlp_end_date}. Send M09 signal: DLP phase active. PMO Director in-app notification: "DLP activated for {project_code}. Period: {start} to {end}." | 🔴 Real-time |
| BR-04-039 | DLPDefect created | defect_code auto-generated. dlp_start_date check. | Validate: date_observed ≥ DLPRegister.dlp_start_date. Validate: DLPRegister.status = Active (cannot raise DLPDefect before SG-11 or after DLP closed). Auto-generate defect_code. DLPRegister.total_defects_raised + 1. DLPRegister.open_defect_count + 1. Signal to M06: updated open_defect_count. | 🔴 Real-time |
| BR-04-040 | DLPDefect — contractor response overdue | contractor_response_due < today AND defect_status = Open or Response_Pending | Decision Queue item: trigger_type = DLP_RESPONSE_OVERDUE, severity = HIGH (Critical/High defects) or MEDIUM (Medium/Low), owner = Project Director, SLA = 24hr. | 🟡 2-4hr |
| BR-04-041 | DLPDefect — Critical/High severity — photo evidence check | defect_severity = Critical or High on save | Validate: photographic_evidence_url is not null (at least 1 photo uploaded). Block save if missing. Error: "Critical/High DLP defects require photographic evidence." | 🔴 Real-time |
| BR-04-042 | DLPDefect status → Closed | reinspection_result = Pass | Update DLPRegister.open_defect_count − 1. Recalculate retention_release_eligible. If now eligible: signal to M06 (open_defect_count = 0). If nabh_observation_link populated: signal to M09 to update DLPComplianceObservation status. | 🔴 Real-time |
| BR-04-043 | DLPDefect reinspection_result = Fail or Partial | Reinspection done but defect not resolved | defect_status remains Rectification_In_Progress. New contractor_response_due set: date_of_failed_reinspection + original severity SLA. Decision Queue item: DLP_REINSPECTION_FAILED, severity = HIGH, owner = Project Director. | 🔴 Real-time |
| BR-04-044 | DLPRegister.open_defect_count changes | Any DLPDefect status change | Recalculate retention_release_eligible. Send updated open_defect_count to M06 (🔴 Real-time signal). If newly eligible: notify Finance Lead (DLP retention release now possible). If new defect opens: notify Finance Lead (DLP retention release now blocked). | 🔴 Real-time |
| BR-04-045 | DLP period end date reached (today = dlp_end_date) | Scheduled daily check | If open_defect_count > 0: Alert to PMO Director + Project Director: "DLP period expired with {N} open defects. Retention release blocked." Decision Queue item: DLP_EXPIRED_WITH_OPEN_DEFECTS, severity = CRITICAL. If open_defect_count = 0: notify Finance Lead: "DLP period closed. Retention release eligible." | 🟢 24hr |
| BR-04-046 | DLPDefect raised after dlp_end_date | date_observed > DLPRegister.dlp_end_date | BLOCK creation. Error: "DLP period ended {date}. DLP defects cannot be raised after DLP period expiry. Use standard NCR process or post-DLP warranty claim register." Warranty claims are outside EPCC scope — informational message only. | 🔴 Real-time |

---

## BLOCK 7 — Integration Points (Amendment)

| Direction | Module | Data Exchanged | Trigger | Speed Tier |
|-----------|--------|---------------|---------|------------|
| RECEIVES FROM | M08 Gate Control | **(NEW v2.2)** DLP activation signal: project_id, sg11_passage_id, dlp_start_date | On SG-11 gate passage | 🔴 Real-time |
| SENDS TO | M06 Financial Control | **(NEW v2.2)** DLPRegister.open_defect_count (updated on every defect status change) | On BR-04-044 | 🔴 Real-time |
| SENDS TO | M06 Financial Control | **(NEW v2.2)** DLP activation signal: dlp_start_date, dlp_end_date (forwarded from M08) | On BR-04-038 | 🔴 Real-time |
| SENDS TO | M09 Compliance Tracker | **(NEW v2.2)** DLP phase active signal. Defect closure signals (nabh_observation_link). | On DLPRegister activation and DLPDefect closure | 🔴 Real-time |
| RECEIVES FROM | M06 Financial Control | **(NEW v2.2)** DLPRegister.status → Closed signal (retention released) | On M06 DLP retention release completion | 🔴 Real-time |
| SENDS TO | M07 EVM Engine | pct_complete_reported per WBS node (unchanged) | On Approved progress entry | 🔴 Real-time |

---

## BLOCK 9 — Explicit Exclusions (Amendment — additions)

```
[ ] Trigger DLP start independently            → Only M08 SG-11 passage activates DLPRegister
[ ] Calculate DLP retention amounts            → M06 owns retention; M04 signals open count
[ ] Track NABH DLP compliance observations     → M09 owns DLPComplianceObservation
[ ] Calculate LD from DLP defects              → No LD during DLP period (post-SG-11)
[ ] Block future gates from DLP defects        → No gates after SG-11; gate blocking irrelevant
[ ] Track warranty claims post-DLP             → Outside EPCC scope
```

---

## BLOCK 10 — Open Questions

**All questions resolved. Zero open questions.**

| # | Question | Resolution |
|---|----------|-----------|
| 1 | Can a DLPDefect be raised before SG-11? | No. BR-04-039 validates date_observed ≥ dlp_start_date and DLPRegister.status = Active. Pre-SG-11 quality issues are Construction NCRs (existing entity). |
| 2 | What if the same physical issue appears as both a construction NCR and a DLP defect? | They are separate records in separate entities. If a construction NCR was "Closed" but the defect reappears during DLP, a new DLPDefect is raised. The two records may cross-reference via notes field, but they are distinct records with different commercial implications. |
| 3 | Who can close a DLPDefect? | Project Director or PMO Director. Site Manager can submit defects but cannot close them. Closure requires reinspection_result = Pass, which requires a formal inspection. |
| 4 | If the contractor disputes a defect, does it still count as open for retention purposes? | Yes. `is_disputed = true` does not remove the defect from open_defect_count. Disputed defects continue to block retention until either (a) dispute resolved and defect closed, or (b) PMO Director override with legal settlement note (BR-06-045 in M06). |
