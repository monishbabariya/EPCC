---
artefact: M05_RiskChangeControl_Workflows_v1_0
round: 36
date: 2026-05-04
author: Monish (with Claude assist)
parent_spec: M05_RiskChangeControl_Spec_v1_0.md (Round 33)
parent_brief: M05_RiskChangeControl_Brief_v1_0a (Round 31; v1.0a 7-state VO patch R33)
x8_version: v0.8
x9_version: v0.5
status: LOCKED
type: Module Workflows (Mermaid flowcharts + BR traceability)
batch_partner: M13_CorrespondenceMeetingRegister_Workflows_v1_0.md (C1b batch per Build Execution Plan §3a)
br_coverage: 36 BR codes (BR-05-001..035 + BR-05-030b) across 5 WFs — 0 gaps (see BR Coverage Matrix)
---

# M05 — Risk & Change Control — Workflows v1.0

## CHANGE LOG

| Version | Date | Author | Change Summary |
|---|---|---|---|
| v1.0 | 2026-05-04 | Monish (with Claude assist) | Initial workflows lock (Round 36). 5 workflows covering all M05 Spec v1.0 (R33) BRs. WF-05-001 Risk Identification (BR-05-002..008); WF-05-002 VO Lifecycle 7-state (BR-05-009..017); WF-05-003 EOT + EWN combined (BR-05-018..026 — EWN folded into EOT WF since EOT requires EWN per OQ-1.8); WF-05-004 LD Accrual + NCR→LD (BR-05-031..035); WF-05-005 Contingency Pool + Project Activation (BR-05-001, 027..030b). All Mermaid flowcharts validate. C1b batch with M13 Workflows. |

---

## Purpose

Runtime workflows for M05 Risk & Change Control. Each Mermaid diagram describes the **runtime behaviour** of a decision-bearing process. Cross-references to BR codes link runtime to the locked specification (M05 Spec v1.0 Block 6).

5 workflows covered:

| # | Workflow | Decision Answered | Primary Role(s) | BR Coverage |
|---|---|---|---|---|
| **WF-05-001** | Risk Identification and Scoring | Has a project risk been formally identified, scored, and assigned an owner + response strategy? | Any view_project role (raise) → PROJECT_DIRECTOR/PMO_DIRECTOR (accept) | BR-05-002..008 |
| **WF-05-002** | Variation Order Lifecycle (7-state) | Has a scope or cost variation been formally assessed, approved (single OR dual sign-off), and materialised into the BOQ — with full audit trail? | QS_MANAGER (assess) → PMO_DIRECTOR + FINANCE_LEAD (approve) | BR-05-009..017 |
| **WF-05-003** | Extension of Time + Early Warning Notice | Has a contractor's EOT claim been formally assessed (with EWN prerequisite per OQ-1.8) and grant decision cascaded to schedule baseline? | PROJECT_DIRECTOR + PLANNING_ENGINEER (assess) → PMO_DIRECTOR (grant) | BR-05-018..026 |
| **WF-05-004** | LD Accrual + NCR→LD Eligibility | Is the contractor accruing liquidated damages, and which NCRs have been assessed as LD-eligible? | M05 SYSTEM (NCR signal consumer) + FINANCE_LEAD (review) | BR-05-031..035 |
| **WF-05-005** | Contingency Pool Drawdown + Project Activation | Has a contingency drawdown been formally requested and approved with pool balance verified? | PROJECT_DIRECTOR (request) → PMO_DIRECTOR (approve, no self-approval) | BR-05-001, 027..030b |

---

## WF-05-001 — Risk Identification and Scoring

> **Decision:** Has a project risk been formally identified, scored, and assigned an owner + response strategy?
> **Primary Role:** Any view_project role (Draft raise per OQ-2.6 broad-raise pattern) → PROJECT_DIRECTOR or PMO_DIRECTOR (Active accept).
> **BR Coverage:** BR-05-002 (state machine), BR-05-003 (risk_score = P × I), BR-05-004 (rag_band derivation 1-4/5-12/13-25), BR-05-005 (READ_ONLY hides numeric), BR-05-006 (Red band requires response_strategy + 48hr SLA), BR-05-007 (ARTA ENUM), BR-05-008 (Risk closure: residual ≤ 6 + PMO sign-off).

### Mermaid State Diagram

```mermaid
stateDiagram-v2
    [*] --> Draft: Any view_project role raises Risk\n(broad-raise per OQ-2.6)
    Draft --> Active: PROJECT_DIRECTOR or PMO_DIRECTOR\nACCEPT_RISK action (BR-05-002)
    Draft --> Withdrawn: Raiser withdraws within 24hr
    Active --> Mitigating: response_strategy populated\n(ARTA per BR-05-007)
    Mitigating --> Closed: residual_risk_score <= 6\nAND PMO_DIRECTOR sign-off (BR-05-008)
    Active --> Reopened: PMO override (audited)
    Mitigating --> Reopened: PMO override (audited)
    Reopened --> Active: re-acceptance
    Withdrawn --> [*]
    Closed --> [*]
```

### Runtime Flow

