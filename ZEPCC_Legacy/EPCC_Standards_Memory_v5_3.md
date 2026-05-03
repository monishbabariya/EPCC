# EPCC — Standards Memory v5.3
## AMENDMENT FILE — Additions to v5.2
**Purpose:** Documents all additions and changes made to EPCC_Standards_Memory v5.2.
Apply to v5.2 to produce the complete v5.3.

**Version:** v5.3 | **Date:** 2026-05-02
**Changes:** Gap analysis verification completed. Engineering Standards advanced to v1.2.
             Nine gap refinements implemented across standards and three module specs.
             Multi-tenant architecture challenge resolved. Deployment tier strategy locked.
             Sections §7.121–§7.137 added.

---

## CHANGE LOG ADDITION (append to v5.2)

| Version | Date | Change Summary |
|---------|------|----------------|
| v5.3 | 2026-05-02 | Gap analysis verified (56% false, 39% partial, 5% valid). Engineering Standards v1.1: ES-DB-008 (Alembic), ES-DB-009 (HDI staging), ES-BL-006 (Celery DLQ), ES-DR-001/002 (DR/RPO-RTO), ES-CICD-001/002 (GitHub Actions), ES-SEC-004/005 (DPDPA 2023 + LLM gateway). Engineering Standards v1.2: ES-DR-002 per-schema backup. M04 v2.1: captured_at field. M10 v2.2: Redis caching + LLM budget governance. PIOE v2.1: LLM governance. Deployment Tier Specification v1.0: Tier 1 / Tier 2. ES-DB-001 confirmed and closed. §7.121–§7.137 added. |

---

## FILE REGISTRY UPDATE

*(Replaces prior file registry entries for these files)*

| File | Module / Purpose | Version (Previous → Current) |
|------|-----------------|-------------------------------|
| `EPCC_Engineering_Standards_v1_2.md` | Engineering Standards | v1.0 → **v1.2** |
| `M04_Execution_Capture_v2_1.md` | Execution Capture | v2.0 → **v2.1** |
| `M10_EPCC_Command_v2_2.md` | EPCC Command | v2.1 → **v2.2** |
| `PIOE_Spec_v2_1.md` | Portfolio Investment Optimisation Engine | v2.0 → **v2.1** |
| `EPCC_Deployment_Tier_Specification_v1_0.md` | Deployment Tier Strategy | **NEW — v1.0** |

*All other module specs unchanged. M01 v2.1, M02 v2.0, M03 v2.3, M05 v2.3, M06 v2.1, M07 v3.0, M08 v2.1, M09 v2.1 remain current.*

---

## 1. GAP ANALYSIS — VERIFICATION OUTCOME (§7.121 – §7.122)

---

### §7.121 — Gap Analysis Verification Summary

```
A 36-item gap analysis document was submitted for EPCC.
Full verification was conducted against all spec files and engineering standards.

VERDICT BREAKDOWN:
  20 gaps (56%) — FALSE: Already fully addressed in existing specs.
                  Acting on these would add unnecessary complexity.
  14 gaps (39%) — PARTIAL: Real but narrower than claimed. Refinements applied.
   2 gaps  (5%) — VALID: Genuinely absent. Addressed in this session.

GENUINELY VALID GAPS (acted on):
  GAP-V1: No CI/CD pipeline defined
          → ES-CICD-001/002: GitHub Actions 7-stage pipeline locked (v1.1)
  GAP-V2: External system integrations (ERP/IoT/BIM) not defined
          → Deferred to Phase 2. IntegrationAdapterSpec to be produced at Phase 2 planning.

INVALID GAPS (do not act on):
  System architecture, auth/RBAC, error handling, backend stack, test strategy,
  environment strategy, data seeding, optimistic locking, audit logging,
  async processing design, BAC integrity SSOT, encryption, deployment architecture.
  All of these were already fully specified in ES-DB-001 through ES-TEST-004.

KEY LESSON:
  The gap analysis was produced without reading EPCC_Engineering_Standards_v1_0.md.
  Any future gap analysis or external review must be cross-checked against both
  the module specs AND the engineering standards before any action is taken.
  Do NOT implement gap recommendations without verification first.
```

