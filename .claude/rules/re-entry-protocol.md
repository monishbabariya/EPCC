# Re-Entry Protocol for New Sessions

> **Purpose:** What Claude does at the start of every new session (compaction, fresh chat, context reset). Locked sequence.

---

## Read Order

When a new session starts, Claude must read these in order before doing anything else:

1. **`CLAUDE.md`** (project root) — project identity, current round status, locked decisions table
2. **`.claude/rules/spec-protocol.md`** — cadence, 10-block template, audit stamps
3. **`.claude/rules/cross-cutting-standards.md`** — current X8 + X9 versions, role mappings
4. **Most recent Round folder's deliverables** (check Section 9 of `CLAUDE.md` to find which round)
5. **The active X8 file** at the version listed in `cross-cutting-standards.md` (currently `SystemAdmin/Cross-link files/X8_GlossaryENUMs_v0_8.md`)
6. **M34 + M01 + M02 specs** as foundation references

---

## After Reading

- ❌ DO NOT auto-start work
- ❌ DO NOT assume continuation from a prior session
- ✅ Confirm the current round number with Monish
- ✅ Confirm which artefact (Brief / Spec / Wireframes / Workflows) is the next deliverable
- ✅ Wait for explicit instruction before generating

---

## When Memory Disagrees with Files

If a memory record conflicts with what the files say:

- **Files win.** Memory is a snapshot; files are source of truth.
- Update or remove the stale memory.

---

## When Asked Where to Find Something

Always cite the canonical reference rather than answering from memory:

| Topic | Canonical Source |
|---|---|
| Authentication, RBAC, roles, permissions | `SystemAdmin/M34_SystemAdminRBAC_Spec_v1_0.md` |
| Project lifecycle, phase, status, contract structure | `SystemAdmin/Modules/M01_ProjectRegistry_Spec_v1_0.md` (read with `M01_ProjectRegistry_v1_1_CascadeNote.md` adding `min_wbs_depth`, `M01_ProjectRegistry_v1_2_CascadeNote.md` removing `reporting_period_type`, `M01_ProjectRegistry_v1_3_CascadeNote.md` adding `Contract.dlp_retention_split_pct` + BR-01-036, and `M01_ProjectRegistry_v1_4_CascadeNote.md`) |
| WBS, BOQ, packages, BAC, templates, units | `SystemAdmin/Modules/M02_StructureWBS_Spec_v1_0.md` |
| Schedule, baseline, milestones, PV, procurement timing, audit events | `SystemAdmin/Modules/M03_PlanningMilestones_Spec_v1_1.md` (read with `M03_PlanningMilestones_v1_2_CascadeNote.md` adding `MILESTONE_ACHIEVED_FINANCIAL` emit hook + BR-03-035 + SENDS TO M06, and `M03_PlanningMilestones_v1_3_CascadeNote.md`) |
| Progress capture, NCRs, material receipts, contractor scoring, ProjectExecutionConfig | `SystemAdmin/Modules/M04_ExecutionCapture_Spec_v1_0.md` (read with Brief v1.0 as decision-history reference + Workflows v1.0 for runtime flows) |
| Cost ledger, RA bills, GRN/invoice match, retention, forex, BG stubs, payment evidence, ProjectFinancialConfig | `SystemAdmin/Modules/M06_FinancialControl_Spec_v1_0.md` (v1.0b in-place patch R29 — read with Brief v1.0 as decision-history reference + `M06_FinancialControl_v1_1_CascadeNote.md` + Workflows v1.0 for runtime flows) |
| Risk register (5×5), VO 7-state, EOT, EWN, LD accrual, contingency drawdown, ARTA response, ProjectRiskConfig | `SystemAdmin/Modules/M05_RiskChangeControl_Spec_v1_0.md` (LOCKED R33; read with Brief v1.0a (R31, 7-state VO patch R33) + Workflows v1.0 (R36) for runtime flows). Key contracts: M04 BR-04-021/022 (NCR signals IN + ld_eligibility_flag write-back); M02 VO_APPROVED → BOQ materialisation; M03 EOT_GRANTED → BaselineExtension; M06 VO_APPROVED_COST_IMPACT + LD_ELIGIBLE_AMOUNT events. ENUMs: X8 v0.7 §3.73-§3.88 (carried forward in v0.8). |
| Correspondence register, notice tracker (50/80/100% SLA), meetings, minutes, action items, RFIs, transmittals, distribution lists, ProjectCorrespondenceConfig | `SystemAdmin/Modules/M13_CorrespondenceMeetingRegister_Spec_v1_0.md` (LOCKED R34; read with Brief v1.0 (R32) + Workflows v1.0 (R36) for runtime flows). Key contracts: M13→M05 (CORRESPONDENCE_M05_FLAGGED for VO/EOT/EWN claims); M13→M11 (ActionItem emit + 8 DQ trigger types); M12 stub (document_id FK). ENUMs: X8 v0.8 §3.89-§3.102. X9 v0.5 §13.3.13 role-default views. |
| ENUMs (any) | `SystemAdmin/Cross-link files/X8_GlossaryENUMs_v0_8.md` |
| Charts, visualisation, role-default views | `SystemAdmin/Cross-link files/X9_VisualisationStandards_Spec_v0_4.md` (content version v0.5 — in-place patched R34; filename retained per in-place patch convention) |
| Naming conventions | `System Specs/EPCC_NamingConvention_v1_0.md` |
| Folder structure | `System Specs/EPCC_FolderIndex_v1_0.md` |
| Audit findings | `System Specs/AUDIT_Round00_ExistingSpecs_v1_0.md` |
| Pilot data | KDMC reference appendices in M01 + M02 specs |
| Architectural standards (DB, deployment, DR, multi-tenancy) | `ZEPCC_Legacy/EPCC_Standards_Memory_v5_3.md` — **locked items only** (`ES-XX-XXX` codes with STATUS: CONFIRMED/LOCKED/CLOSED). Verify ES status before citing. **Note:** legacy SPECS in the same `ZEPCC_Legacy/` folder are deprecated; the Standards Memory entries are NOT — they govern architecture decisions not duplicated in `.claude/rules/`. Example: ES-DB-001 = schema-per-tenant (also referenced in `architecture.md` §Multi-Tenancy + CLAUDE.md §4) |

---

## Patch Notes — 2026-05-04 (Round 37 Pre-Build Audit)

- **H4** — X8 active version refs bumped v0.6 → v0.8 (L15 + canonical-source router row)
- **H5** — M05 + M13 canonical-source router entries added
- **H6** — M01 cascade list extended to v1.4 (v1_4 cascade note now referenced)
- **H7** — M03 cascade list extended to v1.3 (v1_3 cascade note now referenced)
- **H8** — M06 spec version corrected v1.0a → v1.0b; v1.1 cascade note now referenced
