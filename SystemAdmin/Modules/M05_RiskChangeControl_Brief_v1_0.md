# M05 — Risk & Change Control — Brief v1.0b

**Artefact:** M05_RiskChangeControl_Brief_v1_0b
**Round:** 31 (in-place patches: R33 v1.0a 7-state VO; R37 v1.0b stamp refresh)
**Date:** 2026-05-04
**Author:** Monish (with Claude assist)
**Status:** LOCKED
**Last Updated:** 2026-05-04 (v1.0b R37 stamp refresh — Reference Standards bumped to X8 v0.8 + X9 v0.5)
**Last Audited:** v1.0b on 2026-05-04
**Reference Standards:** X8_GlossaryENUMs_v0_8.md, X9_VisualisationStandards_Spec_v0_4.md (content version v0.5; filename retained per in-place patch convention), M34_SystemAdminRBAC_Spec_v1_0a.md, M01_ProjectRegistry_Spec_v1_0a.md (+ v1_1/v1_2/v1_3/v1_4 cascade notes), M02_StructureWBS_Spec_v1_0a.md (+ v1_1 cascade note), M03_PlanningMilestones_Spec_v1_1b.md (+ v1_2/v1_3 cascade notes), M04_ExecutionCapture_Spec_v1_0a.md, M06_FinancialControl_Spec_v1_0b.md (+ v1_1 cascade note)
**Layer:** L2 Control — Risk & Commercial
**Phase:** 1 — Foundational (gates M07 EVM, M08 GateControl, M19 Claims Phase 2)
**Build Priority:** 🔴 Critical (precedes M07, M08; consumes M04 NCR + M03 BaselineExtension + M01 Contract + M02 BOQ)
**Folder:** SystemAdmin/Modules/

---

## CHANGE LOG

| Patch | Date       | Author                      | Changes |
|-------|------------|-----------------------------|---------|
| v1.0b | 2026-05-04 | Monish (with Claude assist) | **R37 in-place patch (stamp refresh).** M3: Reference Standards refreshed to X8 v0.8 + X9 v0.5 (post-cascade per spec-protocol §In-Place Patch Convention). No content/scope change. All R33 v1.0a OQ-1.5 7-state VO decisions preserved intact. |
| v1.0a | 2026-05-04 | Monish (with Claude assist) | OQ-1.5 cascade impact updated: VO state machine extended from 6 to 7 states with explicit `Submitted` handoff between QS_MANAGER assessor and PMO/FINANCE approver. Reason: `VO_PENDING_APPROVAL` Decision Queue trigger (OQ-2.3) needs an in-flight state to anchor on; without `Submitted`, the trigger has nothing to reference. Submitted state cleanly separates "QS_MANAGER has assessed and submitted for approval" from "approver has approved" — required for dual-sign-off discipline above the ₹50L threshold (OQ-1.5). OQ-2.2 append-only ledger transition path also extended to include Submitted. No scope, entity, or BR change beyond state-list extension. |

---

## 1. Purpose

M05 is the **commercial-consequence engine** of EPCC. It owns the deliberation layer where execution-stack reality becomes contractual / financial / schedule consequence — and where the project's response to risk and change is recorded as governance trail.

M05 sits between M04 (faithful site capture, no commercial logic) and M06 (financial transaction processing, no risk deliberation). Where M04 reports an NCR, M05 decides whether it warrants Liquidated Damages. Where M03 records a baseline, M05 decides whether an Extension of Time event modifies it. Where M02 holds a BAC, M05 decides whether a Variation Order materialises into BOQ updates. M05 is the point at which **judgement** enters the system.

**Decision M05 enables:** *"Given everything that has happened on site (NCRs, delays, scope changes, risks materialising), what is the contractual and commercial response — and is the project on track to absorb it within contingency, or are we exceeding tolerance?"*

### Sub-questions M05 answers

- Which risks are active, what is their probability × impact, and who owns the response?
- Has a delay-causing event been formally noticed (Early Warning Notice) and is that notice an adequate prerequisite for downstream EOT/VO claim?
- Does this Variation Order have approval to materialise into a BOQ change (M02) and a CostLedgerEntry (M06)?
- Does this Extension of Time claim warrant a baseline extension (M03) and at what magnitude (full / partial)?
- Are NCRs aging into LD-eligibility, and what is the cumulative LD exposure (capped per `M01.Contract.ld_cap_pct`)?
- Is the contingency pool depletion within governance tolerance, or does drawdown trigger a stage-gate review (M08)?
- What is the risk-adjusted EAC delta to feed M07 EVM Engine?

## 2. Scope (this round)

This Brief surfaces **10 OQ-1 architectural decisions** and **6 OQ-2 pattern defaults** that the M05 Spec (Round 32) will rest on. **All 16 are CLOSED in this Brief** with locked answers — the Spec can be authored without re-opening any of them.

**In scope:**

- **Risk Register** — identification, probability × impact assessment, response strategy (ARTA), owner assignment, RAG band derivation from numeric score
- **Change Register** — scope change tracking; site instructions; RFI integration with M12 (when built); change classification
- **Variation Order (VO) lifecycle** — Draft → Assessed → Approved → Materialised → Closed; cost impact assessment; M02 BOQ materialisation trigger; M06 CostLedgerEntry trigger
- **Extension of Time (EOT) lifecycle** — Claim_Raised → Assessed → Granted (full/partial) / Rejected; M03 BaselineExtension cascade trigger
- **Liquidated Damages (LD) tracking** — exposure calculation, NCR aging consumption, cap enforcement per `M01.Contract.ld_cap_pct`, M04 `ld_eligibility_flag` system-to-system write per BR-04-022, M06 `LD_ELIGIBLE_AMOUNT` event emission
- **Contingency drawdown governance** — pool initialisation from `M01.Contract.risk_buffer_pct`, drawdown approval workflow, stage-gate linkage with M08 (when built)
- **NCR → LD eligibility assessment** — consuming M04 `NCR_RAISED` / `NCR_STATUS_CHANGED` events per BR-04-021, applying age + severity + closure rules, writing back per BR-04-022
- **Early Warning Notice (EWN) management** — mandatory prerequisite for EOT and VO claims (per industry best practice; NEC4 / FIDIC alignment); notice-to-claim time tracking
- **Claims exposure summary** — aggregated view of pending VOs, EOTs, LDs, contingency consumed; feeds M10 EPCCCommand dashboard

**Explicitly NOT in scope (decided OQ-1.1 = B):**

- **Financial transaction processing** → M06 (M05 emits `VO_APPROVED_COST_IMPACT` and `LD_ELIGIBLE_AMOUNT` events; M06 owns CostLedgerEntry writes per BR-06-039)
- **BOQ update execution** → M02 (M05 triggers VO materialisation; M02 executes BOQ updates per Block 7 SENDS TO + `BOQItem.boq_origin = VO_Materialisation`)
- **Baseline recalculation** → M03 (M05 triggers EOT decision; M03 owns `BaselineExtension` entity and downstream PV regen per BR-03-026..028)
- **Site diary** → M16 SiteDiary (Phase 2)
- **Document storage internals (RFI attachments, VO supporting documents)** → M12 DocumentControl (M05 stores `document_id` references; M12 owns blob storage)
- **Long-form claims management (end-of-project disputes)** → **M19 ClaimsManagement** (Phase 2). M05's "claims exposure summary" is the rollup view; M19 (when built) owns formal claim documentation, expert assessments, and arbitration packets
- **HSE incidents** → M31 HSESafetyManagement (Phase 2)
- **Compliance non-conformance** → M09 ComplianceTracker (M05 handles construction NCRs only; M09 owns regulatory/clinical compliance NCRs)
- **DLP retention release** → M15 owns the DLP signal; M06 owns the financial release trigger; M05 is **NOT** in this chain (per M06 v1.1 cascade note H6 Option B lock)
- **Stage gate decision-making** → M08 GateControl (M05 raises drawdown gate requests; M08 owns the gate decision)
- **Risk-adjusted EAC computation** → M07 EVMEngine (M05 emits delta inputs; M07 owns EAC algorithm)