---

### §7.122 — Gap Analysis Rejected Document

```
A second document was submitted: "EPCC Multi-Tenant Database Architecture"
proposing a Hybrid Multi-Tenant Architecture with dedicated databases per tenant.

VERDICT: REJECTED IN FULL. DO NOT IMPLEMENT.

Conflicts with locked decisions:
  1. Database-per-tenant vs Schema-per-tenant (ES-DB-001) — fundamental architecture conflict
  2. Flyway/Liquibase vs Alembic (ES-DB-008) — wrong migration tooling for Python stack
  3. Snowflake/BigQuery/Redshift vs DuckDB — wrong analytics stack (on-prem constraint)
  4. RPO 15min / RTO 1hr vs RPO 24hr / RTO 4hr (ES-DR-001) — targets without deployment context
  5. PgBouncer vs SQLAlchemy pooling — unnecessary complexity at current scale
  6. Node/Java vs Python + FastAPI — wrong backend language

Document appears to be generic AI-generated architecture content not written
for EPCC. It was not reviewed against the existing EPCC engineering standards.

ES-DB-001 (schema-per-tenant) is CONFIRMED and CLOSED as a result of this review.
The rationale in ES-DB-001 stands: at ≤50 tenants, schema isolation is technically
equivalent to database isolation with significantly lower operational overhead.
```

---

## 2. ENGINEERING STANDARDS v1.1 — NEW LOCKED DECISIONS (§7.123 – §7.130)

---

### §7.123 — Alembic Migration Tooling (ES-DB-008)

```
LOCKED: Alembic is the mandatory migration tool for all PostgreSQL schema changes.

Migration directory: /migrations/{module_id}/
Naming: {timestamp}_{description}.py
  e.g.: 20260502_1430_m07_add_tcpi_infeasibility_flag.py

All rules:
  - Every DDL change requires an Alembic migration file — no ad-hoc DDL
  - Both upgrade() and downgrade() functions required (v1.1)
    NOTE: This overrides ES-DB-006 (v1.0) which stated forward-only.
    v1.1 requires downgrade() for all migrations going forward.
    Existing v1.0 migrations are grandfathered.
  - Tenant-aware: loop over all active tenant schemas per migration
  - CI linter (ES-CICD-001) fails build if:
      New table missing BaseModel mixin columns
      Migration has no downgrade()
  - Production migration window: Saturday 10pm–2am IST (unchanged)
  - Staging must run migration before production (unchanged)
```

---

### §7.124 — HDI Staging Pattern (ES-DB-009)

```
LOCKED: All Historical Data Imports use validate-then-promote pattern.

Stages:
  1. LAND    → raw data to hdi_staging_{entity} tables (no FK enforcement)
  2. VALIDATE → full business rule + FK chain validation per row
  3. PROMOTE  → single transaction: staging → live tables
  4. ROLLBACK → on any failure, entire transaction rolls back

Rules:
  - 100% valid rows required before promotion. No partial promotion.
  - Staging tables preserved 48hr on failure for human review.
  - HDIJobLog entity tracks all stages.
  - PMO Director only can initiate HDI (RBAC enforced).
  - Complements existing §7.109–§7.114 HDI governance. This standard
    adds the technical staging infrastructure those sections assumed.

Relationship to existing HDI spec:
  EPCC_HistoricalDataImport_v1_0.md governs the business logic.
  ES-DB-009 governs the technical execution pattern.
  Both apply. Neither supersedes the other.
```

---

### §7.125 — Celery Dead Letter Queue Standard (ES-BL-006)

