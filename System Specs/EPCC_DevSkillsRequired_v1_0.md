# EPCC — Development Skills Required
## Version 1.0
**Owner:** PMO Director / Tech Lead
**Created:** 2026-05-03 | **Status:** Locked
**Purpose:** Define skill profile required to build EPCC clean, robust, low-debug-burden.

---

## 1. PRINCIPLE

Robust software with low debugging burden requires the right team composition — not just headcount. Each role below has explicit, non-overlapping ownership.

---

## 2. CORE STACK SKILLS (mandatory)

### 2.1 Backend — Python / FastAPI

| Skill | Level | Why |
|---|---|---|
| FastAPI framework | Senior | Primary API layer. Async patterns, dependency injection, Pydantic validation |
| Python 3.11+ | Senior | Type hints mandatory, generics, async/await fluency |
| Pydantic v2 | Senior | Every entity is a Pydantic model; validation = enforcement layer |
| SQLAlchemy 2.x | Senior | ORM for Postgres. 2.x async patterns. Avoid legacy 1.x patterns |
| Alembic | Mid | Migration tooling per ES-DB-008. Every schema change = migration |
| pytest + pytest-asyncio | Senior | Testing discipline. >80% coverage on BRs and integrations |
| OpenAPI / Swagger | Mid | Auto-generated from FastAPI; verify each endpoint contract |

**Anti-patterns to avoid:** Django (over-opinionated for this scope), Flask (lacks built-in async/Pydantic), raw SQL in business logic.

### 2.2 Database — PostgreSQL

| Skill | Level | Why |
|---|---|---|
| PostgreSQL 15+ administration | Senior | Multi-tenant via schema-per-tenant per ES-DB-001 |
| Index design | Senior | EVM/dashboard queries scan millions of rows; bad indexes = 10x perf hit |
| JSONB | Mid | Used for flexible fields (e.g., scenario configs, validation_report) |
| Row-level security | Mid | Tenant isolation enforcement |
| Query optimisation (EXPLAIN ANALYZE) | Senior | Mandatory for any query > 100ms |
| pgBouncer / connection pooling | Mid | Production scale concern |

### 2.3 Background Jobs — Celery

| Skill | Level | Why |
|---|---|---|
| Celery 5.x | Mid | EVM recalc, snapshot generation, HDI imports |
| Redis (broker + backend) | Mid | Celery broker + cache layer per existing standards |
| DLQ patterns | Mid | Per ES-BL-006 — every queue has a Dead Letter Queue |
| Idempotency | Senior | Retries must not double-execute; critical for financial calcs |

### 2.4 Frontend — React + TypeScript

| Skill | Level | Why |
|---|---|---|
| React 18+ | Senior | Functional components, hooks, Suspense |
| TypeScript 5+ | Senior | Type discipline mirrors backend Pydantic |
| TanStack Query (React Query) | Senior | Server state management — caching, mutations, invalidation |
| TanStack Table v8 | Mid | Heavy table rendering (gates, BOQ, registers) |
| React Hook Form + Zod | Senior | Form state + validation that mirrors Pydantic backend rules |
| Tailwind CSS | Mid | Per UI Design System v1.0 (to be re-issued) |
| Recharts / Plotly | Mid | EVM curves, S-curves, trend charts |
| AG-Grid (alternative to TanStack Table) | Mid | Consider if Excel-grade grid features needed (BOQ editing, etc.) |

**Anti-patterns:** Redux (over-engineered for this scope; TanStack Query is sufficient), MUI/Ant Design (bloat), CSS-in-JS (performance cost).

### 2.5 File Storage — MinIO

| Skill | Level | Why |
|---|---|---|
| S3-compatible API | Mid | Document uploads, evidence photos, certificates |
| Pre-signed URLs | Mid | Direct upload from browser; never proxy through API |
| Lifecycle policies | Low | Archival of old documents |

### 2.6 DevOps / Infra