## 3. Prior Art

**Legacy reference:** `ZEPCC_Legacy/M05_Risk_Change_v2_3.md`

The legacy v2.3 amendment file in `ZEPCC_Legacy/` was an in-place patch on a bundled "Risk + Change + VO + EOT + LD + Claims + Contingency + Insurance" megamodule. This Brief follows the M04 precedent and **slim-cores** M05 to the deliberation/governance layer, deferring:
- Long-form claims to M19 (Phase 2)
- HSE risk to M31 (Phase 2)
- Insurance management to a future round (BG/insurance integration via M23 BGInsuranceTracker)

### Key drift from legacy v2.3

| Legacy (v2.3) | This Brief (v1.0) | Why |
|---|---|---|
| Single bundled module (Risk + Change + VO + EOT + LD + Claims + HSE + Insurance) | Slim core (Risk + Change + VO + EOT + LD + Contingency + EWN); Claims → M19, HSE → M31, Insurance → M23 | Single-owner discipline (F-005); each concern lives in its dedicated module |
| Probability/impact qualitative only | 5×5 numeric matrix + RAG derivation per X9 dual-encode | Quantitative aggregation needed for portfolio-level rollup (M10, PIOE Phase 2) |
| LD calculation in legacy v2.3 done in spreadsheet-land | M05 owns LD calc; emits to M06 via `LD_ELIGIBLE_AMOUNT` event per M06 line 708 already-locked contract | Anti-drift; system-of-record discipline |
| VO materialisation logic ambiguous between modules | M05 = trigger; M02 = execute BOQ (per M02 Spec line 69 + Block 7 lock) | Single-owner |
| EOT cascade to schedule undefined | M05 triggers; M03 creates `BaselineExtension` (per M03 Spec line 184-206 already-locked contract) | Single-owner |
| Contingency drawdown ungoverned | Drawdown above threshold requires PMO_DIRECTOR + stage-gate alignment with M08 | Governance trail |
| Early Warning Notice not modelled | First-class entity; mandatory before EOT/VO claim | Industry best practice (NEC4 / FIDIC) |
| ARTA response types implicit | Locked at 4 values: `Avoid / Reduce / Transfer / Accept` (X8 v0.7 cascade) | Symmetry with PMBOK; opportunities (positive risks) Phase 2 extension via cascade |

---

## 4. OQ-1 — Design Decisions Required From User

> All 10 decisions are **CLOSED** in this Brief. The M05 Spec (Round 32) will reference these by ID without re-opening.

### OQ-1.1 — Module scope decomposition

**Question:** What does M05 RiskChangeControl include, and what gets split to neighbouring modules?

**Options:**
- A. Bundle everything from legacy v2.3 (Risk + Change + VO + EOT + LD + Claims + HSE + Insurance)
- B. Slim core (Risk + Change + VO + EOT + LD + Contingency + Early Warning); Claims → M19; HSE → M31; Insurance → M23
- C. Slim core + integrate Claims into M05 (as a sub-register)

**Resolution:** **B (LOCKED).** Single-owner discipline (F-005). M05 keeps the deliberation/governance layer; long-form claims work (expert assessments, arbitration packets) belongs to M19 in Phase 2; HSE risk has its own governance system in M31; insurance goes with BG/Insurance in M23. This mirrors the M04 OQ-1.1 = B precedent (slim core).

