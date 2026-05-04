# CLAUDE.md — EPCC Project Context

> **Master context for the EPCC build.** Loaded at the start of every Claude Code session. Keep this file SHORT — detailed rules live in `.claude/rules/`.

**Last Updated:** 2026-05-04 (Round 28 — M06 cascade pass LOCKED, post-merge renumbering applied to avoid collision with parallel Round 23 = EPCC_BuildArchitecture Brief on `main`)
**Current Phase:** Phase 1 — Foundational Module Specifications · **parallel: Phase 1B Build Architecture (Round 23 IN DRAFT on `main`)**
**Active Rounds:**
- **Round 23 IN DRAFT (on `main`):** `System Specs/EPCC_BuildArchitecture_Brief_v1_0.md` — surfaces 10 OQ-1 + ~30 OQ-2 decisions for the build (repo strategy, branch model, sequencing, OIDC, multi-tenancy, pilot seed, CI host, BR-tagged tests, ENUM codegen). Recommends monorepo on `main` + thin vertical slice (M34 → M01 demo) before module deepening. Awaiting Monish OQ-1 answers before Round 23 Spec drafts.
- **Rounds 24–28 LOCKED (this branch — formerly numbered 23–27 in pre-merge drafts):** M06 FinancialControl module (Brief R24 → Spec R25 → Wireframes R26 → Workflows R27) + cascade pass R28 (X8 v0.6, X9 v0.4, M01 v1.3 cascade note, M03 v1.2 cascade note, naming-folders.md refresh).
- **Round-renumbering note:** Pre-merge commit messages (`50cb092`, `eeead43`, `aa058a9`, `c3d20c4`, `276d3e0`) say "Round 23–27" — historical record only. File content + audit stamps are authoritative at Round 24–28.

---

## 1. What is EPCC?

**Enterprise Project Management System** being built greenfield by **Monish** for Indian healthcare infrastructure. Operates across **EPC, DBOT, and PPP** delivery models in multi-project, capital-intensive environments.

**Core philosophy — organisational nervous system:**
- Leadership = Brain (strategy and decisions)
- Projects = Actions (execution)
- Departments = Organs (capabilities)
- Data Systems = Nervous system (visibility and feedback)

**This is NOT** a consulting engagement, a redesign of existing software, or a modification of the KDMC workbook. It IS greenfield software (spec-first, full architectural lockdown before code) that will eventually replace the workbook.

---

## 2. Pilot Project — KDMC

| Field | Value |
|---|---|
| Project code | `KDMC-001-DBOT` |
| Sector | Healthcare → Hospital_DBOT |
| Value | ₹68.4 Cr |
| Type | 150-bed Maternity, Cancer & Cardiology Hospital |
| Client | Kalyan-Dombivli Municipal Corporation |
| Contractor | L&T Construction |
| Phase | Construction (current) |
| Pincode | 421203 (Kalyan-Dombivli, Maharashtra, West region) |
| Source data | `KDMC_CC_Transformed.xlsm` (~12,000 formulas, 45 sheets) |
| Workbook password | `KDMC2025` |

**4 unresolved workbook items** (tracked, NOT being addressed in EPCC build): PKG-to-WBS mapping, Snapshot macro, Named range rollout, Progress_Calc % integration.

---

## 3. Current Module Status

### Foundation + first execution module: COMPLETE

| Module | Brief | Spec | Wireframes | Workflows | Round |
|---|---|---|---|---|---|
| M34 SystemAdminRBAC | N/A — foundation module, direct to Spec at R4 | Done | Done | Done | 1–4 |
| M01 ProjectRegistry | Done | Done v1.0 (+ v1.1 + v1.2 + v1.3 cascade notes) | Done | Done | 5b–8, 16, 18-audit, 28 |
| M02 StructureWBS | Done | Done | Done | Done | 9–12 |
| M03 PlanningMilestones | Done | Done v1.1 (+ v1.2 cascade note) | Done | Done | 15–18, 28 |
| **M04 ExecutionCapture** | Done v1.0 (R19) | Done v1.0 (R20) | Done v1.0 (R21) | Done v1.0 (R22) | 19–22 |
| **M06 FinancialControl** | Done v1.0 (R24) | Done v1.0 (R25) + v1.0a audit-corr (R27) | Done v1.0 (R26) | Done v1.0 (R27) | 24–28 |

