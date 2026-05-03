-- EPCC Postgres bootstrap.
-- Runs once on first container start. Idempotent.

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS citext;

-- Per EPCC_BuildArchitecture_Spec_v1_0.md §4.3, RLS is enabled per-table
-- in Alembic migrations (Round 27+). This file only ensures extensions exist.
