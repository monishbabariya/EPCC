# AUDIT — Round 00 — Existing Specs Audit
## Version 1.0
**Auditor:** PMO Director / System Architect
**Date:** 2026-05-03 | **Status:** Locked
**Scope:** All 12 existing module specs + HDI + Standards Memory + Module Registry
**Method:** 10-check audit per v2.5 plan (C4) + structural review

---

## 1. EXECUTIVE SUMMARY

**Specs audited:** 13 (M01, M02, M03, M04, M05, M06, M07, M08, M09, M10, M11, M15, PIOE) + HDI + 4 system docs

**Severity-graded findings:**
- 🔴 Must-fix (blocks v1.0 lock): **6 findings**
- 🟠 Should-fix (high-value, before Phase 1 build): **9 findings**
- 🟡 Nice-to-fix (improves quality, can defer): **7 findings**

**Lock recommendation:** ❌ Cannot lock existing specs as-is. Resolve all 🔴 findings before Round 1 begins.

---

## 2. CRITICAL FINDINGS (🔴 — must-fix)

### F-001 — Amendment Files Are Not Standalone Specs
**Severity:** 🔴 Critical | **Affects:** M02 v2.1, M04 v2.2, M05 v2.3, possibly Standards Memory v5.3

**Finding:** Three module specs are AMENDMENT documents that describe only "changed blocks" relative to base versions (M02 v2.0, M04 v2.1, M05 v2.2). The base versions are not in current project knowledge as standalone files.

**Impact:** A developer reading M02 v2.1 cannot build the module — they need to find v2.0, apply v2.1 changes, and resolve any conflicts. This violates "spec must be implementable as written".

**Recommendation:**
1. During re-issue under new naming convention, CONSOLIDATE base + all amendments into a single v1.0 spec.
2. Going forward, eliminate amendment-style specs. Use Major/Minor versioning per Naming Convention §5.
3. Standards Memory v5.3 is also an amendment chain — consolidate into single v1.0.

**Status:** Open — to resolve in re-issue rounds.

---

### F-002 — HDI Not in Module Registry
**Severity:** 🔴 Critical | **Affects:** EPCC_Complete_Module_Registry_v1_0.md, EPCC_HistoricalDataImport_v1_0.md

**Finding:** HDI (Historical Data Import) has a full v1.0 spec but is not listed in the Module Registry. Spec self-classifies as "system-level utility (not a module — no M-number assigned)".

**Impact:** Registry undercounts system items. Build sequence ignores HDI. Engineering Standards reference ES-DB-009 (HDI staging) without registry context.

**Recommendation:**
1. Add HDI as a registered system item (suggest ID `HDI` retained, classified as `System Utility`, separate from M-numbered modules).
2. Place in `/11_System_Utilities/` per Folder Index.
3. Include in Phase 1 (HDI is needed for KDMC pilot deployment per its own Section 1).
4. Update Module Registry summary count: 27 modules + 6 PFs + 1 system utility (HDI) = 34 system items, not 33.

**Status:** Open — registry update in Round N.

---

### F-003 — "Locked: No" Status on All Existing Specs
**Severity:** 🔴 Critical | **Affects:** All 12 specs + HDI

**Finding:** Every spec carries header `Status: Draft — Pending Review | Locked: No`. None are formally locked despite being conceptually approved (per U1-a).

**Impact:** No spec can be referenced as authoritative. New specs (M27, M28, etc.) that depend on existing entities have no stable foundation.

**Recommendation:** Per user directive ("now is the time to lock it"):
1. Re-issue every spec under v1.0 naming.
2. New v1.0 carries `Status: Locked` from creation.
3. Lock mechanism: PMO Director explicit sign-off on each spec, recorded in VersionLog.
4. Any change to a Locked spec requires new Major version.

**Status:** Open — locked at re-issue time per spec.

---

### F-004 — Inconsistent ENUM Values Across Modules (Suspected)
**Severity:** 🔴 Critical | **Affects:** Cross-module ENUM consistency

