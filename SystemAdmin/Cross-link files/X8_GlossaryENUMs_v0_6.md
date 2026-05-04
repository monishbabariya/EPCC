# X8 — Glossary & ENUMs
## Cross-Cutting Document v0.6 (LIVING)
**Owner:** PMO Director / System Architect
**Created:** 2026-05-03 (v0.1) | **Updated:** 2026-05-04 (v0.6)
**Status:** Living — appended on every module spec lock
**Source modules locked into this version:** M34, M01, M02, M03, M04, **M06**
**Folder:** SystemAdmin/Cross-link files/ (per Round 18 audit canonical placement)

---

## CHANGES IN v0.6

| # | Change | Driven By |
|---|---|---|
| 1 | Added `CostLedgerEntryState` ENUM (§3.60) — 4-state machine (Budgeted → Committed → Accrued → Paid) | M06 Spec Block 3b |
| 2 | Added `PurchaseOrderStatus` ENUM (§3.61) — 6 values | M06 Spec Block 3c |
| 3 | Added `RABillStatus` ENUM (§3.62) — 5 values | M06 Spec Block 3d |
| 4 | Added `RABillTriggerSource` ENUM (§3.63) — 2 values (Progress/Milestone) | M06 Brief OQ-1.3=B |
| 5 | Added `GRNMatchStatus` ENUM (§3.64) — 4 values; GRN.qc_decision_at_emit reuses §3.59 MaterialQCDecision (no new lifecycle ENUM) | M06 Spec Block 3g |
| 6 | Added `VendorInvoiceStatus` ENUM (§3.65) — 7 values | M06 Spec Block 3h |
| 7 | Added `InvoiceMatchMode` ENUM (§3.66) — 2 values (Two_Way / Three_Way) | M06 Spec Block 3i |
| 8 | Added `InvoiceMatchStatus` ENUM (§3.67) — 6 values | M06 Spec Block 3i |
| 9 | Added `PaymentEvidenceStatus` ENUM (§3.68) — 4 values; absorbs Brief-anticipated PaymentWorkflowStep | M06 Spec Block 3j |
| 10 | Added `RetentionReleaseType` ENUM (§3.69) — 3 values (Substantial_Completion / DLP_End / PMO_Override) | M06 Brief OQ-1.8=C |
| 11 | Added `RetentionReleaseStatus` ENUM (§3.70) — 6 values | M06 Spec Block 3l |
| 12 | Added `ExchangeRateTier` ENUM (§3.71) — 2 values (RBI_Reference / Bank_Transaction) | M06 Brief OQ-1.6=B |
| 13 | Added `BGType` ENUM (§3.72) — 5 values (BGStub-pattern; migrates to M23 in Phase 2 — ENUM stays in X8) | M06 Brief OQ-1.9=B |
| 14 | M06-owned audit event types (43) added to AuditEventType extension (§4.12) — locked from M06 Spec Appendix A | M06 Spec Appendix A |
| 15 | M06-owned Decision Queue trigger types (12) catalogued (§4.17) | M06 Spec Appendix A |
| 16 | M06 append-only entities (4) added to reserved-fields exemption list (§6) — CostLedgerEntry, RABillAuditLog, PaymentEvidenceLedger, ForexRateLog | M06 Spec Block 3a |
| 17 | **§3.10 StageGate description refresh** — SG_9 = "Substantial / Practical Completion (clinical commissioning ready)"; SG_11 = "DLP End / Operations Handover". Sequence stays locked (SG_0 → SG_11 immutable); description text only — pre-empts M08 build-time reopening per Round 26 cascade detection | M06 Spec v1.0a + Workflows v1.0 commitments |
| 18 | Brief→Spec ENUM-count delta (informational) — Brief §9 anticipated PaymentWorkflowStep + BACIntegrityWarningSource ENUMs that Spec did NOT introduce (workflow collapsed into §3.68 PaymentEvidenceStatus; warning collapsed to a boolean flag per OQ-1.4=B). Net new ENUMs: 13, not 15 | M06 Spec Round 24 |

