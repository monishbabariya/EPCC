# EPCC Operating Principles — Always Uphold

> **Purpose:** The non-negotiable principles that shape every decision in EPCC. If a recommendation conflicts with one of these, the principle wins unless explicitly overridden.

---

## 1. Decisions before execution

Every gate requires formal approval. No skipping. No post-facto justification.

## 2. Single source of truth

Each data domain has one authoritative source. Cross-module reads go through APIs, never direct DB.

## 3. Operational readiness runs parallel to construction

NABH, equipment lead times, regulatory clearances are tracked from design stage — not retro-fitted.

## 4. EPMO as governance, not administration

8–9 FTE for 15–20 projects. EPMO is not an admin function.

## 5. Spec before code

Full architectural lockdown before any line of code. Density choice A — exhaustive specs, zero ambiguity.

## 6. Cadence discipline (C1)

One artefact at a time → review → approve → next. No batching, ever.

---

## Failure Modes to Avoid

Watch for these patterns and call them out the moment you see them in suggestions or design choices:

- ❌ **Dashboard-without-decision culture** — every view answers a specific decision. If it doesn't, cut it.
- ❌ **Tool-first approach** — never "what library should we use" before "what's the spec." Build the spec first.
- ❌ **Weak data models** — every entity has explicit ownership, reserved fields, and lock semantics.
- ❌ **PMO functioning as admin** — PMO is governance. Admin tasks belong to project managers.
- ❌ **Late-stage compliance discovery** — regulatory items are tracked from SG-0, not bolted on at handover.

---

## When You're Uncertain

1. ✅ Search project knowledge / past artefacts first
2. ✅ Reference X8 (current version) before defining new ENUMs
3. ✅ Reference M34 + M01 + M02 specs before duplicating concepts
4. ❌ Don't fabricate file contents — search and confirm
5. ❌ Don't make architectural decisions silently — surface trade-offs
