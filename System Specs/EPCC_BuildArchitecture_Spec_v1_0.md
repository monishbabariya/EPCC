---
artefact: EPCC_BuildArchitecture_Spec_v1_0
round: 30
date: 2026-05-04
author: Monish (with Claude assist)
parent_brief: EPCC_BuildArchitecture_Brief_v1_0.md (Round 23)
x8_version: v0.6a
x9_version: v0.4
status: DRAFT
type: Build Governance Spec
re_issue_of: n/a (first lock — no legacy build governance spec existed)
locks_oq1: All 10 OQ-1 BuildArchitecture decisions (R23 → R30) per CLAUDE.md §4
references_locked: ES-DB-001 (schema-per-tenant), ES-DR-002 v1.2 (per-schema backup), ES-CICD-001/002 (7-stage pipeline), ES-SEC-004 (DPDPA 2023), Cadence C1b (2-Spec Buffer)
---

# EPCC Build Architecture — Spec v1.0

> **Type.** Build Governance Spec (not a module spec). Governs the technical build of EPCC: repo, scaffold, CI/CD, database, auth, codegen, and the path from spec to first running demo.
>
> **Authority.** This Spec locks the 10 OQ-1 decisions surfaced in `EPCC_BuildArchitecture_Brief_v1_0.md` (Round 23). The locked answers also live in `CLAUDE.md` §4 — both must agree; if they drift, CLAUDE.md wins.
>
> **Round numbering.** This is Round **30**. The Brief (parent) is Round 23. Pre-merge plan called this Spec "Round 24"; renumbered post-merge to avoid collision with Round 23–28 = M06 module work that landed in parallel. See `CLAUDE.md` §1 round-renumbering note + `EPCC_VersionLog_v1_0.md` §6 activity log.
>
> **Spec convention.** 10-block template (per `spec-protocol.md`), adapted for build governance — Block 3 is "Structure & Standards" instead of "Data Architecture" because there are no entities; Block 4 is "CI/CD Pipeline" instead of "Data Population Rules" because population is what the pipeline does.

---

## CHANGE LOG

| Version | Date | Author | Change Summary |
|---|---|---|---|
| v1.0 | 2026-05-04 | Monish (with Claude assist) | Initial Spec lock (Round 30). Locks all 10 OQ-1 BuildArchitecture decisions surfaced in Brief Round 23. Locks 6 OQ-2 carry-forward questions (BA-OQ-1 through BA-OQ-6) as Block 10 OQ-2 with Claude-recommended defaults. References ES-DB-001 schema-per-tenant + ES-DR-002 v1.2 per-schema backup + ES-CICD-001/002 7-stage pipeline + ES-SEC-004 DPDPA 2023 + Cadence C1b 2-Spec Buffer. Defines monorepo structure, pinned tech stack versions, schema-per-tenant database routing, Keycloak auth implementation, 8-stage GitHub Actions CI/CD pipeline, X8 → Python+TypeScript ENUM codegen pipeline, BR-tagged test convention with active-branch-scope calibration, thin-vertical-slice acceptance criteria for M34+M01, and 10 Architecture Decision Records (ADRs) to be created in Round 31. |

---

## BLOCK 1 — IDENTITY

```
Spec ID                  : EPCC-BUILD-ARCH-v1.0
Spec Name                : EPCC Build Architecture Spec
Type                     : Build Governance Spec (not a module spec)
Layer                    : Cross-cutting — Build Tooling & Governance
Decision It Enables      : "Can a developer (or AI assist) take a locked module
                            spec and produce running, tested, deployable code
                            without inventing architectural decisions?"
Primary User             : Lead Developer (first hire — currently Monish + AI assist)
Secondary Users          : SYSTEM_ADMIN (for tenant provisioning + Keycloak realm),
                            PMO_DIRECTOR (for governance audit trail)
Phase                    : 1 — Foundational (gates Phase 1 build)
Build Priority           : 🔴 Critical (blocks Round 31 scaffold + all downstream code)
Folder                   : System Specs/
Re-Issue Of              : n/a (first lock — no legacy build governance spec existed)
Re-Issue Or              : n/a (this is v1.0)
Source Brief             : EPCC_BuildArchitecture_Brief_v1_0.md (Round 23)
Cadence                  : C1 (Spec; one artefact at a time per spec-protocol.md)
Authority Tree           :
                            CLAUDE.md §4 Locked Decisions (OQ-1 BuildArchitecture row)
                            └── this Spec (Block 3-9 expand each OQ-1 to implementation detail)
                                ├── architecture.md §Multi-Tenancy → ES-DB-001 detail
                                ├── architecture.md §Tech Stack → version-locked toolchain
                                └── spec-protocol.md §Cadence C1b → batch rule for downstream
```

### Decisions It Enables (downstream rounds)

| Round | Artefact | Authority From This Spec |
|---|---|---|
| **R31** | Monorepo scaffold (`apps/`, `packages/`, `infra/`, `scripts/`, CI workflows) | Block 3a (folder layout) + Block 4 (CI pipeline shape) |
| **R32** | X8 → Python + TS ENUM codegen pipeline | Block 5 (codegen contract + CI Stage 3) |
| **R33** | M34 thin slice (auth + 17 roles + audit log) | Block 6 (acceptance criteria AC-1 to AC-3, AC-7) |
| **R34** | M01 thin slice (project create + read for KDMC-001-DBOT) | Block 6 (acceptance criteria AC-4 to AC-6, AC-8, AC-9) |
| **R35** | First end-to-end demo (KDMC-001-DBOT data load + UI render) | Block 6 (acceptance criteria AC-10) |

---

## BLOCK 2 — SCOPE BOUNDARY

### 2a. INCLUDES

| # | Item | Locked At |
|---|---|---|
| 1 | Monorepo folder structure (`apps/`, `packages/`, `infra/`, `scripts/`, `docs/`) | Block 3a |
| 2 | Pinned tech stack versions (Python 3.12, FastAPI 0.110.x, React 18.x, TypeScript 5.x, PostgreSQL 15.x, Redis 7.x, Keycloak 24.x — exact versions, not ranges) | Block 3b |
| 3 | Database strategy implementation — schema-per-tenant per ES-DB-001 (PostgreSQL `search_path` per request, `tenant_id` middleware injection) | Block 3c |
| 4 | Authentication implementation — Keycloak 24.x self-hosted, OIDC client config, 17-role realm seed, MFA enforcement for 5 MFA-required roles | Block 3d |
| 5 | CI/CD pipeline — GitHub Actions, 8 stages (lint → typecheck → enum-codegen-integrity → unit → BR-tagged-test gate → integration → build → e2e), required checks for `main` merge | Block 4 |
| 6 | ENUM codegen pipeline — X8 markdown → Python `StrEnum` + TypeScript `as const`; CI Stage 3 fails on hand-edit or stale generation | Block 5 |
| 7 | BR-tagged test convention — `test_BR_{module}_{seq}_*` naming, CI failure on missing test for any in-scope BR (calibrated to active-branch-scope per OQ-1.9) | Block 4a Stage 5 |
| 8 | Thin vertical slice definition — M34 + M01 scope, 10 acceptance criteria (AC-1 to AC-10) | Block 6 |
| 9 | First demo definition — KDMC-001-DBOT seed loads, multi-role visibility, CI all 8 stages green | Block 6 |
| 10 | Cascade-note → branch protocol — when a locked spec receives a cascade note, the matching code change lands in one PR with cascade-note path referenced | Block 4b |
| 11 | Architecture Decision Records (ADRs) — 10 ADRs to be created in Round 31, one per locked OQ-1 decision | Block 8 |

### 2b. EXCLUDES (out of scope for v1.0)

| # | Item | Reason / Where Addressed |
|---|---|---|
| 1 | Module specs not yet locked (M05, M07–M11, M13–M22, M24–M33, PF01–PF06) | Each module's own R-series spec round |
| 2 | Production hosting / cloud provider choice | Deferred per OQ-1.8; revisit after thin-slice ships and pilot pressure surfaces |
| 3 | KDMC workbook → EPCC full migration | HDI module future spec round; the seed script (Block 5 / Block 7) is HDI v0.1 prototype only |
| 4 | PIOE engine implementation (L0 Strategic — Phase 2) | Phase 2 |
| 5 | External party portal (PF03 ExternalPartyPortal) | Phase 2 |
| 6 | Kubernetes manifests | Deferred per OQ-1.8 to actual scale pressure (>1 tenant or perf constraint) |
| 7 | Performance benchmarking | Post-thin-slice, gated by R35 demo acceptance |
| 8 | Security penetration testing | Pre-production gate (not thin-slice scope) |
| 9 | Multi-region deployment | Phase 3 (per ES-DR roadmap §7.126) |
| 10 | Observability stack (logs / metrics / traces concrete tooling) | First-module-live + 2 weeks per Brief §10 |
| 11 | Mobile / offline strategy | Phase 2 (PF01 MobileFieldPlatform) |
| 12 | LLM gateway / AI features (M10, M26, M29) | Phase 3+ per Standards Memory §7 |
| 13 | 4 unresolved KDMC workbook items (PKG-to-WBS mapping, Snapshot macro, Named range rollout, Progress_Calc % integration) | Tracked separately per CLAUDE.md §2 |

### 2c. Hard Boundaries (must-not-cross during build)