### Cross-cutting

| Doc | Version | Status |
|---|---|---|
| X8 GlossaryENUMs | **v0.6** | Living (M06 ENUMs locked Round 28 — 13 new ENUMs + 43-event AuditEventType ext + 12-trigger DQ ext + 4-ledger §6 ext + SG_9/SG_11 description refresh) |
| X9 VisualisationStandards | **v0.4** | Living (M06 §13.3.6 5→8 roles + §9.5.1 flagship annotation locked Round 28 — zero new chart types) |
| EPCC_NamingConvention | v1.0 | Locked |
| EPCC_FolderIndex | v1.0 | Locked |
| EPCC_VersionLog | v1.1 | Living (reconciled Round 18) |
| AUDIT_Round00 | v1.0 | Locked (22 findings) |
| EPCC_DevSkillsRequired | v1.0 | Locked (~8.5 FTE Phase 1) |

### Pending cascades

- _(none — M01 v1.1 cascade closed Round 18 audit, now documented in `M01_ProjectRegistry_v1_1_CascadeNote.md`)_

### Phase 1 progress

**Total deliverables:** ~85 · **Done:** 32 · **Remaining:** 53 (M06 module COMPLETE + cascade pass closed Round 28 — X8 v0.6 + X9 v0.4 + M01 v1.3 + M03 v1.2 + naming-folders.md refresh)

---

## 4. Locked Decisions — Do Not Revisit

These have been resolved through deliberation. Do not re-open without explicit user direction.

| Topic | Decision |
|---|---|
| Architecture | Greenfield (U3-a) |
| Workbook role | EPCC replaces it (U2-a) |
| Density | Full density, future-proofed (A) |
| Spec template | 10-block structure |
| Cadence | C1 — one artefact at a time |
| Wireframes | Full HTML, Tailwind CDN, no JS deps (D3) |
| Workflows | Mermaid in markdown |
| Phase enum | 10-value (X8 v0.2) |
| Role names | UPPER_SNAKE_CASE canonical (F-014) |
| Decision Queue triggers | UPPER_SNAKE_CASE (F-013) |
| Existing specs | U1-a — locked under v1.0 re-issue |
| Sector model | SectorTopLevel ENUM + CodeMaster sub-types |
| DeliveryModel "Hybrid" | Retired — use free-text notes |
| Project state machine | Draft → Active → terminal (BR-01-024) |
| Closed/Cancelled | Irreversible — must create new project |
| Pincode | Static snapshot ~155k records |
| Field-level rate display | API-serialiser enforced (M02 OQ-2.11) |
| Three-tier templates | Copy-down only; no upward promotion (BR-02-035) |
| BACIntegrityLedger | DB-level UPDATE/DELETE forbidden |
| Cascade pattern | Surgical changes (1 field/BR) → cascade note. Substantive changes (new appendix, multiple BRs, new entity) → full spec re-issue with `git mv` rename (Round 18 audit) |
| Audit stamp formats | 3 accepted: YAML frontmatter (preferred new), markdown bold-header (grandfathered M34/M01/M02/M03), HTML comment (wireframes). See spec-protocol.md (Round 18 audit) |
| Folder placement | Active modules: `SystemAdmin/Modules/`. X-series: `SystemAdmin/Cross-link files/`. Governance: `System Specs/`. 13-folder hierarchy aspirational only (Round 18 audit) |
| Role taxonomy | 13 internal + 4 external = 17. Authoritative source: M34 Spec Block 3. Includes ANALYST (was missing from cross-cutting-standards.md until Round 18 audit) |
| Financial Control state machine | 4-state CostLedgerEntry — Budgeted → Committed → Accrued → Paid. Forward-only; reversals via compensating entries only; UPDATE/DELETE forbidden at DB level (M06 BR-06-001..047, X8 v0.6 §3.60) |
| RA Bill trigger sources | Dual: Progress (M04 BILLING_TRIGGER_READY) + Milestone (M03 MILESTONE_ACHIEVED_FINANCIAL). Both written via M06 RABillTriggerSource ENUM (X8 v0.6 §3.63, M06 OQ-1.3=B) |
| Retention release | Tranche-1 at SG-9 passage; Tranche-2 at SG-11 passage. Per-contract split percentage on `M01.Contract.dlp_retention_split_pct` (default 0.5000); PMO override allowed with justification ≥100 chars + digital evidence (M06 OQ-1.8=C, M01 v1.3 cascade note) |
| Multi-currency | Shipped in v1.0 with 2-tier exchange rate model (RBI_Reference + Bank_Transaction); Forecast/Budgeted/Committed valued at RBI_Reference; Paid reconciled at Bank_Transaction (M06 OQ-1.6=B, X8 v0.6 §3.71) |
| BG tracking | BGStub pattern in Phase 1 (status + expiry only); full lifecycle migrates to M23 in Phase 2; BGType ENUM stays in X8 (M06 OQ-1.9=B, X8 v0.6 §3.72) |
| Stage Gate description (SG_9 / SG_11) | SG_9 = Substantial / Practical Completion (clinical commissioning ready); SG_11 = DLP End / Operations Handover. Sequence locked at v0.1; description text refreshed v0.6 to ratify M06 commitments before M08 brief opens (X8 v0.6 §3.10) |
| Capital Funnel flagship | M06 Capital Funnel = 1st named flagship instance of §11 Pipeline Funnel pattern (X9 v0.4 §9.5.1 annotation; chronologically M04 NCR Funnel was 8th, but Capital Funnel is the formally-designated flagship) |

