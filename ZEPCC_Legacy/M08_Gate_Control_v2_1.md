# M08 — Gate Control
## Module Specification v2.1
## AMENDMENT — Changed Blocks Only
**Status:** Draft — Pending Review | **Locked:** No
**Spec Author:** PMO Director | **Date:** 2026-05-02
**Reference Standards:** EPCC_Standards_Memory_v5_1.md
**Base Version:** M08_Gate_Control_v2.0
**Amendment Scope:** GAP-05: TCPI infeasibility signal wired to GateHealthReview.
                     GAP-13: SFFC substitution for MILP stub.
                     SG-11 DLP activation trigger added.
                     BAC integrity check added as gate criterion (GAP-02 downstream).

---

## CHANGE LOG

| Version | Date | Change Summary |
|---------|------|---------------|
| v2.0 | 2026-04-30 | Block 10 resolved: pre-project hybrid gate modes; Conditional GO deadline; interface templates; configurable authority |
| v2.1 | 2026-05-02 | GAP-05: GateHealthReview entity + TCPI/CPI/SPI signal reception + recovery tracking. GAP-13: SFFC entity substitutes MILP stub for SG-2/SG-3. SG-11: DLP activation trigger. GAP-02 downstream: BAC integrity as SG-7+ criterion. |

---

## BLOCK 2 — Scope Boundary (Updated)

**ADDITIONS to INCLUDES:**

| INCLUDES (New) | Rationale |
|----------------|-----------|
| `GateHealthReview` — systemic performance crisis review triggered by EVM signals | GAP-05: TCPI infeasibility and chronic RAG = Red force formal PMO review |
| Recovery plan tracking per GateHealthReview | GAP-05 |
| SFFC (Simplified Financial Feasibility Calculator) inputs + outputs for SG-2/SG-3 | GAP-13: operational substitute until MILP engine built |
| SG-11 DLP activation trigger → M04 DLPRegister | GAP-07 downstream |
| BAC integrity criterion at SG-7 and above | GAP-02 downstream |

**ADDITION to EXCLUDES:**

| EXCLUDES (Clarification) |
|--------------------------|
| EVM recalculation or TCPI calculation → M07 |
| DLP defect management → M04 |
| DLP retention release decisions → M06 |

---

## BLOCK 3 — Data Architecture (Amendment)

### 3a. New Entities

| Entity | Description | Cardinality |
|--------|-------------|-------------|
| `GateHealthReview` | **(NEW v2.1)** Formal review record triggered by systemic EVM performance signals. Not an override. Documents PMO Director's response and recovery plan. | Many per project (one per signal event) |
| `SFCInput` | **(NEW v2.1)** Simplified Financial Feasibility Calculator inputs and outputs for SG-2/SG-3. Replaces MILPGateInput stub operationally. Both entities coexist — SFCInput activates when milp_run_id is null. | 1 per SG-2 and SG-3 per project |

---

