# M01 — Project Registry
## Brief v1.0a
**Artefact:** M01_ProjectRegistry_Brief_v1_0a
**Status:** LOCKED _(grandfathered: original was "Draft — Pending Review"; Brief was approved at Round 5b → Spec Round 6, content unchanged)_
**Author:** Monish (with Claude assist) _(grandfathered: PMO Director / System Architect)_
**Created:** 2026-05-03 | **Last Updated:** 2026-05-04 (v1.0a in-place patch — Round 29 audit, H15)
**Last Audited:** v1.0a on 2026-05-04
**Reference Standards:** EPCC_NamingConvention_v1_0.md, X8_GlossaryENUMs_v0_1.md _(historical at lock; current X8 v0.6a)_, M34_SystemAdminRBAC_Spec_v1_0.md
**Folder:** /02_L1_Command/
**Phase:** 1 (Foundational — second module after M34)
**Re-Issue Of:** Legacy M01_Project_Registry_v2.1.md (consolidated, not amendment-style)

---

## CHANGE LOG

| Patch | Date       | Author                      | Changes |
|-------|------------|-----------------------------|---------|
| v1.0a | 2026-05-04 | Monish (with Claude assist) | H15 in-place patch (Round 29 audit): added ANALYST + EXTERNAL_AUDITOR rows to §6 ROLES THAT TOUCH THIS MODULE. Both roles canonical since R18 audit; this Brief was authored pre-R18 and never received the propagation cascade. Scope, identity, and decision history unchanged. |

---

## 1. IDENTITY

| Attribute | Value |
|---|---|
| Module ID | M01 |
| Module Name | Project Registry |
| Layer | L1 Command |
| Phase | Phase 1 — Foundational |
| Build Weeks | 4 (estimate from registry) |
| Spec Status | Brief (this) → Spec → Wireframes → Workflows |
| Priority | 🔴 Critical — every other module depends on M01 entities |

---

## 2. DECISION IT ENABLES

> Is this project authorised to exist in the portfolio, and are its foundational parameters — identity, contract, parties, dates, value, thresholds — correctly established as the master reference for all downstream modules?

---

## 3. SCOPE — INCLUDES

| Capability | Description |
|---|---|
| Portfolio / Program / Project hierarchy | 3-level mandatory hierarchy. Multi-portfolio supported. |
| Project identity | code, name, sector, delivery model, geography (pincode), dates, phase, status |
| Multiple contracts per project | Primary / Secondary / Specialist roles |
| Contract financial terms | value (basic + GST), retention, advance, LD, DLP, escalation |
| Party master (global) | Single shared table of external organisations (clients, contractors, consultants) |
| ProjectPartyAssignment | Many-to-many: parties to projects with role |
| Exclusivity tracking | Detect when same party is on multiple active projects in same category |
| Pincode → geography resolution | Embedded `PincodeMaster` (no external API) |
| Scenario configuration | Base / Best / Worst — escalation %, delay months, monsoon, payment delays |
| KPI threshold configuration | Green / Amber / Red bands per KPI per project (per X8 RAGStatus) |
| Project lifecycle phase | Coarse-grained phase progression (per X8 §3.9 Phase enum) |
| Report date | Authoritative "current as-of" date — drives recalculation cascade |
| Soft delete | Per Standards Memory pattern |

---

## 4. SCOPE — EXCLUDES

| Excluded | Where It Lives |
|---|---|
| WBS, packages, BOQ items | M02 Structure & WBS |
| Schedule, milestones, baselines | M03 Planning & Milestones |
| Site progress, NCRs, HSE | M04 Execution Capture |
| Risk register, variation orders | M05 Risk & Change Control |
| Actual cost, billing, retention release | M06 Financial Control |
| EVM (CPI/SPI/EAC) calculation | M07 EVM Engine |
| Stage gate criteria + decisions | M08 Gate Control |
| Compliance, NABH, statutory | M09 Compliance Tracker |
| Portfolio dashboard aggregation | M10 EPCC Command |
| Action items / decision queue resolution | M11 Action Register |
| Tendering / award workflow | M29 Tendering & Award (new) |
| Vendor PQ + scorecards + blacklist | M30 Vendor Master & PQ (new) |
| BG / insurance certificate tracking | M23 BG & Insurance Tracker (Phase 2 sub-module) |
| User accounts and roles | M34 System Administration & RBAC |

---

## 5. ENTITY LIST

