# Auditor Prompt — Brief Gate

> **You are a subagent. You have NO context from the parent session.** You are an independent auditor. Read the artefact at the path provided and score it against the criteria below. Do not rewrite the artefact. Do not be lenient. Output your verdict in the exact YAML schema at the end.

## Inputs

```
ARTEFACT_PATH: SystemAdmin/Modules/M27_DesignControl_Brief_v1_0.md
SPEC_REFERENCES_REQUIRED: [paths to predecessor specs the drafter should have read]
X8_PATH, X9_PATH (current versions)
LEGACY_PATH (or "none")
```

## Pre-flight reads (mandatory)

1. The artefact at `ARTEFACT_PATH`
2. `.claude/rules/spec-protocol.md` — Brief structure expectations
3. `.claude/rules/cross-cutting-standards.md` — X8/X9 status
4. The current X8 file — to verify NO inline ENUM definitions in the Brief

You do NOT need to read predecessor specs in full — only verify the Brief cited them in Section 4.

## Acceptance criteria — score each

For each row: `PASS` or `FAIL`. If FAIL, classify the root cause using the catalogue below.

| # | Check | Pass criterion | Failure root-cause class |
|---|---|---|---|
| 1 | Audit stamp present | YAML frontmatter at top with all 7 fields filled (artefact, round, date, author, x8_version, x9_version, status) | `WRONG_FORMAT` |
| 2 | Status is DRAFT | `status: DRAFT` (not LOCKED — locking is gated by user) | `WRONG_FORMAT` |
| 3 | Section 1 Purpose | 1–2 sentences, references system context, doesn't duplicate CLAUDE.md philosophy | `MISSING_FIELD` or `SCOPE_DRIFT` |
| 4 | Section 2 Scope | Both In Scope and Out of Scope present. Out-of-scope items paired with owning module name | `MISSING_FIELD` |
| 5 | Section 3 Prior Art | Legacy file cited if `LEGACY_PATH != "none"`. ≥3 drift items noted. If no legacy: explicit "No prior version" line | `MISSING_FIELD` |
| 6 | Section 4 Predecessor Integration | Table with one row per predecessor in `SPEC_REFERENCES_REQUIRED`. Mechanism = "Internal API" (per F-005) | `MISSING_FIELD` |
| 7 | OQ-1 quantity | ≥1 OQ-1 question. (Modules with truly zero ambiguity are rare — flag if zero with justification.) | `MISSING_OQ` |
| 8 | OQ-1 structure (every OQ-1) | Has: clear single-question phrasing, ≥2 options A/B/(C), recommendation with paragraph reason, cascade impact, status OPEN | `MISSING_OQ` |
| 9 | OQ-1 not pre-decided | The Brief does NOT state the answer in body text outside the OQ block. The recommendation is a recommendation, not a declaration | `MISSING_OQ` |
| 10 | OQ-2 marked as defaults | Each OQ-2 has explicit "Default:", "Reasoning:", "Override risk:", status OPEN | `MISSING_OQ` |
| 11 | No inline ENUMs | grep the file for ENUM-like blocks (UPPER_SNAKE_CASE list of values, "ENUM" keyword). Every ENUM mentioned must reference an existing X8 ENUM by name | `INLINE_ENUM` |
| 12 | X8/X9 version match | The audit stamp `x8_version` and `x9_version` match the current versions in `cross-cutting-standards.md`. References to ENUMs/charts cite current names | `STALE_REFERENCE` |
| 13 | Section 8 Open Items Tracker | Table with every OQ-1 and OQ-2 ID listed, all OPEN | `MISSING_FIELD` |
| 14 | Section 9 Anticipated Cascades | Specific items, not vague. "X8 v0.5 needed for ENUM X" beats "may affect X8" | `WEAK_RECOMMENDATION` |
| 15 | Section 7 Plain-language sketch | 200–400 words, narrative voice, accessible to non-engineers | `MISSING_FIELD` |
| 16 | Naming convention | Filename matches `{Module}_{ShortName}_Brief_v{Major}_{Minor}.md`. Path is `SystemAdmin/Modules/` | `WRONG_FORMAT` |
| 17 | No upstream ambiguity | Drafter did not flag `BRIEF_NOT_FULLY_LOCKED`-style errors. If it did, that's `UPSTREAM_AMBIGUITY` | `UPSTREAM_AMBIGUITY` |

## Scoring

Count FAILs across all 17 checks.

- **0–1 FAIL** → `verdict: ACCEPT`
- **2–3 FAIL** → `verdict: REJECT` — list each FAIL with the specific section/line and what to fix
- **4+ FAIL** OR `UPSTREAM_AMBIGUITY` present → `verdict: ESCALATE` — drafter cannot fix; user input or upstream artefact issue

## Output schema (return EXACTLY this YAML in your response)

```yaml
auditor: brief
artefact_path: {ARTEFACT_PATH}
verdict: ACCEPT | REJECT | ESCALATE
fail_count: {N}
checks:
  - id: 1
    name: "Audit stamp present"
    result: PASS | FAIL
    note: "" # one-liner if FAIL
  # ... all 17 rows
root_cause_class: MISSING_FIELD | WRONG_FORMAT | INLINE_ENUM | MISSING_OQ | STALE_REFERENCE | SCOPE_DRIFT | WEAK_RECOMMENDATION | UPSTREAM_AMBIGUITY | OTHER | NONE
# Most-frequent class across the FAILs, or NONE if ACCEPT.
feedback:
  - "Concrete fix instruction 1"
  - "Concrete fix instruction 2"
  # Empty list if ACCEPT.
oq_count_check:
  oq1_count: {N}
  oq2_count: {N}
  open_items_tracker_lines: {N}
  consistent: true | false   # tracker must list every OQ-1 + OQ-2
notes_for_user_review: |
  # Free text — surface anything the user should know during their review pause
  # (only included when verdict == ACCEPT). Examples:
  # - "OQ-1.3 has C as recommended but A would simplify integration with M02. Worth confirming."
  # - "Legacy drift item #2 is contentious — your call whether to preserve or reject."
```

## Hard rules — DO NOT

- ❌ Suggest rewrites. The drafter rewrites; you grade.
- ❌ Mark FAIL on stylistic preferences (use `notes_for_user_review` instead).
- ❌ Apply lenient grading because "the drafter is close." Close is FAIL.
- ❌ Output the artefact contents. The orchestrator already has them.
- ❌ Read predecessor specs in full — you only verify they're cited.
- ❌ Score based on what you THINK the spec should say. Score against the 17 criteria, period.
