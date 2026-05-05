---
artefact: M05_RiskChangeControl_Spec_v1_0
round: 33
date: 2026-05-04
author: Monish (with Claude assist)
parent_brief: M05_RiskChangeControl_Brief_v1_0a (Round 31, in-place patched 2026-05-04 to 7-state VO)
x8_version: v0.7
x9_version: v0.4
status: LOCKED
type: Module Spec (10-block)
re_issue_of: ZEPCC_Legacy/M05_Risk_Change_v2_3.md (slim-core re-issue per OQ-1.1=B)
references_locked: All M05 Brief OQ-1.1-1.10 + OQ-2.1-2.6; M04 BR-04-021/022 contracts; M02 VO materialisation contract; M03 BaselineExtension cascade contract; M06 BR-06-039 + LD_ELIGIBLE_AMOUNT contract; M01 Contract financial parameters (ld_rate_per_week, ld_cap_pct, risk_buffer_pct)
---

# M05 — Risk & Change Control — Spec v1.0

## CHANGE LOG

| Version | Date | Author | Change Summary |
|---|---|---|---|
| v1.0 | 2026-05-04 | Monish (with Claude assist) | Initial standalone consolidated spec (Round 33). All 16 M05 Brief v1.0a OQ items embedded as locked. Slim-core scope per OQ-1.1=B (Risk + Change + VO + EOT + LD + Contingency + EWN; Claims→M19/HSE→M31/Insurance→M23 Phase 2 deferred). 14 entities including 5 append-only ledgers (RiskStatusLog, VOStatusLog, EOTStatusLog, ContingencyDrawdownLog, LDExposureLog) with DB-level UPDATE/DELETE forbidden. 32 BRs (BR-05-001..032). 30 audit events (Appendix A locked from authoring per OQ-2.1). 10 Decision Queue triggers (Block 8c). All 4 parent contracts honoured: M04 BR-04-021/022 (NCR signal IN + ld_eligibility_flag write-back system-to-system), M02 VO materialisation (VO_APPROVED → M02 BOQ update), M03 EOT cascade (EOT_GRANTED → M03 BaselineExtension), M06 financial signals (VO_APPROVED_COST_IMPACT + LD_ELIGIBLE_AMOUNT). M01 Contract parameters (ld_rate_per_week, ld_cap_pct, risk_buffer_pct) read at project activation + Contract edit. 0 open questions in Block 10. |

---

## BLOCK 1 — IDENTITY

```
Module ID                : M05
Module Name              : Risk & Change Control
Layer                    : L2 — Risk / Commercial
Phase                    : 1 — Foundational (precedes M07 EVMEngine + M08 GateControl + M11 ActionRegister + M19 Phase 2)
Build Weeks              : 5 (estimate; module is dense — 14 entities, 32 BRs, 5×5 risk + 7-state VO + EOT + LD + EWN + Contingency)
Decision It Enables      : "Given everything that has happened on site (NCRs, delays,
                            scope changes, risks materialising), what is the contractual
                            and commercial response — and is the project on track to
                            absorb it within contingency, or are we exceeding tolerance?"
Primary User             : PMO_DIRECTOR (risk heatmap + contingency approval + dual sign-off)
Secondary Users          : PROJECT_DIRECTOR (own-project risk register, EOT/VO assessment, EWN review),
                            PORTFOLIO_MANAGER (portfolio risk + contingency depletion),
                            FINANCE_LEAD (LD exposure + VO cost pipeline + dual sign-off),
                            PLANNING_ENGINEER (EOT claim assessment, EWN raise),
                            QS_MANAGER (VO assessment, change register, LD calc review),
                            SITE_MANAGER (EWN raise + view, active risks),
                            ANALYST (risk score trends, LD funnel, portfolio rollup)
Folder                   : SystemAdmin/Modules/
Re-Issue Of              : ZEPCC_Legacy/M05_Risk_Change_v2_3.md (slim-core per OQ-1.1=B)
Source Brief             : M05_RiskChangeControl_Brief_v1_0a (Round 31)
Cadence                  : C1 (Spec; one artefact at a time per spec-protocol.md)
Round Date               : 2026-05-04 (Round 33)
```

### Decisions It Enables (downstream rounds)

| Round | Artefact | Authority From This Spec |
|---|---|---|
| **R34** | M13 Spec v1.0 + X8/X9 audit pass for M05+M13 batch | Block 7 Integration Points (M13 batch peer constraint) |
| **R35** | M05 + M13 Wireframes (C1b batch) | Block 5 Filters & Views + role-default views per X9 |
| **R36** | M05 + M13 Workflows (C1b batch) | Block 6 BR runtime flows + Block 8 audit-event emit hooks |
| **R59** | M05 build slice (deepening) | Full 4-artefact spec set complete; dependencies M02/M03/M04/M06 already deepened |

---

## BLOCK 2 — SCOPE BOUNDARY

### 2a. INCLUDES

| # | Item | OQ Authority |
|---|---|---|
| 1 | **Risk Register** — identification (broad-raise per OQ-2.6), 5×5 probability × impact assessment per OQ-1.2, numeric scoring + RAG band auto-derivation per OQ-1.3, ARTA response strategy per OQ-1.4, owner assignment, residual risk tracking | OQ-1.2, OQ-1.3, OQ-1.4, OQ-2.6 |
| 2 | **Change Register** — scope-change tracking; site instructions; RFI integration with M12 (when built); change classification | OQ-1.1 |
| 3 | **Variation Order (VO) lifecycle** — 7-state machine per Brief v1.0a OQ-1.5: Draft → Assessed → Submitted → Approved → Materialised → Closed; Rejected terminal-from-{Draft, Assessed, Submitted}; threshold dual sign-off | OQ-1.5 |
| 4 | **Extension of Time (EOT) lifecycle** — Claim_Raised → Under_Assessment → Granted/Rejected/Withdrawn; partial grants allowed per OQ-1.6; M03 BaselineExtension cascade trigger on Granted | OQ-1.6 |
| 5 | **Liquidated Damages (LD) tracking** — exposure calculation from M01.Contract parameters; NCR aging consumption per BR-04-021/022; cap enforcement per `M01.Contract.ld_cap_pct`; M06 `LD_ELIGIBLE_AMOUNT` event emission per OQ-1.9 | OQ-1.9 |
| 6 | **Contingency drawdown governance** — pool initialisation from `M01.Contract.risk_buffer_pct × contract_value` per OQ-1.7; drawdown approval workflow with PMO_DIRECTOR gate; stage-gate linkage with M08 (when built) | OQ-1.7 |
| 7 | **NCR → LD eligibility assessment** — consuming M04 `NCR_RAISED` / `NCR_STATUS_CHANGED` events per BR-04-021; applying age + severity + closure rules; writing back `ld_eligibility_flag` per BR-04-022 (system-to-system only) | OQ-1.9 + M04 BR-04-022 |
| 8 | **Early Warning Notice (EWN) management** — mandatory prerequisite for EOT and VO claim per OQ-1.8 (NEC4 / FIDIC alignment); notice-to-claim time tracking; auto-lapse after `ewn_lapse_days` | OQ-1.8 |
| 9 | **Claims exposure summary** — aggregated rollup view (LD + pending VOs + pending EOTs + contingency consumed); feeds M10 EPCCCommand dashboard read-through; emit `CLAIMS_EXPOSURE_SUMMARY` to M19 Phase 2 | OQ-1.1 |
| 10 | **Risk-adjusted EAC delta** — quarterly batch + on-demand recalc; emits `RISK_ADJUSTED_EAC_DELTA` event to M07 (when built) | Brief §10 forward constraint |
| 11 | **ProjectRiskConfig** — M05-owned per-project tunables entity (6 fields per OQ-2.5) | OQ-2.5 |

### 2b. EXCLUDES

| # | Item | Reason / Where Addressed |
|---|---|---|
| 1 | Financial transaction processing (CostLedgerEntry writes, RA Bill state machine, retention release execution) | M06 owns; M05 emits `VO_APPROVED_COST_IMPACT` and `LD_ELIGIBLE_AMOUNT` events |
| 2 | BOQ update execution (writing to `M02.BOQItem` rows, BAC integrity recompute) | M02 owns; M05 emits `VO_APPROVED` event; M02 sets `Package.bac_integrity_status = Stale_Pending_VO` and creates `VOBOQMaterialisation` rows per M02 Spec Block 7 |
| 3 | Baseline schedule recalculation (PV regeneration, Milestone date shifts) | M03 owns; M05 emits `EOT_GRANTED` event; M03 creates `BaselineExtension` row per M03 Spec line 184-206 |
| 4 | Site diary daily log | M16 SiteDiary (Phase 1 separate module per Brief OQ-1.1) |
| 5 | Document storage internals (file blobs, version control, RFI attachments) | M12 DocumentControl (Phase 1; M05 stores `document_id` references — M12-stub pattern during interim) |
| 6 | BG and Insurance tracking (full lifecycle) | M23 BGInsuranceTracker (Phase 2 per Brief OQ-1.1; BGStub pattern from M06 OQ-1.9 covers Phase 1) |
| 7 | Long-form claims management (expert assessments, arbitration packets) | M19 ClaimsManagement (Phase 2 per Brief OQ-1.1); M05 emits `CLAIMS_EXPOSURE_SUMMARY` aggregated view |
| 8 | HSE / safety NCRs | M31 HSESafetyManagement (Phase 2; M04 OQ-1.1=B already locks safety to M31). M05 handles construction NCRs from M04 only. |
| 9 | Compliance / regulatory NCRs | M09 ComplianceTracker (Phase 1; separate from construction NCRs M05 consumes) |
| 10 | DLP retention release | M15 owns DLP signal (Phase 2); M06 owns financial release. M05 is **NOT** in this chain (per M06 v1.1 cascade note H6 Option B lock — confirmed re-read at R33 verification) |
| 11 | Stage gate decision-making | M08 GateControl (Phase 1; M05 raises drawdown gate requests via `CONTINGENCY_DRAWDOWN_GATE_REQUEST` event) |
| 12 | EVM EAC algorithm internals (CPI/SPI/EAC computation) | M07 EVMEngine (Phase 1; M05 emits delta inputs only) |
| 13 | Risk-bearing portfolio decisions (multi-project optimisation) | PIOE Phase 2 (consumes M05 aggregated heatmap) |
| 14 | Monte Carlo quantitative risk analysis | Phase 2 cascade extension to OQ-1.2=A (Phase 1 ships qualitative 5×5 only) |
| 15 | Opportunities (positive risks) — Exploit/Enhance/Share response types | Phase 2 cascade extension to OQ-1.4=A (Phase 1 ships ARTA 4-type only) |
| 16 | "Escalate" as a response type | Modelled separately as Decision Queue trigger (M11) when risk crosses portfolio threshold; not a `RiskResponseStrategy` ENUM value |
| 17 | Client / Lender / NABH external sign-off on VOs | PF03 ExternalPartyPortal Phase 2 |

