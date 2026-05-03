---
name: build-module
description: Drives a full module through the EPCC pipeline (Brief → Spec → Wireframes → Workflows) using drafter+auditor subagent loops at each gate. Pauses for OQ-1 user input after Brief and for review after every gate lock. Persists pipeline state so /continue-build can resume after compaction. Use when Monish says "/build-module M0X", "build module M0X", "scaffold the next module", or wants to drive a module through the four-artefact cadence end-to-end.
---

# /build-module — Multi-Agent Module Pipeline

> **Purpose:** Take one module ID through Brief → Spec → Wireframes → Workflows with self-audit loops at each gate. The orchestrator is YOU (the Claude session running this skill). Drafter and auditor work happens in subagents (Agent tool with general-purpose type).

## Required arguments

```
/build-module <module-id> [--branch=draft/build-<module-id>] [--resume]
```

- `<module-id>` — e.g., `M27`, `M28`, `M12`. Must match the canonical registry.
- `--branch` — optional. Default: `draft/build-{module-id-lowercase}`. The orchestrator works on this branch and creates a single PR with 4 commits at the end.
- `--resume` — load existing state from `.claude/state/build-{module}.json` and continue from the recorded phase.

If `<module-id>` is missing or ambiguous, ask. Do not guess.

---

## Phase 0 — Pre-flight

Before any subagent fires:

1. **Read the orchestration context yourself** (these are small, the main session needs them):
   - `CLAUDE.md` — current round, locked decisions, module status
   - `.claude/rules/spec-protocol.md` — cadence, audit stamp formats
   - `.claude/rules/cross-cutting-standards.md` — current X8 + X9 versions
   - `.claude/rules/naming-folders.md` — folder placement
   - `.claude/rules/re-entry-protocol.md` — canonical reference router

2. **Verify cadence:**
   - The module must not already have all 4 gates LOCKED (per CLAUDE.md §3 status table).
   - No other module is mid-pipeline (only one `/build-module` runs at a time).
   - If a state file exists at `.claude/state/build-{module}.json` and `--resume` was not passed, ask Monish whether to resume or restart.

3. **Verify branch:**
   - Run `git status` — working tree must be clean.
   - Run `git rev-parse --abbrev-ref HEAD` — note current branch.
   - Run `git checkout -b {branch}` (or `git checkout {branch}` if it exists). If the branch exists with prior commits, confirm with Monish before continuing.

4. **Initialise state file** at `.claude/state/build-{module}.json` per `state-schema.md`. This file is gitignored — it is transient.

5. **Report to Monish:**
   ```
   Pipeline starting for {module}.
   Branch: {branch}
   X8: v0.X · X9: v0.X
   Predecessors locked: {list}
   Estimated user pauses: 4 (one per gate)
   Type /continue-build {module} to advance after each pause.
   ```

   Wait for Monish's `proceed` before firing Phase 1.

---

## Phases 1–4 — Gate Loop Pattern

Same pattern at every gate. The only thing that changes is which drafter/auditor prompt is loaded.

### Loop pseudocode

```
iteration = 1
last_root_cause = None
same_root_cause_count = 0

while iteration <= 5:
    # 1. Drafter
    drafter_output = spawn_subagent(
        type="general-purpose",
        prompt=load("drafter-{gate}.md") + module_context + last_audit_feedback (if any)
    )

    # 2. Auditor
    audit_result = spawn_subagent(
        type="general-purpose",
        prompt=load("auditor-{gate}.md") + drafter_output
    )
    # audit_result is a JSON-shaped report: {verdict, fail_count, root_cause_class, feedback[]}

    # 3. Decide
    if audit_result.verdict == "ACCEPT":
        save_artefact_to_disk(drafter_output, gate=gate)
        update_state_file(gate=gate, status="LOCKED_PENDING_USER", iter=iteration)
        break

    if audit_result.verdict == "REJECT":
        # Convergence check: same root cause 3 iterations running → escalate
        if audit_result.root_cause_class == last_root_cause:
            same_root_cause_count += 1
        else:
            same_root_cause_count = 1
            last_root_cause = audit_result.root_cause_class

        if same_root_cause_count >= 3:
            escalate_to_monish(gate, iteration, history)
            return

        last_audit_feedback = audit_result.feedback
        iteration += 1
        continue

    if audit_result.verdict == "ESCALATE":
        escalate_to_monish(gate, iteration, history)
        return

if iteration > 5:
    escalate_to_monish(gate, iteration, history)
    return
```