```mermaid
flowchart TD
    A[Any view_project role:<br/>RAISE_RISK action] --> B[Risk created<br/>status=Draft<br/>per BR-05-002]
    B --> C{Probability + Impact<br/>entered 1..5}
    C --> D[risk_score = P × I<br/>auto-computed BR-05-003<br/>read-only in UI]
    D --> E[rag_band auto-derived BR-05-004:<br/>1-4=Green / 5-12=Amber / 13-25=Red]
    E --> F{rag_band == Red<br/>AND response_strategy<br/>NOT populated?}
    F -->|YES| G[After 48hr grace period:<br/>emit HIGH_RISK_THRESHOLD_BREACH<br/>DQ trigger to PROJECT_DIRECTOR<br/>per BR-05-006]
    F -->|NO| H[Persist Risk row]
    G --> H
    H --> I[Audit event: RISK_RAISED<br/>RiskStatusLog entry append-only]
    I --> J{PROJECT_DIRECTOR or<br/>PMO_DIRECTOR review}
    J --> K[ACCEPT_RISK action:<br/>status Draft → Active<br/>RISK_ACCEPTED audit event]
    J --> L[Withdraw if raised in error:<br/>status → Withdrawn within 24hr]
    K --> M[response_strategy populated<br/>per BR-05-007 ARTA<br/>Avoid/Reduce/Transfer/Accept]
    M --> N[status: Active → Mitigating<br/>RISK_RESPONSE_PLAN_UPDATED audit]
    N --> O{Mitigation complete?<br/>residual_probability/impact<br/>populated; residual_score ≤ 6}
    O -->|YES + PMO sign-off| P[status: Mitigating → Closed<br/>per BR-05-008<br/>RISK_CLOSED audit event]
    O -->|NO| Q[Continue mitigation]
    Q --> N

    style D fill:#fef3c7
    style E fill:#fef3c7
    style G fill:#fee2e2
    style P fill:#dcfce7
```

### READ_ONLY Render Rule (BR-05-005)

```mermaid
flowchart LR
    A[API serialiser receives<br/>Risk row for response] --> B{Caller role}
    B -->|READ_ONLY| C[Strip fields:<br/>probability_score<br/>impact_score<br/>risk_score]
    B -->|All other roles| D[Return all fields<br/>incl. numeric scores]
    C --> E[Response: rag_band + title only]
    D --> F[Full response]
```

### Periodic Risk Review (per OQ-2.5)

`ProjectRiskConfig.risk_review_cadence_days` (default 90 — quarterly) drives a sweep:
- Daily background job checks `Risk` rows with `status IN (Active, Mitigating)` AND `last_reviewed_at + risk_review_cadence_days < today`.
- Emits `RISK_REVIEW_DUE` notification to risk owner (no DQ trigger; informational).

### Audit Events Emitted

| Event | Trigger BR | Severity |
|---|---|---|
| `RISK_RAISED` | BR-05-002 (Draft create) | Info |
| `RISK_ACCEPTED` | BR-05-002 (Draft → Active) | Info |
| `RISK_SCORE_CHANGED` | BR-05-003 + BR-05-004 (P or I edit) | Medium (severity-dependent on rag_band) |
| `RISK_RESPONSE_PLAN_UPDATED` | BR-05-007 (response_strategy set) | Info |
| `RISK_CLOSED` | BR-05-008 (closure) | Info |
| `RISK_WITHDRAWN` | BR-05-002 (Draft → Withdrawn) | Info |

### Decision Queue Triggers Emitted

| Trigger | Severity | Owner | SLA | Source BR |
|---|---|---|---|---|
| `HIGH_RISK_THRESHOLD_BREACH` | High | PROJECT_DIRECTOR | 48 hr | BR-05-006 |

### Failure Modes

| Failure | Behaviour |
|---|---|
| Caller attempts to set `risk_score` directly | API rejects 422 — read-only field per BR-05-003 |
| Red band Risk saved without response_strategy after 48hr | `HIGH_RISK_THRESHOLD_BREACH` DQ trigger fires per BR-05-006 |
| Closure attempted with residual_score > 6 | Block transition with reason `RESIDUAL_SCORE_EXCEEDS_GREEN_THRESHOLD` per BR-05-008 |
| Closure attempted by non-PMO_DIRECTOR | Block with reason `CLOSURE_REQUIRES_PMO_SIGNOFF` per BR-05-008 |

---

## WF-05-002 — Variation Order Lifecycle (7-state)

> **Decision:** Has a scope or cost variation been formally assessed, approved (with appropriate dual sign-off where required), and materialised into the BOQ — with full audit trail?
> **Primary Role:** QS_MANAGER (assess + submit) → PMO_DIRECTOR / FINANCE_LEAD (approve; dual above ₹50L) → SYSTEM (Materialise on M02 confirmation).
> **BR Coverage:** BR-05-009 (state machine), BR-05-010 (Draft → Assessed), BR-05-011 (Assessed → Submitted + DQ trigger), BR-05-012 (Submitted → Approved single/dual), BR-05-013 (Approved → emit VO_APPROVED to M02), BR-05-014 (Materialised system action), BR-05-015 (M02 failure handling), BR-05-016 (EWN required if Delay/Scope_Increase), BR-05-017 (VO Materialised → emit VO_APPROVED_COST_IMPACT to M06).

### State Machine (7 states per Brief v1.0a OQ-1.5)

