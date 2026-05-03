# PIOE — Portfolio Investment Optimisation Engine
## Module Specification v2.1
## AMENDMENT — Changed Blocks Only
**Status:** Draft — Pending Review | **Locked:** No
**Spec Author:** PMO Director | **Date:** 2026-05-02
**Reference Standards:** EPCC_Engineering_Standards_v1_1.md
**Base Version:** PIOE_Spec_v2.0
**Amendment Scope:** GAP-ANALYSIS-03: LLM cost, rate, and timeout governance fields added to
                     ExtractionModelConfig entity. ExtractionBudgetLog entity added.
                     Alignment with LLMGateway service (ES-SEC-005) and LLMBudgetLog
                     pattern established in M10_v2.2.

---

## CHANGE LOG

| Version | Date | Change Summary |
|---------|------|----------------|
| v1.0 | 2026-04-30 | Initial draft |
| v2.0 | 2026-04-30 | Block 10 resolved: hybrid AI extraction; IRR soft penalty; live M01 resource data; multi-objective MILP weighted sum |
| v2.1 | 2026-05-02 | GAP-ANALYSIS-03: ExtractionModelConfig LLM governance fields. ExtractionBudgetLog entity. BR-PIOE-NEW-001 through BR-PIOE-NEW-004 added. LLMGateway integration formalised. |

---

## BLOCK 3 — Data Architecture (Amendment)

### 3a. Modified Entity: `ExtractionModelConfig` (v2.1 additions)

*Existing fields from v2.0 remain unchanged.*
*The following fields are ADDED:*

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `max_tokens_per_call` | INTEGER | Y | **(NEW v2.1)** Maximum tokens per single extraction call (input + output combined). Default 8,000 (document extraction requires larger context than narratives). Range: 2,000–32,000. | INPUT |
| `llm_timeout_seconds` | INTEGER | Y | **(NEW v2.1)** Maximum seconds to wait for LLM API response. Default 60. Range: 30–300. Document extraction is slower than narrative generation — longer timeout appropriate. On timeout: extraction attempt status = Failed_Timeout. Manual retry required (no auto-fallback — document extraction requires human review of output regardless). | INPUT |
| `monthly_budget_inr` | DECIMAL(10,2) | Y | **(NEW v2.1)** Maximum INR spend on LLM extraction calls per calendar month across all documents. Default ₹2,000. Range: ₹500–₹100,000. PMO Director / System Admin configurable. | INPUT |
| `budget_alert_threshold_pct` | DECIMAL(4,3) | Y | **(NEW v2.1)** Send budget alert at this % of monthly_budget_inr. Default 0.75 (75%). | INPUT |
| `budget_hard_stop` | BOOLEAN | Y | **(NEW v2.1)** If true: extraction calls blocked when budget exhausted. Manual document extraction workflow activates (human enters fields directly). Default true. | INPUT |
| `max_concurrent_extractions` | INTEGER | Y | **(NEW v2.1)** Maximum simultaneous document extraction calls. Prevents API rate limit breaches and cost spikes from bulk uploads. Default 3. Range: 1–10. | INPUT |
| `retry_on_low_confidence` | BOOLEAN | Y | **(NEW v2.1)** If true: fields with confidence < `confidence_threshold` trigger one automatic re-extraction with refined prompt before flagging for human review. Default false (re-extraction doubles cost; human review is preferred). | INPUT |

---

### 3b. New Entity: `ExtractionBudgetLog`