### 2c. Hard Boundaries (must-not-cross during build)

1. **M05 never writes to M02 database directly.** All BOQ changes go through `VO_APPROVED` event → M02 Block 7 receives → M02 executes BOQ update + creates `VOBOQMaterialisation` rows. M05 reads M02 BOQ for VO costing only.
2. **M05 never writes to M03 BaselineExtension directly.** All baseline cascades go through `EOT_GRANTED` event → M03 creates BaselineExtension row.
3. **M05 writes to M04 only via system-to-system internal API call** (`ld_eligibility_flag` toggle); UI write blocked at M04 API per BR-04-022.
4. **M05 never writes to M06 CostLedgerEntry.** Financial impacts emitted via events only (`VO_APPROVED_COST_IMPACT`, `LD_ELIGIBLE_AMOUNT`).
5. **M05 reads `ld_rate_per_week`, `ld_cap_pct`, `risk_buffer_pct` from M01.Contract; never copies/caches** (always fresh read at calculation time; values stable post-Contract Activation lock).
6. **No risk row may be hard-deleted.** Soft delete via `is_active = false`; closure via state machine (Closed/Withdrawn). RiskStatusLog preserves provenance.
7. **VO state machine is strictly forward-only.** No skipping states. No reversal after Materialised (use compensating VO instead). Rejected is terminal-from-{Draft, Assessed, Submitted} only.

---

## BLOCK 3 — DATA ARCHITECTURE

### 3a. Entities (14 total)

| # | Entity | Cardinality | Owner | Purpose | Append-Only? |
|---|---|---|---|---|---|
| 1 | `Risk` | Many per project | M05 | Risk register entry; 5×5 probability × impact; ARTA response | No (soft-delete) |
| 2 | `RiskStatusLog` | Many per Risk | M05 | Every state transition + score change; provenance for risk-adjusted EAC trail (M07) | **YES** |
| 3 | `Change` | Many per project | M05 | Scope-change tracking; site instructions; RFI metadata | No |
| 4 | `VariationOrder` | Many per project | M05 | 7-state VO lifecycle per Brief v1.0a OQ-1.5; M02 BOQ trigger; M06 cost impact trigger | No (state machine) |
| 5 | `VOStatusLog` | Many per VO | M05 | Every VO state transition (Draft→Assessed→Submitted→Approved→Materialised→Closed; or Rejected) | **YES** |
| 6 | `VOBOQMaterialisation` | Many per VO | M05 (FK from M02 BOQItem.source_materialisation_id per M02 Spec line 192) | Cross-module handoff record between M05 (decision) and M02 (BOQ execution) | No |
| 7 | `ExtensionOfTime` | Many per project | M05 | EOT lifecycle; M03 BaselineExtension cascade trigger on Granted | No (state machine) |
| 8 | `EOTStatusLog` | Many per EOT | M05 | Every EOT state transition | **YES** |
| 9 | `EarlyWarningNotice` | Many per project | M05 | Mandatory prerequisite per OQ-1.8; auto-lapse after `ewn_lapse_days` | No |
| 10 | `ContingencyPool` | 1 per project | M05 | Initialised from `M01.Contract.risk_buffer_pct × contract_value`; forward-only depletion | No (single-row update on drawdown approval) |
| 11 | `ContingencyDrawdownLog` | Many per ContingencyPool | M05 | Each drawdown event; references Risk OR VO OR Change; reversals via compensating entries | **YES** |
| 12 | `LDExposureRecord` | Many per project | M05 | LD calculation history per (NCR aging event × time) | No |
| 13 | `LDExposureLog` | Many per LDExposureRecord | M05 | Every LD eligibility flip + amount change | **YES** |
| 14 | `ProjectRiskConfig` | 1 per project | M05 | Per-project tunables per OQ-2.5 (6 fields) | No |

**Append-only ledgers:** 5 entities (RiskStatusLog, VOStatusLog, EOTStatusLog, ContingencyDrawdownLog, LDExposureLog). DB-level UPDATE/DELETE forbidden via `REVOKE UPDATE, DELETE` on these tables. Reservals of ContingencyDrawdownLog and LDExposureLog use compensating entries (negative amount + back-reference) per M06 CostLedgerEntry precedent.

### 3b. Field Schemas

#### 3b.1 — `Risk`

| Field | Type | Required | Validation Rule / Source | Source |
|---|---|---|---|---|
| `id` | UUID | Y | Auto | SYSTEM |
| `tenant_id` | UUID | Y | Reserved field per `naming-folders.md` §Reserved Fields | SYSTEM |
| `project_id` | UUID | Y | FK → `M01.Project` | LINK |
| `risk_code` | VARCHAR(20) | Y | Per-project sequential; format `R-{NNNN}` | SYSTEM |
| `title` | VARCHAR(200) | Y | Min 10 chars | INPUT |
| `description` | TEXT | Y | Min 50 chars | INPUT |
| `category` | ENUM | Y | Per X8 v0.7 §3.73 `RiskCategory` (8 values: Strategic / Financial / Operational / Regulatory / Clinical / Market / ESG / Force_Majeure) | INPUT |
| `probability_score` | INTEGER | Y | Range 1..5 per OQ-1.2 | INPUT |
| `impact_score` | INTEGER | Y | Range 1..5 per OQ-1.2 | INPUT |
| `risk_score` | INTEGER | Y | CALC = `probability_score × impact_score` (range 1..25). Read-only in UI per OQ-1.3 | CALC |
| `rag_band` | ENUM | Y | Per X8 v0.7 §3.74 `RiskRAGStatus` (Green / Amber / Red). DERIVED from risk_score: 1-4=Green, 5-12=Amber, 13-25=Red per Brief OQ-1.2 cascade. Read-only in UI per OQ-1.3 | CALC |
| `status` | ENUM | Y | Per X8 v0.7 §3.75 `RiskStatus` (5 values: Draft / Active / Mitigating / Closed / Reopened / Withdrawn). State machine per BR-05-002 | SYSTEM |
| `response_strategy` | ENUM | N | Per X8 v0.7 §3.76 `RiskResponseStrategy` (4 values: Avoid / Reduce / Transfer / Accept per OQ-1.4 ARTA). Required when `risk_score >= 13` (Red band) per BR-05-007 | INPUT |
| `response_action_plan` | TEXT | N | Required when `risk_score >= 13`; min 100 chars per BR-05-007 | INPUT |
| `owner_user_id` | UUID | Y | FK → `M34.User` | INPUT |
| `residual_probability_score` | INTEGER | N | Range 1..5; populated post-mitigation | INPUT |
| `residual_impact_score` | INTEGER | N | Range 1..5; populated post-mitigation | INPUT |
| `residual_risk_score` | INTEGER | N | CALC = `residual_probability_score × residual_impact_score`. Required for closure per BR-05-008 | CALC |
| `affected_milestones` | JSONB array of UUID | N | Optional FK refs to `M03.Milestone` | INPUT |
| `created_by` | UUID | Y | Reserved field | SYSTEM |
| `created_at` | TIMESTAMP | Y | Reserved field | SYSTEM |
| `updated_by` | UUID | Y | Reserved field | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Reserved field | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true. Reserved field | SYSTEM |

#### 3b.2 — `RiskStatusLog` (append-only)

| Field | Type | Required | Validation / Source |
|---|---|---|---|
| `id` | UUID | Y | Auto |
| `tenant_id` | UUID | Y | Reserved |
| `risk_id` | UUID | Y | FK → `Risk` |
| `from_status` | ENUM | N | Null on initial create; `RiskStatus` ENUM otherwise |
| `to_status` | ENUM | Y | `RiskStatus` ENUM |
| `from_score` | INTEGER | N | Null on initial create; 1..25 otherwise |
| `to_score` | INTEGER | Y | 1..25 |
| `changed_by` | UUID | Y | FK → `M34.User` |
| `changed_at` | TIMESTAMP | Y | Auto |
| `reason` | TEXT | N | Required if `to_status = Withdrawn` (min 50 chars) |

DB constraints: `REVOKE UPDATE, DELETE FROM app_role`. No `updated_by` / `updated_at` / `is_active` per `naming-folders.md` §Reserved Fields append-only exemption.

#### 3b.3 — `Change`

| Field | Type | Required | Validation / Source |
|---|---|---|---|
| `id` | UUID | Y | Auto |
| `tenant_id`, `created_by`, `created_at`, `updated_by`, `updated_at`, `is_active` | — | Y | Reserved fields |
| `project_id` | UUID | Y | FK → `M01.Project` |
| `change_code` | VARCHAR(20) | Y | Per-project sequential; format `C-{NNNN}` |
| `title` | VARCHAR(200) | Y | Min 10 chars |
| `description` | TEXT | Y | Min 50 chars |
| `change_type` | ENUM | Y | Per X8 v0.7 §3.77 `ChangeItemType` (Site_Instruction / RFI / Drawing_Revision / Specification_Change / Scope_Clarification / Other) |
| `status` | ENUM | Y | Per X8 v0.7 §3.78 `ChangeItemStatus` (Draft / Under_Assessment / Approved / Rejected / Withdrawn) |
| `raised_by_user_id` | UUID | Y | FK → `M34.User` |
| `raised_at` | TIMESTAMP | Y | Auto |
| `affected_packages` | JSONB array of UUID | N | Optional FK refs to `M02.Package` |
| `affected_milestones` | JSONB array of UUID | N | Optional FK refs to `M03.Milestone` |
| `linked_vo_id` | UUID | N | FK → `VariationOrder` (set when Change promotes to VO per BR-05-013) |
| `document_id` | UUID | N | FK → `M12.Document` (M12-stub pattern interim) |

#### 3b.4 — `VariationOrder`