| Entity | Purpose | Schema Owner |
|---|---|---|
| `Portfolio` | Top-level grouping | M01 |
| `Program` | Mid-level grouping under portfolio | M01 |
| `Project` | The capital project | M01 |
| `Contract` | Commercial instrument governing the project | M01 |
| `Party` | Global master: clients, contractors, consultants, vendors | M01 |
| `ProjectPartyAssignment` | Party × Project × Role assignment | M01 |
| `ProjectPhase` | Lifecycle phase transition history | M01 |
| `ScenarioConfig` | Per-project scenario parameters | M01 |
| `KPIThreshold` | Per-project KPI bands | M01 |
| `PincodeMaster` | Pincode → state/city/district lookup | M01 (system seed) |

---

## 6. ROLES THAT TOUCH THIS MODULE

References canonical taxonomy from M34 + X8 §4.1. **No new roles introduced.**

| Role (M34 canonical) | Capability |
|---|---|
| `SYSTEM_ADMIN` | Edit Portfolio/Program (system-level setup) |
| `PMO_DIRECTOR` | Full CRUD on Portfolio/Program/Project/Contract; approve exclusivity overrides; change project status; soft delete |
| `PORTFOLIO_MANAGER` | Edit project identity, KPI thresholds, scenario config; view all projects |
| `PROJECT_DIRECTOR` | Edit own project's identity, assign parties to own project; view own project |
| `FINANCE_LEAD` | Edit contract financial terms; view all projects |
| `PROCUREMENT_OFFICER` | View contracts (read-only context) |
| `PLANNING_ENGINEER` | View own project (for schedule context) |
| `QS_MANAGER` | View own project (for measurement context) |
| `SITE_MANAGER` | View own project (for execution context) |
| `COMPLIANCE_MANAGER` | View own project (for compliance context) |
| `READ_ONLY` | View only |
| `ANALYST` | View project registry; run saved filter sets; export data (read + filter + export only) |
| `EXTERNAL_AUDITOR` | Read-only access to project metadata + stage gate history for audit trail |

---

## 7. DEPENDENCIES — IN

| From | Data Required | Trigger |
|---|---|---|
| M34 (RBAC) | User authentication context, role assignments, permission checks | Every API call |
| M07 (EVM) | BAC total per project (for BAC vs contract value deviation check, BR-01-013) | After EVM recalc |
| M08 (Gate Control) | gate_health indicator (% gates cleared) for project card display | After each gate update |
| M09 (Compliance) | pending_clearances_count for KPI calculation | After compliance update |

---

## 8. DEPENDENCIES — OUT

| To | Data Provided | Trigger |
|---|---|---|
| ALL execution modules (M02–M09) | `project_id`, `tenant_id`, project_status, current_phase, dates | On project activation + status change |
| M02 Structure & WBS | project_id, contract_id(s), planned_start/end, phase list | On activation |
| M03 Planning | project_id, planned dates, current_phase, report_date | On activation + report_date change |
| M06 Financial | contract_id, all financial terms, scenario_config | On activation + contract edit |
| M07 EVM | contract_value_basic per contract, KPI thresholds, active_scenario | On activation + threshold/scenario change |
| M08 Gate Control | project_id, current_phase, contract_type, project_status | On phase/status change |
| M10 EPCC Command | All project summary fields for portfolio cards | On any project update |
| M05 Risk & Change | ld_rate_per_week, ld_cap_pct, risk_buffer_pct (from Contract) | On project activation — for LD calculation + contingency init |
| M34 (Party↔User link) | Party records that have linked users (back-reference via User.party_id) | On party create/update |
| M11 Action Register | Decision-triggering events per BR-01-011, BR-01-013 | When triggered |

---

## 9. CRITICAL OPEN QUESTIONS

### OQ-1 (Design — your decision required)

#### OQ-1.1 — `Phase` enum: legacy 5-value vs X8 10-value

**Question:** Legacy M01 v2.1 used `Phase ENUM { DEV / DES / EPC / COM / OAM }` (5 values). X8 §3.9 locks `Phase ENUM { Pre_Investment / Design / Pre_Construction / Construction / Equipment / Commissioning / Empanelment / Handover / DLP / Closed }` (10 values, aligned with SG-0 through SG-11).

**Options:**
- **A** Adopt X8 10-value enum — aligns with stage gates, finer granularity, future-proof for SG-aware analytics
- **B** Keep legacy 5-value enum — simpler, less data migration, but breaks alignment with M08 stage gates
- **C** Hybrid — use X8 10-value internally; UI shows legacy 5-value rollup

**My read:** Legacy values are SG-aware but coarser. X8 alignment with SG enum makes M01.current_phase directly comparable to M08.gate_status. Removes the cognitive cost of two different phase models in the same system.