```
LOCKED: Every Celery queue has a corresponding Dead Letter Queue (DLQ).
No task failure is silent.

Queue → DLQ mapping:
  recalc_immediate    → dlq_recalc_immediate   (3 retries, exp backoff: 30/60/120s)
  recalc_standard     → dlq_recalc_standard    (5 retries, exp backoff: 5m/15m/30m/1hr/2hr)
  recalc_slow         → dlq_recalc_slow        (3 retries, fixed: 2hr intervals)
  notifications       → dlq_notifications      (5 retries, exp backoff: 1m/5m/15m/30m/1hr)
  hdi_jobs            → dlq_hdi_jobs           (0 retries — HDI failures require human review)
  reporting           → dlq_reporting          (3 retries, fixed: 30m intervals)

RecalcJob entity additions:
  retry_count, max_retry_count, last_failure_reason, last_failed_at,
  dlq_routed_at, dlq_resolved_at, dlq_resolved_by

Alert rules:
  dlq_recalc_immediate entry → CRITICAL to PMO Director + System Admin (5min)
  dlq_recalc_standard/slow   → HIGH (2hr window)
  dlq_notifications           → MEDIUM
  DLQ items never auto-retried. Human resolution required with note (min 50 chars).
```

---

### §7.126 — Disaster Recovery Standard (ES-DR-001 / ES-DR-002)

```
LOCKED:
  RPO: 24 hours (Phase 1 on-prem)
  RTO: 4 hours  (Phase 1 on-prem)

Phase roadmap:
  Phase 1 (now):  Daily pg_dump to MinIO. Weekly offsite. Quarterly drill. RPO=24hr RTO=4hr.
  Phase 2 (cloud): Point-in-time recovery. RPO→5min.
  Phase 3 (scale): Multi-region. Active-passive. RTO→15min.

Daily backup procedure — TWO operations (v1.2 addition):
  OP 1: Full instance pg_dump → MinIO backups/full/{date}/ (30-day retention)
  OP 2: Per-tenant pg_dump --schema=tenant_{slug} → MinIO backups/tenants/{slug}/{date}/
        (90-day retention). Staggered starts, 5min apart from 2:10am IST.

Per-tenant restore (surgical — zero impact on other tenants):
  DROP SCHEMA tenant_{slug} CASCADE → pg_restore → Alembic migrate → validate → restart.
  Other tenants: unaffected, no downtime.

Restore drill: quarterly. Logged in SystemLog (event_type = DR_DRILL).
Backup bucket: epcc-backups (separate from epcc-datalake). System Admin access only.
```

---

### §7.127 — CI/CD Pipeline Standard (ES-CICD-001 / ES-CICD-002)

```
LOCKED: GitHub Actions is the mandatory CI/CD platform.

7-stage pipeline (runs on every PR and merge to main):
  Stage 1: Lint         → Ruff (Python) + mypy (strict) + ESLint (React)
  Stage 2: Migration    → Alembic check + BaseModel mixin linter + downgrade() check
  Stage 3: Unit Tests   → pytest, 100% BR coverage required, BR-XX-YYY test naming
  Stage 4: Integration  → All API endpoints (happy + unhappy + 403 + idempotency + rollback)
  Stage 5: Docker Build → Build + tag (git SHA) + push to registry
  Stage 6: Staging      → Auto-deploy to staging on merge to main + smoke tests
  Stage 7: Production   → Manual approval gate. Migration window enforced (Saturday 10pm–2am IST).

Versioning: Semantic (MAJOR.MINOR.PATCH).
  MAJOR: breaking API change.  MINOR: new feature/BR.  PATCH: bug fix.
  Every production deploy → GitHub Release with migration list + BR changes.
  SystemConfig.current_version updated on every production deploy.
```

---

### §7.128 — Data Privacy Standard — DPDPA 2023 (ES-SEC-004)

```
LOCKED: India's Digital Personal Data Protection Act 2023 (DPDPA 2023) is the
applicable data privacy regulation for EPCC. HIPAA does not apply.

Three-tier data classification:
  Class 1 — PERSONAL:     Identifies a natural person (name, email, phone)
                           Column-level encryption. Masked for all roles except
                           owner + PMO Director. Anonymised on project closure.
                           Retained only as long as purpose requires (DPDPA).
  Class 2 — FINANCIAL:    Commercial-in-confidence financial data (rates, amounts, EAC)
                           Column-level encryption (ES-SEC-003 unchanged).
                           Masked for Read-Only role. Retained 7 years (Companies Act).
  Class 3 — OPERATIONAL:  Project operational data (progress %, dates, scores)
                           Table-level TDE. No masking. Retained project lifetime + 7 years.

Enforcement: SQLAlchemy column info metadata. Masking at API serialisation layer (Pydantic).
PMO Director is designated Data Fiduciary for DPDPA purposes.
PrivacyRequestLog entity: tracks all DPDPA access/correction/erasure requests.
Erasure = anonymisation (replaces personal fields with [ANONYMISED_{timestamp}]).
UUID preserved for referential integrity.
```

