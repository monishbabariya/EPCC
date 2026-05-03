# Drafter Prompt — Workflows Gate

> **You are a subagent. You have NO context from the parent session.** Read the files this prompt points to. Produce output and exit.

## Your role

Drafting **Workflows** for an EPCC module: critical runtime flows expressed as Mermaid diagrams in markdown, with a BR coverage matrix that proves every Business Rule from the Spec is exercised by at least one workflow (or explicitly marked NON_RUNTIME).

## Inputs

```
MODULE_ID, MODULE_SHORTNAME
ROUND_NUMBER, DATE
X8_VERSION, X9_VERSION
LOCKED_SPEC_PATH:        SystemAdmin/Modules/M27_DesignControl_Spec_v1_0.md
LOCKED_WIREFRAMES_PATH:  SystemAdmin/Modules/M27_DesignControl_Wireframes_v1_0.html
OUTPUT_PATH:             SystemAdmin/Modules/M27_DesignControl_Workflows_v1_0.md
PRIOR_AUDIT_FEEDBACK:    (only on iter ≥ 2)
```

## Steps

### 1. Read

1. The locked Spec — extract:
   - Block 4 (Data Population Rules) — each DPR is a workflow trigger
   - Block 6 (Business Rules) — each BR must be referenced
   - Block 8 (Audit Events) — events emitted by workflows
2. The locked Wireframes — understand the user-facing actions that initiate flows
3. **Reference workflow for pattern:** `SystemAdmin/Modules/M03_PlanningMilestones_Workflows_v1_0.md` (most recent locked workflow)

### 2. Identify the workflows

Every Spec yields 3–8 critical workflows. Categories to check:

- **Create / register flows** — entity creation paths
- **State transition flows** — entity moves through its state machine
- **Validation / decision-queue flows** — paths that hit a Decision Queue trigger
- **Cross-module integration flows** — events consumed from or published to predecessors/dependents
- **Audit-only flows** — paths that emit audit events but don't change entities (e.g., login, view)
- **Stage gate evidence flows** — paths that produce data for SG-N gate passage
- **Failure / rollback flows** — what happens when a BR is violated

### 3. Draft

Write to `OUTPUT_PATH`. Structure:

````markdown
---
artefact: {MODULE_ID}_{MODULE_SHORTNAME}_Workflows_v1_0
round: {ROUND_NUMBER}
date: {DATE}
author: Monish (with Claude assist)
x8_version: {X8_VERSION}
x9_version: {X9_VERSION}
status: DRAFT
spec_locked_in: Round {N-X}
wireframes_locked_in: Round {N-1}
---

# {MODULE_ID} {MODULE_SHORTNAME} — Workflows v1.0

## Workflow Index

| ID | Name | Trigger | Primary Role | BRs Referenced | Speed Tier |
|---|---|---|---|---|---|
| WF-{module}-001 | {name} | {trigger} | {role} | BR-{module}-001, ... | T1 |
| WF-{module}-002 | {name} | {trigger} | {role} | BR-{module}-003 | T2 |

---

## WF-{module}-001 — {name}

**Decision answered:** {one sentence}
**Trigger:** {event / user action / scheduled / API call}
**Primary role:** {ROLE_CODE}
**Secondary roles:** {ROLE_CODE list — read access during the flow}
**BR coverage:** BR-{module}-001, BR-{module}-002
**Speed tier:** T1 (real-time) / T2 (near-real-time) / T3 (batch)
**Idempotent:** yes / no — if no, explain duplicate-detection mechanism

```mermaid
flowchart TD
    Start([Trigger: ...]) --> Validate{Validation passes?}
    Validate -->|Yes| Action1[Action 1: persist + emit AUDIT_EVENT_X]
    Validate -->|No| Reject[Audit log: VALIDATION_FAILED · Severity: High]
    Action1 --> DQCheck{Hits Decision Queue?}
    DQCheck -->|Auto-approve| Persist[Final persist + emit ACTION_COMPLETED]
    DQCheck -->|Manual review| Queue[Add to Decision Queue · Notify {role}]
    Queue --> Wait{Decision rendered?}
    Wait -->|Approved| Persist
    Wait -->|Rejected| Rollback[Revert · emit ACTION_REJECTED]
    Persist --> End([Complete])
    Reject --> End
    Rollback --> End
```