1. **No code change without spec authority.** Every PR must reference a locked spec section, BR code, ADR, or cascade note. Anti-drift rule (mirrors Round 18 + Round 29 audit discipline).
2. **No re-litigation of locked OQ-1 answers.** The 10 decisions in CLAUDE.md §4 row "OQ-1 BuildArchitecture (R23→R30)" are LOCKED. Re-open only via new Brief round + explicit deliberation.
3. **No hand-editing of generated files.** Files in `apps/api/src/epcc_api/x_series/enums/` and `apps/web/src/x_series/enums/` and `packages/api-types/` are codegen output. CI Stage 3 enforces.
4. **No long-lived environment branches.** Per OQ-1.2 + ES-CICD-001. Only `main` + short-lived `feat/`, `fix/`, `audit/`, `round/` branches (< 1 week lifetime).
5. **No cross-tenant queries.** Per ES-DB-001, application code MUST NOT explicitly schema-qualify across tenant boundaries except in the system-tenant context (Tenant registry, CodeMaster global).

---

## BLOCK 3 — STRUCTURE & STANDARDS

### 3a. Monorepo Layout (locks OQ-1.1)

The repository is a single monorepo on `main` with the following canonical layout. Round 31 (scaffold) implements this verbatim; deviations require an ADR.

```
EPCC/
├── CLAUDE.md                                        # global project context (existing)
├── .claude/                                         # rules + skills (existing)
│   ├── rules/
│   │   ├── architecture.md
│   │   ├── spec-protocol.md
│   │   ├── naming-folders.md
│   │   ├── cross-cutting-standards.md
│   │   ├── glossary.md
│   │   ├── principles.md
│   │   └── re-entry-protocol.md
│   └── skills/
├── .github/
│   └── workflows/
│       ├── ci.yml                                   # 8-stage pipeline (Block 4a)
│       ├── enum-codegen-check.yml                   # CI Stage 3 (X8 freshness)
│       └── br-test-gate.yml                         # CI Stage 5 (BR coverage)
├── .gitignore                                       # extended for Python + Node + IDE
├── .python-version                                  # pin: 3.12.x
├── .nvmrc                                           # pin: 20.x LTS
├── README.md                                        # repo-level developer entry
├── Makefile                                         # `make up`, `make seed`, `make test`, etc.
│
├── SystemAdmin/                                     # module specs (existing — untouched by this round)
│   ├── M34_SystemAdminRBAC_*.md                     # M34 at root (grandfathered)
│   ├── Modules/                                     # M01+ canonical placement
│   │   ├── M01_ProjectRegistry_*.md
│   │   ├── M02_StructureWBS_*.md
│   │   ├── M03_PlanningMilestones_*.md
│   │   ├── M04_ExecutionCapture_*.md
│   │   ├── M06_FinancialControl_*.md
│   │   └── (cascade notes)
│   └── Cross-link files/                            # X-series living docs
│       ├── X8_GlossaryENUMs_v0_6.md
│       └── X9_VisualisationStandards_Spec_v0_4.md
│
├── System Specs/                                    # governance + audits (existing)
│   ├── EPCC_BuildArchitecture_Brief_v1_0.md
│   ├── EPCC_BuildArchitecture_Spec_v1_0.md          # this file
│   ├── EPCC_NamingConvention_v1_0.md
│   ├── EPCC_FolderIndex_v1_0.md
│   ├── EPCC_VersionLog_v1_0.md
│   ├── EPCC_LegacyManifest_v1_0.md
│   ├── EPCC_DevSkillsRequired_v1_0.md
│   └── AUDIT_Round00_ExistingSpecs_v1_0.md
│
├── ZEPCC_Legacy/                                    # frozen historical (existing)
│   ├── EPCC_Standards_Memory_v5_3.md                # ES-XX-XXX locked items still authoritative
│   ├── EPCC_Deployment_Tier_Specification_v1_0.md
│   ├── EPCC_Engineering_Standards_v1_2.md
│   └── (frozen module specs)
│
├── apps/
│   ├── api/                                         # FastAPI backend
│   │   ├── pyproject.toml                           # uv-managed; pins all versions
│   │   ├── uv.lock                                  # transitive lockfile
│   │   ├── alembic.ini
│   │   ├── ruff.toml
│   │   ├── mypy.ini
│   │   ├── pytest.ini
│   │   ├── src/
│   │   │   └── epcc_api/
│   │   │       ├── __init__.py
│   │   │       ├── main.py                          # FastAPI app entry
│   │   │       ├── core/                            # shared cross-module
│   │   │       │   ├── auth/                        # OIDC client, JWT decode, role check
│   │   │       │   ├── config/                      # settings (12-factor; env-driven)
│   │   │       │   ├── db/                          # SQLAlchemy engine, session, search_path mw
│   │   │       │   ├── exceptions/                  # canonical error types
│   │   │       │   ├── audit/                       # audit-log emission shared
│   │   │       │   ├── tenancy/                     # tenant_id middleware (ES-DB-001)
│   │   │       │   └── deps/                        # FastAPI dependency factories
│   │   │       ├── modules/                         # one folder per locked module spec
│   │   │       │   ├── m34_system_admin_rbac/
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   ├── routes.py                # FastAPI router
│   │   │       │   │   ├── models.py                # SQLAlchemy ORM
│   │   │       │   │   ├── schemas.py               # Pydantic v2
│   │   │       │   │   ├── service.py               # business logic
│   │   │       │   │   ├── repository.py            # DB access
│   │   │       │   │   ├── internal_api.py          # cross-module surface (BA-OQ-6)
│   │   │       │   │   └── tests/                   # module-local tests (BR + non-BR)
│   │   │       │   ├── m01_project_registry/
│   │   │       │   ├── m02_structure_wbs/
│   │   │       │   ├── m03_planning_milestones/
│   │   │       │   ├── m04_execution_capture/
│   │   │       │   └── m06_financial_control/
│   │   │       └── x_series/
│   │   │           ├── __init__.py
│   │   │           └── enums/                       # X8 codegen output — DO NOT HAND-EDIT
│   │   │               ├── __init__.py              # re-exports all ENUMs
│   │   │               └── (one .py per ENUM module)
│   │   ├── alembic/                                 # migrations
│   │   │   ├── env.py                               # search_path-aware multi-schema
│   │   │   └── versions/
│   │   └── tests/
│   │       ├── unit/                                # per-module fast tests
│   │       ├── integration/                         # multi-module + DB
│   │       └── conftest.py                          # pytest-postgresql fixture
│   │
│   └── web/                                         # React frontend
│       ├── package.json                             # pnpm-managed; pins all versions
│       ├── pnpm-lock.yaml
│       ├── tsconfig.json                            # strict null checks
│       ├── vite.config.ts
│       ├── tailwind.config.js
│       ├── biome.json
│       ├── playwright.config.ts
│       ├── src/
│       │   ├── main.tsx
│       │   ├── App.tsx
│       │   ├── routes/                              # React Router 6.x route tree
│       │   ├── modules/                             # mirrors apps/api/modules
│       │   │   ├── m34/
│       │   │   ├── m01/
│       │   │   ├── m02/
│       │   │   └── ...
│       │   ├── core/                                # shared
│       │   │   ├── auth/                            # Keycloak adapter, OIDC PKCE flow
│       │   │   ├── api-client/                      # OpenAPI-generated client wrapper
│       │   │   ├── layouts/                         # role-aware layout shell
│       │   │   └── components/                      # shadcn/ui + custom
│       │   └── x_series/
│       │       └── enums/                           # X8 codegen output (TS) — DO NOT HAND-EDIT
│       └── tests/
│           ├── unit/                                # vitest + RTL
│           └── e2e/                                 # playwright (CI Stage 8)
│
├── packages/
│   ├── epcc-types/                                  # shared TS types (OpenAPI codegen)
│   │   ├── package.json
│   │   ├── src/
│   │   │   └── api-types.ts                        # GENERATED from OpenAPI
│   │   └── README.md
│   └── (future: shared utilities, design tokens)
│
├── infra/
│   ├── docker/
│   │   ├── compose.dev.yml                          # postgres + redis + minio + keycloak (dev)
│   │   ├── compose.test.yml                         # CI overlay
│   │   ├── compose.prod-pilot.yml                   # single-VPS pilot deploy
│   │   ├── api.Dockerfile
│   │   └── web.Dockerfile
│   ├── keycloak/
│   │   ├── realm-export.json                        # KDMC realm + 17 roles + dev users
│   │   └── README.md                                # how to refresh export
│   ├── postgres/
│   │   ├── init.sql                                 # public schema bootstrap
│   │   └── README.md
│   └── seed/
│       ├── kdmc_seed.py                             # HDI v0.1 prototype (OQ-1.6)
│       └── README.md                                # how to extend for new tenants
│
├── scripts/
│   ├── codegen-enums.py                             # X8 → Python + TS (OQ-1.10)
│   ├── codegen-api-types.py                         # OpenAPI → packages/epcc-types/
│   ├── check-br-coverage.py                         # CI Stage 5 enforcer (OQ-1.9)
│   └── lint-spec-stamps.py                          # validates audit-stamp formats per spec-protocol.md
│
└── docs/
    ├── adr/                                         # Architecture Decision Records
    │   ├── ADR-001-monorepo.md                      # OQ-1.1
    │   ├── ADR-002-branch-model.md                  # OQ-1.2
    │   ├── ADR-003-thin-slice.md                    # OQ-1.3
    │   ├── ADR-004-keycloak.md                      # OQ-1.4
    │   ├── ADR-005-schema-per-tenant.md             # OQ-1.5 + ES-DB-001
    │   ├── ADR-006-hdi-prototype.md                 # OQ-1.6
    │   ├── ADR-007-github-actions.md                # OQ-1.7
    │   ├── ADR-008-docker-compose.md                # OQ-1.8
    │   ├── ADR-009-br-test-scope.md                 # OQ-1.9
    │   ├── ADR-010-enum-codegen.md                  # OQ-1.10
    │   └── README.md
    └── runbooks/                                    # ops procedures (per-tenant restore, etc.)
```

