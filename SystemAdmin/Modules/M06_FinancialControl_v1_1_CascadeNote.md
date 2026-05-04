# M06 — Financial Control
## v1.1 Cascade Note
**Status:** Cascade Patch
**Type:** Integration clarification — scope reduction (one stub endpoint removed; one trigger source narrowed)
**Author:** Monish (with Claude assist)
**Created:** 2026-05-04
**Trigger:** Round 29 audit finding H6 — `SG_11_PASSAGE` listed as a co-trigger for BR-06-028 (DLP_End retention release) in Block 7 RECEIVES FROM M08, with corresponding stub endpoint `POST /api/m06/v1/events/sg11-passage`. WF-06-009 also reads "may also accompany SG_11_PASSAGE". Architectural review (H6 Option B, locked 2026-05-04) determined SG_11_PASSAGE is **not** a causal trigger — it co-occurs in practice but the financial signal that drives BR-06-028 is sourced solely from M15.
**Parent Spec:** M06_FinancialControl_Spec_v1_0.md (in-place patched to v1.0b in Round 29; see `M06_FinancialControl_Spec_v1_0.md` CHANGE LOG)
**Reference Standards:** X8_GlossaryENUMs_v0_6.md (v0.6a), M03_PlanningMilestones_Spec_v1_1.md (+ v1.2 cascade note for `MILESTONE_ACHIEVED_FINANCIAL`), M01_ProjectRegistry_Spec_v1_0.md (+ v1.3 cascade note for `Contract.dlp_retention_split_pct`), CLAUDE.md §4 Locked Decisions (H6 row)
**Folder:** SystemAdmin/Modules/

---

## CHANGE LOG

| Version | Date | Change Summary |
|---|---|---|
| v1.0 | 2026-05-03 | Initial standalone consolidated spec (Round 25). 17 entities (4 append-only ledgers, DB UPDATE/DELETE forbidden), 47 BRs, 17 DPRs, 43 audit events, 13 integration points. |
| v1.0a | 2026-05-03 | Round 27 in-place audit-correction patch — Stage Gate naming disambiguation: tranche-1 retention release trigger renamed `SG_11_PASSAGE` → `SG_9_PASSAGE`. Tranche-2 retains `SG_11_PASSAGE`. Both endpoints exposed for M08. |
| v1.0b | 2026-05-04 | Round 29 in-place patch — LOCKED footer (C1), 43-event count fix (C2 ×3 sites), X8/X9 stamp refresh (H2/G), round refs (H5/H8). |
| **v1.1** | **2026-05-04** | **Round 29: H6 Option B — `SG_11_PASSAGE` removed as a trigger for BR-06-028. Stub endpoint `POST /api/m06/v1/events/sg11-passage` REMOVED from Block 7 OPEN INTEGRATION POINTS. BR-06-028 trigger conditions narrowed to `DLP_RETENTION_RELEASE_ELIGIBLE` (M15) + M09 zero-counts only. WF-06-009 informational note added (SG_11_PASSAGE co-occurs but is not consumed). No BR text changed; no entity changed; no field changed.** |

---

## NATURE OF v1.1 CHANGE

This cascade note is **scope-reducing** — one stub integration is removed. It does not add a field, entity, BR, or audit event. The removal closes a defective integration surface where M06 was declaring an IN integration to a signal it does not (and should not) consume.

Per spec-protocol §Cascade-vs-Re-issue: cascade-note vehicle is correct (not re-issue) — 0 fields added/removed, 0 BRs added, 0 entities changed. The single existing BR-06-028 trigger condition list is narrowed by removing one item that should never have been there.

---

## H6 — Decision Summary

**Option B (locked 2026-05-04):** SG_11_PASSAGE is NOT a trigger for BR-06-028 (DLP_End retention release). It co-occurs in practice but is not a causal dependency. M06 owns the financial signal layer; M06 should consume **financial** signals (`DLP_RETENTION_RELEASE_ELIGIBLE` from M15) — not stage-gate events (`SG_11_PASSAGE` from M08).

**Why this matters architecturally:**
- **Layer separation:** Stage-gate events belong to M08 (Stage Gate engine). Financial state machine belongs to M06. Mixing them mints a cross-layer dependency that hides the true causation.
- **Single-Owner Rule (F-005):** M15 owns the DLP completion signal. M06 should consume it through M15, not duplicate the listening surface against M08.
- **Future M08 integration map:** when M08 is specced, scanning M06 Block 7 for declared IN integrations would have surfaced a spurious OUT requirement on M08 for `SG_11_PASSAGE` → M06. Removing the stub now prevents that drift.
- **WF-06-009 wording precision:** "may also accompany SG_11_PASSAGE" describes correlation, not causation. Documentation imprecision, not a missing trigger.

---

## Block 7 — RECEIVES FROM M08 (Edit)

### Before (M06 Spec v1.0b line 709)

> | RECEIVES FROM | M08 GateControl (stub until M08 built) | `SG_9_PASSAGE` event (Substantial / Practical Completion) → Retention.eligible_at population for Substantial_Completion tranche (BR-06-027); **`SG_11_PASSAGE` event (DLP End / Project Closure) consumed alongside M15/M09 zero-counts for DLP_End tranche (BR-06-028)** | Event (stub endpoint contract documented at v1.0) | T1 |

