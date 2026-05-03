# M06 — Financial Control
## Module Specification v2.1
## AMENDMENT — Changed Blocks Only
**Status:** Draft — Pending Review | **Locked:** No
**Spec Author:** PMO Director | **Date:** 2026-05-02
**Reference Standards:** EPCC_Standards_Memory_v5_1.md
**Base Version:** M06_Financial_Control_v2.0
**Amendment Scope:** GAP-06: ForexRateMaster entity. Auditable exchange rate chain.
                     GAP-07 downstream: DLP retention release governance wired to M04 DLPRegister.

---

## CHANGE LOG

| Version | Date | Change Summary |
|---------|------|---------------|
| v2.0 | 2026-04-30 | Full spec: multi-currency, BG tracking, DBOT payments, sub-contractor retention |
| v2.1 | 2026-05-02 | GAP-06: ForexRateMaster entity. PurchaseOrder.po_exchange_rate and ForexVariation.payment_exchange_rate sources changed from INPUT to LINK → ForexRateMaster. BR-06-033 through BR-06-041 added. GAP-07 downstream: DLP retention release pre-conditions and retention blocking logic added to RetentionLedger. BR-06-042 through BR-06-046 added. |

---

## BLOCK 2 — Scope Boundary (Updated)

**ADDITIONS to INCLUDES:**

| INCLUDES (New) | Rationale |
|----------------|-----------|
| `ForexRateMaster` — governed exchange rate repository with two tiers (RBI_Reference / Bank_Transaction) | GAP-06: Eliminates free-text exchange rate entry. Creates auditable, cited, locked rate chain. |
| Exchange rate audit chain — ForexRateMaster → PO → Payment → ForexVariation | GAP-06 |
| DLP retention release blocking — pre-conditions from M04 DLPRegister + M09 DLPComplianceObservation | GAP-07: Retention cannot be released while DLP defects are unresolved |
| DLP retention tranche isolation in RetentionLedger | GAP-07 |

**ADDITION to EXCLUDES:**

| EXCLUDES (Clarification) |
|--------------------------|
| DLP defect management → M04 (DLPRegister, DLPDefect) |
| DLP compliance observations → M09 (DLPComplianceObservation) |
| Checking whether DLP defects exist → M04 owned. M06 receives open_defect_count as a signal. |

---

## BLOCK 3 — Data Architecture (Amendment)

### 3a. New Entity

| Entity | Description | Cardinality |
|--------|-------------|-------------|
| `ForexRateMaster` | **(NEW v2.1)** Governed repository of exchange rates used in all multi-currency transactions. Two-tier: RBI_Reference (manual, cited) and Bank_Transaction (document-backed). Source of truth for all forex in EPCC. | Many per tenant (one entry per currency per date per tier) |

---

