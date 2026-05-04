---
artefact: M06_FinancialControl_Spec_v1_0
round: 25
date: 2026-05-03
author: Monish (with Claude assist)
x8_version: v0.5 (with v0.6 cascade pending — 11 new M06 ENUMs proposed; locked at R28 cascade pass)
x9_version: v0.3 (with v0.4 cascade locked at R28)
status: LOCKED
locked_at: 2026-05-03 (Round 25 user confirmation; auditor ACCEPT 0/26 + 3 cosmetic fixes applied; pre-merge round number was 24 — renumbered to 25 post-merge)
brief_locked_in: Round 24 (SystemAdmin/Modules/M06_FinancialControl_Brief_v1_0.md)
re_issue_of: ZEPCC_Legacy/M06_Financial_Control_v2_1.md (amendment-only — base v2.0 absent)
reference_standards: X8_GlossaryENUMs_v0_5.md (+ v0.6 cascade pending), X9_VisualisationStandards_Spec_v0_3.md, M34_SystemAdminRBAC_Spec_v1_0.md, M01_ProjectRegistry_Spec_v1_0.md (+ v1_1_CascadeNote + v1_2_CascadeNote + v1_3_CascadeNote pending), M02_StructureWBS_Spec_v1_0.md, M03_PlanningMilestones_Spec_v1_1.md, M04_ExecutionCapture_Spec_v1_0.md
---

# M06 — Financial Control — Spec v1.0

## CHANGE LOG

| Version | Date | Change Summary |
|---|---|---|
| v1.0 | 2026-05-03 | Initial standalone consolidated spec (Round 24). All 11 OQ-1 + 6 OQ-2 items from Brief v1.0 (Round 23) carried as locked. 4-state CostLedgerEntry pipeline (Budgeted → Committed → Accrued → Paid) per OQ-1.1=A. Per (Package × Period) RABill grain per OQ-1.2=B. Dual trigger sources (Progress + Milestone) per OQ-1.3=B. Stale_Pending_VO flag-don't-block per OQ-1.4=B. Full-lifetime per-WBS-per-period CashflowForecast per OQ-1.5=A. Multi-currency (ForexRateMaster + ForexVariation) shipped from v1.0 per OQ-1.6=B. Split payment scope — 2/3-way match in EPCC, signature workflow external — per OQ-1.7=C. Tranched retention release with dual sign-off per OQ-1.8=C (triggers M01 v1.3 cascade). BGStub mirroring M04→M12 photo-stub pattern per OQ-1.9=B. M06FinancialConfig per-project tunables per OQ-1.10=A. Tax-record-only per OQ-1.11=C. 17 entities (4 append-only ledgers with DB-level UPDATE/DELETE forbidden). 47 BRs. Audit Events Catalogue locked from authoring (Appendix A — 43 events). |
| v1.0a | 2026-05-03 | **Round 26 Workflows-audit correction (in-place patch, not a version bump):** Stage Gate naming disambiguation per Workflows audit — tranche-1 (Substantial Completion) trigger event renamed from `SG_11_PASSAGE` to `SG_9_PASSAGE` (correctly matches SG-9 = Substantial/Practical Completion in 5-layer architecture); tranche-2 (DLP End) retains `SG_11_PASSAGE`. Affects BR-06-027 trigger, Block 7 RECEIVES FROM M08, stub endpoint paths (now both `/sg9-passage` AND `/sg11-passage` exposed), Appendix A `DLP_RELEASE_PRECONDITION_MET` description, KDMC reference appendix tranche annotations, Block 2 EXCLUDES SG signal reference. M08 (when built) must implement BOTH endpoints. No BR additions/removals; no entity changes; no scope drift. Discovered during /build-module Workflows gate audit and patched pre-module-publish. |

---

## BLOCK 1 — IDENTITY

```
Module ID                : M06
Module Name              : Financial Control
Layer                    : L2 — Risk / Commercial
Decision It Enables      : At this report date, where is each rupee of the BAC inside
                           the four-state funnel (Budgeted → Committed → Accrued → Paid),
                           and how much headroom remains at each state?
Primary User             : FINANCE_LEAD (capital funnel, RA bills, retention, payment)
Secondary Users          : PMO_DIRECTOR (capital funnel cross-project + dual sign-off
                                         on retention release + config edits),
                           PROJECT_DIRECTOR (own-project capital funnel + RA-bills-due),
                           PROCUREMENT_OFFICER (vendor invoice + 2/3-way match,
                                                vendor outstanding bar),
                           SITE_MANAGER (capital funnel % only — ₹ values redacted)
Build Priority           : Critical (precedes M07 EVMEngine which consumes AC;
                                     critical for KDMC monthly RA cycle)
Folder                   : SystemAdmin/Modules/ (per Round 18 audit canonical placement)
Re-Issue Of              : Legacy `M06_Financial_Control_v2_1.md` (amendment file —
                           base v2.0 entities reverse-engineered from v2.1 + cross-references)
```

---

## BLOCK 2 — SCOPE BOUNDARY

| INCLUDES | EXCLUDES |
|---|---|
| `CostLedgerEntry` — 4-state immutable pipeline (Budgeted → Committed → Accrued → Paid). The AC backbone consumed by M07. | BAC computation per package — **M02** (M06 reads `Package.bac_amount` via internal API) |
| `PurchaseOrder` — vendor identity + commercial terms. Back-fills `M03 ProcurementScheduleItem.m06_po_id` on issue. | BACIntegrityLedger writes — **M02** owns. M06 reads via internal API only (Single-Owner F-005) |
| `RABill` — per (Package × Period) grain (per Brief OQ-1.2=B). Triggered by M04 `BILLING_TRIGGER_READY` (progress) OR M03 `MILESTONE_ACHIEVED_FINANCIAL` (milestone) per OQ-1.3=B. | Approved progress percentage — **M04** (M06 receives event) |
| `RABillLine` — per-WBS-per-period billing line within an RABill. | VO initiation, approval, monetary impact — **M05** (M06 receives `VO_APPROVED_COST_IMPACT` stub when M05 lands) |
| `RABillAuditLog` — append-only, every state transition. | LD calculation, contingency draw, risk buffer — **M05** |
| `GRN` — goods receipt note, populated by M04 `MATERIAL_GRN_EMITTED`. | EVM (CPI / SPI / EAC / ETC / VAC / TCPI) — **M07** (M06 supplies AC; M07 computes) |
| `VendorInvoice` — invoice receipt with GST + TDS captured (record-only per OQ-1.11=C). | Stage-gate decisions and SG-9 / SG-11 passage signals — **M08** |
| `InvoiceMatchResult` — 2/3-way PO ↔ GRN ↔ Invoice match outcome (per OQ-1.7=C). | DLP defect register and resolution — **M15 HandoverManagement** (signal stub until M15 lands) |
| `PaymentEvidence` — assembled evidence (PO, GRN, Invoice, Match) handed to external accounting system. | DLP compliance Non_Compliance observations — **M09 ComplianceTracker** (signal stub until M09 lands) |
| `PaymentEvidenceLedger` — append-only, every payment evidence state transition. | Bank file generation, signature workflow, payment release approval — external accounting system |
| `Retention` — tranched per Contract (Substantial_Completion + DLP_End per OQ-1.8=C); dual sign-off (FINANCE_LEAD + PMO_DIRECTOR). | BG identity, expiry tracking, claim workflow — **M23 BGInsuranceTracker** (Phase 2). M06 ships `BGStub`. |
| `CashflowForecast` — full-lifetime per-WBS-per-period (mirrors M03 PVProfile structure per OQ-1.5=A). | Tendering, vendor pre-qualification — **M29 / M30** (Phase 2) |
| `ForexRateMaster` (multi-currency v1.0 per OQ-1.6=B) — RBI_Reference + Bank_Transaction tiers. Append-only after 24-hour lock. | Tax reconciliation engine (GST input credit, TDS aggregation) — **future TaxLedger module** (Phase 2). M06 records GST + TDS on invoice only. |
| `ForexVariation` — period-end forex variation entries against POs in foreign currency. | Document storage internals — **M12 DocumentControl** (M06 stores `document_id` references; MinIO direct-URL stub until M12 lands per OQ-2.5) |
| `ForexRateLog` — append-only rate-entry history. | Accounting-system bidirectional sync (Tally / SAP / Zoho) — out of v1.0 (free-text stub on `M01.Project.accounting_system`) |
| `BGStub` — minimal BG record (number, bank, expiry, coverage, status) — migrates to M23 when Phase 2 lands per OQ-1.9=B. | Working-capital MILP optimisation — L1 Strategic (**M16 / M17 / M18 / M19**) |
| `M06FinancialConfig` — per-project tunables (cost-overrun thresholds, payment SLA, BG warning windows, retention split defaults, forex deviation gate). PMO_DIRECTOR-only edits with audit (per OQ-1.10=A). | Photo / drawing / FEMA-form storage internals — **M12** |
| Decision Queue triggers (capital headroom, payment SLA, forex deviation, BG expiry, retention release blocked, invoice match failed, BAC integrity warning, cashflow regen failed). | Schedule re-baselining triggered by VO — **M03** explicitly excludes (M06 inherits) |
| Audit-events catalogue locked from authoring (Appendix A — 43 events). | |
| Append-only ledgers with DB-level UPDATE/DELETE forbidden (4 ledgers per OQ-2.1). | |

---

## BLOCK 3 — DATA ARCHITECTURE

### 3a. Entities

| Entity | Description | Cardinality | Append-only? |
|---|---|---|---|
| `CostLedgerEntry` | The AC backbone — one immutable row per state-transition event in the 4-state pipeline. | Many per (project × package × period) | **Yes** (4-state-transition append-only model; row is final once written) |
| `PurchaseOrder` | Vendor commercial instrument. Identity + rate + currency + payment terms. Back-fills M03 ProcurementScheduleItem. | Many per package | No (mutable until status=Issued; immutable thereafter) |
| `RABill` | Contractor running-account bill at (Package × Period) grain. Dual trigger source. | 1 per (package × period × trigger_source) | No (mutable until status=Approved; immutable thereafter) |
| `RABillLine` | Per-WBS-per-period billing line within an RABill. | Many per RABill | No (mutable while parent RABill is) |
| `RABillAuditLog` | Append-only. Every RABill state transition. | Many per RABill | **Yes** |
| `GRN` | Goods Receipt Note. Created from M04 `MATERIAL_GRN_EMITTED`. | Many per PurchaseOrder | No (mutable while qc_decision=Pending; rare path) |
| `VendorInvoice` | Vendor invoice record. Captures GST rate, GST amount, TDS amount (per OQ-1.11=C). | Many per PurchaseOrder | No |
| `InvoiceMatchResult` | 2/3-way match outcome (PO ↔ GRN ↔ Invoice) per OQ-1.7=C. | 1 per VendorInvoice | No (immutable once Match_Status terminal) |
| `PaymentEvidence` | Bundle of PO + GRN + Invoice + Match + evidence URLs for external accounting handoff. | 1 per VendorInvoice (when match passes) | No |
| `PaymentEvidenceLedger` | Append-only. Evidence-bundle state transitions. | Many per PaymentEvidence | **Yes** |
| `Retention` | Tranched retention per Contract per RABill (dual sign-off per OQ-1.8=C). | Many per Contract | No |
| `CashflowForecast` | Per-WBS-per-period AC forecast for the full project lifetime. Mirrors M03 PVProfile (per OQ-1.5=A). | 1 per (WBS × period) | No (regenerated atomically per BR-06-040) |
| `ForexRateMaster` | RBI_Reference + Bank_Transaction tier rates per (currency × date). 24-hour edit window then locked. | Many per currency | No (mutable < 24hr; immutable thereafter — DB-level enforcement on lock window) |
| `ForexVariation` | Period-end variation against PO in foreign currency. | Many per (PO × period) | No |
| `ForexRateLog` | Append-only. Every rate entry + lock event. | Many per ForexRateMaster row | **Yes** |
| `BGStub` | Minimal BG record until M23 absorbs (per OQ-1.9=B). | Many per Contract | No |
| `M06FinancialConfig` | Per-project tunables (per OQ-1.10=A). PMO_DIRECTOR-edit only. Mirrors M04 ProjectExecutionConfig pattern. | 1 per project | No (audited via reserved fields + edit BR) |

**Append-only DB-level enforcement (per OQ-2.1 — 4 ledgers):**

```sql
-- For each append-only ledger:
REVOKE UPDATE, DELETE ON {ledger_table} FROM app_role;
GRANT INSERT, SELECT ON {ledger_table} TO app_role;
```

The four enforced ledgers are: `CostLedgerEntry`, `RABillAuditLog`, `PaymentEvidenceLedger`, `ForexRateLog`. Append-only entities have NO `updated_at`, NO `updated_by`, NO `is_active` (no soft-delete).

---

### 3b. Entity: `CostLedgerEntry` (APPEND-ONLY)

