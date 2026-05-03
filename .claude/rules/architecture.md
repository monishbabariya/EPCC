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
| Authentication | OIDC (with local password fallback) |

---

## Single-Owner Rule (F-005)

Every entity has exactly one owning module. Cross-module access is via internal API, **never** direct DB read.