| Skill | Level | Why |
|---|---|---|
| Docker + Docker Compose | Senior | Local dev parity with production |
| Kubernetes (or Docker Swarm minimum) | Mid | Production scaling — multi-tenant requires careful resource sharding |
| GitHub Actions | Senior | Per ES-CICD-001/002 — 7-stage pipeline locked |
| Terraform / IaC | Mid | Cloud infra reproducibility |
| Observability stack: Prometheus + Grafana + Loki | Mid | Metrics + logs |
| Sentry or equivalent | Mid | Error tracking |

---

## 3. DOMAIN SKILLS (mandatory for at least one team member)

### 3.1 Construction / Hospital EPC Domain

| Skill | Why |
|---|---|
| Earned Value Management (EVM) — PMI/AACE conventions | M07 is the heart; missteps = misleading reports |
| Indian construction commercial conventions (RA bills, retention, GST/TDS) | M06 cannot be designed by anyone without this |
| BOQ + CPWD/PWD rate analysis | M02, M14 depend on this |
| Stage gate governance (PMI / institutional capital) | M08 + Project.md core principle |
| NABH accreditation infrastructure requirements | M09, M15, M24 — hospital-specific |
| AERB radiation safety lifecycle | LINAC, MRI, CT-specific tracking |
| BOCW + IS 14489 safety standards | M31 HSE module |

**Recommendation:** At least one team member with hands-on Indian construction PMC experience. Without this, the system will be "generic project management software", not "hospital EPC control".

### 3.2 Compliance & Regulatory

| Skill | Why |
|---|---|
| DPDP Act 2023 | Per ES-SEC-004 — data localization, consent, audit |
| Data retention rules for construction (7+ years for contractual evidence) | Audit log retention rules |
| GST + TDS handling | M06 |

---

## 4. PROCESS / QUALITY SKILLS (mandatory)

### 4.1 Software Engineering Discipline

| Skill | Why |
|---|---|
| Test-driven development (TDD) | BRs are testable units; write tests first |
| Type-driven design | Pydantic + TypeScript — types are the contract |
| Code review etiquette | Every PR needs senior review; no merge without 1 approval |
| Conventional commits (feat:, fix:, docs:) | Auto-generates changelog |
| Semantic versioning per module | Mirrors EPCC's Major/Minor rule |

### 4.2 Security

| Skill | Level | Why |
|---|---|---|
| OWASP Top 10 awareness | Mandatory | Every dev must know |
| Authentication (OAuth2 / OIDC) | Senior | Multi-tenant SSO |
| Authorization (RBAC + ABAC) | Senior | M34 is non-trivial; complex role + scope rules |
| Audit logging discipline | Mandatory | Every state change is logged |
| Secrets management (Vault / AWS Secrets Manager) | Mid | No secrets in code, ever |

### 4.3 Documentation

| Skill | Why |
|---|---|
| API documentation (auto-generated via FastAPI) | Reduces sync drift |
| ADR (Architecture Decision Records) writing | Captures "why" so the next dev doesn't repeat mistakes |
| Markdown discipline | Specs ARE the dev brief |

---

## 5. ROLE COMPOSITION — MINIMUM TEAM

For Phase 1 build (~20 modules over ~30 weeks compressed):

| Role | Count | Mandatory Skills |
|---|---|---|
| Tech Lead / Architect | 1 | Full stack, infra, domain awareness, makes call on §5 ambiguities |
| Senior Backend Engineer | 2 | Python/FastAPI/Postgres/Celery senior, owns 8–10 modules each |
| Senior Frontend Engineer | 2 | React/TS/Tailwind senior, owns dashboards + forms across all modules |
| Mid Backend Engineer | 1 | Supports senior backends, builds simpler modules (M11, M23) |
| QA Engineer | 1 | pytest, Playwright, manual exploratory; not optional |
| DevOps / SRE | 1 | CI/CD, infra, monitoring, on-call rotation |
| Domain Consultant (PT) | 1 | Indian hospital EPC; reviews specs + acceptance tests |
| Tech Writer (PT) | 0.5 | Spec maintenance, ADRs, user-facing docs |