> Per Brief OQ-1.1 = A (LOCKED 2026-05-03): exactly 4 states (`Budgeted / Committed / Accrued / Paid`). Approval governance lives on parent entities (PurchaseOrder.status, RABill.status). Each state-transition writes ONE immutable ledger row.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `entry_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | — | LINK → M01.Project.project_id |
| `package_id` | UUID | Y | — | LINK → M02.Package.package_id |
| `wbs_id` | UUID | N | Optional drill — required for Accrued and Paid states (BR-06-001) | LINK → M02.WBSNode.wbs_id |
| `contract_id` | UUID | Y | The contract under which this rupee moves | LINK → M01.Contract.contract_id |
| `state` | ENUM | Y | `CostLedgerEntryState` (X8 v0.6 cascade — `Budgeted / Committed / Accrued / Paid`) | SYSTEM |
| `prior_state` | ENUM | N | Null only for initial Budgeted entry; required for all transitions (BR-06-002) | SYSTEM |
| `amount_inr` | DECIMAL(15,2) | Y | The rupee amount transitioning. Always INR (forex variation captured separately on ForexVariation). | CALC |
| `amount_foreign` | DECIMAL(15,2) | N | Foreign-currency amount if PO is multi-currency; null otherwise | INPUT (if multi-currency) |
| `currency_code` | VARCHAR(3) | Y | ISO 4217. `INR` for KDMC pilot. Foreign codes for medical-equipment imports per OQ-1.6=B. | LINK → X8 §3.13 Currency |
| `forex_rate_id` | UUID | N | Required if currency_code ≠ INR (BR-06-035) | LINK → ForexRateMaster |
| `period_start` | DATE | Y | Reporting period start (read from M03 LookAheadConfig.reporting_period_type via M03 internal API per OQ-2.4) | CALC |
| `period_end` | DATE | Y | Reporting period end | CALC |
| `source_entity_type` | VARCHAR(40) | Y | One of `M02.Package` (Budgeted), `M06.PurchaseOrder` (Committed), `M06.RABill` / `M06.GRN` (Accrued), `M06.PaymentEvidence` (Paid) | SYSTEM |
| `source_entity_id` | UUID | Y | FK to source row (polymorphic by source_entity_type) | LINK |
| `triggering_event` | VARCHAR(60) | Y | UPPER_SNAKE_CASE — e.g., `BILLING_TRIGGER_READY`, `MATERIAL_GRN_EMITTED`, `MILESTONE_ACHIEVED_FINANCIAL`, `PAYMENT_EVIDENCE_HANDED_OVER` | SYSTEM |
| `bac_integrity_warning_flag` | BOOLEAN | Y | Default false. Set true if M02.Package.bac_integrity_status = Stale_Pending_VO at the moment of write (per OQ-1.4=B — flag, do not block) | CALC |
| `pending_vo_id` | UUID | N | Snapshot of `M02.Package.pending_vo_id` if warning flag true | LINK → M05.VariationOrder (when M05 built) |
| `gst_amount_inr` | DECIMAL(15,2) | N | Captured for Committed (PO-side) and Accrued (RA-bill / GRN-side) entries | INPUT |
| `tds_amount_inr` | DECIMAL(15,2) | N | Captured for Paid entries (deducted-at-source) per OQ-1.11=C | INPUT |
| `created_by` | UUID | Y | Actor (user or system) | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `tenant_id, created_by, created_at` | reserved | Y | Standard append-only reserved subset | SYSTEM |

**No `updated_*` / `is_active`. DB-level UPDATE/DELETE forbidden.**

**Composite uniqueness:** (`tenant_id`, `project_id`, `source_entity_type`, `source_entity_id`, `state`) — exactly one row per (source, state) pair.

---

### 3c. Entity: `PurchaseOrder`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `po_id` | UUID | Y | Auto-generated | SYSTEM |
| `po_code` | VARCHAR(20) | Y | Auto. Format: `PO-{project_code}-{seq_pad5}`. Unique per project. | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | — | LINK → M01.Project.project_id |
| `package_id` | UUID | Y | — | LINK → M02.Package.package_id |
| `procurement_schedule_item_id` | UUID | N | FK → M03 ProcurementScheduleItem. Back-fills `m06_po_id` on PO issue (BR-06-005). | LINK → M03 |
| `contract_id` | UUID | Y | The contract under which the PO is raised | LINK → M01.Contract.contract_id |
| `vendor_party_id` | UUID | Y | Vendor identity from M01 Party master (party_type ∈ {Vendor, Specialist_Subcontractor}) | LINK → M01.Party.party_id |
| `po_value_basic` | DECIMAL(15,2) | Y | > 0. In `currency_code`. | INPUT |
| `currency_code` | VARCHAR(3) | Y | ISO 4217. Default INR. Non-INR allowed per OQ-1.6=B. | LINK → X8 §3.13 |
| `gst_rate` | DECIMAL(5,4) | Y | Default from M01.Contract.gst_rate. Range 0.00–0.28. | INPUT |
| `gst_amount` | DECIMAL(15,2) | Y | Auto = po_value_basic × gst_rate | CALC |
| `po_value_incl_gst` | DECIMAL(15,2) | Y | Auto = po_value_basic + gst_amount | CALC |
| `payment_terms_days` | INTEGER | Y | Default from M01.Contract.payment_credit_days | INPUT |
| `issue_date` | DATE | Y | ≤ today | INPUT |
| `expected_delivery_date` | DATE | N | Read from M03 ProcurementScheduleItem.planned_delivery_date if linked | LINK → M03 |
| `status` | ENUM | Y | `PurchaseOrderStatus` (X8 v0.6 cascade — `Draft / Issued / Partially_Received / Fully_Received / Closed / Cancelled`) | SYSTEM |
| `cancellation_reason` | TEXT | N | Min 100 chars if status=Cancelled (BR-06-008) | INPUT |
| `boq_item_refs` | JSONB | N | Array of M02 BOQItem IDs covered by this PO. Used for line-item invoice match (BR-06-018). | LINK → M02.BOQItem.boq_item_id |
| `document_id` | JSONB | N | Target — M12 references when M12 lands | LINK → M12 (when built) |
| `document_url` | JSONB | N | **STUB FIELD** — array of MinIO URLs. Migration cascade event drafted in Appendix C. | INPUT (stub period) |
| `tenant_id, created_by, created_at, updated_by, updated_at, is_active` | reserved | Y | Standard reserved fields (X8 §6) | SYSTEM |

---

### 3d. Entity: `RABill`

> Per Brief OQ-1.2 = B (LOCKED 2026-05-03): grain is per (Package × Period). Per Brief OQ-1.3 = B (LOCKED 2026-05-03): both progress-driven (M04 `BILLING_TRIGGER_READY`) AND milestone-driven (M03 `MILESTONE_ACHIEVED_FINANCIAL` for `MilestoneType=Financial`) trigger sources.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `ra_bill_id` | UUID | Y | Auto-generated | SYSTEM |
| `ra_bill_code` | VARCHAR(20) | Y | Auto. Format: `RAB-{project_code}-{seq_pad5}`. | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | — | LINK → M01.Project.project_id |
| `package_id` | UUID | Y | — | LINK → M02.Package.package_id |
| `contract_id` | UUID | Y | Contractor contract | LINK → M01.Contract.contract_id |
| `period_start` | DATE | Y | Period start (read from M03 LookAheadConfig.reporting_period_type via M03 API per OQ-2.4) | CALC |
| `period_end` | DATE | Y | Period end | CALC |
| `trigger_source` | ENUM | Y | `RABillTriggerSource` (X8 v0.6 cascade — `Progress / Milestone`) | SYSTEM |
| `triggering_milestone_id` | UUID | N | Required if trigger_source=Milestone (BR-06-014) | LINK → M03.Milestone.milestone_id |
| `gross_amount_inr` | DECIMAL(15,2) | Y | SUM(RABillLine.line_amount_inr) | CALC |
| `retention_amount_inr` | DECIMAL(15,2) | Y | CALC = gross_amount_inr × M01.Contract.retention_pct (BR-06-013) | CALC |
| `mobilisation_recovery_inr` | DECIMAL(15,2) | N | Auto-recovered against M01.Contract.mobilisation_advance_pct on early bills | CALC |
| `material_advance_recovery_inr` | DECIMAL(15,2) | N | Auto-recovered against M01.Contract.material_advance_pct | CALC |
| `gst_amount_inr` | DECIMAL(15,2) | Y | CALC = gross_amount_inr × M01.Contract.gst_rate | CALC |
| `tds_amount_inr` | DECIMAL(15,2) | N | TDS deducted at source (record-only per OQ-1.11=C) | INPUT |
| `net_payable_inr` | DECIMAL(15,2) | Y | CALC = gross_amount_inr − retention − mobilisation_recovery − material_advance_recovery + gst − tds | CALC |
| `status` | ENUM | Y | `RABillStatus` (X8 v0.6 cascade — `Draft / Submitted / Approved / Rejected / Paid`) | SYSTEM |
| `approved_by_qs` | UUID | N | QS_MANAGER required at Approved (BR-06-015) | LINK → M34.User |
| `approved_at_qs` | TIMESTAMP | N | Auto on QS approval | SYSTEM |
| `approved_by_finance` | UUID | N | FINANCE_LEAD required at Approved | LINK → M34.User |
| `approved_at_finance` | TIMESTAMP | N | Auto on Finance approval | SYSTEM |
| `rejection_reason` | TEXT | N | Min 50 chars if status=Rejected | INPUT |
| `compliance_hold_flag` | BOOLEAN | Y | Default false. Set true on M09 `COMPLIANCE_HOLD_BILLING` event (stub until M09 built) | LINK → M09 (when built) |
| `bac_integrity_warning_flag` | BOOLEAN | Y | Default false; set true at create if any source ProgressEntry's package is `Stale_Pending_VO` (per OQ-1.4=B — flag, don't block) | CALC |
| `document_id` | JSONB | N | M12 target | LINK → M12 (when built) |
| `document_url` | JSONB | N | STUB until M12 lands | INPUT |
| `tenant_id, created_by, created_at, updated_by, updated_at, is_active` | reserved | Y | Standard | SYSTEM |

**Composite uniqueness:** (`tenant_id`, `project_id`, `package_id`, `period_start`, `trigger_source`) — at most one progress-RABill and one milestone-RABill per package per period.

---

### 3e. Entity: `RABillLine`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `line_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `ra_bill_id` | UUID | Y | FK → RABill | LINK |
| `wbs_id` | UUID | Y | — | LINK → M02.WBSNode.wbs_id |
| `boq_item_id` | UUID | N | Optional; for itemised bills | LINK → M02.BOQItem.boq_item_id |
| `progress_entry_id` | UUID | N | Required if RABill.trigger_source=Progress (BR-06-012) | LINK → M04.ProgressEntry.entry_id |
| `triggering_milestone_id` | UUID | N | Required if RABill.trigger_source=Milestone | LINK → M03.Milestone.milestone_id |
| `quantity` | DECIMAL(15,4) | N | For itemised lines | INPUT |
| `unit_rate` | DECIMAL(15,2) | N | Snapshot from M02.BOQItem.actual_rate at create | LINK → M02 |
| `pct_complete_approved` | DECIMAL(5,4) | N | Snapshot from M04.ProgressEntry.pct_complete_approved at create | LINK → M04 |
| `line_amount_inr` | DECIMAL(15,2) | Y | CALC: progress-line = pct_complete_approved × M02.WBSNode bac slice; itemised-line = quantity × unit_rate; milestone-line = M01.Contract milestone tranche amount | CALC |
| `tenant_id, created_by, created_at, updated_by, updated_at, is_active` | reserved | Y | Standard | SYSTEM |

---