#### 3a.1 Layout Invariants (must hold after Round 31 scaffold)

| Invariant | Rationale |
|---|---|
| `apps/api/src/epcc_api/modules/m{XX}_{name}/` mirrors `SystemAdmin/Modules/M{XX}_{Name}_Spec_v1_0.md` 1:1 | New engineer reads spec → finds code in seconds; cascade location is obvious |
| `apps/web/src/modules/m{XX}/` mirrors backend module layout | Same rationale on the web side |
| `apps/api/src/epcc_api/x_series/enums/` is **generated only**; no hand-edit | Anti-drift; CI Stage 3 enforces |
| `apps/web/src/x_series/enums/` is **generated only** | Same |
| `packages/epcc-types/src/api-types.ts` is **generated only** (from OpenAPI) | Same |
| `infra/keycloak/realm-export.json` is the source of truth for the 17-role realm; manual Keycloak UI changes must be re-exported and committed | Reproducibility across dev / CI / prod-pilot |
| `infra/seed/kdmc_seed.py` is idempotent (safe to re-run) | Dev workflow + CI integration tests |
| Module-local tests in `apps/api/src/epcc_api/modules/m{XX}/tests/` are unit; cross-module + DB-integration tests live in `apps/api/tests/integration/` | Fast unit tests stay close to code; integration tests share fixtures |

### 3b. Pinned Tech Stack Versions (locks OQ-2 pattern defaults from Brief §4)

> All versions are **exact pins** at Round 30 lock. CI integrity stage validates lockfile hashes (`uv.lock`, `pnpm-lock.yaml`, `compose` digests). Library upgrades are explicit PRs with their own ADR.

#### 3b.1 Backend (Python)

| Package | Version | Pinned In | Notes |
|---|---|---|---|
| python | **3.12.x** (latest patch) | `.python-version` | Stable; type-system mature; `StrEnum` available natively |
| uv | latest stable at scaffold | `.github/workflows/ci.yml` | Package manager — replaces pip/pip-tools/poetry; 10–100× faster |
| fastapi | **0.110.x** | `pyproject.toml` | Locked stack; OpenAPI 3.1 emission for free |
| uvicorn | latest stable | `pyproject.toml` | Dev server (`--reload`) |
| gunicorn | latest stable | `pyproject.toml` | Prod worker (`gunicorn -k uvicorn.workers.UvicornWorker`) |
| sqlalchemy | **2.x** | `pyproject.toml` | Async patterns only (`AsyncEngine`, `AsyncSession`) |
| alembic | latest stable | `pyproject.toml` | Schema-per-tenant migration support (Block 3c.3) |
| pydantic | **2.x** | `pyproject.toml` | Strict mode (`model_config = ConfigDict(strict=True)`) |
| celery | **5.x** | `pyproject.toml` | Broker = Redis; DLQ per ES-BL-006 |
| redis | latest stable client | `pyproject.toml` | Broker + cache layer |
| boto3 | latest stable | `pyproject.toml` | S3-compatible against MinIO; swappable to AWS S3 in prod |
| authlib | latest stable | `pyproject.toml` | OIDC client; integrates with Keycloak |
| pytest | latest stable | `pyproject.toml` | Test runner |
| pytest-asyncio | latest stable | `pyproject.toml` | Async test support (auto mode) |
| pytest-postgresql | latest stable | `pyproject.toml` | Real Postgres in CI (catches RLS/migration bugs SQLite hides) |
| httpx | latest stable | `pyproject.toml` | Async HTTP client; FastAPI test client |
| ruff | latest stable | `pyproject.toml` | Lint + format (replaces black/isort/flake8) |
| mypy | latest stable | `pyproject.toml` | `--strict` on `apps/api/src/`; relaxed in tests |

#### 3b.2 Frontend (Node)

| Package | Version | Pinned In | Notes |
|---|---|---|---|
| node | **20.x LTS** | `.nvmrc` | Match LTS; matches Vite 5 + TS 5 ecosystem |
| pnpm | latest stable | `package.json` `packageManager` field | Disk-efficient + workspace support |
| react | **18.x** | `package.json` | |
| typescript | **5.x** | `package.json` | `strict: true` + `strictNullChecks: true` |
| vite | **5.x** | `package.json` | Bundler + dev server |
| react-router-dom | **6.x** | `package.json` | |
| @tanstack/react-query | **5.x** | `package.json` | Server state |
| @tanstack/react-table | **8.x** | `package.json` | Tables (M01 project list, M02 BOQ, etc.) |
| zustand | latest stable | `package.json` | Client state (lightweight; preferred over Redux) |
| react-hook-form | latest stable | `package.json` | Forms (paired with zod) |
| zod | latest stable | `package.json` | Runtime schema validation; aligns with Pydantic |
| tailwindcss | **3.x** | `package.json` | Locked per wireframe convention (D3 lock) |
| shadcn/ui | copy-into-repo | n/a | Radix + Tailwind primitives; no runtime dep |
| recharts | **3.x** | `package.json` | Locked X9 v0.4 |
| frappe-gantt | **0.7.x** | `package.json` | Locked X9 v0.4 |
| react-flow | **12.x** | `package.json` | Locked X9 v0.4 |
| vitest | latest stable | `package.json` | Unit tests (matches Vite) |
| @testing-library/react | latest stable | `package.json` | Component tests |
| playwright | latest stable | `package.json` | E2E (CI Stage 8) |
| biome | latest stable | `package.json` | Lint + format (replaces ESLint + Prettier) |
| openapi-typescript | latest stable | `package.json` (devDep) | Codegen TS types from OpenAPI 3.1 |
| openapi-fetch | latest stable | `package.json` | Type-safe API client |

#### 3b.3 Infrastructure

| Component | Version | Pinned In | Notes |
|---|---|---|---|
| postgresql | **15.x** | `infra/docker/compose.*.yml` | Major version locked; minor updates via PR |
| redis | **7.x** | `infra/docker/compose.*.yml` | Broker + cache |
| minio | latest stable | `infra/docker/compose.*.yml` | S3-compat object storage |
| keycloak | **24.x** | `infra/docker/compose.*.yml` | Latest LTS at Spec lock; OIDC + MFA + 17-role realm |
| docker | host-version | `Makefile` (version-check) | Compose v2 syntax assumed |

#### 3b.4 Version Bump Discipline

Library upgrades follow this protocol:

1. **Minor / patch bump** (e.g., FastAPI 0.110.0 → 0.110.5): single-line PR; CI runs full pipeline; merged on green.
2. **Major bump** (e.g., Recharts 3.x → 4.x): full ADR (`docs/adr/ADR-XXX-{lib}-{version}.md`) covering breaking changes; visual regression on flagship charts (Capital Funnel + others); separate PR.
3. **Security patch**: bypass ADR; commit immediately to `main` with `security:` prefix; reference CVE.

### 3c. Database Strategy — Schema-Per-Tenant (locks OQ-1.5; references ES-DB-001)

> **Authoritative reference:** `ZEPCC_Legacy/EPCC_Standards_Memory_v5_3.md` §7.137 (ES-DB-001 — STATUS: CONFIRMED. LOCKED. CLOSED.) + `.claude/rules/architecture.md` §Multi-Tenancy.

#### 3c.1 Connection Routing (`tenant_id` middleware → `search_path`)

Every authenticated request flows through this pipeline:

```
Request arrives → FastAPI middleware chain:
  1. AuthMiddleware (apps/api/src/epcc_api/core/auth/middleware.py)
       Decodes JWT (Keycloak-issued)
       Extracts: tenant_id (UUID), user_id, roles[], project_ids[]
       Attaches to request.state

  2. TenancyMiddleware (apps/api/src/epcc_api/core/tenancy/middleware.py)
       Reads request.state.tenant_id
       Looks up Tenant.db_schema_name (cached; cache invalidates on tenant_status change)
       Sets PostgreSQL session variable:
         await session.execute(text(f'SET LOCAL search_path TO "{schema_name}", public'))
       Cross-tenant query is now physically impossible without explicit qualification

  3. AuditContextMiddleware (apps/api/src/epcc_api/core/audit/middleware.py)
       Stashes (tenant_id, user_id, request_id) in contextvars
       Audit-log emitter reads from contextvars (no per-call plumbing)

Route handler runs.
  All ORM queries automatically scoped to the tenant's schema.

Response → middleware unwinds → contextvars cleared.
```

**Failure modes handled explicitly:**

