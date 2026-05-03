---
artefact: EPCC_BuildArchitecture_Brief_v1_0
round: 23
date: 2026-05-03
author: Monish (with Claude assist)
x8_version: v0.5
x9_version: v0.3
status: DRAFT
---

# EPCC Build Architecture — Brief (Round 23)

> **Purpose.** Surface the decisions Monish must make before any code is written for M34, M01, M02, M03, or M04. This Brief does **not** lock anything; it lists OQ-1 user decisions and OQ-2 pattern defaults for review. Decisions become LOCKED in `EPCC_BuildArchitecture_Spec_v1_0.md` (Round 24 deliverable).
>
> **Cadence reminder.** Per principle #5 ("Spec before code") and C1 ("one artefact at a time"), this Brief must be reviewed and OQ-1 answered before the Spec is drafted, and the Spec must be locked before any application code is committed.

---

## 1. Why This Round Exists

Five modules (M34, M01, M02, M03, M04) plus two cross-cutting living standards (X8 v0.5 ENUMs, X9 v0.3 visualisation) are now LOCKED at the artefact level. The next dependency is **execution** — turning specs into running software.

The four-artefact cadence answers *what* we're building per module. It does **not** answer:

- Where does the code live (repo / branch / folder)?
- Which Python / Node toolchain do we standardise on?
- How does a feature flow from `main` → CI → preview → production?
- How do specs and code stay in lockstep when a spec cascades (e.g., M01 v1.2)?
- How is the pilot (KDMC-001-DBOT) provisioned, seeded, and operated?

Round 23 makes those decisions explicit. Without it, the build will accumulate ad-hoc choices that contradict the discipline shown in Rounds 1–22.

---

## 2. Scope Boundary (Round 23 Brief)

**In scope:**

- Repo + branch + folder strategy
- Toolchain (Python, Node, package managers, linters, type checkers, test frameworks)
- API contract pipeline (OpenAPI generation, TypeScript codegen)
- Database + migration strategy (PostgreSQL, Alembic, multi-tenant model)
- Background jobs (Celery + Redis, per locked stack)
- Object storage (MinIO, per locked stack)
- Auth provider concrete choice (OIDC backend + local password fallback)
- Local dev environment (docker-compose layout)
- CI/CD pipeline shape (linter → type → test → build → deploy)
- Module implementation order + thin-slice vs full-stack-per-module sequencing
- ENUM single-source-of-truth pipeline (X8 → Python module + TypeScript types)
- Spec ↔ code traceability convention (how a BR-XX-NNN appears in code/tests)

**Explicitly out of scope:**

- Production hosting / cloud provider choice (defer until M34 + M01 ship)
- Observability stack (defer until first module is live)
- Performance budgets (defer until first module is benchmarked)
- Mobile / offline strategy (Phase 2)
- External party portal hardening (PF03, Phase 2)
- The 4 unresolved KDMC workbook items (tracked separately, not addressed in EPCC build)

---

## 3. OQ-1 — User Decisions Required

These are the decisions Monish must make. Claude has marked a recommendation for each; nothing is locked until Monish confirms in writing.

### OQ-1.1 — Repository / branch strategy

**Question.** Where does code live, and how does it travel from "draft" to "in `main`"?

**Options:**

| Option | Description | Recommendation |
|---|---|---|
| A | **Monorepo on `main`.** Specs and code live in the same repo. Code under `apps/`, `packages/`, `infra/`. Short-lived feature branches per module (`feat/m34-rbac`, `feat/m01-registry`) merged via PR into `main`. | **✅ Recommended** |
| B | Long-lived `Code` branch off `main`. Code-only branch, never merged back. | ❌ Diverges from spec history; cascade discipline (M01 v1.2 pattern) breaks. |
| C | Separate code repo (`epcc-app`). Specs stay in `epcc`. Cross-repo references via commit SHA. | Cleanest CI, worst traceability. Reasonable if you expect external contractors. |