### 3f. Entity: `RABillAuditLog` (APPEND-ONLY)

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `audit_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | SYSTEM |
| `ra_bill_id` | UUID | Y | FK → RABill | LINK |
| `prior_status` | ENUM | N | Null on initial INSERT | SYSTEM |
| `new_status` | ENUM | Y | RABillStatus value after | SYSTEM |
| `event_type` | VARCHAR(60) | Y | UPPER_SNAKE_CASE — `RA_BILL_GENERATED / RA_BILL_SUBMITTED / RA_BILL_APPROVED_QS / RA_BILL_APPROVED_FINANCE / RA_BILL_REJECTED / RA_BILL_PAID` | SYSTEM |
| `actor_id` | UUID | Y | FK → M34 User | LINK |
| `actor_role` | VARCHAR(40) | Y | Snapshot at action time (UPPER_SNAKE_CASE) | SYSTEM |
| `transition_reason` | TEXT | N | Optional context; required on Rejected (carries rejection_reason) | INPUT |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `tenant_id, created_by` | reserved | Y | Standard | SYSTEM |

**No `updated_*` / `is_active`. DB-level UPDATE/DELETE forbidden.**

---

### 3g. Entity: `GRN`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `grn_id` | UUID | Y | Auto-generated | SYSTEM |
| `grn_code` | VARCHAR(20) | Y | Auto. Format: `GRN-{project_code}-{seq_pad5}`. | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | — | LINK → M01.Project.project_id |
| `package_id` | UUID | Y | — | LINK → M02.Package.package_id |
| `po_id` | UUID | Y | FK → PurchaseOrder | LINK |
| `m04_receipt_id` | UUID | Y | FK → M04.MaterialReceipt.receipt_id (the receipt that emitted MATERIAL_GRN_EMITTED) | LINK → M04 |
| `quantity_received` | DECIMAL(15,4) | Y | Mirrored from M04.MaterialReceipt.quantity_received | LINK → M04 |
| `unit_value_inr` | DECIMAL(15,2) | Y | Mirrored from M04.MaterialReceipt.unit_value_inr | LINK → M04 |
| `gross_amount_inr` | DECIMAL(15,2) | Y | CALC = quantity_received × M03.ProcurementScheduleItem.unit_rate (or PO line rate if itemised) | CALC |
| `qc_decision_at_emit` | ENUM | Y | Mirrored from `M04.MaterialReceipt.qc_decision` — X8 v0.5 §3.59 `MaterialQCDecision` ENUM (`Accepted` or `Conditional_Acceptance` only — `Rejected` does not emit GRN per M04 BR-04-029) | LINK → M04 (X8 §3.59) |
| `received_at` | TIMESTAMP | Y | Mirrored from M04.MaterialReceipt.received_at | LINK → M04 |
| `linked_to_invoice_id` | UUID | N | Set when linked to a VendorInvoice during 2/3-way match | LINK → VendorInvoice |
| `match_status` | ENUM | Y | `GRNMatchStatus` (X8 v0.6 cascade — `Unmatched / Linked / Matched / Disputed`) | SYSTEM |
| `tenant_id, created_by, created_at, updated_by, updated_at, is_active` | reserved | Y | Standard | SYSTEM |

---

### 3h. Entity: `VendorInvoice`

> Per Brief OQ-1.7 = C (LOCKED 2026-05-03): EPCC owns 2/3-way match. Per OQ-1.11 = C (LOCKED 2026-05-03): GST + TDS are recorded but NOT reconciled — reconciliation deferred to future TaxLedger module.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `invoice_id` | UUID | Y | Auto-generated | SYSTEM |
| `invoice_code` | VARCHAR(20) | Y | Auto-generated EPCC tracking code (different from vendor_invoice_number). Format: `INV-{project_code}-{seq_pad5}`. | SYSTEM |
| `vendor_invoice_number` | VARCHAR(100) | Y | The vendor's own invoice number (free-text from supplier). Unique within (project_id, vendor_party_id). | INPUT |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | — | LINK → M01.Project.project_id |
| `po_id` | UUID | Y | FK → PurchaseOrder | LINK |
| `vendor_party_id` | UUID | Y | Snapshot from PO (must match) | LINK → M01.Party.party_id |
| `invoice_date` | DATE | Y | ≤ today; ≥ PO.issue_date (BR-06-019) | INPUT |
| `received_date` | DATE | Y | ≤ today; ≥ invoice_date | INPUT |
| `gross_amount` | DECIMAL(15,2) | Y | Vendor's claimed gross amount in PO.currency_code | INPUT |
| `currency_code` | VARCHAR(3) | Y | Must equal PO.currency_code (BR-06-020) | LINK → X8 §3.13 |
| `gst_rate` | DECIMAL(5,4) | Y | As shown on the invoice; record-only per OQ-1.11=C | INPUT |
| `gst_amount` | DECIMAL(15,2) | Y | As shown on the invoice | INPUT |
| `tds_amount` | DECIMAL(15,2) | N | TDS deducted at source if shown | INPUT |
| `net_amount` | DECIMAL(15,2) | Y | gross_amount + gst_amount − tds_amount | CALC |
| `gross_amount_inr` | DECIMAL(15,2) | Y | If currency_code=INR: gross_amount; else CALC via ForexRateMaster (BR-06-035) | CALC |
| `status` | ENUM | Y | `VendorInvoiceStatus` (X8 v0.6 cascade — `Received / Match_Pending / Match_Passed / Match_Failed / Evidence_Assembled / Handed_Over / Cancelled`) | SYSTEM |
| `match_result_id` | UUID | N | FK → InvoiceMatchResult (set after match runs) | LINK |
| `payment_evidence_id` | UUID | N | FK → PaymentEvidence (set after evidence bundle assembled) | LINK |
| `compliance_hold_flag` | BOOLEAN | Y | Default false; set true on M09 COMPLIANCE_HOLD_BILLING (stub) | LINK → M09 (when built) |
| `document_id` | JSONB | N | M12 target | LINK → M12 (when built) |
| `document_url` | JSONB | N | STUB — invoice PDF | INPUT |
| `tenant_id, created_by, created_at, updated_by, updated_at, is_active` | reserved | Y | Standard | SYSTEM |

---

### 3i. Entity: `InvoiceMatchResult`

> Per Brief OQ-1.7 = C (LOCKED 2026-05-03): the 2/3-way match logic is M06's because M06 owns both PO terms and GRN context.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `match_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | — | LINK → M01.Project |
| `invoice_id` | UUID | Y | Unique (1:1 with VendorInvoice) | LINK → VendorInvoice |
| `po_id` | UUID | Y | Snapshot from VendorInvoice.po_id | LINK → PurchaseOrder |
| `grn_ids` | JSONB | N | Array of GRN IDs participating in match. Empty for 2-way match (PO-only when PO is for services-without-receipt). | LINK → GRN |
| `match_mode` | ENUM | Y | `InvoiceMatchMode` (X8 v0.6 cascade — `Two_Way / Three_Way`) | SYSTEM |
| `qty_variance_pct` | DECIMAL(5,4) | N | (invoice.gross_amount − sum(GRN.gross_amount_inr)) / PO.po_value_basic. Range tolerable per M06FinancialConfig.invoice_match_qty_tolerance_pct (default 0.02 = 2%) | CALC |
| `rate_variance_pct` | DECIMAL(5,4) | N | abs((invoice.unit_rate_avg − PO.unit_rate_avg) / PO.unit_rate_avg). Tolerance per M06FinancialConfig.invoice_match_rate_tolerance_pct (default 0.005 = 0.5%) | CALC |
| `match_status` | ENUM | Y | `InvoiceMatchStatus` (X8 v0.6 cascade — `Three_Way_Pass / Three_Way_Fail_Quantity / Three_Way_Fail_Rate / Two_Way_Pass / Pending / Override_Approved`) | SYSTEM |
| `failure_details` | JSONB | N | Diagnostic payload — line-by-line variance, expected vs received | CALC |
| `pmo_override_applied` | BOOLEAN | Y | Default false; PMO_DIRECTOR may override a Failed match with justification ≥ 200 chars (BR-06-022) | INPUT |
| `pmo_override_justification` | TEXT | N | Min 200 chars if pmo_override_applied=true | INPUT |
| `pmo_override_by` | UUID | N | FK → PMO_DIRECTOR user | LINK |
| `pmo_override_at` | TIMESTAMP | N | Auto | SYSTEM |
| `tenant_id, created_by, created_at, updated_by, updated_at, is_active` | reserved | Y | Standard | SYSTEM |

---

### 3j. Entity: `PaymentEvidence`

> Per Brief OQ-1.7 = C (LOCKED 2026-05-03): EPCC assembles evidence; external accounting system executes payment. M06 NEVER stores bank account numbers, signature workflow, or initiates the actual transfer.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `evidence_id` | UUID | Y | Auto-generated | SYSTEM |
| `evidence_code` | VARCHAR(20) | Y | Auto. Format: `PEV-{project_code}-{seq_pad5}`. | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | — | LINK → M01.Project |
| `invoice_id` | UUID | Y | Unique (1:1 with VendorInvoice) | LINK → VendorInvoice |
| `po_id` | UUID | Y | Snapshot from invoice | LINK |
| `match_result_id` | UUID | Y | Match must be `Three_Way_Pass`, `Two_Way_Pass`, or `Override_Approved` (BR-06-024) | LINK → InvoiceMatchResult |
| `evidence_payload` | JSONB | Y | Bundle: PO snapshot, GRN snapshots, invoice snapshot, match outcome, document URLs/IDs | CALC |
| `gross_payable_inr` | DECIMAL(15,2) | Y | net_amount converted to INR | CALC |
| `status` | ENUM | Y | `PaymentEvidenceStatus` (X8 v0.6 cascade — `Assembled / Handed_Over / Confirmed_Paid / Cancelled`) | SYSTEM |
| `assembled_by` | UUID | Y | FINANCE_LEAD | LINK → M34.User |
| `assembled_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `handed_over_at` | TIMESTAMP | N | When evidence pushed to external accounting | SYSTEM |
| `bank_debit_advice_doc_id` | JSONB | N | M12 ref — bank debit advice from external accounting | LINK → M12 |
| `bank_debit_advice_url` | JSONB | N | STUB MinIO URL | INPUT |
| `confirmed_paid_at` | TIMESTAMP | N | When FINANCE_LEAD flips state to Confirmed_Paid (manual per OQ-1.7=C) | INPUT |
| `confirmed_paid_by` | UUID | N | FINANCE_LEAD | LINK → M34.User |
| `tenant_id, created_by, created_at, updated_by, updated_at, is_active` | reserved | Y | Standard | SYSTEM |

---

### 3k. Entity: `PaymentEvidenceLedger` (APPEND-ONLY)

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `ledger_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | SYSTEM |
| `evidence_id` | UUID | Y | FK → PaymentEvidence | LINK |
| `prior_status` | ENUM | N | PaymentEvidenceStatus or null on INSERT | SYSTEM |
| `new_status` | ENUM | Y | PaymentEvidenceStatus | SYSTEM |
| `event_type` | VARCHAR(60) | Y | UPPER_SNAKE_CASE — `EVIDENCE_ASSEMBLED / EVIDENCE_HANDED_OVER / PAYMENT_CONFIRMED / EVIDENCE_CANCELLED` | SYSTEM |
| `actor_id` | UUID | Y | FK → M34.User | LINK |
| `actor_role` | VARCHAR(40) | Y | Snapshot | SYSTEM |
| `transition_reason` | TEXT | N | Optional context | INPUT |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `tenant_id, created_by` | reserved | Y | Standard | SYSTEM |

**No `updated_*` / `is_active`. DB-level UPDATE/DELETE forbidden.**

---

### 3l. Entity: `Retention`

> Per Brief OQ-1.8 = C (LOCKED 2026-05-03): tranched release with dual sign-off (FINANCE_LEAD + PMO_DIRECTOR). Default split per M01.Contract.dlp_retention_split_pct (M01 v1.3 cascade — see "Cascade Implications" section). Default 0.50 = 50% on Substantial Completion (M08 SG-9 evidence) + 50% on DLP End (M15 + M09 zero-counts).

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `retention_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | — | LINK → M01.Project |
| `contract_id` | UUID | Y | — | LINK → M01.Contract |
| `ra_bill_id` | UUID | Y | The RABill that withheld this retention amount | LINK → RABill |
| `withheld_amount_inr` | DECIMAL(15,2) | Y | Mirrored from RABill.retention_amount_inr | LINK |
| `release_type` | ENUM | N | `RetentionReleaseType` (X8 v0.6 cascade — `Substantial_Completion / DLP_End / PMO_Override`). Set on release. | INPUT |
| `release_tranche_pct` | DECIMAL(5,4) | N | The tranche % released in this event (e.g., 0.50). Sum of release_tranche_pct over all released rows for a (contract, ra_bill) pair must equal 1.0 when fully released. | CALC |
| `released_amount_inr` | DECIMAL(15,2) | N | CALC = withheld_amount_inr × release_tranche_pct | CALC |
| `release_status` | ENUM | Y | `RetentionReleaseStatus` (X8 v0.6 cascade — `Withheld / Eligible / Approved_Finance / Released / Blocked / Cancelled`) | SYSTEM |
| `eligible_at` | TIMESTAMP | N | Set when pre-conditions met (BR-06-027 / BR-06-028) | SYSTEM |
| `eligibility_basis` | JSONB | N | Snapshot of pre-conditions met: `{sg9_passed, m15_open_defects, m09_open_noncompliance}`. Populated at eligibility flip. | CALC |
| `approved_by_finance` | UUID | N | FINANCE_LEAD signature on tranche release (BR-06-029) | LINK → M34.User |
| `approved_at_finance` | TIMESTAMP | N | Auto | SYSTEM |
| `approved_by_pmo` | UUID | N | PMO_DIRECTOR signature (dual sign-off per OQ-1.8=C) | LINK → M34.User |
| `approved_at_pmo` | TIMESTAMP | N | Auto | SYSTEM |
| `released_at` | TIMESTAMP | N | Set on Released transition (final state) | SYSTEM |
| `pmo_override_applied` | BOOLEAN | Y | Default false. Set true if PMO bypasses normal pre-conditions (BR-06-030) | INPUT |
| `pmo_override_justification` | TEXT | N | Min 200 chars if pmo_override_applied=true | INPUT |
| `block_reason` | TEXT | N | Min 100 chars if release_status=Blocked (e.g., M15 open defects, M09 open non-compliance) | INPUT |
| `bg_stub_id` | UUID | N | If release is conditional on BG replacement, FK to BGStub used as substitute | LINK → BGStub |
| `tenant_id, created_by, created_at, updated_by, updated_at, is_active` | reserved | Y | Standard | SYSTEM |

---

### 3m. Entity: `CashflowForecast`

> Per Brief OQ-1.5 = A (LOCKED 2026-05-03): full-lifetime per-WBS-per-period grain. Mirrors M03 PVProfile structure for direct EVM consumption symmetry by M07.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `forecast_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | — | LINK → M01.Project |
| `wbs_id` | UUID | Y | — | LINK → M02.WBSNode.wbs_id |
| `package_id` | UUID | Y | — | LINK → M02.Package.package_id |
| `period_start_date` | DATE | Y | Aligned to M03 LookAheadConfig.reporting_period_type (read via M03 internal API) | SYSTEM |
| `period_end_date` | DATE | Y | period_start_date + period_length | SYSTEM |
| `forecast_committed_inr` | DECIMAL(15,2) | Y | Forecast Committed AC for this (WBS × period) — driven by PO schedule + M03 ProcurementScheduleItem.planned_delivery_date | CALC |
| `forecast_accrued_inr` | DECIMAL(15,2) | Y | Forecast Accrued AC — driven by M03 PVProfile.cumulative_pv_amount × adjustment factor for actual progress trend | CALC |
| `forecast_paid_inr` | DECIMAL(15,2) | Y | Forecast Paid AC — Accrued shifted forward by M01.Contract.payment_credit_days | CALC |
| `actual_committed_inr` | DECIMAL(15,2) | N | Actual to-date Committed (sum CostLedgerEntry where state=Committed AND period_start ≤ period_start_date) | CALC |
| `actual_accrued_inr` | DECIMAL(15,2) | N | Actual to-date Accrued | CALC |
| `actual_paid_inr` | DECIMAL(15,2) | N | Actual to-date Paid | CALC |
| `last_regenerated_at` | TIMESTAMP | Y | Set on every regen | SYSTEM |
| `last_regen_job_id` | UUID | Y | FK → cashflow regen job (audit trail) | LINK |
| `tenant_id, created_by, created_at, updated_by, updated_at, is_active` | reserved | Y | Standard | SYSTEM |

**Composite uniqueness:** (`tenant_id`, `project_id`, `wbs_id`, `period_start_date`).

---

### 3n. Entity: `ForexRateMaster`

