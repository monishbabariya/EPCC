# EPCC System Architecture — Locked Decisions

> **Purpose:** Canonical reference for the 5-layer architecture, stage gates, financial control states, EVM metrics, and risk model. Do not redefine these elsewhere — link here.

---

## Module Registry (41 items total)

| Layer | Modules | Count |
|---|---|---|
| L0 Strategic | M16, M17, M18, M19 | 4 |
| L1 Command | M01, M23, M24, M28 | 4 |
| L2 Planning | M02, M03 | 2 |
| L2 Execution | M04, M14, M27, M12, M13 | 5 |
| L2 Risk/Commercial | M05, M06, M22 | 3 |
| L2 Compliance | M09, M25, M30, M31 | 4 |
| L2 Performance | M07, M26, M32 | 3 |
| L3 Intelligence | M08, M10, M11, M15, M29, M33 | 6 |
| Platform Features | PF01-PF06 | 6 |
| System Utilities | M34, HDI | 2 |
| **TOTAL** | | **41** |

---

## 5-Layer Architecture (locked)

```
L1 Strategic     → Portfolio selection, MILP-driven capital allocation
L2 Portfolio     → Prioritization, dependency management, benefit tracking
L3 Project       → Scope, schedule, cost, risk (governed by SG-4 to SG-11)
L4 Department    → Functional execution (Engineering, Finance, HR)
L5 Data          → Data lake, dashboards, analytics
```

---

## Stage Gate Governance

- **Pre-project:** SG-0, SG-1, SG-2, SG-3 (idea → concept → DPR → capital sanction)
- **Project lifecycle:** SG-4 to SG-11
- **Rule:** Formal approval required at every gate. No skipping. No post-facto justification.

---

## Financial Control States (locked)

```
Budgeted → Committed → Accrued → Paid
```

The **Committed-vs-Budget gap** is the primary risk indicator.

---

## EVM Metrics (core)

`BAC, EV, AC, EAC, ETC, VAC, CPI, SPI, TCPI`

Formula references live in M07 EVM Engine spec. Do not redefine inline.

---

## Risk Categories

- Strategic / Financial / Operational / Regulatory / Clinical
- **Methods:** qualitative (heat map) + quantitative (Monte Carlo)
- **Escalation:** Green / Amber / Red thresholds

---

## Tech Stack (locked)

| Layer | Choice |
|---|---|
| Backend | FastAPI (Python) |
| Frontend | React |
| Database | PostgreSQL |
| Async tasks | Celery + Redis |
| Object storage | MinIO |
| Authentication | OIDC — Keycloak self-hosted (OQ-1.4 LOCKED R29; DPDP Act data sovereignty; local password fallback retained) |

---

## Multi-Tenancy (ES-DB-001 — LOCKED)

**Standard:** **Schema-per-tenant** (PostgreSQL `search_path` per tenant).

`tenant_id` is present on all entities — retained for **sub-tenant + JV support**, NOT for row-level discrimination within a single tenant's schema. Within one tenant's schema, all rows belong to that tenant by definition; `tenant_id` is the key for cross-schema federation when sub-tenants/JVs need shared visibility.

**Source of truth:** `ZEPCC_Legacy/EPCC_Standards_Memory_v5_3.md` §7.137 (ES-DB-001 — STATUS: CONFIRMED. LOCKED. CLOSED.).

**Operational note:** Tenant entity (M34) carries `db_schema_name` field with auto-derivation `t_{tenant_code_lower}` mapping to PostgreSQL schema. See M34 Spec Block 3b.

**Re-open triggers (must satisfy ≥1):**
- \>50 active tenants (schema management overhead becomes prohibitive)
- \>40% I/O concentration on a single tenant (cross-schema replica strategy may be required)

Until either trigger fires, **do not revisit this decision.**

---

## Single-Owner Rule (F-005)

Every entity has exactly one owning module. Cross-module access is via internal API, **never** direct DB read.