```mermaid
stateDiagram-v2
    [*] --> Draft: PROJECT_DIRECTOR/QS_MANAGER<br/>DRAFT_VO action
    Draft --> Assessed: QS_MANAGER assesses<br/>(BR-05-010)
    Draft --> Rejected: PROJECT_DIRECTOR rejects
    Assessed --> Submitted: QS_MANAGER submits for approval<br/>cost_impact_inr populated<br/>(BR-05-011)
    Assessed --> Rejected: QS_MANAGER rejects
    Submitted --> Approved: Single sign-off ≤ ₹50L<br/>OR dual sign-off > ₹50L<br/>(BR-05-012)
    Submitted --> Rejected: Approver rejects
    Approved --> Materialised: SYSTEM action<br/>on M02 confirmation<br/>(BR-05-014)
    Materialised --> Closed: Project closeout
    Rejected --> [*]
    Closed --> [*]

    note right of Submitted
        VO_PENDING_APPROVAL
        DQ trigger fires here
        per BR-05-011
    end note

    note right of Materialised
        SYSTEM-only transition
        No human role can manually
        Materialise (per F2 lock)
        PMO_DIRECTOR has retry only
    end note
```

### Runtime Flow

```mermaid
flowchart TD
    A[QS_MANAGER or PROJECT_DIRECTOR<br/>DRAFT_VO action] --> B{vo_cause IN<br/>Delay or Scope_Increase?}
    B -->|YES| C{early_warning_notice_id<br/>populated?<br/>BR-05-016}
    C -->|NO| D[Block create:<br/>EWN_REQUIRED_FOR_DELAY_OR_SCOPE_INCREASE]
    C -->|YES + EWN active| E[VO created<br/>status=Draft<br/>VO_DRAFTED audit]
    B -->|NO| E
    E --> F[QS_MANAGER assesses<br/>cost_impact_inr populated<br/>BR-05-010]
    F --> G[status: Draft → Assessed<br/>VO_ASSESSED audit]
    G --> H[QS_MANAGER submits<br/>BR-05-011]
    H --> I[status: Assessed → Submitted<br/>VO_SUBMITTED audit<br/>VO_PENDING_APPROVAL DQ trigger fires]
    I --> J{cost_impact_inr<br/>vs threshold?<br/>BR-05-012}
    J -->|≤ ₹50L| K[Single sign-off:<br/>PMO_DIRECTOR OR FINANCE_LEAD]
    J -->|> ₹50L| L[Dual sign-off:<br/>PMO_DIRECTOR AND FINANCE_LEAD<br/>both required]
    K --> M{Approved?}
    L --> N{Both Approve?}
    M -->|YES| O[status: Submitted → Approved<br/>VO_APPROVED audit<br/>BR-05-013]
    N -->|YES| O
    M -->|NO| P[status → Rejected<br/>VO_REJECTED audit]
    N -->|NO| P
    O --> Q[M05 emits VO_APPROVED event<br/>to M02 internal API<br/>per BR-05-013]
    Q --> R[M02 sets Package.bac_integrity_status<br/>= Stale_Pending_VO<br/>Creates VOBOQMaterialisation row]
    R --> S{M02 BOQ update<br/>completes?}
    S -->|Complete| T[VO transitions Approved → Materialised<br/>SYSTEM action BR-05-014<br/>VO_MATERIALISED audit]
    S -->|Failed| U[VOBOQMaterialisation.failure_reason<br/>populated<br/>VO stays at Approved<br/>BR-05-015]
    U --> V[VO_MATERIALISATION_FAILED<br/>DQ trigger Critical<br/>to PMO_DIRECTOR + SYSTEM_ADMIN]
    V --> W[PMO_DIRECTOR retry option<br/>OR resolve M02 issue]
    T --> X[M05 emits VO_APPROVED_COST_IMPACT<br/>to M06 per BR-05-017]
    X --> Y[M06 writes Committed CostLedgerEntry<br/>per M06 BR-06-039]
    Y --> Z[VO closes on project closeout<br/>VO_CLOSED audit]

    style I fill:#fef3c7
    style O fill:#dcfce7
    style P fill:#fee2e2
    style T fill:#dcfce7
    style U fill:#fee2e2
    style V fill:#dc2626,color:#fff
```

### Dual Sign-Off Sub-Flow (BR-05-012)

```mermaid
flowchart LR
    A[VO at Submitted<br/>cost_impact_inr > ₹50L threshold] --> B[approved_by_pmo_at NULL<br/>approved_by_finance_at NULL]
    B --> C{PMO_DIRECTOR<br/>approves?}
    C -->|YES| D[approved_by_pmo_at = now<br/>approved_by_pmo_user_id set]
    D --> E{FINANCE_LEAD<br/>also approved?}
    E -->|NO — PMO first| F[Wait for FINANCE_LEAD<br/>VO stays Submitted]
    E -->|YES — both done| G[status: Submitted → Approved]
    C -->|FINANCE_LEAD approves first| H[approved_by_finance_at = now]
    H --> I{PMO_DIRECTOR<br/>also approved?}
    I -->|NO| F
    I -->|YES — both done| G
    F --> J[Reminder DQ:<br/>VO_PENDING_APPROVAL escalates]
```

**Anti-self-approval rule:** Same user cannot populate both `approved_by_pmo_at` AND `approved_by_finance_at` (different `user_id` required). System validates at second-approval time.

### Audit Events Emitted