### After (apply when reading Block 7)

> | RECEIVES FROM | M08 GateControl (stub until M08 built) | `SG_9_PASSAGE` event (Substantial / Practical Completion) → Retention.eligible_at population for Substantial_Completion tranche (BR-06-027) | Event (stub endpoint contract documented at v1.0) | T1 |

### Block 7 — Clarifying Note (Add)

Add the following note immediately below the RECEIVES FROM table in Block 7:

> **Note on SG_11_PASSAGE (M08 → M06):** This event is **NOT** a trigger for BR-06-028. DLP_End retention release fires solely on `DLP_RETENTION_RELEASE_ELIGIBLE` (from M15) plus M09 zero-counts. SG_11_PASSAGE co-occurs in practice (DLP closure typically aligns with the SG-11 stage gate) but M06 does not consume the SG-11 event. M08 need not declare an OUT integration to M06 for `SG_11_PASSAGE`. When M15 is specced, M15 Block 7 must declare OUT → M06 for `DLP_RETENTION_RELEASE_ELIGIBLE` (this is the single, authoritative trigger source). Locked Round 29 audit (H6 Option B).

### Stub Endpoint — REMOVED

M06 Spec v1.0b line 720 declares:

```
POST /api/m06/v1/events/sg11-passage                # M08 → M06 (BR-06-028) — DLP End / Project Closure
```

**This endpoint is removed.** When generating the M06 OpenAPI surface, do not emit a route for `/api/m06/v1/events/sg11-passage`. The remaining stub endpoint `POST /api/m06/v1/events/sg9-passage` (for tranche-1 / BR-06-027) is unchanged and remains in scope.

---

## BR-06-028 — Trigger Conditions (Clarified, Not Changed)

BR-06-028's existing trigger conditions are unchanged in semantics; the cascade note clarifies the **canonical** condition set:

| Trigger Condition | Source | Notes |
|---|---|---|
| `DLP_RETENTION_RELEASE_ELIGIBLE` event | M15 (HandoverManagement / DLP) — Phase 2 | **Sole financial signal.** M15 emits this when DLP period closes and zero pending defects condition is met. |
| M09 zero-counts (open NCRs / open compliance items related to DLP) | M09 (ComplianceTracker) | Pre-existing condition, unchanged |
| `RetentionRelease.tranche_2_status` = ELIGIBLE | M06 internal | Existing internal precondition, unchanged |

**Removed from trigger list:** `SG_11_PASSAGE` event (M08). This was never a true trigger — it appeared in v1.0 as documentation of co-occurrence and was inadvertently structured as a stub integration. Round 29 audit corrects this.

**BR-06-028 text itself is unchanged.** The BR governs *what happens* when triggers fire (RetentionRelease.amount calculation, dual sign-off requirement above ₹50L threshold, audit emit). None of that changes; only the trigger source list is narrowed.

---

## WF-06-009 — Informational Note (Add)

The phrase "may also accompany SG_11_PASSAGE" in WF-06-009 (DLP retention release tranche-2 workflow) describes real-world co-occurrence between DLP closure and SG-11 stage gate passage. It is informational only — **not** a workflow trigger, not a Mermaid-visualised step, and does not require a runtime listener.

When reading WF-06-009, treat any reference to SG_11_PASSAGE as a contextual annotation. The actual trigger is `DLP_RETENTION_RELEASE_ELIGIBLE` (M15) + M09 zero-counts (per BR-06-028 above). No workflow logic change required.

---

## DOWNSTREAM IMPACT

### Forward Constraints (must respect when specced)

| Module | Status | Constraint Imposed by H6 Option B |
|---|---|---|
| **M08** GateControl | Phase 1 — not yet specced | Must NOT declare an OUT integration to M06 for `SG_11_PASSAGE`. M06 does not consume this event. |
| **M15** HandoverManagement (DLP) | Phase 2 — not yet specced | MUST declare OUT → M06 for `DLP_RETENTION_RELEASE_ELIGIBLE`. This is the sole financial-signal source for BR-06-028 tranche-2 release. M15 spec must define when this event is emitted (DLP period close + zero defects). |

These constraints should be added to a "M08 / M15 Spec Pre-Conditions" forward-pointer list when the brief for either module opens.

### No Cascade Required (Already Aligned)

- **M01 v1.3 cascade note** (`Contract.dlp_retention_split_pct`) — already aligned (M06 consumes the field; no change to that integration)
- **M03 v1.2 cascade note** (`MILESTONE_ACHIEVED_FINANCIAL` emit hook) — unrelated to DLP path; concerns RA Bill milestone trigger only
- **M04** ExecutionCapture — unrelated (NCR/progress signals only; no DLP path)
- **No code impact** (Phase 1 spec-only)

### VersionLog Update (Deferred)

VersionLog §3.7 M06 row should reference the v1.0a + v1.0b + v1.1 cascade-note chain when the medium-cleanup branch lands (deferred to `audit/round-29-medium-cleanup`).

---

*Cascade note v1.1 — LOCKED 2026-05-04 — Round 29 audit (H6 Option B). No re-issue required (per spec-protocol.md §Cascade-vs-Re-issue: 0 fields added, 0 BRs added/changed; one stub integration scope-reduced; all changes are reference clarifications).*