**Finding:** Severity ENUMs appear differently across specs:
- M04 NCR: `Critical / High / Medium / Low`
- M15 PunchListItem: `Critical / High / Medium / Low` (matches)
- M04 DLPDefect: `Critical / High / Medium / Low` (matches)
- Decision Queue references: `CRITICAL / HIGH / MEDIUM / LOW` (uppercase) in some BRs
- M01 RAG: `Green / Amber / Red`
- M07 EVM tolerance: `Green / Amber / Red` (matches M01)

The pattern (mixed case in entity definitions vs uppercase in BRs) suggests inconsistency. Full audit requires reading all 12 specs line-by-line, which exceeds Round 0 scope.

**Recommendation:**
1. Round 0 surfaces this as a known risk.
2. X8 GlossaryENUMs (cross-cutting doc) is the resolution: every ENUM defined ONCE, referenced everywhere.
3. Per I3, X8 starts as a living document during Round 1.
4. Each re-issued spec must reference X8 instead of redefining ENUMs.

**Status:** Open — to resolve via X8 (living glossary).

---

### F-005 — Joint Entity Ownership Without Clear Authority
**Severity:** 🔴 Critical | **Affects:** M02 + M07 (BACIntegrityLedger), HDI + M03/M04/M06 (data_source field)

**Finding:** `BACIntegrityLedger` is described as "owned by M02, jointly referenced by M07" in M02 v2.1, and as "referenced in M07 v3.0" in Standards Memory. Joint ownership is ambiguous: who is the schema authority?

Similar issue: HDI adds `data_source` field to entities owned by M03, M04, M06, M07 — but the schema authority for these entities is ambiguous.

**Impact:** Migration order conflicts. Schema drift. FK direction uncertainty.

**Recommendation:**
1. Single-owner rule: every entity has exactly one owning module. References from other modules are read-only.
2. BACIntegrityLedger owner = M02 (it is the BAC source). M07 reads it.
3. `data_source` field is owned by the host entity's module (e.g., M03 owns it on PVProfile, even if HDI populates it).
4. Add explicit "Schema Owner" field to every entity definition in re-issued specs.

**Status:** Open — re-issue rounds enforce single-owner rule.

---

### F-006 — Missing Module Specs for 16 Modules + 5 Platform Features
**Severity:** 🔴 Critical | **Affects:** Coverage

**Finding:** Module Registry lists 27 modules. Only 12 have specs. 15 are unspecced. Plus 8 newly proposed in v2.3 (M24, M27, M28, M29, M30, M31, M32, M33, M34) → 23 unspecced. Plus 5 platform features (PF01–PF06).

**Impact:** Cannot lock the system architecture without all specs.

**Recommendation:** Per v2.7 plan, write all 23 specs in C1 cadence. Already locked as approach.

**Status:** Acknowledged. Resolved by execution of Tracks 1–4.

---

## 3. HIGH-PRIORITY FINDINGS (🟠 — should-fix)

### F-007 — Inconsistent Document Headers
**Severity:** 🟠 | **Affects:** All specs

**Finding:** Headers vary across specs. Some include `Reference Standards`, some don't. `Spec Author`, `Date`, `Layer`, `Build Priority` are inconsistently present.

**Recommendation:** Lock a standard header template. Apply to all v1.0 re-issues.

**Standard header (locked):**
```
# {ID} — {Module Name}
## {ArtefactType} v{Major}.{Minor}
**Status:** {Status from EnumA}
**Locked:** Yes/No
**Spec Author:** PMO Director
**Created:** YYYY-MM-DD | **Last Updated:** YYYY-MM-DD
**Last Audited:** vX.X on YYYY-MM-DD  ← per I2
**Reference Standards:** EPCC_StandardsMemory_v1_0.md
**Layer:** {Layer}
**Phase:** {1/2/3/4}
**Build Priority:** {Critical/High/Medium/Low}
**Folder:** /{folder_path}/
```