**Recommendation:** **A — Adopt X8 10-value enum.** Stronger consistency.

---

#### OQ-1.2 — `Sector` as ENUM or CodeMaster

**Question:** Legacy M01 used `Sector ENUM { Healthcare / Infrastructure / Residential / Commercial / Industrial }`. X8 §3.16/3.17 designates Sector as `CodeMaster` (managed at runtime by PMO_DIRECTOR), NOT as a locked ENUM.

**Options:**
- **A** ENUM — locked at code time, requires release to add new sector
- **B** CodeMaster — runtime-editable, version-tracked, tier-controlled (Domain_Specific tier per X8)
- **C** Both — top-level enum (Healthcare / Infrastructure / Other) + CodeMaster sub-types under each

**My read:** Sector list is stable in practice (5 categories cover all of Indian construction), but sub-types proliferate (Hospital_DBOT, Hospital_PPP, Hospital_EPC, Highway, Metro, Railway, etc.). X8 already lists Sector as CodeMaster. Modules like M09 reference sector for compliance template selection — they need stability, not dynamism.

**Recommendation:** **C — Top-level ENUM (5 values) + CodeMaster for sub-types.** Stability where it matters, flexibility where it varies. Define `SectorTopLevel` ENUM in X8 v0.2; add `SectorSubType` CodeMaster category.

---

#### OQ-1.3 — `DeliveryModel`: include "Hybrid"?

**Question:** Legacy M01 used `DeliveryModel ENUM { EPC / DBOT / PPP / Hybrid }`. X8 §3.18 locks `DeliveryModel ENUM { EPC / EPCM / DBOT / PPP / Turnkey / Construction_Management }` — no "Hybrid".

**Options:**
- **A** Drop Hybrid — adopt X8 list as-is. Hybrid model becomes a free-text `delivery_model_notes` field
- **B** Add Hybrid back — append to X8 v0.2
- **C** Keep "Hybrid" as a fallback only (not user-selectable; data migration only)

**My read:** "Hybrid" is a fudge. Real-world projects have specific structures (EPC + O&M = DBOT; EPCM + Turnkey = bespoke). Forcing the spec to be precise prevents data quality drift.

**Recommendation:** **A — Drop Hybrid.** If a project is genuinely "between models", capture exactly which models in `delivery_model_notes` (free text, max 500 chars).

---

#### OQ-1.4 — `ProjectStatus`: include "Draft" state?

**Question:** Legacy M01 used `{ Active / On Hold / Closed / Cancelled }`. X8 §3.8 adds `Draft` as the entry state: `{ Draft / Active / On_Hold / Closed / Cancelled }`.

**Options:**
- **A** Adopt X8 — `Draft` is the initial state until project is "activated" (passes BR-01-010)
- **B** Keep legacy 4-value — projects skip Draft, immediately Active on creation

**My read:** A `Draft` state is consistent with how the system actually works — projects go through SG-0 to SG-3 before being executable. During Draft, BR-01-010 (at-least-one-Primary-contract check) is permitted to fail. After SG-3 (capital sanction), project moves to Active. This matches reality.

**Recommendation:** **A — Adopt X8 `Draft` initial state.** Activation requires explicit BR-01-010 pass.

---

#### OQ-1.5 — `Party` exclusivity: same category or same type?

**Question:** Legacy BR-01-011 says "Party already active on another project in same `party_type` category → Exclusivity Exception." But the rule is ambiguous: same `party_type` (e.g., Contractor) catches all contractors; same `party_role` per project (e.g., Primary Contractor on KDMC AND Secondary Contractor on another) is more nuanced.

**Options:**
- **A** Same `party_type` only (legacy reading) — flag if same Contractor on 2+ active projects, regardless of role
- **B** Same `party_role` — flag only if same Primary role twice (e.g., same firm as Primary Contractor on 2 projects simultaneously)
- **C** Configurable per party_type — Contractors triggered by primary-role overlap; Consultants triggered by any overlap

**My read:** The intent is risk diversification — preventing one contractor from overcommitting capacity across projects. That's a primary-role concern. Specialist subcontractors (e.g., the same lift OEM) routinely serve multiple projects without problem.

**Recommendation:** **B — Same party_role overlap.** Refines BR-01-011 to fire only when role would conflict with capacity.

---

#### OQ-1.6 — Multiple primary contracts: when is this legal?

**Question:** Legacy resolved Block 10 Q1 with "Yes, multiple primaries supported via contract_role ENUM." But no validation rule limits this. A project with 5 simultaneous Primary contracts is structurally suspect.