### Subagent invocation rules

When you spawn a drafter or auditor:

- Use the **Agent tool** with `subagent_type: "general-purpose"`.
- Pass the **full prompt template + concrete inputs** in `prompt`. Subagents do NOT inherit your context.
- Required inputs the drafter needs (always include in prompt):
  - Module ID + ShortName + layer + owner
  - Current X8 + X9 versions and the file paths
  - List of predecessor specs (file paths) it should read
  - Path to ZEPCC_Legacy file if one exists for this module
  - Path to write the artefact to (`SystemAdmin/Modules/{filename}`)
  - The audit stamp format to use (Format A YAML for new artefacts)
  - For Brief gate: the user has NOT yet answered any OQs — drafter MUST surface them, not pre-decide
  - For Spec gate: include the path to the locked Brief from the prior gate
  - For Wireframes gate: include the path to the locked Spec
  - For Workflows gate: include the path to the locked Spec + Wireframes

- Required inputs the auditor needs (always include in prompt):
  - The drafter's output (or the file path it wrote to)
  - The acceptance criteria checklist (loaded from auditor-{gate}.md)
  - The expected output format: JSON-shaped report (see `state-schema.md`)

### After auditor ACCEPT — pause for user

```
Gate: {gate} → DRAFT_ACCEPTED (audit passed at iter {N})

Artefact: {filename} ({byte_count} bytes)

[Brief gate ONLY]
OQ-1 questions surfaced (need your answers before lock):
  OQ-1.1: <question>
    Options: A — ... / B — ... / C — ...
    My recommendation: <X> (cascade impact: ...)
  OQ-1.2: <question>
    ...

OQ-2 defaults (Claude recommends — confirm or override):
  OQ-2.1: <default>
  OQ-2.2: <default>

[All gates]
Type /continue-build {module} to lock this gate and advance.
Type /continue-build {module} --revise "<feedback>" to send back for another iteration.
Type /continue-build {module} --abort to stop the pipeline.
```

Then **STOP**. Do not auto-advance. Wait for Monish's response.

### After Monish confirms (responds with /continue-build)

1. For Brief gate: parse OQ answers, **echo them back as YAML** for confirmation, wait for Monish to confirm "yes" before locking. This is a hard gate — you cannot guess answers.
2. Update the artefact's audit stamp `status: LOCKED`.
3. `git add` + `git commit` with message `{module} {gate}: lock at iter {N} (X8 v0.X, X9 v0.X)`.
4. Update state file: this gate `LOCKED`, next gate `IN_PROGRESS`.
5. Update CLAUDE.md §3 module status row (use Edit tool — single-line change).
6. Append entry to `System Specs/EPCC_VersionLog_v1_0.md` (or v1.1 if user has bumped it).
7. Proceed to next gate (or to Phase 5 if Workflows just locked).

---

## Phase 5 — Cascade Detection

After Workflows locks:

1. Spawn cascade-detector subagent (load `cascade-detector.md`) with paths to all 4 newly-locked artefacts.
2. Detector returns a list of:
   - X8 ENUM bumps required (with proposed new ENUM values)
   - X9 chart additions required (rare)
   - Predecessor spec cascades required (e.g., M02 needs a new field because M27 references it)
3. **Surface the cascade list to Monish.** Do not auto-apply cascades — they are themselves architectural decisions.
4. If cascades exist, the user resolves them with `/lock-decision` for each (existing skill). Pipeline does not auto-bump X8.

---

## Phase 6 — Wrap-up

1. Final state file update: pipeline `COMPLETE`.
2. Push branch: `git push -u origin {branch}`.
3. Create PR via `gh pr create` (if `gh` available) with title `{module} build: 4-gate pipeline output` and body referencing each gate's commit.
4. Report to Monish:
   ```
   {module} pipeline COMPLETE.

   Gates locked: Brief / Spec / Wireframes / Workflows
   Total iterations: {sum across gates}
   Cascades flagged: {count} (resolve with /lock-decision before merging PR)
   Branch: {branch}
   PR: {url or "create manually — gh not available"}

   Review checklist before merge:
     - Read all 4 artefacts on the draft branch
     - Resolve any flagged cascades
     - Squash-merge or merge-as-is per repo policy
   ```

