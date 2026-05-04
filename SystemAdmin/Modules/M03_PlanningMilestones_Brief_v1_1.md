# M03 — Planning & Milestones
## Brief v1.1a
**Status:** LOCKED (Round 15) — superseded by M03_PlanningMilestones_Spec_v1_1 (in-place patched to v1.1a R29)
**Author:** Monish (with Claude assist) _(grandfathered: PMO Director / System Architect)_
**Created:** 2026-05-03 (v1.0) | **Updated:** 2026-05-04 (v1.1a in-place patch — Round 29 audit medium-cleanup, M22; v1.1 update was 2026-05-03 Round 18 audit reference-standards refresh)
**Last Audited:** v1.1a on 2026-05-04
**Re-Issue Of:** Legacy `M03_Planning_Milestones_v2.3.md` (consolidated from v1.0 → v2.3 chain)
**Reference Standards:** X8_GlossaryENUMs_v0_4.md _(historical at v1.1 lock; current X8 v0.6a)_, X9_VisualisationStandards_Spec_v0_2.md _(historical at v1.1 lock; current X9 v0.4)_, M34_SystemAdminRBAC_Spec_v1_0.md, M01_ProjectRegistry_Spec_v1_0.md (+ v1_1/v1_2/v1_3/v1_4 cascade notes), M02_StructureWBS_Spec_v1_0.md (+ v1_1 cascade note)
**Layer:** L2 Control — Planning & Structure
**Phase:** 1 — Foundational
**Build Priority:** 🔴 Critical (precedes M04, M05, M07, M08, M10)
**Folder:** /03_L2_Planning/ _(aspirational; canonical placement is `SystemAdmin/Modules/` per Round 18 audit)_

> **Why M03 matters architecturally:** M03 is the second of three foundational data structures (after M01 + M02). Without M03 locked, none of the downstream execution modules (M04, M05, M06, M07, M08) can be specified. PV is the foundation of EVM; baseline is the criterion for SG-6; schedule is the spine of everything time-bound.

---

## CHANGE LOG

| Version | Date | Author | Change Summary |
|---|---|---|---|
| v1.1a | 2026-05-04 | Monish (with Claude assist) | M22 in-place patch (Round 29 audit medium-cleanup): **Status** UPPERCASE; author canonicalised; `Updated` field refreshed; `Last Audited` field added; `Reference Standards` historical-at-lock annotations added (X8 v0.4 → v0.6a, X9 v0.2 → v0.4); M01 reference extended with v1_3/v1_4 cascade notes; M02 reference extended with v1_1 cascade note; `Folder` field annotated. CHANGE LOG column count standardised 3→4. No scope/content change. |
| v1.0 | 2026-05-03 | PMO Director / System Architect | Initial standalone consolidated brief. Re-issue of legacy v2.3 amendment chain. Aligned with X8 v0.3 ENUMs + X9 v0.1 visualisation references. Audit fixes (F-001, F-003, F-004, F-005, F-007, F-013, F-014) applied. |
| v1.1 | 2026-05-03 | PMO Director / System Architect | **Added Section 8B — Role-Based Default Views for M03 (locked in X9 §13.3.3, surfaced here for validation). Added OQ-1.11 — role-default view adjustments. Updated approval gate to include OQ-1.11.** Brief reference reorganisation; no scope or content drift. |

---

## 1. IDENTITY

```
Module ID                : M03
Module Name              : Planning & Milestones
Layer                    : L2 Control — Planning
Decision It Enables      : Is the project executing within its approved time
                           baseline, and where it is not — is the variance
                           attributable to client (billable), contractor
                           (LD-applicable), neutral event (governed
                           classification), or approved scope extension —
                           such that schedule control, performance
                           measurement, and commercial recovery are all
                           grounded in a single authoritative baseline?

Primary User             : PLANNING_ENGINEER
Secondary Users          : PMO_DIRECTOR (baseline lock + extension approval),
                           PROJECT_DIRECTOR (raise extensions, milestones),
                           PROCUREMENT_OFFICER (procurement schedule),
                           QS_MANAGER, FINANCE_LEAD (PV reads)
Module Icon              : Calendar (Lucide)
Navigation Section       : L2 Control — Planning
```

---

## 2. SCOPE — INCLUDES

