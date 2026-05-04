# M03 — Planning & Milestones
## v1.3 Cascade Note
**Status:** Cascade Patch
**Type:** Role canonicalisation (column labels) + role row addition (ANALYST + EXTERNAL_AUDITOR) to Block 4a permission matrix
**Author:** Monish (with Claude assist)
**Created:** 2026-05-04
**Trigger:** Round 29 audit findings M25 (RBAC matrix omits ANALYST + EXTERNAL_AUDITOR — same defect class as M01 H14/H16, re-tiered HIGH for symmetry) + D4b (11 existing column labels are truncated; symmetric treatment with M01 H16)
**Parent Spec:** M03_PlanningMilestones_Spec_v1_1.md (in-place patched to v1.1a in Round 29 — see `M03_PlanningMilestones_v1_2_CascadeNote.md` for v1.2 cascade and the v1.1 → v1.1a patch context)
**Reference Standards:** X8_GlossaryENUMs_v0_6.md (v0.6a), X9_VisualisationStandards_Spec_v0_4.md, M34_SystemAdminRBAC_Spec_v1_0.md (Block 3 — canonical 17-role taxonomy), .claude/rules/cross-cutting-standards.md (§17 Canonical Roles), M01_ProjectRegistry_v1_4_CascadeNote.md (parallel H16 fix on M01 Block 4a)
**Folder:** SystemAdmin/Modules/

---

## CHANGE LOG

| Version | Date | Change Summary |
|---|---|---|
| v1.0 | 2026-05-03 | Initial standalone consolidated spec (Round 16). 12 entities, ~32 BRs. ResourceType extended to 4 values. reporting_period_type ownership shifted to M03. Procurement vendor identity owned by M06. Float visibility role-tiered. |
| v1.1 | 2026-05-03 | Round 18 cascade — Appendix C audit-events catalogue (28 events) + BR-03-033 + BR-03-034. Full re-issue (substantive change). |
| v1.1a | 2026-05-04 | Round 29 in-place patch — added forward-pointer to v1.2 cascade note. See `M03_PlanningMilestones_Spec_v1_1.md` CHANGE LOG. |
| v1.2 | 2026-05-04 | Round 28 — `MILESTONE_ACHIEVED_FINANCIAL` audit event added + BR-03-035 + Block 7 SENDS TO M06. See `M03_PlanningMilestones_v1_2_CascadeNote.md`. |
| **v1.3** | **2026-05-04** | **Round 29: M25 — ANALYST + EXTERNAL_AUDITOR columns added to Block 4a matrix (mirroring READ_ONLY). D4b — 10 truncated column labels canonicalised (`SYS_ADMIN` → `SYSTEM_ADMIN`, etc.). No row permissions changed. No BR change. No entity change.** |

---

## NATURE OF v1.3 CHANGE

Two non-substantive fixes bundled into one cascade note. Both are role-name / role-coverage propagation; neither alters any locked permission, BR, entity, or field.

Per spec-protocol §Cascade-vs-Re-issue: cascade-note vehicle is correct (not re-issue) — 0 fields added/removed, 0 BRs changed, 0 entity changes, scope unchanged.

---

## M25 — Block 4a Matrix: ANALYST + EXTERNAL_AUDITOR Columns Added

M03 Spec v1.1 Block 4a permission matrix (line 446-468) covers 11 role columns and 19 action rows. The matrix omits two canonical roles from the M34 17-role taxonomy: `ANALYST` and `EXTERNAL_AUDITOR`. Both were added to the canonical list in the R18 audit but were never propagated to M03 Block 4a.

### Resolution

Per Round 29 user direction (2026-05-04): both new columns mirror the `READ_ONLY` column values verbatim across all 19 actions. No existing column values change.

### Extended Matrix — New Columns (apply to right of existing `READ_ONLY` column)