**Total: ~8.5 FTE for Phase 1.** Smaller team possible only with senior multidisciplinary engineers.

---

## 6. RECOMMENDED PRACTICES (low-debug, low-rework)

| Practice | Reason |
|---|---|
| **Spec → Test → Code** order | TDD + spec-driven; tests = executable BRs |
| **Schema migrations are PRs** | Reviewed like code; never ad-hoc |
| **Feature flags for risky modules** | M07, M26 can be toggled if buggy |
| **Database seed scripts per environment** | Local dev = production-like data |
| **Mocked external integrations in dev** | Tally/Zoho/SAP integration mocks — real systems only in staging |
| **Read-replica for dashboards** | M10 / M18 hit read-replicas; never primary DB |
| **Connection pool sized = expected concurrent users × 2** | Saves a class of production outages |
| **One module = one team owner** | Joint ownership = nobody fixes bugs |
| **Daily 15-min sync (not stand-up)** | Fast unblock; no status theatre |
| **Fortnightly architecture review** | Catches design drift before code |
| **Mandatory pair programming on M07, M08, M27, M34** | Critical-path modules; second brain catches bugs |

---

## 7. ANTI-PATTERNS — DO NOT DO

| Anti-Pattern | Why |
|---|---|
| Microservices from day 1 | Premature; one monolith → split later if scale demands |
| GraphQL | REST suffices for this scope; GraphQL adds complexity without payoff |
| MongoDB / NoSQL primary | Financial data needs ACID; Postgres is correct choice |
| Custom auth | Use proven library (Authlib, FastAPI-Users); never roll your own |
| Building before locking specs | Per current plan — already mitigated |
| Skipping migrations for "small fixes" | Drift is the #1 source of multi-tenant bugs |
| One Excel macro author writing the whole system | Spec is right; execution skill set is different |

---

## 8. HIRING / SOURCING NOTES

| Search Term | Quality Filter |
|---|---|
| "FastAPI Postgres senior" | At least 2 years in this stack, not just Python in general |
| "React TypeScript senior dashboard" | Portfolio with data-heavy UIs (admin, analytics, BI) |
| "Indian construction PMC software" | Rare combo; consider domain consultant + tech generalist |
| "Multi-tenant SaaS" | Schema-per-tenant experience specifically (not row-level only) |

**Compensation note (India market, 2026):**
- Tech Lead: ₹40–70 lakh CTC
- Senior Engineer: ₹25–45 lakh CTC
- Mid Engineer: ₹15–25 lakh CTC
- DevOps: ₹25–40 lakh CTC
- Domain Consultant (PT): ₹3–5 lakh / month

Total Phase 1 burn rate ~₹2.5–3.5 Cr / 6 months. Compare against KDMC pilot project value to validate.

---

## 9. SKILL GAP HANDLING

If a skill below is unavailable in-house:

| Gap | Mitigation |
|---|---|
| EVM / construction domain | Hire domain consultant first; defer M07, M14 specs until they're on board |
| Multi-tenant DB design | Get Postgres consultant for 2-week deep dive at architecture phase |
| Hospital regulatory (NABH/AERB) | Engage NABH consultant; treat as non-negotiable for healthcare modules |
| Frontend at scale | TanStack Query / Table — bring in seasoned React engineer over generalist |

---

## 10. CHECKLIST BEFORE FIRST LINE OF CODE

```
[ ] Tech Lead hired and on-board
[ ] Stack confirmed in writing (lock against ES standards)
[ ] Local dev environment reproducible by every dev (Docker Compose, seed data)
[ ] CI/CD pipeline running on a "hello world" before any module work
[ ] Phase 1 specs all locked at v1.0
[ ] X1 RBAC matrix locked
[ ] X2 Data Dictionary locked
[ ] Test framework chosen and templated (pytest + Playwright)
[ ] Sentry / observability stack provisioned
[ ] PostgreSQL multi-tenant pattern decided + tested
[ ] First module to build picked (recommend: M34 → M01 → M02)
```

---

*v1.0 — locked. Updated when stack changes or new module domains require new skills.*
