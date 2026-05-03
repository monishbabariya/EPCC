# EPCC — Naming Convention
## Version 1.0
**Owner:** PMO Director / System Architect
**Created:** 2026-05-03 | **Status:** Locked
**Supersedes:** All prior ad-hoc filenames

---

## 1. PURPOSE

Lock a single, deterministic naming rule for every artefact. Prevents drift, enables sort-order discovery, and supports machine-readable governance across 80+ files.

---

## 2. FORMAT

```
{Prefix}_{ShortName}_{ArtefactType}_v{Major}_{Minor}.{ext}
```

| Component | Rule |
|---|---|
| `Prefix` | Module ID (`M01`, `M27`, `PF01`, `PIOE`, `HDI`) **OR** cross-cutting tag (`X1`, `EPCC`, `AUDIT`) |
| `ShortName` | CamelCase, no spaces, no underscores within name. Max 30 chars |
| `ArtefactType` | One of: `Brief / Spec / Wireframes / Workflows / Audit / Index / Manifest / Standards / Registry / Log` |
| `vMajor_Minor` | `v1_0`, `v1_1`, `v2_0` — Major = breaking, Minor = additive |
| `ext` | `.md` (specs/briefs/workflows/cross-cutting), `.html` (wireframes), `.csv` (data exports) |

---

## 3. EXAMPLES

```
M01_ProjectRegistry_Brief_v1_0.md
M01_ProjectRegistry_Spec_v1_0.md
M01_ProjectRegistry_Wireframes_v1_0.html
M01_ProjectRegistry_Workflows_v1_0.md

M27_DesignControl_Brief_v1_0.md
PF01_MobileFieldPlatform_Spec_v1_0.md
HDI_HistoricalDataImport_Spec_v1_0.md

X1_RBACMatrix_v1_0.md
X2_DataDictionary_v1_0.md

EPCC_StandardsMemory_v1_0.md
EPCC_ModuleRegistry_v1_0.md
EPCC_VersionLog_v1_0.md
EPCC_NamingConvention_v1_0.md
EPCC_FolderIndex_v1_0.md

AUDIT_Round00_ExistingSpecs_v1_0.md
AUDIT_Round05_M27Brief_v1_0.md
```

---

## 4. RULES

| Rule | Statement |
|---|---|
| **R1** | Every artefact starts at `v1_0` in this restart. Legacy `v2.x` files are archived, not renumbered. |
| **R2** | Major version (`v2_0`) = breaking change to entities, integration points, or business rules. Triggers full audit re-run. |
| **R3** | Minor version (`v1_1`) = additive change (new field, new BR, new ENUM value). No audit re-run unless flagged. |
| **R4** | Filename is the canonical reference. Internal "Document Title" must match filename exactly. |
| **R5** | No spaces, no parentheses, no special chars except `_`. ASCII only. |
| **R6** | Date stamps live in version log, not filename. |
| **R7** | Per-file change logs eliminated (per I1). Master `EPCC_VersionLog_v1_0.md` is the only change log. |

---

## 5. VERSION INCREMENT TRIGGERS

| Trigger | Increment |
|---|---|
| New entity added | Minor |
| New field added (nullable) | Minor |
| New business rule added | Minor |
| New ENUM value added | Minor |
| Entity removed or renamed | Major |
| Field made required | Major |
| FK destination changed | Major |
| Business rule logic changed | Major |
| Integration speed tier changed | Major |
| Block 9 exclusions changed | Major |

---

## 6. ARCHIVAL RULE

Old version files are NOT deleted. Renamed:

```
{original}_ARCHIVED_supersededBy_{new_version}.md
```

Example:
```
M01_ProjectRegistry_Spec_v1_0_ARCHIVED_supersededBy_v1_1.md
```

Archived files move to `/00_Governance/Archive/`. Never deleted. Never modified.

---

## 7. ENFORCEMENT

| Layer | Mechanism |
|---|---|
| Author | This file is the source of truth. Every new file must conform before being added to VersionLog. |
| Review | First check during any audit: filename adherence. |
| CI (future) | When repo exists, GitHub Action validates every PR adds files matching this regex. |

**Filename regex (for future CI):**
```
^(M\d{2}|PF\d{2}|PIOE|HDI|X\d+|EPCC|AUDIT)_[A-Za-z][A-Za-z0-9]{0,29}_(Brief|Spec|Wireframes|Workflows|Audit|Index|Manifest|Standards|Registry|Log)_v\d+_\d+\.(md|html|csv)$
```

---

*v1.0 — locked. Any change requires PMO Director approval and triggers update to VersionLog.*