| Event | Trigger BR | Severity |
|---|---|---|
| `VO_DRAFTED` | BR-05-009 | Info |
| `VO_ASSESSED` | BR-05-010 | Info |
| `VO_SUBMITTED` | BR-05-011 | Info |
| `VO_APPROVED` | BR-05-012 + BR-05-013 | High |
| `VO_REJECTED` | BR-05-009 | Medium |
| `VO_MATERIALISED` | BR-05-014 + BR-05-017 | High |
| `VO_MATERIALISATION_FAILED` | BR-05-015 | Critical |
| `VO_CLOSED` | BR-05-009 | Info |

### Decision Queue Triggers Emitted

| Trigger | Severity | Owner | SLA | Source BR |
|---|---|---|---|---|
| `VO_PENDING_APPROVAL` | Medium | QS_MANAGER (assessor) → PMO_DIRECTOR/FINANCE_LEAD (approvers) | 7 days assess + 7 days approve | BR-05-011 |
| `VO_MATERIALISATION_FAILED` | Critical | PMO_DIRECTOR + SYSTEM_ADMIN | Real-time | BR-05-015 |

### Cross-Module Events

| Direction | Event | Target | Trigger | Speed |
|---|---|---|---|---|
| OUT | `VO_APPROVED` | M02 (BOQ update) | VO Submitted → Approved | 🔴 Real-time |
| IN | M02 confirmation `materialisation_status=Complete OR Failed` | M05 | M02 finishes BOQ update | 🔴 Real-time |
| OUT | `VO_APPROVED_COST_IMPACT` | M06 (CostLedgerEntry) | VO Approved → Materialised | 🔴 Real-time |

---

## WF-05-003 — Extension of Time + Early Warning Notice

> **Decision:** Has a contractor's EOT claim been formally assessed (with EWN prerequisite per OQ-1.8 NEC4/FIDIC alignment) and a grant decision (full / partial / rejected) cascaded to the schedule baseline?
> **Primary Role:** SITE_MANAGER / PROJECT_DIRECTOR (raise EWN) → PLANNING_ENGINEER + PROJECT_DIRECTOR (assess EOT claim) → PMO_DIRECTOR (grant or reject).
> **BR Coverage:** BR-05-018 (EOT requires EWN), BR-05-019 (partial grant requires reason ≥100 chars), BR-05-020 (PMO grant authority), BR-05-021 (EOT_GRANTED → M03 cascade), BR-05-022 (M03 cascade failure), BR-05-023 (EWN create min chars), BR-05-024 (EOT/VO references EWN → close), BR-05-025 (EWN auto-lapse sweep), BR-05-026 (EWN lapse approaching DQ trigger).

### EWN State Machine

```mermaid
stateDiagram-v2
    [*] --> Active: SITE_MANAGER/PROJECT_DIRECTOR<br/>RAISE_EWN action<br/>(BR-05-023)
    Active --> Closed: Linked EOT/VO transitions<br/>to terminal state<br/>(BR-05-024)
    Active --> Lapsed: ewn_lapse_days passed<br/>without claim link<br/>(BR-05-025 daily sweep)
    Closed --> [*]
    Lapsed --> [*]

    note right of Lapsed
        Subsequent EOT/VO claims
        referencing this EWN are
        BLOCKED per BR-05-016/018
    end note
```

### EOT State Machine

```mermaid
stateDiagram-v2
    [*] --> Claim_Raised: EOT claim filed<br/>EWN reference NOT NULL<br/>(BR-05-018)
    Claim_Raised --> Under_Assessment: PLANNING_ENGINEER assesses
    Claim_Raised --> Withdrawn: Claimant withdraws
    Under_Assessment --> Granted: PMO_DIRECTOR grants<br/>full OR partial<br/>(BR-05-020)
    Under_Assessment --> Rejected: PMO_DIRECTOR rejects
    Under_Assessment --> Withdrawn: Claimant withdraws
    Granted --> [*]
    Rejected --> [*]
    Withdrawn --> [*]

    note right of Granted
        If granted_days < claim_days:
        partial_grant_reason ≥ 100 chars
        REQUIRED per BR-05-019
    end note
```

### Runtime Flow