**Options:**
- **A** Allow unlimited Primary contracts — flexibility. Risk: data quality drift.
- **B** Limit to max 1 Primary at a time — strict. Other contracts must be Secondary or Specialist.
- **C** Allow up to 3 Primary contracts, but flag amber > 1; require 100-char justification > 1

**My read:** Real-world projects sometimes have JV structures (JV between two contractors = both Primary). But > 3 Primary is almost always a data error.

**Recommendation:** **C — Soft cap at 3, amber flag > 1 with justification.** Captures JV reality, prevents drift.

---

#### OQ-1.7 — Report date staleness threshold

**Question:** BR-01-017 daily check flags projects where `report_date` not updated in > 35 days. Why 35? Hospital construction projects update monthly (28–31 days); 35 = 1 month + 4-day buffer. Reasonable but arbitrary.

**Options:**
- **A** Keep 35-day default
- **B** Make configurable per project (default 35)
- **C** Tier by reporting_period_type (M03 setting): Monthly → 35d; Weekly → 10d; Daily → 2d

**Recommendation:** **C — Tier by reporting period.** Aligns with M03 reporting cadence. Monthly projects flagged at 35d; weekly projects flagged at 10d.

---

#### OQ-1.8 — User ↔ Party linkage direction

**Question:** M34 spec already declared `User.party_id` (optional FK) per OQ-1.10. Should M01 also maintain a back-reference (Party.linked_users) or is User → Party direction sufficient?

**Options:**
- **A** One-way (M34 only) — User.party_id, no back-reference. Simple. Query via JOIN when needed.
- **B** Two-way maintained — User.party_id + Party.linked_user_ids JSONB array. Faster lookup but redundancy risk.
- **C** One-way + DB view — User.party_id, plus a materialised view for "users by party" queries

**Recommendation:** **A — One-way only (M34 owns the link).** Single ownership; query JOIN is cheap with proper index.

---

#### OQ-1.9 — Pincode coverage

**Question:** PincodeMaster is "embedded — no external API". India has ~155,000 pincodes. Storing all of them is feasible (~2 MB). But updates (new pincodes added by India Post) are quarterly.

**Options:**
- **A** Static snapshot — load once at install. Manual refresh by SYSTEM_ADMIN when needed.
- **B** Quarterly auto-refresh — system pulls latest pincode dataset from India Post or a maintained mirror
- **C** On-demand validation — accept any 6-digit pincode; resolve via external API only when state/city/district are needed (cache in PincodeMaster)

**Recommendation:** **A — Static snapshot, manual refresh.** Simplicity wins. Hospital projects don't change pincode mid-lifecycle. Refresh annually is fine.

---

#### OQ-1.10 — Soft delete on Project: what cascades?

**Question:** When PMO_DIRECTOR soft-deletes a project (`is_active=false`), what should happen to dependent data in M02–M09?

**Options:**
- **A** Cascade soft-delete to all child records (WBS, BOQ, schedule, NCRs, etc.) — clean, comprehensive
- **B** Set project read-only — child records preserved but locked from edits
- **C** Block soft-delete if any child records exist — force explicit cleanup first

**My read:** Legacy BR-01-014 says "status → Closed → all downstream modules read-only". That's option B for status change. Soft-delete is more drastic — it implies the project shouldn't exist.

**Recommendation:** **C — Block soft-delete if child records exist.** Soft-delete is reserved for projects created in error (no real data). Real projects move to Closed/Cancelled status, not deleted.

---

### OQ-2 (Pattern — defaults proposed, you accept/reject)

| # | Question | Default (proposed) |
|---|---|---|
| OQ-2.1 | KPI threshold defaults | **Keep legacy values** (CPI ≥1.0/0.95, SPI same, Gross Margin ≥20%/10%, Open High Risks ≤5/8, Pending Clearances ≤3/6) — proven on KDMC pilot |
| OQ-2.2 | GST default | **18%** (legacy default; standard for construction in India) |
| OQ-2.3 | Project code format | **`[CLIENT]-[SEQ]-[TYPE]`** e.g., `KDMC-001-DBOT` (legacy default) |
| OQ-2.4 | Reserved fields on every entity | **Per X8 §6** — `tenant_id`, `created_by/at`, `updated_by/at`, `is_active` |
| OQ-2.5 | UUID primary keys | **Yes** — ES-DB-001 |
| OQ-2.6 | Project name uniqueness | **Project code unique system-wide; project name unique within program** (case-insensitive) |
| OQ-2.7 | SLA escalation table for Decision Queue | **Keep legacy table** (12hr / 24hr / 36hr breach with severity escalation) |
| OQ-2.8 | Speed tier for cascade on report_date change | **🔴 Real-time** (legacy lock; cascade is project_month → pct_time_elapsed → M03 PV → M07 EVM → M01 RAG → M10 cards) |
| OQ-2.9 | Default scenario | **Base** (legacy default) |
| OQ-2.10 | Pincode validation timing | **On-blur during entry** (real-time validation, blocks save if invalid) |
| OQ-2.11 | Contract role primary check at activation | **At least one Primary contract required** (BR-01-010 retained) |
| OQ-2.12 | Audit log retention for M01 | **Permanent** for project create, contract create, party assignment, status changes; **7 years** for routine field edits (per X8 + Standards Memory) |

