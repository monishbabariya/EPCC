# X8 — Glossary & ENUMs
## Cross-Cutting Document v0.7 (LIVING)
**Owner:** PMO Director / System Architect
**Created:** 2026-05-03 (v0.1) | **Updated:** 2026-05-04 (v0.7)
**Status:** Living — appended on every module spec lock
**Source modules locked into this version:** M34, M01, M02, M03, M04, M06, **M05** (NEW v0.7)
**Folder:** SystemAdmin/Cross-link files/ (per Round 18 audit canonical placement)
**Version bump rationale:** Minor version bump (v0.6 → v0.7) — adds 16 new ENUMs from M05 lock + 16 new audit event types (§4.12 extension) + 10 new Decision Queue trigger types (§4.17 extension). Substantive cascade per spec-protocol.md §Cascade-vs-Re-issue rule (>1 ENUM addition; cross-cutting scope expansion). New filename per minor-version-bump convention; v0.6 + v0.6a content preserved historically (this v0.7 supersedes for current usage).

---

## IN-PLACE PATCH CHANGE LOG

(no in-place patches yet on v0.7; reserved for future letter-suffix patches)

---

## CHANGES IN v0.7

| # | Change | Driven By |
|---|---|---|
| 1 | Added `RiskCategory` ENUM (§3.73) — 8 values (Strategic / Financial / Operational / Regulatory / Clinical / Market / ESG / Force_Majeure) | M05 Spec Block 3b.1 (Risk.category) |
| 2 | Added `RiskRAGStatus` ENUM (§3.74) — 3 values (Green / Amber / Red) — derived from risk_score per Brief OQ-1.2 lock | M05 Spec Block 3b.1 (Risk.rag_band) |
| 3 | Added `RiskStatus` ENUM (§3.75) — 6 values (Draft / Active / Mitigating / Closed / Reopened / Withdrawn) | M05 Spec Block 3b.1 (Risk.status) |
| 4 | Added `RiskResponseStrategy` ENUM (§3.76) — 4 values (Avoid / Reduce / Transfer / Accept) per OQ-1.4 ARTA | M05 Spec Block 3b.1 (Risk.response_strategy) |
| 5 | Added `ChangeItemType` ENUM (§3.77) — 6 values | M05 Spec Block 3b.3 (Change.change_type) |
| 6 | Added `ChangeItemStatus` ENUM (§3.78) — 5 values (Draft / Under_Assessment / Approved / Rejected / Withdrawn) | M05 Spec Block 3b.3 (Change.status) |
| 7 | Added `VariationOrderType` ENUM (§3.79) — 6 values | M05 Spec Block 3b.4 (VariationOrder.vo_type) |
| 8 | Added `VOCause` ENUM (§3.80) — 6 values | M05 Spec Block 3b.4 (VariationOrder.vo_cause) |
| 9 | Added `VOStatus` ENUM (§3.81) — **7-state machine** (Draft / Assessed / Submitted / Approved / Materialised / Closed / Rejected) per Brief v1.0a OQ-1.5 patch — explicit Submitted handoff between QS_MANAGER assessor and PMO_DIRECTOR / FINANCE_LEAD approver | M05 Spec Block 3b.4 (VariationOrder.status) |
| 10 | Added `VOApprovalLevel` ENUM (§3.82) — 2 values (Single / Dual) — derived from cost_impact_inr vs threshold | M05 Spec Block 3b.4 (VariationOrder.approval_level) |
| 11 | Added `VOMaterialisationStatus` ENUM (§3.83) — 3 values (In_Progress / Complete / Failed) | M05 Spec Block 3b.6 (VOBOQMaterialisation.materialisation_status) |
| 12 | Added `EOTClaimBasis` ENUM (§3.84) — 5 values (Employer_Default / Statutory_Delay / Unforeseen_Ground / Force_Majeure / Concurrent_Delay) | M05 Spec Block 3b.7 (ExtensionOfTime.claim_basis) |
| 13 | Added `EOTStatus` ENUM (§3.85) — 5 values (Claim_Raised / Under_Assessment / Granted / Rejected / Withdrawn) | M05 Spec Block 3b.7 (ExtensionOfTime.status) |
| 14 | Added `EWNStatus` ENUM (§3.86) — 3 values (Active / Closed / Lapsed) | M05 Spec Block 3b.9 (EarlyWarningNotice.status) |
| 15 | Added `ContingencyDrawdownStatus` ENUM (§3.87) — 4 values (Requested / Approved / Rejected / Reversed) | M05 Spec Block 3b.11 (ContingencyDrawdownLog.status) |
| 16 | Added `LDStatus` ENUM (§3.88) — 4 values (Not_Started / Accruing / Cap_Reached / Waived) | M05 Spec Block 3b.12 (LDExposureRecord.ld_status) |
| 17 | §4.12 `AuditEventType` extended with 16 new M05-owned event types (Block 8b of M05 Spec) | M05 Spec Block 8b |
| 18 | §4.17 `M05_DecisionQueueTriggerType` (NEW; M05-owned) — 10 trigger types (Block 8c of M05 Spec) | M05 Spec Block 8c |

