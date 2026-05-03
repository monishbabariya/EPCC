# EPCC — Enterprise Project Management System

Greenfield enterprise project management system for Indian healthcare infrastructure (EPC / DBOT / PPP delivery models). Pilot project: KDMC-001-DBOT (₹68.4 Cr, 150-bed hospital, Kalyan-Dombivli Municipal Corporation).

## Repository layout

```
EPCC/
├── apps/
│   ├── api/          # FastAPI backend (Python 3.12)
│   └── web/          # React frontend (TypeScript 5, Vite 5)
├── packages/
│   ├── enums/        # Generated from X8 (Python + TypeScript)
│   └── api-types/    # Generated from FastAPI OpenAPI
├── infra/            # docker-compose, Postgres init, Keycloak realm, KDMC seed
├── scripts/          # codegen scripts (X8 → enums, OpenAPI → types)
├── SystemAdmin/      # Module specs (M01, M02, M03, M04, M34, X-series)
└── System Specs/     # Governance, naming, version log, audits
```

## Quickstart

Prerequisites: Docker, Docker Compose, `uv` (Python), Node 20+ with `pnpm` (or `npm`), `make`.

```bash
git clone <repo>
cd EPCC
cp .env.example .env.local         # edit if needed; defaults work for dev
make up                            # docker-compose: postgres + redis + minio + keycloak
make migrate                       # alembic upgrade head
make seed                          # KDMC-001-DBOT + 17 role users
make dev                           # uvicorn (8000) + vite (5173) in parallel
```

Once running:

- Frontend: <http://localhost:5173>
- Backend health: <http://localhost:8000/api/v1/health>
- Backend docs: <http://localhost:8000/api/v1/docs>
- Keycloak admin: <http://localhost:8080> (admin/admin in dev)
- MinIO console: <http://localhost:9001> (minio/miniopassword)

## Make targets

| Target | Purpose |
|---|---|
| `make up` / `make down` | docker-compose lifecycle |
| `make dev` | uvicorn + vite in parallel |
| `make migrate` | `alembic upgrade head` |
| `make seed` | run `infra/seed/kdmc.py` |
| `make test` | pytest + vitest |
| `make e2e` | Playwright |
| `make lint` | ruff + biome |
| `make typecheck` | mypy + tsc |
| `make codegen` | regenerate enums + api-types |
| `make health` | curl `/api/v1/health` |
| `make demo` | seed + dev (open browser to KDMC dashboard) |

## Status

- **Phase 1 specs (M34, M01, M02, M03, M04)**: locked.
- **Phase 1B build architecture (Round 23 + 24)**: locked 2026-05-03.
- **Round 25 scaffold**: this commit.
- **Round 26 ENUM codegen**: in progress.
- **Rounds 27-29**: M34 thin slice → M01 thin slice → first end-to-end demo.

See `CLAUDE.md` for project context and `System Specs/EPCC_BuildArchitecture_Spec_v1_0.md` for the locked build architecture.

## Spec → code mapping

Each module's spec at `SystemAdmin/Modules/M0X_*_Spec_*.md` maps to:

- Backend: `apps/api/src/epcc_api/modules/m0x_<short_name>/`
- Frontend: `apps/web/src/modules/m0x_<short_name>/`

## License

Private — pilot phase. License determined post-pilot.
