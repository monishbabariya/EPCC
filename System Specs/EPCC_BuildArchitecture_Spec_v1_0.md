---
artefact: EPCC_BuildArchitecture_Spec_v1_0
round: 24
date: 2026-05-03
author: Monish (with Claude assist)
x8_version: v0.5
x9_version: v0.3
status: LOCKED
---

# EPCC Build Architecture — Spec v1.0 (Round 24)

> **Purpose.** Lock the concrete build architecture for EPCC v1.0. Every choice in this Spec is binding for Rounds 25–29 (scaffold → ENUM codegen → M34 thin slice → M01 thin slice → demo) and for the subsequent module-deepening rounds.
>
> **Inputs.** Round 23 Brief + OQ-1 ANSWERS (all 10 user decisions + ~30 OQ-2 defaults locked 2026-05-03).
>
> **Cadence.** Round 24 Spec is the final gate before code touches the repo. Round 25 may begin scaffolding immediately on lock.

---

## Block 1 — Identity

| Field | Value |
|---|---|
| Artefact ID | `EPCC_BuildArchitecture_Spec_v1_0` |
| Type | System Spec (governance — not a module) |
| Owner | PMO Director (delegated to Monish for v1.0) |
| Round | 24 |
| Status | LOCKED |
| References | Round 23 Brief; CLAUDE.md §4 (locked decisions); `.claude/rules/architecture.md`; `.claude/rules/spec-protocol.md`; `.claude/rules/naming-folders.md`; X8 v0.5; X9 v0.3 |
| Replaces | (nothing — first build-architecture artefact) |

---

## Block 2 — Scope Boundary

### In scope (LOCKED)

1. Repository, branch, and folder layout for code + specs in one monorepo.
2. Backend toolchain (Python 3.12 + FastAPI + SQLAlchemy + Alembic + Celery + tests).
3. Frontend toolchain (Vite + React + TypeScript + Tailwind + shadcn + TanStack Query + e2e tests).
4. ENUM codegen pipeline (X8 markdown → Python module + TypeScript types).
5. API contract pipeline (FastAPI → OpenAPI 3.1 → TS client).
6. Database conventions (Postgres 16, RLS for tenant isolation, Alembic migrations, reserved fields).
7. Auth (Keycloak realm + 17 roles + MFA for 5 designated roles + local password fallback).
8. Local dev environment (docker-compose: Postgres + Redis + MinIO + Keycloak).
9. CI pipeline (GitHub Actions, gates, required checks).
10. Branch protection + PR template.
11. Spec ↔ code traceability convention (BR codes in test names + CI coverage check).
12. Cascade discipline applied to code (inherits Round 18 lock).
13. Pilot seed (KDMC-001-DBOT) reproducibility.
14. Module implementation sequence and "thin vertical slice" definition.

### Explicitly out of scope (deferred / Phase 2)

- Production hosting choice (OQ-1.8 deferred until first module ships).
- Observability stack (logs/metrics/traces — defer 2 weeks past first-module-live).
- Performance budgets (defer until first benchmark).
- Mobile / offline strategy.
- External party portal hardening (PF03).
- Real-time WebSocket transport (X9 v0.3 §OQ-1.8 — out of v1.0).
- HDI / Historical Data Import workstream (separate, gated by M02 lock + workbook readiness).
- The 4 unresolved KDMC workbook items.
- 13-folder hierarchy migration (deferred indefinitely per Round 18 audit).

---

## Block 3 — Repository & Folder Architecture

### 3.1 Repository

- **Location:** `monishbabariya/EPCC` on GitHub.
- **Visibility:** private during pilot.
- **Strategy:** **monorepo on `main`** (OQ-1.1 = A).
- **Branch model:** trunk-based (OQ-1.2 = A). `main` always deployable.
- **No long-lived branches** other than `main`. `claude/*` agent branches are short-lived (< 3 days) and merged via PR.

### 3.2 Folder layout (LOCKED)