---

## SECTIONS UNCHANGED FROM v0.6a

§1 (Naming Conventions), §2 (Versioning Discipline), §3.1 — §3.72 (existing system + M01-M06 ENUMs), §5 (ENUM Reference Patterns), §6 (Reserved Fields), §7 (Glossary).

For full content of unchanged sections, refer to `X8_GlossaryENUMs_v0_6.md` (preserved historically).

---

## §3 ENUM CATALOGUE (M05 NEW v0.7 — additive)

### 3.1 — 3.72 *Unchanged from v0.6a.*

[Severity, RAGStatus, HealthBand, SpeedTier, RecordStatus, LockState, UserStatus, ProjectStatus, Phase, StageGate, GatePassageOutcome, DataSource, Currency, Unit, BillableState, Discipline, SectorTopLevel, DeliveryModel, PartyType, PartyRole, ContractRole, ContractType, ScenarioActive, KPIName, KPIDirection, Region, BACIntegrityStatus, BOQOrigin, BOQRateSpikeFormula, PackageTemplateTier, BACChangeType, UnitTier, UnitCategory, UnitSystem, PackageType, ChainValidationStatus, CSVImportMode, CSVImportTarget, CSVImportRecordAction, BaselineExtensionCause, LoadingProfileType, ResourceType, ReportingPeriodType, MilestoneStatus, MilestoneType, ScheduleEntryStatus, ProcurementItemStatus, WeatherWindowSeverity, BaselineExtensionStatus, ScheduleImportSource, ScheduleImportMode, ProgressMeasurementMethod, ProgressApprovalStatus, EVConfidence, NCRStatus, NCRRootCauseCategory, MaterialReceiptStatus, MaterialQCStatus, MaterialQCDecision, CostLedgerEntryState, PurchaseOrderStatus, RABillStatus, RABillTriggerSource, GRNMatchStatus, VendorInvoiceStatus, InvoiceMatchMode, InvoiceMatchStatus, PaymentEvidenceStatus, RetentionReleaseType, RetentionReleaseStatus, ExchangeRateTier, BGType — see v0.3 / v0.4 / v0.5 / v0.6 / v0.6a.]

---

### 3.73 `RiskCategory` (M05-owned) — **NEW v0.7**

Per M05 Brief OQ-1.1 implicit + Spec Block 3b.1 `Risk.category`. Captures the dominant nature of a risk for filtering, reporting, and portfolio rollup.

```
ENUM RiskCategory {
  Strategic        // Risks affecting strategic objectives (e.g., portfolio shift, market entry)
  Financial        // Risks with primary financial exposure (e.g., cost overrun, currency, payment delay)
  Operational      // Risks affecting operational delivery (e.g., resource availability, vendor performance)
  Regulatory       // Risks tied to regulatory compliance (e.g., environmental clearance, statutory deadlines)
  Clinical         // Risks tied to clinical / hospital operational readiness (KDMC pilot context)
  Market           // Risks from external market conditions (e.g., commodity prices, demand shift)
  ESG              // Environmental / Social / Governance risks (deferred substantive treatment to Phase 2 M32 BenefitRealization)
  Force_Majeure    // Risks from acts of god, war, pandemic, etc.
}
```