| Capability | Description |
|---|---|
| Master Schedule | `ScheduleEntry` per WBS — planned start/finish, baseline dates, float, critical path flag |
| Baseline (single immutable) | `Baseline` snapshot at SG-6; sealed forever |
| Approved Extensions | `BaselineExtension` — cause-classified additions to baseline; commercially tracked |
| Extension Cause Classification | 6 categories with auto-flag rules + PMO override |
| Milestones | `Milestone` — key dates, status, predecessor, gate links, delay tracking |
| Planned Value (PV) | `PVProfile` — time-phased S-curve distributed per WBS per period; foundation of EVM |
| Loading Profiles | `LoadingProfile` — S-curve distribution rules per activity category |
| Resource Allocation | `ResourceAllocation` — role mandatory + named optional |
| Resource Master | `ResourceMaster` — Internal / Contractor / Consultant unified |
| Procurement Schedule | `ProcurementScheduleItem` — lead time, order/delivery dates per package |
| Weather / Monsoon Config | `WeatherWindowConfig` — region-default + project-override |
| Look-ahead Window | Configuration field in `LookAheadConfig` (default 4 weeks; range 2–12) |
| Reporting Period | `reporting_period_type` ENUM per project (Monthly/Weekly/Daily/Event_Driven) |
| Float / Slack | Schedule-calculated, not user-entered |
| Critical Path | Schedule-calculated via inbuilt CPM algorithm |
| Schedule Import | `ScheduleImport` — Primavera P6 / MSP CSV import (modal-gated) |
| Decision Queue Triggers | 5 trigger types feeding M11 |

---

## 3. SCOPE — EXCLUDES

| Excluded | Where It Lives |
|---|---|
| WBS structure and hierarchy | M02 |
| BOQ items + package structure | M02 |
| Actual progress % complete | M04 |
| Actual cost transactions | M06 |
| EVM calculations (CPI, SPI, EAC) | M07 |
| Stage gate approvals | M08 |
| Risk register + variation orders | M05 |
| Vendor PO value + payment terms | M06 |
| Regulatory compliance tracking | M09 |
| Document storage | MinIO + M12 |
| Contractor performance scoring | M04 |
| Sub-contract financial terms | M06 |
| Gate entry/exit criteria | M08 |
| BIM model integration | PF02 (Phase 4) |
| Schedule re-baselining (versioned baselines) | NOT SUPPORTED in v1.0 — single immutable + extensions only |

---

## 4. ENTITY LIST (preview — full schemas in spec)

| Entity | Cardinality | Schema Owner | Notes |
|---|---|---|---|
| `ScheduleEntry` | 1 per WBS node | M03 | Time dimension of every WBS node |
| `Baseline` | 1 per project | M03 | Immutable JSONB snapshot at SG-6 |
| `BaselineExtension` | Many per project | M03 | Cause-classified additions |
| `PVProfile` | 1 per WBS per period | M03 | Time-phased PV (S-curve) |
| `LoadingProfile` | Global shared | M03 | System defaults + user overrides |
| `Milestone` | Many per project | M03 | Key dates, gate-linked optionally |
| `ResourceAllocation` | Many per WBS | M03 | Role + optional named |
| `ResourceMaster` | Global per tenant | M03 | Type-classified: Internal/Contractor/Consultant |
| `ProcurementScheduleItem` | Many per project | M03 | Schedule side only; financial in M06 |
| `WeatherWindowConfig` | Many per project | M03 | Region-default + project-override |
| `LookAheadConfig` | 1 per project | M03 | Window weeks + reporting period type |
| `ScheduleImport` | Many per project | M03 | Primavera/MSP import sessions |

**Entity count: 12** — comparable to M02 (also 12).

---

## 5. ROLES THAT TOUCH M03

| Role | Primary Capabilities |
|---|---|
| PMO_DIRECTOR | Lock baseline, approve extensions, classify Neutral_Event, override flags, all reads |
| PROJECT_DIRECTOR | Create schedule (pre-baseline), raise extensions, milestones, all own-project reads |
| PLANNING_ENGINEER | Master schedule editor (pre-baseline), forecast updates, loading profile config |
| PROCUREMENT_OFFICER | Procurement schedule editor |
| QS_MANAGER | Read schedule + procurement |
| FINANCE_LEAD | Read PV S-curve + procurement schedule |
| SITE_MANAGER | **4-week Look-ahead Gantt** (own packages); read-only |
| COMPLIANCE_MANAGER | Read schedule (for permit timeline overlay) |
| READ_ONLY | Read schedule (scoped) |
| EXTERNAL_AUDITOR | Read schedule + extensions (forensic) |

Full role × action matrix in spec Block 4a. Default views per role specified in **X9 §13.3.3** (locked).

---

## 6. DEPENDENCIES — INPUT