**Why A wins for EPCC.** Specs cascade (M01 v1.2 removed `reporting_period_type` ~2 weeks after lock). With A, the cascade note + the corresponding code change land in one PR — auditable in one place. With B or C, the spec change and the code change live in different histories and can drift silently. EPCC's whole value proposition is anti-drift discipline; the repo strategy must reinforce it.

### OQ-1.2 — Branch model

**Question.** Trunk-based development on `main`, or git-flow with a long-lived `develop`?

**Options:**

| Option | Description | Recommendation |
|---|---|---|
| A | **Trunk-based.** `main` is always deployable. Feature branches < 3 days old. CI gates merge. | **✅ Recommended** |
| B | git-flow. `main` for releases, `develop` for integration, `release/*` for stabilisation. | Adds ceremony with no benefit at single-engineer + AI-assist scale. |

### OQ-1.3 — Module implementation sequencing

**Question.** Do we implement modules end-to-end one at a time, or build a thin slice across multiple modules first?

**Options:**

| Option | Description | Recommendation |
|---|---|---|
| A | **Thin vertical slice first.** M34 (auth + RBAC for 17 roles) → M01 (project create + read) → end-to-end demo with KDMC-001-DBOT seeded → then deepen each module. | **✅ Recommended** |
| B | Module-by-module fully complete. M34 100% → M01 100% → M02 100% etc. | Higher risk: integration issues only surface at M04. M34 alone takes ~6 weeks. |
| C | Parallel module development. Multiple feature branches active per module. | Premature; team is currently 1 + AI assist. |

**Why A wins.** A thin slice exposes integration assumptions (auth → tenant_id → project → audit log → wireframe render) within ~3 weeks, when course-correction is cheap. Module-by-module risks discovering an architectural mistake at M04 that requires rework of M34.

### OQ-1.4 — Auth backend concrete choice

**Question.** Stack lock says "OIDC with local password fallback." Which OIDC provider for v1.0?

**Options:**

| Option | Description | Recommendation |
|---|---|---|
| A | **Self-hosted Keycloak** (docker-compose for dev, container for prod). | **✅ Recommended for pilot** |
| B | Auth0 (managed SaaS). | Faster setup, but lock-in + per-MAU pricing. |
| C | Azure AD / Entra ID. | Strong if KDMC stakeholders already have Microsoft tenancy. Confirm before choosing. |
| D | Keycloak now, swap to managed if pilot succeeds. | Same as A in v1.0; flag as Phase 2 review. |

**Recommendation rationale.** Keycloak is OIDC-compliant, supports local password fallback (M34 requirement), supports MFA (5 of 17 roles require it), and runs locally for dev with zero per-MAU cost during pilot. Decision is reversible (M34 spec abstracts the IdP).

### OQ-1.5 — Multi-tenant model in v1.0

**Question.** M34 + M01 specs assume `tenant_id` as a reserved field on every entity. Confirm the v1.0 tenancy model:

**Options:**

| Option | Description | Recommendation |
|---|---|---|
| A | **Shared schema, `tenant_id` filtering at app layer + RLS at DB layer.** Single Postgres schema; row-level security policies enforce tenant isolation. | **✅ Recommended** |
| B | Schema-per-tenant. New Postgres schema per onboarded org. | Stronger isolation; ~10x ops cost; premature for pilot (1 tenant). |
| C | Database-per-tenant. | Premature. Defer until > 5 paying tenants. |

### OQ-1.6 — Pilot tenant provisioning

**Question.** How does KDMC-001-DBOT enter the running system?

**Options:**

| Option | Description | Recommendation |
|---|---|---|
| A | **Seed script** (`infra/seed/kdmc.py`) creates tenant, project, KDMC reference data, sample users for each of 17 roles. Runs on `docker-compose up` for dev; explicit invocation for prod. | **✅ Recommended** |
| B | Hand-create via UI on first deploy. | Doesn't scale; not reproducible across dev/staging/prod. |
| C | Import from `KDMC_CC_Transformed.xlsm` directly. | Worth doing eventually (HDI module M-tier work), but blocks initial demo. Defer to a later round. |

### OQ-1.7 — CI/CD host

**Question.** Where do builds, tests, and deploys run?

**Options:**