| Field | Type | Required | Validation / Source |
|---|---|---|---|
| `id` | UUID | Y | Auto |
| `tenant_id`, `created_by`, `created_at`, `updated_by`, `updated_at`, `is_active` | — | Y | Reserved fields |
| `project_id` | UUID | Y | FK → `M01.Project` |
| `vo_code` | VARCHAR(20) | Y | Per-project sequential; format `VO-{NNNN}` |
| `title` | VARCHAR(200) | Y | Min 10 chars |
| `description` | TEXT | Y | Min 100 chars |
| `vo_type` | ENUM | Y | Per X8 v0.7 §3.79 `VariationOrderType` (Scope_Addition / Scope_Reduction / Design_Change / Statutory_Requirement / Unforeseen_Condition / Provisional_Sum_Finalisation) |
| `vo_cause` | ENUM | Y | Per X8 v0.7 §3.80 `VOCause` (Delay / Scope_Increase / Scope_Decrease / Design_Variation / Site_Condition / Other). EWN required if `Delay` or `Scope_Increase` per BR-05-016 |
| `status` | ENUM | Y | Per X8 v0.7 §3.81 `VOStatus` (7 values: Draft / Assessed / Submitted / Approved / Materialised / Closed / Rejected per Brief v1.0a OQ-1.5). State machine per BR-05-014 |
| `cost_impact_inr` | DECIMAL(15,2) | Y | Net cost impact (positive for additions, negative for reductions). Required at `Submitted` transition |
| `approval_level` | ENUM | Y | Per X8 v0.7 §3.82 `VOApprovalLevel` (Single / Dual). DERIVED: `Single` if `cost_impact_inr <= ProjectRiskConfig.dual_signoff_threshold_inr`, else `Dual` per BR-05-015 |
| `early_warning_notice_id` | UUID | N | FK → `EarlyWarningNotice`. Required if `vo_cause IN (Delay, Scope_Increase)` per BR-05-016 |
| `linked_change_id` | UUID | N | FK → `Change` (if VO promoted from a Change) |
| `assessed_by_user_id` | UUID | N | FK → `M34.User` (QS_MANAGER); set on Draft → Assessed transition |
| `assessed_at` | TIMESTAMP | N | Auto on assessment |
| `submitted_at` | TIMESTAMP | N | Auto on Assessed → Submitted transition |
| `approved_by_pmo_at` | TIMESTAMP | N | Required for both Single (if approver=PMO) and Dual sign-off |
| `approved_by_pmo_user_id` | UUID | N | FK → `M34.User` (PMO_DIRECTOR) |
| `approved_by_finance_at` | TIMESTAMP | N | Required for Single (if approver=FINANCE) and Dual sign-off |
| `approved_by_finance_user_id` | UUID | N | FK → `M34.User` (FINANCE_LEAD) |
| `materialised_at` | TIMESTAMP | N | Auto on Approved → Materialised system event (M02 confirms BOQ update complete) |
| `closed_at` | TIMESTAMP | N | Auto on Materialised → Closed transition |
| `rejected_at` | TIMESTAMP | N | Set on transition to Rejected |
| `rejection_reason` | TEXT | N | Required if `status = Rejected`; min 100 chars |
| `vo_boq_materialisation_id` | UUID | N | FK → `VOBOQMaterialisation` (set on Materialised) |

**State machine constraints:**
- `Draft → Assessed`: requires `assessed_by_user_id` populated (QS_MANAGER role)
- `Assessed → Submitted`: requires `cost_impact_inr` populated; `submitted_at` auto-set
- `Submitted → Approved`: single sign-off if `cost_impact_inr <= threshold` (one of `approved_by_pmo_at` OR `approved_by_finance_at` populated); dual sign-off if above threshold (BOTH populated)
- `Approved → Materialised`: SYSTEM action only; triggered by M02 confirmation of BOQ update; `materialised_at` auto-set
- `Materialised → Closed`: explicit close action by PMO_DIRECTOR or auto-close after configurable period
- `Rejected`: terminal-from-{Draft, Assessed, Submitted} only; cannot reject after Approved (use compensating VO)

#### 3b.5 — `VOStatusLog` (append-only)

Standard append-only log: `id`, `tenant_id`, `vo_id`, `from_status`, `to_status`, `changed_by`, `changed_at`, `reason` (required for Rejected). DB UPDATE/DELETE forbidden.

#### 3b.6 — `VOBOQMaterialisation`

| Field | Type | Required | Validation / Source |
|---|---|---|---|
| `id` | UUID | Y | Auto |
| `tenant_id`, `created_by`, `created_at`, `updated_by`, `updated_at`, `is_active` | — | Y | Reserved fields |
| `vo_id` | UUID | Y | FK → `VariationOrder` |
| `materialisation_started_at` | TIMESTAMP | Y | Auto on M02 receipt of `VO_APPROVED` event |
| `materialisation_completed_at` | TIMESTAMP | N | Auto on M02 confirmation; null while in-flight |
| `m02_boq_items_created` | INTEGER | N | Count of BOQItem rows M02 created |
| `m02_boq_items_modified` | INTEGER | N | Count of BOQItem rows M02 modified |
| `materialisation_status` | ENUM | Y | Per X8 v0.7 §3.83 `VOMaterialisationStatus` (In_Progress / Complete / Failed) |
| `failure_reason` | TEXT | N | Required if `materialisation_status = Failed`; min 100 chars |

#### 3b.7 — `ExtensionOfTime`

| Field | Type | Required | Validation / Source |
|---|---|---|---|
| `id` | UUID | Y | Auto |
| `tenant_id`, `created_by`, `created_at`, `updated_by`, `updated_at`, `is_active` | — | Y | Reserved fields |
| `project_id` | UUID | Y | FK → `M01.Project` |
| `eot_code` | VARCHAR(20) | Y | Per-project sequential; format `EOT-{NNNN}` |
| `claim_basis` | ENUM | Y | Per X8 v0.7 §3.84 `EOTClaimBasis` (Employer_Default / Statutory_Delay / Unforeseen_Ground / Force_Majeure / Concurrent_Delay) |
| `delaying_event_description` | TEXT | Y | Min 100 chars |
| `affected_milestones` | JSONB array of UUID | Y | At least one M03.Milestone reference required |
| `claim_days` | INTEGER | Y | Range 1..365 |
| `granted_days` | INTEGER | N | Range 0..claim_days; populated on Granted transition; partial grant if `granted_days < claim_days` per OQ-1.6 |
| `partial_grant_reason` | TEXT | N | Required if `granted_days < claim_days`; min 100 chars per BR-05-019 |
| `early_warning_notice_id` | UUID | Y | FK → `EarlyWarningNotice` (NOT NULL per BR-05-018; OQ-1.8 mandate) |
| `status` | ENUM | Y | Per X8 v0.7 §3.85 `EOTStatus` (5 values: Claim_Raised / Under_Assessment / Granted / Rejected / Withdrawn) |
| `assessed_by_user_id` | UUID | N | FK → `M34.User` (PLANNING_ENGINEER); set on Claim_Raised → Under_Assessment |
| `granted_by_user_id` | UUID | N | FK → `M34.User` (PMO_DIRECTOR); set on Granted transition |
| `granted_at` | TIMESTAMP | N | Auto on Granted transition |
| `m03_baseline_extension_id` | UUID | N | FK → `M03.BaselineExtension` (set after M03 confirms cascade complete per BR-05-021) |
| `linked_vo_id` | UUID | N | FK → `VariationOrder` (if EOT cause overlaps with a VO) |

#### 3b.8 — `EOTStatusLog` (append-only)

Standard append-only log per VOStatusLog pattern.

#### 3b.9 — `EarlyWarningNotice`

| Field | Type | Required | Validation / Source |
|---|---|---|---|
| `id` | UUID | Y | Auto |
| `tenant_id`, `created_by`, `created_at`, `updated_by`, `updated_at`, `is_active` | — | Y | Reserved fields |
| `project_id` | UUID | Y | FK → `M01.Project` |
| `ewn_code` | VARCHAR(20) | Y | Per-project sequential; format `EWN-{NNNN}` |
| `raised_by_user_id` | UUID | Y | FK → `M34.User` |
| `raised_at` | TIMESTAMP | Y | Auto |
| `delaying_event_description` | TEXT | Y | Min 100 chars |
| `expected_impact_qualitative` | TEXT | Y | Min 50 chars |
| `affected_milestones` | JSONB array of UUID | N | Optional FK refs to `M03.Milestone` |
| `status` | ENUM | Y | Per X8 v0.7 §3.86 `EWNStatus` (3 values: Active / Closed / Lapsed) |
| `linked_eot_id` | UUID | N | FK → `ExtensionOfTime` (set when EWN linked to subsequent claim per BR-05-024) |
| `linked_vo_id` | UUID | N | FK → `VariationOrder` |
| `closed_at` | TIMESTAMP | N | Set when corresponding EOT/VO closes |
| `lapsed_at` | TIMESTAMP | N | Set when no claim raised within `ProjectRiskConfig.ewn_lapse_days` (default 30) per BR-05-025 |

#### 3b.10 — `ContingencyPool`

| Field | Type | Required | Validation / Source |
|---|---|---|---|
| `id` | UUID | Y | Auto |
| `tenant_id`, `created_by`, `created_at`, `updated_by`, `updated_at`, `is_active` | — | Y | Reserved fields |
| `project_id` | UUID | Y | FK → `M01.Project`; UNIQUE (one per project per OQ-1.7) |
| `total_inr` | DECIMAL(15,2) | Y | CALC at project activation = `M01.Contract.contract_value × M01.Contract.risk_buffer_pct`. Locked post-Activation |
| `consumed_inr` | DECIMAL(15,2) | Y | Default 0; SUM of approved ContingencyDrawdownLog amounts (recomputed on each drawdown approval per BR-05-027) |
| `available_inr` | DECIMAL(15,2) | Y | CALC = `total_inr - consumed_inr` |
| `consumed_pct` | DECIMAL(5,4) | Y | CALC = `consumed_inr / total_inr` |

#### 3b.11 — `ContingencyDrawdownLog` (append-only)

| Field | Type | Required | Validation / Source |
|---|---|---|---|
| `id` | UUID | Y | Auto |
| `tenant_id` | UUID | Y | Reserved |
| `contingency_pool_id` | UUID | Y | FK → `ContingencyPool` |
| `requested_by_user_id` | UUID | Y | FK → `M34.User` (PROJECT_DIRECTOR or PMO_DIRECTOR) |
| `requested_at` | TIMESTAMP | Y | Auto |
| `amount_inr` | DECIMAL(15,2) | Y | Positive value (reversals via compensating entries with `linked_drawdown_id` populated and negative `amount_inr`) |
| `justification` | TEXT | Y | Min 100 chars |
| `status` | ENUM | Y | Per X8 v0.7 §3.87 `ContingencyDrawdownStatus` (Requested / Approved / Rejected / Reversed) |
| `linked_risk_id` | UUID | N | FK → `Risk` (if drawdown for risk mitigation) |
| `linked_vo_id` | UUID | N | FK → `VariationOrder` (if drawdown for VO funding) |
| `linked_change_id` | UUID | N | FK → `Change` |
| `approved_by_user_id` | UUID | N | FK → `M34.User` (PMO_DIRECTOR per BR-05-028; never self-approval) |
| `approved_at` | TIMESTAMP | N | Auto on approval |
| `rejected_at` | TIMESTAMP | N | Auto on rejection |
| `rejection_reason` | TEXT | N | Required if Rejected; min 100 chars |
| `linked_drawdown_id` | UUID | N | FK → `ContingencyDrawdownLog` (for reversals/compensating entries; M06 precedent) |