> Per Brief OQ-1.6 = B (LOCKED 2026-05-03): multi-currency shipped from v1.0. Two tiers: `RBI_Reference` (system-published RBI rate per currency per date — daily seed) and `Bank_Transaction` (actual conversion rate at PO / invoice / payment time, with FEMA Form A2 evidence requirement above threshold). Append-only at DB level after the 24-hour lock window (BR-06-033).

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `rate_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `currency_code` | VARCHAR(3) | Y | ISO 4217 (e.g., `USD`, `EUR`, `GBP`, `JPY`) | LINK → X8 §3.13 |
| `rate_date` | DATE | Y | Effective date | INPUT |
| `rate_tier` | ENUM | Y | `ExchangeRateTier` (X8 v0.6 cascade — `RBI_Reference / Bank_Transaction`) | INPUT |
| `rate_to_inr` | DECIMAL(12,6) | Y | INR per 1 unit foreign currency. > 0. | INPUT |
| `source_reference` | TEXT | N | URL or document for RBI_Reference; Bank advice number for Bank_Transaction | INPUT |
| `is_locked` | BOOLEAN | Y | Default false; auto-set true 24 hours after created_at (BR-06-033) | SYSTEM |
| `locked_at` | TIMESTAMP | N | Auto | SYSTEM |
| `pmo_approval_required` | BOOLEAN | Y | CALC = (rate_tier=Bank_Transaction AND deviation from RBI_Reference > M06FinancialConfig.forex_deviation_pct (default 0.05)) per BR-06-034 | CALC |
| `pmo_approved_by` | UUID | N | PMO_DIRECTOR if pmo_approval_required=true (BR-06-034) | LINK → M34.User |
| `pmo_approved_at` | TIMESTAMP | N | Auto | SYSTEM |
| `fema_form_a2_doc_id` | JSONB | N | M12 ref — required if rate_tier=Bank_Transaction AND amount > M06FinancialConfig.fema_form_a2_threshold_usd | LINK → M12 |
| `fema_form_a2_url` | JSONB | N | STUB MinIO URL | INPUT |
| `tenant_id, created_by, created_at, updated_by, updated_at, is_active` | reserved | Y | Standard | SYSTEM |

**Note:** While the entity has reserved `updated_*` fields, BR-06-033 enforces that no UPDATE may change `rate_to_inr` after `is_locked=true`. The append-only enforcement applies to `ForexRateLog` (the change-history record), not directly to ForexRateMaster — but functionally the master row becomes immutable after the 24-hour lock.

---

### 3o. Entity: `ForexVariation`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `variation_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | — | LINK → M01.Project |
| `po_id` | UUID | Y | The PO whose foreign-currency exposure is being measured | LINK → PurchaseOrder |
| `period_start` | DATE | Y | Reporting period | SYSTEM |
| `period_end` | DATE | Y | Reporting period | SYSTEM |
| `currency_code` | VARCHAR(3) | Y | PO.currency_code | LINK |
| `committed_amount_foreign` | DECIMAL(15,2) | Y | Sum of foreign-currency amount committed in period | CALC |
| `forex_rate_at_commit_id` | UUID | Y | FK → ForexRateMaster row used at commit time | LINK |
| `forex_rate_at_period_end_id` | UUID | Y | FK → ForexRateMaster row at period end (RBI_Reference tier) | LINK |
| `variation_inr` | DECIMAL(15,2) | Y | CALC = committed_amount_foreign × (rate_at_period_end − rate_at_commit). Positive = unfavourable; negative = favourable. | CALC |
| `tenant_id, created_by, created_at, updated_by, updated_at, is_active` | reserved | Y | Standard | SYSTEM |

---

### 3p. Entity: `ForexRateLog` (APPEND-ONLY)

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `log_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `rate_id` | UUID | Y | FK → ForexRateMaster | LINK |
| `event_type` | VARCHAR(60) | Y | UPPER_SNAKE_CASE — `FOREX_RATE_ENTERED / FOREX_RATE_LOCKED / FOREX_RATE_PMO_APPROVED / FOREX_DEVIATION_REVIEW` | SYSTEM |
| `prior_rate` | DECIMAL(12,6) | N | Pre-edit rate (only meaningful while is_locked=false) | SYSTEM |
| `new_rate` | DECIMAL(12,6) | Y | Rate after event | SYSTEM |
| `actor_id` | UUID | Y | FK → M34.User or `SYSTEM` for daily RBI seed | LINK |
| `actor_role` | VARCHAR(40) | Y | Snapshot | SYSTEM |
| `change_reason` | TEXT | N | Optional context; required ≥ 100 chars on PMO override | INPUT |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `tenant_id, created_by` | reserved | Y | Standard | SYSTEM |

**No `updated_*` / `is_active`. DB-level UPDATE/DELETE forbidden.**

---

### 3q. Entity: `BGStub`

> Per Brief OQ-1.9 = B (LOCKED 2026-05-03): minimal BG record until M23 BGInsuranceTracker absorbs in Phase 2. Mirrors M04→M12 photo-stub pattern. Migration cascade event drafted in Appendix C.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `bg_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | — | LINK → M01.Project |
| `contract_id` | UUID | Y | — | LINK → M01.Contract |
| `bg_number` | VARCHAR(60) | Y | Bank-issued BG reference number; unique within (tenant_id, contract_id) | INPUT |
| `issuing_bank` | VARCHAR(200) | Y | — | INPUT |
| `bg_type` | ENUM | Y | `BGType` (X8 v0.6 cascade — `Performance / Advance_Payment / Retention_Substitute / Bid / Other`) | INPUT |
| `coverage_amount_inr` | DECIMAL(15,2) | Y | > 0 | INPUT |
| `issue_date` | DATE | Y | ≤ today | INPUT |
| `expiry_date` | DATE | Y | > issue_date | INPUT |
| `claim_period_end_date` | DATE | N | Date until which a claim can be made (typically expiry + 30/60/90 days) | INPUT |
| `is_active` | BOOLEAN | Y | Default true; auto-flip to false on expiry_date < today (BR-06-031) | SYSTEM |
| `expiry_warning_emitted_90d` | BOOLEAN | Y | Default false. Set true after 90-day warning fires (BR-06-032) | SYSTEM |
| `expiry_warning_emitted_30d` | BOOLEAN | Y | Default false. | SYSTEM |
| `expiry_warning_emitted_7d` | BOOLEAN | Y | Default false. | SYSTEM |
| `migrated_to_m23_at` | TIMESTAMP | N | Set when M23 absorbs this stub via Appendix C migration | SYSTEM |
| `m23_bg_id` | UUID | N | FK to M23 BG record after migration | LINK → M23 (when built) |
| `document_id` | JSONB | N | M12 target — BG certificate scan | LINK → M12 |
| `document_url` | JSONB | N | STUB MinIO URL | INPUT |
| `tenant_id, created_by, created_at, updated_by, updated_at` | reserved | Y | Standard (note: `is_active` overridden by BR-06-031 expiry logic but otherwise reserved) | SYSTEM |

---

### 3r. Entity: `M06FinancialConfig`