```
EPCC/
├── CLAUDE.md
├── README.md                          # ← created Round 25
├── Makefile                           # ← created Round 25 (top-level dev commands)
├── .gitignore                         # ← extended Round 25 for Python + Node + tooling
├── .editorconfig                      # ← created Round 25
├── .env.example                       # ← created Round 25 (no secrets, just keys)
├── .claude/                           # rules + skills (existing)
├── .github/
│   └── workflows/
│       ├── ci.yml                     # ← Round 25 (full pipeline)
│       └── enum-codegen-check.yml     # ← Round 26
├── SystemAdmin/                       # specs (existing — untouched)
├── System Specs/                      # governance (existing)
├── ZEPCC_Legacy/                      # frozen (existing)
├── apps/
│   ├── api/                           # FastAPI backend
│   │   ├── pyproject.toml
│   │   ├── alembic.ini
│   │   ├── README.md
│   │   ├── src/epcc_api/
│   │   │   ├── __init__.py
│   │   │   ├── main.py                # FastAPI entrypoint
│   │   │   ├── core/
│   │   │   │   ├── config.py          # pydantic-settings
│   │   │   │   ├── db.py              # async engine + session
│   │   │   │   ├── auth.py            # OIDC + local fallback
│   │   │   │   ├── deps.py            # FastAPI dependencies (current_user, current_tenant)
│   │   │   │   └── audit.py           # audit-log emitter
│   │   │   ├── modules/
│   │   │   │   ├── m34_rbac/
│   │   │   │   ├── m01_project_registry/
│   │   │   │   ├── m02_structure_wbs/
│   │   │   │   ├── m03_planning_milestones/
│   │   │   │   └── m04_execution_capture/
│   │   │   └── shared/
│   │   │       ├── tenant.py          # tenant_id middleware
│   │   │       ├── reserved_fields.py # the 6 reserved columns mixin
│   │   │       └── exceptions.py
│   │   ├── migrations/                # Alembic
│   │   └── tests/
│   │       ├── unit/
│   │       ├── integration/
│   │       └── conftest.py
│   └── web/
│       ├── package.json
│       ├── vite.config.ts
│       ├── tsconfig.json
│       ├── biome.json
│       ├── tailwind.config.ts
│       ├── README.md
│       ├── src/
│       │   ├── main.tsx
│       │   ├── App.tsx
│       │   ├── routes/
│       │   ├── modules/
│       │   │   ├── m34_rbac/
│       │   │   ├── m01_project_registry/
│       │   │   └── ...
│       │   ├── components/
│       │   │   └── ui/                # shadcn/ui copies
│       │   ├── lib/
│       │   │   ├── api.ts             # openapi-fetch client
│       │   │   ├── auth.ts
│       │   │   └── utils.ts
│       │   └── styles/
│       │       └── globals.css
│       ├── public/
│       └── tests/
│           ├── unit/
│           └── e2e/                   # Playwright
├── packages/
│   ├── enums/
│   │   ├── python/
│   │   │   ├── pyproject.toml
│   │   │   └── src/epcc_enums/        # generated, gitignored except __init__.py stub
│   │   └── typescript/
│   │       ├── package.json
│   │       └── src/                   # generated
│   └── api-types/
│       ├── package.json
│       └── src/                       # openapi-typescript output
├── infra/
│   ├── docker-compose.yml             # postgres, redis, minio, keycloak
│   ├── docker-compose.test.yml        # CI overlay
│   ├── postgres/
│   │   └── init.sql                   # extensions + RLS bootstrap
│   ├── keycloak/
│   │   └── realm-export.json          # 17 roles pre-configured
│   ├── minio/
│   │   └── README.md
│   └── seed/
│       ├── __init__.py
│       └── kdmc.py                    # pilot seed
├── scripts/
│   ├── codegen-enums.py               # X8 .md → python + ts
│   └── codegen-api-types.sh           # openapi → ts
└── docs/
    └── (empty for v1.0; future home for ADRs / runbooks)
```

### 3.3 Code-to-spec mapping (LOCKED)

For every locked module, code modules mirror spec layout 1:1:

| Spec | Backend module | Frontend module |
|---|---|---|
| `M34_SystemAdminRBAC_Spec_v1_0.md` | `apps/api/src/epcc_api/modules/m34_rbac/` | `apps/web/src/modules/m34_rbac/` |
| `M01_ProjectRegistry_Spec_v1_0.md` | `apps/api/src/epcc_api/modules/m01_project_registry/` | `apps/web/src/modules/m01_project_registry/` |
| `M02_StructureWBS_Spec_v1_0.md` | `apps/api/src/epcc_api/modules/m02_structure_wbs/` | `apps/web/src/modules/m02_structure_wbs/` |
| `M03_PlanningMilestones_Spec_v1_1.md` | `apps/api/src/epcc_api/modules/m03_planning_milestones/` | `apps/web/src/modules/m03_planning_milestones/` |
| `M04_ExecutionCapture_Spec_v1_0.md` | `apps/api/src/epcc_api/modules/m04_execution_capture/` | `apps/web/src/modules/m04_execution_capture/` |