---

## 10. REFERENCE TO EXISTING MODULES

M01 spec rewrite affects every other module that references its entities. Compatibility expected — same entity names, same FK relationships. Differences flagged:

| Module | Likely Update on Re-issue |
|---|---|
| M02 | No structural change — references Project, Contract unchanged |
| M03 | Report date cascade unchanged. Phase enum migration if OQ-1.1 = A |
| M05 | LD/contingency reading unchanged. ScenarioConfig field names unchanged. |
| M06 | Contract financial term references unchanged. Scenario field migration if needed. |
| M07 | KPI threshold reading unchanged. RAG status producer unchanged. |
| M08 | Phase enum alignment — if OQ-1.1 = A, gate-to-phase mapping becomes 1:1 |
| M09 | Sector-driven compliance template selection — if OQ-1.2 = C, CodeMaster sub-type filter required |
| M10 | Project card payload structure unchanged |
| M34 | User.party_id reference unchanged |
| All | Replace mixed-case role refs (`PMO Director`) with M34 canonical (`PMO_DIRECTOR`) |

---

## 11. DELIVERABLES UPON SPEC LOCK

1. `M01_ProjectRegistry_Spec_v1_0.md` — full 10-block spec
2. `M01_ProjectRegistry_Wireframes_v1_0.html` — Project list, detail view, create wizard, contract panel, party assignment, scenario config, KPI thresholds — per role
3. `M01_ProjectRegistry_Workflows_v1_0.md` — Mermaid: project creation flow, activation gating (BR-01-010), report-date cascade, party exclusivity exception flow, status transition flow
4. **Update X8 GlossaryENUMs to v0.2** — add SectorTopLevel enum, append Phase migration note, document any other ENUM additions

---

## 12. RISKS / NOTES

| Risk | Mitigation |
|---|---|
| Phase enum migration breaks downstream modules | OQ-1.1 = A locks the change; affected modules (M03, M08) already reference X8 in their re-issue |
| KDMC pilot data already entered with legacy phase enum (`EPC`) | One-time data migration script: `EPC` → `Construction` |
| Sector ENUM split (top-level + CodeMaster) requires double lookup | Acceptable; Sector data is read-mostly |
| Multiple-Primary-contract soft cap at 3 may be too restrictive for unusual JVs | Override: PMO_DIRECTOR can request higher limit via Decision Queue (one-time per project) |
| Pincode static snapshot becomes stale | Annual refresh by SYSTEM_ADMIN; ~155k records, 2MB file |

---

## 13. APPROVAL GATE

To proceed to Spec writing (Round 6), resolve:

```
OQ-1.1  Phase enum:                  A / B / C        (reco: A — adopt X8)
OQ-1.2  Sector model:                A / B / C        (reco: C — top-level enum + CodeMaster sub-types)
OQ-1.3  DeliveryModel "Hybrid":      A / B / C        (reco: A — drop)
OQ-1.4  ProjectStatus "Draft":       A / B            (reco: A — adopt)
OQ-1.5  Party exclusivity rule:      A / B / C        (reco: B — same party_role)
OQ-1.6  Multiple primary contracts:  A / B / C        (reco: C — soft cap 3)
OQ-1.7  Report date staleness:       A / B / C        (reco: C — tier by reporting period)
OQ-1.8  User-Party linkage:          A / B / C        (reco: A — one-way, M34 owns)
OQ-1.9  Pincode dataset:             A / B / C        (reco: A — static snapshot)
OQ-1.10 Soft delete cascade:         A / B / C        (reco: C — block if child records exist)

OQ-2 defaults: ACCEPT ALL / REJECT [list IDs] / MODIFY [specify]
```

---

## SHORTCUT REPLY

If you accept all my recommendations + OQ-2 defaults:

```
Use all your recommendations + ACCEPT OQ-2 defaults + GO Round 6
```

---

*v1.0 — Brief locked. Awaiting OQ resolutions to proceed to Spec.*
