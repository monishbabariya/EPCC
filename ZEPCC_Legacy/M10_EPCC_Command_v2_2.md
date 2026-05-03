# M10 — EPCC Command
## Module Specification v2.2
## AMENDMENT — Changed Blocks Only
**Status:** Draft — Pending Review | **Locked:** No
**Spec Author:** PMO Director | **Date:** 2026-05-02
**Reference Standards:** EPCC_Engineering_Standards_v1_1.md
**Base Version:** M10_EPCC_Command_v2.1
**Amendment Scope:** GAP-ANALYSIS-02: Redis dashboard caching specification (TTL per widget type).
                     GAP-ANALYSIS-03: LLM cost and rate governance fields added to
                     NarrativeConfig entity. LLMBudgetLog entity added for cost tracking.

---

## CHANGE LOG

| Version | Date | Change Summary |
|---------|------|----------------|
| v2.0 | 2026-05-02 | Block 10 closed — all questions resolved. Six additional layers. |
| v2.1 | 2026-05-02 | GAP-09: Narrative engine governance. NarrativeGeneration, NarrativeApprovalRecord, NarrativeTemplate entities. |
| v2.2 | 2026-05-02 | GAP-ANALYSIS-02: Redis caching spec — per-widget TTL, cache invalidation rules, cache key standard. GAP-ANALYSIS-03: NarrativeConfig LLM budget fields. LLMBudgetLog entity. BR-10-046 through BR-10-052 added. |

---

## BLOCK 3 — Data Architecture (Amendment)

### 3a. New Entity: `DashboardCacheConfig`

Governs Redis TTL and cache invalidation rules per M10 widget type.
One record per widget type per tenant (configurable by System Admin).
System-shipped defaults applied on tenant provisioning.

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `cache_config_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `widget_type` | ENUM | Y | See widget type table below | INPUT (dropdown) |
| `ttl_seconds` | INTEGER | Y | Min 300 (5 min). Max 86400 (24hr). See defaults below. | INPUT |
| `invalidation_trigger` | ENUM | Y | `TTL_Only / Event_Driven / TTL_And_Event` | INPUT |
| `invalidation_events` | JSONB | N | List of RecalcJob trigger types that force cache flush for this widget. Required if invalidation_trigger ≠ TTL_Only. | INPUT |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |
| `last_updated_by` | UUID | Y | System Admin | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

**Widget type TTL defaults (shipped on tenant creation):**

| Widget Type | Default TTL | Invalidation Trigger | Invalidation Events |
|-------------|-------------|---------------------|---------------------|
| `health_index` | 14,400s (4hr) | TTL_And_Event | REPORT_DATE_CHANGE, EVM_RECALC_COMPLETE, GATE_STATUS_CHANGE |
| `evm_snapshot` | 86,400s (24hr) | TTL_And_Event | EVM_RECALC_COMPLETE, BAC_INTEGRITY_CHANGE |
| `decision_queue` | 300s (5min) | TTL_And_Event | DECISION_QUEUE_ITEM_CREATED, DECISION_QUEUE_ITEM_RESOLVED |
| `cashflow_position` | 86,400s (24hr) | TTL_And_Event | PAYMENT_APPROVED, VO_MATERIALISATION_COMPLETE |
| `portfolio_health` | 14,400s (4hr) | TTL_And_Event | EVM_RECALC_COMPLETE, GATE_STATUS_CHANGE |
| `risk_heatmap` | 14,400s (4hr) | TTL_And_Event | RISK_SCORE_CHANGE, MONTE_CARLO_COMPLETE |
| `milestone_tracker` | 14,400s (4hr) | TTL_And_Event | MILESTONE_STATUS_CHANGE, BASELINE_EXTENSION_APPROVED |
| `gate_readiness` | 14,400s (4hr) | TTL_And_Event | GATE_CRITERION_UPDATED, GATE_STATUS_CHANGE |
| `compliance_dashboard` | 86,400s (24hr) | TTL_And_Event | COMPLIANCE_ITEM_STATUS_CHANGE, NABH_PATHWAY_CHANGE |
| `narrative_panel` | 3,600s (1hr) | TTL_And_Event | NARRATIVE_APPROVED, NARRATIVE_GENERATION_COMPLETE |
| `executive_summary` | 3,600s (1hr) | TTL_Only | — |
| `revenue_readiness` | 14,400s (4hr) | TTL_And_Event | COMPLIANCE_SNAPSHOT_UPDATED, DLP_STATUS_CHANGE |

**Cache key standard:**
```
Format: epcc:{tenant_slug}:{widget_type}:{scope_id}:{user_role}
Examples:
  epcc:kdmc:health_index:project_kdmc-001-dbot:pmo_director
  epcc:kdmc:portfolio_health:portfolio_p001:read_only
  epcc:kdmc:decision_queue:global:pmo_director

