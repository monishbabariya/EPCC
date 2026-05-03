# Re-Entry Protocol for New Sessions

> **Purpose:** What Claude does at the start of every new session (compaction, fresh chat, context reset). Locked sequence.

---

## Read Order

When a new session starts, Claude must read these in order before doing anything else:

1. **`CLAUDE.md`** (project root) — project identity, current round status, locked decisions table
2. **`.claude/rules/spec-protocol.md`** — cadence, 10-block template, audit stamps
3. **`.claude/rules/cross-cutting-standards.md`** — current X8 + X9 versions, role mappings
4. **Most recent Round folder's deliverables** (check Section 9 of `CLAUDE.md` to find which round)
5. **The active X8 file** at the version listed in `cross-cutting-standards.md` (currently `SystemAdmin/Cross-link files/X8_GlossaryENUMs_v0_4.md`)
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
| Project lifecycle, phase, status, contract structure | `SystemAdmin/Modules/M01_ProjectRegistry_Spec_v1_0.md` (read with `M01_ProjectRegistry_v1_1_CascadeNote.md` adding `min_wbs_depth` and `M01_ProjectRegistry_v1_2_CascadeNote.md` removing `reporting_period_type`) |
| WBS, BOQ, packages, BAC, templates, units | `SystemAdmin/Modules/M02_StructureWBS_Spec_v1_0.md` |
| Schedule, baseline, milestones, PV, procurement timing, audit events | `SystemAdmin/Modules/M03_PlanningMilestones_Spec_v1_1.md` |
| Progress capture, NCRs, material receipts, contractor scoring, ProjectExecutionConfig | `SystemAdmin/Modules/M04_ExecutionCapture_Spec_v1_0.md` (read with Brief v1.0 as decision-history reference + Workflows v1.0 for runtime flows) |
| ENUMs (any) | `SystemAdmin/Cross-link files/X8_GlossaryENUMs_v0_4.md` |
| Charts, visualisation, role-default views | `SystemAdmin/Cross-link files/X9_VisualisationStandards_Spec_v0_2.md` |
| Naming conventions | `System Specs/EPCC_NamingConvention_v1_0.md` |
| Folder structure | `System Specs/EPCC_FolderIndex_v1_0.md` |
| Audit findings | `System Specs/AUDIT_Round00_ExistingSpecs_v1_0.md` |
| Pilot data | KDMC reference appendices in M01 + M02 specs |