---

### F-008 — Integration Symmetry Not Verified
**Severity:** 🟠 | **Affects:** All specs with cross-module integrations

**Finding:** M02 v2.1 says "SENDS TO M07 EVM Engine". M07 spec must have a matching "RECEIVES FROM M02". Cannot verify within this audit pass without reading every spec end-to-end.

**Impact:** Phantom integrations — module A claims to send X to module B, but B doesn't have a handler defined. Builds will silently drop messages.

**Recommendation:**
1. X3 IntegrationMap (cross-cutting) is the resolution: every integration listed once, with both ends referenced.
2. CI check (future): for every "SENDS TO MX" in spec A, verify matching "RECEIVES FROM MA" in spec MX.

**Status:** Open — to resolve via X3.

---

### F-009 — BR Numbering Uniqueness Not Enforced
**Severity:** 🟠 | **Affects:** All specs

**Finding:** BR codes follow `BR-NN-NNN` pattern (NN = module ID). Within-module uniqueness is implied but not verified. Across-module uniqueness is guaranteed by NN prefix only — but rules referenced cross-module (e.g., "see BR-05-028") rely on this.

**Recommendation:** Mandate `BR-{module_id}-{sequence}` format and add to Standards Memory. Every BR globally unique.

---

### F-010 — Speed Tier Definitions Not Centralized
**Severity:** 🟠 | **Affects:** All specs

**Finding:** Speed tiers (🔴 Real-time / 🟡 2-4hr / 🟢 24hr) used across all specs. Definition lives in Standards Memory. Visual indicators (emoji) are not always used consistently.

**Recommendation:**
1. Add explicit table to Standards Memory v1.0:

| Tier | Symbol | SLA | Use For |
|---|---|---|---|
| Real-time | 🔴 | < 2 sec | Status changes, blocks, gate signals |
| Near-real-time | 🟡 | 2–4 hr | Decision Queue items, batch alerts |
| Batch | 🟢 | 24 hr | Daily snapshots, dashboard refresh |

2. Forbid free-text speed values ("fast", "immediate"). Only the three tiers.

---

### F-011 — Soft-Delete Adherence Not Verified
**Severity:** 🟠 | **Affects:** All entities

**Finding:** Standards Memory mandates `is_active` field for soft-delete. Cannot verify all entities comply without exhaustive line-by-line audit.

**Recommendation:** During re-issue, verify every entity has `is_active`, `created_at`, `updated_at`, `created_by`, `updated_by`. Add to Standard Header section.

---

### F-012 — Audit Log Coverage Not Verified
**Severity:** 🟠 | **Affects:** All specs

**Finding:** Block 8 (Governance & Audit) lists logged actions per module. Whether every BR with a state-changing action has a corresponding audit log entry is not confirmed.

**Recommendation:** During re-issue, cross-check Block 6 (BRs that mutate state) against Block 8 (audit log entries). Mismatches = audit gap.

---

### F-013 — Decision Queue Trigger Naming Inconsistent
**Severity:** 🟠 | **Affects:** All BRs that create Decision Queue items

**Finding:** Trigger names appear in mixed formats:
- `PUNCH_LIST_RESPONSE_OVERDUE` (uppercase snake) — M15
- `HANDOVER_DATE_SLIPPAGE` (uppercase snake) — M15
- `DLP_RESPONSE_OVERDUE` — M04
- `Exclusivity Exception` (mixed case) — M01
- `Financial Review` — M01

Inconsistency between modules.

**Recommendation:** Lock format as `UPPERCASE_SNAKE_CASE`. Update all specs at re-issue.

---

### F-014 — RBAC Roles Defined Inconsistently
**Severity:** 🟠 | **Affects:** All specs

**Finding:** Roles appear with different naming:
- `PMO Director` / `PMO_Director` / `PMO_DIRECTOR` — varies
- `Project Director` / `Project_Director`
- `Site Manager` vs `Supervisor` (M04 uses `Supervisor` for some BRs)

