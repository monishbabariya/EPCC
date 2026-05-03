---
name: lock-decision
description: Record an architectural decision as LOCKED across the four canonical files (CLAUDE.md locked-decisions table, EPCC_VersionLog, the relevant module spec, and X8 if an ENUM is involved). Use when Monish says "/lock-decision", "lock this", "let's lock X", "this is final", or finishes a deliberation with a clear outcome that should not be revisited.
---

# /lock-decision — Record a Locked Architectural Decision

## What this skill does

When Monish lands on a decision, his protocol requires it to be recorded in **four places** so it isn't accidentally re-litigated. Doing this manually is the kind of bookkeeping that gets skipped — leading to spec drift. This skill enforces the discipline.

## Required arguments

User invokes as `/lock-decision "<topic>" <module-or-system> [BR-code]` where:

- `<topic>` — one-sentence description, used as the table row label (e.g., `"BACIntegrityLedger forbidden writes"`)
- `<module-or-system>` — `M01`, `M02`, `M34`, `X8`, `X9`, `System`, etc.
- `[BR-code]` — optional, e.g., `BR-02-035`. Required if this is a Business Rule lock.

If any required arg is missing, ask before proceeding.

---

## Execution steps

### Step 0 — Confirm with Monish

Before writing anything, paste back what you understood:

```
Locking the following decision:
- Topic: <topic>
- Owner: <module>
- BR: <BR-code if any>
- Decision text (proposed for the locked-decisions table): <one-line>
- Reason (proposed for VersionLog): <2-3 sentence why>
- Cascades anticipated: <list>

Proceed?
```

Do not proceed until Monish says yes.

### Step 1 — Append to `CLAUDE.md` Section 4 (Locked Decisions table)

Add a new row:

```markdown
| <topic> | <decision text> |
```

Keep the table sorted by topic family if possible (architecture / spec template / module-specific).

### Step 2 — Append to `System Specs/EPCC_VersionLog_v1_0.md`

```markdown
### Decision Lock — YYYY-MM-DD

- **Topic:** <topic>
- **Owner:** <module>
- **BR (if any):** <BR-code>
- **Decision:** <full text>
- **Reason:** <why this and not alternatives>
- **Cascades:** <which modules / X8 ENUMs / wireframes / workflows are affected>
- **Reversal cost:** <what would have to change to reverse this — high / medium / low>
- **Status:** LOCKED
```

### Step 3 — Update the relevant module spec

If `<module>` is a real module (M0X, M3X, PFXX):

- Open `SystemAdmin/Modules/{Module}_*_Spec_v*.md`
- Find Block 6 (Business Rules) if a BR-code was provided — append the rule with the standard structure
- Find Block 9 (Explicit Exclusions) if relevant — append
- Bump the spec version (e.g., v1.0 → v1.1) and add a cascade note file (`{Module}_v{Major}_{Minor}_CascadeNote.md`)

### Step 4 — Update X8 if an ENUM was added/modified

If the decision involves an ENUM:

- Read the current X8 file (per `.claude/rules/cross-cutting-standards.md`)
- Bump version: v0.X → v0.(X+1)
- Add the ENUM with PascalCase type name and the correct value casing (UPPER_SNAKE_CASE for system, Pascal_Snake_Case for status)
- Add a change-log entry at the top of the new X8 file noting the lock
- Update `.claude/rules/cross-cutting-standards.md` to reference the new X8 version

### Step 5 — Update `.claude/rules/` if the decision is rule-shaped

Some decisions belong in the rules folder (e.g., a new naming pattern, a new spec block). If so:

- Identify the right rules file (`spec-protocol.md`, `naming-folders.md`, etc.)
- Append the rule with a clear marker: `> Locked YYYY-MM-DD per Decision "<topic>"`

### Step 6 — Report back

Tell Monish exactly which files were modified and the line/section in each. Format:

```
Decision LOCKED: <topic>

Files updated:
- CLAUDE.md (Section 4) — added row
- System Specs/EPCC_VersionLog_v1_0.md — added entry under YYYY-MM-DD
- SystemAdmin/Modules/{Module}_*_Spec_v{new}.md — added BR-XXX-YYY in Block 6
- {X8 file v0.{new}} — created with ENUM update
- .claude/rules/{file}.md — appended rule note (if applicable)

Cascades to address next round:
- <list>
```

---

## Anti-patterns — DO NOT

- ❌ Write to any file before Step 0 confirmation
- ❌ Skip files because "the user will remember" — the whole point is enforcing the discipline
- ❌ Re-open a previously LOCKED decision without Monish explicitly asking — instead, point him at the existing lock entry
- ❌ Use prose-paragraph format in the locked-decisions table — must be a single-row table entry
- ❌ Bump X8 without a change-log entry