> Per Brief OQ-1.10 = A (LOCKED 2026-05-03): per-project tunables, mirrors M04 ProjectExecutionConfig. PMO_DIRECTOR-only edits with audit (BR-06-046). Auto-seeded at M01 Project transition to Active.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `config_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | Unique (1:1 with Project) | LINK → M01.Project |
| `capital_headroom_amber_pct` | DECIMAL(5,4) | Y | Default 0.9500 (95% of BAC). When Committed/BAC ≥ this, Decision Queue trigger AMBER. | INPUT |
| `capital_headroom_red_pct` | DECIMAL(5,4) | Y | Default 1.0000 (100%). When Committed/BAC ≥ this, RED. Per X9 §9.5.1 thresholds. | INPUT |
| `cost_overrun_warn_pct` | DECIMAL(5,4) | Y | Default 1.0500 (Accrued/BAC > 105% per package = warn) | INPUT |
| `cost_overrun_red_pct` | DECIMAL(5,4) | Y | Default 1.1500 (115% = red) | INPUT |
| `payment_sla_warn_days` | INTEGER | Y | Default = M01.Contract.payment_credit_days + 5 (per project; computed at seed). Floor 7. | INPUT |
| `payment_sla_red_days` | INTEGER | Y | Default = M01.Contract.payment_credit_days + 15 | INPUT |
| `forex_deviation_pct` | DECIMAL(5,4) | Y | Default 0.0500 (5%) — gates PMO approval per BR-06-034 (legacy v2.1 number) | INPUT |
| `fema_form_a2_threshold_usd` | DECIMAL(15,2) | Y | Default 25000.00 (per FEMA Form A2 statutory threshold) | INPUT |
| `bg_warning_days_90` | INTEGER | Y | Default 90 | INPUT |
| `bg_warning_days_30` | INTEGER | Y | Default 30 | INPUT |
| `bg_warning_days_7` | INTEGER | Y | Default 7 | INPUT |
| `retention_release_stale_days` | INTEGER | Y | Default 30 (days after `eligible_at` without release → Decision Queue) | INPUT |
| `retention_minor_release_pct_default` | DECIMAL(5,4) | Y | Default 0.5000 — used at Project create to seed M01.Contract.dlp_retention_split_pct (M01 v1.3 cascade) | INPUT |
| `invoice_match_qty_tolerance_pct` | DECIMAL(5,4) | Y | Default 0.0200 (2%) | INPUT |
| `invoice_match_rate_tolerance_pct` | DECIMAL(5,4) | Y | Default 0.0050 (0.5%) | INPUT |
| `cashflow_regen_max_runtime_seconds` | INTEGER | Y | Default 300 (5 min). Decision Queue trigger if exceeded (BR-06-040) | INPUT |
| `last_edited_by` | UUID | N | FK → PMO_DIRECTOR | LINK |
| `last_edit_justification` | TEXT | N | Min 100 chars on every edit (BR-06-046) | INPUT |
| `tenant_id, created_by, created_at, updated_by, updated_at, is_active` | reserved | Y | Standard | SYSTEM |

---

## BLOCK 4 — DATA POPULATION RULES

| Rule | Trigger | Action |
|---|---|---|
| Auto-create `M06FinancialConfig` | M01.Project transitions to Active (M01 BR-01-007) | Insert M06FinancialConfig row with all defaults; emit `M06_CONFIG_CREATED` audit |
| Seed initial `Budgeted` CostLedgerEntry | M02.Package created OR `M02_BAC_RECONCILED` event | Write CostLedgerEntry(state=Budgeted, amount_inr=Package.bac_amount, source_entity=M02.Package) |
| Auto-generate `po_code` | PurchaseOrder INSERT | Format: `PO-{project.project_code}-{seq_pad5}` |
| Auto-generate `ra_bill_code` | RABill INSERT | Format: `RAB-{project.project_code}-{seq_pad5}` |
| Auto-generate `grn_code` | GRN INSERT | Format: `GRN-{project.project_code}-{seq_pad5}` |
| Auto-generate `invoice_code` | VendorInvoice INSERT | Format: `INV-{project.project_code}-{seq_pad5}` |
| Auto-generate `evidence_code` | PaymentEvidence INSERT | Format: `PEV-{project.project_code}-{seq_pad5}` |
| Back-fill M03 ProcurementScheduleItem.m06_po_id | PurchaseOrder transitions to Issued | Call M03 internal API (BR-06-005); emit `PROCUREMENT_ORDER_PLACED` (M03 audit type) |
| Derive `period_start` / `period_end` | Any entity needing reporting period (CostLedgerEntry, RABill, CashflowForecast) | Read M03 LookAheadConfig.reporting_period_type via M03 internal API per OQ-2.4; cache for the duration of the regen / write job |
| Buffer Approved progress entries for period close | M04 BILLING_TRIGGER_READY received | Insert pending RA bill candidate row keyed on (package_id, period); generate RABill on period close |
| Generate progress-RABill | Period close cron OR explicit user trigger | For each (package_id, period) with buffered progress entries: assemble RABillLines; create RABill(trigger_source=Progress); emit `RA_BILL_GENERATED` |
| Generate milestone-RABill | M03 MILESTONE_ACHIEVED_FINANCIAL received (per OQ-1.3=B) | Create RABill(trigger_source=Milestone, triggering_milestone_id=...); compute amount from M01.Contract milestone-tranche schedule; emit `RA_BILL_GENERATED` |
| Persist GRN | M04 MATERIAL_GRN_EMITTED received | Create GRN row; persist linkage to PO (via package_id + procurement_schedule_item_id resolution); emit `GRN_RECEIVED` |
| Compute `bac_integrity_warning_flag` | CostLedgerEntry INSERT or RABill INSERT | Snapshot M02.Package.bac_integrity_status via internal API; flag if Stale_Pending_VO; persist `pending_vo_id` snapshot |
| Auto-flip BGStub.is_active | Daily sweep | Set is_active=false where expiry_date < today; emit `BG_STATUS_UPDATED` |
| Daily RBI rate seed | Daily 06:00 IST cron | Fetch RBI reference rates for active currencies; INSERT ForexRateMaster rows (rate_tier=RBI_Reference); emit `FOREX_RATE_ENTERED` per row |
| ForexRateMaster lock | Hourly sweep | For rows where created_at + 24h < now AND is_locked=false: set is_locked=true; emit `FOREX_RATE_LOCKED` |
| Photo migration to M12 | M12 v1.0 lock | One-shot script `20260XXX_M12_absorb_M06_document_urls.py` (Appendix C); emit `DOCUMENT_MIGRATED_TO_M12` per row; deprecate `document_url` JSONB |
| BG migration to M23 | M23 v1.0 lock | One-shot script `20260XXX_M23_absorb_M06_BGStub.py` (Appendix C); emit `BG_MIGRATED_TO_M23` per row |

---

## BLOCK 5 — FILTERS AND VIEWS

### Common filters across views

- `project_id` (mandatory — RBAC scope per M34)
- `package_id` / `wbs_id` (drill)
- `period_start` / `period_end` (date range)
- `state` (CostLedgerEntry only — Budgeted / Committed / Accrued / Paid)
- `status` (entity-specific: PurchaseOrderStatus / RABillStatus / VendorInvoiceStatus / PaymentEvidenceStatus / RetentionReleaseStatus)
- `vendor_party_id` (PO / GRN / VendorInvoice filtering)
- `currency_code` (multi-currency views)
- `match_status` (InvoiceMatchResult)

### Role-default views (per Brief Section 7 + X9 v0.3 §13.3.6 LOCKED)

| Role | Primary view | Secondary widgets | Hidden |
|---|---|---|---|
| `FINANCE_LEAD` | **Capital Funnel** ⭐ (X9 §9.5.1 — flagship pipeline pattern instance) | Cashflow time-series; payment aging (0-30/31-60/61-90/90+); vendor outstanding bar; pending RA bills queue; pending retention releases | — |
| `PMO_DIRECTOR` | Capital Funnel (read primary) | Margin by package (BAC vs Accrued vs Paid); variance bar; M06FinancialConfig editor; pending dual-sign-off retention queue | — |
| `PROJECT_DIRECTOR` | Capital Funnel (own project) | Recent payments, RA bills due this period, cashflow vs PV S-curve overlay | Cross-project |
| `PROCUREMENT_OFFICER` | Vendor outstanding bar + PO status pipeline | Procurement spend trend; long-lead PO tracking (link → M03); 2/3-way match queue | Internal margins |
| `SITE_MANAGER` | Capital Funnel (% only — ₹ values redacted per X9 §6 / cross-cutting role mapping) | — | All ₹ values |
| `QS_MANAGER` | RA bill queue (own packages) — pending QS approval | Variance analysis: declared progress vs RABill amount | Cross-project |
| `EXTERNAL_AUDITOR` | Append-only ledger viewer (read-only across all 4 ledgers) | Forex rate log, BG expiry calendar, retention release log | — |
| `READ_ONLY` | Capital Funnel (% only, status badges) | — | All ₹ values, all action surfaces |

⭐ = Primary view. **NCR pipeline funnel from M04 was 8th instance; M06 Capital Funnel is the 1st named instance and the flagship per X9 §9.5.1.**

### Mandatory-input fields per entity (M03 / M04 pattern)

| Field | Required at | Block save if blank? |
|---|---|---|
| `cancellation_reason` | PO status=Cancelled | Y (BR-06-008, ≥100 chars) |
| `rejection_reason` | RABill status=Rejected | Y (≥50 chars) |
| `pmo_override_justification` | InvoiceMatchResult.pmo_override_applied=true | Y (BR-06-022, ≥200 chars) |
| `pmo_override_justification` | Retention.pmo_override_applied=true | Y (BR-06-030, ≥200 chars) |
| `block_reason` | Retention.release_status=Blocked | Y (≥100 chars) |
| `last_edit_justification` | M06FinancialConfig edit | Y (BR-06-046, ≥100 chars) |
| `change_reason` (ForexRateLog) | PMO override of forex rate | Y (≥100 chars) |
| `qc_notes` (mirrored from M04 GRN) | GRN qc_decision=Conditional_Acceptance | Y (mirrored from M04 BR-04-030) |

---

## BLOCK 6 — BUSINESS RULES

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---|---|---|---|---|
| BR-06-001 | CostLedgerEntry INSERT | If state ∈ {Accrued, Paid} → wbs_id required | Block insert if wbs_id null | T1 |
| BR-06-002 | CostLedgerEntry INSERT | Validate state-transition: Budgeted has prior_state=null; Committed has prior_state=Budgeted; Accrued has prior_state=Committed; Paid has prior_state=Accrued | Block insert on illegal transition | T1 |
| BR-06-003 | CostLedgerEntry INSERT | Snapshot M02.Package.bac_integrity_status via M02 internal API at write time. If Stale_Pending_VO → set bac_integrity_warning_flag=true AND pending_vo_id; **DO NOT block** (per Brief OQ-1.4=B) | Persist with flag; emit `BAC_INTEGRITY_WARNING_FLAGGED` | T1 |
| BR-06-004 | CostLedgerEntry sum check | For any (project, package), assert SUM(state=Committed) ≤ SUM(state=Budgeted) only when capital_headroom_red_pct < 1.0 (some configs allow over-commit). When over, generate Decision Queue: `CAPITAL_HEADROOM_BREACH` severity=Critical. | Decision created | T2 (sweep on every Committed write) |
| BR-06-005 | PurchaseOrder transitions to Issued | If procurement_schedule_item_id present: call M03 internal API to back-fill `m06_po_id` AND `actual_order_date=issue_date` | M03 receives; M03 BR-03-022 fires | T1 |
| BR-06-006 | PurchaseOrder INSERT | If currency_code ≠ INR → require ForexRateMaster row for currency_code on or before issue_date | Block insert if no rate available; emit `FOREX_RATE_NOT_AVAILABLE` Decision (severity=High) | T1 |
| BR-06-007 | PurchaseOrder transitions to Issued | Write CostLedgerEntry(state=Committed, amount_inr=po_value_basic in INR (via forex if foreign), source=PurchaseOrder, triggering_event=`PO_ISSUED`) | CostLedgerEntry persisted; capital funnel updates | T1 |
| BR-06-008 | PurchaseOrder transitions to Cancelled | cancellation_reason ≥ 100 chars; if PO already had Committed CostLedgerEntry, write reversing CostLedgerEntry(state=Budgeted, amount_inr= -committed_amount, triggering_event=`PO_CANCELLED`). Use the same source_entity_id (composite uniqueness allows this because state=Budgeted differs from state=Committed for the same PO — see compound key). | CostLedgerEntry reversal; emit `PURCHASE_ORDER_CANCELLED` | T1 |
| BR-06-009 | RABill auto-generation (period close) — trigger_source=Progress | For each (package_id, period) with one or more Approved M04 ProgressEntries received via BILLING_TRIGGER_READY: assemble RABillLines (one per ProgressEntry); compute gross_amount_inr, retention_amount_inr, GST, recoveries; create RABill(status=Draft, trigger_source=Progress); emit `RA_BILL_GENERATED` | RABill row + RABillLines + audit | T2 (period close cron) |
| BR-06-010 | RABill auto-generation — trigger_source=Milestone (per OQ-1.3=B) | On M03 MILESTONE_ACHIEVED_FINANCIAL event: lookup M01.Contract milestone-tranche schedule (from `payment_terms` JSONB or contract attachment); compute milestone tranche amount; create RABill(status=Draft, trigger_source=Milestone, triggering_milestone_id=...); emit `RA_BILL_GENERATED` | RABill row | T1 |
| BR-06-011 | RABill INSERT | If any source ProgressEntry's package has bac_integrity_status=Stale_Pending_VO → set RABill.bac_integrity_warning_flag=true (per OQ-1.4=B). Continue. | Persist with flag | T1 |
| BR-06-012 | RABillLine INSERT where parent.trigger_source=Progress | progress_entry_id required AND must reference an Approved M04 ProgressEntry | Block insert otherwise | T1 |
| BR-06-013 | RABill compute | retention_amount_inr = gross_amount_inr × M01.Contract.retention_pct; mobilisation_recovery_inr per M01.Contract.mobilisation_advance_pct schedule; material_advance_recovery_inr per M01.Contract.material_advance_pct | Persist | T1 |
| BR-06-014 | RABill INSERT where trigger_source=Milestone | triggering_milestone_id required AND M03.Milestone.milestone_type=Financial AND M03.Milestone.status=Achieved | Block insert otherwise | T1 |
| BR-06-015 | RABill transition Draft → Submitted → Approved | Submitted requires SITE_MANAGER or QS_MANAGER. Approved requires BOTH approved_by_qs (QS_MANAGER) AND approved_by_finance (FINANCE_LEAD); compliance_hold_flag must be false (else block with reason `COMPLIANCE_HOLD_BILLING_ACTIVE`) | Persist; emit `RA_BILL_APPROVED_QS` then `RA_BILL_APPROVED_FINANCE`; on final Approved, write CostLedgerEntry(state=Accrued, source=RABill) | T1 |
| BR-06-016 | RABill Approved | Withhold retention: create Retention(release_status=Withheld, withheld_amount_inr=RABill.retention_amount_inr, ra_bill_id=...) | Retention persisted; emit `RETENTION_WITHHELD` | T1 |
| BR-06-017 | M04 MATERIAL_GRN_EMITTED received | Create GRN row; if PO is found via package_id + procurement_schedule_item_id → write CostLedgerEntry(state=Accrued, amount_inr=GRN.gross_amount_inr, source=GRN, triggering_event=`MATERIAL_GRN_EMITTED`); else queue for manual PO linkage | GRN persisted; CostLedgerEntry written | T1 |
| BR-06-018 | InvoiceMatchResult compute | For Three_Way mode: validate (a) sum(GRN.gross_amount_inr) − invoice.gross_amount_inr | / PO.po_value_basic ≤ M06FinancialConfig.invoice_match_qty_tolerance_pct AND (b) abs((invoice.unit_rate_avg − PO.unit_rate_avg) / PO.unit_rate_avg) ≤ invoice_match_rate_tolerance_pct. Set match_status accordingly. | Persist match outcome; if pass → emit `INVOICE_MATCH_PASSED`; if fail → emit `INVOICE_MATCH_FAILED` AND Decision Queue trigger | T1 |
| BR-06-019 | VendorInvoice INSERT | invoice_date ≥ PO.issue_date; received_date ≥ invoice_date; received_date ≤ today | Block insert otherwise | T1 |
| BR-06-020 | VendorInvoice INSERT | currency_code must equal PO.currency_code | Block insert otherwise | T1 |
| BR-06-021 | VendorInvoice match run | Auto-run InvoiceMatchResult compute on VendorInvoice INSERT (Two_Way if no GRNs linked yet; Three_Way otherwise) | Match result row created | T1 |
| BR-06-022 | InvoiceMatchResult.pmo_override_applied=true | Caller=PMO_DIRECTOR; pmo_override_justification ≥ 200 chars; only allowed if match_status ∈ {Three_Way_Fail_Quantity, Three_Way_Fail_Rate} | Persist override; emit `INVOICE_MATCH_OVERRIDE_APPLIED` | T1 |
| BR-06-023 | PaymentEvidence assemble | Caller=FINANCE_LEAD; match_result_id must reference a `Three_Way_Pass`, `Two_Way_Pass`, or `Override_Approved` match | Block otherwise; on success persist evidence_payload bundle and emit `EVIDENCE_ASSEMBLED` | T1 |
| BR-06-024 | PaymentEvidence transition to Confirmed_Paid | Caller=FINANCE_LEAD; bank_debit_advice_doc_id (or _url stub) required; manual flip per OQ-1.7=C (no automation in v1.0) | Persist; write CostLedgerEntry(state=Paid, amount_inr=gross_payable_inr, source=PaymentEvidence) | T1 |
| BR-06-025 | Payment SLA sweep (T3 daily) | For VendorInvoice WHERE status ∈ {Match_Passed, Evidence_Assembled, Handed_Over} AND (today − invoice.received_date) > M06FinancialConfig.payment_sla_warn_days: Decision Queue `PAYMENT_SLA_BREACH` severity=Medium (warn) or High (red beyond payment_sla_red_days) | Decision created | T3 |
| BR-06-026 | Retention create | Auto on RABill Approved (BR-06-016). release_status=Withheld; eligibility computed lazily by BR-06-027/028 sweeps. | Persist | T1 |
| BR-06-027 | Substantial completion eligibility sweep | On M08 `SG_9_PASSAGE` event (stub until M08 built — SG-9 = Substantial / Practical Completion gate): For each Retention WHERE release_status=Withheld AND release_type IS NULL: set release_type=Substantial_Completion; release_tranche_pct = M01.Contract.dlp_retention_split_pct (M01 v1.3 cascade — default 0.5); release_status=Eligible; eligible_at=now; populate eligibility_basis | Emit `DLP_RELEASE_PRECONDITION_MET` | T2 (event-driven) |
| BR-06-028 | DLP-end eligibility sweep | On `DLP_RETENTION_RELEASE_ELIGIBLE` event (stub from M15) AND M09 zero-count signal: For each Retention WHERE release_status ∈ {Withheld, Released-tranche1}: validate M15.open_defect_count=0 AND M09.open_noncompliance_count=0; if pass: set release_type=DLP_End, release_tranche_pct=(1.0 − previously_released_pct), release_status=Eligible, eligible_at=now. Else: release_status=Blocked, block_reason populated | Emit `DLP_RELEASE_PRECONDITION_MET` or `DLP_RELEASE_PRECONDITION_BLOCKED` | T2 |
| BR-06-029 | Retention transition Eligible → Approved_Finance → Released | Approved_Finance requires FINANCE_LEAD signature. Released requires PMO_DIRECTOR signature (dual sign-off per OQ-1.8=C). On Released: write CostLedgerEntry(state=Paid, source=Retention, amount_inr=released_amount_inr, triggering_event=`RETENTION_TRANCHE_RELEASED`) | Persist; emit `RETENTION_TRANCHE_RELEASED` | T1 |
| BR-06-030 | Retention.pmo_override_applied=true | Caller=PMO_DIRECTOR; pmo_override_justification ≥ 200 chars; allowed only when normal pre-conditions blocked. Bypasses M15 / M09 zero-count check. | Persist; emit `DLP_RELEASE_PMO_OVERRIDE` | T1 |
| BR-06-031 | BGStub daily expiry sweep | For each BGStub WHERE expiry_date < today AND is_active=true: set is_active=false; emit `BG_STATUS_UPDATED` | T3 sweep | T3 |
| BR-06-032 | BGStub expiry warning sweep | For each BGStub WHERE is_active=true AND not yet warned at threshold: emit `BG_EXPIRING_SOON` Decision Queue at 90/30/7-day thresholds (per M06FinancialConfig.bg_warning_days_*); set respective `expiry_warning_emitted_*` true | Decision created | T3 |
| BR-06-033 | ForexRateMaster lock sweep | For each row WHERE created_at + 24h < now AND is_locked=false: set is_locked=true; emit `FOREX_RATE_LOCKED`. After lock, any UPDATE attempt on rate_to_inr is blocked at app layer (T1 enforced via API guard); the row's history is preserved in ForexRateLog. | Persist lock; emit log row | T2 (hourly sweep) |
| BR-06-034 | ForexRateMaster.rate_tier=Bank_Transaction with deviation > M06FinancialConfig.forex_deviation_pct | Compute deviation against most recent RBI_Reference for same (currency_code, rate_date). If deviation > threshold: pmo_approval_required=true; row stays in pending state; Decision Queue `FOREX_DEVIATION_APPROVAL` severity=High; on PMO approval, set pmo_approved_by + pmo_approved_at | Persist; emit `FOREX_RATE_PMO_APPROVED` on approval | T1 |
| BR-06-035 | CostLedgerEntry / VendorInvoice INSERT where currency_code ≠ INR | forex_rate_id required AND must be locked (is_locked=true) AND PMO-approved if applicable | Block insert otherwise; emit `FOREX_RATE_NOT_LOCKED` Decision | T1 |
| BR-06-036 | ForexVariation period-end compute | Quarterly (or per reporting_period): for each open PO with currency_code ≠ INR: compute variation_inr = committed_amount_foreign × (rate_at_period_end − rate_at_commit); persist ForexVariation row; emit `FOREX_VARIATION_COMPUTED` | Persist | T2 |
| BR-06-037 | M02 BAC_INTEGRITY_STATUS_CHANGED received | Snapshot affected packages; if any open RA bills or PO commitments exist for the package, set bac_integrity_warning_flag on those records (per OQ-1.4=B). On status return to Confirmed: clear flags, write reconciliation note in audit log. | Flag updates; emit `BAC_INTEGRITY_WARNING_FLAGGED` | T1 |
| BR-06-038 | M09 COMPLIANCE_HOLD_BILLING received (stub until M09 built) | Set RABill.compliance_hold_flag=true AND VendorInvoice.compliance_hold_flag=true on records linked to the affected package_id; block all subsequent state transitions (BR-06-015 enforces) until M09 clears the hold | Flag updates; emit `COMPLIANCE_HOLD_APPLIED` | T1 |
| BR-06-039 | M05 VO_APPROVED_COST_IMPACT received (stub until M05 built) | Write CostLedgerEntry(state=Committed, source=`M05.VariationOrder`, amount_inr=vo_cost_impact_inr, triggering_event=`VO_APPROVED`) per the approved VO; respects BACIntegrityLedger contract (no DB read of M02 ledger) | CostLedgerEntry persisted | T1 |
| BR-06-040 | CashflowForecast regen | Atomic transaction: lock affected (project_id, wbs_id, period_start_date) rows; recompute forecast_committed/accrued/paid from PO schedule + M03 PVProfile + payment_credit_days shift; recompute actual_committed/accrued/paid from CostLedgerEntry sums; commit. If runtime exceeds M06FinancialConfig.cashflow_regen_max_runtime_seconds: rollback; emit `CASHFLOW_REGEN_FAILED` Decision Queue trigger. | T2 heavyweight | T2 (event-driven on report_date change OR reporting_period_type change OR Approved progress) |
| BR-06-041 | M03 reporting_period_type change received | Trigger BR-06-040 cashflow regen; period boundary fields on existing CostLedgerEntry rows are NOT mutated (append-only); future writes use new period boundaries; emit `CASHFLOW_REGENERATED` | Cashflow regen | T2 |
| BR-06-042 | Capital headroom advisory | T3 daily sweep: for each (project, package) compute Committed/BAC. If ≥ capital_headroom_amber_pct: AMBER Decision Queue. If ≥ capital_headroom_red_pct: RED. | Decision created | T3 |
| BR-06-043 | Cost overrun advisory | T3 daily sweep: for each (project, package) compute (Accrued + Committed_uninvoiced)/BAC. If > cost_overrun_warn_pct: warn. If > cost_overrun_red_pct: red. | Decision created | T3 |
| BR-06-044 | Retention release stale check | T3 daily sweep: for each Retention WHERE release_status=Eligible AND (today − eligible_at) > M06FinancialConfig.retention_release_stale_days: Decision Queue `RETENTION_RELEASE_BLOCKED_DLP` severity=Medium | Decision created | T3 |
| BR-06-045 | M01 v1.3 cascade — `Contract.dlp_retention_split_pct` (NEW field) | On Contract create: default = M06FinancialConfig.retention_minor_release_pct_default (0.50). PMO_DIRECTOR-edit only with justification ≥ 100 chars. Range 0.0001–0.9999 (must split). | Persist on M01 Contract entity | T1 |
| BR-06-046 | M06FinancialConfig edit | Caller=PMO_DIRECTOR; last_edit_justification ≥ 100 chars; numeric values within sane bounds (e.g., capital_headroom thresholds in [0.50, 1.20]; payment_sla_warn_days in [1, 90]; tolerances in [0.0, 0.10]) | Persist; emit `M06_CONFIG_EDITED` | T1 |
| BR-06-047 | Document upload (stub mode pre-M12) | document_url JSONB; per URL validate MinIO domain + content-type; upload allowed only by writers of the parent entity (PO, Invoice, BG cert); emit `DOCUMENT_ATTACHED` | Persist; one-time migration when M12 lands (Appendix C) | T1 |

---

## BLOCK 7 — INTEGRATION POINTS

| Direction | Module | Data Exchanged | Trigger | Speed Tier |
|---|---|---|---|---|
| RECEIVES FROM | M34 | Auth, role, project scope; FINANCE_LEAD MFA enforcement; field-level rate spike formulas (X9 §6); audit log shell | Every API call | T1 |
| RECEIVES FROM | M01 | `project_id`, `Contract.contract_value_basic`, `Contract.gst_rate`, `Contract.retention_pct`, `Contract.dlp_term_days`, `Contract.payment_credit_days`, `Contract.mobilisation_advance_pct`, `Contract.material_advance_pct`, `Contract.dlp_retention_split_pct` (M01 v1.3 cascade — NEW field), `Party` master for vendor identity, `KPIThreshold` (Margin band) | On Activation + Contract edit + scenario change | T1 |
| RECEIVES FROM | M02 | `Package.bac_amount` (per-package BAC for Budgeted seed), `Package.bac_integrity_status` + `pending_vo_id` (read-only — flag, don't block per OQ-1.4=B), `BOQItem.actual_rate` (line-item invoice match), `BACIntegrityLedger` (read-only audit consumption via API per F-005 — never DB read) | Internal API | T1 |
| RECEIVES FROM | M03 | `LookAheadConfig.reporting_period_type` (period boundaries — cached per regen job per OQ-2.4); `PVProfile.cumulative_pv_amount` per (WBS × period) for cashflow forecast symmetry per OQ-1.5; `ProcurementScheduleItem.planned_delivery_date` for cashflow forecast committed-tier; `Milestone` where milestone_type=Financial AND status=Achieved → `MILESTONE_ACHIEVED_FINANCIAL` event for milestone-driven RA bills (per OQ-1.3=B) | Internal API + event | T1 + T2 (cashflow regen) |
| RECEIVES FROM | M04 | `BILLING_TRIGGER_READY` event (entry_id, package_id, entry_value_inr, approved_at) per BR-04-012 — drives RABill creation; `MATERIAL_GRN_EMITTED` event (receipt_id, package_id, unit_value_inr, qc_decision) per BR-04-028 — drives GRN creation + Accrued CostLedgerEntry | Event subscription (internal pub/sub) | T1 |
| SENDS TO | M01 | `Contract.dlp_retention_split_pct` cascade note write (M01 v1.3); `M06_CONFIG_CREATED` notification on auto-seed | On Project Active + Contract edit | T1 |
| SENDS TO | M03 | `actual_order_date` back-fill on PO Issued (BR-06-005) → M03.ProcurementScheduleItem.actual_order_date AND m06_po_id | On PO Issued | T1 |
| SENDS TO | M07 EVMEngine (when built) | AC per (project × WBS × period) via internal API: SUM(CostLedgerEntry.amount_inr WHERE state IN (Accrued, Paid) AND period overlaps target period). Also EAC inputs from Cost overrun trends. | API read by M07 (no event needed) | T1 |
| SENDS TO | M10 EPCC Command (when built) | Capital Funnel data, cashflow time-series, vendor outstanding bar, payment aging | On any change | T2 |
| SENDS TO | M11 ActionRegister (when built) | Decision Queue items: CAPITAL_HEADROOM_BREACH, COST_OVERRUN_ADVISORY, PAYMENT_SLA_BREACH, FOREX_DEVIATION_APPROVAL, BG_EXPIRING_SOON, RETENTION_RELEASE_BLOCKED_DLP, INVOICE_MATCH_FAILED, BAC_INTEGRITY_WARNING, CASHFLOW_REGEN_FAILED | On condition match | T1 / T2 / T3 per trigger |
| RECEIVES FROM | M05 Risk & Change (stub until M05 built) | `VO_APPROVED_COST_IMPACT` event → BR-06-039 writes Committed CostLedgerEntry; `LD_ELIGIBLE_AMOUNT` event → CostLedgerEntry deduction tracker | Event (stub endpoint contract documented at v1.0) | T1 |
| RECEIVES FROM | M08 GateControl (stub until M08 built) | `SG_9_PASSAGE` event (Substantial / Practical Completion) → Retention.eligible_at population for Substantial_Completion tranche (BR-06-027); `SG_11_PASSAGE` event (DLP End / Project Closure) consumed alongside M15/M09 zero-counts for DLP_End tranche (BR-06-028) | Event (stub endpoint contract documented at v1.0) | T1 |
| RECEIVES FROM | M09 ComplianceTracker (stub until M09 built) | `COMPLIANCE_HOLD_BILLING` flag → block RABill / VendorInvoice transitions (BR-06-038); `COMPLIANCE_OPEN_NONCOMPLIANCE_COUNT_CHANGED` → Retention DLP-end eligibility recompute | Event (stub endpoint contract documented at v1.0) | T1 |
| RECEIVES FROM | M15 HandoverManagement (stub until M15 built) | `DLP_RETENTION_RELEASE_ELIGIBLE` event (open_defect_count=0 signal) → Retention DLP-end eligibility recompute (BR-06-028) | Event (stub endpoint contract documented at v1.0) | T1 |
| BIDIRECTIONAL | M23 BGInsuranceTracker (Phase 2) | One-time migration from BGStub to M23 BG records — Appendix C migration script. Until M23 lands: M06 owns BGStub. | Migration cascade event | T3 (one-time) |
| BIDIRECTIONAL | M12 DocumentControl (when built) | One-time migration from `document_url` MinIO stubs to M12 Document references — Appendix C migration script | Migration cascade event | T3 (one-time) |

**Stub endpoint contracts** (documented at v1.0 lock; consuming modules implement when built):

```
POST /api/m06/v1/events/vo-approved-cost-impact     # M05 → M06 (BR-06-039)
POST /api/m06/v1/events/sg9-passage                 # M08 → M06 (BR-06-027) — Substantial Completion
POST /api/m06/v1/events/sg11-passage                # M08 → M06 (BR-06-028) — DLP End / Project Closure
POST /api/m06/v1/events/compliance-hold-billing     # M09 → M06 (BR-06-038)
POST /api/m06/v1/events/compliance-noncompliance-count-changed  # M09 → M06 (BR-06-028)
POST /api/m06/v1/events/dlp-retention-release-eligible  # M15 → M06 (BR-06-028)
GET  /api/m06/v1/ac/by-period?wbs_id=&period_start=  # M07 reads (when built)
```

---

## BLOCK 8 — GOVERNANCE AND AUDIT

### 8a. Logged Events (action-level — full names locked in Appendix A)

| Action | Logged | Field-Level Detail | Visible To | Retention |
|---|---|---|---|---|
| CostLedgerEntry create (any state) | Yes | All fields, immutable row | FINANCE_LEAD, PMO_DIRECTOR, EXTERNAL_AUDITOR | **Permanent** |
| CostLedgerEntry state transition cascade (Budgeted → Committed → Accrued → Paid) | Yes (each is its own row by design) | Transition event_type | FINANCE_LEAD, PMO_DIRECTOR, EXTERNAL_AUDITOR | **Permanent** |
| PurchaseOrder create / amend / cancel | Yes | All fields, before/after | FINANCE_LEAD, PROCUREMENT_OFFICER, PMO_DIRECTOR | **Permanent** |
| RABill create / submit / approve / reject / paid | Yes | All fields, all signatures | QS_MANAGER, FINANCE_LEAD, PMO_DIRECTOR | **Permanent** |
| VendorInvoice receipt + match | Yes | Match details (qty/rate variance), match_status | FINANCE_LEAD, PROCUREMENT_OFFICER | Project lifetime |
| InvoiceMatchResult PMO override | Yes | Match details + override justification (≥200 chars) | FINANCE_LEAD, PMO_DIRECTOR, EXTERNAL_AUDITOR | **Permanent** |
| PaymentEvidence assemble / hand-over / confirm | Yes | Evidence bundle snapshot | FINANCE_LEAD, PMO_DIRECTOR, EXTERNAL_AUDITOR | **Permanent** |
| Retention withhold / release tranche / PMO override | Yes | All fields incl. dual sign-off + eligibility basis | FINANCE_LEAD, PMO_DIRECTOR, EXTERNAL_AUDITOR | **Permanent** |
| Forex rate enter / lock / PMO approve | Yes | Old/new rate, deviation, FEMA evidence ref | FINANCE_LEAD, PMO_DIRECTOR, EXTERNAL_AUDITOR | **Permanent** |
| BGStub create / status update / migration | Yes | Coverage, expiry, status flips | FINANCE_LEAD, PMO_DIRECTOR | Project lifetime → Permanent on Phase 2 migration |
| M06FinancialConfig create / edit | Yes | All fields, justification | PMO_DIRECTOR, FINANCE_LEAD, EXTERNAL_AUDITOR | **Permanent** |
| Cashflow regenerate / regen-fail | Yes | Job ID, runtime, affected rows | FINANCE_LEAD, PMO_DIRECTOR | Project lifetime |
| Document migration to M12 (one-shot) | Yes | Pre/post counts, M12 doc IDs | SYSTEM_ADMIN, PMO_DIRECTOR | **Permanent** |
| BG migration to M23 (one-shot) | Yes | Pre/post mapping | SYSTEM_ADMIN, PMO_DIRECTOR | **Permanent** |
| BAC integrity warning flag set/clear | Yes | pending_vo_id snapshot | FINANCE_LEAD, PMO_DIRECTOR | **Permanent** |

### 8b. Immutability Rules (DB-level)

- **`CostLedgerEntry`** — DB-level UPDATE/DELETE forbidden; INSERT only. Reversal achieved via additional INSERT (e.g., negative-amount Budgeted on PO cancel per BR-06-008).
- **`RABillAuditLog`** — DB-level UPDATE/DELETE forbidden; INSERT only.
- **`PaymentEvidenceLedger`** — DB-level UPDATE/DELETE forbidden; INSERT only.
- **`ForexRateLog`** — DB-level UPDATE/DELETE forbidden; INSERT only.
- **`ForexRateMaster`** — App-layer enforced immutability of `rate_to_inr` after `is_locked=true` (24h window). The `is_locked` flip itself is recorded in ForexRateLog.
- **`PurchaseOrder`** — Mutable until status=Issued; immutable thereafter except `status` transitions to {Partially_Received, Fully_Received, Closed, Cancelled}.
- **`RABill`** — Mutable until status=Approved; immutable thereafter except `status` transitions to {Paid}. RABillLines mutable while parent is.
- **`Retention`** — Mutable until release_status=Released; immutable thereafter.
- **`PaymentEvidence`** — Mutable until status=Confirmed_Paid; immutable thereafter.

### 8c. Privacy / Role Visibility

- **Field-level rate display** (per X9 §6 + cross-cutting role mapping locked in M02 BR-02-008): SITE_MANAGER and READ_ONLY see `[RESTRICTED]` for ₹ values on the Capital Funnel and all rate-bearing fields. PROJECT_DIRECTOR / PORTFOLIO_MANAGER / PROCUREMENT_OFFICER / COMPLIANCE_MANAGER see Loaded × 1.15. PLANNING_ENGINEER / QS_MANAGER see Indexed × 1.08. SYSTEM_ADMIN / PMO_DIRECTOR / FINANCE_LEAD / EXTERNAL_AUDITOR see actuals (with `RATE_ACCESSED_PRIVILEGED` audit per X9 §6).
- PMO_DIRECTOR override justifications (InvoiceMatchResult, Retention, ForexRateMaster) visible only to PMO_DIRECTOR + FINANCE_LEAD + EXTERNAL_AUDITOR.
- BGStub.coverage_amount_inr visible to FINANCE_LEAD + PMO_DIRECTOR; redacted for SITE_MANAGER + READ_ONLY.
- ForexRateMaster bank advice references (`source_reference` for Bank_Transaction tier) visible only to FINANCE_LEAD + PMO_DIRECTOR + EXTERNAL_AUDITOR.
- VendorInvoice.tds_amount visible to FINANCE_LEAD only (TDS detail withheld from QS / Procurement views).
- All append-only ledger reads gated by M34 RBAC; EXTERNAL_AUDITOR has read access to all four ledgers.

---

## BLOCK 9 — EXPLICIT EXCLUSIONS

```
This module does NOT:
─────────────────────────────────────────────────────────────────────
[ ] Compute BAC per package                                     → M02 StructureWBS (M06 reads via API)
[ ] Write BACIntegrityLedger                                    → M02 owns; M06 reads only via API
[ ] Calculate or own approved progress percentage               → M04 ExecutionCapture (M06 receives BILLING_TRIGGER_READY)
[ ] Initiate, approve, or compute monetary impact of VOs        → M05 Risk & Change (M06 receives VO_APPROVED_COST_IMPACT)
[ ] Calculate LD eligibility or contingency draw                → M05
[ ] Compute EVM (CPI / SPI / EAC / ETC / VAC / TCPI)            → M07 EVMEngine (M06 supplies AC; M07 computes)
[ ] Decide stage-gate passage / SG-11 evidence                  → M08 GateControl
[ ] Track DLP defects (count, status, resolution)               → M15 HandoverManagement
[ ] Track regulatory non-compliance (NABH, AERB, EC, Fire NOC)  → M09 ComplianceTracker
[ ] Maintain BG identity master / claim workflow                → M23 BGInsuranceTracker (Phase 2; M06 ships BGStub)
[ ] Reconcile GST input credit / aggregate TDS for filing       → future TaxLedger module (Phase 2). M06 records GST + TDS on invoice; no reconciliation in v1.0 (per OQ-1.11=C).
[ ] Generate bank file or initiate payment transfer             → external accounting system (Tally / SAP / Zoho per OQ-1.7=C). M06 hands evidence; accounting executes.
[ ] Run signature workflow for payment release                  → external accounting system
[ ] Manage vendor master / pre-qualification / scorecards       → M30 VendorMasterPQ (Phase 2). M06 references M01 Party only.
[ ] Bidirectional sync with Tally / SAP / Zoho                  → out of v1.0 (M01.Project.accounting_system is free-text stub)
[ ] Override M03 reporting_period_type                          → M03 owns (per M01 v1.2 cascade); M06 reads via API
[ ] Re-baseline schedule on VO                                  → M03 explicitly excludes (M06 inherits)
[ ] Authenticate users / manage roles / audit shell             → M34 SystemAdminRBAC
[ ] Run working-capital MILP optimisation                       → L1 Strategic (M16 / M17 / M18 / M19)
[ ] Localise to non-Indian currency taxonomies (e.g., AED)      → out of v1.0 even with multi-currency (medical-equipment USD/EUR only)
```

---

## BLOCK 10 — OPEN QUESTIONS

**All questions resolved. Zero open questions.** All 11 OQ-1 + 6 OQ-2 items from Brief v1.0 (Round 23) closed at Brief lock 2026-05-03.

| # | Source | Resolution |
|---|---|---|
| OQ-1.1 | Brief | **A — 4-state machine LOCKED** (Budgeted → Committed → Accrued → Paid). Approval governance on parent entities, not on ledger. |
| OQ-1.2 | Brief | **B — per (Package × Period) RABill grain LOCKED.** KDMC monthly RA pattern. |
| OQ-1.3 | Brief | **B — both progress + milestone trigger sources LOCKED.** RABillTriggerSource ENUM (X8 v0.6 cascade). |
| OQ-1.4 | Brief | **B — flag, do not block on Stale_Pending_VO LOCKED.** `bac_integrity_warning_flag` field on CostLedgerEntry + RABill. |
| OQ-1.5 | Brief | **A — full project lifetime per-WBS-per-period CashflowForecast LOCKED.** Mirrors M03 PVProfile. |
| OQ-1.6 | Brief | **B — multi-currency from v1.0 LOCKED.** ForexRateMaster + ForexVariation entities; ExchangeRateTier ENUM (X8 v0.6 cascade). KDMC pilot defaults to INR but system supports foreign-currency contracts. |
| OQ-1.7 | Brief | **C — split scope LOCKED.** EPCC owns 2/3-way match (M06.VendorInvoice + M06.InvoiceMatchResult); external accounting executes payment + signature workflow. |
| OQ-1.8 | Brief | **C — tranched retention release with dual sign-off LOCKED.** M01 v1.3 cascade for `Contract.dlp_retention_split_pct`. Default 50/50 split (Substantial Completion + DLP End). |
| OQ-1.9 | Brief | **B — BGStub pattern LOCKED.** Mirrors M04→M12 photo-stub. Migration cascade Appendix C for M23 (Phase 2). |
| OQ-1.10 | Brief | **A — M06FinancialConfig per-project tunables LOCKED.** Mirrors M04 ProjectExecutionConfig. PMO_DIRECTOR-only edits. |
| OQ-1.11 | Brief | **C — invoice-record-only tax LOCKED.** GST + TDS captured on VendorInvoice; no reconciliation. Future TaxLedger module (Phase 2). |
| OQ-2.1 | Brief | **Confirmed — 4 append-only ledgers LOCKED** (CostLedgerEntry, RABillAuditLog, PaymentEvidenceLedger, ForexRateLog). DB-level UPDATE/DELETE forbidden. |
| OQ-2.2 | Brief | **Confirmed — Audit Events Catalogue locked from authoring (Appendix A — 43 events).** |
| OQ-2.3 | Brief | **Confirmed — speed-tier mapping LOCKED.** T1 transactional integrity, T2 cashflow regen heavyweight, T3 batch sweeps. |
| OQ-2.4 | Brief | **Confirmed — read `reporting_period_type` from M03 internal API per F-005; cache for regen job duration; no denormalised storage.** |
| OQ-2.5 | Brief | **Confirmed — document references stub LOCKED.** `document_url` JSONB (MinIO direct) + `document_id` JSONB (M12 target). One-time migration cascade Appendix C. |
| OQ-2.6 | Brief | **N/A — OQ-1.6=B (multi-currency shipped); rule about "no nullable forex hooks" doesn't apply.** |

---

## CASCADE IMPLICATIONS (for VersionLog + downstream modules)

**X8 v0.6 — new ENUMs proposed (M06-owned unless noted):**

| ENUM | Values | Source BR / Entity |
|---|---|---|
| `CostLedgerEntryState` | `Budgeted / Committed / Accrued / Paid` | OQ-1.1=A; CostLedgerEntry.state |
| `PurchaseOrderStatus` | `Draft / Issued / Partially_Received / Fully_Received / Closed / Cancelled` | PurchaseOrder.status |
| `RABillStatus` | `Draft / Submitted / Approved / Rejected / Paid` | RABill.status |
| `RABillTriggerSource` | `Progress / Milestone` | OQ-1.3=B; RABill.trigger_source |
| `GRNMatchStatus` | `Unmatched / Linked / Matched / Disputed` | GRN.match_status |
| `VendorInvoiceStatus` | `Received / Match_Pending / Match_Passed / Match_Failed / Evidence_Assembled / Handed_Over / Cancelled` | OQ-1.7=C; VendorInvoice.status |
| `InvoiceMatchMode` | `Two_Way / Three_Way` | InvoiceMatchResult.match_mode |
| `InvoiceMatchStatus` | `Three_Way_Pass / Three_Way_Fail_Quantity / Three_Way_Fail_Rate / Two_Way_Pass / Pending / Override_Approved` | OQ-1.7=C; InvoiceMatchResult.match_status |
| `PaymentEvidenceStatus` | `Assembled / Handed_Over / Confirmed_Paid / Cancelled` | PaymentEvidence.status |
| `RetentionReleaseType` | `Substantial_Completion / DLP_End / PMO_Override` | OQ-1.8=C; Retention.release_type |
| `RetentionReleaseStatus` | `Withheld / Eligible / Approved_Finance / Released / Blocked / Cancelled` | Retention.release_status |
| `ExchangeRateTier` | `RBI_Reference / Bank_Transaction` | OQ-1.6=B; ForexRateMaster.rate_tier |
| `BGType` | `Performance / Advance_Payment / Retention_Substitute / Bid / Other` | BGStub.bg_type |

**X8 v0.6 — Decision Queue trigger types catalogued (M06_DecisionQueueTriggerType):**

```
CAPITAL_HEADROOM_BREACH        BR-06-042 / BR-06-004
COST_OVERRUN_ADVISORY          BR-06-043
PAYMENT_SLA_BREACH             BR-06-025
FOREX_DEVIATION_APPROVAL       BR-06-034
BG_EXPIRING_SOON               BR-06-032
RETENTION_RELEASE_BLOCKED_DLP  BR-06-044
INVOICE_MATCH_FAILED           BR-06-018
BAC_INTEGRITY_WARNING          BR-06-003 / BR-06-037
CASHFLOW_REGEN_FAILED          BR-06-040
FOREX_RATE_NOT_AVAILABLE       BR-06-006
FOREX_RATE_NOT_LOCKED          BR-06-035
COMPLIANCE_HOLD_APPLIED        BR-06-038
```

**X8 v0.6 — append-only entity exemption list extension:** add `CostLedgerEntry`, `RABillAuditLog`, `PaymentEvidenceLedger`, `ForexRateLog` to §6.

**X8 v0.6 — AuditEventType extension:** 28 M06 event types per Appendix A.

**X9 v0.4 cascade:** §13.3.6 row already exists at v0.3; M06 wireframes (Round 25) will validate. May need refinement post-Wireframes.

**M01 v1.3 cascade note** (per OQ-1.8=C, BR-06-045): adds `Contract.dlp_retention_split_pct DECIMAL(5,4) DEFAULT 0.5000` field. Cascade-note pattern (small change → 1 field), NOT full re-issue.

**M03 minor cascade** (per OQ-1.3=B): M03 Spec gains explicit emit hook on `Milestone.status → Achieved` for `milestone_type=Financial` — `MILESTONE_ACHIEVED_FINANCIAL` event. Cascade-note pattern.

**M04 read-side confirmation** (no cascade): M04 BR-04-012 (`BILLING_TRIGGER_READY`) and BR-04-028 (`MATERIAL_GRN_EMITTED`) already locked-from-authoring; M06 consumes per locked contract.

---

## APPENDIX A — Audit Events Catalogue (LOCKED from authoring per OQ-2.2)

> **Status:** LOCKED. Source of truth for M06 audit event names until X3 Audit Event Catalogue is built. When X3 lands, names migrate to X3 unchanged. Naming follows X8 §2 — UPPER_SNAKE_CASE. Authored alongside Spec per Round 18 cascade-pattern decision (avoids retro-cascade).

### Event registry (43 events)

| Event Name | Source BR | Severity | Trigger Description |
|---|---|---|---|
| `COST_LEDGER_ENTRY_CREATED` | BR-06-001..003 | Info | Any state ledger row inserted |
| `COST_LEDGER_STATE_TRANSITIONED` | BR-06-002, BR-06-007, BR-06-015, BR-06-017, BR-06-024, BR-06-029, BR-06-039 | Info | Logical alias for state-transition row inserts (Budgeted → Committed → Accrued → Paid) |
| `PURCHASE_ORDER_CREATED` | BR-06-005..007 | Info | PO created |
| `PURCHASE_ORDER_AMENDED` | (PO edit while Draft) | Info | PO edited pre-Issued |
| `PURCHASE_ORDER_CANCELLED` | BR-06-008 | Medium | PO cancelled with cancellation_reason ≥ 100 chars; reversing CostLedgerEntry written |
| `RA_BILL_CANDIDATE_BUFFERED` | BR-04-012 receipt | Info | M04 BILLING_TRIGGER_READY received and buffered for period close |
| `RA_BILL_GENERATED` | BR-06-009, BR-06-010 | Info | RABill row created (Progress or Milestone trigger) |
| `RA_BILL_SUBMITTED` | BR-06-015 | Info | Draft → Submitted by SITE_MANAGER / QS_MANAGER |
| `RA_BILL_APPROVED_QS` | BR-06-015 | Info | QS_MANAGER signature captured |
| `RA_BILL_APPROVED_FINANCE` | BR-06-015 | Info | FINANCE_LEAD signature captured; Approved final state |
| `RA_BILL_REJECTED` | BR-06-015 | Medium | Rejection with reason ≥ 50 chars |
| `RA_BILL_PAID` | BR-06-024 | Info | RABill associated PaymentEvidence flipped to Confirmed_Paid |
| `GRN_RECEIVED` | BR-06-017 | Info | M04 MATERIAL_GRN_EMITTED received and GRN row created |
| `GRN_LINKED_TO_PO` | BR-06-017 | Info | GRN successfully linked to PurchaseOrder |
| `GRN_INVOICE_MATCHED` | BR-06-018 | Info | GRN.match_status flipped to Matched |
| `VENDOR_INVOICE_RECEIVED` | BR-06-019..021 | Info | Invoice received and match initiated |
| `INVOICE_MATCH_PASSED` | BR-06-018 | Info | Three_Way_Pass or Two_Way_Pass |
| `INVOICE_MATCH_FAILED` | BR-06-018 | High | **Decision Queue trigger** — match failed (qty or rate variance) |
| `INVOICE_MATCH_OVERRIDE_APPLIED` | BR-06-022 | High | PMO override of failed match; justification ≥ 200 chars |
| `EVIDENCE_ASSEMBLED` | BR-06-023 | Info | PaymentEvidence bundle assembled |
| `EVIDENCE_HANDED_OVER` | BR-06-023 | Info | Evidence pushed to external accounting |
| `PAYMENT_CONFIRMED` | BR-06-024 | Info | FINANCE_LEAD flipped PaymentEvidence to Confirmed_Paid; Paid CostLedgerEntry written |
| `RETENTION_WITHHELD` | BR-06-016 | Info | Retention row created at RABill Approved |
| `RETENTION_TRANCHE_RELEASED` | BR-06-029 | Info | Tranche released (Substantial_Completion or DLP_End); Paid CostLedgerEntry written |
| `DLP_RELEASE_PRECONDITION_MET` | BR-06-027, BR-06-028 | Info | Release pre-conditions met (SG-9 passage for Substantial_Completion tranche OR SG-11 passage + M15/M09 zero counts for DLP_End tranche) |
| `DLP_RELEASE_PRECONDITION_BLOCKED` | BR-06-028 | Medium | DLP-end blocked due to M15 open defects OR M09 open non-compliance |
| `DLP_RELEASE_PMO_OVERRIDE` | BR-06-030 | High | PMO override of DLP release pre-conditions; justification ≥ 200 chars |
| `FOREX_RATE_ENTERED` | BR-06-033 (daily seed) | Info | New ForexRateMaster row inserted |
| `FOREX_RATE_LOCKED` | BR-06-033 | Info | 24h lock window expired; row immutable thereafter |
| `FOREX_RATE_PMO_APPROVED` | BR-06-034 | Medium | PMO approved Bank_Transaction tier rate with deviation > threshold |
| `FOREX_DEVIATION_REVIEW` | BR-06-034 | High | **Decision Queue trigger** — Bank_Transaction rate deviates > forex_deviation_pct from RBI_Reference |
| `FOREX_VARIATION_COMPUTED` | BR-06-036 | Info | Period-end variation row written |
| `CASHFLOW_REGENERATED` | BR-06-040, BR-06-041 | Info | Successful cashflow regen |
| `CASHFLOW_REGEN_FAILED` | BR-06-040 | High | **Decision Queue trigger** — regen runtime exceeded or commit failed |
| `M06_CONFIG_CREATED` | (Project Active seed) | Info | M06FinancialConfig auto-created |
| `M06_CONFIG_EDITED` | BR-06-046 | Medium | PMO edit with justification ≥ 100 chars |
| `BG_STATUS_UPDATED` | BR-06-031 | Info | BGStub.is_active flipped or coverage updated |
| `BG_EXPIRING_SOON` | BR-06-032 | Medium | **Decision Queue trigger** — 90 / 30 / 7-day warning |
| `BG_MIGRATED_TO_M23` | (Appendix C) | Info | One-time migration cascade event |
| `BAC_INTEGRITY_WARNING_FLAGGED` | BR-06-003, BR-06-037 | Medium | CostLedgerEntry / RABill written against Stale_Pending_VO package |
| `COMPLIANCE_HOLD_APPLIED` | BR-06-038 | High | M09 hold flag set on RABill / VendorInvoice |
| `DOCUMENT_ATTACHED` | BR-06-047 | Info | Stub-period document URL added |
| `DOCUMENT_MIGRATED_TO_M12` | (Appendix C) | Info | One-time migration cascade event |

### Decision Queue triggers (12) — summary

`CAPITAL_HEADROOM_BREACH`, `COST_OVERRUN_ADVISORY`, `PAYMENT_SLA_BREACH`, `INVOICE_MATCH_FAILED`, `FOREX_DEVIATION_APPROVAL` (alias `FOREX_DEVIATION_REVIEW`), `FOREX_RATE_NOT_AVAILABLE`, `FOREX_RATE_NOT_LOCKED`, `BG_EXPIRING_SOON`, `RETENTION_RELEASE_BLOCKED_DLP`, `BAC_INTEGRITY_WARNING`, `CASHFLOW_REGEN_FAILED`, `COMPLIANCE_HOLD_APPLIED`.

Spec count discipline: the 28-event registry above includes both audit-only events and the 12 events that ALSO act as Decision Queue triggers. Event count = 28 named entries; trigger count = 12 (subset of named entries plus alias).

### Notes

- `COST_LEDGER_STATE_TRANSITIONED` is a **logical alias** for Budgeted → Committed → Accrued → Paid sequence — the underlying append-only row inserts each carry their own `triggering_event` field. The audit-event name allows SIEM filtering at a higher level of abstraction.
- `BG_EXPIRING_SOON` fires at 90 / 30 / 7 day thresholds; the same row in BGStub fires three times across its lifecycle (with separate `expiry_warning_emitted_*` boolean idempotency markers).
- Migration events (`BG_MIGRATED_TO_M23`, `DOCUMENT_MIGRATED_TO_M12`) are one-time per row at Phase 2 module landings.

---

## APPENDIX B — KDMC Reference Data Mapping

| KDMC Excel Source | M06 Entity | Notes |
|---|---|---|
| `06_Cost_Ledger` (legacy sheet) | CostLedgerEntry | Approx. 12,000 transitions over project lifetime per legacy v2.1; KDMC monthly cadence |
| `06_Purchase_Orders` | PurchaseOrder | KDMC ~80 POs across L&T civil, MEP subcontractors, medical-equipment vendors |
| `06_RA_Bills_Register` | RABill (trigger_source=Progress) | Monthly RA bills; KDMC has ~36 RA bills planned across project lifetime |
| `06_Milestone_Payments` (manual) | RABill (trigger_source=Milestone) | DBOT milestone tranche schedule per M01.Contract — typical 6–10 milestone bills |
| `06_GRN_Register` | GRN | Material receipts driven by M04 MaterialReceipt with qc_decision=Accepted |
| `06_Vendor_Invoices` | VendorInvoice + InvoiceMatchResult | Three-way match runs on every invoice; KDMC equipment imports trigger Forex matching |
| `06_Retention_Ledger` | Retention | KDMC retention_pct = 5% of contract value = ₹3.42 Cr (₹68.4 Cr × 0.05) |
| `06_Cashflow_Forecast` | CashflowForecast | ~30 WBS × 36 monthly periods = 1,080 rows (per Brief OQ-1.5=A) |
| `06_Forex_Variations` | ForexVariation + ForexRateMaster | KDMC may not exercise (project value = INR); LINAC / MRI / CT vendors typically USD/EUR for future projects |
| `06_BG_Register` | BGStub | KDMC: 5% performance BG (₹3.42 Cr) + mobilisation BG (₹6.84 Cr) + advance BG |
| (none — new) | M06FinancialConfig | Seeded at KDMC project Active state with defaults; PMO can tune thresholds |

**KDMC Specifics:**
```
Primary contractor:           L&T Construction (contract_id from M01)
Project value:                ₹68.4 Cr (₹68,40,00,000)
Pilot currency:               INR only (KDMC; system supports multi-currency for future projects)
Retention pct:                5.00% (M01.Contract.retention_pct = 0.0500)
Total retention withheld:     ₹3.42 Cr at full execution
DLP retention split:          50/50 (Substantial Completion + DLP End)
                              → ₹1.71 Cr release at SG-9 passage (Substantial / Practical Completion)
                              → ₹1.71 Cr release at SG-11 passage (DLP End — gated by M15 + M09 zero-counts)