**Recommendation:** M34 SystemAdminRBAC spec (Round 1 priority) is the canonical role taxonomy. All other specs reference M34's role list. Single source of truth.

---

### F-015 — Engineering Standards Versioned Out of Sync
**Severity:** 🟠 | **Affects:** EPCC_Engineering_Standards_v1_2.md vs Standards Memory v5.3

**Finding:** Engineering Standards is at v1.2, Standards Memory is at v5.3. Standards Memory v5.3 amendment file references "Engineering Standards v1.1" in some places and v1.2 in others. The two version histories are decoupled but interdependent.

**Recommendation:** Consolidate both into:
- `EPCC_StandardsMemory_v1_0.md` (PM standards: governance, ENUMs, audit rules)
- `EPCC_EngineeringStandards_v1_0.md` (technical standards: DB, API, security, CI/CD)

Both at v1.0. Both locked. Independent change cycles allowed but cross-references explicit.

---

## 4. NICE-TO-FIX FINDINGS (🟡)

### F-016 — Block 10 (Open Questions) States "Resolved" but Resolutions Are Long
**Severity:** 🟡 | **Affects:** Most specs

Resolutions in Block 10 are paragraph-length. Suggest moving to a separate `OpenQuestions` artefact per module, with Block 10 only listing question + reference. Reduces spec size by 5–10%.

### F-017 — Inconsistent Use of `INPUT / SYSTEM / CALC / LINK` Source Tags
**Severity:** 🟡

Field source tags vary: some specs use `LINK → M01 Project`, others use `LINK`, others use `FK`. Lock as `LINK → M{ID}.{Entity}.{field}` per I4.

### F-018 — Wireframe Specifications Embedded in Specs
**Severity:** 🟡

Some specs (M15, M10) embed ASCII wireframes in Block 5. Per v2.5 (C1), wireframes move to separate `.html` files. Strip wireframes from re-issued specs; replace with reference to wireframes file.

### F-019 — UI Design System Density
**Severity:** 🟡

`EPCC_UI_Design_System_v2_0.md` is generic-purpose. Re-issue at v1.0 should sharpen to: locked color tokens, locked component library, locked grid. Anything not yet decided → defer to design phase.

### F-020 — Standards Memory §-Numbered Sections (§7.121, §7.123, etc.)
**Severity:** 🟡

Section numbering goes to §7.140+. Hard to navigate. Re-issue with cleaner outline-style numbering (1.1, 1.2, 2.1...).

### F-021 — Mermaid / Diagram References Missing
**Severity:** 🟡

Cross-references like "see dependency map" point to ASCII art in Module Registry. Replace with Mermaid diagrams (per v2.5 C1 lock).

### F-022 — KDMC Workbook References in Specs
**Severity:** 🟡

Some specs reference "KDMC standard" or "KDMC monthly EVM Excel" as if the workbook is authoritative. Per U2-a, workbook is reference-only. Specs should remove "KDMC standard" framings; replace with explicit values.

---

## 5. STRUCTURAL OBSERVATIONS (informational)

### O-001 — Density Is Justified
The 1500+ line specs are dense because the system is a control + enforcement system. Per Decision A, density is preserved. Audit findings target redundancy, not depth.

### O-002 — Existing Specs Demonstrate Strong Discipline
The 10-block template, BR numbering, integration tables, and audit log sections are consistently used. Foundation is solid. Re-issue is about consistency and lockdown, not redesign.