**Anti-drift note:** Phase 2 cascade may add finer-grained sub-categories via `RiskCategorySubType` ENUM additive cascade. Existing 8 values remain stable as parent categories.

---

### 3.74 `RiskRAGStatus` (M05-owned, derived) — **NEW v0.7**

Per M05 Brief OQ-1.2 cascade lock + Spec BR-05-004. Read-only derivation from `risk_score = probability_score × impact_score`.

```
ENUM RiskRAGStatus {
  Green            // risk_score in 1..4    (low concern)
  Amber            // risk_score in 5..12   (moderate; monitor)
  Red              // risk_score in 13..25  (high; response_strategy MANDATORY per BR-05-006)
}
```

**Anti-drift note:** Threshold values (1-4, 5-12, 13-25) locked in M05 Spec BR-05-004; not configurable; not user-overridable. Aligns with X9 v0.4 dual-encode discipline (numeric drives RAG; never the inverse).

---

### 3.75 `RiskStatus` (M05-owned) — **NEW v0.7**

Per M05 Brief OQ-2.6 + Spec BR-05-002. State machine reflecting risk lifecycle.

```
ENUM RiskStatus {
  Draft            // Just raised; not yet accepted by PROJECT_DIRECTOR / PMO_DIRECTOR (broad-raise pattern per OQ-2.6)
  Active           // Accepted; under monitoring
  Mitigating       // Response strategy populated; mitigation in progress
  Closed           // Mitigation complete; residual_risk_score <= 6 + PMO_DIRECTOR sign-off (per BR-05-008)
  Reopened         // Re-opened from Closed (PMO override; audited)
  Withdrawn        // Raised in error; withdrawn within 24hr by raiser (Draft only)
}
```

**State transitions:** `Draft → Active` (ACCEPT_RISK by PROJECT_DIRECTOR/PMO_DIRECTOR), `Active → Mitigating` (response_strategy populated), `Mitigating → Closed` (residual_risk_score ≤ 6 + PMO sign-off), `Active/Mitigating → Reopened` (PMO override), `Draft → Withdrawn` (raiser within 24hr only).

---

### 3.76 `RiskResponseStrategy` (M05-owned) — **NEW v0.7**

Per M05 Brief OQ-1.4 ARTA lock. PMBOK 4-type (threats only).

```
ENUM RiskResponseStrategy {
  Avoid            // Eliminate the risk by changing the project plan
  Reduce           // Reduce probability or impact via mitigation actions
  Transfer         // Transfer the risk to another party (insurance, contracts, BG)
  Accept           // Acknowledge and accept the risk; budget contingency for it
}
```

**Anti-drift note:** PMBOK 7-type (with Exploit / Enhance / Share for opportunities) is Phase 2 cascade extension. Phase 1 ships ARTA only.

---

### 3.77 `ChangeItemType` (M05-owned) — **NEW v0.7**

Per M05 Spec Block 3b.3 `Change.change_type`. Classifies the trigger of a scope change before potential promotion to VO.

```
ENUM ChangeItemType {
  Site_Instruction         // Verbal/written instruction from engineer's representative
  RFI                       // Request For Information (formal correspondence — M13 owns metadata, M05 references)
  Drawing_Revision          // Updated design drawing requiring scope review
  Specification_Change      // Specification document amendment
  Scope_Clarification       // Clarification on existing scope (often closes without VO)
  Other                     // Free-form (description ≥ 100 chars required per BR for type=Other; future BR cascade)
}
```

---

### 3.78 `ChangeItemStatus` (M05-owned) — **NEW v0.7**

Per M05 Spec Block 3b.3 `Change.status`.

```
ENUM ChangeItemStatus {
  Draft                     // Just raised
  Under_Assessment          // QS_MANAGER reviewing for potential VO promotion
  Approved                  // Accepted as scope change (may or may not promote to VO)
  Rejected                  // Determined to not be a scope change
  Withdrawn                 // Raiser withdrew before assessment
}
```

---

### 3.79 `VariationOrderType` (M05-owned) — **NEW v0.7**