DLP term:                     365 days post substantial completion
Payment credit:               30 days (default M01.Contract.payment_credit_days)
GST rate:                     18% (default; M01.Contract.gst_rate = 0.1800)
GST amount:                   ₹12.31 Cr (₹68.4 Cr × 0.18)
Mobilisation advance:         10% (₹6.84 Cr) — recovered in early RA bills
Material advance:             5% (₹3.42 Cr)
Performance BG:               5% (₹3.42 Cr) tracked in BGStub
LD rate:                      0.5% per week
LD cap:                       10% of contract value (₹6.84 Cr)
Risk buffer:                  5% (₹3.42 Cr) — owned by M05 contingency
Capital headroom thresholds:  AMBER 95% (₹64.98 Cr), RED 100% (₹68.40 Cr)
RA bill cadence:              Monthly (from M03 LookAheadConfig.reporting_period_type=Monthly)
RA bill count expected:       ~36 progress + ~6-10 milestone over project lifetime
Forex relevance:              Minimal (KDMC contract INR); medical-equipment imports may be milestone-tranched within INR contract
BG warning thresholds:        90 / 30 / 7 days before expiry
Cashflow forecast rows:       ~30 WBS × ~36 periods = ~1,080 rows
```

---

## APPENDIX C — Migration Scripts (Drafted)

> **Status:** Drafted only — execute when the absorbing module's v1.0 lands. Both scripts follow the M04→M12 photo-stub pattern as the canonical precedent.

### C.1 — `20260XXX_M23_absorb_M06_BGStub.py` (when M23 v1.0 lands)

```python
# 20260XXX_M23_absorb_M06_BGStub.py
# One-shot migration from M06 BGStub to M23 BGInsuranceTracker BG records.