---

### §7.129 — LLM Gateway Standard (ES-SEC-005)

```
LOCKED: All LLM API calls (M10 Narrative Engine + PIOE document extraction)
route through a single LLMGateway service. No module calls LLM APIs directly.

LLMGateway enforces before every call:
  - Tenant isolation: system prompt prefix per tenant
  - PII scrubbing: personal fields replaced with generic labels
  - Financial rounding: exact figures rounded to nearest ₹1 Cr labelled "approximate"
  - Tenant/project anonymisation: CLIENT_A, PROJECT_1 labels replace real names

LLMCallLog entity: tenant_id (not sent to API), model, token_in, token_out, cost_inr,
  prompt_hash, response_hash, timestamp. Full prompt/response in MinIO (encrypted, Class 2).

Cross-tenant contamination detection: if LLM response contains another tenant_id →
  CRITICAL alert + LLM calls suspended for that tenant pending investigation.
```

---

### §7.130 — Observability Stack Standard (ES-OBS — ES-DEPLOY-001 update)

```
LOCKED: Observability stack added to Docker Compose (v1.1):
  loki:           Grafana Loki — log aggregation
  promtail:       Log shipper (Docker logs → Loki)
  prometheus:     Metrics scraping (FastAPI /metrics + Celery)
  grafana:        Unified dashboard (logs + metrics + alerts)
  otel-collector: OpenTelemetry Collector — distributed tracing

Mandatory Grafana alerts (configured on first deployment):
  API 5xx > 1% over 5min     → CRITICAL
  Any DLQ entry              → HIGH
  PG connections > 80% pool  → HIGH
  API p95 latency > 2s       → HIGH
  Volume > 80%               → MEDIUM
  recalc_immediate depth > 50 → MEDIUM

Log format: JSON structured logging per ES-CODE-003 (unchanged).
```

---

## 3. MODULE AMENDMENTS v5.3 (§7.131 – §7.134)

---

### §7.131 — M04 v2.1: captured_at Field Standard

```
LOCKED: ProgressEntry, MaterialReceipt, QAChecklist, ContractorScorecard all
require a captured_at timestamp distinct from created_at.

captured_at: when data was physically measured/observed on-site.
created_at:  when data was entered into the EPCC system. (unchanged system field)
submission_lag_hours: CALC = (created_at − captured_at) in hours.
submission_lag_flag:  CALC = true if lag > 72 hours.

Business rules:
  BR-04-NEW-001: lag > 72hr → LOW Decision Queue item to Project Director (informational)
  BR-04-NEW-002: captured_at > 14 days old → entry blocked. LateEntryOverride required.
  BR-04-NEW-003: M07 uses captured_at (not created_at) as effective EV period anchor.

Cross-module impact:
  M07: RecalcJob effective_date = ProgressEntry.captured_at. M07 spec amendment required.
  M03: actual_delivery_date for procurement milestones = MaterialReceipt.captured_at. M03 amendment required.

New entity: LateEntryOverride — PMO Director only, min 100 char reason, max 24hr turnaround.
```

---

### §7.132 — M10 v2.2: Redis Dashboard Caching Standard

