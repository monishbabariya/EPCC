# EPCC Spec Generation Protocol — LOCKED

> **Purpose:** How specs are produced. Cadence, artefact types, the 10-block template, density rules, and the I1–I10 improvements adopted.

---

## Cadence (C1) — LOCKED

**One artefact at a time → review → approve → next.** No batching.

---

## 4 Artefacts per Module

```
Brief → Spec → Wireframes → Workflows
```

| Artefact | Format | Purpose |
|---|---|---|
| Brief | Markdown (.md) | Surfaces design questions (OQ-1 user decisions, OQ-2 pattern defaults), recommends |
| Spec | Markdown (.md) | Full 10-block specification (locked from Brief decisions) |
| Wireframes | Single HTML file | Tailwind CDN, role switcher, all views per role |
| Workflows | Markdown with Mermaid | Critical runtime flows with BR traceability |

**Wireframe rules (D3 lock):** Full HTML, Tailwind CDN, no JS deps.
**Workflow rules:** Mermaid in markdown.

---

## 10-Block Spec Template (LOCKED)

```
1.  Identity
2.  Scope Boundary
3.  Data Architecture
4.  Data Population Rules
5.  Filters & Views
6.  Business Rules
7.  Integration Points
8.  Governance & Audit
9.  Explicit Exclusions
10. Open Questions  ← must close at zero before lock
```

**Rule:** A spec cannot be marked LOCKED while any Open Question is unresolved.

---

## Density Choice (A) — LOCKED

Full density, future-proofed. Specs are dense and exhaustive — designed to drive the build with zero ambiguity.

---

## Improvements Adopted (I1–I10)

- **I1** Master VersionLog tracker
- **I2** Audit stamps on every artefact
- **I3** Living glossary (X8 ENUMs)
- **I4** Fully-qualified FK references
- **I5** Brief → Spec → Wireframe gating
- **I6** Audit per round
- **I7** Legacy frozen as ARCHIVED
- **I8** Continuous ENUM audit
- **I9** Living cross-cutting docs (X1-X8)
- **I10** _INDEX file per folder

---

## Audit Stamp (I2) — Required Header on Every Artefact

Three accepted formats — pick by artefact type:

### Format A — YAML frontmatter (preferred for new markdown artefacts from Round 18 onward)

```markdown
---
artefact: {Module}_{ShortName}_{Type}_v{Major}_{Minor}
round: {N}
date: YYYY-MM-DD
author: Monish (with Claude assist)
x8_version: v0.X
x9_version: v0.X
status: DRAFT | UNDER_REVIEW | LOCKED
---
```

### Format B — Markdown bold-header block (grandfathered for Briefs and Specs locked Rounds 1–17)

Used by M34/M01/M02/M03 Briefs and Specs. Acceptable on existing artefacts; not required to retro-convert. New Briefs/Specs from Round 19+ should prefer Format A unless cadence dictates otherwise. Required fields:

```markdown
**Status:** Locked | Draft | UNDER_REVIEW
**Author:** Monish (with Claude assist) | _grandfathered: PMO Director / System Architect_
**Created:** YYYY-MM-DD | **Last Updated:** YYYY-MM-DD
**Last Audited:** v{Major}.{Minor} on YYYY-MM-DD
**Reference Standards:** _(comma-separated — current X8 + X9 versions + cross-module specs at their current revisions or cascade notes)_
```

### Format C — HTML comment block (for `.html` wireframes)

```html
<!--
artefact: {Module}_{ShortName}_Wireframes_v{Major}_{Minor}
round: {N}
date: YYYY-MM-DD
author: Monish (with Claude assist)
x8_version: v0.X
x9_version: v0.X (or "n/a (pre-X9)" for wireframes locked before X9 v0.1)
status: LOCKED
-->
<!DOCTYPE html>
```

### Cascade notes