| Option | Description | Recommendation |
|---|---|---|
| A | **GitHub Actions** (repo is already on GitHub at `monishbabariya/epcc`). | **✅ Recommended** |
| B | Self-hosted runner. | Premature; cost-justified only at high CI volume. |

### OQ-1.8 — Production hosting (commitment level)

**Question.** Do we lock production hosting now, or defer until M34 + M01 ship?

**Options:**

| Option | Description | Recommendation |
|---|---|---|
| A | **Defer.** Lock dev (docker-compose) + staging shape. Pick prod hosting after first module ships. | **✅ Recommended** |
| B | Lock now (e.g., AWS ECS, GCP Cloud Run, Hetzner). | Premature commitment; production needs (RTO, RPO, region) clarify after pilot. |

### OQ-1.9 — Spec → code traceability convention

**Question.** How does a Business Rule (e.g., `BR-01-024`) surface in the codebase?

**Options:**

| Option | Description | Recommendation |
|---|---|---|
| A | **Test name carries BR code.** `test_BR_01_024_project_status_transitions_draft_to_active`. Code references BR via inline comment only when a non-obvious invariant ties to a BR. | **✅ Recommended** |
| B | Code comments everywhere a BR is enforced. | Comment rot; comments lie when code changes. |
| C | Separate traceability matrix file. | Decays unless someone owns it. |

**Why A wins.** Tests are mechanically verifiable: a CI check can assert that every locked BR has at least one test referencing its code. The matrix is generated, not hand-maintained.

### OQ-1.10 — ENUM single source of truth pipeline

**Question.** X8 v0.5 defines ~40 ENUMs. They must exist in Python (FastAPI / SQLAlchemy) and TypeScript (React). How are they kept in sync?

**Options:**

| Option | Description | Recommendation |
|---|---|---|
| A | **Codegen from X8 markdown.** Parse X8 → emit `packages/enums/python/__init__.py` + `packages/enums/typescript/index.ts`. CI fails if generated files are stale. | **✅ Recommended** |
| B | Hand-maintain in both languages. | Drift inevitable. Violates anti-drift principle. |
| C | Single Python source, generate TS via OpenAPI. | Works but couples ENUMs to API surface; harder to use ENUMs in non-API contexts (e.g., seed scripts). |

---

## 4. OQ-2 — Pattern Defaults (Claude Recommends, Monish Confirms)

These are technical defaults where Claude has a strong recommendation. Monish confirms or overrides; no surfacing as full OQ-1 unless Monish wants to dig in.

### Backend (FastAPI / Python)

| Topic | Default | Notes |
|---|---|---|
| Python version | **3.12** | Stable, fast, type-system mature. |
| Package manager | **`uv`** | 10-100× faster than pip; lockfile + workspace support. |
| Web framework | **FastAPI 0.110+** | Locked in stack. |
| ASGI server | **uvicorn (dev) + gunicorn-uvicorn-workers (prod)** | Standard FastAPI deployment. |
| ORM | **SQLAlchemy 2.x async** | Async-first; integrates with FastAPI dependency injection. |
| Migration | **Alembic** | Standard SQLAlchemy companion; supports autogenerate. |
| Validation | **Pydantic v2** | Already a FastAPI dependency. |
| Background jobs | **Celery 5.x + Redis** | Locked in stack. |
| Object storage SDK | **`boto3` against MinIO** | S3-compatible; swappable to AWS S3 in prod. |
| Auth library | **`authlib`** | OIDC client; works with Keycloak. |
| Test framework | **pytest + pytest-asyncio + httpx** | Standard async FastAPI test stack. |
| Test DB | **`pytest-postgresql`** (real Postgres in CI, ephemeral per test) | Catches RLS / migration bugs that SQLite hides. |
| Linter + formatter | **`ruff`** (replaces black, isort, flake8) | One tool, fast. |
| Type checker | **`mypy --strict`** on `apps/api/`; relaxed on tests | Strict at boundaries; pragmatic in tests. |
| Coverage gate | **80% line, 100% on BR-tagged tests** | BR tests are the load-bearing ones. |

### Frontend (React)