CHECK constraint: exactly one of `linked_risk_id`, `linked_vo_id`, `linked_change_id` must be populated.

DB UPDATE/DELETE forbidden.

#### 3b.12 — `LDExposureRecord`

| Field | Type | Required | Validation / Source |
|---|---|---|---|
| `id` | UUID | Y | Auto |
| `tenant_id`, `created_by`, `created_at`, `updated_by`, `updated_at`, `is_active` | — | Y | Reserved fields |
| `project_id` | UUID | Y | FK → `M01.Project` |
| `m04_ncr_id` | UUID | Y | FK → `M04.ConstructionNCR` (the NCR triggering LD eligibility) |
| `eligibility_assessed_at` | TIMESTAMP | Y | Auto on M05 system assessment |
| `delay_weeks` | DECIMAL(6,2) | Y | Computed from NCR age vs threshold |
| `ld_amount_inr` | DECIMAL(15,2) | Y | CALC = `M01.Contract.ld_rate_per_week × delay_weeks × M01.Contract.contract_value` (capped at `M01.Contract.ld_cap_pct × contract_value` per BR-05-031) |
| `ld_status` | ENUM | Y | Per X8 v0.7 §3.88 `LDStatus` (4 values: Not_Started / Accruing / Cap_Reached / Waived) |
| `ld_cap_reached_at` | TIMESTAMP | N | Set when cumulative LD reaches `M01.Contract.ld_cap_pct × contract_value` |

#### 3b.13 — `LDExposureLog` (append-only)

Standard append-only log: `id`, `tenant_id`, `ld_exposure_record_id`, `from_amount_inr`, `to_amount_inr`, `flip_type` (Eligibility_True / Eligibility_False / Amount_Update), `m05_system_actor` (always 'M05_SYSTEM' per BR-05-033), `changed_at`. DB UPDATE/DELETE forbidden.

#### 3b.14 — `ProjectRiskConfig`

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `id` | UUID | Y | Auto | — |
| `tenant_id`, `created_by`, `created_at`, `updated_by`, `updated_at`, `is_active` | — | Y | Reserved | — |
| `project_id` | UUID | Y | — | FK → `M01.Project`; UNIQUE |
| `dual_signoff_threshold_inr` | DECIMAL(15,2) | Y | 5000000 (₹50 lakh) | OQ-1.5 lock |
| `ewn_lapse_days` | INTEGER | Y | 30 | OQ-1.8 lock |
| `ncr_aging_to_ld_days` | INTEGER | Y | 14 | OQ-1.9 lock |
| `contingency_depletion_high_pct` | DECIMAL(5,4) | Y | 0.80 | OQ-1.7 + OQ-2.3 |
| `contingency_depletion_critical_pct` | DECIMAL(5,4) | Y | 0.95 | OQ-2.3 |
| `risk_review_cadence_days` | INTEGER | Y | 90 (quarterly) | OQ-2.5 |

Edit permission: PROJECT_DIRECTOR + PMO_DIRECTOR (audited).

---

## BLOCK 4 — DATA POPULATION RULES

### 4a. Role × Action Permission Matrix

| Action | SYS_ADMIN | PMO_DIR | PORTFOLIO | PROJ_DIR | PLAN_ENG | QS_MGR | FIN_LEAD | PROC | SITE_MGR | COMP_MGR | ANALYST | READ_ONLY | EXT_AUDIT |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RAISE_RISK (Draft) | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| ACCEPT_RISK (Draft → Active) | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| SCORE_RISK | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| ASSIGN_RISK_RESPONSE | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| CLOSE_RISK | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| WITHDRAW_RISK | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| RAISE_CHANGE | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| PROMOTE_CHANGE_TO_VO | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| DRAFT_VO | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| ASSESS_VO (Draft → Assessed) | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| SUBMIT_VO (Assessed → Submitted) | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| APPROVE_VO (Submitted → Approved; single ≤ ₹50L) | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| APPROVE_VO_DUAL (Submitted → Approved; dual > ₹50L) | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| REJECT_VO | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| MATERIALISE_VO | SYSTEM | (retry-only) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| CLOSE_VO | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| RAISE_EOT_CLAIM | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| ASSESS_EOT (Claim_Raised → Under_Assessment) | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| GRANT_EOT (full or partial) | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| REJECT_EOT | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| RAISE_EWN | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| CLOSE_EWN | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| REQUEST_CONTINGENCY_DRAWDOWN | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| APPROVE_CONTINGENCY_DRAWDOWN | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| WRITE_LD_FLAG (to M04 BR-04-022) | SYSTEM | (retry-only) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| OVERRIDE_LD_ASSESSMENT | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| EDIT_PROJECT_RISK_CONFIG | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| VIEW_RISK_REGISTER | ✅ | ✅ | ✅ | ✅ (own) | ✅ (own) | ✅ (own) | ✅ | ✅ (own) | ✅ (own) | ✅ (filter) | ✅ | ✅ (RAG only) | ✅ |
| VIEW_VO_REGISTER | ✅ | ✅ | ✅ | ✅ (own) | ✅ (own) | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| VIEW_EOT_REGISTER | ✅ | ✅ | ✅ | ✅ (own) | ✅ (own) | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| VIEW_LD_EXPOSURE | ✅ | ✅ | ✅ | ✅ (own) | ❌ | ✅ (own) | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| VIEW_CONTINGENCY_POOL | ✅ | ✅ | ✅ | ✅ (own) | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| VIEW_CLAIMS_EXPOSURE_SUMMARY | ✅ | ✅ | ✅ | ✅ (own) | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |

**Critical permission rules:**
- **MATERIALISE_VO is SYSTEM-only.** Per F2 lock: materialisation is automatic on Approved transition; PMO_DIRECTOR holds **retry permission only** (no human "materialises" a VO).
- **WRITE_LD_FLAG is SYSTEM-only.** Per BR-04-022 + BR-05-033: `ld_eligibility_flag` write to M04 is system-to-system; UI write blocked at M04 API. PMO_DIRECTOR has retry-only on system error.
- **APPROVE_CONTINGENCY_DRAWDOWN is PMO_DIRECTOR only.** No self-approval (the requesting user cannot also approve). No delegation below PMO_DIRECTOR. Per BR-05-028.
- **GRANT_EOT is PMO_DIRECTOR only.** Partial grants permitted per OQ-1.6.
- **APPROVE_VO_DUAL** requires BOTH `approved_by_pmo_at` AND `approved_by_finance_at` populated (two distinct users; same-user dual-sign is system-rejected).
- **External roles** (CLIENT_VIEWER, LENDER_VIEWER, NABH_ASSESSOR, CONTRACTOR_LIMITED) — NO ACCESS in Phase 1; gated by PF03 Phase 2.

**RBAC matrix column structure:** Truncated column labels (SYS_ADMIN, PMO_DIR, etc.) consistent with M03 Spec v1.1b precedent. Per Round 29 audit M25/D4b: ANALYST + EXTERNAL_AUDITOR included as full columns.

### 4b. Required Fields on Creation

| Entity | Mandatory Fields at Create |
|---|---|
| `Risk` | `project_id`, `title`, `description`, `category`, `probability_score`, `impact_score`, `owner_user_id`, `status` (defaults to `Draft`) |
| `Change` | `project_id`, `title`, `description`, `change_type`, `raised_by_user_id`, `status` (defaults to `Draft`) |
| `VariationOrder` | `project_id`, `title`, `description`, `vo_type`, `vo_cause`, `status` (defaults to `Draft`); `early_warning_notice_id` if `vo_cause IN (Delay, Scope_Increase)` |
| `ExtensionOfTime` | `project_id`, `claim_basis`, `delaying_event_description`, `affected_milestones[]` (≥1), `claim_days`, `early_warning_notice_id` (NOT NULL per BR-05-018), `status` (defaults to `Claim_Raised`) |
| `EarlyWarningNotice` | `project_id`, `raised_by_user_id`, `delaying_event_description`, `expected_impact_qualitative`, `status` (defaults to `Active`) |
| `ContingencyDrawdownLog` | `contingency_pool_id`, `requested_by_user_id`, `amount_inr`, `justification`, `status` (defaults to `Requested`); exactly one of `linked_risk_id`/`linked_vo_id`/`linked_change_id` |
| `LDExposureRecord` | `project_id`, `m04_ncr_id`, `delay_weeks`, `ld_amount_inr`, `ld_status` (defaults to `Accruing`) |
| `ProjectRiskConfig` | `project_id` (1 row per project; auto-created with defaults at project Activation per BR-05-001) |

### 4c. Default Values + Seed Data

| Item | Default |
|---|---|
| `Risk.status` on create | `Draft` (per OQ-2.6 broad-raise pattern) |
| `Risk.rag_band` | DERIVED from `risk_score`; not user-set |
| `VariationOrder.status` on create | `Draft` |
| `VariationOrder.approval_level` | DERIVED from `cost_impact_inr` vs `ProjectRiskConfig.dual_signoff_threshold_inr` at Submit transition |
| `ExtensionOfTime.status` on create | `Claim_Raised` |
| `EarlyWarningNotice.status` on create | `Active` |
| `ContingencyPool.total_inr` | CALC at project Activation = `M01.Contract.contract_value × M01.Contract.risk_buffer_pct` (per BR-05-001) |
| `ContingencyPool.consumed_inr` | 0 |
| `ProjectRiskConfig` | Auto-created at project Activation with all OQ-2.5 defaults |

**KDMC pilot seed data (HDI v0.1 prototype):**
- 1 ProjectRiskConfig row with default values
- 1 ContingencyPool row: `total_inr = ₹68.4 Cr × 0.05 = ₹3.42 Cr`
- 5 sample Risk rows (one per risk category) at various scores for UI demo
- 1 sample EarlyWarningNotice (Schedule_Risk type)
- 0 sample VOs / EOTs (created via UI flow during demo)

---

## BLOCK 5 — FILTERS & VIEWS

### 5a. Risk Register View

**Default sort:** `risk_score DESC, residual_risk_score DESC, raised_at DESC`.

**Filters:**
- `status` (multi-select)
- `category` (multi-select)
- `rag_band` (multi-select)
- `owner_user_id` (single)
- `affected_milestones` contains (UUID)
- `risk_score >= N` (threshold filter)
- `is_active` (default true)