Cascade notes (e.g., `M01_ProjectRegistry_v1_X_CascadeNote.md`) follow Format B with `Status: Cascade Patch` and `Type: {field addition | field removal | minor bump}`. See `M01_ProjectRegistry_v1_2_CascadeNote.md` as the canonical pattern.

### Cascade-vs-Re-issue decision (locked Round 18 audit)

When a locked module receives a downstream cascade:

- **1 small change (1 field add/remove, 1 BR addition, scope unchanged)** → cascade note. Don't re-issue the full spec.
- **Substantive change (new appendix, multiple BRs, new entity, scope-shifting)** → full spec re-issue with `_v{Major}_{Minor+1}.md` rename via `git mv`.
- **Examples:** M01 v1.1 (field add) + v1.2 (field remove) = cascade notes. M03 v1.1 (Appendix C + 2 BRs) = full re-issue.

### In-Place Patch Convention (locked 2026-05-04)

An **in-place patch** corrects factual errors, stale references, or internal contradictions in a LOCKED artefact **without extending scope**. It is distinct from a cascade note (which extends scope) and a re-issue (which changes substance).

**When permitted:**

- Correcting internal contradictions within a single LOCKED artefact (e.g., status field says LOCKED but footer says DRAFT)
- Updating frontmatter version stamps after a cross-cutting doc (X8/X9) bumps post-lock
- Correcting stale round/date references that don't change any decision
- Correcting ENUM label drift where the intended value is unambiguous

**When NOT permitted (use cascade note or re-issue instead):**

- Adding a new field, entity, BR, or integration point
- Changing a locked decision (any item in CLAUDE.md §4)
- Resolving an OQ that was marked closed (re-open via new Brief round instead)
- Any change affecting Block 2 (Scope Boundary) or Block 6 (Business Rules)

**Versioning:**

- First patch: `v{Major}.{Minor}a` (e.g., v1.0 → v1.0a)
- Second patch: `v{Major}.{Minor}b`, and so on
- File is edited in-place — no `git mv`, no new file created
- Update only the version reference in the frontmatter `artefact:` field (or Format B H2 heading) and the `CHANGE LOG` entry; filename on disk remains `_v1_0.md`
- **Letter suffix only** — numeric dot-suffixes (e.g. `v0.6.1`) are not used. Living cross-cutting docs (X8, X9) use the same convention as specs: `v0.6a`, `v0.6b`. This distinction applies regardless of document type.

**Required documentation within the patched file:**

Every in-place patch MUST add a `CHANGE LOG` entry at the top of the file (below the audit stamp) in this format:

```markdown
| Patch | Date       | Author                      | Changes |
|-------|------------|-----------------------------|---------|
| v1.0b | YYYY-MM-DD | Monish (with Claude assist) | [1-line description per fix] |
```

**Audit stamp update on patch:**

- `artefact:` field (Format A) / H2 heading (Format B): update version suffix (v1_0 → v1_0b for Format A; v0.6 → v0.6a for Format B)
- `date:` field: update to patch date
- `status:` must remain LOCKED (a patch does not re-open the artefact)
- `x8_version:` / `x9_version:`: update if the patch corrects a stale stamp
- All other fields: unchanged

**Git commit message convention:**

```
patch({module}): {ArtefactType} v{X}.{Y}{letter} — {reason}
```

Example: `patch(M06): Spec v1.0b — fix DRAFT footer, resolve 43-vs-28 event count contradiction, refresh X8/X9 stamps`

---

## Anti-Drift Rules (X8 reference)

- Every spec references X8 — never redefines ENUMs inline
- New ENUM values require X8 version bump + change log entry
- Deprecated ENUMs marked DEPRECATED, not deleted

---

## When to Stop and Ask

A Brief MUST surface decisions, never silently make them. Categories:

- **OQ-1** (user decisions): architecture, scope, behaviour the user must choose
- **OQ-2** (pattern defaults): technical defaults Claude recommends, user confirms

If a question doesn't fit either, raise it in conversation before adding to Brief.