| Topic | Default | Notes |
|---|---|---|
| Bundler | **Vite 5.x** | Fast dev, simple config. |
| Language | **TypeScript 5.x strict** | Strict null checks on. |
| Routing | **React Router 6.x** | De facto standard. |
| Server state | **TanStack Query (React Query) v5** | Caching + optimistic updates + refetch. |
| Client state | **Zustand** | Minimal; avoid Redux unless we need it. |
| Forms | **`react-hook-form` + `zod`** | zod schemas align with Pydantic on the backend. |
| Styling | **Tailwind CSS 3.x** | Locked via wireframe convention (D3). |
| Component primitives | **`shadcn/ui`** (Radix + Tailwind) | Copy-into-repo model; no runtime lock-in. |
| Charts | **Recharts 3.x** | Locked in X9 v0.3. |
| Gantt | **frappe-gantt 0.7.x** | Locked in X9 v0.3. |
| Network graph | **react-flow 12.x** | Locked in X9 v0.3. |
| Test (unit) | **Vitest + React Testing Library** | Vitest matches Vite; fast. |
| Test (e2e) | **Playwright** | Cross-browser; supports auth + multi-tenant scenarios. |
| Linter + formatter | **`biome`** (replaces ESLint + Prettier) | One tool, fast. Fall back to ESLint if a plugin we need isn't covered. |

### API contract

| Topic | Default | Notes |
|---|---|---|
| Source of truth | **FastAPI route definitions → OpenAPI 3.1** | FastAPI emits this for free. |
| TypeScript client | **`openapi-typescript` + `openapi-fetch`** | Type-safe client generated on every backend change. |
| Versioning | **URL prefix `/api/v1/`** | Single major version in v1.0; prepare for v2 if breaking changes appear. |

### Infra (dev)

| Topic | Default | Notes |
|---|---|---|
| Local orchestration | **`docker-compose`** | Postgres, Redis, MinIO, Keycloak in one file. |
| Hot reload | **`uvicorn --reload` + Vite HMR** | Sub-second feedback. |
| Seed | **`make seed`** (or `uv run seed`) | Runs `infra/seed/kdmc.py`. |

### CI

| Topic | Default | Notes |
|---|---|---|
| Provider | **GitHub Actions** (per OQ-1.7 recommendation) | |
| Pipeline | lint → typecheck → unit tests → integration tests (Postgres + Redis) → frontend build → e2e (Playwright) → ENUM-codegen-stale check → BR-coverage check | |
| Required checks | All of the above must pass before merge to `main` | |

---

## 5. Proposed Repo Layout (subject to OQ-1.1 lock)

If Monish accepts OQ-1.1 Option A (monorepo on `main`):

```
EPCC/
├── CLAUDE.md
├── .claude/                          # rules + skills (existing)
├── .gitignore                        # extended for new languages
├── .github/
│   └── workflows/
│       ├── ci.yml                    # full pipeline
│       └── enum-codegen-check.yml    # X8 freshness gate
├── SystemAdmin/                      # specs (existing — untouched)
├── System Specs/                     # governance (existing)
├── ZEPCC_Legacy/                     # frozen (existing)
├── apps/
│   ├── api/                          # FastAPI backend
│   │   ├── pyproject.toml
│   │   ├── alembic.ini
│   │   ├── src/epcc_api/
│   │   │   ├── main.py
│   │   │   ├── core/                 # config, db, auth, deps
│   │   │   ├── modules/
│   │   │   │   ├── m34_rbac/
│   │   │   │   ├── m01_project_registry/
│   │   │   │   ├── m02_structure_wbs/
│   │   │   │   ├── m03_planning_milestones/
│   │   │   │   └── m04_execution_capture/
│   │   │   └── shared/               # tenant_id middleware, audit log, etc.
│   │   ├── migrations/               # Alembic
│   │   └── tests/
│   └── web/                          # React frontend
│       ├── package.json
│       ├── vite.config.ts
│       ├── src/
│       │   ├── main.tsx
│       │   ├── routes/
│       │   ├── modules/
│       │   │   ├── m34_rbac/
│       │   │   ├── m01_project_registry/
│       │   │   └── ... (per module)
│       │   ├── components/           # shadcn/ui + custom
│       │   ├── lib/                  # api client, auth, utils
│       │   └── styles/
│       └── tests/
├── packages/
│   ├── enums/                        # X8 codegen output
│   │   ├── python/                   # importable as epcc_enums
│   │   └── typescript/               # importable as @epcc/enums
│   └── api-types/                    # openapi-typescript output
├── infra/
│   ├── docker-compose.yml            # postgres, redis, minio, keycloak
│   ├── docker-compose.test.yml       # CI overlay
│   ├── seed/
│   │   └── kdmc.py                   # KDMC-001-DBOT pilot seed
│   └── keycloak/
│       └── realm-export.json         # 17 roles pre-configured
├── scripts/
│   ├── codegen-enums.py              # X8 .md → python + ts
│   └── codegen-api-types.sh          # openapi → ts
└── tests/
    └── e2e/                          # Playwright cross-module scenarios
```