Scope types:
  project_{project_code}    → project-scoped widget
  portfolio_{portfolio_id}  → portfolio-scoped widget
  global                    → tenant-wide widget (decision queue, portfolio health)
```

**Cache invalidation flow:**
```
RecalcJob completes
  → RecalcQueue completion handler checks invalidation_events registry
  → For each widget_type with matching invalidation_event:
      → Flush Redis key: epcc:{tenant_slug}:{widget_type}:*
      → Next API request for that widget recalculates from database
      → Fresh value written to Redis with new TTL
```

---

### 3b. Modified Entity: `NarrativeConfig` (v2.2 additions)

*Existing fields from v2.1 remain unchanged.*
*The following fields are ADDED:*

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `monthly_llm_budget_inr` | DECIMAL(10,2) | Y | **(NEW v2.2)** Maximum INR spend on LLM API calls for narratives for this project per calendar month. Default ₹500. Range: ₹100–₹50,000. PMO Director configurable. | INPUT |
| `max_tokens_per_call` | INTEGER | Y | **(NEW v2.2)** Maximum tokens per single LLM narrative generation call (input + output combined). Default 4,000. Range: 1,000–8,000. Prevents runaway costs on a single call. | INPUT |
| `llm_timeout_seconds` | INTEGER | Y | **(NEW v2.2)** Maximum seconds to wait for LLM API response before timeout. Default 30. Range: 10–120. On timeout: generation fails gracefully, `NarrativeGeneration.status = Failed_Timeout`. Template fallback activates. | INPUT |
| `llm_fallback_on_failure` | BOOLEAN | Y | **(NEW v2.2)** If true: on any LLM failure (timeout, API error, budget exhaustion), automatically generate narrative using Phase 1 template engine. If false: generation fails and requires manual retry. Default true. | INPUT |
| `budget_alert_threshold_pct` | DECIMAL(4,3) | Y | **(NEW v2.2)** Send budget alert when monthly LLM spend reaches this % of `monthly_llm_budget_inr`. Default 0.80 (80%). | INPUT |
| `budget_hard_stop` | BOOLEAN | Y | **(NEW v2.2)** If true: LLM calls blocked when monthly budget is exhausted. Template fallback activates. If false: calls continue but CRITICAL alert sent. Default true. | INPUT |

---

### 3c. New Entity: `LLMBudgetLog`

Tracks LLM API spend per project per month for cost governance.

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `budget_log_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | LINK → M01 Project |
| `budget_month` | DATE | Y | First day of the calendar month. e.g., 2026-05-01 | SYSTEM |
| `module_source` | ENUM | Y | `M10_Narrative / PIOE_Extraction` | SYSTEM |
| `total_calls` | INTEGER | Y | Count of LLM API calls in the month | SYSTEM |
| `total_tokens_in` | INTEGER | Y | Cumulative input tokens | SYSTEM |
| `total_tokens_out` | INTEGER | Y | Cumulative output tokens | SYSTEM |
| `total_cost_inr` | DECIMAL(10,2) | Y | Total INR cost. Calculated from `LLMCallLog` records. | CALC |
| `budget_limit_inr` | DECIMAL(10,2) | Y | Snapshot of `NarrativeConfig.monthly_llm_budget_inr` at time of log creation | LINK |
| `budget_utilisation_pct` | DECIMAL(5,4) | Y | CALC: total_cost_inr / budget_limit_inr | CALC |
| `budget_alert_sent` | BOOLEAN | Y | True if alert was sent when utilisation crossed threshold | SYSTEM |
| `budget_hard_stopped` | BOOLEAN | Y | True if LLM calls were blocked due to budget exhaustion | SYSTEM |
| `last_updated_at` | TIMESTAMP | Y | Updated after each LLM call in the month | SYSTEM |

*Note: LLMBudgetLog is complementary to `LLMCallLog` (defined in ES-SEC-005).
LLMCallLog = per-call record. LLMBudgetLog = monthly aggregate per project.*

---

## BLOCK 6 — Business Rules (Amendment)