Each backend module follows a fixed internal layout:

```
m0X_<name>/
├── __init__.py
├── models.py        # SQLAlchemy entities (Block 3 of spec)
├── schemas.py       # Pydantic request/response (Block 3 + Block 5 of spec)
├── routes.py        # FastAPI router (Block 7 of spec)
├── service.py       # business rules (Block 6 of spec)
├── permissions.py   # RBAC checks (M34 + module-specific)
└── tests/
    ├── test_models.py
    ├── test_service.py
    └── test_routes.py     # BR-tagged tests live here
```

Frontend module follows:

```
m0X_<name>/
├── index.ts
├── routes.tsx
├── pages/
├── components/
├── hooks/           # TanStack Query hooks
└── types.ts         # re-exports from @epcc/api-types
```

### 3.4 Existing folders untouched

- `SystemAdmin/`, `System Specs/`, `ZEPCC_Legacy/` are unchanged.
- M34 stays at `SystemAdmin/M34_*` (Round 18 audit lock).

---

## Block 4 — Toolchain Lock

### 4.1 Backend (Python 3.12)

| Concern | Choice | Pin |
|---|---|---|
| Package manager | `uv` | latest (auto-update via dev container) |
| Web framework | `fastapi` | `^0.110.0` |
| ASGI server (dev) | `uvicorn[standard]` | `^0.27.0` |
| ASGI server (prod) | `gunicorn` w/ `uvicorn.workers.UvicornWorker` | `^21.2.0` |
| ORM | `SQLAlchemy` (2.x async) | `^2.0.27` |
| DB driver | `asyncpg` | `^0.29.0` |
| Migration | `alembic` | `^1.13.0` |
| Validation | `pydantic` (v2) | `^2.6.0` |
| Settings | `pydantic-settings` | `^2.2.0` |
| Background jobs | `celery` | `^5.3.0` |
| Broker | `redis` (Python client) | `^5.0.0` |
| Object storage | `boto3` | `^1.34.0` |
| OIDC client | `authlib` | `^1.3.0` |
| HTTP test client | `httpx` | `^0.27.0` |
| Test runner | `pytest` | `^8.0.0` |
| Async test plugin | `pytest-asyncio` | `^0.23.0` |
| DB fixture | `pytest-postgresql` | `^5.0.0` |
| Coverage | `coverage[toml]` | `^7.4.0` |
| Lint + format | `ruff` | `^0.3.0` |
| Type checker | `mypy` | `^1.9.0` |

**`mypy` configuration:** `--strict` for `apps/api/src/epcc_api/`. Tests use `disallow_untyped_decorators = false` to permit `pytest` decorators.

**`ruff` configuration:** rules `E`, `F`, `W`, `I`, `N`, `B`, `UP`, `SIM`, `PT`, `RUF`. Line length 100. Auto-fix on save.

### 4.2 Frontend (TypeScript 5)

| Concern | Choice | Pin |
|---|---|---|
| Bundler | Vite | `^5.2.0` |
| Language | TypeScript | `^5.4.0` |
| UI runtime | React | `^18.3.0` |
| Routing | React Router | `^6.22.0` |
| Server state | TanStack Query | `^5.28.0` |
| Client state | Zustand | `^4.5.0` |
| Forms | react-hook-form | `^7.51.0` |
| Schema validation | zod | `^3.22.0` |
| Styling | Tailwind CSS | `^3.4.0` |
| Component primitives | shadcn/ui (copy-into-repo) | tracked via `components.json` |
| Charts | Recharts | `^3.0.0` (X9 v0.3 lock) |
| Gantt | frappe-gantt | `^0.7.0` (X9 v0.3 lock) |
| Network graph | react-flow | `^12.0.0` (X9 v0.3 lock) |
| API client | openapi-fetch | `^0.9.0` |
| Type codegen | openapi-typescript | `^6.7.0` |
| Test runner (unit) | Vitest | `^1.4.0` |
| RTL | @testing-library/react | `^14.2.0` |
| E2E | Playwright | `^1.42.0` |
| Lint + format | biome | `^1.6.0` |