| Failure | Behaviour |
|---|---|
| JWT missing or invalid | 401 Unauthorized; no DB session created |
| `tenant_id` claim missing from valid JWT | 403 Forbidden + audit-log `AUTH_TENANT_CLAIM_MISSING` |
| `tenant_id` references non-existent or suspended Tenant | 403 Forbidden + audit-log `AUTH_TENANT_INVALID_OR_SUSPENDED` |
| Tenant exists but `db_schema_name` schema doesn't exist in Postgres | 500 + audit-log `TENANT_SCHEMA_MISSING` (operational alert) |
| `search_path` SET fails (DB error) | 500 + audit-log `TENANT_SCHEMA_ROUTING_FAILED` |

#### 3c.2 Schema Provisioning

| Operation | Trigger | Mechanism |
|---|---|---|
| **Create tenant schema** | `Tenant.status` transitions Draft → Active (M34 BR) | Operational job: `CREATE SCHEMA t_{tenant_code_lower};` then `alembic upgrade head` against new schema |
| **Suspend tenant** | `Tenant.status` → Suspended | Auth middleware blocks access; schema retained intact |
| **Archive tenant** | `Tenant.status` → Archived | Schema renamed `archived_t_{tenant_code_lower}_{date}`; readable only by SYSTEM_ADMIN escape hatch |
| **Drop tenant** | Explicit operator action with PMO_DIRECTOR sign-off | `DROP SCHEMA t_{tenant_code_lower} CASCADE` after final per-tenant backup |
| **Per-tenant restore** | DR drill or incident | Per ES-DR-002 v1.2: `pg_restore` schema-scoped backup; zero impact on other tenants |

**Tenant entity field — `db_schema_name`** (per M34 Spec Block 3b):

- Auto-derived: `t_{tenant_code_lower}` (e.g., `KDMC` → `t_kdmc`)
- Validated: PostgreSQL identifier rules (`^[a-z][a-z0-9_]{0,62}$`), lowercase, no reserved words
- Immutable post-creation (renaming a tenant requires a new tenant + data migration; M34 enforces)

#### 3c.3 Alembic Migration Strategy

Multi-schema migration loop (`apps/api/alembic/env.py`):

```python
# Pseudocode — actual implementation in Round 31
def run_migrations_online():
    config = context.config
    target_metadata = Base.metadata

    # Phase 1: public schema (system tables)
    with engine.connect() as conn:
        conn.execute(text("SET search_path TO public"))
        context.configure(connection=conn, target_metadata=target_metadata,
                          include_schemas=True, version_table_schema="public")
        context.run_migrations()

    # Phase 2: each active tenant schema
    active_schemas = list_active_tenant_schemas(conn)  # SELECT db_schema_name FROM public.tenant
    for schema in active_schemas:
        with engine.connect() as conn:
            conn.execute(text(f'SET search_path TO "{schema}", public'))
            context.configure(connection=conn, target_metadata=target_metadata,
                              version_table_schema=schema)
            context.run_migrations()
```

**Operational invariant:** every Alembic revision MUST be schema-agnostic. Forbidden: hardcoded schema names in migrations.

#### 3c.4 `tenant_id` Reserved Field — Purpose Clarified

Per `naming-folders.md` §Reserved Fields, every entity (except 7 append-only ledger exemptions per X8 §6) carries `tenant_id`. Under schema-per-tenant, this field is **NOT used for row-level filtering** (search_path already isolates rows physically). It is retained for:

| Purpose | Trigger |
|---|---|
| **Sub-tenant federation** | Future requirement: a parent tenant has child sub-tenants who share parent schema but need scoped views (e.g., a regional PMO with branch offices) |
| **JV (Joint Venture) structures** | Multiple parent tenants temporarily share data within a JV-scoped schema; `tenant_id` records the originating tenant |
| **Cross-schema reporting** | Future analytics layer that aggregates across tenants for benchmarking (anonymised) |
| **Audit trail integrity** | Audit logs federated into a system schema retain `tenant_id` for forensics |

**Operational rule:** application code MUST set `tenant_id = request.state.tenant_id` at record creation. Cross-tenant query is allowed only in:
- `public` schema (system tables: Tenant, CodeMaster global)
- Future analytics layer (Phase 2+) with explicit schema-qualification + audit-log entry

### 3d. Authentication — Keycloak Self-Hosted (locks OQ-1.4)

> **Authoritative reference:** `M34_SystemAdminRBAC_Spec_v1_0a` Block 3 (17-role taxonomy, 5 MFA-required roles) + `architecture.md` §Tech Stack (Keycloak self-hosted).

#### 3d.1 Keycloak Realm Configuration

| Item | Value |
|---|---|
| Keycloak version | 24.x (latest LTS at Spec lock) |
| Deployment | Docker Compose container (`infra/docker/compose.*.yml`) |
| Realm name | `epcc` |
| Realm export | `infra/keycloak/realm-export.json` (committed; source of truth) |
| Refresh procedure | UI changes → export realm → commit JSON; never hand-edit JSON |
| Client (web) | `epcc-web` — public client, PKCE flow, redirect URIs configured per env |
| Client (api) | `epcc-api` — confidential client, client_credentials flow for service-to-service |
| Realm roles | 17 (exact match to M34 ENUMs): SYSTEM_ADMIN, PMO_DIRECTOR, PORTFOLIO_MANAGER, PROJECT_DIRECTOR, PLANNING_ENGINEER, QS_MANAGER, FINANCE_LEAD, PROCUREMENT_OFFICER, SITE_MANAGER, COMPLIANCE_MANAGER, ANALYST, READ_ONLY, EXTERNAL_AUDITOR, CLIENT_VIEWER, LENDER_VIEWER, NABH_ASSESSOR, CONTRACTOR_LIMITED |
| MFA-required roles | 5: SYSTEM_ADMIN, PMO_DIRECTOR, PORTFOLIO_MANAGER, FINANCE_LEAD, EXTERNAL_AUDITOR — TOTP enrolment required at first login |
| Local password fallback | Native Keycloak Username/Password flow (M34 spec requirement) |

#### 3d.2 JWT Claims Contract

The JWT issued by Keycloak to `epcc-web` and `epcc-api` carries:

| Claim | Type | Source | Used By |
|---|---|---|---|
| `sub` | UUID | Keycloak | `user_id` mapping |
| `tenant_id` | UUID | Keycloak custom claim (mapped from user attribute) | TenancyMiddleware |
| `roles` | string[] | Keycloak realm roles | RBAC dependency factories |
| `project_ids` | UUID[] (optional) | Keycloak custom claim (project assignments) | M01 own-project filtering |
| `mfa_satisfied` | boolean | Keycloak (TOTP step-up) | M34 MFA gate dependency |
| `iat`, `exp`, `iss`, `aud` | standard | Keycloak | authlib validation |

**Token expiry:** access token 15 min; refresh token 8 hr (configurable per env in `realm-export.json`).

#### 3d.3 M34 Auth Service Layer

All module code calls into a thin abstraction at `apps/api/src/epcc_api/core/auth/`:

```
core/auth/
  client.py           # authlib client; Keycloak discovery
  middleware.py       # extract JWT from Authorization header → request.state
  dependencies.py     # FastAPI deps: require_role(), require_any_role(), require_mfa()
  exceptions.py       # AuthError, InsufficientRole, MFARequired
  __init__.py         # re-exports
```

**Module code never imports `authlib` or `keycloak-py` directly.** This makes Phase 2 IdP-swap (Auth0, Entra) a single-file change.

### 3e. Cross-Cutting Implementation Patterns

| Pattern | Location | Module Code Convention |
|---|---|---|
| Audit log emission | `apps/api/src/epcc_api/core/audit/` | Decorator `@emit_audit("EVENT_TYPE")` on service methods OR explicit `audit.emit(...)` for runtime branches |
| Tenant context (read-only) | `apps/api/src/epcc_api/core/tenancy/` | `current_tenant_id()` contextvar accessor |
| User context (read-only) | `apps/api/src/epcc_api/core/auth/` | `current_user_id()` contextvar accessor |
| Decision Queue trigger emission | (lives per-module; M11 ActionRegister consumes) | Service-layer call to `decision_queue.raise(...)` |
| Soft-delete guard | `apps/api/src/epcc_api/core/db/` | Base SQLAlchemy mixin with `is_active` + automatic `WHERE is_active = TRUE` filter (overridable for SYSTEM_ADMIN audit views) |
| Append-only-ledger guard | `apps/api/src/epcc_api/core/db/` | DB-level: `REVOKE UPDATE, DELETE` on ledger tables (BACIntegrityLedger, IDGovernanceLog, CSVImportRecord, ProjectPhaseHistory, ProjectStatusHistory, LoginAttempt, SystemAuditLog, Baseline, BaselineExtension, PVProfileSnapshot, ProgressEntryAudit, NCRStatusLog, MaterialReceiptLedger, ContractorPerformanceScoreLog, CostLedgerEntry, RABillAuditLog, PaymentEvidenceLedger, ForexRateLog) per X8 §6 + naming-folders.md |
| `tenant_id` injection | `apps/api/src/epcc_api/core/db/` | SQLAlchemy event listener on `before_insert`: sets `tenant_id` from contextvar |
| Reserved fields injection | `apps/api/src/epcc_api/core/db/` | Same listener: `created_by`, `created_at`, `updated_by`, `updated_at`, `is_active=True` |

---

## BLOCK 4 — CI/CD PIPELINE (locks OQ-1.7 + OQ-1.9)

> **Authoritative reference:** `ZEPCC_Legacy/EPCC_Standards_Memory_v5_3.md` §7.127 ES-CICD-001/002 (7-stage pipeline) — this Spec extends to **8 stages** by inserting CI Stage 5 (BR-tagged-test gate, OQ-1.9-calibrated).