| # | Action | ANALYST | EXTERNAL_AUDITOR | Notes |
|---|---|---|---|---|
| 1 | Create/edit schedule (pre-baseline) | ❌ | ❌ | Mirrors READ_ONLY |
| 2 | Edit schedule (post-baseline) | ❌ | ❌ | Mirrors READ_ONLY |
| 3 | Lock baseline | ❌ | ❌ | Mirrors READ_ONLY |
| 4 | Submit baseline extension | ❌ | ❌ | Mirrors READ_ONLY |
| 5 | Approve baseline extension | ❌ | ❌ | Mirrors READ_ONLY |
| 6 | Override billable/vendor flags | ❌ | ❌ | Mirrors READ_ONLY |
| 7 | Create/edit milestones | ❌ | ❌ | Mirrors READ_ONLY |
| 8 | Update milestone forecast | ❌ | ❌ | Mirrors READ_ONLY |
| 9 | Configure loading profiles | ❌ | ❌ | Mirrors READ_ONLY |
| 10 | Override PV period | ❌ | ❌ | Mirrors READ_ONLY |
| 11 | Allocate resources (role) | ❌ | ❌ | Mirrors READ_ONLY |
| 12 | Assign named resource | ❌ | ❌ | Mirrors READ_ONLY |
| 13 | Manage ResourceMaster | ❌ | ❌ | Mirrors READ_ONLY |
| 14 | Create/edit procurement schedule | ❌ | ❌ | Mirrors READ_ONLY |
| 15 | Configure weather windows | ❌ | ❌ | Mirrors READ_ONLY |
| 16 | Configure look-ahead window | ❌ | ❌ | Mirrors READ_ONLY |
| 17 | Schedule import | ❌ | ❌ | Mirrors READ_ONLY |
| 18 | **View float values** | ❌ (status only) | ❌ (status only) | Mirrors READ_ONLY. **Informational note (EXTERNAL_AUDITOR):** an external audit role typically expects full numeric visibility for audit-trail purposes; the conservative `❌ (status only)` posture matches the principle that float-value disclosure is governed by BR-03-031 (OQ-1.10 lock) and applies uniformly to non-editing roles. Revisit when external-portal RBAC is specced under PF03 ExternalPartyPortal (Phase 2). |
| 19 | View all schedule | ✅ (all) | ✅ (all) | **Modulation from READ_ONLY:** READ_ONLY = `✅ (own)` is project-ownership-scoped, but neither ANALYST nor EXTERNAL_AUDITOR has a project-ownership relationship in M01 — both are organisationally / tenant-scoped read roles. Therefore both are `✅ (all)` within the tenant. **Informational note:** EXTERNAL_AUDITOR cross-tenant access is gated by PF03 ExternalPartyPortal (Phase 2); in Phase 1 this is in-tenant only. |

### Float Visibility Annotation (BR-03-031)

The Block 4a footer note "All editing roles see float values; READ_ONLY sees only schedule status badges (no float numerics)" is preserved verbatim. ANALYST and EXTERNAL_AUDITOR fall under the same float-redaction posture as READ_ONLY for action #18.

---

## D4b — Column Label Canonicalisation (Symmetric with M01 v1.4 H16)

M03 Spec v1.1 Block 4a uses **truncated** column labels that do not match the canonical UPPER_SNAKE_CASE 17-role taxonomy (M34 Spec Block 3). Same defect class as M01 H16 — addressed in this cascade note for symmetric treatment in one Round 29 pass.

### Substitution Table — Apply When Reading Block 4a

| Block 4a label (line 448) | Canonical name (M34 Block 3) |
|---|---|
| `SYS_ADMIN` | `SYSTEM_ADMIN` |
| `PMO_DIR` | `PMO_DIRECTOR` |
| `PORTFOLIO` | `PORTFOLIO_MANAGER` |
| `PROJ_DIR` | `PROJECT_DIRECTOR` |
| `PLAN_ENG` | `PLANNING_ENGINEER` |
| `QS_MGR` | `QS_MANAGER` |
| `FIN_LEAD` | `FINANCE_LEAD` |
| `PROC` | `PROCUREMENT_OFFICER` |
| `SITE_MGR` | `SITE_MANAGER` |
| `COMP_MGR` | `COMPLIANCE_MANAGER` |
| `READ_ONLY` | `READ_ONLY` _(already canonical — listed for completeness)_ |

**No permission values changed** under any column. Labels only.

**Why now:** symmetric with the M01 H16 fix landing in `M01_ProjectRegistry_v1_4_CascadeNote.md` this same round. M02 Block 5 rate-display matrix already uses canonical names (no canonicalisation needed there). Treating M01 + M03 in the same Round 29 pass closes the cluster.

---

## DOWNSTREAM IMPACT

- **No M01/M02/M04/M06 cascade required.** Other modules don't redefine M03's permission matrix.
- **PF03 ExternalPartyPortal (Phase 2)** — when specced, will need to revisit EXTERNAL_AUDITOR cross-tenant access posture. Note in informational annotations above.
- **No code impact** (Phase 1 spec-only; no implementation yet).
- **VersionLog §3.5 M03 row** should reference v1.1a + v1.2 + v1.3 cascade-note chain when the medium-cleanup branch lands (deferred to `audit/round-29-medium-cleanup`).

---

*Cascade note v1.3 — LOCKED 2026-05-04 — Round 29 audit. No re-issue required (per spec-protocol.md §Cascade-vs-Re-issue: 0 fields added, 0 BRs changed, scope unchanged — column additions + label canonicalisation only).*