**`biome` configuration:** strict TS rules, double quotes, 100-char line, sorted imports. ESLint fallback only if a rule biome doesn't yet support is required.

### 4.3 Database

- **Engine:** PostgreSQL 16.
- **Extensions enabled at bootstrap:** `pgcrypto`, `uuid-ossp`, `citext`.
- **Multi-tenant isolation:** Row-level security (RLS) policies on every tenant-scoped table. Policy: `tenant_id = current_setting('epcc.tenant_id')::uuid`. Set per-request via SQLAlchemy `event.listens_for("after_begin")`.
- **Reserved fields mixin:** `tenant_id`, `created_by`, `created_at`, `updated_by`, `updated_at`, `is_active` on every entity except the locked exemptions (per `naming-folders.md`).
- **Migration discipline:** every PR touching SQLAlchemy models must include the matching `alembic revision --autogenerate -m "<message>"` output. CI fails if `alembic check` reports drift.

### 4.4 Auth — Keycloak

- **Realm:** `epcc` (single realm, all tenants).
- **Realm export:** `infra/keycloak/realm-export.json` (checked in, idempotent on import).
- **Roles pre-configured:** all 17 from M34 spec Block 3.
- **MFA enforced for:** `SYSTEM_ADMIN`, `PMO_DIRECTOR`, `PORTFOLIO_MANAGER`, `FINANCE_LEAD`, `EXTERNAL_AUDITOR` (M34 lock).
- **Local password fallback:** Keycloak's built-in password grant for users without OIDC IdP linkage. Phase 2 may swap to enterprise IdP federation; the M34 abstraction permits this without code changes.
- **Token format:** JWT (RS256). Backend validates via Keycloak JWKS endpoint cached for 1 hour.

### 4.5 Object storage

- **Engine:** MinIO in dev (S3-compatible API). Production may swap to AWS S3 / Cloud Storage / Azure Blob without code change.
- **Buckets:** `epcc-photos`, `epcc-documents`, `epcc-exports`. Created idempotently on first start.
- **Access:** signed URLs (TTL 15 min) for client uploads/downloads. No public buckets.

### 4.6 Background jobs

- **Engine:** Celery 5.x with Redis broker + result backend.
- **Concurrency:** prefork, 4 workers in dev; tunable in prod.
- **Queues:** `default`, `imports`, `nightly`. M04 NCR daily sweep + M04 ContractorPerformanceScore quarterly batch use `nightly`.

---

## Block 5 — API Contract Pipeline

### 5.1 Sources of truth

- **Backend:** FastAPI route definitions emit OpenAPI 3.1 at `/api/v1/openapi.json` (dev) and at build time (`apps/api/scripts/dump-openapi.py`).
- **Frontend:** consumes the dumped JSON via `openapi-typescript` to generate `packages/api-types/src/index.ts`. Frontend imports `@epcc/api-types`.

### 5.2 URL versioning

- All routes prefixed `/api/v1/`.
- Single major version in v1.0. Breaking changes require a new major prefix; opening a v2 round if/when needed.

### 5.3 Conventions

- Resource names: plural lowercase (`/projects`, `/work-packages`).
- IDs: UUIDv4 (no auto-increment integers exposed externally).
- Pagination: `?page=&page_size=` with `X-Total-Count` header.
- Errors: RFC 9457 problem-details JSON.
- Audit: every mutation returns the audit-log ID in the response (`X-Audit-Id` header).

---

## Block 6 — Business Rules (build-level)