**Cascade impact:**
- M19 ClaimsManagement Brief (Phase 2 future round) will absorb formal claims content; M05 emits `CLAIMS_EXPOSURE_SUMMARY` aggregated view
- M31 HSESafetyManagement Brief (Phase 2) absorbs HSE risk
- M23 BGInsuranceTracker Brief absorbs insurance (BGStub pattern from M06 Brief OQ-1.9 already extends to M05's insurance scope)
- M05 v1.0 Spec is materially smaller than legacy v2.3 — easier to lock cleanly

**Status:** CLOSED

---

### OQ-1.2 — Probability × Impact matrix granularity

**Question:** What granularity for the risk probability × impact matrix?

**Options:**
- A. **5×5 matrix** (25-cell heatmap; 5 probability bands × 5 impact bands) — quantitative; PMBOK industry standard
- B. 3×3 matrix (9-cell) — simpler, RAG-friendly
- C. 5×5 with optional Monte Carlo overlay for top-N risks

**Resolution:** **A (LOCKED).** 5×5 is PMBOK-aligned and gives finer prioritisation discrimination than 3×3 (especially for the 3-amber-cells problem in 3×3). Monte Carlo overlay (Option C) is Phase 2; the architecture (CLAUDE.md §4 Risk Categories already locks "qualitative heat map + quantitative Monte Carlo") supports both — Phase 1 ships qualitative; Phase 2 adds MC.

**Cascade impact:**
- New X8 ENUMs (v0.7 cascade): `RiskProbabilityBand` (5 values: Very_Low / Low / Moderate / High / Very_High), `RiskImpactBand` (5 values: same names)
- Numeric mapping: probability_score = 1..5; impact_score = 1..5; risk_score = product (1..25)
- RAG derivation rule: 1-4 = Green, 5-12 = Amber, 13-25 = Red (per X9 v0.4 dual-encode + RAGStatus ENUM)

**Status:** CLOSED

---

### OQ-1.3 — Risk scoring method

**Question:** How is risk scored — qualitative bands only, numeric score, or both?

**Options:**
- A. RAG-only (qualitative bands; user assigns Green/Amber/Red directly)
- B. **Numeric score** (probability_score × impact_score) **+ RAG band auto-derived**
- C. Both numeric AND user-overridable RAG (override audited)

**Resolution:** **B (LOCKED).** Numeric score for sorting / aggregation / portfolio rollup (M10, PIOE Phase 2 input); RAG band auto-derived from score per the §OQ-1.2 mapping rule. Aligns with X9 v0.4 dual-encode discipline (numeric drives RAG; never the inverse). Override (Option C) creates audit drift; defer to Phase 2 if pressure surfaces.

**Cascade impact:**
- M05 entity `Risk` carries `probability_score` (INT 1..5), `impact_score` (INT 1..5), `risk_score` (CALC = product), `rag_band` (DERIVED from risk_score)
- BR: `rag_band` is read-only in UI; recomputed on every probability/impact edit
- X9 v0.4 §13.3 role-default views: PMO_DIRECTOR + PROJECT_DIRECTOR get 5×5 risk heatmap; ANALYST gets risk score trend; READ_ONLY gets RAG-only view (numeric scores hidden)

**Status:** CLOSED

---

### OQ-1.4 — Risk response types (ARTA vs extended)

**Question:** What risk response strategies does M05 support?

**Options:**
- A. **ARTA** — Avoid / Reduce / Transfer / Accept (PMBOK 4-type, threats only)
- B. Extended — ARTA + Exploit / Enhance / Share (PMBOK 7-type, includes opportunities)
- C. ARTA + custom org-specific "Escalate"

**Resolution:** **A (LOCKED) for Phase 1.** ARTA aligns with Indian EPC contractual practice (FIDIC + standard EPC clauses speak ARTA language). Opportunities (positive risks) are less salient in EPC delivery (where most "risks" are downside) and add UI/cognitive overhead. Phase 2 cascade can extend to 7-type via additive ENUM cascade (no schema change). "Escalate" is a workflow concept, not a response type — modelled separately as a Decision Queue trigger (M11) when a risk crosses portfolio threshold.

**Cascade impact:**
- New X8 ENUM (v0.7): `RiskResponseStrategy` = `Avoid / Reduce / Transfer / Accept`
- M05 BR: every Risk row with `risk_score >= 13` (Red band) MUST have a populated `response_strategy` and `response_action_plan` (≥ 100 chars)

**Status:** CLOSED

---

### OQ-1.5 — VO approval workflow

**Question:** Who approves a Variation Order, and is the approval threshold-tiered?

**Options:**
- A. Single-authority (PROJECT_DIRECTOR for all VOs)
- B. **Threshold-based dual sign-off** — single below threshold; dual (PMO_DIRECTOR + FINANCE_LEAD) above
- C. Multi-level with client (CLIENT_VIEWER) sign-off above higher threshold

**Resolution:** **B (LOCKED) with default threshold ₹50 lakh.** Mirrors M04 dual sign-off threshold (M04 OQ-1.4 = C, ₹50 lakh of WBS-node BAC slice). Single sign-off (Option A) under-governs commercial impact; client sign-off (Option C) is a Phase 2 concern when PF03 ExternalPartyPortal lands. Threshold is configurable per project via M05-owned `ProjectRiskConfig` entity (resolves where the threshold lives — see OQ-2.5).

**Cascade impact (v1.0a — patched 2026-05-04):**
- New X8 ENUMs (v0.7): `VOStatus` (state machine — **Draft / Assessed / Submitted / Approved / Materialised / Closed / Rejected; 7 states with explicit `Submitted` handoff between QS_MANAGER assessor and PMO/FINANCE approver**), `VOApprovalLevel` (Single / Dual)
- VO state transitions: `Draft → Assessed` (QS_MANAGER assesses cost impact) → `Submitted` (QS_MANAGER submits for approval) → `Approved` (single sign-off ≤ threshold; dual sign-off > threshold) → `Materialised` (system action on Approved event; M02 BOQ update completes) → `Closed`. `Rejected` is terminal-from-{Draft, Assessed, Submitted}; cannot reject after Approved (use compensating VO instead).
- M05 BR-05-XXX: `VO.cost_impact_inr <= ProjectRiskConfig.dual_signoff_threshold_inr` (default ₹50 lakh) allows single-sign-off path (PMO_DIRECTOR OR FINANCE_LEAD); above threshold requires both `approved_by_pmo_at` AND `approved_by_finance_at` populated
- Decision Queue trigger `VO_PENDING_APPROVAL` (per OQ-2.3) anchors on `Submitted` state — escalates to PMO_DIRECTOR/FINANCE_LEAD on entry to Submitted (7-day SLA per OQ-2.3)
- Default threshold stored on `ProjectRiskConfig.dual_signoff_threshold_inr` (configurable; M05-owned, mirrors M04 `ProjectExecutionConfig` pattern)

**Status:** CLOSED

---

### OQ-1.6 — EOT grant model

**Question:** Are partial EOT grants allowed, or is grant binary (full claim or full reject)?

**Options:**
- A. Binary (full grant or full reject)
- B. **Partial grants allowed** (claim 30 days, grant 21 days; rejection_reason required if granted < claimed)
- C. Multi-stage (provisional grant → final grant after impact analysis)

**Resolution:** **B (LOCKED).** Real-world EOT claims commonly resolve at partial grants — the contractor over-claims as a negotiating posture, the engineer assesses the merit of each delay event, and the final grant is some fraction of the claim. Forcing binary creates pressure to either over-grant (leniency) or unnecessarily reject (creates dispute). Multi-stage (Option C) adds workflow complexity without proportionate value at Phase 1 scale.

**Cascade impact:**
- M05 entity `ExtensionOfTime`: `claim_days INT NOT NULL`, `granted_days INT NULLABLE` (set on Granted transition; ≤ claim_days), `partial_grant_reason TEXT` (required if granted_days < claim_days, ≥ 100 chars)
- New X8 ENUM (v0.7): `EOTStatus` = Claim_Raised / Under_Assessment / Granted / Rejected / Withdrawn
- M03 BaselineExtension `granted_days` populated from M05.ExtensionOfTime.granted_days on Granted transition

**Status:** CLOSED

---

### OQ-1.7 — Contingency pool structure

**Question:** Is there one contingency pool per project, per phase, or per WBS top-level?

**Options:**
- A. **One pool per project** (`contingency_pool_inr` initialised from `M01.Contract.contract_value × Contract.risk_buffer_pct`)
- B. One pool per phase (per X8 §3.9 Phase ENUM — 10 values)
- C. One pool per WBS top-level node

**Resolution:** **A (LOCKED).** Project-level pool aligns with M01 Contract field semantics (`risk_buffer_pct` is already contract-level). Phase-pool (Option B) is over-engineered for Phase 1 — most projects in pilot scope (KDMC-001-DBOT) have a single primary phase active at a time. WBS-top-level (Option C) creates allocation friction without governance benefit. Phase 2 cascade can split the pool into phase pools via additive entity (`ContingencySubPool`) if scale demands.

**Cascade impact:**
- M05 entity `ContingencyPool`: 1 row per project; `total_inr CALC = M01.contract_value × M01.risk_buffer_pct`; `consumed_inr` updated on each Drawdown approval
- M05 entity `ContingencyDrawdown`: append-only ledger of drawdowns; each row references a Risk OR a VO OR a ChangeOrder
- BR: project-level pool depletion ≥ 80% emits `CONTINGENCY_POOL_DEPLETION_HIGH` Decision Queue trigger to PMO_DIRECTOR

**Status:** CLOSED

---

### OQ-1.8 — Early Warning Notice as prerequisite

**Question:** Is an Early Warning Notice (EWN) mandatory before an EOT or VO claim?

**Options:**
- A. **Mandatory before EOT or VO claim** (NEC4 / FIDIC industry best practice)
- B. Mandatory before EOT only (VO can be raised without prior EWN)
- C. Optional with audit annotation

**Resolution:** **A (LOCKED).** Industry best practice — NEC4 contracts mandate EWN, FIDIC 2017 strengthened EWN clauses (Clause 8.4 / 20.1), and the discipline forces early surface of issues rather than late surprise claims. Indian EPC market is moving toward NEC4-style early-warning regimes. The cost of "no EWN" is forfeit-of-claim; the cost of "EWN raised but no claim" is zero — asymmetric in favour of mandate.

**Cascade impact:**
- M05 entity `EarlyWarningNotice`: `id`, `project_id`, `raised_by_user_id`, `raised_at`, `delaying_event_description`, `affected_milestones[]`, `expected_impact_qualitative`, `closed_at` (nullable; set when corresponding EOT/VO closes)
- BR-05-XXX: ExtensionOfTime.create requires `early_warning_notice_id` FK populated (NOT NULL); same for VariationOrder.create where `vo_cause = Delay` or `vo_cause = Scope_Increase`
- New X8 ENUM (v0.7): `EWNStatus` = Active / Closed / Lapsed (if no claim raised within X days; X configurable via `ProjectRiskConfig.ewn_lapse_days`, default 30)
- Audit event `EWN_RAISED`, `EWN_CLOSED`, `EWN_LAPSED`

**Status:** CLOSED

---

### OQ-1.9 — LD enforcement model

**Question:** How does Liquidated Damages flow from M05 to financial impact?

**Options:**
- A. M05 calculates LD exposure; UI shows alongside billing (manual deduction by FINANCE_LEAD)
- B. **M05 calculates LD; M06 deducts from RA Bill via `LD_ELIGIBLE_AMOUNT` event**; FINANCE_LEAD review gate
- C. M05 calculates LD; manual deduction by FINANCE_LEAD on RA Bill (no auto-trigger)

**Resolution:** **B (LOCKED).** Aligns with M06 Spec line 708 already-locked contract: M06 receives `LD_ELIGIBLE_AMOUNT` event from M05 and writes to CostLedgerEntry deduction tracker. Auto-deduction with FINANCE_LEAD review gate gives both anti-drift discipline (every LD-eligible amount automatically surfaces in financials) and governance control (FINANCE_LEAD reviews before deduction commits). Option A creates a manual reconciliation gap; Option C breaks the M06 already-locked contract.

**Cascade impact:**
- M05 BR-05-XXX: when a ConstructionNCR aged > X days (X = `M01.Contract.ncr_aging_to_ld_days`, default 14) AND severity ∈ {Critical, High} AND `ld_eligibility_flag = false`, M05 system writes `ld_eligibility_flag = true` to M04.ConstructionNCR (per M04 BR-04-022 system-to-system contract) AND emits `LD_ELIGIBLE_AMOUNT` event to M06
- LD amount calculation: `M01.Contract.ld_rate_per_week × delay_weeks × M01.Contract.contract_value` (capped at `M01.Contract.ld_cap_pct × contract_value`)
- M05 BR-05-XXX: cumulative LD ≥ 80% of cap emits `LD_CAP_APPROACHING` Decision Queue to PMO_DIRECTOR + FINANCE_LEAD; at 100% blocks further LD accrual (cap enforced)

**Status:** CLOSED

---

### OQ-1.10 — Role-default views per X9 v0.4 §13.3.x

**Question:** What is each role's primary + secondary chart view in M05?

**Resolution:** **Mapping (a) LOCKED:**

| Role | Primary view | Secondary view |
|---|---|---|
| `PMO_DIRECTOR` | **Risk heatmap** (5×5 dual-encoded probability × impact) | LD exposure trend (cumulative vs cap) |
| `PROJECT_DIRECTOR` | Project risk register (filtered to own project; sortable by risk_score) | Pending VOs / EOTs queue |
| `PORTFOLIO_MANAGER` | **Portfolio risk heatmap** (aggregated across projects) | Contingency depletion across projects (table) |
| `FINANCE_LEAD` | LD exposure dashboard (per project + cumulative) | VO cost impact pipeline (Draft → Approved → Materialised funnel — X9 §11 flagship pattern instance #3 — **VO Funnel**) |
| `PLANNING_ENGINEER` | EOT claim queue (own project; assess pending) | Early Warning Notice log |
| `QS_MANAGER` | VO assessment queue (cost-impact reviews) | Change register (own packages) |
| `SITE_MANAGER` | Early Warning Notice — raise / view (own project) | Active risks affecting current site work |
| `COMPLIANCE_MANAGER` | (no primary M05 view; M09 owns) | Risk register read-only filter for compliance-classified risks |
| `PROCUREMENT_OFFICER` | (no primary M05 view; M06/M03 own) | VO impact on procurement schedule (link → M03) |
| `ANALYST` | Risk score trend curves | NCR-to-LD aging funnel (X9 §11 flagship pattern instance #4 — **LD Funnel**) |
| `READ_ONLY` | Risk register card (RAG-only; numeric scores hidden) | — |
| `EXTERNAL_AUDITOR` | Risk register full read-only | LD exposure history (audit trail) |
| `ANALYST` | (also: portfolio risk roll-up if project_ids[] spans multiple) | — |
| `SYSTEM_ADMIN` | (no primary; system roles only) | — |
| `CLIENT_VIEWER` (Phase 2) | (no primary; PF03 deferred) | — |
| `LENDER_VIEWER` (Phase 2) | (no primary; PF03 deferred) | — |
| `NABH_ASSESSOR` (Phase 2) | (no primary; PF03 deferred) | — |
| `CONTRACTOR_LIMITED` (Phase 2) | (no primary; PF03 deferred) | — |

**Cascade impact:**
- X9 v0.5 cascade — add M05 row to §13.3 role-default views table
- **3 new flagship pipeline pattern instances** (per X9 §11 Pipeline Funnel pattern):
  - **VO Funnel** (Draft → Assessed → Approved → Materialised → Closed) — instance #3 of named flagships (after M06 Capital Funnel #1, M04 NCR Funnel #2)
  - **LD Funnel** (NCR_Raised → Aging → LD_Eligible → LD_Applied) — instance #4
  - **EOT Funnel** (Claim_Raised → Under_Assessment → Granted/Partial/Rejected) — instance #5
- 5×5 risk heatmap is a new chart variant (dual-encoded; not previously instantiated) — confirm with X9 catalogue audit during Spec round; may require X9 §catalogue addition or fit as extension of existing matrix chart type

**Status:** CLOSED

---

## 5. OQ-2 — Pattern Defaults (Claude recommended; user confirmed)

### OQ-2.1 — Audit event naming discipline

**Default:** Lock proposed audit event names in this Brief (Appendix A) so the Spec carries them as locked from authoring — avoids retro-cascade.

**Reasoning:** M04 OQ-2.1 + M03 v1.1 cascade pattern: lock-in-Brief is the discipline. Estimated 28-32 events (3 Risk transitions + 4 VO transitions + 4 EOT + 2 EWN + 4 LD + 3 Contingency + 5-7 system + cross-module emits).

**Status:** CLOSED — proceed with lock-in-Brief

### OQ-2.2 — Append-only ledgers

**Default:** Following entities are append-only (DB-level UPDATE/DELETE forbidden — same pattern as M02 BACIntegrityLedger, M04 NCRStatusLog, M06 CostLedgerEntry):

- `RiskStatusLog` — every Risk state transition + score change
- `VOStatusLog` — every VO state transition (Draft → Assessed → Submitted → Approved → Materialised → Closed; 7-state per v1.0a OQ-1.5 cascade)
- `EOTStatusLog` — every EOT state transition
- `ContingencyDrawdownLog` — every drawdown event (forward-only; reversals via compensating entries per M06 precedent)
- `LDExposureLog` — every LD eligibility flip + amount change

**Reasoning:** Provenance is the value. Audits / arbitration / claims (M19 Phase 2) need the unaltered trail.

**Status:** CLOSED

### OQ-2.3 — Decision Queue SLA defaults

**Default:**

| Trigger | Severity | Owner | SLA |
|---|---|---|---|
| `HIGH_RISK_THRESHOLD_BREACH` (risk_score ≥ 13 with no response_action_plan) | High | PROJECT_DIRECTOR | 48 hr |
| `EWN_LAPSE_APPROACHING` | Medium | PROJECT_DIRECTOR | 7 days before lapse |
| `EOT_CLAIM_PENDING_ASSESSMENT` | Medium | PLANNING_ENGINEER | 14 days |
| `VO_PENDING_APPROVAL` | Medium | QS_MANAGER (assessor) → then PMO_DIRECTOR/FINANCE_LEAD (approvers) | 7 days at assessment; 7 days at approval |
| `LD_CAP_APPROACHING` (cumulative ≥ 80%) | High | PMO_DIRECTOR + FINANCE_LEAD | 24 hr |
| `LD_CAP_REACHED` (cumulative = 100%) | Critical | PMO_DIRECTOR + FINANCE_LEAD | 24 hr |
| `CONTINGENCY_POOL_DEPLETION_HIGH` (≥ 80%) | High | PMO_DIRECTOR | 24 hr |
| `CONTINGENCY_POOL_DEPLETION_CRITICAL` (≥ 95%) | Critical | PMO_DIRECTOR | Real-time |
| `VO_MATERIALISATION_FAILED` (M02 sync error) | Critical | PMO_DIRECTOR + SYSTEM_ADMIN | Real-time |
| `EOT_BASELINE_CASCADE_FAILED` (M03 sync error) | Critical | PMO_DIRECTOR + SYSTEM_ADMIN | Real-time |

**Reasoning:** Aligns with M03/M04/M06 Decision Queue SLA conventions.

**Status:** CLOSED

### OQ-2.4 — Speed tier defaults

**Default:**

| Event class | Speed tier |
|---|---|
| Risk create / update / response edit | 🔴 Real-time |
| VO state transition (any) | 🔴 Real-time |
| EOT state transition (any) | 🔴 Real-time |
| EWN raise / close | 🔴 Real-time |
| LD eligibility flip (M04 system-to-system write per BR-04-022) | 🔴 Real-time |
| LD amount calculation on RA Bill submission | 🔴 Real-time |
| Contingency drawdown approval | 🔴 Real-time |
| Daily NCR aging sweep (NCR-to-LD eligibility check) | 🟢 24 hr |
| Quarterly risk register review batch | 🟢 24 hr |
| Risk-adjusted EAC delta to M07 | 🟡 1 hr (batch with M07 EAC recalc cycle) |

**Status:** CLOSED

### OQ-2.5 — ProjectRiskConfig entity (where M05 thresholds live)

**Default:** M05-owned `ProjectRiskConfig` entity (1 row per project) carries:

| Field | Default | Notes |
|---|---|---|
| `dual_signoff_threshold_inr` | ₹50,00,000 (50 lakh) | OQ-1.5 lock |
| `ewn_lapse_days` | 30 | OQ-1.8 lock |
| `ncr_aging_to_ld_days` | 14 | OQ-1.9 lock |
| `contingency_depletion_high_pct` | 0.80 | OQ-1.7 + OQ-2.3 |
| `contingency_depletion_critical_pct` | 0.95 | OQ-2.3 |
| `risk_review_cadence_days` | 90 (quarterly) | risk register review batch |

**Reasoning:** Mirrors M04 `ProjectExecutionConfig` pattern. Avoids M01 cascade for every project-level tunable. PROJECT_DIRECTOR + PMO_DIRECTOR may edit; audited.

**Status:** CLOSED

### OQ-2.6 — Risk identification ownership (who can raise a Risk?)

**Default:** Any role with `view_project` permission may **raise** a Risk (Draft state). Risks transition to `Active` status only after PROJECT_DIRECTOR (or PMO_DIRECTOR) review. This mirrors M04 ProgressEntry's three-state pattern (Draft → Submitted → Approved) — broad capture, governed acceptance.

**Reasoning:** Risk identification is an early-warning function; restricting the "raise" action to senior roles dampens signal. The state machine separates capture from acceptance, preserving governance discipline.

**Status:** CLOSED

---

## 6. Users & Roles (all 17 canonical roles per M34 Spec Block 3)

| Role | M05 Access |
|---|---|
| `SYSTEM_ADMIN` | Full read; system-context only (no primary M05 surface) |
| `PMO_DIRECTOR` | **PRIMARY** — Risk heatmap, contingency drawdown approval, dual sign-off (above threshold), portfolio risk view, LD cap enforcement |
| `PORTFOLIO_MANAGER` | **PRIMARY** — Portfolio risk heatmap aggregation, contingency depletion across projects |
| `PROJECT_DIRECTOR` | **PRIMARY** — Own-project risk register, EOT/VO assessment, EWN review, contingency drawdown raise |
| `PLANNING_ENGINEER` | **PRIMARY** — EOT claim assessment (own project; baseline-impact analysis), EWN raise |
| `QS_MANAGER` | **PRIMARY** — VO assessment (cost impact), change register (own packages), LD calc review |
| `FINANCE_LEAD` | **PRIMARY** — LD exposure dashboard, VO cost impact pipeline, dual sign-off (above threshold) |
| `PROCUREMENT_OFFICER` | **SECONDARY** — VO impact on procurement schedule (link to M03) |
| `SITE_MANAGER` | **PRIMARY** — Early Warning Notice raise + view (own project), active risks affecting current site work |
| `COMPLIANCE_MANAGER` | **SECONDARY** — Read-only filter on compliance-classified risks (M09 owns regulatory NCRs separately) |
| `ANALYST` | **PRIMARY** — Risk score trend curves, LD-aging funnel, portfolio rollup analytics |
| `READ_ONLY` | **VIEW-ONLY** — Risk register card (RAG-only; numeric scores hidden) |
| `EXTERNAL_AUDITOR` | **VIEW-ONLY** — Risk register full read-only, LD exposure history (MFA-required per M34) |
| `CLIENT_VIEWER` (Phase 2) | **NO ACCESS** Phase 1 — gated by PF03 ExternalPartyPortal |
| `LENDER_VIEWER` (Phase 2) | **NO ACCESS** Phase 1 — gated by PF03 |
| `NABH_ASSESSOR` (Phase 2) | **NO ACCESS** Phase 1 — gated by PF03 |
| `CONTRACTOR_LIMITED` (Phase 2) | **NO ACCESS** Phase 1 — gated by PF03 |

**Float-value visibility (per M03 OQ-1.10 lock pattern):** RAG-only view enforced for READ_ONLY; numeric `risk_score` hidden. All other internal roles see numeric scores. EXTERNAL_AUDITOR sees both (audit-trail visibility).

**MFA-required roles (per M34):** SYSTEM_ADMIN, PMO_DIRECTOR, PORTFOLIO_MANAGER, FINANCE_LEAD, EXTERNAL_AUDITOR. M05 inherits M34's MFA gate; no module-specific re-implementation.

---

## 7. Key Entities (Spec Round 32 will detail; Brief locks the shape)

| Entity | Cardinality | Owner | Purpose |
|---|---|---|---|
| `Risk` | Many per project | M05 | The risk register entry. 5×5 probability × impact, RAG-derived, ARTA response. |
| `RiskStatusLog` | Many per Risk | M05 (append-only) | Every state transition + score change. Provenance for risk-adjusted EAC trail (M07). |
| `Change` | Many per project | M05 | Scope-change tracking; site instructions; RFI integration with M12 (when built). |
| `VariationOrder` | Many per project | M05 | VO lifecycle. M02 BOQ materialisation trigger; M06 CostLedgerEntry trigger. |
| `VOStatusLog` | Many per VO | M05 (append-only) | Every state transition. |
| `VOBOQMaterialisation` | Many per VO | M05 (FK from M02 BOQItem.source_materialisation_id per M02 Spec line 192) | The cross-module handoff record between M05 (decision) and M02 (BOQ execution). |
| `ExtensionOfTime` | Many per project | M05 | EOT lifecycle. M03 BaselineExtension cascade trigger. |
| `EOTStatusLog` | Many per EOT | M05 (append-only) | Every state transition. |
| `EarlyWarningNotice` | Many per project | M05 | Mandatory prerequisite for EOT/VO claim. Auto-lapses after `ewn_lapse_days`. |
| `ContingencyPool` | 1 per project | M05 | Initialised from M01.Contract.risk_buffer_pct × contract_value. Forward-only depletion. |
| `ContingencyDrawdown` | Many per ContingencyPool | M05 (append-only) | Each drawdown event. References Risk OR VO OR Change. |
| `LDExposureRecord` | Many per project | M05 | LD calculation history per (NCR aging event × time). |
| `LDExposureLog` | Many per LDExposureRecord | M05 (append-only) | Every LD eligibility flip. |
| `ProjectRiskConfig` | 1 per project | M05 | Per-project tunables (OQ-2.5 lock). |

**Total entities:** 14 (5 primary + 4 transactional + 4 append-only ledgers + 1 config). Comparable to M06 (17) and M04 (10).

---

## 8. Integration Points (sketch — full spec in Block 7 of Round 32 Spec)

### IN (M05 receives from)

| From | Data | Trigger | Speed |
|---|---|---|---|
| M01 | `Contract.ld_rate_per_week`, `ld_cap_pct`, `risk_buffer_pct`, `contract_value_basic` (per M01 Spec line 619 already-locked SENDS TO M05) | On Contract Activation + edit | 🔴 |
| M01 | `Project.current_phase`, `project_status`, `report_date` | On Project state change | 🔴 |
| M02 | `BOQItem` schema for VO costing (estimate-mode reads); `Package.bac_amount` for VO impact calc | On VO costing assessment | 🔴 |
| M02 | `BACIntegrityLedger.bac_integrity_status = Stale_Pending_VO` (FK from `Package.pending_vo_id` to `M05.VariationOrder` per M02 Spec line 156) | On VO Approved → Materialisation start | 🔴 |
| M03 | `BaselineExtension` schema (M03-owned entity; M05 triggers, M03 owns row) per M03 Spec line 184-206 | On EOT Granted | 🔴 |
| M03 | `Milestone` IDs and dates (for EWN affected_milestones[] selection) | On EWN raise | 🔴 |
| **M04 BR-04-021** | **`NCR_RAISED` + `NCR_STATUS_CHANGED`** events with full ConstructionNCR payload | On M04 NCR create + status change | 🔴 |
| M04 | `ConstructionNCR.severity`, `raised_at`, `closed_at` (for NCR aging → LD eligibility) | Read on aging sweep | 🟢 24hr |
| M34 | Auth, role, project scope, MFA gate | Every API call | 🔴 |
| M11 ActionRegister (when built) | Decision Queue acknowledgement back-events | On owner action | 🔴 |

### OUT (M05 sends to)

| To | Data | Trigger | Speed |
|---|---|---|---|
| **M02** | **VO materialisation trigger** — `VO_APPROVED` event → M02 sets `Package.bac_integrity_status = Stale_Pending_VO`, creates `VOBOQMaterialisation` rows (per M02 Spec Block 7 contract) | On VO Approved | 🔴 |
| M02 | VO closure confirmation on materialisation complete (M02 sends back; M05 records) | On M02 reports materialisation done | 🔴 |
| **M03** | **EOT cascade** — `EOT_GRANTED` event → M03 creates `BaselineExtension` row with `granted_days`, `cause_category`, `variation_order_id` (if linked), `is_billable_to_client` (per M03 Spec line 202) | On EOT Granted | 🔴 |
| **M04 BR-04-022** | **`ld_eligibility_flag` write-back** — system-to-system call; UI cannot perform this write | On NCR aging crosses threshold + severity check | 🔴 |
| **M06 BR-06-039** | **`VO_APPROVED_COST_IMPACT` event** with `vo_id`, `vo_cost_impact_inr`, `triggering_event = VO_APPROVED` (per M06 Spec line 682 already-locked contract) | On VO Approved | 🔴 |
| **M06** | **`LD_ELIGIBLE_AMOUNT` event** with calculated LD amount, NCR_id reference, contract_id (per M06 Spec line 708 already-locked contract) | On LD eligibility flip true OR cumulative recalc | 🔴 |
| M07 EVMEngine (when built) | `RISK_ADJUSTED_EAC_DELTA` event — sum of (probability × impact_inr) for all Active risks; quarterly cadence | Quarterly batch + on-demand recalc | 🟡 1hr |
| M08 GateControl (when built) | `CONTINGENCY_DRAWDOWN_GATE_REQUEST` event — for drawdowns above stage-gate threshold (defined by M08 when built) | On drawdown raise above threshold | 🔴 |
| M10 EPCCCommand (when built) | Risk heatmap data + LD exposure aggregation for Command dashboard | On request (read-through) | 🟡 1hr cache |
| M11 ActionRegister (when built) | Decision Queue triggers (HIGH_RISK_THRESHOLD_BREACH, LD_CAP_APPROACHING, etc.) | On condition match | 🔴 / 🟢 |
| M19 ClaimsManagement (Phase 2) | `CLAIMS_EXPOSURE_SUMMARY` aggregated rollup (LD + pending VOs + pending EOTs + contingency consumed) | On request + monthly batch | 🟡 1hr cache |

---

## 9. Key Business Rules (OQ-level — full BRs in Round 32 Spec Block 6)

The following are the **hard rules** locked at Brief stage. Numbered `BR-05-xxx` in Spec round.

| # | Rule (one-line summary) | Authority |
|---|---|---|
| 1 | **No contingency drawdown without PMO_DIRECTOR approval above threshold** (stage-gate linkage with M08 when built) | OQ-1.7 + OQ-2.3 |
| 2 | **VO cannot materialise until Approved** — no pre-approval BOQ touch; M02 only acts on VO_APPROVED event | OQ-1.5 |
| 3 | **EOT claim must reference specific delaying event + affected milestones** — M05 EarlyWarningNotice FK NOT NULL on EOT.create | OQ-1.6 + OQ-1.8 |
| 4 | **LD assessment owned by M05; flag write to M04 is system-to-system only** (per M04 BR-04-022 — UI writes blocked at API layer) | OQ-1.9 + M04 BR-04-022 contract |
| 5 | **EWN mandatory before EOT/VO claim** (where vo_cause = Delay or Scope_Increase); EWN.lapse after `ewn_lapse_days` blocks claim | OQ-1.8 |
| 6 | **Risk score Red band requires response_action_plan** (≥ 100 chars) — block save without it | OQ-1.4 |
| 7 | **LD cap enforcement** — cumulative LD ≥ `M01.Contract.ld_cap_pct × contract_value` blocks further LD accrual | OQ-1.9 |
| 8 | **VO cost impact must respect BACIntegrityLedger** — M02 owns BAC integrity contract; M05 reads but never writes M02 ledger | OQ-1.1 + M02 Spec |
| 9 | **EOT cascade is one-way** — M05 emits, M03 creates BaselineExtension (append-only after approval per M03 Spec Block 3d). M05 cannot edit M03's BaselineExtension. | M03 single-owner |
| 10 | **Dual sign-off above threshold** — VO above ₹50 lakh requires both `approved_by_pmo_at` AND `approved_by_finance_at`; same for ContingencyDrawdown above threshold | OQ-1.5 + OQ-2.3 |
| 11 | **Risk register is append-only via RiskStatusLog** — no row deletion; archive via Withdrawn status | OQ-2.2 |
| 12 | **EWN auto-lapse** — EWN that has not been linked to an EOT/VO claim within `ewn_lapse_days` (default 30) auto-transitions to Lapsed; subsequent claims referencing a Lapsed EWN are blocked | OQ-1.8 |

---

## 10. Forward Constraints for Downstream Modules

When future module specs are authored, they must respect M05's locked contracts:

| Module | Constraint Imposed by M05 v1.0 |
|---|---|
| **M07 EVMEngine** (future round) | MUST consume M05 `RISK_ADJUSTED_EAC_DELTA` event in EAC calculation. M05 is the sole authority on risk-adjusted forecast deltas; M07 does not maintain its own risk weighting |
| **M08 GateControl** (future round) | MUST accept M05 `CONTINGENCY_DRAWDOWN_GATE_REQUEST` events and process via stage-gate review. M08 owns the gate decision; M05 owns the trigger |
| **M10 EPCCCommand** (future round) | M05 risk heatmap + LD exposure rollup feed Command dashboard via M05 internal API. M10 does not store risk data; reads-through to M05 |
| **M11 ActionRegister** (future round) | M05 is one of the largest Decision Queue trigger emitters (10+ trigger types per OQ-2.3). M11 must accept all trigger types listed |
| **M19 ClaimsManagement** (Phase 2) | M05 emits `CLAIMS_EXPOSURE_SUMMARY` rollup. M19 (when specced) absorbs formal claim documentation; M05 retains exposure-summary view |
| **M02 StructureWBS** | Already-locked: M02 Spec line 69 + Block 7 + line 156 — Package.pending_vo_id FK to M05.VariationOrder; BOQItem.source_materialisation_id FK to M05.VOBOQMaterialisation. M02 v1.0a + v1.1 cascade note already honour this |
| **M03 PlanningMilestones** | Already-locked: M03 Spec line 184-206 BaselineExtension entity owns granted_days from M05.ExtensionOfTime; line 202 variation_order_id FK to M05 |
| **M04 ExecutionCapture** | Already-locked: M04 BR-04-021 emits NCR events to M05; BR-04-022 only M05 system writes ld_eligibility_flag. M04 v1.0a honours this |
| **M06 FinancialControl** | Already-locked: M06 BR-06-039 stub for M05 VO_APPROVED_COST_IMPACT (line 682); M06 line 708 stub for M05 LD_ELIGIBLE_AMOUNT. M06 v1.0b honours this |
| **PF03 ExternalPartyPortal** (Phase 2) | When built: revisit CLIENT_VIEWER access to VO approval workflow (potential 3rd sign-off level above threshold per OQ-1.5 deferred Option C) |

---

## 11. Deliverables Upon Spec Lock

| Round | Artefact | Cadence |
|---|---|---|
| **31 (this)** | M05_RiskChangeControl_Brief_v1_0.md | C1 (Brief, single artefact) |
| 32 | M05_RiskChangeControl_Spec_v1_0.md + X8 v0.7 cascade (M05 ENUMs: RiskProbabilityBand, RiskImpactBand, RiskResponseStrategy, VOStatus, EOTStatus, EWNStatus, plus 7-9 status sub-state ENUMs) | C1 (Spec, single artefact — cadence preserved per spec-protocol C1) |
| 33 | **M05 + M13 Wireframes** (C1b 2-Spec Buffer batch — post X8/X9 audit; M13 CorrespondenceRegister is independent peer module per dependency-first principle) | C1b batch |
| 34 | **M05 + M13 Workflows** (C1b 2-Spec Buffer batch) | C1b batch |

**Note on C1b batching of M13:** M13 CorrespondenceRegister has zero hard dependency on M05 (M13 governs project correspondence; M05 governs commercial deliberation). The two are peer modules per dependency-first principle, satisfying C1b batch constraint (no upstream→downstream dependency).

If M13 Brief and Spec rounds run before R33, the batch can proceed. If M13 is not yet through Spec, R33-R34 reverts to C1 single-module cadence (M05 only) with M13 catch-up in R35-R36.

---

## 12. Open Items Tracker

| ID | Topic | Type | Status |
|---|---|---|---|
| OQ-1.1 | Module scope — slim core (B); Claims→M19, HSE→M31, Insurance→M23 | User Decision | **CLOSED** |
| OQ-1.2 | Probability × Impact matrix — 5×5 (A); MC overlay Phase 2 | User Decision | **CLOSED** |
| OQ-1.3 | Risk scoring — numeric + RAG auto-derived (B) | User Decision | **CLOSED** |
| OQ-1.4 | Risk response types — ARTA 4-type (A); Phase 1 only | User Decision | **CLOSED** |
| OQ-1.5 | VO approval — threshold dual sign-off ₹50L (B) | User Decision | **CLOSED** |
| OQ-1.6 | EOT grant model — partial grants allowed (B) | User Decision | **CLOSED** |
| OQ-1.7 | Contingency pool — one per project (A) | User Decision | **CLOSED** |
| OQ-1.8 | Early Warning Notice — mandatory before EOT/VO claim (A) | User Decision | **CLOSED** |
| OQ-1.9 | LD enforcement — M05 calculates → M06 deducts via event (B) | User Decision | **CLOSED** |
| OQ-1.10 | Role-default views per X9 v0.4 §13.3 — proposed mapping | User Decision | **CLOSED** |
| OQ-2.1 | Lock audit events in Brief | Pattern Default | **CLOSED** |
| OQ-2.2 | Append-only ledgers (5 entities) | Pattern Default | **CLOSED** |
| OQ-2.3 | Decision Queue SLA defaults (10 triggers) | Pattern Default | **CLOSED** |
| OQ-2.4 | Speed tier defaults | Pattern Default | **CLOSED** |
| OQ-2.5 | ProjectRiskConfig entity for per-project tunables | Pattern Default | **CLOSED** |
| OQ-2.6 | Risk identification — broad raise + governed accept | Pattern Default | **CLOSED** |

**Lock criterion met:** All 16 items CLOSED. Brief LOCKED.

---

## 13. Cascade Notes (for Spec Round 32)

The M05 Spec Round 32 will produce / require:

| Cascade | Type | Target | Notes |
|---|---|---|---|
| **X8 v0.7 cascade** | New ENUMs | `X8_GlossaryENUMs_v0_7.md` (file rename via in-place patch convention — letter-suffix if patch-only OR new minor version if substantive ENUM addition; substantive expected → v0.7) | Add: `RiskProbabilityBand` (5 values), `RiskImpactBand` (5 values), `RiskResponseStrategy` (4 values: ARTA), `VOStatus` (state machine), `VOApprovalLevel` (Single / Dual), `EOTStatus` (state machine), `EWNStatus` (state machine), `RiskStatus` (state machine), `ChangeType` (TBD in Spec round), plus audit event extensions |
| **X9 v0.5 cascade** | Role-default views update + 3 new flagship pipeline pattern instances | `X9_VisualisationStandards_Spec_v0_5.md` | Add M05 row to §13.3 role-default views per OQ-1.10. Confirm 3 new flagship instances: VO Funnel (#3), LD Funnel (#4), EOT Funnel (#5). Verify 5×5 risk heatmap fits existing matrix chart variant or requires §catalogue extension |
| **M02 → M05 already locked** | Existing | M02 Spec already references M05 for VO materialisation FK fields | No new M02 cascade required in v1.0 (M02 v1.0a + v1.1 cascade note already covers) |
| **M03 → M05 already locked** | Existing | M03 Spec already references M05 for BaselineExtension.variation_order_id FK | No new M03 cascade required in v1.0 |
| **M04 → M05 already locked** | Existing | M04 BR-04-021 + BR-04-022 already define the M05 contract | No new M04 cascade |
| **M06 → M05 already locked** | Existing | M06 BR-06-039 + line 708 stub for M05 VO + LD events | No new M06 cascade |
| **M01 → M05 already locked** | Existing | M01 Spec line 619 SENDS TO M05 (Contract financial parameters) | No new M01 cascade |
| **CLAUDE.md §3 module status update** | Status update | Add M05 row to §3 status table on Brief lock | One-line VersionLog activity entry |
| **CLAUDE.md §4 OQ-1 row sequencing** | One-line note | Round 31 — M05 Brief reassignment vs original "Monorepo scaffold" plan | Brief commit message notes; CLAUDE.md §4 update can fold into next governance commit |
| **M05 Spec Appendix A — Audit Events Catalogue** | New section | M05 Spec Round 32 | Per OQ-2.1 — lock event names from authoring. Estimated 28-32 events |
| **ProjectRiskConfig entity** | New | M05 Spec Round 32 Block 3 | Per OQ-2.5 — avoids further M01 cascade for M05-specific tunables |

### Modules unblocked by M05 lock

- **M07 EVMEngine** — needs M05 risk-adjusted EAC delta inputs for forecast computation
- **M08 GateControl** — needs M05 contingency drawdown gate request contract
- **M10 EPCCCommand** — needs M05 risk heatmap + LD exposure for Command dashboard
- **M11 ActionRegister** — needs M05 Decision Queue trigger inventory (M05 is one of the largest emitters)
- **M19 ClaimsManagement** (Phase 2) — needs M05 claims exposure summary as upstream contract
- **M13 CorrespondenceRegister** — peer module; can batch with M05 in C1b cadence at Round 33-34 if its Brief+Spec land first

---

## Appendix A — Proposed Audit Events Catalogue (locked from authoring)

Per OQ-2.1 — events locked at Brief stage so Spec is a re-statement, not a re-issue.

### A.1 Risk events
- `RISK_RAISED` — Risk created in Draft state
- `RISK_ACCEPTED` — Risk transitions Draft → Active
- `RISK_SCORE_CHANGED` — probability_score or impact_score modified
- `RISK_RESPONSE_PLAN_UPDATED` — response_strategy or response_action_plan modified
- `RISK_CLOSED` — Risk transitions to Closed (mitigated / no longer relevant)
- `RISK_WITHDRAWN` — Risk transitions to Withdrawn (raised in error)

### A.2 Change + VO events
- `CHANGE_RAISED`
- `CHANGE_CLASSIFIED`
- `VO_DRAFTED`
- `VO_ASSESSED` — QS_MANAGER cost impact assessment complete
- `VO_APPROVED` — single or dual sign-off complete
- `VO_REJECTED`
- `VO_MATERIALISED` — M02 confirms BOQ updates complete
- `VO_CLOSED`
- `VO_APPROVED_COST_IMPACT` — emit to M06 (BR-06-039 contract)
- `VO_MATERIALISATION_FAILED` — M02 sync error (Critical Decision Queue)

### A.3 EOT events
- `EOT_CLAIM_RAISED`
- `EOT_UNDER_ASSESSMENT`
- `EOT_GRANTED` — full or partial; granted_days populated
- `EOT_REJECTED`
- `EOT_WITHDRAWN`
- `EOT_BASELINE_CASCADE_TRIGGERED` — emit to M03
- `EOT_BASELINE_CASCADE_FAILED` — M03 sync error (Critical Decision Queue)

### A.4 Early Warning Notice events
- `EWN_RAISED`
- `EWN_LINKED_TO_CLAIM` — EWN attached to subsequent EOT or VO
- `EWN_CLOSED`
- `EWN_LAPSED` — auto-transition after ewn_lapse_days

### A.5 Liquidated Damages events
- `LD_ELIGIBILITY_FLIPPED_TRUE` — M05 system call to M04 BR-04-022 (NCR aging crossed threshold)
- `LD_ELIGIBILITY_FLIPPED_FALSE` — NCR closed before LD finalised; reversal
- `LD_AMOUNT_CALCULATED` — emit to M06 LD_ELIGIBLE_AMOUNT
- `LD_CAP_APPROACHING` — cumulative ≥ 80%
- `LD_CAP_REACHED` — cumulative = 100%; further accrual blocked

### A.6 Contingency events
- `CONTINGENCY_DRAWDOWN_RAISED`
- `CONTINGENCY_DRAWDOWN_APPROVED` — single or dual sign-off
- `CONTINGENCY_DRAWDOWN_REJECTED`
- `CONTINGENCY_POOL_DEPLETION_HIGH` — ≥ 80%
- `CONTINGENCY_POOL_DEPLETION_CRITICAL` — ≥ 95%
- `CONTINGENCY_DRAWDOWN_GATE_REQUEST` — emit to M08 (above stage-gate threshold)

### A.7 Cross-module emit events
- `RISK_ADJUSTED_EAC_DELTA` — emit to M07 (quarterly batch)
- `CLAIMS_EXPOSURE_SUMMARY` — emit to M19 (Phase 2; rollup view)

**Estimated total:** 30 events (A.1: 6 + A.2: 10 + A.3: 7 + A.4: 4 + A.5: 5 + A.6: 6 + A.7: 2 — minus 10 because some events span sections). Round 32 Spec finalises exact count.

---

## What This Brief Does NOT Cover

- **Long-form claims management** (deferred to M19 ClaimsManagement Phase 2)
- **HSE risk** (deferred to M31 HSESafetyManagement Phase 2)
- **Insurance management** (deferred to M23 BGInsuranceTracker)
- **Regulatory / clinical compliance NCRs** (M09 ComplianceTracker owns; M05 handles construction NCRs only — sourced from M04)
- **Stage gate decision-making** (M08 GateControl owns; M05 raises gate requests for above-threshold drawdowns)
- **EVM EAC algorithm internals** (M07 owns; M05 emits delta input only)
- **DLP retention release** (M15 owns DLP signal; M06 owns financial release; M05 NOT in this chain per M06 v1.1 cascade note H6)
- **Risk-bearing portfolio decisions** (PIOE Phase 2; M05 emits aggregated heatmap, PIOE consumes for portfolio optimisation)
- **Monte Carlo quantitative risk analysis** (Phase 2 cascade extension to OQ-1.2 = A)

---

*v1.0 — Brief LOCKED. All 16 OQ items CLOSED. Ready for Round 32 Spec authoring.*