```mermaid
flowchart TD
    A[SITE_MANAGER or PROJECT_DIRECTOR<br/>RAISE_EWN action] --> B[EarlyWarningNotice created<br/>delaying_event_description ≥ 100 chars<br/>expected_impact_qualitative ≥ 50 chars<br/>BR-05-023]
    B --> C[status=Active<br/>EWN_RAISED audit event]
    C --> D[EWN lapse timer starts:<br/>raised_at + ProjectRiskConfig.ewn_lapse_days<br/>default 30 days]
    D --> E{Daily EWN sweep:<br/>BR-05-025 + BR-05-026}
    E --> F{75% lapse window?<br/>BR-05-026}
    F -->|YES| G[Emit EWN_LAPSE_APPROACHING<br/>DQ trigger Medium<br/>to PROJECT_DIRECTOR]
    F -->|NO| H{100% lapse window?<br/>BR-05-025}
    H -->|YES + no claim link| I[status: Active → Lapsed<br/>EWN_LAPSED audit event<br/>Subsequent claims referencing<br/>this EWN now BLOCKED]
    H -->|NO| E
    G --> H

    C --> J[Contractor or PMC<br/>RAISE_EOT_CLAIM action]
    J --> K{early_warning_notice_id<br/>populated AND EWN.status=Active?<br/>BR-05-018}
    K -->|NO| L[Block create:<br/>EWN_REQUIRED_BR_05_018]
    K -->|YES| M[EOT created<br/>status=Claim_Raised<br/>EOT_CLAIM_RAISED audit]
    M --> N[PLANNING_ENGINEER assesses<br/>delaying event merit<br/>EOT_CLAIM_PENDING_ASSESSMENT DQ<br/>14-day SLA]
    N --> O[status: Claim_Raised → Under_Assessment<br/>EOT_UNDER_ASSESSMENT audit]
    O --> P{PMO_DIRECTOR<br/>decision per BR-05-020}
    P -->|Grant full| Q[granted_days = claim_days]
    P -->|Grant partial| R{partial_grant_reason<br/>≥ 100 chars?<br/>BR-05-019}
    R -->|NO| S[Block transition:<br/>PARTIAL_GRANT_REASON_REQUIRED]
    R -->|YES| T[granted_days < claim_days<br/>partial_grant_reason populated]
    P -->|Reject| U[status → Rejected<br/>EOT_REJECTED audit]
    Q --> V[status: Under_Assessment → Granted<br/>EOT_GRANTED audit]
    T --> V
    V --> W[M05 emits EOT_GRANTED event<br/>to M03 per BR-05-021<br/>payload: eot_id, granted_days,<br/>cause_category, affected_milestones,<br/>variation_order_id if linked]
    W --> X{M03 BaselineExtension<br/>creation succeeds?}
    X -->|YES| Y[M03 callback with<br/>m03_baseline_extension_id<br/>M05 stores reference]
    X -->|NO| Z[Emit EOT_BASELINE_CASCADE_FAILED<br/>DQ trigger Critical<br/>to PMO_DIRECTOR + SYSTEM_ADMIN<br/>per BR-05-022]

    V --> AA[EWN.linked_eot_id populated<br/>EWN.status: Active → Closed<br/>EWN_CLOSED audit per BR-05-024]
    U --> AA

    style L fill:#fee2e2
    style I fill:#fee2e2
    style V fill:#dcfce7
    style Z fill:#dc2626,color:#fff
```

### Audit Events Emitted

| Event | Trigger BR | Severity |
|---|---|---|
| `EWN_RAISED` | BR-05-023 | Info |
| `EWN_CLOSED` | BR-05-024 | Info |
| `EWN_LAPSED` | BR-05-025 | Medium |
| `EOT_CLAIM_RAISED` | BR-05-018 | Info |
| `EOT_UNDER_ASSESSMENT` | (state transition) | Info |
| `EOT_GRANTED` | BR-05-020 + BR-05-021 | High |
| `EOT_REJECTED` | (state transition) | Medium |
| `EOT_BASELINE_CASCADE_FAILED` | BR-05-022 | Critical |

### Decision Queue Triggers Emitted

| Trigger | Severity | Owner | SLA | Source BR |
|---|---|---|---|---|
| `EWN_LAPSE_APPROACHING` | Medium | PROJECT_DIRECTOR | 7 days before lapse | BR-05-026 |
| `EOT_CLAIM_PENDING_ASSESSMENT` | Medium | PLANNING_ENGINEER | 14 days | (Block 4a action SLA) |
| `EOT_BASELINE_CASCADE_FAILED` | Critical | PMO_DIRECTOR + SYSTEM_ADMIN | Real-time | BR-05-022 |

### Cross-Module Events

| Direction | Event | Target | Trigger | Speed |
|---|---|---|---|---|
| OUT | `EOT_GRANTED` | M03 (BaselineExtension creation) | EOT Under_Assessment → Granted | 🔴 Real-time |
| IN | M03 callback `baseline_extension_id` OR cascade failure | M05 | Async after M03 receives EOT_GRANTED | 🔴 Real-time |

---

## WF-05-004 — LD Accrual + NCR→LD Eligibility

> **Decision:** Is the contractor accruing liquidated damages, and which NCRs have been assessed as LD-eligible (with the M04 system-to-system flag write per BR-04-022)?
> **Primary Role:** M05 SYSTEM (NCR signal consumer + daily aging sweep) + FINANCE_LEAD (review LD exposure dashboard).
> **BR Coverage:** BR-05-031 (LD amount calculation + cap), BR-05-032 (Daily NCR aging sweep), BR-05-033 (M05_SYSTEM actor for ld_eligibility_flag write — UI blocked at M04 API), BR-05-034 (LD cap approaching 80% DQ), BR-05-035 (LD cap reached 100% DQ + accrual block).

### NCR→LD Eligibility Flow (System-to-System per BR-04-022)