### 4a. Pipeline Stages

**Trigger:** every push to any branch + every PR to `main`.

**Total target time:** < 40 min (feature branches skip Stage 8; main-merge runs all 8).

| Stage | Name | Time Budget | Tooling | Failure Mode |
|---|---|---|---|---|
| 1 | Lint + Format | < 2 min | Backend: `ruff check` + `ruff format --check` · Frontend: `biome check` | Any lint error → block merge |
| 2 | Type Check | < 3 min | Backend: `mypy --strict apps/api/src/` · Frontend: `tsc --noEmit` | Any type error → block merge |
| 3 | ENUM Codegen Integrity | < 1 min | `python scripts/codegen-enums.py --check` (regenerates to temp dir, diffs against committed) | Any diff (X8 bumped without re-run, OR generated file hand-edited) → block merge |
| 4 | Unit Tests | < 5 min | Backend: `pytest apps/api/tests/unit/ --cov=apps/api/src/ --cov-fail-under=80` · Frontend: `vitest run apps/web/src/` | Coverage < 80% OR any test fail → block merge |
| 5 | **BR-Tagged Test Gate** | < 2 min | `python scripts/check-br-coverage.py --scope={active_modules}` | Any in-scope BR without matching `test_BR_{module}_{seq}_*` test → block merge |
| 6 | Integration Tests | < 10 min | `pytest apps/api/tests/integration/` (uses `pytest-postgresql` ephemeral DB; real Postgres) | Any integration test fail → block merge |
| 7 | Build | < 5 min | Backend: `python -m build` (package check) · Frontend: `pnpm build` (Vite production bundle) | Any build error → block merge |
| 8 | E2E (main only) | < 15 min | `playwright test` against Docker Compose stack (M34 + M01 thin slice) | Any e2e fail → block merge to `main`; not required for feature branches |

#### 4a.1 Stage 5 — BR-Tagged Test Gate Detail (OQ-1.9 — calibrated to active-branch-scope)

**Naming convention:** `test_BR_{module:02d}_{seq:03d}_{description_snake_case}`

Examples:
```
test_BR_01_024_project_status_transitions_draft_to_active
test_BR_06_028_dlp_retention_release_blocked_by_open_defects
test_BR_34_005_mfa_required_for_finance_lead_role
```

**Active-branch-scope logic** (per OQ-1.9 calibration):

```python
# Pseudocode — actual implementation in Round 31 (scripts/check-br-coverage.py)
def check_br_coverage(active_modules: list[str]) -> int:
    """
    Returns 0 (pass) or 1 (fail).

    For each module in active_modules:
      Parse {module}_*_Spec_v1_*.md for BR-XX-YYY codes.
      Find tests matching test_BR_{XX}_{YYY}_* in apps/api/tests/.
      Fail if any in-scope BR has no matching test.

    Modules NOT in active_modules are skipped (their BRs may be unimplemented).
    """
```

**Active-modules definition by phase:**

| Phase | Active Modules | BR Count Approx |
|---|---|---|
| Round 33 (M34 thin slice) | M34 only | ~30 BRs |
| Round 34 (M01 thin slice added) | M34 + M01 | ~66 BRs total |
| Round 35 (first demo) | M34 + M01 (frozen scope) | ~66 BRs |
| Round 36+ (M02 deepening) | M34 + M01 + M02 | ~90 BRs |
| ... incrementally per module merge into thin slice | | |

**Scope file:** `apps/api/tests/active_modules.yaml` — committed; updated as part of each module-merge PR; referenced by `check-br-coverage.py`.

#### 4a.2 Coverage Floors

| Test Type | Floor | Enforced In |
|---|---|---|
| Unit-test line coverage on `apps/api/src/` | 80% | Stage 4 (`--cov-fail-under=80`) |
| Unit-test line coverage on `apps/web/src/` | 70% (lower because UI logic is harder to unit-test; e2e covers behavior) | Stage 4 (Vitest config) |
| BR-tagged test count (in-scope BRs with matching test) | 100% | Stage 5 |
| E2E acceptance criteria coverage | 100% on AC-1 to AC-10 | Stage 8 (Playwright) |

### 4b. Branch + Cascade Protocol (locks OQ-1.2)

#### 4b.1 Branch Types

| Branch | Pattern | Lifetime | Use |
|---|---|---|---|
| `main` | trunk | permanent | Production-ready; all PRs merge here; governance commits land directly per Round 29 precedent |
| `feat/{slug}` | `feat/m34-user-create`, `feat/m01-create-project` | < 1 week | Feature work; merged via PR |
| `fix/{slug}` | `fix/keycloak-mfa-prompt`, `fix/m01-status-transition-bug` | < 3 days | Bug fixes |
| `audit/{slug}` | `audit/round-29-remediation`, `audit/round-29-cascade-notes` | < 2 weeks | Audit remediation passes (pattern from Round 29) |
| `round/{n}` | `round/30-build-arch-spec`, `round/31-scaffold` | < 1 week | Spec artefact rounds (no code; spec files only) |

**No long-lived environment branches.** Per OQ-1.2 + ES-CICD-001 + Brief §3 OQ-1.2 Option A. `main` is always deployable.

#### 4b.2 Merge to `main` Rules

