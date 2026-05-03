---
name: new-round
description: Scaffold a new EPCC round artefact (Brief, Spec, Wireframes, or Workflows) with the locked naming, audit stamp, and template. Pre-fills the version log entry. Stops to ask OQ-1 design questions before generating content. Use when Monish says "/new-round", "start round N", "scaffold M0X brief", or asks to begin the next artefact in the cadence.
---

# /new-round — Scaffold an EPCC Round Artefact

## What this skill does

Creates the next round folder + artefact file with all the locked formatting in place, so Monish can immediately work on content rather than bookkeeping. Enforces cadence C1 (one artefact at a time), audit stamp I2, and the 10-block spec template.

## Required arguments

The user invokes as `/new-round <module> <artefact-type>` where:

- `<module>` is the module ID (e.g., `M03`, `M27`, `X8`, `X9`, `PF01`)
- `<artefact-type>` is one of: `brief`, `spec`, `wireframes`, `workflows`, `bump` (only valid for X8/X9)

If either is missing, ask before proceeding. Do not guess.

---

## Execution steps

### Step 1 — Confirm cadence is honoured

1. Read the current `CLAUDE.md` Section 3 (Module Status table).
2. Verify that the requested artefact is the **next** in the Brief → Spec → Wireframes → Workflows sequence for that module. If not (e.g., user asks for Spec when Brief isn't done), STOP and ask Monish to confirm — cadence C1 forbids batching/skipping.
3. Verify cross-cutting versions: read `.claude/rules/cross-cutting-standards.md` for the current X8 + X9 versions to stamp into the header.

### Step 2 — Determine round number

1. List directories matching `Round*` under `SystemAdmin/Modules/` and the project root output area (or wherever the user has historically placed rounds — confirm if ambiguous).
2. The next round number is `max(existing) + 1`.
3. Confirm the round number with Monish before creating the folder.

### Step 3 — For Briefs only: surface OQ-1 questions

A Brief MUST surface design questions, never silently make decisions.

- Read the most recent legacy / draft / prior version of this module if one exists (e.g., `ZEPCC_Legacy/M03_Planning_Milestones_v2.3.md`).
- Identify drift between legacy and current X8/X9 conventions.
- Compose a list of OQ-1 (user decisions) and OQ-2 (pattern defaults — Claude recommends, user confirms) questions.
- **Present the question list to Monish first.** Wait for answers. Only after answers are in, generate the Brief content.

### Step 4 — For Specs only: pull from approved Brief

- Read the locked Brief from the prior round.
- Verify all OQ-1 / OQ-2 questions are CLOSED in the Brief.
- If any are open, refuse to start the Spec — cadence requires the Brief to be locked first.

### Step 5 — Create the file

Folder: `Round{NN:02d}/`
Filename: `{Module}_{ShortName}_{ArtefactType}_v{Major}_{Minor}.{ext}`

Use these conventions:
- `_v1_0` for first version of an artefact
- `_v0_X` for living docs (X8, X9) where v1.0 hasn't been earned yet
- Extensions: `.md` for Brief/Spec/Workflows, `.html` for Wireframes

### Step 6 — Apply the audit stamp (I2)

Every artefact MUST start with this header:

```markdown
---
artefact: {Module}_{ShortName}_{Type}_v{Major}_{Minor}
round: {N}
date: YYYY-MM-DD
author: Monish (with Claude assist)
x8_version: v0.X
x9_version: v0.X
status: DRAFT
prior_version: {if applicable, link to predecessor}
---
```

For HTML wireframes, put the same metadata in an HTML comment at the top.

### Step 7 — Apply the artefact template

See template files in this same folder:

- `template-brief.md`
- `template-spec.md`
- `template-wireframes.html`
- `template-workflows.md`

Copy the relevant template into the new file under the audit stamp.

### Step 8 — Append to VersionLog

Append a new entry to `System Specs/EPCC_VersionLog_v1_0.md`:

```markdown
## Round {NN} — {YYYY-MM-DD}

- **Artefact:** {filename}
- **Module:** {Module}
- **Type:** {Brief | Spec | Wireframes | Workflows}
- **X8 version referenced:** v0.X
- **X9 version referenced:** v0.X
- **Status:** DRAFT
- **Notes:** _[fill in after artefact is locked]_
```

### Step 9 — Update CLAUDE.md Section 3

Move the row for that module's artefact from "Pending" to "In Progress" in the status table. Update the `Active Round` field at the top of CLAUDE.md.

### Step 10 — Report back

Tell Monish exactly:
- The folder + filename created
- Which prior artefact informed it (if any)
- The OQ-1 questions surfaced (for Briefs only)
- What's needed from him to proceed

---

## Anti-patterns — DO NOT

- ❌ Auto-generate content for a Brief without surfacing OQ-1 first
- ❌ Skip the audit stamp
- ❌ Use a different naming convention "for clarity" — the convention is locked
- ❌ Batch multiple artefacts in one round (cadence C1)
- ❌ Define a new ENUM inline — must go through X8 version bump (use `/lock-decision` for that)
- ❌ Modify the locked decisions table in CLAUDE.md without `/lock-decision`