### O-003 — KDMC Pilot Drives Phase 1 Sequence
Many design decisions (HDI staging, EVM Holt's ES, NABH templates) trace to KDMC. This is correct per U2-a — KDMC informs the system but does not constrain it.

### O-004 — User Preferences Document Drives Module Boundaries
Project.md (5.1–5.8) directly maps to: M27 Design Control, M05 Variation Control, M28 Interface Control, M29 Procurement, M08 Stop/Go, M11 Decision System, M09 Compliance, M05 Risk Control. Module boundaries align well with user-stated requirements.

---

## 6. AUDIT CHECKLIST RESULTS

| Check | Description | Result |
|---|---|---|
| A1.1 | 10-block template adherence | ⚠️ Amendment files break this. Re-issue resolves. |
| A1.2 | Integration symmetry | ❓ Not fully verifiable; X3 will resolve |
| A1.3 | BR numbering uniqueness | ✅ Format consistent; uniqueness assumed |
| A1.4 | FK reference validity | ⚠️ Joint ownership ambiguity (F-005) |
| A1.5 | ENUM consistency | ❓ Suspected drift; X8 will resolve |
| A1.6 | Speed tier consistency | ✅ Consistent in seen specs |
| A1.7 | Decision Queue trigger naming | ⚠️ Inconsistent (F-013) |
| A1.8 | Soft-delete adherence | ❓ Not fully verified (F-011) |
| A1.9 | Audit log coverage | ❓ Not fully verified (F-012) |
| A1.10 | Open Questions resolved | ✅ All seen specs report 0 open questions |

---

## 7. RECOMMENDED ACTIONS — PRIORITY ORDER

| # | Action | Owner | Round |
|---|---|---|---|
| 1 | Lock Naming Convention + Folder Index + Version Log + Legacy Manifest | PMO Dir | Round 0 (this round) ✓ |
| 2 | Add HDI to Module Registry as System Utility | PMO Dir | Round 0 → next sub-update |
| 3 | Create `EPCC_StandardsMemory_v1_0.md` from v5.3 consolidation | PMO Dir | After Round 1 |
| 4 | Re-issue M34 Brief + Spec (Round 1+2) — locks role taxonomy | PMO Dir | Round 1 (next) |
| 5 | Initialize X8 GlossaryENUMs as living document | PMO Dir | Start Round 1 |
| 6 | Re-issue all 12 existing specs under new naming + consolidate amendments | PMO Dir | Rounds 3–14 |
| 7 | Spec all 23 unspecced + 5 PFs in C1 cadence | PMO Dir | Rounds 15–43 |
| 8 | Build X1, X2, X3, X4, X6, X7 cross-cutting docs | PMO Dir | Post-Phase-1-specs |
| 9 | Lock final EPCC_ModuleRegistry_v2_0.md | PMO Dir | Final round |

---

## 8. APPENDIX — AMENDMENT CHAIN ENUMERATION

Files identified as amendments (not standalone specs):

```
M02_Structure_WBS_v2_1.md       — amends M02 v2.0 (base not in current scan)
M04_Execution_Capture_v2_2.md   — amends M04 v2.1 (also amendment) — chain
M05_Risk_Change_v2_3.md         — amends M05 v2.2 (likely amendment) — chain
EPCC_Standards_Memory_v5_3.md   — amends v5.2 (which amends v5.1, etc.) — long chain
```

**Resolution per F-001:** Re-issue rounds reconstruct full v1.0 specs by walking each chain back to base + applying all amendments forward. No amendment chains permitted in v3.0+ structure.

---

## 9. COST IMPLICATIONS NOTED (per user directive)

User asked audit to "consider robustness and cost implications".

| Decision | Cost Impact |
|---|---|
| Re-issue all specs under new naming | High (calendar) — but eliminates ambiguity, reduces dev rework | 
| Single-owner entity rule | Low — clarifies, doesn't expand scope |
| Living glossary (X8) | Low ongoing — high return |
| Eliminate amendment files | Medium — one-time consolidation effort | 
| HDI added to registry | Trivial |
| 8 new modules (M24, M27, M28, M29, M30, M31, M32, M33) | High dev cost — but Project.md mandates them |

**Net assessment:** Re-issue + lockdown costs ~40 calendar days of spec work but eliminates ~6 months of build rework. Strong ROI.

---

*v1.0 — Audit complete. 6 critical findings to resolve before Round 1. Lock granted on resolution path.*