- **All PRs**: required status checks (Stages 1–7) must pass; Stage 8 required only for PRs to `main`.
- **Governance commits** (CLAUDE.md §4 lock updates, .claude/rules/* changes, System Specs/* governance docs): may land directly on `main` without PR per Round 29 precedent. CI runs on the commit; failure rolls forward via fix-commit (no force-push).
- **Module thin-slice work**: PR required; one reviewer may be Claude-assist if Monish-as-author.
- **No force-push to `main`** (Git Safety Protocol).
- **No direct `main` commits except** governance class above. Code changes go through feat/fix branches.

#### 4b.3 Cascade-Note → Branch Protocol

When a locked spec receives a cascade note, the matching code change is required to land in lockstep. Protocol:

```
Step 1: Cascade note authored on a feat/ or audit/ branch
        File: SystemAdmin/Modules/M{XX}_{Name}_v{x}_{y}_CascadeNote.md
        Round: tagged in cascade note's Trigger field
        Status: Cascade Patch | LOCKED

Step 2: Code changes paired in the SAME branch (or a paired feat/ branch
         opened simultaneously, merged in coordinated PRs):
        - Alembic migration if field add/remove
        - Pydantic model update (apps/api/.../schemas.py)
        - SQLAlchemy ORM update (.../models.py)
        - Zod schema update (apps/web/.../schema.ts)
        - Affected BR-tagged test updates
        - Generated files re-run if X8 affected

Step 3: PR description MUST reference:
        - Cascade note path (e.g., `M01_v1_5_CascadeNote.md`)
        - Finding ID(s) closed (e.g., `closes H21, closes M27`)
        - List of BR codes touched
        - Migration name (if any)

Step 4: CI must pass all 8 stages including BR-tagged gate (Stage 5)

Step 5: Merge to main → cascade note + code change land atomically
```

**Failure mode protection:** if a cascade note is merged without paired code changes, the BR-tagged test gate (Stage 5) detects the new BR with no test and blocks future merges until the code lands. This is exactly the "drift detection" property the audit discipline is designed to enforce.

---

## BLOCK 5 — ENUM CODEGEN PIPELINE (locks OQ-1.10)

### 5a. Source of Truth

| Item | Value |
|---|---|
| Authoritative source | `SystemAdmin/Cross-link files/X8_GlossaryENUMs_v0_6.md` (current content version v0.6a — in-place patched R29; filename retained per in-place patch convention) |
| ENUM count at lock | ~75 ENUMs across §3 (system + module-owned) and §4 (M34-owned event types + decision-queue triggers) |
| Version-bump trigger | Every X8 minor (v0.X) and letter-suffix patch (v0.6a, v0.6b) requires re-run |

### 5b. Codegen Script — `scripts/codegen-enums.py`

#### 5b.1 Inputs

| Input | Type | Source |
|---|---|---|
| X8 markdown path | CLI arg `--source`, default `SystemAdmin/Cross-link files/X8_GlossaryENUMs_v0_6.md` | This Spec |
| Output Python dir | CLI arg `--py-out`, default `apps/api/src/epcc_api/x_series/enums/` | Block 3a |
| Output TypeScript dir | CLI arg `--ts-out`, default `apps/web/src/x_series/enums/` | Block 3a |
| Mode | `--check` (validate; non-zero exit on diff) or `--write` (regenerate) | This Spec |

#### 5b.2 Output Format — Python

Each X8 ENUM produces a `StrEnum` (Python 3.12 native):

```python
# GENERATED FROM X8_GlossaryENUMs_v0_6.md — DO NOT HAND-EDIT
# X8 version: v0.6a | Generated: 2026-05-04T12:00:00Z | §3.8

from enum import StrEnum


class ProjectStatus(StrEnum):
    """M01-owned (X8 §3.8). Locked v0.2."""
    DRAFT = "Draft"
    ACTIVE = "Active"
    SUSPENDED = "Suspended"
    CLOSED = "Closed"
    CANCELLED = "Cancelled"
```

The `__init__.py` re-exports all ENUMs for convenience:
```python
# GENERATED — DO NOT HAND-EDIT
from .project_status import ProjectStatus
from .phase import Phase
from .stage_gate import StageGate
# ... (one line per ENUM)

__all__ = ["ProjectStatus", "Phase", "StageGate", ...]
```

#### 5b.3 Output Format — TypeScript

Each X8 ENUM produces a `const`-asserted object + derived type (idiomatic TS for string ENUMs):

```typescript
// GENERATED FROM X8_GlossaryENUMs_v0_6.md — DO NOT HAND-EDIT
// X8 version: v0.6a | Generated: 2026-05-04T12:00:00Z | §3.8

export const ProjectStatus = {
  DRAFT: "Draft",
  ACTIVE: "Active",
  SUSPENDED: "Suspended",
  CLOSED: "Closed",
  CANCELLED: "Cancelled",
} as const;

export type ProjectStatus = typeof ProjectStatus[keyof typeof ProjectStatus];
```

The `index.ts` re-exports all ENUMs.

### 5c. CI Enforcement (Stage 3)

`scripts/codegen-enums.py --check`:

1. Reads X8 markdown.
2. Generates Python + TS to a temp directory.
3. Diffs temp vs committed `apps/api/.../x_series/enums/` and `apps/web/.../x_series/enums/`.
4. Exit 0 if identical; exit 1 with diff summary if not.

CI Stage 3 invokes this. Any diff blocks merge.

### 5d. X8 Version Tracking in Generated Files

Header comment on every generated file:
```
# GENERATED FROM X8_GlossaryENUMs_v0_6.md — DO NOT HAND-EDIT
# X8 version: v0.6a | Generated: {ISO 8601 timestamp} | {ENUM section ref}
```

A developer can `grep "X8 version" apps/api/src/epcc_api/x_series/enums/*.py` to detect staleness without running codegen.

### 5e. Developer Workflow

```
1. Edit X8 (add ENUM value, mark deprecated, etc.)
2. Bump X8 version per in-place patch convention (v0.6a → v0.6b)
3. Run: python scripts/codegen-enums.py --write
4. Inspect git diff (Python + TS files updated)
5. Commit X8 + regenerated enums + any code touching the ENUM in same PR
6. CI Stage 3 passes (diff = 0); merge
```

### 5f. ENUM Package Versioning (BA-OQ-1 resolution)

Generated enums are versioned with the X8 version:
- Python: `apps/api/pyproject.toml` carries `epcc_x8_version = "v0.6a"` metadata field
- TypeScript: `apps/web/src/x_series/enums/version.ts` exports `export const X8_VERSION = "v0.6a"`

Phase 2 may externalise to PyPI / npm packages (`epcc-enums==0.6.0a`) — deferred until cross-repo consumers exist.

---

## BLOCK 6 — THIN VERTICAL SLICE (locks OQ-1.3)

### 6a. Slice Scope

**Modules in scope:** M34 (auth + RBAC) + M01 (project create + list).

**Brief sequencing (post-merge renumbering):**

| Round | Deliverable | Acceptance Gate |
|---|---|---|
| R31 | Monorepo scaffold | CI runs (all stages skeleton-pass); Docker Compose stack boots locally |
| R32 | ENUM codegen pipeline | CI Stage 3 enforces; X8 → Python + TS round-trip clean |
| R33 | M34 thin slice | AC-1 to AC-3, AC-7 (this Block) |
| R34 | M01 thin slice | AC-4 to AC-6, AC-8, AC-9 |
| R35 | First demo | AC-10 (CI all 8 green on `main`) |

### 6b. Acceptance Criteria (AC-1 to AC-10) — All Must Pass for R35 Demo

| ID | Criterion | Test Vehicle |
|---|---|---|
| **AC-1** | A user can log in via Keycloak (OIDC PKCE flow) with `SYSTEM_ADMIN` role and reach a protected route | Playwright e2e (Stage 8) |
| **AC-2** | A user can log in via Keycloak local password fallback (no external IdP) | Playwright e2e |
| **AC-3** | MFA challenge (TOTP) fires for `SYSTEM_ADMIN` on first login; subsequent logins skip if step-up cached and within session window | Playwright e2e + integration test |
| **AC-4** | A `SYSTEM_ADMIN` (or `PMO_DIRECTOR` of the KDMC tenant) can create a new project (M01 ProjectRegistry) via the UI; Project entity persists with `tenant_id = KDMC tenant UUID`, `project_status = Draft` | Integration test + Playwright e2e |
| **AC-5** | The created project appears in the project list view with status badge `Draft`; project detail page renders correctly per M01 wireframe | Playwright e2e |
| **AC-6** | A `PROJECT_DIRECTOR` of a different tenant CANNOT create a project in KDMC tenant; CANNOT see KDMC projects in list | Integration test (cross-tenant negative case) |
| **AC-7** | All M34 BRs in active scope have passing tests (M34 has ~30 BRs in v1.0 spec; thin-slice scope = login + role check + audit emit, ~10 BRs) | CI Stage 5 (BR-tagged test gate) |
| **AC-8** | All M01 BRs in create-and-list path have passing tests (~12 BRs in scope: project create validation, status transitions, tenant_id assignment, list filtering) | CI Stage 5 |
| **AC-9** | KDMC-001-DBOT seed (HDI v0.1 prototype) loads without error: 1 tenant + 1 project + 17 sample users (one per role) + KDMC reference data | Integration test (seed runner) |
| **AC-10** | CI pipeline passes all 8 stages on `main` after thin-slice merge | GitHub Actions on `main` post-merge |

### 6c. Out of Scope for Thin Slice

| Item | Reason | Where Addressed |
|---|---|---|
| All M02–M06 functionality | Not in active-modules scope | Round 36+ (per-module deepening) |
| Wireframe pixel-perfect fidelity | Functional correctness only; UI polish later | Round 36+ |
| Performance optimisation | No baseline yet | Post-R35 benchmarking |
| External party portal (PF03) | Phase 2 | Phase 2 |
| Full M34 (RBAC matrix UI, password policy, MFA enrolment UX, all 17 roles fully tested) | Thin slice scope = auth-works-for-1-role + role-switcher | Round 36 (M34 deepening) |
| Full M01 (lifecycle state machine all transitions, scenario A/B/W, KPIs, parties + contracts) | Thin slice = create + list + detail-render only | Round 37+ (M01 deepening) |

### 6d. Thin-Slice → Module-Deepening Transition (Phase B per Brief §6)

After R35 demo passes, Phase B begins (per Brief §6.2 — concurrent, gated by Phase A demo). Module deepening order follows dependency-first principle:

1. M34 deepening (full 17-role implementation, RBAC matrix UI, MFA enrolment, password policy)
2. M01 deepening (lifecycle, scenario A/B/W, KPIs, parties, contracts)
3. M02 implementation (WBS, BOQ, packages, BAC integrity ledger)
4. M03 implementation (schedule, baseline, milestones, PV, procurement timing)
5. M04 implementation (progress capture, NCRs, material receipts, contractor scoring)
6. M06 implementation (cost ledger, RA bills, GRN/invoice match, retention, forex)
7. M07 EVM Engine (consumes M02 BAC + M03 PV + M04 EV)
8. M08 GateControl (consumes M07 metrics + M06 financial signals + M15 DLP triggers)
9. M11 ActionRegister (consumes Decision Queue triggers from all modules)

Each deepening lap follows C1b cadence (2-Spec Buffer per spec-protocol.md) where module pairs allow.

---

## BLOCK 7 — INTEGRATION POINTS (build-layer, not module-layer)

> **Distinction:** module integration points (M01 → M07, M03 → M06, etc.) live in each module's Block 7. THIS Block 7 covers **build-layer** integrations — codegen, CI, infrastructure boundaries.

### 7a. Build-Layer Integrations

| Direction | From | To | Trigger | Data |
|---|---|---|---|---|
| OUT | X8 (`X8_GlossaryENUMs_v0_6.md`) | `scripts/codegen-enums.py` | X8 version bump (v0.X → v0.X+1 or letter-suffix patch) | ENUM definitions (parsed from markdown) |
| OUT | `codegen-enums.py` | `apps/api/src/epcc_api/x_series/enums/` | codegen `--write` run | Python `StrEnum` classes (one file per ENUM) |
| OUT | `codegen-enums.py` | `apps/web/src/x_series/enums/` | codegen `--write` run | TypeScript `const` objects + type aliases |
| OUT | FastAPI route definitions | OpenAPI 3.1 spec | Build (`fastapi.openapi()` introspection) | Route signatures + Pydantic schemas |
| OUT | OpenAPI spec | `scripts/codegen-api-types.py` | Build | TypeScript client types |
| OUT | `codegen-api-types.py` | `packages/epcc-types/src/api-types.ts` | Build | Generated TS interfaces (consumed by `apps/web` + future packages) |
| OUT | GitHub Actions (CI) | Keycloak (dev container) | CI Stage 8 (e2e) | OIDC auth flow validation |
| IN | Keycloak | `apps/api/src/epcc_api/core/auth/` | Every request | JWT with `tenant_id`, `user_id`, `roles[]`, `project_ids[]`, `mfa_satisfied` |
| IN | `apps/api/.../core/tenancy/` | PostgreSQL (per-request) | Every authenticated request | `SET LOCAL search_path TO "{schema_name}", public` |
| IN | `infra/seed/kdmc_seed.py` | PostgreSQL `t_kdmc` schema | Dev startup, CI integration tests, manual run | KDMC pilot data (1 project, 17 sample users, reference appendix) |
| IN | Alembic | PostgreSQL (each tenant schema + public) | `alembic upgrade head` | Migration revisions (per `alembic/versions/`) |
| IN | MinIO | `apps/api/.../core/storage/` | Object upload/download | S3-API operations (boto3) |
| OUT | Celery worker | Redis | Job dispatch | Task payloads |
| OUT | Celery worker | PostgreSQL | Long-running job DB writes | Job status updates, async results |

### 7b. Spec-Repo Integrations (governance-layer)

| Direction | From | To | Trigger | Data |
|---|---|---|---|---|
| IN | `SystemAdmin/Modules/*Spec*.md` | `scripts/check-br-coverage.py` | CI Stage 5 | BR-XX-YYY codes parsed from spec body |
| IN | `apps/api/tests/active_modules.yaml` | `scripts/check-br-coverage.py` | CI Stage 5 | List of in-scope module IDs |
| IN | `SystemAdmin/Modules/*CascadeNote*.md` | PR review (manual + automated) | PR open | Cascade note path → must match a code change in same PR |
| OUT | Round commit | `EPCC_VersionLog_v1_0.md` §6 Activity Log | Manual at round close | Round summary entry |

### 7c. Forward Constraints on Future Modules (carry-forward from this Spec)

When future module specs are authored, they must respect the following build-layer contracts established here:

| Constraint | Source | Affects |
|---|---|---|
| All entities reside in `apps/api/src/epcc_api/modules/m{XX}_{name}/models.py` (mirrors spec layout 1:1) | Block 3a.1 invariant | All future module implementations |
| All ENUMs come from `from epcc_api.x_series.enums import ...` (never hand-defined) | Block 5 | All future module Pydantic + SQLAlchemy code |
| All `tenant_id` injection uses the SQLAlchemy event listener; no per-module duplication | Block 3e | All future entities except 17 append-only ledger exemptions |
| All audit-log emission uses `apps/api/.../core/audit/` decorator or explicit emitter | Block 3e | All future modules |
| All cross-module API calls go through `internal_api.py` boundary (BA-OQ-6 resolution) | Block 3a + Block 10 | All future cross-module calls |
| All BR codes follow `BR-{module:02d}-{seq:03d}` and have matching tests `test_BR_{XX}_{YYY}_*` | Block 4a Stage 5 | All future BRs |
| All migrations are schema-agnostic (no hardcoded schema names) | Block 3c.3 | All future Alembic revisions |

---

## BLOCK 8 — GOVERNANCE & AUDIT

### 8a. Architecture Decision Records (ADRs)

10 ADRs to be created in Round 31 scaffold, one per locked OQ-1 decision. Format (per common ADR convention — Michael Nygard style):

```markdown
# ADR-{seq}: {title}

**Status:** Accepted | Superseded by ADR-XXX | Deprecated
**Date:** YYYY-MM-DD
**Context:** {what's the problem; what constraints apply}
**Decision:** {what we decided}
**Consequences:** {what follows from this — positive, negative, neutral}
**Alternatives Rejected:** {what we considered + why we said no}
**Authority:** {Brief OQ-X.Y, this Spec section, ES-XX-XXX, etc.}
```

#### 8a.1 ADR Inventory (to be created in Round 31)

| ADR | Title | Authority |
|---|---|---|
| ADR-001 | Monorepo on `main` | Brief OQ-1.1 + this Spec Block 3a |
| ADR-002 | Trunk-based branching with short-lived feature branches | Brief OQ-1.2 + this Spec Block 4b |
| ADR-003 | Thin vertical slice (M34 → M01) before module deepening | Brief OQ-1.3 + this Spec Block 6 |
| ADR-004 | Keycloak self-hosted as OIDC provider | Brief OQ-1.4 + this Spec Block 3d |
| ADR-005 | Schema-per-tenant database strategy | Brief OQ-1.5 + ES-DB-001 + this Spec Block 3c |
| ADR-006 | KDMC seed as HDI v0.1 prototype | Brief OQ-1.6 + this Spec Block 5/Block 7 |
| ADR-007 | GitHub Actions as CI/CD host | Brief OQ-1.7 + ES-CICD-001 + this Spec Block 4 |
| ADR-008 | Docker Compose for dev + prod-pilot; K8s deferred | Brief OQ-1.8 + this Spec Block 2b |
| ADR-009 | BR-tagged tests with active-branch-scope calibration | Brief OQ-1.9 + this Spec Block 4a Stage 5 |
| ADR-010 | X8 → Python + TypeScript ENUM codegen | Brief OQ-1.10 + this Spec Block 5 |

### 8b. Spec-Change Audit Trail

Every spec change must produce a matching audit-trail event:

| Spec Change Type | Audit Trail |
|---|---|
| Cascade note created (1 field / 1 BR) | Cascade note file + matching code PR + cascade-note path in PR description |
| In-place patch (letter suffix v1.0a / v1.0b) | Patched file's CHANGE LOG entry + code PR (if rendered/runtime affected) |
| Re-issue (`git mv` to v1.X+1.md) | Renamed file + matching code PR series |
| ADR change (Status: Superseded) | New ADR superseding old + reference in CLAUDE.md §4 |

### 8c. Data Privacy Enforcement (DPDPA 2023 — references ES-SEC-004)

> **Authoritative reference:** Standards Memory §7.128 ES-SEC-004 — DPDPA 2023 is the applicable data privacy regulation; HIPAA does not apply.

| Class | Examples | Encryption | Masking | Retention |
|---|---|---|---|---|
| Class 1 — PERSONAL | Name, email, phone | Column-level encryption | Masked for all roles except owner + PMO_DIRECTOR | Anonymised on project closure |
| Class 2 — FINANCIAL | Rates, amounts, EAC | Column-level encryption (ES-SEC-003) | Masked for READ_ONLY | 7 years (Companies Act) |
| Class 3 — OPERATIONAL | Progress %, dates, scores | Table-level TDE | No masking | Project lifetime + 7 years |

**Enforcement:** SQLAlchemy column metadata + Pydantic serialiser in `apps/api/.../core/privacy/`. Masking logic is centralised; module code declares column class via metadata, not by writing masking code per-field.

**Designated Data Fiduciary:** PMO_DIRECTOR (per ES-SEC-004).

### 8d. Disaster Recovery (references ES-DR-001 / ES-DR-002 v1.2)

> **Authoritative reference:** Standards Memory §7.126.

| Phase | RPO | RTO | Backup Strategy |
|---|---|---|---|
| Phase 1 (now) | 24 hr | 4 hr | Daily `pg_dump` + per-tenant `pg_dump --schema=t_{slug}` to MinIO `epcc-backups` bucket. Weekly offsite. Quarterly drill. |
| Phase 2 (cloud) | 5 min | 4 hr | Point-in-time recovery (WAL archiving) |
| Phase 3 (scale) | 5 min | 15 min | Multi-region active-passive |

**Per-tenant restore (surgical — zero impact on other tenants):**
```
DROP SCHEMA t_{slug} CASCADE
→ pg_restore (schema-scoped backup)
→ alembic upgrade head (against restored schema)
→ validate Tenant entity reachable
→ restart api workers (Keycloak session invalidation optional)
```

Drill: quarterly. Logged in `SystemAuditLog` (event_type = `DR_DRILL`).

### 8e. Round 30 Spec Lock Authority

This Spec is locked under the authority of:

| Authority | Reference |
|---|---|
| OQ-1 user lock | CLAUDE.md §4 row "OQ-1 BuildArchitecture (R23→R30)" |
| Multi-tenancy lock | CLAUDE.md §4 row "Multi-tenancy" + architecture.md §Multi-Tenancy + ES-DB-001 |
| Cadence C1b lock | spec-protocol.md §Cadence C1b — 2-Spec Buffer |
| In-place patch convention | spec-protocol.md §In-Place Patch Convention |
| Audit-stamp Format A | spec-protocol.md §Audit Stamp (this Spec uses Format A YAML frontmatter) |
| Spec Block 10 closure rule | spec-protocol.md §10-Block Spec Template — "must close at zero before lock" |

---

## BLOCK 9 — EXPLICIT EXCLUSIONS

The following are explicitly NOT addressed by this Spec and MUST NOT be inferred from it:

| # | Excluded | Reason | Where Addressed (Future) |
|---|---|---|---|
| 1 | M05–M41 module implementation details | Each module has its own spec round | Future spec rounds (R36+) |
| 2 | Production hosting / cloud provider concrete choice | Deferred per OQ-1.8; revisit after R35 demo + pilot pressure | Future round (post-R35) |
| 3 | KDMC workbook → EPCC full migration | HDI module future spec round | Future spec round |
| 4 | PIOE engine implementation | Phase 2 (L0 Strategic) | Phase 2 |
| 5 | External party portal (PF03) | Phase 2 | Phase 2 |
| 6 | Kubernetes manifests | Deferred per OQ-1.8 to actual scale pressure | Future round (>1 tenant or perf constraint) |
| 7 | Performance benchmarking baseline | Post-R35 demo | Future round |
| 8 | Security penetration testing | Pre-production gate | Pre-prod gate (post-R35) |
| 9 | Multi-region deployment | Phase 3 per ES-DR-001 roadmap | Phase 3 |
| 10 | Observability stack concrete tooling (logs / metrics / traces) | Defer until first module is live | First-module-live + 2 weeks (per Brief §10) |
| 11 | Mobile / offline strategy | Phase 2 (PF01 MobileFieldPlatform) | Phase 2 |
| 12 | LLM gateway / AI features (M10, M26, M29 LLM-aspects) | Phase 3+ per Standards Memory §7 | Phase 3+ |
| 13 | 4 unresolved KDMC workbook items | Tracked separately | Per CLAUDE.md §2 |
| 14 | Module Wireframe HTML auto-regeneration from spec | Wireframes are manually updated per cascade per Round 18 lock | Manual sync (acknowledged limit per Brief §7a) |
| 15 | API rate limiting concrete thresholds | Defer until first prod pressure | Post-R35 |
| 16 | Tenant onboarding UX (provisioning wizard) | Tier 1 Manual today; UX deferred | Phase 2 |
| 17 | Phase 2 IdP swap (Auth0, Entra ID) | Auth abstraction layer designed for it; concrete swap deferred | Phase 2 |

---

## BLOCK 10 — OPEN QUESTIONS

### 10a. OQ-1 Status

**All 10 OQ-1 BuildArchitecture decisions are LOCKED** (CLAUDE.md §4). Zero open questions in Block 10 OQ-1.

| OQ-1 | Topic | Locked Answer |
|---|---|---|
| 1.1 | Repo strategy | Monorepo on `main` |
| 1.2 | Branch model | main + short-lived feature branches + cascade-note→BR-test branch protocol |
| 1.3 | Module sequencing | Thin vertical slice M34 → M01 before module deepening |
| 1.4 | OIDC provider | Keycloak self-hosted (DPDPA data sovereignty; swappable Phase 2) |
| 1.5 | Multi-tenancy | Schema-per-tenant (ES-DB-001) |
| 1.6 | Pilot seed | HDI v0.1 prototype (scripted fixture load from KDMC workbook export) |
| 1.7 | CI host | GitHub Actions |
| 1.8 | Container strategy | Docker Compose dev + prod-pilot; K8s deferred |
| 1.9 | BR-tagged tests | Calibrated to active-branch-scope; Phase 2 module merge requires full BR coverage |
| 1.10 | ENUM codegen | X8 → `scripts/codegen-enums.py` → Python + TS; CI fails on manual edit |

### 10b. OQ-2 — Pattern Defaults (Claude Recommends, Monish Confirms)

The 6 carry-forward open questions from Brief §9 (BA-OQ-1 to BA-OQ-6) are resolved here as OQ-2 with locked Claude-recommended defaults. Any future override produces an ADR amendment.

#### OQ-2.1 (was BA-OQ-1) — ENUM package versioning

**Question:** How are generated ENUM packages versioned?

**Answer (LOCKED):** Generated files carry X8 version in header comment + dedicated metadata field.
- Python: `apps/api/pyproject.toml` carries `epcc_x8_version = "v0.6a"` (read by codegen script; refreshed on every `--write`)
- TypeScript: `apps/web/src/x_series/enums/version.ts` exports `export const X8_VERSION = "v0.6a" as const`
- Phase 2 may externalise to PyPI / npm as `epcc-enums==0.6.0a` if cross-repo consumers emerge — deferred until pressure exists.

**Reference:** Block 5f.

#### OQ-2.2 (was BA-OQ-2) — PR template required fields

**Question:** What fields must every PR description include?

**Answer (LOCKED):** Every PR uses `.github/pull_request_template.md` with these required fields:
1. **Linked spec section** (e.g., `M01 Spec Block 6 BR-01-024` or `Build Arch Spec Block 4a`)
2. **BR codes touched** (e.g., `BR-01-024, BR-01-025`) — empty list permitted only for governance/scaffold/infra PRs
3. **Cascade note path** (e.g., `M01_v1_5_CascadeNote.md`) if applicable, else `n/a`
4. **Migration name** (e.g., `2026_05_04_add_dlp_retention_split.py`) if applicable
5. **Active-modules YAML touched?** (Y/N — affects CI Stage 5 scope)
6. **Test plan** (bulleted; what was tested)
7. **CI checks expected to pass** (default: all 8; deviations explained)

#### OQ-2.3 (was BA-OQ-3) — Branch protection rules on `main`

**Question:** What protections enforce on `main`?

**Answer (LOCKED):**
- Required status checks: CI Stages 1–7 (Stage 8 required for PRs to `main`)
- Required reviewers: 0 (single-developer; AI assist is not a reviewer)
- Signed commits: NOT required at thin-slice phase; revisit at Phase 2 production deploy
- Force-push to `main`: BLOCKED (Git Safety Protocol)
- Direct commits to `main`: ALLOWED for governance-class only (CLAUDE.md §4 updates, .claude/rules/* changes, System Specs/* governance docs) per Round 29 precedent. CI runs; failure rolls forward via fix-commit.
- Linear history required: NO (merge commits permitted; matches Round 29 PR series convention)
- Admin bypass: SYSTEM_ADMIN role on GitHub repo for emergency only; logged.

**Phase 2 hardening (deferred):** Required reviewers (when team grows), signed commits (when prod data exists), branch protection enforcement at GitHub org level.

#### OQ-2.4 (was BA-OQ-4) — Secrets management

**Question:** Where do secrets live across dev / CI / prod-pilot?

**Answer (LOCKED):**

| Environment | Secret Store | Examples |
|---|---|---|
| Dev (local) | `.env.local` (gitignored); `.env.example` committed with placeholder keys | DB password, Keycloak admin, MinIO root |
| CI (GitHub Actions) | GitHub Secrets (repo + environment scoped) | Test DB password, Keycloak test realm, Playwright test user creds |
| Prod-pilot | Single-VPS environment file (`/etc/epcc/env`, root-readable, 0600 perms) — committed example only | Real Keycloak admin, real DB password, real MinIO |

**Phase 2 deferral:** vault-backed secret management (HashiCorp Vault, 1Password Connect, or AWS Secrets Manager) — pick when prod hosting is locked.

**Discipline:** No secret may be committed to the repo. CI Stage 1 includes a basic secret-scanner pass (e.g., `gitleaks`) on push.

#### OQ-2.5 (was BA-OQ-5) — Local-dev OIDC user provisioning

**Question:** How are the 17 role users provisioned for dev?

**Answer (LOCKED):** Auto-create on `make seed`. The seed script (`infra/seed/kdmc_seed.py`) is idempotent and creates 17 sample users (one per canonical role), all with default password `epcc-dev-{role-lower}` and TOTP pre-enrolled (using a known-test secret) for the 5 MFA-required roles.

**File:** `infra/keycloak/realm-export.json` already includes the 17 users; `kdmc_seed.py` reconciles users into the database (ProjectParty, ProjectAssignment, etc.) so the UI doesn't show "user not found".

**Production:** users are created via M34 admin UI (not by seed script).

#### OQ-2.6 (was BA-OQ-6) — Cross-module API call convention

**Question:** When module A needs data from module B, is the call in-process function call or HTTP?

**Answer (LOCKED):** **In-process function call for v1.0** — modules live in the same FastAPI app process. Each module exposes a public surface at `apps/api/src/epcc_api/modules/m{XX}_{name}/internal_api.py` documenting which functions are callable cross-module. Module code MUST NOT import from another module's `service.py` or `repository.py` directly — only from `internal_api.py`.

**Rationale:**
- v1.0 deployment is single-VPS Docker Compose; HTTP overhead is unjustified
- The `internal_api.py` boundary is explicit: Phase 2 can refactor any module to a separate service by replacing `internal_api.py` with an HTTP client without touching consumers
- This matches the Single-Owner Rule (F-005) discipline: cross-module access is via a declared API surface, not direct DB read

**Forward constraint:** every module spec authored after Round 30 must define its `internal_api.py` exports in Block 7 (Integration Points).

### 10c. Open Questions Surfaced During Authoring

**None.** All questions encountered during this Spec authoring resolved via Brief / CLAUDE.md / Standards Memory references. Block 10 closes at zero per spec-protocol.md §10-Block Spec Template lock rule.

---

## QUALITY GATES — Pre-Lock Verification

| # | Gate | Verification |
|---|---|---|
| 1 | Every OQ-1 decision from CLAUDE.md §4 appears in Spec body | Block 10a table maps 1.1–1.10 to Block sections; cross-references throughout |
| 2 | ES-DB-001 schema-per-tenant correctly described in Block 3c | Block 3c.1–3c.4 documents implementation; Block 8d covers DR per ES-DR-002 v1.2 |
| 3 | C1b cadence not contradicted anywhere | Block 6d and Block 4b reference C1 + C1b consistently |
| 4 | All 10 ADR titles listed in Block 8 | Block 8a.1 inventory complete (ADR-001 to ADR-010) |
| 5 | Block 10 shows 0 OQ-1 + explicit OQ-2 list | Block 10a (0 open) + Block 10b (6 OQ-2 with locked answers) |
| 6 | Audit stamp complete (all fields) | Frontmatter at top — artefact, round, date, author, parent_brief, x8_version, x9_version, status, type, references_locked, locks_oq1 |
| 7 | No reference to ZEPCC_Legacy specs as active authority | Standards Memory §7.X items cited (ES-DB-001, ES-DR-002 v1.2, ES-CICD-001/002, ES-SEC-004) — these ARE active per re-entry-protocol.md router; legacy SPECS are not cited as active |

---

*— End of Spec v1.0 (DRAFT). Awaiting Monish review before LOCKED status.*