**Cascade notes:** M06 also triggers a single-field cascade on M01 (`Contract.dlp_retention_split_pct` — see `M01_ProjectRegistry_v1_3_CascadeNote.md`) and a minor cascade on M03 (`MILESTONE_ACHIEVED_FINANCIAL` audit-event emit hook — see `M03_PlanningMilestones_v1_2_CascadeNote.md`). Neither alters X8 scope; both are predecessor-spec changes that consume X8 v0.6 ENUMs.

---

## 1. PURPOSE

[unchanged from v0.5]

Single canonical reference for:
- Every ENUM type used across EPCC modules
- Every system-wide vocabulary term
- Every reserved keyword that a module spec must NOT redefine

**Rule:** When writing any module spec, look up here FIRST.

---

## 2. NAMING CONVENTIONS — LOCKED

[unchanged from v0.3]

| Concept | Convention | Example |
|---|---|---|
| ENUM type name | PascalCase | `UserStatus`, `BaselineExtensionCause` |
| ENUM values (system identifiers) | `UPPER_SNAKE_CASE` | `SYSTEM_ADMIN` |
| ENUM values (status states) | `Pascal_Snake_Case` | `Stale_Pending_VO`, `Force_Majeure` |
| Severity / RAG | Pascal single word | `Critical`, `Green` |
| Permission codes | `lower_snake_case` | `view_project` |
| Role codes | `UPPER_SNAKE_CASE` | `PMO_DIRECTOR` |
| Field names | `lower_snake_case` | `user_id` |
| BR codes | `BR-{module_id}-{seq}` | `BR-03-008` |
| Decision Queue triggers | `UPPER_SNAKE_CASE` | `CRITICAL_PATH_DELAY` |
| Audit event types | `UPPER_SNAKE_CASE` | `BASELINE_LOCKED` |

---

## 3. SYSTEM-WIDE ENUMS

### 3.1 — 3.9 *Unchanged from v0.5.*

[Severity, RAGStatus, HealthBand, SpeedTier, RecordStatus, LockState, UserStatus, ProjectStatus, Phase — see v0.3.]

---

### 3.10 `StageGate` (System-owned) — **DESCRIPTION REFRESHED v0.6**

**Sequence locked at v0.1 — v0.6 refreshes only the per-gate description text** to ratify M06 Spec v1.0a + Workflows v1.0 SG_9/SG_11 semantics. No new values; no value renames; no ordering change.

```
ENUM StageGate {
  SG_0           // Pre-investment screen / portfolio admission
  SG_1           // Concept feasibility approval
  SG_2           // DPR / FEED approval
  SG_3           // Capital sanction / financial close
  SG_4           // Design freeze / IFC issue
  SG_5           // Construction mobilisation / contract award
  SG_6           // Baseline lock (schedule + BAC + cost)
  SG_7           // Mid-construction control gate
  SG_8           // Pre-commissioning readiness
  SG_9           // Substantial / Practical Completion
                 // (clinical commissioning ready; tranche-1 retention release trigger per M06 BR-06-027)
  SG_10          // Operations commencement / contract Go-Live
  SG_11          // DLP End / Operations Handover
                 // (defects-liability period closure; tranche-2 retention release trigger per M06 BR-06-028)
}
```

**Description-refresh rationale (Round 26):** Earlier v0.1 description text labelled SG_9 = "Clinical commissioning" and SG_11 = "Operations handover". M06 Spec v1.0a (in-place patch from `SG_11_PASSAGE` → `SG_9_PASSAGE` for tranche-1) clarified that in healthcare DBOT context "Clinical commissioning ready" *is* Substantial Completion, and "Operations handover" maps semantically to DLP End. v0.6 ratifies this so M08 builder does not face an open question. Stage-gate sequence (`SG_0 → SG_11`, ordered, immutable) unchanged.

