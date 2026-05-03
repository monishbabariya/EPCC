# CLAUDE.md — EPCC Project Context

> **Master context for the EPCC build.** Loaded at the start of every Claude Code session. Keep this file SHORT — detailed rules live in `.claude/rules/`.

**Last Updated:** 2026-05-03 (after Round 17 — M03 Wireframes; FIRST module using X9 charts)
**Current Phase:** Phase 1 — Foundational Module Specifications
**Active Round:** Awaiting Round 18 (M03 Workflows — completes M03 module)

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
| M34 SystemAdminRBAC | Done | Done | Done | Done | 1–4 |
| M01 ProjectRegistry | Done | Done (v1.2 cascade note) | Done | Done | 5b–8, 16 |
| M02 StructureWBS | Done | Done | Done | Done | 9–12 |
| **M03 PlanningMilestones** | Done | Done | Done | Pending Round 18 | 15–17 |

### Cross-cutting

| Doc | Version | Status |
|---|---|---|
| X8 GlossaryENUMs | **v0.4** | Living |
| X9 VisualisationStandards | **v0.2** | Living |
| EPCC_NamingConvention | v1.0 | Locked |
| EPCC_FolderIndex | v1.0 | Locked |
| EPCC_VersionLog | v1.0 | Locked (appended per round) |
| AUDIT_Round00 | v1.0 | Locked (22 findings) |
| EPCC_DevSkillsRequired | v1.0 | Locked (~8.5 FTE Phase 1) |

### Pending cascades

- **M01 v1.1** — add `Project.min_wbs_depth` field (per OQ-1.1=B from M02)

### Phase 1 progress

**Total deliverables:** ~85 · **Done:** 18 · **Remaining:** 67

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