*All existing rules BR-10-001 through BR-10-045 from v2.1 remain in force.*
*The following rules are ADDED in v2.2:*

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---------|---------|-------|--------|------------|
| BR-10-046 | API request for any M10 dashboard widget | Before database query | Check Redis cache key for this widget+scope+role. If cache hit and not expired: return cached value. If cache miss or expired: query database, compute value, write to Redis with TTL from DashboardCacheConfig. | 🔴 Real-time |
| BR-10-047 | RecalcJob completes with event type matching a widget's `invalidation_events` | On RecalcQueue completion handler | Flush all Redis keys matching: `epcc:{tenant_slug}:{widget_type}:*`. This ensures the next dashboard load reflects the fresh calculation. | 🔴 Real-time |
| BR-10-048 | LLM API call initiated for NarrativeGeneration | Before LLM API request | Check: (1) `budget_hard_stop = true` AND `LLMBudgetLog.budget_utilisation_pct ≥ 1.0` → Block call. If `llm_fallback_on_failure = true`: activate template engine. (2) `budget_utilisation_pct ≥ budget_alert_threshold_pct` → Send budget alert to PMO Director (non-blocking). | 🔴 Real-time |
| BR-10-049 | LLM API call completes (success or failure) | On LLMGateway response | Write `LLMCallLog` entry (ES-SEC-005). Update `LLMBudgetLog` for project+month: increment total_calls, total_tokens_in, total_tokens_out, total_cost_inr. Recalculate budget_utilisation_pct. | 🔴 Real-time |
| BR-10-050 | LLM API call times out (elapsed > `llm_timeout_seconds`) | On LLMGateway timeout | Set `NarrativeGeneration.status = Failed_Timeout`. If `llm_fallback_on_failure = true`: immediately trigger template engine generation. Log timeout event. If timeout rate for this project > 3 in 24hr: MEDIUM alert to System Admin (LLM API degraded). | 🔴 Real-time |
| BR-10-051 | LLM monthly budget exhausted (`budget_utilisation_pct ≥ 1.0`) | On LLMBudgetLog update | Set `LLMBudgetLog.budget_hard_stopped = true` (if hard_stop = true). CRITICAL alert to PMO Director: "LLM narrative budget exhausted for {project_code}. Template engine active for remainder of month." M10 narrative panel badge: "LLM Budget Exhausted — Template Mode Active". | 🔴 Real-time |
| BR-10-052 | First day of new calendar month | Celery Beat — 12:05am IST on 1st of month | Create new `LLMBudgetLog` record for each active project with `budget_hard_stopped = false`. Previous month's log is sealed (read-only). Budget resets. LLM calls unblocked. | 🟢 24hr |

---

## BLOCK 7 — Integration Points (Amendment)

| Direction | Module | Data Exchanged | Trigger | Speed Tier |
|-----------|--------|---------------|---------|------------|
| INTERNAL | Redis | Cache key read/write per widget | Every M10 dashboard API request | 🔴 Real-time |
| INTERNAL | Redis | Cache flush per widget type | RecalcJob completion with matching event | 🔴 Real-time |
| INTERNAL | LLMGateway service | LLM API call via ES-SEC-005 gateway | NarrativeGeneration request | 🔴 Real-time |
| SENDS TO | LLMBudgetLog | Cost + token data | After every LLM call | 🔴 Real-time |

---

## BLOCK 9 — Explicit Exclusions (Amendment — additions)

```
[ ] Cache financial transaction data in Redis              → Redis is KPI cache only; source of truth is PostgreSQL
[ ] Store narrative text in Redis                          → Narrative text in PostgreSQL (NarrativeGeneration entity)
[ ] Access LLM APIs directly (bypass LLMGateway)          → All LLM calls must route through ES-SEC-005 LLMGateway
[ ] Override LLM budget mid-month without PMO Director     → Budget changes require PMO Director approval + AuditLog
```

---

## BLOCK 10 — Open Questions

**All v2.2 questions resolved. Zero open questions.**

| # | Question | Resolution |
|---|----------|-----------|
| 1 | Should Redis cache be per-user or per-role? | Per-role. Individual user-level caching would create too many cache keys and negate cache efficiency. Role is the correct granularity — a Read-Only user sees the same data as another Read-Only user for the same scope. Sensitive field masking (ES-SEC-004) is applied at API serialisation layer before caching, so cached values are already role-appropriate. |
| 2 | What is the LLM cost calculation basis for `total_cost_inr`? | Based on published API pricing stored in `SystemConfig` table as `llm_cost_per_1k_tokens_inr` per model. Updated by System Admin when pricing changes. LLMGateway calculates cost per call: `(tokens_in + tokens_out) / 1000 × rate`. Exchange rate from ForexRateMaster if USD-denominated pricing. |
| 3 | Is the default ₹500/month budget sufficient? | For M10 narratives (one per project per reporting period, ~1,000 tokens per generation): approximately 200 narrative generations per month. For a project with monthly reporting, this is more than sufficient. PMO Director can increase per-project as needed. |

---

*Amendment complete. Pending PMO Director review.*
*LLMGateway service definition resides in ES-SEC-005 (EPCC_Engineering_Standards_v1_1.md).*