### 3b. New Entity Fields — `GateHealthReview`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `gate_health_review_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | LINK → M01 Project |
| `current_gate_code` | VARCHAR(10) | Y | Gate active when review triggered. e.g., SG-7 | LINK → StageGate |
| `current_gate_id` | UUID | Y | FK → StageGate | LINK → StageGate |
| `trigger_source` | ENUM | Y | `M07_TCPI / M07_CPI_Critical / M07_SPI_Critical_Late` | SYSTEM |
| `trigger_metric` | VARCHAR(20) | Y | e.g., "tcpi", "cpi", "spi" | SYSTEM |
| `trigger_value` | DECIMAL(8,4) | Y | Actual metric value at trigger | LINK → M07 |
| `trigger_threshold` | DECIMAL(8,4) | Y | Threshold that was breached: TCPI=1.20, CPI=0.75, SPI=0.70 | SYSTEM |
| `trigger_period` | DATE | Y | M07 reporting period that generated the signal | LINK → M07 |
| `consecutive_count` | INTEGER | Y | Count of consecutive unresolved GateHealthReviews for this project | CALC |
| `status` | ENUM | Y | `Open / Responded / Under_Remediation / Resolved / Escalated_To_Board` | SYSTEM |
| `decision_queue_id` | UUID | Y | FK → DecisionQueueItem (CRITICAL, 24hr SLA) | LINK → DecisionQueueItem |
| `pmo_response_by` | UUID | N | FK → Users. Mandatory on Responded status. | INPUT (PMO Director) |
| `pmo_responded_at` | TIMESTAMP | N | Auto on status transition to Responded | SYSTEM |
| `root_cause` | TEXT | N | Min 100 chars. Mandatory before status → Responded. | INPUT (PMO Director) |
| `recovery_plan` | TEXT | N | Min 200 chars. Concrete actions, owners, deadlines. Mandatory before status → Responded. | INPUT (PMO Director) |
| `recovery_decision` | ENUM | N | `Continue_With_Remediation / Scope_Reduction / Timeline_Extension / Escalate_To_Board` | INPUT (PMO Director) |
| `constraint_log_id` | UUID | N | FK → ConstraintLog — recovery plan tracked as active constraint | LINK → ConstraintLog |
| `resolved_period` | DATE | N | Reporting period when trigger metric returned to safe range | LINK → M07 |
| `resolved_at` | TIMESTAMP | N | Auto when status → Resolved | SYSTEM |
| `board_escalation_date` | TIMESTAMP | N | Auto on consecutive_count ≥ 3 or recovery_decision = Escalate_To_Board | SYSTEM |

---

### 3b. New Entity Fields — `SFCInput` (SFFC — GAP-13 Resolution)

*(Simplified Financial Feasibility Calculator — operational substitute for MILP until engine built)*

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `sfc_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `gate_id` | UUID | Y | SG-2 or SG-3 only | LINK → StageGate |
| `project_id` | UUID | Y | — | LINK → M01 Project |
| `gate_code` | ENUM | Y | `SG-2 / SG-3` | LINK → StageGate |
| `project_cost_estimate` | DECIMAL(15,2) | Y | Total project cost — P80 from M05 Monte Carlo preferred. Manual if MC not run. | INPUT (Finance Lead) |
| `cost_source` | ENUM | Y | `M05_Monte_Carlo_P80 / Manual_Estimate` | INPUT |
| `annual_revenue_year1` | DECIMAL(15,2) | Y | Year 1 projected revenue | INPUT (Finance Lead) |
| `revenue_growth_rate_pct` | DECIMAL(6,4) | Y | Annual revenue growth rate. Range 0–0.30. | INPUT |
| `operating_cost_ratio` | DECIMAL(6,4) | Y | OpEx as ratio of revenue. Range 0.20–0.90. | INPUT |
| `discount_rate` | DECIMAL(6,4) | Y | WACC or hurdle rate. Min 0.08 (8%). | INPUT |
| `debt_proportion` | DECIMAL(6,4) | Y | Fraction of project cost funded by debt. Range 0–0.80. | INPUT |
| `debt_interest_rate` | DECIMAL(6,4) | N | Annual interest rate. Required if debt_proportion > 0. | INPUT |
| `debt_tenure_years` | INTEGER | N | Loan repayment period. Required if debt_proportion > 0. | INPUT |
| `projection_years` | INTEGER | Y | DCF horizon. Default 15. Range 10–25. | INPUT |
| `irr` | DECIMAL(8,4) | N | CALC — Internal Rate of Return | CALC |
| `npv` | DECIMAL(15,2) | N | CALC — Net Present Value at discount_rate | CALC |
| `payback_years` | DECIMAL(5,2) | N | CALC — Simple payback period | CALC |
| `dscr_year1` | DECIMAL(6,4) | N | CALC — Debt Service Coverage Ratio Year 1 | CALC |
| `dscr_minimum` | DECIMAL(6,4) | N | CALC — Minimum DSCR across projection period | CALC |
| `worst_case_viable` | BOOLEAN | N | CALC — IRR > discount_rate under P90 cost scenario | CALC |
| `irr_passes` | BOOLEAN | N | CALC = irr > discount_rate | CALC |
| `npv_passes` | BOOLEAN | N | CALC = npv > 0 | CALC |
| `dscr_passes` | BOOLEAN | N | CALC = dscr_minimum ≥ 1.25 | CALC |
| `overall_sfc_pass` | BOOLEAN | Y | CALC = irr_passes AND npv_passes AND worst_case_viable AND (dscr_passes OR debt_proportion = 0) | CALC |
| `financial_model_url` | VARCHAR(500) | N | Data Lake URL — supporting DCF model document | INPUT |
| `entered_by` | UUID | Y | Finance Lead | SYSTEM |
| `entered_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `approved_by` | UUID | N | PMO Director approval required before SG-2/SG-3 gate review | INPUT (PMO Director) |
| `approved_at` | TIMESTAMP | N | Auto on approval | SYSTEM |