```
LOCKED: M10 React dashboard uses Redis caching with per-widget TTL.

New entity: DashboardCacheConfig — one record per widget type per tenant.
Cache key format: epcc:{tenant_slug}:{widget_type}:{scope_id}:{user_role}

Widget TTL defaults:
  decision_queue:    300s (5min)   — event-driven invalidation
  health_index:      14,400s (4hr) — event-driven invalidation
  portfolio_health:  14,400s (4hr) — event-driven invalidation
  milestone_tracker: 14,400s (4hr) — event-driven invalidation
  risk_heatmap:      14,400s (4hr) — event-driven invalidation
  gate_readiness:    14,400s (4hr) — event-driven invalidation
  revenue_readiness: 14,400s (4hr) — event-driven invalidation
  narrative_panel:   3,600s (1hr)  — event-driven invalidation
  executive_summary: 3,600s (1hr)  — TTL only
  evm_snapshot:      86,400s (24hr) — event-driven invalidation
  cashflow_position: 86,400s (24hr) — event-driven invalidation
  compliance_dash:   86,400s (24hr) — event-driven invalidation

Cache invalidation: RecalcQueue completion handler flushes
  epcc:{tenant_slug}:{widget_type}:* for all widgets with matching invalidation_events.

Role caching: per-role (not per-user). Masking applied at API serialisation before caching.
```

---

### §7.133 — M10 v2.2 + PIOE v2.1: LLM Budget Governance Standard

```
LOCKED: LLM cost and rate governance is mandatory on all LLM-consuming entities.

NarrativeConfig additions (M10):
  monthly_llm_budget_inr:      Max INR/month for LLM narrative calls. Default ₹500.
  max_tokens_per_call:         Default 4,000. Range 1,000–8,000.
  llm_timeout_seconds:         Default 30. On timeout: template fallback activates.
  llm_fallback_on_failure:     Default true. Template engine activates on any LLM failure.
  budget_alert_threshold_pct:  Default 80%. Alert at this % of budget.
  budget_hard_stop:            Default true. Blocks LLM calls at 100% budget utilisation.

ExtractionModelConfig additions (PIOE):
  Same fields with adjusted defaults:
    max_tokens_per_call: 8,000 (documents need larger context)
    llm_timeout_seconds: 60 (document extraction slower than narratives)
    monthly_budget_inr: ₹2,000
    max_concurrent_extractions: 3 (prevents rate limit breaches on bulk uploads)
    retry_on_low_confidence: false (human review preferred over auto-retry cost)

New entities:
  LLMBudgetLog (M10): monthly aggregate per project — total calls, tokens, cost, utilisation.
  ExtractionBudgetLog (PIOE): same pattern scoped to document extraction.
  Both reset on 1st of each month (Celery Beat).

Budget exhaustion flow:
  budget_utilisation_pct ≥ 1.0 AND budget_hard_stop = true
    → LLM calls blocked → template/manual fallback → CRITICAL alert to PMO Director
    → M10 badge: "LLM Budget Exhausted — Template Mode Active"
    → Resets automatically on 1st of next month
```

---

### §7.134 — PIOE v2.1: LLMGateway Integration Formalised

```
LOCKED: PIOE document extraction now formally routes through LLMGateway (ES-SEC-005).

All rules from ES-SEC-005 apply to PIOE extraction calls:
  - PII scrubbing before send
  - Financial rounding to nearest ₹1 Cr
  - Tenant/project anonymisation

DocumentExtractionResult additions:
  extraction_cost_inr, tokens_consumed, extraction_attempts, timed_out, llm_call_ids

On timeout: status = Failed_Timeout. NO auto-retry (document extraction requires human
  review — silent retry risks cost with poor output). Manual retry by Portfolio Manager.

Concurrent extraction enforcement: Redis counter (INCR atomic) tracks active extractions.
  Counter checked before each call. Queued if at max_concurrent_extractions limit.
```

---

## 4. MULTI-TENANT DEPLOYMENT DECISION (§7.135 – §7.137)

---

### §7.135 — Multi-Tenant Architecture Question — Resolution

```
QUESTION RAISED: With multiple EPC firms using EPCC, should each get a dedicated database?

ANSWER: No. ES-DB-001 (schema-per-tenant) is technically correct and sufficient.
Schema-level isolation in PostgreSQL is a hard namespace boundary.
search_path = tenant_{slug} + tenant_id JWT injection = two independent enforcement layers.
A cross-tenant data leak requires an application exploit or PostgreSQL engine bug —
identical risk profile to database-per-tenant.

WHAT THE QUESTION CORRECTLY IDENTIFIED:
  1. Per-tenant backup/restore was not specified → Fixed in ES-DR-002 v1.2
  2. Enterprise EPC clients may have contractual data residency requirements
     that schema isolation does not satisfy commercially → Fixed by Tier 2 deployment

WHAT THE QUESTION DID NOT REQUIRE:
  Changing ES-DB-001. Schema-per-tenant is confirmed and closed.
```