| ID | Rule | Enforcement |
|---|---|---|
| **BR-BA-001** | All code modules under `apps/api/src/epcc_api/modules/` must mirror the spec naming `m0X_<short_name>`. | CI lint check reads `SystemAdmin/Modules/` filenames + asserts mirror exists. |
| **BR-BA-002** | Every locked Business Rule (`BR-XX-NNN`) in any module spec must have ≥ 1 test named `test_BR_XX_NNN_*`. | Custom pytest plugin scans spec files + asserts coverage. CI fails on gap. |
| **BR-BA-003** | Generated files (`packages/enums/`, `packages/api-types/`) must be regenerated whenever the source changes. | CI runs codegen + diffs; non-empty diff fails the build. |
| **BR-BA-004** | No direct DB access across modules. Cross-module reads MUST go through the owning module's internal HTTP API (F-005 single-owner rule). | CI lint check rejects imports of `other_module.models` from a different module's package. |
| **BR-BA-005** | Every entity inheriting `ReservedFieldsMixin` must populate `created_by` + `updated_by` from the request user. | SQLAlchemy event listener; raises if the values are unset on flush. |
| **BR-BA-006** | RLS policy must be active on every tenant-scoped table. | Postgres test query at startup verifies `pg_policy` row count against expected. |
| **BR-BA-007** | No commit may merge to `main` with a failing CI check. | GitHub branch protection (BA-OQ-3 lock). |
| **BR-BA-008** | Every PR description must reference a spec section path (or "n/a — infra/scaffold change"). | PR template + manual reviewer enforcement. |
| **BR-BA-009** | Append-only ledgers (per X8 §6 exemption list) MUST forbid `UPDATE` and `DELETE` at the database level. | `REVOKE UPDATE, DELETE ON <table> FROM PUBLIC` + Alembic migration; integration test verifies. |
| **BR-BA-010** | Cascade discipline (Round 18) applies: 1-field changes → cascade note + single PR; substantive changes → full re-issue + multi-PR. | Manual reviewer enforcement; documented in PR template. |

---

## Block 7 — Integration Points

| Integration | Direction | Mechanism |
|---|---|---|
| Specs ↔ code | Specs drive code | File-name mirroring (`M0X_<name>` → `m0x_<name>/`). Manual sync; no automation in v1.0. |
| X8 ENUMs ↔ Python | X8 → generated | `scripts/codegen-enums.py` parses X8 markdown tables → emits `packages/enums/python/`. |
| X8 ENUMs ↔ TypeScript | X8 → generated | Same script emits `packages/enums/typescript/`. |
| Backend ↔ Frontend types | Backend → generated | FastAPI OpenAPI → `openapi-typescript` → `packages/api-types/`. |
| Backend ↔ Postgres | Backend writes | SQLAlchemy 2.x async + asyncpg + Alembic migrations. RLS enforces tenancy. |
| Backend ↔ Redis | Backend reads/writes | Celery broker + result backend. |
| Backend ↔ MinIO | Backend issues signed URLs | `boto3` against MinIO endpoint. |
| Backend ↔ Keycloak | Backend validates JWT | `authlib` + JWKS cache. |
| Frontend ↔ Backend | HTTP/JSON | `openapi-fetch` typed client + TanStack Query. |
| CI ↔ GitHub | CI runs on PR | GitHub Actions; required checks gate merge. |

---

## Block 8 — Governance & Audit

### 8.1 Branch protection (LOCKED — applied in Round 25 admin step)

- `main` is protected.
- Required CI checks: `lint`, `typecheck`, `test`, `e2e`, `enum-codegen-stale`, `br-coverage`.
- Required reviewers: 1 (Monish for v1.0).
- Linear history enforced (squash-merge only).
- Force-push to `main` blocked.
- Direct pushes to `main` blocked.

### 8.2 PR template (LOCKED)

```markdown
## Summary
<1-3 sentences>

## Spec reference
<path + section, or "n/a — scaffold/infra change">

## BR codes touched
<comma-separated, or "none">

## Cascade note
<path, or "n/a">

## Checklist
- [ ] Tests added/updated
- [ ] Migrations included (if model changed)
- [ ] ENUM codegen re-run (if X8 changed)
- [ ] Screenshot attached (if UI changed)
- [ ] Spec/code parity verified

## Test plan
<bullet list>
```

### 8.3 Audit-log convention

- Every mutation through `core.audit.emit()`. Schema: `event_type` (UPPER_SNAKE_CASE per X8), `actor_user_id`, `tenant_id`, `entity_type`, `entity_id`, `before_value`, `after_value`, `request_id`, `ip`, `user_agent`, `at`.
- Append-only table `system_audit_log` (M34 spec, exempt from `updated_*` per `naming-folders.md`).
- Round 27 wires this for M34; subsequent modules inherit.