# Pseudo-code:
for stub in select_where("bg_stub.migrated_to_m23_at IS NULL AND bg_stub.is_active = true"):
    m23_bg = m23.create_bg(
        source_module='M06',
        source_id=stub.bg_id,
        contract_id=stub.contract_id,
        bg_number=stub.bg_number,
        issuing_bank=stub.issuing_bank,
        bg_type=stub.bg_type,
        coverage_amount_inr=stub.coverage_amount_inr,
        issue_date=stub.issue_date,
        expiry_date=stub.expiry_date,
        claim_period_end_date=stub.claim_period_end_date,
        document_url=stub.document_url,  # M23 does its own M12 migration if needed
        document_id=stub.document_id,
        # Preserve audit history:
        original_created_by=stub.created_by,
        original_created_at=stub.created_at,
    )
    update('bg_stub', stub.bg_id,
        migrated_to_m23_at=now(),
        m23_bg_id=m23_bg.id,
        is_active=False,  # M23 owns active state thereafter
    )
    emit_audit('BG_MIGRATED_TO_M23', stub.bg_id, m23_bg_id=m23_bg.id)

# Post-migration: M06 reads BG data via M23 internal API for retention/payment-hold decisions.
# BGStub table remains as historical reference; new BGStub inserts blocked at app layer (M23 active).
```

### C.2 — `20260XXX_M12_absorb_M06_document_urls.py` (when M12 v1.0 lands)

```python
# 20260XXX_M12_absorb_M06_document_urls.py
# One-shot migration from M06 document_url JSONB stubs to M12 Document references.

