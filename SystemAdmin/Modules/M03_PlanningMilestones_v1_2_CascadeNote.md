# M03 — Planning & Milestones
## v1.2 Cascade Note
**Status:** Cascade Patch
**Type:** Minor version bump (audit-event addition + integration-point addition + 1 BR)
**Author:** Monish (with Claude assist)
**Created:** 2026-05-04
**Last Audited:** v1.2 on 2026-05-04 (Round 29 medium-cleanup — Format B field backfill, M29; round chronology fix M33)
**Trigger:** M06 spec lock OQ-1.3=B (dual RA Bill trigger sources — Progress + Milestone). M06 BR-06-010 + WF-06-005 require an upstream signal when a milestone of `milestone_type=Financial` is achieved, so M06 can instantiate a milestone-driven RA Bill.
**Reference Standards:** X8_GlossaryENUMs_v0_6.md, M06_FinancialControl_Spec_v1_0.md (v1.0a), M06_FinancialControl_Workflows_v1_0.md (WF-06-005)
**Folder:** SystemAdmin/Modules/

---

## CHANGE LOG

| Version | Date | Change Summary |
|---|---|---|
| v1.0 | 2026-05-03 | Initial standalone consolidated spec (Round 16) |
| v1.1 | 2026-05-03 | Appendix C audit-event catalogue (28 events) + BR-03-033 (CP transactionality) + BR-03-034 (atomic rollback). Full re-issue per Round 18 cascade-vs-re-issue rule (substantive change). |
| **v1.2** | **2026-05-04** | **`MILESTONE_ACHIEVED_FINANCIAL` audit event added (emit hook on `Milestone.status → Achieved` when `milestone_type = Financial`). New BR-03-035 (emit governance). New SENDS TO M06 entry in Block 7. Triggered by M06 BR-06-010 milestone-RA Bill creation path under Brief OQ-1.3=B.** |

---

## NATURE OF v1.2 CHANGE

This is a **surgical 3-item cascade** — minor bump triggered by M06 spec lock decision OQ-1.3=B.

### What Changes

| Aspect | Before (v1.1) | After (v1.2) |
|---|---|---|
| Milestone-achievement audit events | `MILESTONE_AUTO_ACHIEVED` (per-Achieved transition) + `MILESTONE_AUTO_DELAYED` + `MILESTONE_FORECAST_UPDATED` | **Adds** `MILESTONE_ACHIEVED_FINANCIAL` — narrow event emitted ONLY when achievement transition has `milestone_type = Financial` (subset of MILESTONE_AUTO_ACHIEVED firings) |
| Block 7 SENDS-TO list | Includes M04, M07, M09 | **Adds** M06 — receives `MILESTONE_ACHIEVED_FINANCIAL` for milestone-driven RA Bill creation |
| BR catalogue | BR-03-001 .. BR-03-034 | **Adds** BR-03-035 — emit governance for the new event |

### What Stays the Same

- All existing BRs (BR-03-001 through BR-03-034) — including BR-03-021 (daily delayed-status sweep) and BR-03-033 (CP transactionality) — unchanged
- All M03 ENUMs (X8 §3.40 through §3.51 unchanged from v0.4)
- Schedule, baseline, milestone, PV, procurement-timing core data models — unchanged
- Existing SENDS-TO targets (M04, M07, M09) and RECEIVES-FROM sources unchanged
- All existing audit events (28 catalogued in Appendix C) — unchanged

---

## CASCADE EXECUTION

### New Audit Event — `MILESTONE_ACHIEVED_FINANCIAL`

**Event type:** `MILESTONE_ACHIEVED_FINANCIAL` (UPPER_SNAKE_CASE per F-013)

**Emit trigger:** Whenever `Milestone.status` transitions to `Achieved` AND `Milestone.milestone_type = Financial`. This is a SUBSET of `MILESTONE_AUTO_ACHIEVED` firings — both events fire on the same transition for `Financial`-type milestones (the broad event for general consumers; the narrow event for M06 to subscribe without filter logic).

**Payload:**

```json
{
  "milestone_id": "uuid",
  "project_id": "uuid",
  "package_id": "uuid",
  "contract_id": "uuid",
  "milestone_type": "Financial",
  "milestone_planned_date": "YYYY-MM-DD",
  "achieved_at": "ISO datetime",
  "achieved_by": "user_id",
  "actual_date": "YYYY-MM-DD"
}
```

**Retention:** Standard 7-year audit retention (matches all M03 audit events).

### New Business Rule — BR-03-035

**Rule:** On any state transition into `Milestone.status = Achieved`, the system MUST evaluate `milestone_type`. If `milestone_type = Financial`, emit `MILESTONE_ACHIEVED_FINANCIAL` *in addition to* the standard `MILESTONE_AUTO_ACHIEVED` event. Both emits must occur within the same transactional boundary as the status update (atomic — failure to emit either event rolls back the status transition per BR-03-034 atomic rollback rule).

**Trigger:** Internal — fires from the milestone status-transition logic paths (manual `PATCH /api/v1/milestones/:id/achieve` AND auto-achievement via M04 progress reaching 100% on a milestone-bound activity).

**Validation chain:**
1. Status transition validated per existing BR-03-021 daily sweep + manual-achieve path
2. `milestone_type` resolved from Milestone row (no additional read — same row update)
3. If `Financial` → emit both events; else → emit only `MILESTONE_AUTO_ACHIEVED` (existing behaviour)
4. Both emits + status update commit as single transaction per BR-03-034