Per M05 Spec Block 3b.4 `VariationOrder.vo_type`. Classifies the nature of the variation.

```
ENUM VariationOrderType {
  Scope_Addition                    // Net positive addition to scope/cost
  Scope_Reduction                   // Net negative reduction to scope/cost
  Design_Change                     // Design modification (may be cost-neutral)
  Statutory_Requirement             // Driven by regulatory change
  Unforeseen_Condition              // Site condition not foreseeable at tender (e.g., rock encountered)
  Provisional_Sum_Finalisation      // Conversion of provisional sum to firm scope
}
```

---

### 3.80 `VOCause` (M05-owned) — **NEW v0.7**

Per M05 Spec Block 3b.4 `VariationOrder.vo_cause`. Drives EWN-mandate logic per BR-05-016.

```
ENUM VOCause {
  Delay                     // Caused a schedule delay (EWN MANDATORY per BR-05-016)
  Scope_Increase            // Scope increased (EWN MANDATORY per BR-05-016)
  Scope_Decrease            // Scope reduced (no EWN required)
  Design_Variation          // Design change without scope shift (no EWN required)
  Site_Condition            // Site condition discovery (EWN strongly recommended; not strict-mandate)
  Other                     // Free-form (justification ≥ 200 chars required per future BR)
}
```

**Anti-drift note:** EWN-mandate logic is BR-driven, not ENUM-driven. Adding new VOCause values requires BR-05-016 rule update.

---

### 3.81 `VOStatus` (M05-owned) — **NEW v0.7**

Per M05 Brief v1.0a OQ-1.5 cascade lock + Spec BR-05-009. **7-state machine** with explicit Submitted handoff between QS_MANAGER assessor and PMO_DIRECTOR / FINANCE_LEAD approver.

```
ENUM VOStatus {
  Draft                     // Created; cost_impact_inr may be null
  Assessed                  // QS_MANAGER has assessed cost impact; cost_impact_inr populated
  Submitted                 // QS_MANAGER submits for approval; VO_PENDING_APPROVAL DQ trigger fires per BR-05-011
  Approved                  // Single sign-off (≤ threshold) OR dual sign-off (> threshold) complete per BR-05-012
  Materialised              // SYSTEM action: M02 has confirmed BOQ update complete; VOBOQMaterialisation.materialisation_status=Complete (per BR-05-014)
  Closed                    // Final state; VO fully reconciled
  Rejected                  // Terminal-from-{Draft, Assessed, Submitted}; cannot reject after Approved (use compensating VO)
}
```

**State machine constraints (from Spec BR-05-009..017):**
- Forward-only transitions; no skipping; no reversal after Materialised
- `Materialised` is a SYSTEM action only; no human role can manually transition to Materialised (per F2 governance lock; PMO_DIRECTOR has retry permission only)
- `Submitted` state is required for `VO_PENDING_APPROVAL` Decision Queue trigger to anchor on (per OQ-2.3)

---

### 3.82 `VOApprovalLevel` (M05-owned, derived) — **NEW v0.7**

Per M05 Brief OQ-1.5 + Spec Block 3b.4. Read-only derivation from `cost_impact_inr` vs `ProjectRiskConfig.dual_signoff_threshold_inr`.

```
ENUM VOApprovalLevel {
  Single           // cost_impact_inr <= threshold; PMO_DIRECTOR OR FINANCE_LEAD signs
  Dual             // cost_impact_inr > threshold; BOTH PMO_DIRECTOR AND FINANCE_LEAD sign
}
```

**Default threshold:** ₹50,00,000 (50 lakh) per OQ-1.5; configurable via `ProjectRiskConfig.dual_signoff_threshold_inr` per OQ-2.5.

---

### 3.83 `VOMaterialisationStatus` (M05-owned) — **NEW v0.7**

Per M05 Spec Block 3b.6 `VOBOQMaterialisation.materialisation_status`.

```
ENUM VOMaterialisationStatus {
  In_Progress      // M02 has received VO_APPROVED event; BOQ update in flight
  Complete         // M02 confirmed BOQ update successful; M05.VO transitions to Materialised per BR-05-014
  Failed           // M02 reported failure; M05.VO stays at Approved; VO_MATERIALISATION_FAILED DQ trigger raised per BR-05-015
}
```