**SFC vs MILP relationship:**
```
MILPGateInput.milp_run_id = null (stub) → System uses SFCInput.overall_sfc_pass for gate criterion
MILPGateInput.milp_run_id = populated   → System uses MILPGateInput.overall_milp_pass
SFCInput is deactivated when MILP engine is live and milp_run_id is populated
Both entities coexist — no data migration needed when MILP engine comes online
```

---

### 3b. Updated Fields — `StageGate` (v2.1 additions)

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `dlp_activation_triggered` | BOOLEAN | Y | **(NEW)** Default false. Set true on SG-11 passage. | SYSTEM |
| `dlp_activation_sent_at` | TIMESTAMP | N | **(NEW)** Timestamp when DLP activation signal sent to M04. | SYSTEM |
| `active_health_review_id` | UUID | N | **(NEW)** FK → GateHealthReview. Populated when an Open or Under_Remediation review exists. | LINK → GateHealthReview |
| `health_review_blocks_go` | BOOLEAN | Y | **(NEW)** True when active_health_review_id is set AND pmo_responded_at is null (unacknowledged). | CALC |

---

### 3b. Updated Fields — `GateCriterion` (v2.1 — new category value)

ENUM update for `criterion_category` — add: `BAC_Integrity` (new value)

This enables BAC integrity status to be a system-verifiable gate criterion:
- `criterion_category = BAC_Integrity`
- `verification_module = M02`
- `verification_field = Package.bac_integrity_status`
- `pass_condition = all packages Confirmed`

---

## BLOCK 6 — Business Rules (Amendment — new rules v2.1)

