# Auditor Prompt — Workflows Gate

> **You are a subagent. Independent auditor. Read the artefact, score against criteria, output the YAML schema.**

## Inputs

```
ARTEFACT_PATH:        SystemAdmin/Modules/M27_DesignControl_Workflows_v1_0.md
LOCKED_SPEC_PATH:     SystemAdmin/Modules/M27_DesignControl_Spec_v1_0.md
LOCKED_WIREFRAMES_PATH: SystemAdmin/Modules/M27_DesignControl_Wireframes_v1_0.html
```

## Pre-flight reads

1. The artefact at `ARTEFACT_PATH`
2. The locked Spec — extract:
   - All BR IDs from Block 6
   - All audit event types from Block 8
   - All Decision Queue triggers from Block 8
   - All entity names from Block 3
3. `.claude/rules/spec-protocol.md` — workflow expectations
4. `.claude/rules/cross-cutting-standards.md` — speed tiers, severity ENUMs

## Acceptance criteria

| # | Check | Pass criterion | Failure root-cause class |
|---|---|---|---|
| 1 | Audit stamp Format A YAML | All 7 fields. `spec_locked_in` and `wireframes_locked_in` populated | `WRONG_FORMAT` |
| 2 | Status DRAFT | `status: DRAFT` | `WRONG_FORMAT` |
| 3 | Workflow Index table | Present with ID/Name/Trigger/Primary Role/BRs Referenced/Speed Tier columns | `MISSING_FIELD` |
| 4 | Workflow ID format | `WF-{module-lowercase}-NNN` sequential. No gaps, no duplicates | `WRONG_FORMAT` |
| 5 | Each workflow has full structure | Decision answered, Trigger, Primary role, BR coverage, Speed tier, Idempotent, Mermaid diagram, Step-by-step, Audit events, Failure modes, Cross-module touches | `MISSING_FIELD` |
| 6 | Mermaid validity | Each ` ```mermaid ` block is syntactically valid: balanced brackets, no orphan nodes, no syntax errors. Mentally trace each | `WRONG_FORMAT` |
| 7 | BR coverage matrix present | Section "BR Coverage Matrix" with one row per Spec BR | `MISSING_FIELD` |
| 8 | All BRs covered | Every BR ID from Spec Block 6 appears in BR coverage matrix | `MISSING_FIELD` |
| 9 | NON_RUNTIME justified | Any BR marked NON_RUNTIME has a reason consistent with: DB CHECK constraint, NOT NULL constraint, unique index, FK cascade. Business logic / role authorization / audit emission are NOT acceptable as NON_RUNTIME | `WEAK_RECOMMENDATION` |
| 10 | Audit event coverage matrix present | Section "Audit Event Coverage Matrix" with one row per Spec audit event | `MISSING_FIELD` |
| 11 | All audit events emitted | Every audit event type from Spec Block 8 maps to ≥1 workflow | `MISSING_FIELD` |
| 12 | DQ trigger coverage matrix | Every Decision Queue trigger from Spec Block 8 maps to a workflow that raises it | `MISSING_FIELD` |
| 13 | Stage gate coupling section | If module participates in any SG-N (per Spec Block 8), section populated with evidence/output entity per gate | `MISSING_FIELD` |
| 14 | No invented entities | Every entity referenced in workflow steps exists in Spec Block 3 | `STALE_REFERENCE` |
| 15 | No invented audit events | Every event in workflow "Audit events emitted" tables exists in Spec Block 8 | `STALE_REFERENCE` |
| 16 | Speed tier values valid | Each workflow's Speed Tier is T1, T2, or T3 (matching `SpeedTier` ENUM in X8) | `STALE_REFERENCE` |
| 17 | Idempotency declared | Each workflow declares `Idempotent: yes/no`. If no, has duplicate-detection mechanism | `MISSING_FIELD` |
| 18 | Decision-first principle (per workflow) | Each "Decision answered:" line is a single-sentence runtime decision question | `WEAK_RECOMMENDATION` |
| 19 | Cross-module touches use API | Reads/Publishes lines reference API endpoints or event topics, not direct DB | `WRONG_FORMAT` |
| 20 | Naming convention | Filename matches `{Module}_{ShortName}_Workflows_v{Major}_{Minor}.md`. Path is `SystemAdmin/Modules/` | `WRONG_FORMAT` |

## Scoring

- **0–2 FAIL** → `verdict: ACCEPT`
- **3–4 FAIL** → `verdict: REJECT`
- **5+ FAIL** OR coverage gap (uncovered BR / unemitted audit event / unraised DQ trigger) → `verdict: ESCALATE`

(Coverage gaps are auto-escalate because they suggest the Spec was incomplete or workflows scope-shifted.)

## Output schema

```yaml
auditor: workflows
artefact_path: {ARTEFACT_PATH}
verdict: ACCEPT | REJECT | ESCALATE
fail_count: {N}
checks:
  - id: 1
    name: "Audit stamp Format A YAML"
    result: PASS | FAIL
    note: ""
  # ... all 20
root_cause_class: MISSING_FIELD | WRONG_FORMAT | INLINE_ENUM | STALE_REFERENCE | SCOPE_DRIFT | WEAK_RECOMMENDATION | UPSTREAM_AMBIGUITY | OTHER | NONE
feedback:
  - "BR-{module}-007 from Spec Block 6 is not covered by any workflow"
  - "Workflow WF-{module}-002 references audit event 'FOO_BAR' which doesn't exist in Spec Block 8"
coverage:
  spec_brs_total: {N}
  brs_runtime_covered: {N}
  brs_non_runtime: {N}
  brs_uncovered: {N}                   # MUST be 0 for ACCEPT
  spec_audit_events_total: {N}
  audit_events_emitted: {N}             # MUST equal _total for ACCEPT
  spec_dq_triggers_total: {N}
  dq_triggers_raised: {N}              # MUST equal _total for ACCEPT
  workflow_count: {N}
  mermaid_blocks: {N}                  # MUST equal workflow_count
notes_for_user_review: |
  # Free text — only when ACCEPT.
```

## Hard rules

- ❌ Don't fix workflows. Grade only.
- ❌ Don't accept "TBD" as NON_RUNTIME justification.
- ❌ Coverage gaps are auto-ESCALATE — escalation is the right signal that something upstream needs revisiting.
- ❌ Don't grade Mermaid aesthetics. Validity (parses, renders, no orphans) only.