### Step-by-step

1. **Trigger fires.** {detail of who initiates and through which UI/API}
2. **Validation.** {BR references — be specific: "BR-{module}-001 enforces ...", "BR-{module}-002 enforces ..."}
3. **Branch logic.** {what determines auto-approve vs Decision Queue}
4. **Persistence.** {entities written, fields updated, audit events emitted}
5. **Notification.** {who is notified, via what channel — typically `NotificationDispatch` from M34}
6. **Outcome.** {final entity state, downstream events published}

### Audit events emitted

| Event Type | When in flow | Severity | Payload |
|---|---|---|---|
| `{EVENT_NAME}` | {step #} | {Critical/High/Medium/Low/Info} | {fields} |

### Failure modes

| Failure | Detection | Response | Audit event |
|---|---|---|---|
| {failure} | {how detected} | {what happens — revert / retry / escalate} | `{EVENT_NAME}` |

### Cross-module touches

- **Reads from:** {Module}.{entity} via {API endpoint}
- **Publishes to:** {event consumer} via {event topic}

---

## WF-{module}-002 — {next workflow}

[Same structure.]

---

[Repeat for each workflow.]

---

## BR Coverage Matrix

> **Lock criterion:** Every BR from the Spec must appear in ≥1 workflow OR be explicitly marked NON_RUNTIME with justification.

| BR | Workflow(s) covering it | NON_RUNTIME reason |
|---|---|---|
| BR-{module}-001 | WF-{module}-001 | — |
| BR-{module}-002 | WF-{module}-001, WF-{module}-002 | — |
| BR-{module}-003 | — | NON_RUNTIME — DB CHECK constraint, validated at write time |

[NON_RUNTIME is acceptable for: DB CHECK constraints, NOT NULL constraints, unique indices, foreign-key cascades. NOT acceptable for: business decisions, role-based authorization, audit emission.]

## Audit Event Coverage Matrix

| Audit Event (from Spec Block 8) | Workflow(s) emitting | Frequency expectation |
|---|---|---|
| `{EVENT_NAME}` | WF-{module}-001 | per-event |

[Every audit event listed in Spec Block 8 must be emitted by at least one workflow.]

## Decision Queue Trigger Coverage

| Trigger (from Spec Block 8) | Workflow(s) raising | Decision owner role |
|---|---|---|
| `{TRIGGER_NAME}` | WF-{module}-002 | {ROLE} |

## Stage Gate Coupling

[For each SG-N gate this module participates in (per Spec Block 8), describe the workflow that produces the evidence.]

| Stage Gate | Evidence required | Workflow producing | Output entity |
|---|---|---|---|
| SG-{N} | {what} | WF-{module}-X | {entity} |

---

*Workflows locked → Module is COMPLETE. Cascade detector runs next.*
````

### 4. Output summary

```yaml
artefact_path: {OUTPUT_PATH}
workflow_count: {N}
br_total: {N}                  # from Spec Block 6
br_runtime_covered: {N}
br_non_runtime: {N}
br_uncovered: {N}              # MUST be 0 for ACCEPT
audit_events_total: {N}        # from Spec Block 8
audit_events_emitted: {N}      # MUST equal _total for ACCEPT
dq_triggers_total: {N}
dq_triggers_raised: {N}        # MUST equal _total for ACCEPT
mermaid_blocks: {N}            # one per workflow
```

---

## Hard rules — DO NOT

- ❌ Skip the BR coverage matrix. It's the lock criterion.
- ❌ Mark a BR as NON_RUNTIME unless it really is a DB constraint. Business logic is always runtime.
- ❌ Use a Mermaid diagram that doesn't render (test mentally: balanced brackets, valid syntax, no cycles unless explicit).
- ❌ Reference an audit event or DQ trigger not declared in Spec Block 8. Either add to coverage table or push back on Spec.
- ❌ Reference an entity not declared in Spec Block 3.
- ❌ Output the workflows into your response. Write to file. Output only the YAML summary.