---

### 3.84 `EOTClaimBasis` (M05-owned) — **NEW v0.7**

Per M05 Spec Block 3b.7 `ExtensionOfTime.claim_basis`. Classifies the contractual ground for EOT.

```
ENUM EOTClaimBasis {
  Employer_Default          // Delay caused by employer's default (e.g., delayed land handover)
  Statutory_Delay           // Delay caused by statutory/regulatory authority (e.g., environmental clearance)
  Unforeseen_Ground         // Unforeseen physical condition (e.g., rock, water table)
  Force_Majeure             // Acts of god, war, pandemic
  Concurrent_Delay          // Multiple concurrent causes (assessment apportions days_granted)
}
```

---

### 3.85 `EOTStatus` (M05-owned) — **NEW v0.7**

Per M05 Spec Block 3b.7 `ExtensionOfTime.status`.

```
ENUM EOTStatus {
  Claim_Raised              // Just raised; awaiting assessment
  Under_Assessment          // PLANNING_ENGINEER assessing claim merit + days
  Granted                   // PMO_DIRECTOR granted (full or partial); cascade to M03 BaselineExtension fires per BR-05-021
  Rejected                  // PMO_DIRECTOR rejected; rejection_reason mandatory ≥100 chars
  Withdrawn                 // Claimant withdrew before assessment
}
```

**Partial grant logic:** when `granted_days < claim_days`, `partial_grant_reason` mandatory ≥100 chars per BR-05-019.

---

### 3.86 `EWNStatus` (M05-owned) — **NEW v0.7**

Per M05 Spec Block 3b.9 `EarlyWarningNotice.status`. Auto-lapse after `ProjectRiskConfig.ewn_lapse_days` (default 30) per BR-05-025.

```
ENUM EWNStatus {
  Active           // Just raised; valid as prerequisite for EOT/VO claim
  Closed           // Linked to subsequent EOT/VO that has reached terminal state per BR-05-024
  Lapsed           // Auto-transitioned by daily sweep when no claim raised within ewn_lapse_days per BR-05-025; subsequent claims referencing this EWN are blocked
}
```

---

### 3.87 `ContingencyDrawdownStatus` (M05-owned) — **NEW v0.7**

Per M05 Spec Block 3b.11 `ContingencyDrawdownLog.status`.

```
ENUM ContingencyDrawdownStatus {
  Requested        // Just raised by PROJECT_DIRECTOR or PMO_DIRECTOR
  Approved         // PMO_DIRECTOR approved (no self-approval per BR-05-028); ContingencyPool.consumed_inr updated atomically
  Rejected         // PMO_DIRECTOR rejected; rejection_reason mandatory ≥100 chars
  Reversed         // Compensating entry created; original drawdown semantically reversed (M06 precedent)
}
```

---

### 3.88 `LDStatus` (M05-owned) — **NEW v0.7**

Per M05 Spec Block 3b.12 `LDExposureRecord.ld_status`.

```
ENUM LDStatus {
  Not_Started      // NCR exists but not yet aged past threshold
  Accruing         // NCR aged past ncr_aging_to_ld_days; LD eligibility flag set true; amount accruing per BR-05-031
  Cap_Reached      // Cumulative LD reached ld_cap_pct × contract_value; further accrual blocked per BR-05-035
  Waived           // PMO_DIRECTOR override (audited); NCR-specific LD waived
}
```

**Anti-drift note:** Cap is project-level cumulative across all LDExposureRecord rows, not per-NCR. Cap_Reached on one record cascades to global stop on subsequent NCR sweeps.

---

## §4 — M34-OWNED ENUMs (extended in v0.7)

[§4.1 through §4.11 unchanged from v0.6a — see prior versions.]

### §4.12 `AuditEventType` — extended in v0.7

**M05-owned event types — NEW v0.7 (16 events from M05 Spec Block 8b):**