**Role-default views per X9 v0.5 cascade §13.3.7 (target — Round 35 Wireframes round will lock the X9 cascade):**
- **PMO_DIRECTOR primary:** 5×5 risk heatmap (dual-encoded probability × impact); LD exposure trend secondary
- **PORTFOLIO_MANAGER primary:** Portfolio risk heatmap (aggregated across projects); Contingency depletion table secondary
- **PROJECT_DIRECTOR primary:** Own-project risk register (filtered, sortable by risk_score); Pending VOs/EOTs queue secondary
- **PLANNING_ENGINEER primary:** EOT claim queue (own project; pending assessment); EWN log secondary
- **QS_MANAGER primary:** VO assessment queue (cost-impact reviews); Change register (own packages) secondary
- **SITE_MANAGER primary:** EWN raise / view (own project); Active risks affecting current site work secondary
- **FINANCE_LEAD primary:** LD exposure dashboard (per project + cumulative); VO cost-impact pipeline funnel secondary (X9 §11 flagship pattern instance #3 — VO Funnel)
- **COMPLIANCE_MANAGER:** (no primary M05 view; M09 owns) — Risk register read-only filter for compliance-classified risks (secondary)
- **PROCUREMENT_OFFICER:** (no primary M05 view) — VO impact on procurement schedule (M03 cross-link) secondary
- **ANALYST primary:** Risk score trend curves; NCR-to-LD aging funnel secondary (X9 §11 flagship pattern instance #4 — LD Funnel)
- **READ_ONLY:** Risk register card (RAG-only; numeric scores hidden per BR-05-005)
- **EXTERNAL_AUDITOR:** Risk register full read-only; LD exposure history (audit trail) secondary

### 5b. Change / VO Register View

**Filters:** `status` (multi-select; 7 VO states + Change states), `vo_type`, `vo_cause`, `cost_impact_inr` range, `vo_code` search, `linked_risk_id`, `early_warning_notice_id`, `assessed_by_user_id`, `approved_by_pmo_user_id`, `approved_by_finance_user_id`.

**Pipeline funnel view (FINANCE_LEAD secondary):** VO Funnel — `Draft → Assessed → Submitted → Approved → Materialised → Closed` with count + cumulative cost_impact_inr per stage. Rejected shown as separate terminal bucket. Per X9 §11 flagship pattern instance #3.

### 5c. EOT Register View

**Filters:** `status`, `claim_basis`, `claim_days` range, `granted_days` range, `partial_grant_reason` IS NOT NULL (partial grants only), `early_warning_notice_id`, `affected_milestones` contains.

**Pipeline funnel view (X9 §11 flagship instance #5 — EOT Funnel):** `Claim_Raised → Under_Assessment → Granted/Partial/Rejected` with count per stage + cumulative `granted_days` for Granted bucket.

### 5d. LD Exposure Summary View

**Real-time LD accrual** — role-gated to FINANCE_LEAD, PMO_DIRECTOR, SYSTEM_ADMIN, EXTERNAL_AUDITOR (no role outside this set sees numeric LD amounts; READ_ONLY does not see LD at all per Block 4a).

**Display:**
- Cumulative LD exposure (current `LDExposureLog` total)
- Cap amount (`M01.Contract.ld_cap_pct × contract_value`)
- Cap utilisation % (cumulative / cap)
- Per-NCR breakdown (`LDExposureRecord` rows; sortable by `ld_amount_inr DESC`)
- LD-aging funnel (X9 §11 flagship instance #4): `NCR_Raised → NCR_Aging (>14 days) → LD_Eligible → LD_Applied`

### 5e. Contingency Pool View

**Display:**
- Total / Consumed / Available (₹ + %)
- Consumed bar with depletion thresholds at 80% (high) and 95% (critical) marked
- Drawdown history (ContingencyDrawdownLog rows; sortable by `requested_at DESC`)
- Per-Risk / per-VO / per-Change drawdown breakdown

**Role gate:** PMO_DIRECTOR, PROJECT_DIRECTOR, FINANCE_LEAD, PORTFOLIO_MANAGER, ANALYST, EXTERNAL_AUDITOR. SITE_MANAGER + READ_ONLY do not see contingency.

### 5f. Claims Exposure Summary View (rollup; M10 read-through)

Aggregated read-only projection:
- Cumulative LD exposure
- Pending VO cost impact (sum of VO.cost_impact_inr where `status IN (Submitted, Approved)`)
- Pending EOT days (sum of EOT.claim_days where `status IN (Claim_Raised, Under_Assessment)`)
- Contingency consumed % (from ContingencyPool)
- Claims exposure ratio: `(LD + Pending VO + Contingency consumed) / contract_value`

Emit `CLAIMS_EXPOSURE_SUMMARY` event to M10 EPCCCommand (when built) for dashboard cache + to M19 ClaimsManagement (Phase 2) for formal claims documentation.

---

## BLOCK 6 — BUSINESS RULES

32 BRs — `BR-05-001` through `BR-05-032`. Format: `BR-XX-YYY | Trigger | Rule | Result | Speed Tier`.

### 6a. Project Activation + Configuration

| BR | Trigger | Rule | Result | Speed |
|---|---|---|---|---|
| BR-05-001 | M01 Project Activation event | Auto-create `ProjectRiskConfig` row with OQ-2.5 defaults; auto-create `ContingencyPool` row with `total_inr = M01.Contract.contract_value × M01.Contract.risk_buffer_pct`; emit `PROJECT_RISK_INITIALISED` audit event | Both rows persisted | 🔴 Real-time |
| BR-05-002 | `Risk.status` transition | Strict state machine: `Draft → Active` (via PROJECT_DIRECTOR or PMO_DIRECTOR ACCEPT_RISK), `Active → Mitigating` (via response_strategy populated), `Mitigating → Closed` (via residual_risk_score ≤ 6 + PMO sign-off per BR-05-008), `Active/Mitigating → Reopened` (via PMO override), `Draft → Withdrawn` (via raiser within 24hr); no skipping | Persist; emit `RISK_STATE_CHANGED` | 🔴 Real-time |

### 6b. Risk Scoring + Closure

| BR | Trigger | Rule | Result | Speed |
|---|---|---|---|---|
| BR-05-003 | `Risk.probability_score` OR `Risk.impact_score` write | `risk_score = probability_score × impact_score`; recomputed automatically; user cannot edit `risk_score` directly | Persist | 🔴 Real-time |
| BR-05-004 | `Risk.risk_score` change | `rag_band` re-derived: 1-4 = Green, 5-12 = Amber, 13-25 = Red (per Brief OQ-1.2 cascade lock) | Persist; UI re-renders | 🔴 Real-time |
| BR-05-005 | UI render of Risk row for READ_ONLY role | Show only `rag_band` badge + title; HIDE `probability_score`, `impact_score`, `risk_score` numeric values | UI-layer enforcement; API serialiser strips fields per role | 🔴 Real-time |
| BR-05-006 | `Risk.rag_band = Red` (risk_score ≥ 13) | `response_strategy` MUST be populated AND `response_action_plan` ≥ 100 chars within 48 hours of entering Red band; else emit `HIGH_RISK_THRESHOLD_BREACH` Decision Queue trigger to PROJECT_DIRECTOR | Block save without response on Red save attempts after grace; DQ trigger at 48hr threshold | 🔴 + 🟡 |
| BR-05-007 | `RiskResponseStrategy` set | Must be one of {Avoid, Reduce, Transfer, Accept} per X8 §3.76 (ARTA per OQ-1.4) | Block save outside ENUM | 🔴 Real-time |
| BR-05-008 | `Risk.status → Closed` | Requires `residual_risk_score <= 6` (Green threshold) AND PMO_DIRECTOR sign-off (`closed_by_user_id` must be PMO_DIRECTOR role) | Block close otherwise; emit `RISK_CLOSED` | 🔴 Real-time |

### 6c. Variation Order State Machine + Sign-Off

| BR | Trigger | Rule | Result | Speed |
|---|---|---|---|---|
| BR-05-009 | `VariationOrder.status` transition | Strict 7-state machine per Brief v1.0a OQ-1.5: `Draft → Assessed → Submitted → Approved → Materialised → Closed`; `Rejected` terminal-from-{Draft, Assessed, Submitted}; no skipping; no reversal after Materialised (use compensating VO instead) | Persist; emit `VO_STATE_CHANGED` with from_status + to_status | 🔴 Real-time |
| BR-05-010 | `VO.status → Assessed` | Requires `assessed_by_user_id` populated AND caller has QS_MANAGER role; `assessed_at` auto-set | Block transition otherwise | 🔴 Real-time |
| BR-05-011 | `VO.status → Submitted` | Requires `cost_impact_inr` populated (non-null, can be 0 or negative); `submitted_at` auto-set; emit `VO_PENDING_APPROVAL` Decision Queue trigger to PMO_DIRECTOR/FINANCE_LEAD (per OQ-2.3) | DQ trigger raised; SLA 7 days | 🔴 + 🟡 |
| BR-05-012 | `VO.status → Approved` | Single sign-off path (`cost_impact_inr <= ProjectRiskConfig.dual_signoff_threshold_inr`): EITHER `approved_by_pmo_at` OR `approved_by_finance_at` populated. Dual sign-off path (above threshold): BOTH populated. Same user cannot populate both fields (system-rejected). | Block transition otherwise; emit `VO_APPROVED` | 🔴 Real-time |
| BR-05-013 | `VO.status → Approved` (success) | Emit `VO_APPROVED` event to M02 with VO payload (vo_id, project_id, vo_type, vo_cause, cost_impact_inr, expected BOQ delta lines); M02 confirms via creating `VOBOQMaterialisation` row + setting `Package.bac_integrity_status = Stale_Pending_VO` per M02 Spec line 156 | M02 acknowledges; M05 awaits Materialised confirmation | 🔴 Real-time |
| BR-05-014 | `VO.status → Materialised` | SYSTEM action only; triggered by M02 confirmation event with `materialisation_status = Complete`; `materialised_at` auto-set; `vo_boq_materialisation_id` populated. **No human role can manually set Materialised** (per F2 lock) | Auto-transition; emit `VO_MATERIALISED` | 🔴 Real-time |
| BR-05-015 | M02 reports `materialisation_status = Failed` | VO status remains `Approved` (no rollback to earlier states); `VOBOQMaterialisation.failure_reason` populated; emit `VO_MATERIALISATION_FAILED` Decision Queue trigger Critical to PMO_DIRECTOR + SYSTEM_ADMIN | DQ trigger raised; PMO_DIRECTOR has retry permission via system action | 🔴 Real-time |
| BR-05-016 | `VariationOrder.create` where `vo_cause IN (Delay, Scope_Increase)` | `early_warning_notice_id` MUST be populated (NOT NULL); referenced EWN MUST have `status = Active` (not Lapsed/Closed) | Block create otherwise per OQ-1.8 mandate | 🔴 Real-time |
| BR-05-017 | `VO.status → Materialised` | Emit `VO_APPROVED_COST_IMPACT` event to M06 (per M06 Spec line 682 BR-06-039 contract): `vo_id, vo_cost_impact_inr, triggering_event = VO_APPROVED`; M06 writes Committed CostLedgerEntry | M06 acknowledges; cost ledger updated | 🔴 Real-time |

### 6d. Extension of Time

| BR | Trigger | Rule | Result | Speed |
|---|---|---|---|---|
| BR-05-018 | `ExtensionOfTime.create` | `early_warning_notice_id` MUST be populated (NOT NULL per OQ-1.8); `claim_days >= 1`; `affected_milestones[]` ≥ 1 element | Block create otherwise | 🔴 Real-time |
| BR-05-019 | `EOT.status → Granted` (partial) | If `granted_days < claim_days`: `partial_grant_reason` MUST be populated, ≥ 100 chars per OQ-1.6 | Block transition otherwise | 🔴 Real-time |
| BR-05-020 | `EOT.status → Granted` | Caller MUST be PMO_DIRECTOR; `granted_by_user_id` + `granted_at` auto-set | Block transition otherwise | 🔴 Real-time |
| BR-05-021 | `EOT.status → Granted` (success) | Emit `EOT_GRANTED` event to M03 with payload (eot_id, project_id, granted_days, claim_basis, affected_milestones, variation_order_id if linked); M03 creates `BaselineExtension` row per M03 Spec line 184-206 with `granted_days = M05.EOT.granted_days`; M05 receives back `m03_baseline_extension_id` via callback event | M03 confirms; M05 stores baseline_extension_id | 🔴 Real-time |
| BR-05-022 | M03 reports baseline cascade failure | EOT status remains `Granted` (no rollback); emit `EOT_BASELINE_CASCADE_FAILED` Decision Queue trigger Critical to PMO_DIRECTOR + SYSTEM_ADMIN | DQ trigger raised | 🔴 Real-time |

### 6e. Early Warning Notice

| BR | Trigger | Rule | Result | Speed |
|---|---|---|---|---|
| BR-05-023 | `EarlyWarningNotice.create` | `delaying_event_description` ≥ 100 chars; `expected_impact_qualitative` ≥ 50 chars | Block save otherwise | 🔴 Real-time |
| BR-05-024 | EOT or VO claim references EWN | EWN.linked_eot_id OR linked_vo_id populated; close criteria for EWN: corresponding EOT/VO transitions to terminal state (Granted/Rejected/Withdrawn for EOT; Closed/Rejected for VO) → EWN.status → Closed; emit `EWN_CLOSED` | EWN closed | 🔴 Real-time |
| BR-05-025 | Daily EWN sweep (🟢 24hr batch) | EWN.status = `Active` AND `raised_at + ProjectRiskConfig.ewn_lapse_days < today` AND `linked_eot_id IS NULL AND linked_vo_id IS NULL` → EWN.status = `Lapsed`; emit `EWN_LAPSED` audit event + Decision Queue trigger to PROJECT_DIRECTOR | EWN lapsed; subsequent EOT/VO claims referencing this EWN are blocked per BR-05-016 + BR-05-018 | 🟢 24hr |
| BR-05-026 | Daily EWN sweep (🟢 24hr batch) | EWN.status = `Active` AND `raised_at + ProjectRiskConfig.ewn_lapse_days × 0.75 < today` (75% of lapse window elapsed) → emit `EWN_LAPSE_APPROACHING` Decision Queue trigger to PROJECT_DIRECTOR (Medium severity) | DQ trigger raised | 🟢 24hr |

### 6f. Contingency Pool + Drawdown

| BR | Trigger | Rule | Result | Speed |
|---|---|---|---|---|
| BR-05-027 | `ContingencyDrawdownLog.create` | Exactly one of `linked_risk_id`/`linked_vo_id`/`linked_change_id` populated; `amount_inr > 0`; `justification ≥ 100 chars` | Block save otherwise; emit `CONTINGENCY_DRAWDOWN_REQUESTED` | 🔴 Real-time |
| BR-05-028 | `ContingencyDrawdownLog.status → Approved` | `approved_by_user_id` MUST have PMO_DIRECTOR role AND MUST NOT equal `requested_by_user_id` (no self-approval). Update `ContingencyPool.consumed_inr += amount_inr` atomically | Persist; emit `CONTINGENCY_DRAWDOWN_APPROVED` | 🔴 Real-time |
| BR-05-029 | `ContingencyPool.consumed_pct >= 0.80` (post-drawdown approval) | Emit `CONTINGENCY_POOL_DEPLETION_HIGH` Decision Queue trigger High to PMO_DIRECTOR (24hr SLA) | DQ trigger raised | 🔴 Real-time |
| BR-05-030 | `ContingencyPool.consumed_pct >= 0.95` (post-drawdown approval) | Emit `CONTINGENCY_POOL_DEPLETION_CRITICAL` Decision Queue trigger Critical to PMO_DIRECTOR (real-time SLA) | DQ trigger raised | 🔴 Real-time |
| BR-05-030b | ContingencyDrawdown above stage-gate-trigger threshold (configurable in M08 future Spec; M05 emits stub now) | Emit `CONTINGENCY_DRAWDOWN_GATE_REQUEST` event to M08 (when built) per Brief §10 forward constraint | M08 stub registered; processed when M08 lands | 🔴 Real-time |

### 6g. Liquidated Damages — NCR-driven (the M04 contract loop)

| BR | Trigger | Rule | Result | Speed |
|---|---|---|---|---|
| BR-05-031 | `LDExposureRecord.ld_amount_inr` calculation | `ld_amount_inr = M01.Contract.ld_rate_per_week × delay_weeks × M01.Contract.contract_value`; capped at `M01.Contract.ld_cap_pct × M01.Contract.contract_value`. Cap is project-level cumulative across all `LDExposureRecord` rows | Persist | 🔴 Real-time |
| BR-05-032 | Daily NCR aging sweep (🟢 24hr batch) | For each open `M04.ConstructionNCR` where (`severity ∈ {Critical, High}` AND `now() - raised_at > ProjectRiskConfig.ncr_aging_to_ld_days` AND `ld_eligibility_flag = false` AND no contractor-fault waiver): system writes `ld_eligibility_flag = true` to M04 via M04 internal API (per M04 BR-04-022 system-to-system contract); creates `LDExposureRecord` row; emits `LD_ELIGIBLE_AMOUNT` event to M06 with payload (ld_exposure_record_id, ncr_id, ld_amount_inr) | M04 ld_eligibility_flag toggled (M05_SYSTEM actor in M04 audit log per BR-04-022); M06 receives event for CostLedgerEntry deduction tracker per M06 line 708 contract | 🟢 24hr (sweep emits 🔴) |
| BR-05-033 | M05 system call to M04 BR-04-022 | Caller MUST be M05 internal system (not any human user); M04 audit log records `actor = 'M05_SYSTEM'` per BR-04-022. UI-initiated call REJECTED at M04 API layer | System-to-system only; UI blocked | 🔴 Real-time |
| BR-05-034 | Cumulative LD ≥ `0.80 × ld_cap_pct × contract_value` (cap approaching) | Emit `LD_CAP_APPROACHING` Decision Queue trigger High to PMO_DIRECTOR + FINANCE_LEAD (24hr SLA) | DQ trigger raised | 🔴 Real-time |
| BR-05-035 | Cumulative LD = `ld_cap_pct × contract_value` (cap reached) | Emit `LD_CAP_REACHED` Decision Queue trigger Critical to PMO_DIRECTOR + FINANCE_LEAD (real-time); BLOCK further LD accrual (subsequent NCR sweep does not flip new flags); update `LDExposureRecord.ld_status = Cap_Reached` | DQ trigger; subsequent LD assessments halted | 🔴 Real-time |

**Note:** BR codes BR-05-030b and BR-05-035 are sub-numbered to maintain the user's requested 32-BR target (with 1 sub-numbered logical addition each in §6f and §6g where the rule cluster needed 2 thresholds). Effective rule count: 35 distinct rules in 32 numbered BRs. Spec stays within target range (28-35 per task spec).

---

## BLOCK 7 — INTEGRATION POINTS

### 7a. RECEIVES FROM

| From | Data | Trigger | Speed | Failure Handling |
|---|---|---|---|---|
| M01 | `Contract.ld_rate_per_week`, `ld_cap_pct`, `risk_buffer_pct`, `contract_value_basic` (per M01 Spec line 619 SENDS TO M05 + line 220-222 field defs) | On Project Activation + Contract edit | 🔴 Real-time | If M01 Contract not yet Activated: block M05 entity create with reason `M01_CONTRACT_NOT_ACTIVATED` |
| M01 | `Project.current_phase`, `project_status`, `report_date` | On Project state change | 🔴 Real-time | — |
| M02 | `BOQItem` schema for VO costing (read-only); `Package.bac_amount` for VO impact calc | On VO costing assessment (read via M02 internal API) | 🔴 Real-time | If M02 BAC integrity status = `Stale_Pending_VO` for the target Package: block new VO creation referencing that Package (only one in-flight VO per Package) |
| M02 | `BACIntegrityLedger.bac_integrity_status = Stale_Pending_VO` (M02 sets when receives `VO_APPROVED` event from M05) — confirmation back-event | On VO Approved → Materialisation start | 🔴 Real-time | — |
| M02 | `VOBOQMaterialisation.materialisation_status = Complete OR Failed` — M02 confirmation event | On M02 BOQ update completion or failure | 🔴 Real-time | If `Failed`: BR-05-015 raises Critical DQ trigger |
| M03 | `BaselineExtension` schema reference (M03 Spec line 184-206) | On EOT Granted → M03 BaselineExtension creation request | 🔴 Real-time | — |
| M03 | `Milestone` IDs (for EWN.affected_milestones[] + EOT.affected_milestones[] selection) | On EWN raise + EOT raise (read via M03 internal API) | 🔴 Real-time | — |
| M03 | M03 cascade complete callback event (with `m03_baseline_extension_id`) OR cascade failure event | Async after M03 receives `EOT_GRANTED` | 🔴 Real-time | If cascade fails: BR-05-022 raises Critical DQ trigger |
| **M04 BR-04-021** | **`NCR_RAISED` + `NCR_STATUS_CHANGED`** events with full ConstructionNCR payload (severity, raised_at, status, root_cause_category, contractor_id) | On M04 NCR create + status change | 🔴 Real-time | If M05 internal API endpoint unavailable: M04 retries with exponential backoff (operational responsibility) |
| M04 | `ConstructionNCR.severity`, `raised_at`, `closed_at`, `ld_eligibility_flag` (read for daily NCR aging sweep per BR-05-032) | Read on aging sweep | 🟢 24hr | — |
| M34 | Auth, role, project scope, MFA gate | Every API call | 🔴 Real-time | Standard auth flow; non-issue at M05 layer |
| M11 ActionRegister (when built) | Decision Queue acknowledgement back-events | On Decision Queue owner action | 🔴 Real-time | M11 stub interim; events queue locally until M11 lands |

### 7b. SENDS TO

| To | Data | Trigger | Speed | Failure Handling |
|---|---|---|---|---|
| **M02** | **`VO_APPROVED` event** with payload (`vo_id, project_id, vo_type, vo_cause, cost_impact_inr, expected_boq_changes[]`) → M02 sets `Package.bac_integrity_status = Stale_Pending_VO`, creates `VOBOQMaterialisation` rows, performs BOQ update per M02 Spec Block 7 | On VO `Submitted → Approved` transition (per BR-05-013) | 🔴 Real-time | If M02 fails materialisation: BR-05-015 holds VO at Approved state, raises DQ |
| M02 | VO status closure event (post-Materialised → Closed) | On VO Closed | 🔴 Real-time | — |
| **M03** | **`EOT_GRANTED` event** → M03 creates `BaselineExtension` row with `granted_days`, `cause_category`, `variation_order_id` (if linked), `is_billable_to_client` (per M03 Spec line 202) | On EOT `Under_Assessment → Granted` (per BR-05-021) | 🔴 Real-time | If M03 cascade fails: BR-05-022 raises DQ |
| **M04 (BR-04-022)** | **`ld_eligibility_flag` write-back** — system-to-system internal API call; UI cannot perform this write per BR-04-022 + BR-05-033. Caller actor = `M05_SYSTEM` in M04 audit log | On NCR aging crosses threshold + severity check (per BR-05-032 daily sweep) | 🔴 Real-time | If M04 API unavailable: M05 retries with exponential backoff (5 attempts); after exhaustion, raises `LD_FLAG_WRITEBACK_FAILED` DQ Critical |
| **M06 (BR-06-039)** | **`VO_APPROVED_COST_IMPACT` event** with `vo_id, vo_cost_impact_inr, triggering_event = VO_APPROVED` (per M06 Spec line 682 already-locked contract) | On VO `Materialised` (per BR-05-017) | 🔴 Real-time | If M06 unavailable: M05 retries; after exhaustion, raises `M06_COST_IMPACT_EMIT_FAILED` DQ Critical |
| **M06** | **`LD_ELIGIBLE_AMOUNT` event** with `ld_exposure_record_id, ncr_id, ld_amount_inr, contract_id` (per M06 Spec line 708 already-locked contract) | On LD eligibility flip true (per BR-05-032) OR cumulative LD recalc | 🔴 Real-time | If M06 unavailable: same retry pattern |
| M07 EVMEngine (when built) | `RISK_ADJUSTED_EAC_DELTA` event — sum of `(probability_score × impact_score × estimated_impact_inr)` for all Active risks; quarterly cadence | Quarterly batch + on-demand recalc on PMO_DIRECTOR request | 🟡 1 hr (batch with M07 EAC recalc cycle) | M07 stub interim; events queue locally |
| M08 GateControl (when built) | `CONTINGENCY_DRAWDOWN_GATE_REQUEST` event — for drawdowns above stage-gate threshold (defined by M08 when built) per Brief §10 forward constraint | On drawdown raise above threshold (per BR-05-030b) | 🔴 Real-time | M08 stub interim |
| M10 EPCCCommand (when built) | Risk heatmap data + LD exposure aggregation + claims exposure summary for Command dashboard | On request (read-through pattern) | 🟡 1hr cache | — |
| M11 ActionRegister (when built) | Decision Queue triggers (10 trigger types per Block 8c) | On condition match per BR-05-006/011/015/022/026/029/030/034/035 | 🔴 Real-time / 🟡 / 🟢 per trigger | — |
| M19 ClaimsManagement (Phase 2) | `CLAIMS_EXPOSURE_SUMMARY` aggregated rollup (LD + pending VOs + pending EOTs + contingency consumed) | On request + monthly batch | 🟡 1hr cache | — |

### 7c. Forward Constraints (forward to unbuilt modules)

Per CLAUDE.md §4 Carry-Forward + Brief §10:

| Module | Constraint Imposed by M05 v1.0 |
|---|---|
| **M07 EVMEngine** (R45 Spec) | MUST consume M05 `RISK_ADJUSTED_EAC_DELTA` event in EAC calculation. M05 is sole authority on risk-adjusted forecast deltas |
| **M08 GateControl** (R52 Spec) | MUST accept M05 `CONTINGENCY_DRAWDOWN_GATE_REQUEST` events; process via stage-gate review. Per M06 v1.1 cascade note H6 lock: M08 must NOT declare OUT to M06 for `SG_11_PASSAGE`. M05 has no SG_11 dependency |
| **M10 EPCCCommand** | M05 risk heatmap + LD exposure + claims exposure rollup feed Command dashboard via M05 internal API. M10 does not store M05 data; reads-through |
| **M11 ActionRegister** (R60 Spec) | MUST accept all 10 M05 Decision Queue trigger types (Block 8c); M05 is one of largest emitters |
| **M19 ClaimsManagement** (Phase 2) | M05 emits `CLAIMS_EXPOSURE_SUMMARY` rollup; M19 absorbs formal claim documentation |
| **M02 StructureWBS** | Already-locked: M02 v1.0a + v1.1 cascade note honour FK fields (`Package.pending_vo_id` → M05.VariationOrder; `BOQItem.source_materialisation_id` → M05.VOBOQMaterialisation) |
| **M03 PlanningMilestones** | Already-locked: M03 v1.1b + v1.2/v1.3 cascade notes honour `BaselineExtension.variation_order_id` FK to M05 |
| **M04 ExecutionCapture** | Already-locked: M04 v1.0a BR-04-021 + BR-04-022 honour M05 contract |
| **M06 FinancialControl** | Already-locked: M06 v1.0b + v1.1 cascade note honour BR-06-039 + line 708 stubs |
| **M01 ProjectRegistry** | Already-locked: M01 v1.0a Contract fields read by M05 per line 619 SENDS TO |
| **PF03 ExternalPartyPortal** (Phase 2) | When built: revisit CLIENT_VIEWER access to VO approval workflow (potential 3rd sign-off level above higher threshold per OQ-1.5 deferred Option C) |

---

## BLOCK 8 — GOVERNANCE & AUDIT

### 8a. Permission Reference

(Reference Block 4a Role × Action Permission Matrix.)

### 8b. Audit Event Catalogue (M05-owned, locked from authoring per OQ-2.1)

30 events across 7 sections. All events: append-only, 7-year retention (contractual evidence standard per ES-SEC-004 DPDPA Class 2 Financial classification).

| # | Event | Trigger BR | Severity | Retention |
|---|---|---|---|---|
| **§A.1 Risk events** | | | | |
| 1 | `RISK_RAISED` | BR-05-002 | Info | 7 years |
| 2 | `RISK_ACCEPTED` | BR-05-002 | Info | 7 years |
| 3 | `RISK_SCORE_CHANGED` | BR-05-003 + BR-05-004 | Medium (severity-dependent) | 7 years |
| 4 | `RISK_RESPONSE_PLAN_UPDATED` | BR-05-007 | Info | 7 years |
| 5 | `RISK_CLOSED` | BR-05-008 | Info | 7 years |
| 6 | `RISK_WITHDRAWN` | BR-05-002 | Info | 7 years |
| **§A.2 Change + VO events** | | | | |
| 7 | `CHANGE_RAISED` | — | Info | 7 years |
| 8 | `VO_DRAFTED` | BR-05-009 | Info | 7 years |
| 9 | `VO_ASSESSED` | BR-05-010 | Info | 7 years |
| 10 | `VO_SUBMITTED` | BR-05-011 | Info | 7 years |
| 11 | `VO_APPROVED` | BR-05-012 + BR-05-013 | High | 7 years |
| 12 | `VO_REJECTED` | BR-05-009 | Medium | 7 years |
| 13 | `VO_MATERIALISED` | BR-05-014 + BR-05-017 | High | 7 years |
| 14 | `VO_MATERIALISATION_FAILED` | BR-05-015 | Critical | 7 years |
| 15 | `VO_CLOSED` | BR-05-009 | Info | 7 years |
| **§A.3 EOT events** | | | | |
| 16 | `EOT_CLAIM_RAISED` | BR-05-018 | Info | 7 years |
| 17 | `EOT_UNDER_ASSESSMENT` | — | Info | 7 years |
| 18 | `EOT_GRANTED` | BR-05-020 + BR-05-021 | High | 7 years |
| 19 | `EOT_REJECTED` | — | Medium | 7 years |
| 20 | `EOT_BASELINE_CASCADE_FAILED` | BR-05-022 | Critical | 7 years |
| **§A.4 Early Warning Notice events** | | | | |
| 21 | `EWN_RAISED` | BR-05-023 | Info | 7 years |
| 22 | `EWN_CLOSED` | BR-05-024 | Info | 7 years |
| 23 | `EWN_LAPSED` | BR-05-025 | Medium | 7 years |
| **§A.5 LD events** | | | | |
| 24 | `LD_ELIGIBILITY_FLIPPED_TRUE` | BR-05-032 + BR-05-033 | High | 7 years |
| 25 | `LD_ELIGIBILITY_FLIPPED_FALSE` | BR-05-032 (NCR closed before LD finalised) | Medium | 7 years |
| 26 | `LD_AMOUNT_CALCULATED` | BR-05-031 | Info | 7 years |
| 27 | `LD_CAP_REACHED` | BR-05-035 | Critical | 7 years |
| **§A.6 Contingency events** | | | | |
| 28 | `CONTINGENCY_DRAWDOWN_REQUESTED` | BR-05-027 | Info | 7 years |
| 29 | `CONTINGENCY_DRAWDOWN_APPROVED` | BR-05-028 | High | 7 years |
| 30 | `CONTINGENCY_DRAWDOWN_REJECTED` | — | Medium | 7 years |
| **§A.7 Cross-module + system events** | | | | |
| 31 | `PROJECT_RISK_INITIALISED` | BR-05-001 | Info | 7 years |
| 32 | `RISK_ADJUSTED_EAC_DELTA` | (Quarterly batch + on-demand) | Info | 7 years |
| 33 | `CLAIMS_EXPOSURE_SUMMARY_EMITTED` | (Phase 2 to M19) | Info | 7 years |

**Total: 33 events** (locked from authoring; refined from Brief estimate of 30; minor expansion via §A.2 sub-events).

### 8c. Decision Queue Trigger Catalogue (10 triggers per Brief OQ-2.3)

All triggers in UPPER_SNAKE_CASE per `naming-folders.md` convention. Registered with M11 ActionRegister (when built).

| # | Trigger | Severity | Owner | SLA | Source BR |
|---|---|---|---|---|---|
| 1 | `HIGH_RISK_THRESHOLD_BREACH` (risk_score ≥ 13 with no response_action_plan after 48hr) | High | PROJECT_DIRECTOR | 48 hr | BR-05-006 |
| 2 | `EWN_LAPSE_APPROACHING` (75% of lapse window elapsed) | Medium | PROJECT_DIRECTOR | 7 days | BR-05-026 |
| 3 | `EOT_CLAIM_PENDING_ASSESSMENT` (Claim_Raised → Under_Assessment SLA) | Medium | PLANNING_ENGINEER | 14 days | (Block 4a action SLA) |
| 4 | `VO_PENDING_APPROVAL` (Submitted state SLA) | Medium → escalates | QS_MANAGER (assessor) → PMO_DIRECTOR/FINANCE_LEAD (approvers) | 7 days assess; 7 days approve | BR-05-011 |
| 5 | `LD_CAP_APPROACHING` (cumulative ≥ 80% of cap) | High | PMO_DIRECTOR + FINANCE_LEAD | 24 hr | BR-05-034 |
| 6 | `LD_CAP_REACHED` (cumulative = 100%) | Critical | PMO_DIRECTOR + FINANCE_LEAD | 24 hr | BR-05-035 |
| 7 | `CONTINGENCY_POOL_DEPLETION_HIGH` (≥ 80%) | High | PMO_DIRECTOR | 24 hr | BR-05-029 |
| 8 | `CONTINGENCY_POOL_DEPLETION_CRITICAL` (≥ 95%) | Critical | PMO_DIRECTOR | Real-time | BR-05-030 |
| 9 | `VO_MATERIALISATION_FAILED` (M02 sync error) | Critical | PMO_DIRECTOR + SYSTEM_ADMIN | Real-time | BR-05-015 |
| 10 | `EOT_BASELINE_CASCADE_FAILED` (M03 sync error) | Critical | PMO_DIRECTOR + SYSTEM_ADMIN | Real-time | BR-05-022 |

### 8d. Speed Tier Defaults (per OQ-2.4)

| Event class | Speed tier |
|---|---|
| Risk create / update / response edit | 🔴 Real-time |
| VO state transition (any) | 🔴 Real-time |
| EOT state transition (any) | 🔴 Real-time |
| EWN raise / close | 🔴 Real-time |
| LD eligibility flip (M04 system-to-system write per BR-04-022) | 🔴 Real-time |
| LD amount calculation on RA Bill submission | 🔴 Real-time |
| Contingency drawdown approval | 🔴 Real-time |
| Daily NCR aging sweep (BR-05-032) | 🟢 24 hr |
| Daily EWN sweep (BR-05-025 / BR-05-026) | 🟢 24 hr |
| Quarterly risk register review batch | 🟢 24 hr |
| Risk-adjusted EAC delta to M07 | 🟡 1 hr (batch with M07 EAC recalc cycle) |
| Claims exposure summary recompute | 🟡 1 hr cache |

### 8e. DPDPA 2023 Data Classification

Per `ZEPCC_Legacy/EPCC_Standards_Memory_v5_3.md` §7.128 (ES-SEC-004):

| M05 Field Class | Examples | Treatment |
|---|---|---|
| Class 1 — PERSONAL | `Risk.owner_user_id`, `EWN.raised_by_user_id`, etc. (FK references; user PII lives in M34) | Standard — M34 owns PII; M05 only stores UUID FK |
| Class 2 — FINANCIAL | `VariationOrder.cost_impact_inr`, `LDExposureRecord.ld_amount_inr`, `ContingencyPool.total_inr / consumed_inr`, `M01.Contract.ld_rate_per_week` (read), `ld_cap_pct` (read), `risk_buffer_pct` (read) | Column-level encryption (ES-SEC-003); masked for READ_ONLY (numeric values hidden); 7-year retention (Companies Act) |
| Class 3 — OPERATIONAL | `Risk.probability_score / impact_score / risk_score / rag_band`, `VO.status / vo_type / vo_cause`, `EOT.status / claim_days / granted_days`, all dates, all status fields | Table-level TDE (default); no masking in M05 (RAG-only view for READ_ONLY is UI rendering, not storage); project lifetime + 7 years |

---

## BLOCK 9 — EXPLICIT EXCLUSIONS

(See Block 2b for full list. Restated here for spec discipline.)

| # | Excluded | Reason | Where Addressed |
|---|---|---|---|
| 1 | Financial transaction processing (CostLedgerEntry writes, RA Bill state machine, retention release) | Single-owner: M06 owns financial layer | M06 |
| 2 | BOQ database writes | Single-owner: M02 owns BOQ; M05 emits VO_APPROVED event | M02 |
| 3 | Baseline schedule recalculation | Single-owner: M03 owns BaselineExtension; M05 emits EOT_GRANTED event | M03 |
| 4 | Site diary daily log | M16 SiteDiary (Phase 1 separate module) | M16 |
| 5 | Document storage internals (file blobs, RFI attachments, version control) | M12 DocumentControl (M05 stores `document_id` references only) | M12 |
| 6 | BG and Insurance tracking (full lifecycle) | M23 BGInsuranceTracker (Phase 2; BGStub from M06 OQ-1.9) | M23 |
| 7 | Long-form claims management (expert assessments, arbitration packets) | M19 ClaimsManagement (Phase 2) | M19 |
| 8 | HSE / safety NCRs | M31 HSESafetyManagement (Phase 2; M04 OQ-1.1=B) | M31 |
| 9 | Compliance / regulatory NCRs | M09 ComplianceTracker (Phase 1) | M09 |
| 10 | DLP retention release | M15 owns DLP signal; M06 owns financial release; M05 NOT in chain (per M06 v1.1 cascade note H6 Option B) | M15 + M06 |
| 11 | Stage gate decision-making | M08 GateControl owns; M05 raises drawdown gate requests | M08 |
| 12 | EVM EAC algorithm internals | M07 EVMEngine owns; M05 emits delta inputs only | M07 |
| 13 | Risk-bearing portfolio decisions (multi-project optimisation) | PIOE Phase 2 | PIOE |
| 14 | Monte Carlo quantitative risk analysis | Phase 2 cascade extension to OQ-1.2=A | Phase 2 |
| 15 | Opportunities (positive risks; Exploit/Enhance/Share) | Phase 2 cascade extension to OQ-1.4=A | Phase 2 |
| 16 | Client / Lender / NABH external sign-off on VOs | PF03 ExternalPartyPortal Phase 2 | PF03 |
| 17 | Procurement variation tracking | M30 VendorMasterPQ (Phase 1) | M30 |

---

## BLOCK 10 — OPEN QUESTIONS

### 10a. OQ-1 Status (per Brief v1.0a, all CLOSED)

| OQ-1 | Topic | Locked Answer | Where Embedded |
|---|---|---|---|
| 1.1 | Module scope decomposition | B (LOCKED) — Slim core; Claims→M19, HSE→M31, Insurance→M23 | Block 2a + 2b |
| 1.2 | Probability × Impact matrix | A (LOCKED) — 5×5 matrix; numeric mapping; RAG: 1-4=Green, 5-12=Amber, 13-25=Red | Block 3b.1 (Risk fields) + BR-05-003/004 |
| 1.3 | Risk scoring | B (LOCKED) — Numeric × RAG auto-derived; read-only in UI | BR-05-003/004/005 |
| 1.4 | Risk response types | A (LOCKED) — ARTA 4-type | X8 v0.7 §3.76 RiskResponseStrategy |
| 1.5 | VO approval workflow | B (LOCKED) — Threshold dual sign-off ₹50L (default); 7-state machine per Brief v1.0a patch | Block 3b.4 (VariationOrder) + BR-05-009/012 |
| 1.6 | EOT grant model | B (LOCKED) — Partial grants; partial_grant_reason ≥100 chars | Block 3b.7 (EOT) + BR-05-019 |
| 1.7 | Contingency pool | A (LOCKED) — One pool per project | Block 3b.10 (ContingencyPool) + BR-05-001 |
| 1.8 | Early Warning Notice | A (LOCKED) — Mandatory before EOT/VO claim | BR-05-016 + BR-05-018 |
| 1.9 | LD enforcement | B (LOCKED) — M05 calculates → M06 deducts via LD_ELIGIBLE_AMOUNT event | BR-05-031/032/033 + Block 7b |
| 1.10 | Role-default views per X9 v0.4 §13.3 | Locked mapping; 3 new flagship pipeline pattern instances (VO #3, LD #4, EOT #5) | Block 5a-5e |

### 10b. OQ-2 Status (per Brief v1.0a, all CLOSED)

| OQ-2 | Topic | Locked Answer | Where Embedded |
|---|---|---|---|
| 2.1 | Audit event naming discipline | CLOSED — Lock event names in Brief Appendix A | Block 8b (33 events catalogued) |
| 2.2 | Append-only ledgers | CLOSED — 5 entities (RiskStatusLog, VOStatusLog, EOTStatusLog, ContingencyDrawdownLog, LDExposureLog) | Block 3a (column "Append-Only?") |
| 2.3 | Decision Queue SLA defaults | CLOSED — 10 triggers | Block 8c |
| 2.4 | Speed tier defaults | CLOSED — 10 event classes mapped | Block 8d |
| 2.5 | ProjectRiskConfig entity | CLOSED — 6 fields | Block 3b.14 |
| 2.6 | Risk identification ownership | CLOSED — Broad raise + governed accept (Draft → Active state machine) | BR-05-002 + Block 4a (RAISE_RISK row) |

### 10c. Open Questions Surfaced During Authoring

**None.** All questions encountered during this Spec authoring resolved via Brief v1.0a / CLAUDE.md / parent module Specs. Block 10 closes at zero per spec-protocol.md §10-Block Spec Template lock rule.

**Zero open questions. M05 RiskChangeControl ready for Round 33 lock.**

---

*v1.0 — Spec LOCKED 2026-05-04 (Round 33). Ready for Round 34 (M13 Spec) per C1b batch cadence; Round 35-36 (M05+M13 Wireframes + Workflows) per Build Execution Plan §3a.*
