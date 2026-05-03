# EPCC API (FastAPI)

Backend for the EPCC system. Implements module specs M01, M02, M03, M04, M34.

## Layout

```
apps/api/
├── pyproject.toml          # uv-managed dependencies
├── alembic.ini
├── src/epcc_api/
│   ├── main.py             # FastAPI entrypoint
│   ├── core/               # config, db, auth, deps, audit
│   ├── modules/            # one folder per spec (m34_*, m01_*, ...)
│   └── shared/             # tenant middleware, reserved fields, exceptions
├── migrations/             # Alembic
└── tests/                  # unit + integration
```

## Local development

From the **repo root** (not from this directory):

```bash
make up        # start postgres + redis + minio + keycloak
make migrate   # apply Alembic migrations
make seed      # KDMC pilot data
make dev       # uvicorn --reload (this app) + vite (the web app)
```

To run only the API:

```bash
cd apps/api
uv sync
uv run uvicorn epcc_api.main:app --reload --port 8000
```

## Testing

```bash
make test-api          # unit + integration
cd apps/api && uv run pytest tests/unit
cd apps/api && uv run pytest tests/integration -m integration
```

BR-tagged tests are named `test_BR_XX_NNN_*` and a CI gate verifies every locked
Business Rule from `SystemAdmin/Modules/M0X_*_Spec_*.md` has at least one test.