---

### §7.136 — Deployment Tier Strategy (EPCC_Deployment_Tier_Specification_v1_0)

```
LOCKED: Two deployment tiers defined.

TIER 1 — Multi-Tenant Shared Deployment:
  Target: Growing EPC firms, PMCs, hospital trusts
  Model:  Schema-per-tenant (ES-DB-001) on shared infrastructure
  Isolation: Schema-level (complete, technically equivalent to DB-level)
  EPCC commits to: dedicated schema, no cross-tenant queries, per-schema backup on request
  EPCC does NOT commit to: physical server dedicated to one client
  Capacity: ≤50 tenants per instance
  Pricing: SaaS subscription per project per month

TIER 2 — Dedicated Single-Tenant Deployment:
  Target: Large enterprise EPC firms with contractual data residency requirements
  Model:  Entire EPCC stack on client's own or dedicated infrastructure
  Isolation: Physical infrastructure separation (same codebase, same schema model)
  EPCC commits to: no other EPC firm's data on same server/instance/VPC
  Options: A) Client's own on-prem server. B) EPCC-managed dedicated cloud VPC.
  Pricing: Annual enterprise license + deployment fee + support

ENGINEERING IMPACT: Zero. Same codebase. Same Docker Compose. Same schema model.
  TENANT_COUNT=1 env var. tenant_id enforcement retained for future sub-tenant support.

TIER 1 → TIER 2 MIGRATION PATH:
  pg_dump --schema=tenant_{slug} from Tier 1 instance (ES-DR-002 v1.2)
  → pg_restore to dedicated Tier 2 instance
  → Alembic migrate to HEAD
  → DNS cutover
  → 48hr parallel run
  → Decommission from Tier 1
  Estimated window: 4–6 hours. Non-destructive and reversible until final step.
```

---

### §7.137 — ES-DB-001 Final Confirmation

```
STATUS: CONFIRMED. LOCKED. CLOSED.

ES-DB-001 (Schema-Per-Tenant) is the permanent multi-tenancy standard for EPCC.
This decision was challenged, reviewed against first principles, and upheld.

Arguments reviewed and rejected:
  "Competitor data on same DB" → Tier 2 deployment resolves contractual concern.
                                  Schema isolation resolves technical concern.
  "Cannot restore one tenant"  → ES-DR-002 v1.2 per-schema backup resolves this.
  "Database-per-tenant is industry standard" → False. Schema-per-tenant is widely used
    by production SaaS systems (Notion, Intercom, Shopify at smaller scales). Decision
    is appropriate for ≤50 tenant 5-year horizon.

This decision will be re-evaluated if and only if:
  Tenant count exceeds 50 active tenants, OR
  A specific tenant generates >40% of total database I/O (resource starvation risk)
  In either case: affected tenant migrates to Tier 2, not architecture change.

Do not reopen this question without the above trigger conditions being met.
```

---

## 5. PENDING ACTIONS FROM THIS SESSION

*(Items that were identified but not yet executed — for next session)*

| # | Action | Module/File | Priority |
|---|--------|-------------|----------|
| 1 | M07 amendment: update RecalcJob effective_date to use captured_at from M04 | M07_EVM_Engine_v3_1 | P1 |
| 2 | M03 amendment: actual_delivery_date source = MaterialReceipt.captured_at | M03_Planning_Milestones_v2_4 | P1 |
| 3 | Phase 2 IntegrationAdapterSpec: ERP/IoT/BIM adapter layer | New document | P3 (Phase 2) |
| 4 | Lock Engineering Standards v1.2 after PMO Director review | ES v1.2 | P0 |
| 5 | Lock Deployment Tier Specification v1.0 after PMO Director review | Tier Spec v1.0 | P1 |

---

*Amendment complete. Apply to v5.2 to produce v5.3.*
*Next memory version will be v5.4 when pending actions above are completed.*
