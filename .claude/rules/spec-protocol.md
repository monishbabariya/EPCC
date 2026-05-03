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
