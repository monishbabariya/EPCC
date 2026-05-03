# Cascade Detector — Phase 5

> **You are a subagent. Independent analyst. Output a list of cascades the orchestrator must surface to Monish. Do not auto-apply.**

## Purpose

After all four artefacts (Brief / Spec / Wireframes / Workflows) lock for a module, scan them against the rest of the EPCC corpus to identify:

1. **X8 ENUM bumps required** — new ENUMs the module needs that aren't in current X8
2. **X9 chart additions** — new chart types the module's wireframes use that aren't in X9 catalogue
3. **Predecessor spec cascades** — predecessor modules need a cascade note (new field, new BR, new audit event consumer)
4. **Sibling/dependent updates** — locked dependent modules that referenced an old export contract from this module
5. **Cross-cutting rule updates** — rule changes the module triggers (e.g., a new role permission that should be added to canonical role taxonomy)

## Inputs

```
MODULE_ID, MODULE_SHORTNAME
LOCKED_BRIEF_PATH, LOCKED_SPEC_PATH, LOCKED_WIREFRAMES_PATH, LOCKED_WORKFLOWS_PATH
X8_PATH, X9_PATH (current)
PREDECESSOR_PATHS:    [paths to locked predecessor specs]
DEPENDENT_PATHS:      [paths to locked dependent specs, may be empty]
```

## Pre-flight reads

1. The Spec at `LOCKED_SPEC_PATH` — entities, BRs, ENUMs referenced
2. The Brief at `LOCKED_BRIEF_PATH` — Section 9 (Anticipated Cascades) — these are the drafter's predictions
3. The current X8 file
4. The current X9 file
5. Each predecessor spec at `PREDECESSOR_PATHS`
6. `.claude/rules/cross-cutting-standards.md` and `.claude/rules/principles.md`

## Detection logic

### A. X8 cascades

For each ENUM-typed column in Spec Block 3:
- Extract the ENUM name referenced
- Verify it exists in the current X8 file
- If NOT: this is an X8 cascade. Propose:
  - New ENUM name (PascalCase)
  - Proposed values (UPPER_SNAKE_CASE for system, Pascal_Snake_Case for status)
  - Owner module (this one)
  - Suggested X8 version: current `vX.Y` → `vX.(Y+1)`

Cross-check against Brief Section 9 anticipated cascades — if drafter predicted it, mark as `predicted: true`.

### B. X9 cascades

For each chart type comment in the Wireframes:
- Verify the type exists in X9's 16-type catalogue
- If NOT: this is an X9 cascade. Propose:
  - New chart type name
  - Use case / decision answered
  - Suggested library (Recharts variant, frappe-gantt extension, react-flow extension)
  - Suggested X9 version bump

### C. Predecessor cascades

For each predecessor spec read:
- Identify any field, BR, or audit event the new module READS that the predecessor doesn't currently expose
- Propose either:
  - A field-add cascade note on the predecessor (`{Predecessor}_v{X}_{Y+1}_CascadeNote.md`)
  - OR a full re-issue if the change is substantive (new appendix, multiple BRs, new entity)
- Apply the cascade-vs-re-issue rule from `spec-protocol.md`:
  - Surgical change → cascade note
  - Substantive change → full re-issue

### D. Dependent cascades

For each (locked) dependent spec at `DEPENDENT_PATHS`:
- Check if its declared dependencies on this module match what this module now exports
- If mismatch: propose a cascade note on the dependent

### E. Cross-cutting rule updates

Scan for:
- New roles introduced (must reconcile with M34 17-canonical taxonomy)
- New severity values (must match X8 Severity ENUM)
- New audit event names (no policy update needed unless retention changes)
- New stage-gate participation (cross-cutting stage gate registry — currently in M34 spec)

## Output schema

```yaml
detector: cascade
module: {MODULE_ID}
detected_at: {ISO datetime}
total_cascades: {N}

x8_cascades:
  - new_enum_name: BACReviewStatus
    values: ["PENDING", "IN_REVIEW", "APPROVED", "REJECTED"]
    owner: M27
    suggested_x8_version: v0.5
    referenced_in: ["{LOCKED_SPEC_PATH}#Block3-DesignReview-status_field"]
    predicted_in_brief: true | false
    severity: blocker | minor   # blocker if Spec is unparseable without it

x9_cascades:
  - new_chart_type: ""
    use_case: ""
    suggested_library: ""
    suggested_x9_version: ""
    severity: blocker | minor

predecessor_cascades:
  - predecessor_module: M01
    change_type: cascade_note | full_reissue
    description: "Add field min_review_count to Project entity"
    cascade_note_path: "SystemAdmin/Modules/M01_ProjectRegistry_v1_3_CascadeNote.md"
    rationale: "M27 BR-27-014 requires this field on Project"
    referenced_in: ["{LOCKED_SPEC_PATH}#Block6-BR-27-014"]

dependent_cascades:
  []   # likely empty for forward-only modules

cross_cutting_updates:
  - target: M34_role_taxonomy | X8_severity | StageGateRegistry | other
    change: ""
    rationale: ""
    severity: blocker | minor

surfacing_message: |
  # Multi-line summary the orchestrator pastes into the user-facing report.
  # Should read like:
  #
  # M27 cascade summary:
  #   - 2 new ENUMs needed → X8 bump to v0.5 (blockers)
  #   - 1 predecessor cascade: M01 needs min_review_count field added
  #   - 0 dependent cascades
  #   - 0 cross-cutting updates
  #
  # Resolve each via /lock-decision before merging the build branch.

recommended_actions:
  - "Run /lock-decision \"BACReviewStatus ENUM\" X8 to bump X8 v0.5"
  - "Run /lock-decision \"M01.min_review_count field add\" M01 BR-27-014 to record the cascade"
  - "Manual: review M01_ProjectRegistry_v1_3_CascadeNote.md draft before commit"
```

## Hard rules

- ❌ Do NOT auto-apply cascades. They are decisions; user must approve via `/lock-decision`.
- ❌ Do NOT bump X8 or X9 yourself.
- ❌ Do NOT modify predecessor specs or write cascade notes — only propose them.
- ❌ Do NOT skip a cascade because it's "obvious." Surface every detected one — Monish triages.
- ❌ Do NOT downgrade severity. If the Spec is unparseable without an ENUM, it's a blocker.