*All existing rules BR-08-001 through BR-08-034 from v2.0 remain in force.*
*The following rules are ADDED in v2.1:*

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---------|---------|-------|--------|------------|
| BR-08-035 | M07 sends `tcpi_infeasibility_alert` (TCPI > 1.20) | Received via integration event | Create `GateHealthReview` (trigger_source = M07_TCPI). Create `DecisionQueueItem` (CRITICAL, 24hr SLA, PMO Director). Set `StageGate.active_health_review_id`. Set `health_review_blocks_go = true` until PMO Director responds. Notify all channels (Critical override — cannot opt out). | 🟡 2-4hr |
| BR-08-036 | M07 sends CPI_Critical signal (CPI < 0.75, 3 consecutive periods) | Received via integration event | Create `GateHealthReview` (trigger_source = M07_CPI_Critical). Same Decision Queue + notification as BR-08-035. | 🟡 2-4hr |
| BR-08-037 | M07 sends SPI_Critical_Late signal (SPI < 0.70 AND pct_time_elapsed > 75%) | Received via integration event | Create `GateHealthReview` (trigger_source = M07_SPI_Critical_Late). Same Decision Queue + notification as BR-08-035. | 🟡 2-4hr |
| BR-08-038 | GateHealthReview SLA: 24hr elapsed without PMO Director response | System check | Governance breach logged. `GateHealthReview.status` remains Open. Portfolio Manager notified. Badge on M10: "HEALTH REVIEW OVERDUE — {project_code}". | 🟡 2-4hr |
| BR-08-039 | PMO Director submits GateHealthReview response | root_cause + recovery_plan + recovery_decision populated | Validate: root_cause ≥ 100 chars, recovery_plan ≥ 200 chars. Set status = Responded. Create `ConstraintLog` entry (constraint_type = TCPI_Recovery, severity = Critical, owner = PMO Director). Set `health_review_blocks_go = false`. Decision Queue item resolved. M10 badge: switches from RECOVERY REVIEW REQUIRED → UNDER REMEDIATION. | 🔴 Real-time |
| BR-08-040 | GateHealthReview — M07 confirms metric returned to safe range | TCPI ≤ 1.20 for 1 period after recovery | Set status = Resolved. resolved_period populated. ConstraintLog entry closed. M10 badge cleared. Active_health_review_id cleared on StageGate. | 🟡 2-4hr |
| BR-08-041 | consecutive_count ≥ 3 (three consecutive unresolved GateHealthReviews) | Auto-check on new GateHealthReview creation | Set status = Escalated_To_Board. board_escalation_date populated. Create DecisionQueueItem: CRITICAL, owner = PMO Director, SLA = 12hr, trigger_type = BOARD_ESCALATION_REQUIRED. Portfolio Manager also notified. | 🔴 Real-time |
| BR-08-042 | Gate review attempted while health_review_blocks_go = true | PMO Director triggers gate review | Gate review CAN proceed (do not block gate review initiation). But gate CANNOT pass to GO or Conditional_GO status. Gate verdict capped at STOP until PMO Director acknowledges GateHealthReview. Display: "Gate blocked: Unacknowledged performance review. Add GateHealthReview response to proceed." | 🔴 Real-time |
| BR-08-043 | SG-7+ gate — BAC integrity criterion check | GateCriterionCheck auto-check | criterion_category = BAC_Integrity. Fetch M02 Package.bac_integrity_status for all project packages. Pass = ALL packages Confirmed. Fail = ANY package Stale_Pending_VO. If Fail: gate cannot achieve GO status. | 🔴 Real-time |
| BR-08-044 | SG-2 or SG-3 gate review — SFFC check | milp_run_id = null (MILP not live) | System checks SFCInput for this gate. If no SFCInput record: gate criterion = Fail (SFFC_Missing). If SFCInput exists but not PMO Director approved: gate criterion = Fail. If SFCInput.overall_sfc_pass = true AND approved: gate criterion = Pass. | 🔴 Real-time |
| BR-08-045 | SG-11 gate passes (actual_passage_date populated, status = Passed) | GatePassage.gate_code = SG-11 | Send DLP activation signal to M04: {project_id, sg11_passage_id, dlp_start_date = passage_date}. Set `StageGate.dlp_activation_triggered = true`. Set `StageGate.dlp_activation_sent_at = NOW()`. | 🔴 Real-time |

---

### Updated Rule — BR-08-018 (EVM RAG handling — extended for GateHealthReview)

```
BR-08-018 (EVM RAG = Red) — Updated in v2.1:
  Existing behaviour (unchanged):
    M07 sends rag_overall = Red → GateCriterionCheck for EVM criterion → Fail.

  New behaviour (v2.1):
    If rag_overall = Red for 3 consecutive periods:
      → Also triggers BR-08-036 (CPI_Critical GateHealthReview)
    These are separate consequences — the gate criterion fail and the health review
    are not mutually exclusive. Both apply simultaneously.

  Plain language: A Red RAG blocks the gate AND forces a formal health review if it persists.
```

---

### Updated Decision Queue Trigger Table (v2.1 additions to Block 3c)