```mermaid
flowchart TD
    A[M04 emits NCR_RAISED or<br/>NCR_STATUS_CHANGED event<br/>per M04 BR-04-021] --> B[M05 receives via internal API endpoint]
    B --> C[Daily NCR aging sweep<br/>🟢 24hr batch<br/>per BR-05-032]
    C --> D{For each open<br/>M04.ConstructionNCR}
    D --> E{severity ∈ Critical, High?}
    E -->|NO| F[Skip — LD not applicable<br/>by severity policy]
    E -->|YES| G{now - raised_at ><br/>ProjectRiskConfig.ncr_aging_to_ld_days?<br/>default 14}
    G -->|NO| H[Skip — below aging threshold]
    G -->|YES| I{ld_eligibility_flag<br/>currently false?}
    I -->|YES| J{contractor-fault waiver<br/>OR cumulative LD<br/>at cap?<br/>BR-05-035}
    J -->|YES| K[Skip — flag NOT set<br/>logged: LD_ELIGIBILITY_ASSESSED_FALSE]
    J -->|NO| L[M05 SYSTEM calls M04 internal API<br/>PATCH ld_eligibility_flag = true<br/>actor = M05_SYSTEM<br/>per BR-05-033 + M04 BR-04-022]
    I -->|NO| M[Already flagged; skip]
    L --> N[M04 records flip in audit log<br/>actor = M05_SYSTEM]
    L --> O[M05 creates LDExposureRecord row<br/>ld_status = Accruing]
    O --> P[Compute ld_amount_inr:<br/>M01.Contract.ld_rate_per_week ×<br/>delay_weeks ×<br/>contract_value_basic<br/>per BR-05-031]
    P --> Q{Cumulative LD ≥<br/>ld_cap_pct × contract_value?}
    Q -->|YES — capped| R[ld_amount_inr capped at remaining<br/>cap headroom; ld_status: Cap_Reached<br/>BR-05-031]
    Q -->|NO| S[ld_amount_inr accrues to record]
    R --> T[Emit LD_AMOUNT_CALCULATED audit]
    S --> T
    T --> U[Emit LD_ELIGIBILITY_FLIPPED_TRUE audit<br/>LDExposureLog row append-only]
    U --> V[M05 emits LD_ELIGIBLE_AMOUNT event to M06<br/>per BR-05-009 = OQ-1.9 = B<br/>+ M06 BR-06-039 line 708 contract]
    V --> W[M06 writes CostLedgerEntry deduction tracker<br/>FINANCE_LEAD review gate]

    P --> X{Cumulative LD ≥ 80% of cap?<br/>BR-05-034}
    X -->|YES| Y[Emit LD_CAP_APPROACHING DQ trigger<br/>High to PMO_DIRECTOR + FINANCE_LEAD<br/>24hr SLA]
    X -->|NO| W

    P --> Z{Cumulative LD = 100% of cap?<br/>BR-05-035}
    Z -->|YES| AA[Emit LD_CAP_REACHED DQ trigger<br/>Critical to PMO_DIRECTOR + FINANCE_LEAD<br/>Real-time]
    AA --> AB[Subsequent NCR aging sweeps<br/>do NOT flip new flags<br/>BR-05-035 cap-enforced block]

    style L fill:#fef3c7
    style R fill:#fef3c7
    style Y fill:#fee2e2
    style AA fill:#dc2626,color:#fff
```

### NCR→LD Eligibility Reversal (per BR-05-013 audited override)

```mermaid
flowchart LR
    A[NCR closed before LD finalised<br/>OR PMO_DIRECTOR override] --> B[M05 SYSTEM calls M04<br/>PATCH ld_eligibility_flag = false]
    B --> C[M04 records flip:<br/>actor = M05_SYSTEM<br/>direction = true→false]
    C --> D[Emit LD_ELIGIBILITY_FLIPPED_FALSE audit]
    D --> E[LDExposureRecord.ld_status<br/>updated to Waived]
    E --> F[Both true→false and false→true<br/>flips audited per audit-trail discipline]
```

### Audit Events Emitted

| Event | Trigger BR | Severity |
|---|---|---|
| `LD_ELIGIBILITY_FLIPPED_TRUE` | BR-05-032 + BR-05-033 | High |
| `LD_ELIGIBILITY_FLIPPED_FALSE` | BR-05-032 (NCR closed before LD finalised) | Medium |
| `LD_AMOUNT_CALCULATED` | BR-05-031 | Info |
| `LD_CAP_REACHED` | BR-05-035 | Critical |

### Decision Queue Triggers Emitted

| Trigger | Severity | Owner | SLA | Source BR |
|---|---|---|---|---|
| `LD_CAP_APPROACHING` | High | PMO_DIRECTOR + FINANCE_LEAD | 24 hr | BR-05-034 |
| `LD_CAP_REACHED` | Critical | PMO_DIRECTOR + FINANCE_LEAD | 24 hr | BR-05-035 |

### Cross-Module Events

| Direction | Event | Target | Trigger | Speed |
|---|---|---|---|---|
| IN | `NCR_RAISED` / `NCR_STATUS_CHANGED` | M05 | M04 NCR create + status change | 🔴 Real-time (per M04 BR-04-021) |
| OUT | `ld_eligibility_flag = true` (system-to-system) | M04 | NCR aging crosses threshold | 🔴 Real-time (per M04 BR-04-022 + BR-05-033) |
| OUT | `LD_ELIGIBLE_AMOUNT` | M06 | LD eligibility flip true OR cumulative recalc | 🔴 Real-time |

### Failure Modes

| Failure | Behaviour |
|---|---|
| M04 internal API unavailable for `ld_eligibility_flag` write | M05 retries with exponential backoff (5 attempts); after exhaustion raises `LD_FLAG_WRITEBACK_FAILED` DQ Critical |
| UI attempts to set `ld_eligibility_flag` directly via M04 API | M04 API rejects per BR-04-022 (only M05 internal API allowed) |
| Cumulative LD exceeds cap mid-calculation | Cap enforcement clamps to remaining headroom; `LD_CAP_REACHED` DQ fires per BR-05-035 |

