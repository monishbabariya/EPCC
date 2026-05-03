# Pipeline State Schema

> Lives at `.claude/state/build-{module-lowercase}.json`. Gitignored. Survives session compaction so `/build-module {module} --resume` can pick up cleanly.

## Purpose

Single JSON file the orchestrator reads/writes between subagent calls. It's the source of truth for "where are we in the pipeline."

## Schema

```json
{
  "schema_version": 1,
  "module": "M27",
  "module_shortname": "DesignControl",
  "started_at": "2026-05-04T10:30:00Z",
  "last_updated_at": "2026-05-04T11:45:00Z",
  "branch": "draft/build-m27",
  "x8_version_at_start": "v0.4",
  "x9_version_at_start": "v0.2",

  "current_phase": "spec",
  "phase_state": "DRAFTING",

  "phases": {
    "brief": {
      "status": "LOCKED",
      "started_at": "2026-05-04T10:30:00Z",
      "locked_at": "2026-05-04T10:55:00Z",
      "iterations": 2,
      "iteration_history": [
        {
          "iter": 1,
          "drafter_output_path": "SystemAdmin/Modules/M27_DesignControl_Brief_v1_0.md",
          "auditor_verdict": "REJECT",
          "fail_count": 3,
          "root_cause_class": "MISSING_OQ",
          "feedback_summary": "OQ-1.2 pre-decided in body without surfacing options"
        },
        {
          "iter": 2,
          "drafter_output_path": "SystemAdmin/Modules/M27_DesignControl_Brief_v1_0.md",
          "auditor_verdict": "ACCEPT",
          "fail_count": 0,
          "root_cause_class": "NONE"
        }
      ],
      "oq1_count": 5,
      "oq2_count": 3,
      "oq_answers": {
        "OQ-1.1": { "answer": "B", "answered_at": "2026-05-04T10:50:00Z" },
        "OQ-1.2": { "answer": "A", "answered_at": "2026-05-04T10:50:00Z" }
      },
      "git_commit": "abc123de"
    },
    "spec": {
      "status": "DRAFTING",
      "started_at": "2026-05-04T11:00:00Z",
      "iterations": 1,
      "iteration_history": [
        {
          "iter": 1,
          "drafter_output_path": "SystemAdmin/Modules/M27_DesignControl_Spec_v1_0.md",
          "auditor_verdict": "REJECT",
          "fail_count": 4,
          "root_cause_class": "MISSING_FIELD",
          "feedback_summary": "Reserved fields missing on DesignReview entity"
        }
      ]
    },
    "wireframes": { "status": "PENDING" },
    "workflows": { "status": "PENDING" },
    "cascade_detection": { "status": "PENDING" }
  },

  "convergence_tracker": {
    "last_root_cause_class": "MISSING_FIELD",
    "same_root_cause_count": 1
  },

  "escalations": []
}
```

## State machine — `phase_state` per phase

```
PENDING → DRAFTING → AUDITING → ACCEPTED → LOCKED_PENDING_USER → LOCKED
                  ↓                                              ↑
                  REJECTED → DRAFTING (next iter)               (user /continue-build)
                  ↓
                  ESCALATED → (await Monish)
```

## Status field values for each phase

| Status | Meaning |
|---|---|
| `PENDING` | Not yet started |
| `DRAFTING` | Drafter subagent currently running OR drafter output captured, awaiting audit |
| `AUDITING` | Auditor subagent currently running |
| `REJECTED` | Auditor rejected, ready for next iter |
| `ACCEPTED` | Auditor accepted, awaiting user pause confirmation |
| `LOCKED_PENDING_USER` | Same as ACCEPTED — explicit "user must `/continue-build`" state |
| `LOCKED` | User confirmed, git committed |
| `ESCALATED` | 5 iter exceeded OR same root cause 3× — pipeline halted |

## Convergence tracker

Updated on every audit:

- If new `root_cause_class` differs from `last_root_cause_class`: reset `same_root_cause_count = 1`, update `last_root_cause_class`
- If new `root_cause_class` matches: `same_root_cause_count += 1`
- If `same_root_cause_count >= 3`: orchestrator must escalate (do not proceed to iter 4)

## Escalations array

Append-only log of escalations:

```json
{
  "phase": "brief",
  "escalated_at": "2026-05-04T11:30:00Z",
  "reason": "same_root_cause_3x | iter_limit_5 | upstream_ambiguity",
  "diagnostic_table": "...rendered 5-row table..."
}
```

## Read/write rules

- Orchestrator reads at the start of every phase
- Orchestrator writes after every drafter run, every audit, every state transition
- Subagents do NOT read or write this file — they receive their inputs via prompt and return outputs via response
- File is JSON — atomic write (write to `.tmp` + rename) to avoid corruption under crash

## Resume protocol

When `--resume` is passed:

1. Read state file
2. If `phases[current_phase].status == LOCKED_PENDING_USER`: this means user paused mid-flow. Surface the pause-prompt again.
3. If `phases[current_phase].status == DRAFTING/AUDITING/REJECTED`: continue from next iter
4. If `phases[current_phase].status == ESCALATED`: refuse to resume. Tell user to address the escalation reason and clear the state file (or rerun without `--resume` to restart).