### 3b. New Entity Fields — `ForexRateMaster`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `rate_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `currency_code` | CHAR(3) | Y | ISO 4217. FK → CurrencyMaster. Cannot be INR (base currency). | LINK → CurrencyMaster |
| `rate_date` | DATE | Y | Date this rate applies to. Unique constraint: currency_code + rate_date + rate_tier. | INPUT (Finance Lead) |
| `rate_tier` | ENUM | Y | `RBI_Reference / Bank_Transaction` | INPUT (Finance Lead) |
| `exchange_rate` | DECIMAL(12,6) | Y | INR per 1 foreign currency unit. e.g., 83.420000 for USD. Must be > 0. | INPUT (Finance Lead) |
| `source_reference` | TEXT | Y | **Mandatory for both tiers.** RBI_Reference: FBIL circular number, dated reference, or URL. Bank_Transaction: SWIFT MT103 number, bank debit advice reference, or FEMA Form A2 number. Min 10 chars. | INPUT (Finance Lead) |
| `supporting_document_url` | VARCHAR(500) | N | **Mandatory for Bank_Transaction only.** Data Lake URL — SWIFT confirmation / bank debit note / FEMA declaration. Block save if Bank_Transaction and URL missing. | INPUT (Finance Lead) |
| `rbi_reference_rate` | DECIMAL(12,6) | N | For Bank_Transaction entries: the RBI_Reference rate for same currency + date. Auto-fetched from ForexRateMaster if an RBI_Reference entry exists for same day. If not: Finance Lead must enter manually. | CALC or INPUT |
| `deviation_from_rbi_pct` | DECIMAL(8,4) | N | CALC = abs(exchange_rate − rbi_reference_rate) / rbi_reference_rate × 100. Null if rbi_reference_rate not available. | CALC |
| `deviation_flag` | BOOLEAN | Y | CALC = deviation_from_rbi_pct > 5.0. Default false. | CALC |
| `pmo_approval_required` | BOOLEAN | Y | CALC = deviation_flag = true. | CALC |
| `pmo_approved_by` | UUID | N | FK → Users (PMO Director). Required before rate can be used in any transaction if pmo_approval_required = true. | INPUT (PMO Director) |
| `pmo_approved_at` | TIMESTAMP | N | Auto on PMO Director approval | SYSTEM |
| `is_locked` | BOOLEAN | Y | Default false. Auto = true after 24 hours from entered_at. Locked rates cannot be edited. | SYSTEM |
| `is_superseded` | BOOLEAN | Y | Default false. Set true if a newer entry for same currency+date+tier exists. | SYSTEM |
| `entered_by` | UUID | Y | FK → Users (Finance Lead) | SYSTEM |
| `entered_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `used_in_po_count` | INTEGER | Y | CALC — count of POs referencing this rate entry | CALC |
| `used_in_payment_count` | INTEGER | Y | CALC — count of payment transactions referencing this rate entry | CALC |

---

### 3b. Updated Fields — Entity: `PurchaseOrder` (v2.1)

| Field | Change | New Rule | Source |
|-------|--------|----------|--------|
| `po_exchange_rate` | **Source changed: INPUT → LINK** | FK → ForexRateMaster.rate_id. Rate for po_currency on po_date. System fetches closest available rate (±1 business day). If no ForexRateMaster entry exists for po_currency + po_date: PO creation BLOCKED until Finance Lead adds rate. | LINK → ForexRateMaster |
| `po_exchange_rate_id` | **(NEW field)** | UUID. FK → ForexRateMaster. Immutable after PO creation. | LINK → ForexRateMaster |
| `po_exchange_rate` | Retained as DECIMAL | Now populated from ForexRateMaster.exchange_rate. Not free text. | CALC from LINK |

---

### 3b. Updated Fields — Entity: `ForexVariation` (v2.1)

| Field | Change | New Rule | Source |
|-------|--------|----------|--------|
| `payment_exchange_rate` | **Source changed: INPUT → LINK** | FK → ForexRateMaster.rate_id for currency + payment_date. System checks ForexRateMaster. If no entry: payment BLOCKED. | LINK → ForexRateMaster |
| `payment_exchange_rate_id` | **(NEW field)** | UUID. FK → ForexRateMaster. | LINK → ForexRateMaster |
| `payment_exchange_rate` | Retained as DECIMAL | Now populated from ForexRateMaster.exchange_rate. Immutable on GRN confirmation. | CALC from LINK |
| `po_exchange_rate_id` | **(NEW field)** | UUID. FK → ForexRateMaster (PO date rate). For audit chain. | LINK → ForexRateMaster |

---

### 3b. Updated Fields — Entity: `RetentionLedger` (v2.1 — DLP release governance)

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `dlp_period_start` | DATE | N | **(NEW)** Populated on SG-11 passage (from M08 signal). Mandatory when release_type = DLP_End. | LINK → M08 GatePassage |
| `dlp_period_end` | DATE | N | **(NEW)** CALC = dlp_period_start + M01.Contract.dlp_term_days | CALC |
| `dlp_retention_amount` | DECIMAL(15,2) | N | **(NEW)** Portion of total retention held for DLP period. CALC from contract terms. | CALC |
| `dlp_release_eligible` | BOOLEAN | Y | **(NEW)** CALC = (today ≥ dlp_period_end) AND (M04_open_defect_count = 0) AND (M09_open_non_compliance = 0) | CALC |
| `dlp_release_blocked_by` | TEXT | N | **(NEW)** Auto-populated: "X open defects (DLP-003, DLP-007). Y open NABH Non_Compliance observations." Cleared when eligible. | CALC |
| `m04_open_defect_count` | INTEGER | N | **(NEW)** Live count from M04 DLPRegister.open_defect_count. Updated via M04 signal. | LINK → M04 DLPRegister |
| `m09_open_non_compliance` | INTEGER | N | **(NEW)** Live count of open Non_Compliance DLPComplianceObservations from M09. Updated via M09 signal. | LINK → M09 DLPComplianceObservation |

---

## BLOCK 6 — Business Rules (Amendment — new rules v2.1)

*All existing rules BR-06-001 through BR-06-032 from v2.0 remain in force.*

### New Rules: ForexRateMaster Governance (GAP-06)

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---------|---------|-------|--------|------------|
| BR-06-033 | Multi-currency PO creation — `po_currency ≠ INR` | System checks ForexRateMaster for po_currency + po_date (±1 business day tolerance) | If entry exists + not pending PMO approval: auto-link `po_exchange_rate_id`. If entry pending PMO approval: PO creation BLOCKED. If no entry: PO creation BLOCKED. Error: "No confirmed exchange rate for {currency} on {date}. Add to ForexRateMaster first." | 🔴 Real-time |
| BR-06-034 | ForexRateMaster entry created | `deviation_flag` auto-calculated on save | If `deviation_from_rbi_pct > 5.0`: set `pmo_approval_required = true`. Create Decision Queue item: trigger_type = FOREX_DEVIATION_APPROVAL, severity = MEDIUM, owner = PMO Director, SLA = 24hr. Rate cannot be used in any transaction until PMO Director approves. | 🔴 Real-time |
| BR-06-035 | ForexRateMaster `is_locked` check | Scheduled check: set `is_locked = true` when `NOW() > entered_at + 24hr` | Once locked: rate fields (exchange_rate, source_reference, supporting_document_url) cannot be edited. PMO Director can add a superseding entry (new rate_id same currency+date+tier). Old entry: `is_superseded = true`. Active transactions still reference original rate (immutable links). | 🟢 24hr |
| BR-06-036 | Multi-currency PO payment initiated | System checks ForexRateMaster for po_currency + payment_date (±1 business day) | If entry found + confirmed: auto-link payment_exchange_rate_id. If Bank_Transaction entry: verify supporting_document_url not null (uploaded). If no entry or pending approval: payment workflow BLOCKED. | 🔴 Real-time |
| BR-06-037 | ForexVariation computed | After payment_exchange_rate_id linked | forex_gain_loss = (ForexRateMaster[payment_rate_id].exchange_rate − ForexRateMaster[po_rate_id].exchange_rate) × po_amount_foreign. Positive = loss (paid more INR than committed). Negative = gain. | 🔴 Real-time |
| BR-06-038 | `forex_gain_loss > 5% of po_amount_inr` | On ForexVariation record save | Decision record + Finance Lead + PMO Director notification (unchanged from v2.0). Now: also includes both rate_ids in context for audit traceability. | 🔴 Real-time |
| BR-06-039 | ForexRateMaster entry edited after lock | is_locked = true AND edit attempted | BLOCK edit. Return error: "Rate locked — entered {N} hours ago. Create a new entry to supersede." | 🔴 Real-time |

---

### New Rules: DLP Retention Release Governance (GAP-07 downstream)

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---------|---------|-------|--------|------------|
| BR-06-040 | M08 SG-11 gate passage signal received | DLP activation signal: {project_id, sg11_passage_id, dlp_start_date} | Set RetentionLedger.dlp_period_start = dlp_start_date. CALC: dlp_period_end = dlp_start_date + M01.Contract.dlp_term_days. CALC: dlp_retention_amount = (total retention withheld × dlp_retention_split_pct from contract terms). | 🔴 Real-time |
| BR-06-041 | M04 sends open_defect_count update | DLPRegister.open_defect_count changed | Update RetentionLedger.m04_open_defect_count. Recalculate dlp_release_eligible. Update dlp_release_blocked_by text. If now eligible: notify Finance Lead. If newly blocked: notify Finance Lead + PMO Director. | 🔴 Real-time |
| BR-06-042 | M09 sends open_non_compliance update | DLPComplianceObservation count changed | Update RetentionLedger.m09_open_non_compliance. Same recalculation and notification logic as BR-06-041. | 🟡 2-4hr |
| BR-06-043 | DLP retention release requested (Finance Lead initiates) | retention release workflow triggered for release_type = DLP_End | Pre-condition check: (a) today ≥ dlp_period_end (b) m04_open_defect_count = 0 (c) m09_open_non_compliance = 0. If all pass: allow 5-step PaymentWorkflow to proceed. If any fail: BLOCK release. Show dlp_release_blocked_by text. | 🔴 Real-time |
| BR-06-044 | DLP retention release — all pre-conditions met AND 5-step workflow complete | PaymentWorkflow.step_5 = completed | CostLedgerEntry: entry_type = Retention_DLP_Release. TaxLedgerEntry auto-created. AccountingSync stub triggered. RetentionLedger.release_date_dlp populated. M04 DLPRegister.status → Closed (signal sent). | 🔴 Real-time |
| BR-06-045 | PMO Director override: DLP retention release with open defects | pmo_override_dlp_release submitted with reason | Log as governance override. ViolationLog entry created. Require: override_reason min 200 chars + explicit confirmation of legal settlement or disputed waiver. DLPRegister.status NOT auto-closed — PMO Director must separately close in M04. | 🔴 Real-time |
| BR-06-046 | `dlp_retention_split_pct` not set in contract terms at SG-9 | Pre-SG-10 check | Alert to Finance Lead + PMO Director: "DLP retention split not defined in contract terms. Required before SG-11 passage." SG-10 gate criterion added: DLP retention split must be confirmed. | 🟢 24hr |

---

## BLOCK 7 — Integration Points (Amendment)

| Direction | Module | Data Exchanged | Trigger | Speed Tier |
|-----------|--------|---------------|---------|------------|
| RECEIVES FROM | M08 Gate Control | **(NEW v2.1)** DLP activation signal: project_id + sg11_passage_id + dlp_start_date | On SG-11 gate passage | 🔴 Real-time |
| RECEIVES FROM | M04 Execution Capture | **(NEW v2.1)** DLPRegister.open_defect_count update | On DLPDefect status change | 🔴 Real-time |
| RECEIVES FROM | M09 Compliance Tracker | **(NEW v2.1)** Count of open Non_Compliance DLPComplianceObservations | On DLPComplianceObservation status change | 🟡 2-4hr |
| SENDS TO | M04 Execution Capture | **(NEW v2.1)** DLPRegister.status → Closed signal on DLP retention release completion | On BR-06-044 completion | 🔴 Real-time |
| RECEIVES FROM | M05 Risk & Change | Approved VO cost → contract value adjustment (unchanged) | On VO approval | 🔴 Real-time |
| RECEIVES FROM | M04 Execution Capture | material_receipt_id for GRN eligibility (unchanged) | On material receipt | 🔴 Real-time |

---

## BLOCK 9 — Explicit Exclusions (Amendment — additions)

```
[ ] Manage DLP defect records or reinspection tracking      → M04
[ ] Track NABH DLP compliance observations                  → M09
[ ] Trigger DLP Register activation                         → M08 SG-11 passage triggers it; M06 receives signal
[ ] Determine whether DLP defects are resolved              → M04 owns resolution; M06 receives count
[ ] Source or validate exchange rates independently         → ForexRateMaster is the only source
[ ] Accept free-text exchange rate inputs                   → Prohibited from v2.1. All rates via ForexRateMaster.
```

---

## BLOCK 10 — Open Questions

**All questions resolved. Zero open questions.**

| # | Question | Resolution |
|---|----------|-----------|
| 1 | What is `dlp_retention_split_pct`? | A contract term field in M01: what percentage of the total retention is withheld specifically for the DLP period. Standard is 50% of total retention held for DLP (the other 50% released at SG-11/practical completion). Added as mandatory M01 Contract field check at SG-10. |
| 2 | Can RBI reference rates be fetched automatically from an external API? | Not in v2.1 (on-prem constraint — no external API). Finance Lead enters manually with source citation. Future enhancement: scheduled RBI FBIL rate fetch when internet connectivity is confirmed. Rate will still require Finance Lead confirmation before use. |
| 3 | What if NABH Non_Compliance observation is raised after DLP retention was released? | Once released, it cannot be clawed back via EPCC. This is a contractual and legal matter. M09 continues tracking the observation for licensing readiness purposes. PMO Director should ensure NABH clearance before releasing DLP retention. |
| 4 | Partial DLP retention release — is it possible? | Not permitted. DLP retention is all-or-nothing. If PMO Director wants staged release, this must be negotiated as a contract amendment (separate retention tranche structure in M01) before SG-11. |