---

## WF-05-005 — Contingency Pool Drawdown + Project Activation

> **Decision:** Has a contingency drawdown been formally requested and approved — with the pool balance verified before release and the depletion thresholds enforced?
> **Primary Role:** PROJECT_DIRECTOR or PMO_DIRECTOR (request) → PMO_DIRECTOR (approve; no self-approval per BR-05-028).
> **BR Coverage:** BR-05-001 (Project Activation auto-creates ContingencyPool + ProjectRiskConfig), BR-05-027 (Drawdown create), BR-05-028 (PMO approval no self-approval), BR-05-029 (Pool depletion HIGH 80%), BR-05-030 (Pool depletion CRITICAL 95%), BR-05-030b (CONTINGENCY_DRAWDOWN_GATE_REQUEST to M08).

### Project Activation Sub-Flow (BR-05-001)

```mermaid
flowchart LR
    A[M01 emits PROJECT_ACTIVATED event] --> B[M05 receives]
    B --> C[Auto-create ProjectRiskConfig row<br/>with OQ-2.5 defaults]
    B --> D[Auto-create ContingencyPool row<br/>total_inr = M01.Contract.contract_value × risk_buffer_pct<br/>consumed_inr = 0]
    C --> E[Emit PROJECT_RISK_INITIALISED audit event]
    D --> E
```

### Drawdown Approval Flow

```mermaid
flowchart TD
    A[PROJECT_DIRECTOR or PMO_DIRECTOR<br/>REQUEST_CONTINGENCY_DRAWDOWN action] --> B{Required fields<br/>per BR-05-027?}
    B -->|missing| C[Block save with reason<br/>FIELDS_MISSING]
    B -->|all present| D{Exactly one of<br/>linked_risk_id /<br/>linked_vo_id /<br/>linked_change_id?<br/>BR-05-027 CHECK constraint}
    D -->|NO — zero or multiple| E[Block save:<br/>EXACTLY_ONE_LINK_REQUIRED]
    D -->|YES — exactly one| F[ContingencyDrawdownLog row<br/>status = Requested<br/>amount_inr > 0<br/>justification ≥ 100 chars]
    F --> G[CONTINGENCY_DRAWDOWN_REQUESTED<br/>audit event]
    G --> H{requested_amount ≤<br/>ContingencyPool.available_inr?}
    H -->|NO| I[Auto-reject:<br/>INSUFFICIENT_BALANCE<br/>status → Rejected]
    H -->|YES| J{Above stage-gate threshold?<br/>BR-05-030b]
    J -->|YES| K[Emit CONTINGENCY_DRAWDOWN_GATE_REQUEST<br/>to M08 stub<br/>per Brief §10 forward constraint]
    J -->|NO| L[Direct to PMO_DIRECTOR approval]
    K --> L
    L --> M[Decision Queue:<br/>CONTINGENCY_DRAWDOWN_APPROVAL_REQUIRED<br/>to PMO_DIRECTOR]
    M --> N{PMO_DIRECTOR review:<br/>BR-05-028 anti-self-approval}
    N --> O{requested_by_user_id ==<br/>approved_by_user_id?}
    O -->|YES — self-approval| P[Block: SELF_APPROVAL_FORBIDDEN<br/>per BR-05-028]
    O -->|NO — different user| Q{PMO_DIRECTOR<br/>decision}
    Q -->|Approve| R[ContingencyDrawdownLog.status<br/>= Approved<br/>approved_by_user_id + approved_at set]
    Q -->|Reject| S[status = Rejected<br/>rejection_reason ≥ 100 chars]
    R --> T[Atomically update:<br/>ContingencyPool.consumed_inr += amount_inr<br/>ContingencyPool.consumed_pct re-derived]
    T --> U[CONTINGENCY_DRAWDOWN_APPROVED audit event]
    U --> V{Check depletion thresholds<br/>per BR-05-029 / BR-05-030}
    V --> W{consumed_pct ≥ 0.80?<br/>BR-05-029}
    W -->|YES| X[Emit CONTINGENCY_POOL_DEPLETION_HIGH<br/>DQ trigger High to PMO_DIRECTOR<br/>24hr SLA]
    V --> Y{consumed_pct ≥ 0.95?<br/>BR-05-030}
    Y -->|YES| Z[Emit CONTINGENCY_POOL_DEPLETION_CRITICAL<br/>DQ trigger Critical to PMO_DIRECTOR<br/>Real-time]
    S --> AA[CONTINGENCY_DRAWDOWN_REJECTED audit]

    style I fill:#fee2e2
    style P fill:#fee2e2
    style R fill:#dcfce7
    style X fill:#fee2e2
    style Z fill:#dc2626,color:#fff
```

### Reversal via Compensating Entry (per M06 precedent)

```mermaid
flowchart LR
    A[Drawdown reversal needed<br/>e.g. risk closed before fund use] --> B[Create new ContingencyDrawdownLog row<br/>amount_inr = NEGATIVE original<br/>linked_drawdown_id = original<br/>status = Reversed]
    B --> C[Original row remains intact<br/>append-only ledger discipline]
    C --> D[ContingencyPool.consumed_inr<br/>recomputed = SUM all rows]
```