# Pseudo-code:
for table in ['purchase_order', 'ra_bill', 'vendor_invoice', 'payment_evidence', 'forex_rate_master', 'bg_stub']:
    for row in select_where(f"{table}.document_url IS NOT NULL AND jsonb_array_length(document_url) > 0"):
        document_ids = []
        for url in row.document_url:
            doc = m12.create_document(
                source_module='M06',
                source_entity=table,
                source_id=row.pk,
                minio_url=url,
                uploaded_by=row.created_by,
                uploaded_at=row.created_at,  # preserve original timestamp
                # M06 document categories:
                #   purchase_order      → PO_PDF
                #   ra_bill             → RA_BILL_PDF
                #   vendor_invoice      → INVOICE_PDF
                #   payment_evidence    → BANK_DEBIT_ADVICE_PDF or EVIDENCE_BUNDLE_PDF
                #   forex_rate_master   → FEMA_FORM_A2_PDF or BANK_ADVICE_PDF
                #   bg_stub             → BG_CERTIFICATE_PDF
                category=DERIVE_FROM_TABLE(table),
            )
            document_ids.append(doc.id)
        update_row(table, row.pk, document_id=document_ids)
        emit_audit('DOCUMENT_MIGRATED_TO_M12', row.pk, table=table, count=len(document_ids))
    # Drop document_url column in M06 v1.1 cascade — one cycle later (additive safety per M04 Open Question #4 precedent).
```

### C.3 — Post-migration cleanup (M06 v1.1 cascade — one version after each absorbing module ships)

- Drop `BGStub.document_url` and `BGStub.is_active` (M23 owns active state)
- Drop `purchase_order.document_url`, `ra_bill.document_url`, `vendor_invoice.document_url`, `payment_evidence.document_url`, `payment_evidence.bank_debit_advice_url`, `forex_rate_master.fema_form_a2_url` after M12 v1.0 + 1 cycle
- These are M06 v1.1 cascade-note items, NOT v1.0 spec changes (per Round 18 cascade-pattern discipline)

---

*v1.0 — Spec DRAFT. Zero open questions. M06 FinancialControl ready for Round 24 audit pass. Cascades pending: X8 v0.6 (13 new ENUMs + 12 trigger types + 28 audit events + 4 append-only ledger exemptions); X9 v0.4 (already prepared at v0.3 §13.3.6); M01 v1.3 cascade note (`Contract.dlp_retention_split_pct`); M03 minor cascade (MILESTONE_ACHIEVED_FINANCIAL emit hook).*