**Rationale highlights:**

- `apps/api/src/epcc_api/modules/m34_rbac/` mirrors the spec layout exactly. A new engineer reading the spec can find the code in seconds.
- `packages/enums/` is generated, never hand-edited. CI fails if X8 was bumped without regenerating.
- `infra/seed/kdmc.py` makes the pilot reproducible — every clone is one `make up && make seed` away from a running KDMC dashboard.

---

## 6. Proposed Module Implementation Sequence

If Monish accepts OQ-1.3 Option A (thin slice first):

### Phase A — Foundation & first vertical slice (target: 4-6 weeks)

1. **Round 24:** Lock `EPCC_BuildArchitecture_Spec_v1_0.md` (this Brief's Spec).
2. **Round 25:** Scaffold monorepo (`apps/api`, `apps/web`, `packages/`, `infra/`, CI). No business logic yet.
3. **Round 26:** ENUM codegen pipeline (X8 → Python + TS). CI gate live.
4. **Round 27:** M34 thin slice — login (OIDC + local fallback), 17-role seed, role switcher in UI, audit log skeleton.
5. **Round 28:** M01 thin slice — project create + read for KDMC-001-DBOT, tenant_id RLS verified.
6. **Round 29:** First end-to-end demo. KDMC project visible in the UI as PMO_DIRECTOR, PROJECT_DIRECTOR, READ_ONLY.

### Phase B — Module deepening (concurrent, gated by Phase A demo)

7. M34 deepening (RBAC matrix UI, MFA enrolment, password policy, all 17 roles fully implemented).
8. M01 deepening (lifecycle state machine, scenario A/B/W, KPIs, parties + contracts).
9. M02 implementation (WBS, BOQ, packages, BAC integrity ledger).
10. M03 implementation (schedule, baseline, milestones, PV).
11. M04 implementation (progress, NCR, material receipts, contractor scoring).

Cascade discipline applies throughout: a spec change → a single PR that updates spec + code + tests in lockstep.

---

## 7. Cascade & Spec-Code Coupling

A locked spec is the contract. When code-level reality forces a spec change:

| Change scope | Process |
|---|---|
| **1 field, 1 BR, no scope shift** | Cascade note (`M0X_v1_Y_CascadeNote.md`) + matching code change in the same PR. |
| **New entity, new appendix, multiple BRs** | Full spec re-issue (`_v1_Y+1.md` via `git mv`) + matching code change in a separate PR (review the spec first). |
| **Cross-module** | Update CLAUDE.md "Pending cascades" + open one PR per affected module. |

This mirrors the Round 18 audit lock; no new convention.

---

## 7a. Change Management — How the System Absorbs Future Updates

The proposed architecture is explicitly designed for spec churn. EPCC has already cascaded **3 times** in 22 rounds (M01 v1.1, M01 v1.2, M03 v1.1) with two more rounds (X8 four bumps, X9 three bumps). The build must treat change as the steady state, not the exception.

### What changes, and what each one costs

| Change type | Example from history | Cost to absorb | Mechanism |
|---|---|---|---|
| **Single field added to a spec** | M01 v1.1 added `min_wbs_depth` | ~1 hour: Alembic migration + Pydantic model + zod schema + 1 test | Cascade note + single PR |
| **Single field removed** | M01 v1.2 removed `reporting_period_type` | ~30 min: Alembic migration + remove field + delete tests | Cascade note + single PR |
| **New ENUM value** | X8 v0.4 → v0.5 added M04 ENUMs | ~5 min: bump X8 → run codegen → CI passes | X8 codegen pipeline (OQ-1.10) |
| **New BR added** | M03 v1.1 added 2 BRs in Appendix C | ~2-4 hours per BR: write test → implement → wire to existing endpoints | BR test-naming convention (OQ-1.9) |
| **New entity (full re-issue)** | M03 v1.1 added Appendix C | ~1-3 days: new SQLAlchemy model + Alembic migration + endpoints + UI + tests | Full spec re-issue + multi-PR series |
| **Cross-module change** | (none yet, but inevitable) | Days-to-weeks: coordinate cascades across affected modules | "Pending cascades" tracking in CLAUDE.md + sequenced PRs |
| **Library version bump** (Recharts 3 → 4) | (anticipated) | ~1 day per library: update pin, regenerate types, smoke-test charts | Pinned versions in `pyproject.toml` / `package.json` + visual regression on flagship charts |
| **Architectural pivot** (e.g., split monorepo) | (hopefully never) | Weeks: full migration | Out of scope for cascade discipline; would require its own round |

### Built-in flexibility mechanisms

1. **Code mirrors spec layout 1:1.** `apps/api/src/epcc_api/modules/m01_project_registry/` maps to `M01_ProjectRegistry_Spec_v1_0.md`. When a spec section moves, the matching code module moves with it. No detective work to find the affected code.
2. **ENUM codegen pipeline (OQ-1.10).** X8 is the source of truth. Bump X8 → run `scripts/codegen-enums.py` → Python + TS regenerate. CI fails if a developer hand-edits the generated files or forgets to regenerate after an X8 bump. The previous M01 → M02 → M03 → M04 ENUM cascades would each have been a one-line X8 edit + autoregen.
3. **OpenAPI → TypeScript codegen.** Backend route signature changes propagate to the frontend client at build time. No silent contract drift.
4. **BR-tagged tests.** Adding a new BR to a spec → CI fails until a test named `test_BR_XX_NNN_*` exists. Removing a BR → the corresponding test is deleted in the same PR. Spec/test divergence is mechanically detected.
5. **Single source of truth for tenancy + audit.** Tenant_id middleware and audit-log emission live in `apps/api/src/epcc_api/shared/`. Any new entity inherits these for free; no per-module reimplementation drift.
6. **Cascade note convention (Round 18 lock).** Already in use. `M01_ProjectRegistry_v1_2_CascadeNote.md` is the canonical pattern. The build inherits this; nothing new to invent.
7. **Migration tool (Alembic) with autogenerate.** Add a column to a SQLAlchemy model → `alembic revision --autogenerate` produces the migration. Reviewer checks before merge.
8. **Feature branches are short-lived.** No long-running branch can drift from `main`. The longest open branch should be < 3 days. This bounds the "merge debt" any single change creates.
9. **Pinned versions.** Both `pyproject.toml` (uv lockfile) and `package.json` (npm/pnpm lockfile) pin transitive dependencies. Library updates are explicit PRs, not silent drift.
10. **Reproducible dev env.** `make up && make seed` produces an identical environment from a clean clone. New contributor (or future-Monish on a new laptop) is productive in minutes, not days.

### Where flexibility has limits (worth being honest about)

- **Wireframes don't auto-regenerate from code.** A UI change to match a spec cascade requires the wireframe HTML to be updated in a separate edit (Tailwind CDN + no JS deps was a deliberate D3 lock — keeps them readable but breaks any "live" coupling). v1.0 accepts manual wireframe sync.
- **Cross-module spec changes still require human sequencing.** If M02 changes a field that M04 reads, the cascade order matters: update M02 → cascade M04 spec → land both in coordinated PRs. The architecture surfaces this via "Pending cascades" in CLAUDE.md, but doesn't automate the sequencing.
- **Architectural decisions (locked in §4 of CLAUDE.md) are intentionally hard to change.** "Greenfield (U3-a)", "Cadence C1", "Tailwind CDN no JS deps", etc. are gates against thrash, not invitations to revisit. A real change to one of these requires a new round with explicit deliberation, not a cascade.
- **Retroactive renames are expensive.** M34 stayed at `SystemAdmin/` rather than moving to `SystemAdmin/Modules/` because renaming would break every cross-reference. The build will inherit the same constraint: prefer additive changes over renames once a module is referenced from other modules' code.
- **Single-tenant pilot today; multi-tenant claims need verification.** RLS + tenant_id is designed in, but until a second tenant is onboarded, the multi-tenant claim is partially theoretical. Round 27/28 should add a minimal "second tenant in seed" CI test to keep the design honest.

### Net answer

Yes — the architecture is designed for change. Spec cascades, ENUM bumps, library upgrades, and module deepening are all **cheap** (minutes-to-hours per cascade) because:

- Code layout mirrors spec layout (cascade location is obvious),
- Codegen pipelines (ENUMs, API types) eliminate manual translation,
- BR-tagged tests mechanically detect spec/code drift,
- Cascade notes + monorepo PRs keep spec change and code change in one atomic, reviewable unit.

What is **expensive** by design: changing the locked architectural decisions themselves (cadence, tech stack, monorepo strategy). Those gates exist because thrashing them is what kills enterprise builds. The cost asymmetry — easy cascade, hard pivot — is the feature, not the bug.

---

## 8. What I Need from You (Monish)

Answer the OQ-1 questions in §3. OQ-2 defaults can be confirmed in bulk ("OQ-2 all ✅") unless you want to change one.

The fastest path:

```
OQ-1.1 → A (monorepo on main)
OQ-1.2 → A (trunk-based)
OQ-1.3 → A (thin vertical slice first)
OQ-1.4 → A (Keycloak)
OQ-1.5 → A (shared schema + RLS)
OQ-1.6 → A (seed script)
OQ-1.7 → A (GitHub Actions)
OQ-1.8 → A (defer prod hosting)
OQ-1.9 → A (BR codes in test names)
OQ-1.10 → A (codegen from X8)
OQ-2 → all defaults accepted
```

If that's the answer, the Round 24 Spec writes itself and we can start Round 25 scaffolding the day after Round 24 locks.

---

## 9. Open Questions to Round 24 (Spec)

These will be carried forward and addressed at the Spec-locking gate:

- **BA-OQ-1** Versioning of generated ENUM packages — pin to X8 version (e.g., `epcc_enums==0.5.0`)?
- **BA-OQ-2** PR template — what fields are required (linked spec section, BR codes touched, cascade note path)?
- **BA-OQ-3** Branch protection rules on `main` — required reviewers, status checks, signed commits?
- **BA-OQ-4** Secrets management — `.env.local` for dev; what about CI and prod (1Password / GitHub Secrets / vault)?
- **BA-OQ-5** Local-dev OIDC user provisioning — auto-create the 17 role users on `make seed`, or interactive `make seed-users`?
- **BA-OQ-6** Cross-module API call convention — internal HTTP, in-process function call, or both gated by config?

These are flagged here so they don't disappear into the gap between Brief and Spec.

---

## 10. Out of Scope for Round 23 (Confirmation)

For completeness — these are NOT being decided in Round 23 or 24, and remain in their existing locked / deferred state:

- 4 unresolved KDMC workbook items (PKG-to-WBS mapping, Snapshot macro, Named range rollout, Progress_Calc % integration).
- Phase 2 modules (M05, M06, …, PF03 ExternalPartyPortal).
- 13-folder hierarchy migration (deferred indefinitely per Round 18 audit).
- HDI / Historical Data Import (separate workstream, gated by M02 lock + KDMC workbook readiness).
- Production observability (logs, metrics, traces) — deferred to first-module-live + 2 weeks.

---

*— End of Brief. Awaiting OQ-1 answers from Monish before drafting Round 24 Spec.*