### Audit Events Emitted

| Event | Trigger BR | Severity |
|---|---|---|
| `PROJECT_RISK_INITIALISED` | BR-05-001 | Info |
| `CONTINGENCY_DRAWDOWN_REQUESTED` | BR-05-027 | Info |
| `CONTINGENCY_DRAWDOWN_APPROVED` | BR-05-028 | High |
| `CONTINGENCY_DRAWDOWN_REJECTED` | (state transition) | Medium |

### Decision Queue Triggers Emitted

| Trigger | Severity | Owner | SLA | Source BR |
|---|---|---|---|---|
| `CONTINGENCY_POOL_DEPLETION_HIGH` | High | PMO_DIRECTOR | 24 hr | BR-05-029 |
| `CONTINGENCY_POOL_DEPLETION_CRITICAL` | Critical | PMO_DIRECTOR | Real-time | BR-05-030 |
| `CONTINGENCY_DRAWDOWN_GATE_REQUEST` | (M08-defined) | M08 (when built) | (M08-defined) | BR-05-030b |

### Cross-Module Events

| Direction | Event | Target | Trigger | Speed |
|---|---|---|---|---|
| IN | `PROJECT_ACTIVATED` | M05 | M01 Project state transitions | 🔴 Real-time |
| IN | `M01.Contract.contract_value` + `risk_buffer_pct` | M05 | Read at Activation | 🔴 Real-time |
| OUT | `CONTINGENCY_DRAWDOWN_GATE_REQUEST` | M08 stub (when built) | Drawdown above stage-gate threshold | 🔴 Real-time |

---

## BR Coverage Matrix — M05

Every BR in M05 Spec v1.0 (R33) Block 6 mapped to at least one workflow. **0 coverage gaps.**

| BR Code | BR Summary | WF-05-001 Risk | WF-05-002 VO | WF-05-003 EOT+EWN | WF-05-004 LD | WF-05-005 Contingency |
|---|---|---|---|---|---|---|
| BR-05-001 | Project Activation auto-create | | | | | ✓ |
| BR-05-002 | Risk state machine | ✓ | | | | |
| BR-05-003 | risk_score = P × I | ✓ | | | | |
| BR-05-004 | rag_band derivation 1-4/5-12/13-25 | ✓ | | | | |
| BR-05-005 | READ_ONLY hides numeric scores | ✓ | | | | |
| BR-05-006 | Red band requires response_strategy + 48hr | ✓ | | | | |
| BR-05-007 | ARTA ENUM | ✓ | | | | |
| BR-05-008 | Risk closure (residual ≤ 6 + PMO) | ✓ | | | | |
| BR-05-009 | VO 7-state machine | | ✓ | | | |
| BR-05-010 | VO Draft → Assessed (QS_MANAGER) | | ✓ | | | |
| BR-05-011 | VO Assessed → Submitted + DQ trigger | | ✓ | | | |
| BR-05-012 | VO Submitted → Approved single/dual | | ✓ | | | |
| BR-05-013 | VO Approved → emit VO_APPROVED to M02 | | ✓ | | | |
| BR-05-014 | VO Materialised SYSTEM action | | ✓ | | | |
| BR-05-015 | M02 materialisation failure handling | | ✓ | | | |
| BR-05-016 | EWN required if vo_cause Delay/Scope_Increase | | ✓ | | | |
| BR-05-017 | VO Materialised → emit VO_APPROVED_COST_IMPACT | | ✓ | | | |
| BR-05-018 | EOT requires EWN | | | ✓ | | |
| BR-05-019 | Partial grant requires reason ≥100 chars | | | ✓ | | |
| BR-05-020 | EOT Granted by PMO_DIRECTOR | | | ✓ | | |
| BR-05-021 | EOT_GRANTED → M03 BaselineExtension | | | ✓ | | |
| BR-05-022 | M03 baseline cascade failure | | | ✓ | | |
| BR-05-023 | EWN create min description chars | | | ✓ | | |
| BR-05-024 | EOT/VO references EWN → close | | | ✓ | | |
| BR-05-025 | Daily EWN sweep — Lapsed transition | | | ✓ | | |
| BR-05-026 | EWN sweep — Lapse approaching DQ | | | ✓ | | |
| BR-05-027 | ContingencyDrawdown create | | | | | ✓ |
| BR-05-028 | PMO approval no self-approval | | | | | ✓ |
| BR-05-029 | Pool depletion HIGH 80% | | | | | ✓ |
| BR-05-030 | Pool depletion CRITICAL 95% | | | | | ✓ |
| BR-05-030b | CONTINGENCY_DRAWDOWN_GATE_REQUEST to M08 | | | | | ✓ |
| BR-05-031 | LD amount calculation + cap | | | | ✓ | |
| BR-05-032 | Daily NCR aging sweep | | | | ✓ | |
| BR-05-033 | M05_SYSTEM actor for ld_eligibility_flag | | | | ✓ | |
| BR-05-034 | LD cap approaching 80% DQ | | | | ✓ | |
| BR-05-035 | LD cap reached 100% DQ + accrual block | | | | ✓ | |

**Coverage:** 36 / 36 BR codes covered. **0 gaps.**

---

*v1.0 — Workflows LOCKED 2026-05-04 (Round 36). C1b batch with M13 Workflows. M05 build-ready after this round.*