| From | What |
|---|---|
| M34 | Auth context, role, permission scope |
| M01 | `project_id`, `current_phase`, `planned_start_date`, `planned_end_date`, `report_date`, `contract_id` |
| M02 | `wbs_id` list per project, `package_id` list, BAC per package (for PV distribution), WBS hierarchy |
| M05 | `variation_order_id` (linkage for billable extensions); EOT VO triggers BaselineExtension auto-creation |
| M08 | SG-6 gate passage signal → triggers baseline lock |
| M09 | Compliance permit grant dates → auto-populate gate-linked milestone `actual_date` |
| M04 | Material receipt date → populates `actual_delivery_date` on procurement items |

---

## 7. DEPENDENCIES — OUTPUT

| To | What |
|---|---|
| M04 | `wbs_id` list with planned dates → progress capture grain |
| M05 | Schedule context for VO impact assessment |
| M06 | Procurement schedule (PO timing trigger) + PV per period (cashflow forecast) |
| M07 | **PV per period per WBS — foundation of EVM** |
| M08 | Baseline state + gate-linked milestones for gate criteria |
| M09 | Schedule for permit timeline overlay |
| M10 | Schedule health, critical path status, milestone summary, S-curve data |
| M11 | 5 Decision Queue trigger types |

---

## 8. CRITICAL OPEN QUESTIONS (OQ-1) — YOUR DECISION REQUIRED

Most legacy M03 v2.3 design decisions are mature and battle-tested. Below are the questions where genuine drift exists between legacy and X8 v0.3 / X9 v0.1, OR where I believe re-confirmation is warranted before lock.

### OQ-1.1 — Baseline Model: Single Immutable + Extensions vs Versioned Baselines?

**Legacy lock:** Single immutable baseline at SG-6 + Approved Extensions. No re-baselining.

**Question:** Confirm legacy lock?

**Options:**
- **A** Single immutable + Extensions (legacy lock) — every change is BaselineExtension with cause + approver
- **B** Versioned baselines with re-baselining capability — more flexible
- **C** Hybrid — single original baseline, but allow PMO_DIRECTOR to "freeze new baseline" with full audit trail

**Recommendation:** **A — Single immutable + Extensions.** Reasons:
- Audit-clean: every change is causally traceable
- Forces governance discipline
- Industry-canonical for capital projects
- Re-baselining invites baseline drift (PMO can rationalise away schedule slippage)
- Extensions handle every legitimate change use case

---

### OQ-1.2 — BaselineExtension Cause Categories: Lock 6 as ENUM?

**Legacy lock:** 6 categories — `Scope_Addition`, `Design_Change`, `Force_Majeure`, `Client_Delay`, `Contractor_Delay`, `Neutral_Event`.

**Question:** Lock as `BaselineExtensionCause` ENUM in X8 v0.4?

**Options:**
- **A** Lock 6 as-is (legacy lock)
- **B** Add 7th: `Regulatory_Delay` (e.g., AERB clearance overrun) distinct from Force_Majeure
- **C** Reduce to 4: collapse Force_Majeure + Neutral_Event into "External_Event"

**Recommendation:** **A — Lock 6.** Healthcare projects in India regularly encounter regulatory delays, but they're already handled under `Force_Majeure` (with contract clause referencing the regulatory authority). Adding a 7th category creates classification ambiguity. The 6 categories cover all observed cases in the legacy KDMC implementation.

---

### OQ-1.3 — Neutral_Event Auto-Reclassification Rule