---

### 3.11 — 3.59 *Unchanged from v0.5.*

[GatePassageOutcome, DataSource, Currency, Unit, BillableState, Discipline, Sector→DEPRECATED, SectorTopLevel, DeliveryModel, PartyType, PartyRole, ContractRole, ContractType, ScenarioActive, KPIName, KPIDirection, Region, BACIntegrityStatus, BOQOrigin, BOQRateSpikeFormula, PackageTemplateTier, BACChangeType, UnitTier, UnitCategory, UnitSystem, PackageType, ChainValidationStatus, CSVImportMode, CSVImportTarget, CSVImportRecordAction, BaselineExtensionCause, LoadingProfileType, ResourceType, ReportingPeriodType, MilestoneStatus, MilestoneType, ScheduleEntryStatus, ProcurementItemStatus, WeatherWindowSeverity, BaselineExtensionStatus, ScheduleImportSource, ScheduleImportMode, ProgressMeasurementMethod, ProgressApprovalStatus, EVConfidence, NCRStatus, NCRRootCauseCategory, MaterialReceiptStatus, MaterialQCStatus, MaterialQCDecision — see v0.3 / v0.4 / v0.5.]

---

### 3.60 `CostLedgerEntryState` (M06-owned) — **NEW v0.6**

Per M06 Brief OQ-1.1=A and Spec Block 3b. The 4-state machine mirrors `architecture.md` Financial Control States lock. Transitions are append-only (each state change writes a new CostLedgerEntry row with `state` set; predecessor row's `state` is never updated — DB-level UPDATE/DELETE forbidden via REVOKE).

```
ENUM CostLedgerEntryState {
  Budgeted       // BAC allocation accepted from M02; no commitment yet
  Committed      // PO issued (or contract milestone obligated) — funds reserved
  Accrued        // GRN received OR Approved RA Bill — economic obligation incurred
  Paid           // PaymentEvidence confirmed; cash/bank evidence handed to ERP
}
```

**Forward-only transitions:** `Budgeted → Committed → Accrued → Paid`. Reversals are NOT in-place edits — they are new compensating entries (e.g., a `Paid` reversal writes a new row with negative amount and a back-reference). See M06 BR-06-001..047 for transition rules.

---

### 3.61 `PurchaseOrderStatus` (M06-owned) — **NEW v0.6**

Per M06 Spec Block 3c.

```
ENUM PurchaseOrderStatus {
  Draft                  // PO authored; not yet issued to vendor
  Issued                 // PO sent to vendor; CostLedgerEntry transitions to Committed
  Partially_Received     // Some GRN'd; balance pending
  Fully_Received         // All GRNs in; ready for invoice match
  Closed                 // All invoices reconciled / no further activity
  Cancelled              // PO withdrawn before issuance OR cancelled with reversing CostLedgerEntry
}
```

---

### 3.62 `RABillStatus` (M06-owned) — **NEW v0.6**

Per M06 Spec Block 3d. RA Bill = Running Account Bill (per X8 §7 + glossary.md).

```
ENUM RABillStatus {
  Draft        // Generated from candidate buffer; not yet submitted
  Submitted    // Sent to QS_MANAGER for line-by-line approval
  Approved     // QS + FINANCE_LEAD signed; CostLedgerEntry → Accrued
  Rejected     // QS or FINANCE_LEAD rejected with reason ≥ 100 chars
  Paid         // PaymentEvidence confirmed; CostLedgerEntry → Paid
}
```

---

### 3.63 `RABillTriggerSource` (M06-owned) — **NEW v0.6**

Per M06 Brief OQ-1.3=B (dual trigger: progress-driven + milestone-driven). Locked at 2 values.

```
ENUM RABillTriggerSource {
  Progress     // Generated from M04 BR-04-012 BILLING_TRIGGER_READY (approved progress)
  Milestone    // Generated from M03 MILESTONE_ACHIEVED_FINANCIAL (milestone_type=Financial achieved)
}
```

**Coupling:** Milestone path requires M03 v1.2 cascade note (`MILESTONE_ACHIEVED_FINANCIAL` emit hook).

---

### 3.64 `GRNMatchStatus` (M06-owned) — **NEW v0.6**

Per M06 Spec Block 3g. Match-status only — does NOT track GRN lifecycle. The QC decision recorded at GRN emission is sourced from M04 §3.59 `MaterialQCDecision` ENUM via `GRN.qc_decision_at_emit` field (read-once at emit, never updated thereafter).

```
ENUM GRNMatchStatus {
  Unmatched     // Just received from M04; no PO link yet
  Linked        // PO linked; quantity reconciliation pending
  Matched       // Quantity + rate reconciliation passed
  Disputed      // Discrepancy raised; routes to Decision Queue
}
```

---

### 3.65 `VendorInvoiceStatus` (M06-owned) — **NEW v0.6**

Per M06 Spec Block 3h. Captures the invoice-receipt-to-handoff lifecycle, distinct from `InvoiceMatchStatus` (which tracks the match-engine outcome).

```
ENUM VendorInvoiceStatus {
  Received           // Invoice document received from vendor
  Match_Pending      // PO + GRN linkage in progress
  Match_Passed       // 3-way (or 2-way) match successful
  Match_Failed       // Match failure; routes to Decision Queue
  Evidence_Assembled // PaymentEvidence packet assembled
  Handed_Over        // Evidence handed to FINANCE_LEAD / ERP gateway
  Cancelled          // Invoice withdrawn or duplicated
}
```

---

### 3.66 `InvoiceMatchMode` (M06-owned) — **NEW v0.6**

Per M06 Spec Block 3i. Per-invoice mode selection captured at match-engine entry; defaults to Three_Way for goods, Two_Way for services per M06 ProjectExecutionConfig.

```
ENUM InvoiceMatchMode {
  Two_Way      // Invoice ↔ PO only (services, fee-based engagements)
  Three_Way    // Invoice ↔ PO ↔ GRN (goods receipt required)
}
```

---

### 3.67 `InvoiceMatchStatus` (M06-owned) — **NEW v0.6**

Per M06 Spec Block 3i. Granular match outcome — drives Decision Queue routing decisions.

```
ENUM InvoiceMatchStatus {
  Three_Way_Pass            // PO + GRN + Invoice quantity & rate reconcile within tolerance
  Three_Way_Fail_Quantity   // Quantity mismatch; PMO/QS review
  Three_Way_Fail_Rate       // Rate mismatch; QS/Finance review
  Two_Way_Pass              // PO + Invoice reconcile (services mode)
  Pending                   // Match in progress; not yet evaluated
  Override_Approved         // Mismatch overridden with PMO_DIRECTOR justification ≥ 100 chars
}
```

---

### 3.68 `PaymentEvidenceStatus` (M06-owned) — **NEW v0.6**

Per M06 Spec Block 3j. Absorbs Brief-anticipated `PaymentWorkflowStep` (4 states cover the workflow without a separate ENUM).

```
ENUM PaymentEvidenceStatus {
  Assembled         // Evidence packet (invoice + PO + GRN + match result) bundled; ready for handoff
  Handed_Over       // Handed to FINANCE_LEAD / external ERP gateway
  Confirmed_Paid    // ERP / bank evidence received; CostLedgerEntry → Paid
  Cancelled         // Evidence withdrawn (e.g., invoice cancelled, duplicate detected)
}
```

---

### 3.69 `RetentionReleaseType` (M06-owned) — **NEW v0.6**

Per M06 Brief OQ-1.8=C — locked at 3 values. Tranche split percentage stored on `M01.Contract.dlp_retention_split_pct` (default 0.5000 — see M01 v1.3 cascade note).

```
ENUM RetentionReleaseType {
  Substantial_Completion    // Tranche-1 — released at SG_9_PASSAGE per BR-06-027
  DLP_End                   // Tranche-2 — released at SG_11_PASSAGE per BR-06-028
                            // (gated on M15/M09 zero-counts when those modules ship)
  PMO_Override              // PMO_DIRECTOR releases out-of-cycle with justification ≥ 100 chars
                            // and digital evidence; emits separate audit event
}
```

---

### 3.70 `RetentionReleaseStatus` (M06-owned) — **NEW v0.6**

Per M06 Spec Block 3l.

```
ENUM RetentionReleaseStatus {
  Withheld           // Default; retention deducted from each RA Bill, accumulating
  Eligible           // SG-9 passed (tranche-1) OR SG-11 passed with zero-count guards (tranche-2)
  Approved_Finance   // FINANCE_LEAD approved release packet
  Released           // Payment evidence handed; CostLedgerEntry transitions to Paid
  Blocked            // Release pre-condition failed (e.g., M15 defect count > 0 at SG-11)
  Cancelled          // Release withdrawn (rare; PMO action only)
}
```

---

### 3.71 `ExchangeRateTier` (M06-owned) — **NEW v0.6**

Per M06 Brief OQ-1.6=B (multi-currency support shipped in v1.0). Locked at 2 values.

```
ENUM ExchangeRateTier {
  RBI_Reference        // RBI Reference Rate (ratesheet authority); used for pre-transaction valuation
  Bank_Transaction     // Bank-confirmed transaction rate (post-trade); used for actual reconciliation
}
```

**Default:** `RBI_Reference` for `Forecast`/`Budgeted`/`Committed` valuation; `Bank_Transaction` for `Paid` reconciliation.

---

### 3.72 `BGType` (M06-owned, BGStub-pattern) — **NEW v0.6**

Per M06 Brief OQ-1.9=B. BGStub pattern: M06 owns minimal Bank Guarantee tracking in Phase 1 (status + expiry); full BG lifecycle migrates to M23 in Phase 2. The ENUM stays in X8 — M23 will consume the same definition.

```
ENUM BGType {
  Performance               // Performance BG (most common; tracks contract obligations)
  Advance_Payment           // ABG against advance to vendor/contractor
  Retention_Substitute      // BG in lieu of retention deduction
  Bid                       // Bid BG (often expires at contract award; rare in M06)
  Other                     // Free-form; description must clarify (≥ 50 chars)
}
```

---

## 4. M34-OWNED ENUMS

[§4.1 through §4.11 unchanged from v0.3]

### 4.12 `AuditEventType` (extended in v0.4 + v0.5 + **v0.6**)

**M03-owned event types (locked v0.4):** *unchanged from v0.5* — see v0.5 §4.12.

**M04-owned event types (locked v0.5):** *unchanged from v0.5* — see v0.5 §4.12.

**M06-owned event types — NEW v0.6** (sourced from `M06_FinancialControl_Spec_v1_0.md` Appendix A — 43 events; locked from authoring per Round 18 cascade-pattern discipline):

```
COST_LEDGER_ENTRY_CREATED          // Insert (any state)
COST_LEDGER_STATE_TRANSITIONED     // State machine progression Budgeted→Committed→Accrued→Paid
PURCHASE_ORDER_CREATED             // PO authored (Draft)
PURCHASE_ORDER_AMENDED             // Field edits between Issued and Closed (audit-trail rich)
PURCHASE_ORDER_CANCELLED           // Cancellation event with reversing CostLedgerEntry
RA_BILL_CANDIDATE_BUFFERED         // Bill candidate held in buffer awaiting QS approval batch
RA_BILL_GENERATED                  // Bill instantiated from candidate
RA_BILL_SUBMITTED                  // Submitted to QS for review
RA_BILL_APPROVED_QS                // QS_MANAGER signs (intermediate)
RA_BILL_APPROVED_FINANCE           // FINANCE_LEAD signs (final)
RA_BILL_REJECTED                   // QS or Finance rejects with reason ≥ 100 chars
RA_BILL_PAID                       // PaymentEvidence confirmed; CostLedgerEntry → Paid
GRN_RECEIVED                       // GRN emitted from M04 (BR-04-028 MATERIAL_GRN_EMITTED consumer)
GRN_LINKED_TO_PO                   // PO link established
GRN_INVOICE_MATCHED                // Match engine result captured
VENDOR_INVOICE_RECEIVED            // VendorInvoice document captured
INVOICE_MATCH_PASSED               // 2-way or 3-way pass
INVOICE_MATCH_FAILED               // Match failure (Quantity / Rate)
INVOICE_MATCH_OVERRIDE_APPLIED     // PMO override on a failed match (justification ≥ 100 chars)
EVIDENCE_ASSEMBLED                 // PaymentEvidence packet assembled
EVIDENCE_HANDED_OVER               // Evidence handed to FINANCE_LEAD / ERP gateway
PAYMENT_CONFIRMED                  // Bank evidence captured; CostLedgerEntry → Paid
RETENTION_WITHHELD                 // Retention deducted from RA bill (per-bill event)
RETENTION_TRANCHE_RELEASED         // Tranche-1 or Tranche-2 release event
DLP_RELEASE_PRECONDITION_MET       // SG-11 + M15/M09 zero-counts satisfied
DLP_RELEASE_PRECONDITION_BLOCKED   // SG-11 reached but defect/compliance counts > 0
DLP_RELEASE_PMO_OVERRIDE           // PMO override release outside SG-9/11 windows
FOREX_RATE_ENTERED                 // Manual rate entry into ForexRateLog
FOREX_RATE_LOCKED                  // Rate locked for valuation period
FOREX_RATE_PMO_APPROVED            // PMO approval of out-of-tolerance rate
FOREX_DEVIATION_REVIEW             // Decision Queue trigger — rate deviation > tolerance
FOREX_VARIATION_COMPUTED           // BAC-vs-Actual forex impact computation
CASHFLOW_REGENERATED               // Cashflow projection refresh (scheduled or event-driven)
CASHFLOW_REGEN_FAILED              // Decision Queue trigger — regen errored
M06_CONFIG_CREATED                 // ProjectFinancialConfig auto-create on Project Active
M06_CONFIG_EDITED                  // PMO edit with justification ≥ 100 chars
BG_STATUS_UPDATED                  // BGStub status edit (manual; sparse in Phase 1)
BG_EXPIRING_SOON                   // Decision Queue trigger — BG expiry < threshold (default 30 days)
BG_MIGRATED_TO_M23                 // One-time migration cascade event when M23 lands
BAC_INTEGRITY_WARNING_FLAGGED      // M02 BAC drift surfaced into M06 view (read-only)
COMPLIANCE_HOLD_APPLIED            // M09 compliance hold blocks payment (when M09 ships)
DOCUMENT_ATTACHED                  // Stub-period document URL added (per OQ-2.5)
DOCUMENT_MIGRATED_TO_M12           // One-time migration cascade event when M12 lands
```

### 4.13 `M01_DecisionQueueTriggerType` — *unchanged from v0.3*

### 4.14 `M02_DecisionQueueTriggerType` — *unchanged from v0.3*

### 4.15 `M03_DecisionQueueTriggerType` — *unchanged from v0.4*

### 4.16 `M04_DecisionQueueTriggerType` — *unchanged from v0.5*

### 4.17 `M06_DecisionQueueTriggerType` — **NEW v0.6**

```
CAPITAL_HEADROOM_BREACH              // BR-06-040: cumulative Committed > BAC × headroom_threshold (default 0.95)
COST_OVERRUN_ADVISORY                // BR-06-041: package-level Accrued > BAC × overrun_threshold (default 1.05)
PAYMENT_SLA_BREACH                   // BR-06-042: VendorInvoice in Match_Pending > SLA (default 7 days)
INVOICE_MATCH_FAILED                 // BR-06-024: 3-way match returns Three_Way_Fail_*
FOREX_DEVIATION_APPROVAL             // BR-06-035: rate deviation from RBI_Reference > tolerance pct
FOREX_RATE_NOT_AVAILABLE             // BR-06-036: foreign-currency txn requested with no rate locked for period
FOREX_RATE_NOT_LOCKED                // BR-06-037: payment scheduled in foreign ccy but Bank_Transaction tier missing
BG_EXPIRING_SOON                     // BR-06-043: BGStub.expiry_date < today + threshold (default 30 days)
RETENTION_RELEASE_BLOCKED_DLP        // BR-06-028: SG-11 reached but M15 defects > 0 OR M09 compliance gaps > 0
BAC_INTEGRITY_WARNING                // BR-06-039: M02 surfaces BACIntegrityLedger drift; advisory only (OQ-1.4=B)
CASHFLOW_REGEN_FAILED                // BR-06-044: scheduled regen erroring repeatedly
COMPLIANCE_HOLD_APPLIED              // BR-06-046: M09 compliance hold blocks payment (when M09 ships)
```

All UPPER_SNAKE_CASE per F-013 lock. Confirms M06 Spec Appendix A summary count of 12 Decision Queue triggers.

---

## 5. CODEMASTER CATEGORIES — *unchanged from v0.3*

[unchanged]

---

## 6. RESERVED FIELDS — *updated v0.6*

Every entity (except append-only logs and junction tables) MUST include:

```
tenant_id, created_by, created_at, updated_by, updated_at, is_active
```

**Append-only entity exemption (v0.6 explicit list — extended with M06 ledgers):**
- `BACIntegrityLedger` (M02) — UPDATE/DELETE forbidden at DB level
- `IDGovernanceLog` (M02)
- `CSVImportRecord` (M02)
- `ProjectPhaseHistory` (M01)
- `ProjectStatusHistory` (M01)
- `LoginAttempt` (M34)
- `SystemAuditLog` (M34)
- `Baseline` (M03) — sealed at SG-6; immutable after lock
- `BaselineExtension` (M03) — append-only after approval (no edits to approved extensions)
- `PVProfileSnapshot` (M03) — historical snapshots immutable
- `ProgressEntryAudit` (M04) — every state transition; UPDATE/DELETE forbidden at DB level
- `NCRStatusLog` (M04) — every NCR transition + severity change; UPDATE/DELETE forbidden
- `MaterialReceiptLedger` (M04) — every QC decision + receipt event; UPDATE/DELETE forbidden
- `ContractorPerformanceScoreLog` (M04) — every score recompute / override; UPDATE/DELETE forbidden
- **`CostLedgerEntry` (M06)** — every state transition (Budgeted → Committed → Accrued → Paid); UPDATE/DELETE forbidden at DB level. Reversals via compensating entries with back-reference, never in-place edits.
- **`RABillAuditLog` (M06)** — every RA Bill state change (Draft → Submitted → Approved → Paid / Rejected); UPDATE/DELETE forbidden
- **`PaymentEvidenceLedger` (M06)** — every PaymentEvidence packet event (Assembled → Handed_Over → Confirmed_Paid); UPDATE/DELETE forbidden
- **`ForexRateLog` (M06)** — every rate entry and lock event; UPDATE/DELETE forbidden. Per-tier (RBI_Reference / Bank_Transaction) rates retained for full audit reconstruction.

---

## 7. NAMING DICTIONARY — *unchanged from v0.3*

[unchanged]

---

## 8. EXTENSION PROTOCOL — *unchanged*

[unchanged from v0.3]

---

## 9. CHANGE LOG

| Version | Date | Change |
|---|---|---|
| v0.1 | 2026-05-03 | Initial. M34 ENUMs locked. System-wide ENUMs locked. |
| v0.2 | 2026-05-03 | M01 lock. SectorTopLevel + 8 other M01 ENUMs added. Phase enum migration note. DeliveryModel "Hybrid" retired. |
| v0.3 | 2026-05-03 | M02 lock. 13 new M02 ENUMs added. M02 audit event types and Decision Queue triggers catalogued. CodeMaster Discipline ownership clarified. Append-only entity exemption list explicit. |
| v0.4 | 2026-05-03 | M03 lock. 12 new M03 ENUMs added (BaselineExtensionCause, LoadingProfileType, ResourceType (4 values incl. Vendor_Resource), ReportingPeriodType, MilestoneStatus, MilestoneType, ScheduleEntryStatus, ProcurementItemStatus, WeatherWindowSeverity, BaselineExtensionStatus, ScheduleImportSource, ScheduleImportMode). M03 audit event types (28) and Decision Queue triggers (5) catalogued. Append-only entity exemption list extended with Baseline + BaselineExtension + PVProfileSnapshot. Cascade: M01 v1.2 removes reporting_period_type; M03 owns. |
| v0.5 | 2026-05-03 | M04 lock (Round 20). 8 new M04 ENUMs added (ProgressMeasurementMethod, ProgressApprovalStatus, EVConfidence, NCRStatus, NCRRootCauseCategory, MaterialReceiptStatus, MaterialQCStatus, MaterialQCDecision). M04 audit event types (22 — locked from authoring per Round 18 cascade-pattern) and Decision Queue triggers (8) catalogued. Append-only entity exemption list extended with M04 ledgers (ProgressEntryAudit, NCRStatusLog, MaterialReceiptLedger, ContractorPerformanceScoreLog). EVConfidence carried forward from M07 v3.0 legacy for forward-traceability — M04 writes High/Low; M07 will write Fallback/Derived when built. |
| **v0.6** | **2026-05-04** | **M06 lock (Round 26 + cascade Round 27). 13 new M06 ENUMs added (CostLedgerEntryState, PurchaseOrderStatus, RABillStatus, RABillTriggerSource, GRNMatchStatus, VendorInvoiceStatus, InvoiceMatchMode, InvoiceMatchStatus, PaymentEvidenceStatus, RetentionReleaseType, RetentionReleaseStatus, ExchangeRateTier, BGType). M06 audit event types (43 — locked from authoring per Round 18 cascade-pattern) and Decision Queue triggers (12) catalogued. Append-only entity exemption list extended with 4 M06 ledgers (CostLedgerEntry, RABillAuditLog, PaymentEvidenceLedger, ForexRateLog). §3.10 StageGate description text refreshed — SG_9 = "Substantial / Practical Completion (clinical commissioning ready)" + SG_11 = "DLP End / Operations Handover" — sequence unchanged, ratifies M06 Spec v1.0a + Workflows v1.0 commitments before M08 brief opens. Cascades: M01 v1.3 cascade note (Contract.dlp_retention_split_pct field add) + M03 v1.2 cascade note (MILESTONE_ACHIEVED_FINANCIAL emit hook). Brief→Spec ENUM-count delta: Brief §9 anticipated PaymentWorkflowStep + BACIntegrityWarningSource ENUMs that Spec did NOT introduce (workflow collapsed into PaymentEvidenceStatus; warning collapsed to a boolean flag per OQ-1.4=B) — net new ENUMs: 13.** |

**Future bumps:**
- v0.7 — after M05 spec lock
- v0.8 — after M07 / M08 spec lock
- v0.9 — after M09 / M10 lock
- v1.0 — after all Phase 1 specs locked

---

## 10. ENFORCEMENT — *unchanged*

[unchanged from v0.3]

---

*v0.6 — Living document. M06 ENUMs locked. Next bump on M05 spec lock.*