Tracks LLM API spend for document extraction per calendar month.
Mirrors the LLMBudgetLog pattern in M10 v2.2 but scoped to PIOE extraction.

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `budget_log_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `budget_month` | DATE | Y | First day of calendar month | SYSTEM |
| `total_documents_processed` | INTEGER | Y | Count of documents with completed extraction | SYSTEM |
| `total_calls` | INTEGER | Y | Total LLM API calls (may exceed documents — retries counted) | SYSTEM |
| `total_tokens_in` | INTEGER | Y | Cumulative input tokens | SYSTEM |
| `total_tokens_out` | INTEGER | Y | Cumulative output tokens | SYSTEM |
| `total_cost_inr` | DECIMAL(10,2) | Y | CALC from LLMCallLog | CALC |
| `budget_limit_inr` | DECIMAL(10,2) | Y | Snapshot of ExtractionModelConfig.monthly_budget_inr | LINK |
| `budget_utilisation_pct` | DECIMAL(5,4) | Y | CALC: total_cost_inr / budget_limit_inr | CALC |
| `failed_timeout_count` | INTEGER | Y | Count of calls that timed out | SYSTEM |
| `budget_alert_sent` | BOOLEAN | Y | True if threshold alert was sent | SYSTEM |
| `budget_hard_stopped` | BOOLEAN | Y | True if extraction was blocked due to budget exhaustion | SYSTEM |
| `last_updated_at` | TIMESTAMP | Y | Updated after each extraction call | SYSTEM |

---

### 3c. Modified Entity: `DocumentExtractionResult` (v2.1 additions)

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `extraction_cost_inr` | DECIMAL(8,4) | Y | **(NEW v2.1)** Cost of LLM call(s) for this document's extraction. CALC from LLMCallLog. | CALC |
| `tokens_consumed` | INTEGER | Y | **(NEW v2.1)** Total tokens (in + out) for this document's extraction. | SYSTEM |
| `extraction_attempts` | INTEGER | Y | **(NEW v2.1)** Number of LLM calls made for this document (1 = first attempt succeeded; >1 = retry occurred). | SYSTEM |
| `timed_out` | BOOLEAN | Y | **(NEW v2.1)** True if any extraction attempt timed out. | SYSTEM |
| `llm_call_ids` | JSONB | Y | **(NEW v2.1)** Array of LLMCallLog UUIDs for this document. Enables full cost traceability per document. | LINK |

---

## BLOCK 6 — Business Rules (Amendment)

*All existing PIOE rules from v2.0 remain in force.*
*The following rules are ADDED in v2.1:*

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---------|---------|-------|--------|------------|
| BR-PIOE-NEW-001 | Document extraction initiated | Before LLM API call via LLMGateway | Check: (1) `budget_hard_stop = true` AND `ExtractionBudgetLog.budget_utilisation_pct ≥ 1.0` → Block extraction. Return: "Monthly extraction budget exhausted. Manual field entry required or contact PMO Director to increase budget." (2) Active concurrent extractions ≥ `max_concurrent_extractions` → Queue extraction. Return: "Extraction queued. {N} document(s) ahead of this one." | 🔴 Real-time |
| BR-PIOE-NEW-002 | LLM extraction call completes | On LLMGateway response | Update DocumentExtractionResult (cost, tokens, attempts). Update ExtractionBudgetLog (increment all counters). If budget_utilisation_pct ≥ budget_alert_threshold_pct: send MEDIUM alert to PMO Director / System Admin. | 🔴 Real-time |
| BR-PIOE-NEW-003 | Extraction call times out | On LLMGateway timeout (elapsed > llm_timeout_seconds) | Set DocumentExtractionResult.timed_out = true. Set extraction status = Failed_Timeout. Do NOT auto-retry (document extraction requires human review — silent retry risks cost with poor output). Alert Portfolio Manager: "Document extraction timed out: {document_name}. Please retry or enter fields manually." | 🔴 Real-time |
| BR-PIOE-NEW-004 | First day of new calendar month | Celery Beat — 12:10am IST on 1st of month | Create new ExtractionBudgetLog for the new month. Previous month log sealed. Budget resets. Hard stop (if active) lifted. | 🟢 24hr |

---

## BLOCK 7 — Integration Points (Amendment)

| Direction | Module | Data Exchanged | Trigger | Speed Tier |
|-----------|--------|---------------|---------|------------|
| SENDS TO (NEW v2.1) | LLMGateway service (ES-SEC-005) | Document content (PII-scrubbed), extraction prompt, model config | On document extraction initiation | 🔴 Real-time |
| RECEIVES FROM (NEW v2.1) | LLMGateway service | Extraction result, tokens consumed, cost_inr, call_id | On LLM API response | 🔴 Real-time |
| SENDS TO (NEW v2.1) | ExtractionBudgetLog | Cost + token data per call | After every extraction call | 🔴 Real-time |

---

## BLOCK 9 — Explicit Exclusions (Amendment — additions)

```
[ ] Call LLM APIs directly (bypass LLMGateway)            → All LLM calls route through ES-SEC-005 LLMGateway
[ ] Auto-approve extracted data without human review       → Human review is mandatory regardless of confidence score
[ ] Send exact financial figures to LLM APIs              → LLMGateway rounds to nearest ₹1 Cr (ES-SEC-005)
[ ] Share tenant name or project codes with LLM APIs      → LLMGateway substitutes generic labels (ES-SEC-005)
```

---

## BLOCK 10 — Open Questions

**All v2.1 questions resolved. Zero open questions.**

| # | Question | Resolution |
|---|----------|-----------|
| 1 | Why is `retry_on_low_confidence` default false when re-extraction could improve accuracy? | Re-extraction doubles the cost of that document and still requires human review. The human reviewer can request a manual re-extraction after seeing the confidence-flagged output. Auto-retry without human judgement wastes budget on documents where the issue may be in the source document quality, not the prompt. Default false is the conservative, budget-safe position. PMO Director can enable per config if needed. |
| 2 | How is `max_concurrent_extractions` enforced technically? | A Redis counter `epcc:{tenant_slug}:pioe:active_extractions` is incremented before each extraction call and decremented on completion (success or failure). Before initiating, check counter ≥ max_concurrent_extractions → queue. Redis atomic increment (INCR command) ensures race-condition-safe enforcement. |
| 3 | Should ExtractionBudgetLog be per-cycle or per-month? | Per-month. Optimisation cycles do not align cleanly with calendar months, and cost governance is a financial control that aligns with monthly budget cycles. Cycle-level cost is derivable by filtering LLMCallLog by cycle dates. Monthly is the correct primary aggregation. |

---

*Amendment complete. Pending PMO Director review.*
*LLMGateway service architecture defined in ES-SEC-005 (EPCC_Engineering_Standards_v1_1.md).*
*ExtractionBudgetLog and M10 LLMBudgetLog are sibling entities — same pattern, different scope.*