**Legacy lock:** If `cause_category=Neutral_Event` AND `contract_clause_ref` blank → auto-reclassify to `Contractor_Delay`. (Logic: contractor's supply chain risk by default unless contract specifies otherwise.)

**Question:** Confirm legacy rule?

**Options:**
- **A** Keep auto-reclassify to `Contractor_Delay` (legacy lock)
- **B** Auto-reclassify to `Force_Majeure` (more contractor-friendly)
- **C** Block save (no auto-reclassification; user must explicitly classify)
- **D** Soft-warn but allow save with PMO_DIRECTOR override

**Recommendation:** **A — Keep legacy.** This is a battle-tested rule that protects the client commercially. Contract clause omission should default to contractor risk; the contractor must affirmatively claim contract relief. Soft-warning (D) creates classification drift.

---

### OQ-1.4 — LoadingProfile Distribution Types: Keep 4 + Custom?

**Legacy lock:** 5 values — `Front_Loaded`, `Bell`, `Back_Loaded`, `Linear`, `Custom`.

**Question:** Lock as `LoadingProfileType` ENUM?

**Options:**
- **A** Lock 5 (Front_Loaded / Bell / Back_Loaded / Linear / Custom) — legacy
- **B** Add 6th: `Double_Hump` (for activities with two peaks, e.g., civil work + commissioning rework)
- **C** Replace `Custom` with formula-based curve specification

**Recommendation:** **A — Lock 5.** `Custom` already covers any non-standard curve through the JSONB `distribution_curve` field. Double_Hump is rare and can be expressed as Custom. Formula-based (C) would require curve-language design work; defer to Phase 2 if real demand emerges.

---

### OQ-1.5 — ResourceMaster Type Taxonomy: 3 Types Locked?

**Legacy lock:** 3 types — `Internal`, `Contractor_Resource`, `Consultant_Resource`.

**Question:** Lock as `ResourceType` ENUM?

**Options:**
- **A** Lock 3 (legacy)
- **B** Add 4th: `Vendor_Resource` (for equipment vendor's onsite engineers — distinct from contractors)
- **C** Add 5th: `External_Auditor_Resource` (third-party QS, NABH consultants)

**Recommendation:** **B — 4 types** (add `Vendor_Resource`).

Rationale: KDMC pilot has MEP equipment vendors (LINAC, MRI, CT) sending field engineers for installation/commissioning. They're operationally distinct from general contractors (different commercial terms, shorter engagement windows, equipment-specific liability). `External_Auditor_Resource` (C) can be merged into `Consultant_Resource`.

This is a minor change to legacy. **Decide before spec.**

---

### OQ-1.6 — Reporting Period Type: Lock 4 ENUM?

**Legacy lock:** 4 values — `Monthly` (default) / `Weekly` / `Daily` / `Event_Driven`.

**Question:** Lock as `ReportingPeriodType` ENUM?

**Options:**
- **A** Lock 4 (legacy)
- **B** Add 5th: `Bi_Weekly` (some clients prefer 2-week reporting for moderate-pace projects)
- **C** Reduce to 3: drop `Event_Driven` (rare in healthcare)

**Recommendation:** **A — Lock 4.** Bi-Weekly is uncommon enough that Weekly + skip-period workflow handles it. Event_Driven is rare but valuable for projects with major irregular phases (e.g., post-monsoon catch-up). The legacy 4 cover all observed cases.

---

### OQ-1.7 — Look-ahead Window Default + Range

**Legacy lock:** Default 4 weeks, configurable range 2–12.

**Question:** Confirm?

**Options:**
- **A** Default 4 weeks, range 2–12 (legacy)
- **B** Default 4 weeks, range 2–8 (tighter cap)
- **C** Sector-default: Healthcare = 4w, Infrastructure = 8w
- **D** Per-role default: Site Manager = 2w, Planning Engineer = 4w, PMO_DIRECTOR = 8w

**Recommendation:** **A — Legacy lock.** 12-week ceiling is rarely used but provides flexibility for long-cycle phases (commissioning). Per-role defaults (D) create UX inconsistency — same project should have one look-ahead window. Sector defaults (C) require sector-config infrastructure; defer to Phase 2.

---

### OQ-1.8 — Reporting Period Type: Module Ownership

**Legacy ambiguity:** `reporting_period_type` is stored in `LookAheadConfig` but referenced by M01 (for project staleness calculation) and M07 (for EVM period boundaries).

**Question:** Where does `reporting_period_type` live?

**Options:**
- **A** M03 owns (`LookAheadConfig.reporting_period_type`); M01 and M07 read via API
- **B** M01 owns (`Project.reporting_period_type`); M03 and M07 read
- **C** M03 owns + duplicate to M01 cache (denormalisation)

**Recommendation:** **A — M03 owns.** Reasoning:
- Reporting period is fundamentally a planning/scheduling concept
- M01 already reads many M03 fields (`baseline_start`, `baseline_finish`)
- Single-Owner rule (F-005) — one entity, one owner
- M01 v1.1 minor bump should remove `reporting_period_type` field if it's there

**Cascade:** If A locked, M01 v1.2 needs to remove `reporting_period_type` field (currently `Project` table per legacy?). Need to verify in M01 spec — flag as cascade item.

---

### OQ-1.9 — Procurement Schedule Scope Boundary

**Legacy ambiguity in v2.3:** M03 owns lead-time + dates; M06 owns financial PO. But "vendor selection" sits between them.

**Question:** Where does vendor identity (vendor_id, vendor_name) live for procurement items?

**Options:**
- **A** M03 stores `selected_vendor_id` (FK → M01 Party) for schedule visibility
- **B** M06 owns vendor identity; M03 references via `m06_po_id` only after PO created
- **C** Hybrid — M03 stores `recommended_vendor_id` (planning-stage); M06 stores final PO vendor

**Recommendation:** **B — M06 owns vendor identity.** Reasoning:
- Single-Owner rule again
- M03 ProcurementScheduleItem tracks WHEN; M06 PO tracks WHO + HOW MUCH
- Until PO is issued, vendor is just a recommendation — not authoritative
- M03 can show vendor name via M06 API when PO exists

---

### OQ-1.10 — Float Visibility Per Role

**Legacy ambiguity in v2.3:** All roles can see float values.

**Question:** Should float values be role-tiered?

**Options:**
- **A** All editing roles see float; READ_ONLY sees status badge only
- **B** Float visible to all (legacy)
- **C** Float hidden from external roles (Client/Contractor/Consultant via portal)

**Recommendation:** **A — All editing roles see float; READ_ONLY sees status only.** Reasoning:
- Float is a strategic information — knowing where buffer exists helps internal teams plan
- External viewers (legal, audit) don't need float; they need outcome state
- Aligns with M02's role-tiered display philosophy
- Float for external party portal users (Phase 2) handled separately when portal ships

---

### OQ-1.11 — Role-Default Views for M03 (Adjustments to X9 §13.3.3)?

**Background:** X9 §13.3.3 (Round 14) locked role-default views for M03. See Section 8B above for the full table.

**Question:** Do the locked X9 §13.3.3 role-default views remain correct for M03, or do specific roles need adjustment?

**Options:**
- **A** Keep all locked X9 §13.3.3 defaults as-is (no changes)
- **B** Adjust specific roles — list which and how
- **C** Significant rework needed — escalate to X9 review

**Specific decision points (sub-questions if Option B):**

| Sub | Adjustment | Default | Reco |
|---|---|---|---|
| 1.11.a | PROJECT_DIRECTOR — add PV S-curve as secondary widget? | No (current) | **Yes — add as secondary.** Project Director balances schedule + cost; PV S-curve is exactly that. |
| 1.11.b | PLANNING_ENGINEER — show PV roll-up (no ₹, just shape)? | No (financials hidden) | **Yes — show shape only.** They build loading profiles; need feedback on aggregate. |
| 1.11.c | COMPLIANCE_MANAGER — invert primary/secondary (milestone timeline primary, permit Gantt secondary)? | Permit Gantt primary | **Keep current.** Permit Gantt is more decision-driving for compliance role. |
| 1.11.d | QS_MANAGER — dedicated view (procurement + measurement context) vs Master Gantt read? | Master Gantt read primary | **Keep current.** QS_MANAGER lives mainly in M02/M14; M03 access is supplementary. |
| 1.11.e | EXTERNAL_AUDITOR — include in M03 default views table? | Currently shown as "Schedule + extension log (forensic)" | **Keep current.** Forensic role; needs schedule + extension audit trail. |

**Recommendation (combined):** **B with adjustments 1.11.a + 1.11.b only.**

- Add PV S-curve as secondary for PROJECT_DIRECTOR (+1.11.a)
- Add PV roll-up shape (no values, just curve) for PLANNING_ENGINEER (+1.11.b)
- All other roles: keep X9 §13.3.3 as locked

**Cascade if locked:** X9 v0.1 → v0.2 minor bump in Round 16. Tiny scope, contained change.

---

## 8B. ROLE-BASED DEFAULT VIEWS FOR M03

**Status:** Locked in X9 §13.3.3 (Round 14) — surfaced here for validation as part of M03 deliberation.

When a user opens M03, they land on a role-specific default view. Per X9 §13.0 architectural rule:

> "Defaults are system-wide, not tenant-overridable in v1.0. User personalisation deferred to Phase 2."

### 8B.1 — Default Views Locked Per Role

| Role | Primary View | Secondary Widgets | Hidden / Restricted |
|---|---|---|---|
| **PMO_DIRECTOR** | Master Gantt with baseline + critical path | Milestone timeline, S-curve variance, RAG status | — |
| **PORTFOLIO_MANAGER** | Schedule variance summary (multi-project) | Cross-project critical path comparison | Single-project detail |
| **PROJECT_DIRECTOR** | Master Gantt (own project) + variance bar | Look-ahead Gantt, milestone timeline | — |
| **PLANNING_ENGINEER** | WBS Gantt builder + float histogram | Critical path DAG, baseline lock state | Financials |
| **SITE_MANAGER** | **4-week Look-ahead Gantt** | Today's milestones, resource roster | Master Gantt, financials, baseline detail |
| **QS_MANAGER** | Master Gantt (read) + procurement schedule | BOQ progress | — |
| **FINANCE_LEAD** | PV S-curve + procurement Gantt | Financial milestones, schedule variance ₹ impact | — |
| **PROCUREMENT_OFFICER** | Procurement Gantt | Long-lead-time alerts, vendor schedule | Master Gantt detail |
| **COMPLIANCE_MANAGER** | Permit Gantt + milestone timeline | Compliance events on schedule | — |
| **READ_ONLY** | Master Gantt (read-only) | — | Most widgets |
| **EXTERNAL_AUDITOR** | Schedule + extension log (forensic) | Audit trail | Operational dashboards |

### 8B.2 — Site Manager Subtraction Principle

SITE_MANAGER intentionally sees only:
- Action-oriented views (4-week look-ahead, today's milestones, resource roster)
- Hidden: master schedule complexity, baseline detail, financials
- Rationale: Site Manager's job is **execution**, not strategy. Surfacing strategic dashboards distracts from operational work.

### 8B.3 — Validation Questions (resolve via OQ-1.11)

Surface for your review before lock:

1. Should **PROJECT_DIRECTOR** see PV S-curve as a secondary widget? Currently PV is reserved for FINANCE_LEAD. Project Director cares about schedule + cost balance.
2. Should **PLANNING_ENGINEER** see PV roll-up despite being non-financial? They build loading profiles that produce PV — knowing aggregate shape may help calibration.
3. Should **COMPLIANCE_MANAGER** see compliance milestone timeline as primary, with permit Gantt secondary? Reverse of current ordering.
4. Should **QS_MANAGER** have their own dedicated view (e.g., procurement + measurement context) rather than Master Gantt read?
5. Should **EXTERNAL_AUDITOR** appear in the M03 default view table at all? Currently shows forensic schedule + extension log — confirm this is appropriate.
6. Are there roles missing from the table? (Currently: 11 roles. The 2 not addressed: ROLE_X if any.)

### 8B.4 — Reference Format in M03 Spec

When M03 spec is written (Round 16), Block 5 (Filters & Views) will reference X9 §13.3.3:

```
M03 Block 5 — Filters and Views
─────────────────────────────────
5a. Default Role-Based Views: see X9 §13.3.3 M03 — Planning & Milestones
5b. View Components: as listed below (each with full spec)
```

This keeps single source of truth (no duplication between X9 and M03 spec).

### 8B.5 — Cascade Implication if Adjustments Made

If OQ-1.11 reveals role-default changes needed:

- X9 v0.1 → v0.2 minor bump
- X9 §13.3.3 table updated
- Audit log entry: `ROLE_DEFAULT_VIEW_CHANGED`
- M03 spec references the updated X9 v0.2

---

## 9. PATTERN DEFAULTS (OQ-2) — ACCEPT/REJECT

| # | Pattern | Default (proposed) | Rationale |
|---|---|---|---|
| OQ-2.1 | UUID primary keys | Yes (per X8 §6) | Standard |
| OQ-2.2 | Reserved fields (tenant_id, created_*, updated_*, is_active) | Yes (per X8 §6) | Standard |
| OQ-2.3 | Soft delete pattern | Yes (per X8 §6) | Standard |
| OQ-2.4 | Schedule date format | ISO 8601 (DATE only, no TIME for schedule entries) | Time-of-day not relevant for project schedule |
| OQ-2.5 | PV currency | Inherits M01 contract currency (typically INR) | Avoid currency drift |
| OQ-2.6 | Float threshold for amber RAG | < 10 days | Industry standard near-critical threshold |
| OQ-2.7 | Critical path inclusion threshold | float ≤ 0 days | Industry standard |
| OQ-2.8 | Default reporting period | `Monthly` (KDMC pilot uses monthly) | Most common in Indian capital projects |
| OQ-2.9 | Audit retention — baseline events | Permanent | Forensic requirement |
| OQ-2.10 | Audit retention — routine events | 7 years | Compliance norm |
| OQ-2.11 | CSV import file size limit | 20 MB / 10,000 rows | Aligns with M02 CSV import limits |
| OQ-2.12 | Schedule import sources | Primavera P6 (XML, XER) + MSP (XML) | Industry-standard formats |

**Reply:** ACCEPT ALL / REJECT [list IDs] / MODIFY [specify]

---

## 10. CASCADE IMPLICATIONS

If recommendations locked, these cascades trigger:

### 10a. X8 v0.4 Update (NEW ENUMs)

| New ENUM | Values |
|---|---|
| `BaselineExtensionCause` | Scope_Addition, Design_Change, Force_Majeure, Client_Delay, Contractor_Delay, Neutral_Event |
| `LoadingProfileType` | Front_Loaded, Bell, Back_Loaded, Linear, Custom |
| `ResourceType` | Internal, Contractor_Resource, Consultant_Resource, **Vendor_Resource** (new per OQ-1.5) |
| `ReportingPeriodType` | Monthly, Weekly, Daily, Event_Driven |
| `MilestoneStatus` | Not_Started, In_Progress, Achieved, Delayed, At_Risk |
| `MilestoneType` | Design, Procurement, Construction, Commissioning, Regulatory, Financial, Handover |
| `ScheduleEntryStatus` | Not_Started, In_Progress, Completed, Delayed |
| `ProcurementItemStatus` | Planned, RFQ_Issued, Order_Placed, Manufactured, In_Transit, Delivered, Installed |
| `WeatherWindowSeverity` | Low, Medium, High, Severe (productivity factor bands) |
| `BaselineExtensionStatus` | Pending, Approved, Rejected |
| `ScheduleImportSource` | Primavera_P6_XML, Primavera_P6_XER, MSP_XML |
| `ScheduleImportMode` | Create_Only, Create_And_Update (matches M02 CSVImportMode pattern) |

**X8 v0.4 estimated:** ~12 new ENUMs.

### 10b. M01 v1.2 Cascade (if OQ-1.8=A locked)

If `reporting_period_type` moves from M01 to M03 ownership, M01 needs minor bump:
- Remove field `Project.reporting_period_type` (if currently in M01)
- M01 spec Block 7 (Integration Points) updated to read this from M03

**Decide:** Apply M01 v1.2 cascade in same Round 16 (with M03 spec)? Or defer?

**Recommendation:** Apply in same round — minor bump, contained scope.

### 10c. X9 v0.1 → v0.2 Cascade (if OQ-1.11 = B with adjustments)

If OQ-1.11 locks adjustments to role-default views (recommended adjustments: 1.11.a + 1.11.b):

- X9 v0.1 → v0.2 minor bump in Round 16
- §13.3.3 M03 table updated:
  - PROJECT_DIRECTOR: add "PV S-curve (cost overlay)" to Secondary widgets
  - PLANNING_ENGINEER: add "PV roll-up shape (no values)" to Secondary widgets
- Audit log: `ROLE_DEFAULT_VIEW_CHANGED` per role
- M03 spec references X9 v0.2 (not v0.1)
- Living document discipline maintained — same pattern as X8 lifecycle

### 10d. Future Modules That Will Reference M03

- M04 will read `wbs_id` list, planned dates per WBS
- M05 will read schedule context for VO impact + EOT triggers
- M06 will read PV per period for cashflow forecast
- **M07 will read PV per period for EVM** (most critical dependency)
- M08 will read baseline lock state + gate-linked milestones
- M09 will overlay permit Gantt on schedule
- M10 will roll up schedule health into Command dashboard

---

## 11. DELIVERABLES UPON SPEC LOCK

| Round | Artefact | Description |
|---|---|---|
| 15 (this) | `M03_PlanningMilestones_Brief_v1_1.md` | This file (v1.1 — added Section 8B + OQ-1.11) |
| 16 | `M03_PlanningMilestones_Spec_v1_0.md` + `X8_GlossaryENUMs_v0_4.md` | Full 10-block spec; X8 living doc bumped with M03 ENUMs |
| 16 (cascade if 1.11=B) | `X9_VisualisationStandards_Spec_v0_2.md` | Minor bump if OQ-1.11=B; updates §13.3.3 M03 role defaults |
| 16 (cascade if 1.8=A) | `M01_ProjectRegistry_Spec_v1_2.md` | Minor bump if OQ-1.8=A locked (remove reporting_period_type) |
| 17 | `M03_PlanningMilestones_Wireframes_v1_0.html` | First module to use X9 charts: Master Gantt, S-curve, Milestone Timeline, Resource Histogram, PV S-curve, Procurement Gantt, Look-ahead, Float Histogram, Critical Path DAG |
| 18 | `M03_PlanningMilestones_Workflows_v1_0.md` | Mermaid flows: schedule create, baseline lock, extension approval, PV recalc cascade, schedule import |

After Round 18: M03 module COMPLETE. Master progress: 17/85 done.

---

## 12. RISKS / NOTES

| Risk | Mitigation |
|---|---|
| M03 has 12 entities — spec will be substantial (~1000 lines) | Acceptable; M02 was 871 lines; M03 has more entities + more BRs |
| LoadingProfile defaults are sector-specific (Civil ≠ MEP) | Per-package activity_type override allowed; Healthcare-tuned defaults shipped |
| Baseline lock at SG-6 cross-references M08 | M08 spec (when re-issued) must respect this contract — flag M08 brief input |
| KDMC pilot uses Monthly reporting; weekly projects may emerge | OQ-2.8 default Monthly; per-project configurable |
| Float visibility is contested | OQ-1.10 explicit role mapping locked |
| Schedule import (P6/MSP) is parser-heavy backend work | Defer parser implementation to Round 18+ build phase; spec only |
| `reporting_period_type` ownership ambiguous between M01 and M03 | OQ-1.8 surfaces this explicitly; cascade flagged |
| Vendor_Resource (OQ-1.5) is minor change to legacy | Justified by KDMC MEP vendor reality |
| Critical path computation is performance-sensitive (CPM algorithm) | Spec will include performance budget; algo can use pre-computed snapshots |

---

## 13. APPROVAL GATE

To proceed to Spec writing (Round 16), resolve:

```
OQ-1.1   Baseline model:                A / B / C        (reco: A — single + extensions)
OQ-1.2   Cause categories:              A / B / C        (reco: A — lock 6)
OQ-1.3   Neutral_Event auto-reclassify: A / B / C / D    (reco: A — keep legacy)
OQ-1.4   LoadingProfile types:          A / B / C        (reco: A — lock 5 incl Custom)
OQ-1.5   ResourceType taxonomy:         A / B / C        (reco: B — 4 types incl Vendor_Resource)
OQ-1.6   ReportingPeriodType:           A / B / C        (reco: A — lock 4)
OQ-1.7   Look-ahead window:             A / B / C / D    (reco: A — default 4w, range 2-12)
OQ-1.8   reporting_period_type owner:   A / B / C        (reco: A — M03 owns; M01 v1.2 cascade)
OQ-1.9   Procurement vendor identity:   A / B / C        (reco: B — M06 owns)
OQ-1.10  Float visibility:              A / B / C        (reco: A — editing roles see; READ_ONLY status only)
OQ-1.11  Role-default views (X9 §13.3.3):  A / B / C     (reco: B — adjustments 1.11.a + 1.11.b only)
   1.11.a  PROJECT_DIRECTOR + PV S-curve secondary?     (reco: yes)
   1.11.b  PLANNING_ENGINEER + PV roll-up shape?         (reco: yes)
   1.11.c  COMPLIANCE_MANAGER invert primary/secondary?  (reco: no — keep current)
   1.11.d  QS_MANAGER dedicated view?                    (reco: no — keep current)
   1.11.e  EXTERNAL_AUDITOR included?                    (reco: yes — keep current)

OQ-2 defaults: ACCEPT ALL / REJECT [list IDs] / MODIFY [specify]
```

---

## SHORTCUT REPLY

If you accept all my recommendations + OQ-2 defaults:

```
Use all your recommendations + ACCEPT OQ-2 defaults + GO Round 16
```

---

## 14. PREVIEW — WHAT ROUND 16 WILL DELIVER

M03 spec will be the first module to fully reference both X8 (ENUMs) AND X9 (charts + role-default views). Block structure:

- Block 1: Identity (locked from this brief)
- Block 2: Scope Boundary (locked from this brief)
- Block 3: Data Architecture — 12 entities with full schemas, validation rules, source attribution
- Block 4: Data Population Rules — role × action matrix, mandatory fields, entry methods, defaults
- Block 5: Filters & Views — **references X9 §8.3 and §13.3.3** (no inline redefinition)
- Block 6: Business Rules — ~30 BRs covering schedule, baseline, extensions, PV, milestones, resources, procurement, weather
- Block 7: Integration Points — M34, M01, M02, M04, M05, M06, M07, M08, M09, M10, M11
- Block 8: Governance & Audit — full audit trail per BR; permanent retention for baseline events
- Block 9: Explicit Exclusions — boundary table
- Block 10: Open Questions — must close at zero before lock

Plus appendices: API surface, KDMC reference data migration, X8 ENUM additions.

---

*v1.1 — Brief locked. Awaiting OQ resolutions (now 11 OQ-1 + 12 OQ-2) to proceed to M03 Spec (Round 16).*