### 8.4 Versioning

- Application version: SemVer in `apps/api/pyproject.toml` and `apps/web/package.json`. Bumped on each `main` merge that ships a feature.
- Generated package version: `epcc_enums` follows `<x8.major>.<x8.minor>.<patch>` (BA-OQ-1 lock).
- Migration version: Alembic revision IDs (auto).

### 8.5 Round-on-code traceability

- Each commit message references the round in the form `Round NN(:|—) <action>`.
- Each PR title includes the round number.
- VersionLog updated on every artefact event; CLAUDE.md banner updated on every round transition.

---

## Block 9 — Explicit Exclusions

- No production-grade hosting decision in v1.0 (deferred per OQ-1.8).
- No SSO federation beyond Keycloak in v1.0.
- No GraphQL / gRPC layers — REST + OpenAPI only.
- No microservices — single FastAPI app, single deploy unit (BA-OQ-6 cross-module rule).
- No real-time WebSocket transport (X9 v0.3 lock).
- No ESLint by default — biome only; ESLint allowed only as a rule-coverage fallback.
- No premature observability stack — first-module-live + 2 weeks before deciding.
- No PostgreSQL extensions beyond the three listed in §4.3 without a new round.
- No mobile / offline. No PWA.

---

## Block 10 — Open Questions

**Zero.** All Round 23 OQ-1 + OQ-2 questions answered. All BA-OQ-1 to BA-OQ-6 carry-forwards resolved. Round 24 LOCKS.

---

## Appendix A — Module Implementation Sequence (LOCKED)

| Round | Deliverable | Definition of Done |
|---|---|---|
| 25 | Monorepo scaffold | `apps/api` + `apps/web` + `packages/` + `infra/` directories created. `make up` brings dev env online (Postgres + Redis + MinIO + Keycloak). `make health` returns 200. CI green on lint+typecheck+empty-test. |
| 26 | ENUM codegen pipeline | `scripts/codegen-enums.py` parses `X8_GlossaryENUMs_v0_5.md` → emits Python + TS. CI gate `enum-codegen-stale` active. `epcc_enums` import works in `apps/api`; `@epcc/enums` import works in `apps/web`. |
| 27 | M34 thin slice | OIDC login + local fallback + 17 roles seeded in Keycloak + role-switcher UI + audit-log skeleton + first BR-tagged tests pass. |
| 28 | M01 thin slice | KDMC-001-DBOT seeded + project-create endpoint + project-list view + tenant_id RLS verified by integration test. |
| 29 | First end-to-end demo | Logged-in PMO_DIRECTOR sees KDMC project list. PROJECT_DIRECTOR sees subset. READ_ONLY sees redacted fields. Demo runs from `make demo`. |

After Round 29, sequence pivots to module deepening:

```
M34 deepening → M01 deepening → M02 → M03 → M04
```

Each module's deepening rounds follow the cadence: Brief decisions (already locked) → implement Spec entities → implement BRs → implement wireframes → implement workflows → integration tests → demo. Estimated 2-4 rounds per module.

## Appendix B — Local-dev quickstart contract (Round 25 must satisfy)

A new contributor (or future-Monish on a new laptop) executes:

```bash
git clone <repo>
cd EPCC
cp .env.example .env.local
make up          # docker-compose: postgres + redis + minio + keycloak
make migrate     # alembic upgrade head
make seed        # KDMC-001-DBOT + 17 role users
make dev         # starts uvicorn + vite in parallel
```

…and reaches a running EPCC at `http://localhost:5173` (frontend) calling `http://localhost:8000` (backend) within 5 minutes (excluding Docker pull time).

`make` targets to be defined in Round 25:

| Target | Purpose |
|---|---|
| `up` | docker-compose up |
| `down` | docker-compose down |
| `dev` | uvicorn + vite parallel |
| `migrate` | alembic upgrade head |
| `seed` | run `infra/seed/kdmc.py` |
| `test` | pytest + vitest |
| `e2e` | Playwright |
| `lint` | ruff + biome |
| `typecheck` | mypy + tsc |
| `codegen` | enums + api-types |
| `health` | curl `/api/v1/health` |
| `demo` | seed + dev + open browser |

---

*— Round 24 LOCKED 2026-05-03. Round 25 may begin.*
