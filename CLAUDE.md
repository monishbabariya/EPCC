# CLAUDE.md — EPCC Project Context

> **Master context for the EPCC build.** Loaded at the start of every Claude Code session. Keep this file SHORT — detailed rules live in `.claude/rules/`.

**Last Updated:** 2026-05-03 (Round 24 — M06 FinancialControl Spec v1.0 LOCKED via /build-module pipeline)
**Current Phase:** Phase 1 — Foundational Module Specifications
**Active Round:** Round 24 — M06 Spec LOCKED (iter 1 + 3 cosmetic fixes). Wireframes gate firing next.

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
| M01 ProjectRegistry | Done | Done v1.0 (+ v1.1 + v1.2 cascade notes) | Done | Done | 5b–8, 16, 18-audit |
| M02 StructureWBS | Done | Done | Done | Done | 9–12 |
| **M03 PlanningMilestones** | Done | Done (v1.1) | Done | Done | 15–18 |
| **M04 ExecutionCapture** | Done v1.0 (R19) | Done v1.0 (R20) | Done v1.0 (R21) | Done v1.0 (R22) | 19–22 |
| **M06 FinancialControl** | Done v1.0 (R23) | Done v1.0 (R24) | Pending R25 | Pending | 23–24 |

### Cross-cutting

| Doc | Version | Status |
|---|---|---|
| X8 GlossaryENUMs | **v0.5** | Living (M04 ENUMs locked Round 20) |
| X9 VisualisationStandards | **v0.3** | Living (M04 §13.3.4 row locked Round 20) |
| EPCC_NamingConvention | v1.0 | Locked |
| EPCC_FolderIndex | v1.0 | Locked |
| EPCC_VersionLog | v1.1 | Living (reconciled Round 18) |
| AUDIT_Round00 | v1.0 | Locked (22 findings) |
| EPCC_DevSkillsRequired | v1.0 | Locked (~8.5 FTE Phase 1) |

### Pending cascades

- _(none — M01 v1.1 cascade closed Round 18 audit, now documented in `M01_ProjectRegistry_v1_1_CascadeNote.md`)_

### Phase 1 progress

**Total deliverables:** ~85 · **Done:** 28 · **Remaining:** 57 (M06 Spec v1.0 locked Round 24)

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