---

## 5. Where to Find Detailed Rules

This file is intentionally short. Detailed rules live in `.claude/rules/`:

| File | What's in it |
|---|---|
| [`architecture.md`](.claude/rules/architecture.md) | 5-layer model, stage gates, financial control states, EVM metrics, tech stack |
| [`spec-protocol.md`](.claude/rules/spec-protocol.md) | Cadence C1, 4 artefacts, 10-block template, audit stamps, I1–I10 |
| [`naming-folders.md`](.claude/rules/naming-folders.md) | File naming, identifier conventions, 13-folder hierarchy |
| [`cross-cutting-standards.md`](.claude/rules/cross-cutting-standards.md) | X1–X9 index, X8 ENUM map, X9 viz rules, role mappings |
| [`principles.md`](.claude/rules/principles.md) | Operating principles + failure modes to avoid |
| [`glossary.md`](.claude/rules/glossary.md) | Domain vocabulary (BAC, EVM, BOQ, NABH, etc.) |
| [`re-entry-protocol.md`](.claude/rules/re-entry-protocol.md) | What to read at session start; canonical reference router |

Personal working style + persona live in `~/.claude/CLAUDE.md` (global).

---

## 6. Skills (Custom Commands)

| Command | What it does |
|---|---|
| `/new-round` | Scaffolds a new round folder + artefact template with locked headers and version-log entry |
| `/lock-decision` | Records a locked decision across VersionLog + this CLAUDE.md table + audit notes |

See `.claude/skills/` for definitions.

---

## 7. Re-Entry Protocol

When a new Claude session starts:

1. Read this file in full
2. Read `.claude/rules/re-entry-protocol.md` for the full read order
3. Confirm current round + next artefact with Monish
4. **Do not auto-start work**

---

*— CLAUDE.md v2.0 — Restructured 2026-05-03. Detailed rules moved to `.claude/rules/`. Update this file on every module completion + every X8/X9 version bump.*