```
RISK_RAISED                              // BR-05-002
RISK_ACCEPTED                            // BR-05-002
RISK_SCORE_CHANGED                       // BR-05-003 + BR-05-004
RISK_RESPONSE_PLAN_UPDATED               // BR-05-007
RISK_CLOSED                              // BR-05-008
RISK_WITHDRAWN                           // BR-05-002
CHANGE_RAISED                            // M05 Spec Block 3b.3
VO_DRAFTED                               // BR-05-009
VO_ASSESSED                              // BR-05-010
VO_SUBMITTED                             // BR-05-011
VO_APPROVED                              // BR-05-012 + BR-05-013
VO_REJECTED                              // BR-05-009
VO_MATERIALISED                          // BR-05-014 + BR-05-017
VO_MATERIALISATION_FAILED                // BR-05-015
VO_CLOSED                                // BR-05-009
EOT_CLAIM_RAISED                         // BR-05-018
EOT_UNDER_ASSESSMENT                     // M05 Spec Block 3b.7
EOT_GRANTED                              // BR-05-020 + BR-05-021
EOT_REJECTED                             // M05 Spec Block 3b.7
EOT_BASELINE_CASCADE_FAILED              // BR-05-022
EWN_RAISED                               // BR-05-023
EWN_CLOSED                               // BR-05-024
EWN_LAPSED                               // BR-05-025
LD_ELIGIBILITY_FLIPPED_TRUE              // BR-05-032 + BR-05-033
LD_ELIGIBILITY_FLIPPED_FALSE             // BR-05-032
LD_AMOUNT_CALCULATED                     // BR-05-031
LD_CAP_REACHED                           // BR-05-035
CONTINGENCY_DRAWDOWN_REQUESTED           // BR-05-027
CONTINGENCY_DRAWDOWN_APPROVED            // BR-05-028
CONTINGENCY_DRAWDOWN_REJECTED            // M05 Spec Block 3b.11
PROJECT_RISK_INITIALISED                 // BR-05-001
RISK_ADJUSTED_EAC_DELTA                  // M05 Spec Block 7b (forward to M07)
CLAIMS_EXPOSURE_SUMMARY_EMITTED          // M05 Spec Block 7b (forward to M19 Phase 2)
```

**Total M05 event types: 33 events.**