| Trigger Condition | Decision Type | Owner | SLA | Escalation |
|-----------------|--------------|-------|-----|-----------|
| TCPI > 1.20 received from M07 | Gate Health Review (TCPI) | PMO Director | 24 hrs | 24hr → Portfolio Manager + governance breach |
| CPI < 0.75 for 3 periods from M07 | Gate Health Review (CPI) | PMO Director | 24 hrs | Same |
| SPI < 0.70 late-stage from M07 | Gate Health Review (SPI) | PMO Director | 24 hrs | Same |
| 3 consecutive unresolved reviews | Board Escalation Required | PMO Director | 12 hrs | Immediate Portfolio Manager |
| SFCInput missing for SG-2/SG-3 | SFFC_Missing gate criterion | Finance Lead | 48 hrs | 72hr → PMO Director |
| BAC integrity fail at SG-7+ | BAC integrity criterion fail | QS Manager | 48 hrs | 72hr → PMO Director |

---

## BLOCK 7 — Integration Points (Amendment)

| Direction | Module | Data Exchanged | Trigger | Speed Tier |
|-----------|--------|---------------|---------|------------|
| RECEIVES FROM | M07 EVM Engine | **(NEW v2.1)** `tcpi_infeasibility_alert` (TCPI > 1.20) | After EVM recalculation (BR-07-033 in M07) | 🟡 2-4hr |
| RECEIVES FROM | M07 EVM Engine | **(NEW v2.1)** `cpi_critical_signal` (CPI < 0.75, 3 consecutive periods) | After EVM recalculation | 🟡 2-4hr |
| RECEIVES FROM | M07 EVM Engine | **(NEW v2.1)** `spi_critical_late_signal` (SPI < 0.70, pct_time_elapsed > 75%) | After EVM recalculation | 🟡 2-4hr |
| RECEIVES FROM | M02 Structure & WBS | **(NEW v2.1)** `bac_integrity_status` per package (for SG-7+ gate criterion check) | On BAC integrity status change | 🔴 Real-time |
| SENDS TO | M04 Execution Capture | **(NEW v2.1)** DLP activation signal: project_id + sg11_passage_id + dlp_start_date | On SG-11 gate passage (BR-08-045) | 🔴 Real-time |
| SENDS TO | M10 EPCC Command | **(NEW v2.1)** GateHealthReview status + badge type (RECOVERY REVIEW REQUIRED / UNDER REMEDIATION / OVERDUE) | On GateHealthReview creation + status change | 🟡 2-4hr |
| SENDS TO | M05 Risk & Change | `change_event_id` — on gate reopen (unchanged) | On gate reopen | 🔴 Real-time |
| RECEIVES FROM | M09 Compliance | Compliance status per regulatory item for gate criteria (unchanged) | On compliance status change | 🔴 Real-time |

---

## BLOCK 9 — Explicit Exclusions (Amendment — additions)

```
[ ] Calculate TCPI, CPI, or SPI                              → M07
[ ] Initiate EVM recalculation                               → RecalcQueue service
[ ] Override gate decisions based on GateHealthReview        → GateHealthReview is advisory
[ ] Manage DLP defects or DLP rectification                  → M04
[ ] Process DLP retention release payment                    → M06
[ ] Run Monte Carlo or financial feasibility modelling       → M05 (Monte Carlo), SFFC (Python engine)
[ ] Write back to M07 EVM data                               → M08 is read-only consumer of M07
```

---

## BLOCK 10 — Open Questions

**All questions resolved. Zero open questions.**

| # | Question | Resolution |
|---|----------|-----------|
| 1 | Does GateHealthReview block the gate? | Only blocks GO/Conditional_GO if PMO Director has NOT acknowledged (responded) within 24hr SLA. Once responded, gate can proceed to GO. Review does not permanently block gates. |
| 2 | SFFC vs MILP — coexistence? | SFCInput activates when milp_run_id = null. MILPGateInput takes over when MILP engine is live. Both entities coexist. No migration needed. |
| 3 | Can a project have multiple simultaneous GateHealthReviews? | Yes — TCPI, CPI, and SPI are separate triggers. Each creates its own review. Consecutive_count applies per-trigger-type. Board escalation at 3 consecutive of any single trigger type. |
| 4 | What happens to GateHealthReview records post-project? | Retained permanently per standard audit policy. They are governance documents. |
