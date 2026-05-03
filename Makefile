# EPCC top-level orchestration
# All targets are thin wrappers — heavy lifting lives in apps/*, infra/*, scripts/*.

.PHONY: help up down dev migrate seed test test-api test-web e2e lint typecheck codegen health demo clean reset

SHELL := /bin/bash
COMPOSE := docker compose -f infra/docker-compose.yml
API_DIR := apps/api
WEB_DIR := apps/web

help:
	@echo "EPCC — common targets:"
	@echo "  make up         docker-compose up (postgres, redis, minio, keycloak)"
	@echo "  make down       docker-compose down"
	@echo "  make dev        uvicorn + vite in parallel"
	@echo "  make migrate    alembic upgrade head"
	@echo "  make seed       run KDMC-001-DBOT pilot seed"
	@echo "  make test       pytest + vitest"
	@echo "  make e2e        Playwright"
	@echo "  make lint       ruff + biome"
	@echo "  make typecheck  mypy + tsc"
	@echo "  make codegen    regenerate enums + api-types"
	@echo "  make health     curl /api/v1/health"
	@echo "  make demo       seed + dev"

up:
	$(COMPOSE) up -d
	@echo "Waiting for services to become healthy..."
	@$(COMPOSE) ps

down:
	$(COMPOSE) down

dev:
	@echo "Starting uvicorn (8000) + vite (5173)..."
	@( cd $(API_DIR) && uv run uvicorn epcc_api.main:app --reload --host 0.0.0.0 --port 8000 ) & \
	( cd $(WEB_DIR) && pnpm dev ) & \
	wait

migrate:
	cd $(API_DIR) && uv run alembic upgrade head

seed:
	cd $(API_DIR) && uv run python -m infra.seed.kdmc

test: test-api test-web

test-api:
	cd $(API_DIR) && uv run pytest

test-web:
	cd $(WEB_DIR) && pnpm test

e2e:
	cd $(WEB_DIR) && pnpm exec playwright test

lint:
	cd $(API_DIR) && uv run ruff check . && uv run ruff format --check .
	cd $(WEB_DIR) && pnpm exec biome check .

typecheck:
	cd $(API_DIR) && uv run mypy src
	cd $(WEB_DIR) && pnpm exec tsc --noEmit

codegen:
	uv run python scripts/codegen-enums.py
	bash scripts/codegen-api-types.sh

health:
	@curl -fsS http://localhost:8000/api/v1/health || echo "API not reachable on :8000"

demo: seed
	@echo "Seed complete. Starting dev environment..."
	@$(MAKE) dev

clean:
	cd $(API_DIR) && rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage coverage.xml
	cd $(WEB_DIR) && rm -rf node_modules/.vite test-results playwright-report

reset: down
	$(COMPOSE) down -v
	@echo "All containers + volumes removed. Run 'make up' to rebuild."