[Other modules' event types (M01-M06) unchanged from v0.6a.]

---

### §4.17 `M05_DecisionQueueTriggerType` (NEW v0.7) — M05-owned

10 trigger types per M05 Spec Block 8c. All UPPER_SNAKE_CASE per `naming-folders.md`.

```
ENUM M05_DecisionQueueTriggerType {
  HIGH_RISK_THRESHOLD_BREACH               // risk_score ≥ 13 with no response_action_plan after 48hr (BR-05-006)
  EWN_LAPSE_APPROACHING                    // 75% of lapse window elapsed (BR-05-026)
  EOT_CLAIM_PENDING_ASSESSMENT             // Under_Assessment SLA (M05 Spec Block 4a action SLA)
  VO_PENDING_APPROVAL                      // Submitted state SLA (BR-05-011)
  LD_CAP_APPROACHING                       // cumulative ≥ 80% of cap (BR-05-034)
  LD_CAP_REACHED                           // cumulative = 100% (BR-05-035)
  CONTINGENCY_POOL_DEPLETION_HIGH          // ≥ 80% (BR-05-029)
  CONTINGENCY_POOL_DEPLETION_CRITICAL      // ≥ 95% (BR-05-030)
  VO_MATERIALISATION_FAILED                // M02 sync error (BR-05-015)
  EOT_BASELINE_CASCADE_FAILED              // M03 sync error (BR-05-022)
}
```

[Other modules' Decision Queue trigger ENUMs (e.g., §4.13 M01_DecisionQueueTriggerType, §4.14 M02_..., etc.) unchanged from v0.6a.]

---

## §5 — ENUM Reference Patterns (unchanged from v0.6a)

[See prior versions.]

---

## §6 — Reserved Fields (extended in v0.7 — M05 append-only ledger exemptions added)

Append-only entities (DB-level UPDATE/DELETE forbidden — no `updated_by`, `updated_at`, `is_active`):

| Module | Entity | Why Append-Only |
|---|---|---|
| M02 | BACIntegrityLedger | DB UPDATE/DELETE forbidden; provenance |
| M02 | IDGovernanceLog | Append-only |
| M02 | CSVImportRecord | Append-only |
| M01 | ProjectPhaseHistory | Append-only |
| M01 | ProjectStatusHistory | Append-only |
| M34 | LoginAttempt | Append-only |
| M34 | SystemAuditLog | Append-only |
| M03 | Baseline | Sealed at SG-6; immutable after lock |
| M03 | BaselineExtension | Append-only after approval |
| M03 | PVProfileSnapshot | Historical snapshots immutable |
| M04 | ProgressEntryAudit | Append-only |
| M04 | NCRStatusLog | Append-only |
| M04 | MaterialReceiptLedger | Append-only |
| M04 | ContractorPerformanceScoreLog | Append-only |
| M06 | CostLedgerEntry | 4-state Budgeted→Committed→Accrued→Paid; reversals via compensating entries |
| M06 | RABillAuditLog | Append-only |
| M06 | PaymentEvidenceLedger | Append-only |
| M06 | ForexRateLog | Append-only |
| **M05** | **RiskStatusLog** | **NEW v0.7 — Append-only per M05 Spec Block 3b.2 + OQ-2.2** |
| **M05** | **VOStatusLog** | **NEW v0.7 — Append-only per M05 Spec Block 3b.5 + OQ-2.2** |
| **M05** | **EOTStatusLog** | **NEW v0.7 — Append-only per M05 Spec Block 3b.8 + OQ-2.2** |
| **M05** | **ContingencyDrawdownLog** | **NEW v0.7 — Append-only per M05 Spec Block 3b.11 + OQ-2.2; reversals via compensating entries (M06 precedent)** |
| **M05** | **LDExposureLog** | **NEW v0.7 — Append-only per M05 Spec Block 3b.13 + OQ-2.2** |

**Total append-only entities: 23** (was 18 in v0.6a; +5 from M05 in v0.7).

---

## §7 — Glossary (unchanged from v0.6a)

[See prior versions for ARTA, EAC, EVM, EOT, EWN, LD, PV, RA Bill, VO, etc.]

**New v0.7 glossary terms (M05-driven):**

- **EWN — Early Warning Notice.** Formal notice raised under NEC4 / FIDIC alignment (M05 OQ-1.8 lock) before raising an EOT or VO claim. Mandatory for VO with `vo_cause IN (Delay, Scope_Increase)` and for all EOT claims. Auto-lapses after `ProjectRiskConfig.ewn_lapse_days` (default 30) if no claim links to it.

- **ARTA — Avoid / Reduce / Transfer / Accept.** PMBOK 4-type risk response strategy (threats only). Phase 1 lock (M05 OQ-1.4 = A). Phase 2 cascade may extend to PMBOK 7-type (with Exploit / Enhance / Share for opportunities).

- **VO Materialisation.** The system action by which an Approved VariationOrder triggers M02 BOQ update. Performed by SYSTEM (M02 receives `VO_APPROVED` event from M05; M02 creates `VOBOQMaterialisation` rows; M05 transitions VO to Materialised on M02 confirmation). No human role can manually materialise a VO (governance lock).

- **Contingency Pool.** Per-project monetary buffer initialised from `M01.Contract.contract_value × M01.Contract.risk_buffer_pct` (default 5%). Drawdowns approved by PMO_DIRECTOR only (no self-approval). Forward-only depletion; reversals via compensating ContingencyDrawdownLog entries.

- **LD (Liquidated Damages) Cap.** Project-level cumulative ceiling on LD accrual = `M01.Contract.ld_cap_pct × M01.Contract.contract_value` (default 10%). Beyond cap, further LD accrual is blocked per BR-05-035 (the rule that converts theoretical LD exposure into commercial reality).

---

*v0.7 — LOCKED 2026-05-04 (Round 33). Source modules: M34, M01, M02, M03, M04, M05 (NEW v0.7), M06. Next bump: v0.8 anticipated at M07 EVMEngine Spec lock (Round 45).*