---

## Escalation — when iteration limit hit OR same root cause 3 times

Stop the pipeline. Do not silently fail. Output this 5-row diagnostic table to Monish:

```
ESCALATION — {module} {gate} stuck after {N} iterations

| Iter | Drafter delta | Auditor reject reason | Root cause class | Suggested user action |
|------|---------------|------------------------|-------------------|-----------------------|
| 1    | <one-line>    | <one-line>             | <class>           | <hint>                |
| 2    | <one-line>    | <one-line>             | <class>           | <hint>                |
| 3    | <one-line>    | <one-line>             | <class>           | <hint>                |
| 4    | <one-line>    | <one-line>             | <class>           | <hint>                |
| 5    | <one-line>    | <one-line>             | <class>           | <hint>                |

Most likely root cause: {repeated class}
Recommended action: {one of:
  - "Provide manual OQ-1 answers to unblock"
  - "The predecessor spec is incomplete; revise it first"
  - "Module scope is too broad; consider splitting"
  - "Cross-cutting rule conflict — needs your decision"
}

State preserved at .claude/state/build-{module}.json
Resume after fixing with: /build-module {module} --resume
```

Then STOP. Do not retry. Do not auto-fix. Wait for Monish's call.

---

## Anti-patterns — DO NOT

- ❌ Skip the user pause after a gate ACCEPT, even if you're confident
- ❌ Pre-answer OQ-1 questions in the Brief gate (violates locked rule)
- ❌ Auto-apply cascade fixes (cascades are decisions — use /lock-decision)
- ❌ Run multiple gates' subagents in parallel (cadence C1 forbids batching)
- ❌ Push to main directly (always work on the draft branch, PR at the end)
- ❌ Treat audit `REVIEW` as `ACCEPT` (REVIEW means "minor tweaks needed" — surface those tweaks to user, don't lock)
- ❌ Continue past iteration 5 — escalation is mandatory at the limit
- ❌ Inherit drafter context into auditor (auditor must read fresh from the artefact file)

---

## Smart-exit convergence rule (Q7)

The auditor's `root_cause_class` field classifies each rejection into one of:

- `MISSING_FIELD` — drafter omitted a required field/section
- `WRONG_FORMAT` — wrong audit stamp / wrong template / wrong file extension
- `INLINE_ENUM` — drafter defined an ENUM inline instead of referencing X8
- `MISSING_OQ` — drafter pre-decided a question instead of surfacing OQ-1
- `STALE_REFERENCE` — drafter referenced an old X8/X9/spec version
- `SCOPE_DRIFT` — drafter exceeded or undershot the stated scope
- `WEAK_RECOMMENDATION` — Brief recommendation lacks justification or cascade impact
- `UPSTREAM_AMBIGUITY` — predecessor spec is unclear, drafter cannot proceed
- `OTHER` — uncatalogued

If the **same class** appears in 3 consecutive iterations → escalate (don't burn iter 4–5). Other classes flipping each iteration is normal — that means the drafter is converging.

---

## File reference

This skill folder contains:

| File | Used by |
|---|---|
| `SKILL.md` | This file — orchestration |
| `drafter-brief.md` | Brief gate drafter prompt |
| `drafter-spec.md` | Spec gate drafter prompt |
| `drafter-wireframes.md` | Wireframes gate drafter prompt |
| `drafter-workflows.md` | Workflows gate drafter prompt |
| `auditor-brief.md` | Brief gate auditor prompt + criteria |
| `auditor-spec.md` | Spec gate auditor prompt + criteria |
| `auditor-wireframes.md` | Wireframes gate auditor prompt + criteria |
| `auditor-workflows.md` | Workflows gate auditor prompt + criteria |
| `cascade-detector.md` | Phase 5 cascade detector prompt |
| `state-schema.md` | JSON schema for `.claude/state/build-{module}.json` |