**Cascade impact:** M06 BR-06-010 subscribes to `MILESTONE_ACHIEVED_FINANCIAL` (not `MILESTONE_AUTO_ACHIEVED` — narrow event lets M06 skip filter logic and consume only relevant transitions). M06 WF-06-005 documents the consumption flow.

### New Integration Point — Block 7 SENDS-TO M06

```
SENDS TO M06 (FinancialControl):
  - Event: MILESTONE_ACHIEVED_FINANCIAL
  - Channel: internal event bus (same channel as MILESTONE_AUTO_ACHIEVED)
  - Consumer: M06 BR-06-010 (milestone-RA Bill creation under RABillTriggerSource = Milestone)
  - Coupling: required (M06 milestone-billing path is unfunctional without this signal)
  - Cascade origin: M06 Brief OQ-1.3=B (RABillTriggerSource ENUM at X8 §3.63)
```

### M03 Spec References Updated

The M03 spec v1.1 (locked Round 18 — Workflows-cascade lock; Wireframes were Round 17) requires the following minor edits when next re-issued:

| Block | Change |
|---|---|
| Block 6 — Business Rules | Add BR-03-035 (emit governance for MILESTONE_ACHIEVED_FINANCIAL) |
| Block 7 — Integration Points | Add SENDS TO M06 entry |
| Block 8 — Audit catalogue | Add `MILESTONE_ACHIEVED_FINANCIAL` row |
| Appendix C — audit events catalogue | Append `MILESTONE_ACHIEVED_FINANCIAL` (catalogue grows 28 → 29) |

**These edits are documented here as patch notes**; the M03 spec file v1.1 remains in place as the canonical pre-cascade reference. A consolidated M03 v2.0 spec re-issue is not warranted for this surgical change.

---

## RATIONALE FOR CASCADE NOTE FORMAT

Per `spec-protocol.md` Round 18 audit cascade-vs-re-issue rule:

- **Surgical addition: 1 audit event + 1 SENDS-TO entry + 1 BR (BR-03-035), scope unchanged** → cascade note (this document)
- **NOT substantive** — no new appendix, no new entity, no scope shift

Pattern precedent: `M01_ProjectRegistry_v1_1_CascadeNote.md` (single field add) + `M01_ProjectRegistry_v1_2_CascadeNote.md` (single field remove) + `M01_ProjectRegistry_v1_3_CascadeNote.md` (single field add + 1 BR). M03 v1.2 follows the same surgical pattern. (The Round 17 M03 v1.1 was a full re-issue because Appendix C was an entire new appendix — substantive.)

---

## DOWNSTREAM EFFECTS

| Module | Effect |
|---|---|
| M01 | None |
| M02 | None |
| M04 | None — M04 already emits BILLING_TRIGGER_READY for progress path (BR-04-012); milestone path is M03-driven |
| M05 | None — VO impact independent of milestone-financial emission |
| **M06** | **Consumes `MILESTONE_ACHIEVED_FINANCIAL` via internal event bus. WF-06-005 milestone-RA Bill flow unblocked. RABillTriggerSource ENUM (X8 §3.63) Milestone path operational.** |
| M07 | None — EV computation triggered by progress events, not milestone-financial |
| M09 | None — compliance milestones use `milestone_type = Regulatory`; this event fires only on `Financial` |
| M11 | None |

Bus subscription:

```
EVENT_BUS subscriber:
  consumer: M06.MilestoneRABillCreator
  filter: { event_type: "MILESTONE_ACHIEVED_FINANCIAL" }
  handler: BR-06-010
```

---

## VERIFICATION CHECKLIST

```
[ ] BR-03-035 implemented in milestone status-transition handlers (manual + auto paths)
[ ] Atomic emit + status update verified (rollback test with forced emit failure)
[ ] MILESTONE_ACHIEVED_FINANCIAL appears in audit log only when milestone_type = Financial
[ ] MILESTONE_AUTO_ACHIEVED still emits for ALL Achieved transitions (no regression)
[ ] M06 BR-06-010 subscriber receives event and instantiates RA Bill candidate
[ ] X8 v0.6 §4.12 audit-event registry includes MILESTONE_ACHIEVED_FINANCIAL (M03-listed in M03 v1.2 patch; consumed by M06)
[ ] M03 spec v1.1 referenced + this cascade note attached
[ ] No regression in BR-03-021 daily delayed-status sweep
[ ] No regression in BR-03-033 CP transactionality
[ ] No regression in BR-03-034 atomic rollback
```

---

## PENDING M03 CASCADES

For tracking — pending M03 cascades that should be consolidated into M03 v2.0 when re-issued:

| Pending | Source | Status |
|---|---|---|
| Appendix C (28 audit events) + BR-03-033 + BR-03-034 | Round 17 cascade | **DONE** — M03 v1.1 full re-issue |
| Add `MILESTONE_ACHIEVED_FINANCIAL` emit hook + BR-03-035 + SENDS TO M06 | M06 OQ-1.3=B | **This document** |

1 cascade note accumulated post-v1.1. Below the M03 v2.0 re-issue threshold. Cascade-note approach remains appropriate.

---

*v1.2 — Cascade note locked. M06 v1.0 consumption pre-wired (BR-06-010, WF-06-005). Subscribe-without-filter pattern operational.*
