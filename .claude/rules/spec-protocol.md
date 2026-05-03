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
