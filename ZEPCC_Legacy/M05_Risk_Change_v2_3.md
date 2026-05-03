# M05 — Risk & Change Control
## Module Specification v2.3
## AMENDMENT — Changed Blocks Only
**Status:** Draft — Pending Review | **Locked:** No
**Spec Author:** PMO Director | **Date:** 2026-05-02
**Reference Standards:** EPCC_Standards_Memory_v5_0.md
**Base Version:** M05_Risk_Change_v2.2
**Amendment Scope:** GAP-02 resolution — VO-to-BOQ Materialisation workflow.
                     VO lifecycle extended. VOBOQMaterialisation entity added.

> **HOW TO READ THIS FILE:**
> This is an amendment document. All blocks not listed here remain
> unchanged from M05_Risk_Change_v2.2.
> Apply these changes on top of v2.2 to produce the complete v2.3 spec.

---

## CHANGE LOG

| Version | Date | Change Summary |
|---------|------|---------------|
| v2.0 | 2026-04-30 | Block 10 resolved: hybrid categories; proactive VO; LD auto; combined Monte Carlo |
| v2.1 | 2026-04-30 | Block 7 updated: M06 BG expiry signal to M05 |
| v2.2 | 2026-04-30 | Block 7: M05 sends change_event_id to M08 on ChangeLog entry |
| v2.3 | 2026-05-02 | GAP-02: VOBOQMaterialisation entity added. VO lifecycle extended with materialisation step. BR-05-028 through BR-05-034 added. Block 7 updated with M02 and M07 integration for materialisation. |

---

## BLOCK 2 — Scope Boundary (Updated)

**ADDITIONS to INCLUDES:**

| INCLUDES (New) | Rationale |
|----------------|-----------|
| VO-to-BOQ Materialisation workflow — trigger, tracking, and completion | GAP-02: Ensures approved VO cost is reflected in M02 BAC before M07 resumes EAC calculations |
| `VOBOQMaterialisation` entity — materialisation record with SLA governance | GAP-02 |
| BAC integrity signal — triggers M02 and M07 on VO approval with cost impact | GAP-02 |

**ADDITION to EXCLUDES:**

| EXCLUDES (Clarification) |
|--------------------------|
| BOQ item creation or quantity revision — initiated via materialisation workflow but executed in M02 |
| BAC recalculation — M02 owns BAC. M05 triggers the materialisation; M02 performs the update. |

---

## BLOCK 3 — Data Architecture (Amendment)

### 3a. New Entity

| Entity | Description | Cardinality |
|--------|-------------|-------------|
| `VOBOQMaterialisation` | **(NEW v2.3)** Tracks the workflow of translating an approved VO's cost impact into updated BOQ items in M02. Ensures BAC integrity is maintained after every VO approval. | 1 per approved VO with cost_impact > 0 |

---

### 3b. New Entity Fields — `VOBOQMaterialisation`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `materialisation_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | LINK → M01 Project |
| `vo_id` | UUID | Y | FK → VariationOrder. One materialisation per VO (where cost_impact > 0). | LINK → VariationOrder |
| `vo_code` | VARCHAR(20) | Y | Denormalised from VO for display | LINK → VariationOrder |
| `cost_impact_approved` | DECIMAL(15,2) | Y | Copied from VariationOrder.approved_cost at trigger time. Immutable. | LINK → VariationOrder |
| `cost_impact_materialised` | DECIMAL(15,2) | N | Actual BAC change confirmed by M02 after QS completes update. CALC on completion. | CALC |
| `materialisation_status` | ENUM | Y | `Pending / In_Progress / Completed / Escalated` | SYSTEM |
| `option_selected` | ENUM | N | `Quantity_Revision / New_BOQ_Items / Split` — QS selects. Required before In_Progress. | INPUT (QS Manager) |
| `affected_package_ids` | JSONB | Y | Array of package_ids affected by this VO. System-identified from VO scope. | SYSTEM |
| `affected_boq_ids` | JSONB | N | Array of boq_ids updated/created during materialisation. Populated on completion by M02. | LINK → M02 |
| `old_bac_snapshot` | DECIMAL(15,2) | Y | Total project BAC at moment of VO approval — for audit. Captured at trigger time. | SYSTEM |
| `new_bac_snapshot` | DECIMAL(15,2) | N | Total project BAC after materialisation completes. Populated by M02. | LINK → M02 |
| `bac_delta_actual` | DECIMAL(15,2) | N | CALC = new_bac_snapshot − old_bac_snapshot. Should equal cost_impact_approved ± rounding. | CALC |
| `delta_variance` | DECIMAL(15,2) | N | CALC = bac_delta_actual − cost_impact_approved. Flagged if > ₹10,000. | CALC |
| `materialised_by` | UUID | N | FK → Users (QS Manager who completed the workflow) | INPUT (QS Manager) |
| `materialised_at` | TIMESTAMP | N | Auto on completion | SYSTEM |
| `qs_notes` | TEXT | N | Free text — min 30 chars mandatory when option_selected | INPUT (QS Manager) |
| `sla_deadline` | TIMESTAMP | Y | Auto = VO approval_date + 48 hours | CALC |
| `decision_queue_id` | UUID | Y | FK → DecisionQueueItem created at trigger | LINK → DecisionQueueItem |
| `escalation_level` | ENUM | Y | `None / QS_Manager / Project_Director / PMO_Director` — current escalation state | SYSTEM |

---

### 3b. Updated Fields — Entity: `VariationOrder`

**Fields ADDED to existing VariationOrder entity:**

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `materialisation_required` | BOOLEAN | Y | **(NEW)** Auto = true when vo_status = Approved AND cost_impact > 0. False otherwise. | CALC |
| `materialisation_id` | UUID | N | **(NEW)** FK → VOBOQMaterialisation. Populated when materialisation record created. | LINK → VOBOQMaterialisation |
| `materialisation_status` | ENUM | N | **(NEW)** Denormalised from VOBOQMaterialisation.materialisation_status for fast VO list view. | LINK → VOBOQMaterialisation |
| `bac_integrity_cleared_at` | TIMESTAMP | N | **(NEW)** Populated when materialisation completes and M02 BAC is updated. | LINK → VOBOQMaterialisation |

---

### 3c. VO Lifecycle — Updated (v2.3)

The existing 11-stage VO lifecycle is extended as follows for VOs with cost_impact > 0:

```
EXISTING LIFECYCLE (unchanged):
Draft → Internal_Review → Submitted → Client_Assessment → Negotiation
→ Approved / Partially_Approved / Rejected / Disputed
→ (if approved/partially_approved) → Settled / Arbitration

NEW POST-APPROVAL STEP (v2.3 — applies when Approved AND cost_impact > 0):
→ Approved
      └─→ BOQ_Materialisation_Pending    [auto-state — set immediately after Approved]
                  └─→ BOQ_Materialisation_In_Progress   [QS Manager starts workflow]
                              └─→ BOQ_Materialisation_Complete   [M02 BAC updated, confirmed]
                                          └─→ Settled   [existing final state]

For VOs with cost_impact = 0 (time-only EOT VOs):
  Approved → [no materialisation step] → routes to M03 BaselineExtension → Settled

The VO.vo_status field ENUM must be extended to include:
  BOQ_Materialisation_Pending
  BOQ_Materialisation_In_Progress
  BOQ_Materialisation_Complete

These are internal workflow states — not visible to the client.
On all external-facing VO views and exports: status shown as "Approved (Processing)" until Settled.
```

---

## BLOCK 6 — Business Rules (Amendment — new rules v2.3)

*All existing rules BR-05-001 through BR-05-027 from v2.2 remain in force.*
*The following rules are ADDED in v2.3:*

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---------|---------|-------|--------|------------|
| BR-05-028 | `VariationOrder.vo_status` → `Approved` AND `cost_impact > 0` | Materialisation workflow initialised | (1) Create `VOBOQMaterialisation` record (status = Pending). (2) Set `VariationOrder.materialisation_required = true`. (3) Set `VariationOrder.vo_status = BOQ_Materialisation_Pending`. (4) Signal to M02: set `Package.bac_integrity_status = Stale_Pending_VO` for all affected packages. (5) Signal to M07: `bac_integrity_status = Stale_Pending_VO` → EAC suspended. (6) Create DecisionQueueItem (see below). | 🔴 Real-time |
| BR-05-029 | BR-05-028 fires — Decision Queue creation | Following BR-05-028 | Create DecisionQueueItem: `trigger_type = VO_BOQ_MATERIALISATION_REQUIRED`, severity = `HIGH`, owner_role = `QS_Manager`, owner_user_id = assigned QS Manager for project, sla_hours = 48, context = {vo_id, vo_code, cost_impact_approved, packages_affected}. WhatsApp + in-app notification to QS Manager and Project Director. | 🔴 Real-time |
| BR-05-030 | QS Manager opens VOBOQMaterialisation workflow | `materialisation_status → In_Progress`. QS selects Option A, B, or C. | Set `VariationOrder.vo_status = BOQ_Materialisation_In_Progress`. Validate: option_selected is not null and qs_notes ≥ 30 chars before allowing BOQ edits in M02. | 🔴 Real-time |
| BR-05-031 | VOBOQMaterialisation workflow submitted by QS | All affected M02 BOQ items updated or created | Receive confirmation from M02: `cost_impact_materialised` + `new_bac_snapshot` populated. Set `materialisation_status = Completed`. Set `VariationOrder.materialisation_status = BOQ_Materialisation_Complete`. Set `VariationOrder.bac_integrity_cleared_at = NOW()`. Signal to M02: `bac_integrity_status = Confirmed` for all affected packages. Signal to M07: `bac_integrity_status = Confirmed` → EAC suspension lifted → STANDARD RecalcQueue job created. Set `VariationOrder.vo_status = BOQ_Materialisation_Complete`. Resolve Decision Queue item. | 🔴 Real-time |
| BR-05-032 | `bac_delta_actual` deviates from `cost_impact_approved` by > ₹10,000 | Calculated on materialisation completion | `delta_variance` field populated. Alert to PMO Director and Finance Lead: "VO materialisation BAC delta mismatch: Approved ₹{X} vs Actual BAC change ₹{Y}. QS review required." Decision Queue item created: severity = MEDIUM, owner = PMO Director, SLA = 48hr. | 🔴 Real-time |
| BR-05-033 | VOBOQMaterialisation SLA breach — 48hr elapsed | System check | Escalate Decision Queue item to Project Director. Set `materialisation_status = Escalated`. `escalation_level = Project_Director`. Governance breach notification to PMO Director. | 🟡 2-4hr |
| BR-05-034 | VOBOQMaterialisation SLA breach — 72hr elapsed total | System check | Escalate to PMO Director. `escalation_level = PMO_Director`. GovernanceBreachLog entry created (permanent). Badge on M10 portfolio war room: "BAC Integrity — VO Materialisation Overdue: {project_code}". | 🟡 2-4hr |

---

### Updated Rule — BR-05-009 (VO Approval — existing rule, updated)

The existing VO approval rule must be updated to route VOs with cost_impact > 0 through the materialisation workflow:

```
BR-05-009 (VO Approval) — Updated in v2.3:
  When VO is approved:
    IF cost_impact > 0:
      → Execute BR-05-028 (materialisation workflow initialisation)
      → VO does NOT proceed to "Settled" until materialisation completes
    IF cost_impact = 0 (time-only EOT VO):
      → Skip materialisation workflow
      → Execute existing EOT → M03 BaselineExtension path unchanged
      → VO proceeds to Settled via existing workflow

  Partial Approvals (Partially_Approved status):
    IF approved_cost > 0:
      → VOBOQMaterialisation triggered for approved_cost only
      → cost_impact_approved = approved_cost (NOT total_cost)
      → Remaining disputed portion remains in dispute register
      → Materialisation covers only the approved scope
```

---

## BLOCK 7 — Integration Points (Amendment)

**UPDATED/NEW integration points for v2.3:**

| Direction | Module | Data Exchanged | Trigger | Speed Tier |
|-----------|--------|---------------|---------|------------|
| SENDS TO | M02 Structure & WBS | **(NEW v2.3)** `bac_integrity_status = Stale_Pending_VO` for affected package_ids. `vo_id`, `vo_code`, `cost_impact_approved`. | On VO approval with cost_impact > 0 (BR-05-028) | 🔴 Real-time |
| SENDS TO | M02 Structure & WBS | **(NEW v2.3)** Materialisation option + qs_notes: instruction for QS Manager to update BOQ. Confirmed via M02 callback on completion. | On QS Manager starts materialisation (In_Progress) | 🔴 Real-time |
| RECEIVES FROM | M02 Structure & WBS | **(NEW v2.3)** Materialisation completion confirmation: `cost_impact_materialised`, `new_bac_snapshot`, `affected_boq_ids`. | On M02 BAC recalculation after QS update | 🔴 Real-time |
| SENDS TO | M07 EVM Engine | **(NEW v2.3)** `bac_integrity_status` change signals: Stale_Pending_VO (on VO approval) and Confirmed (on materialisation complete). | On VO approval + materialisation completion | 🔴 Real-time |
| SENDS TO | M03 Planning | `BaselineExtension` — auto-created on EOT VO approval (cost_impact = 0). Unchanged. | On EOT VO approval | 🔴 Real-time |
| SENDS TO | M06 Financial | Approved VO cost → contract value adjustment. Approved contingency draw-down → cost entry. LD applied amount. | On VO approval + draw-down approval + LD notification | 🔴 Real-time |

---

## BLOCK 8 — Governance & Audit (Amendment)

New audit entries for materialisation workflow:

| Action | Logged | Field-Level Detail | Visible To | Retention |
|--------|--------|--------------------|-----------|-----------|
| VOBOQMaterialisation created | Yes | vo_id, vo_code, cost_impact_approved, old_bac_snapshot, sla_deadline | PMO Director, Finance Lead, QS Manager | Permanent |
| Materialisation started (In_Progress) | Yes | vo_id, option_selected, qs_notes, started_by | PMO Director, QS Manager | Permanent |
| Materialisation completed | Yes | vo_id, cost_impact_materialised, new_bac_snapshot, bac_delta_actual, delta_variance, materialised_by | PMO Director, Finance Lead | Permanent |
| BAC delta mismatch flagged | Yes | vo_id, approved_amount, materialised_amount, variance, flag_reason | PMO Director, Finance Lead | Permanent |
| Materialisation SLA breach (48hr) | Yes | vo_id, elapsed_time, escalation_to | PMO Director | Permanent |
| Materialisation governance breach (72hr) | Yes | vo_id, full timeline, breach_log_id | PMO Director, Portfolio Manager | Permanent |

---

## BLOCK 9 — Explicit Exclusions (Amendment — additions)

**Added to existing exclusions:**

```
[ ] Execute BOQ item creation or quantity revision            → M02 (QS Manager acts in M02)
[ ] Recalculate BAC after BOQ update                         → M02 owns BAC recalculation
[ ] Lift EAC suspension in M07                               → M07 lifts on receipt of Confirmed signal from M02
[ ] Approve the materialisation scope                        → PMO Director approves the VO; QS implements in M02
[ ] Track the financial payment of the approved VO amount    → M06 owns payment workflow
```

---

## BLOCK 10 — Open Questions

**All questions resolved. Zero open questions.**

| # | Question | Resolution |
|---|----------|-----------|
| 1 | What happens if QS creates wrong BOQ items and needs to undo materialisation? | Materialisation completion sets bac_integrity_status = Confirmed. If QS made errors in M02 BOQ, they must be corrected via a standard M02 Structural Variation (BR-02-011), which creates a new BACIntegrityLedger entry and returns to Confirmed state after correction. Materialisation itself cannot be reversed. |
| 2 | Can a VO be Settled without materialisation completing? | No. BR-05-028 blocks VO status from reaching Settled until BOQ_Materialisation_Complete. PMO Director can force-settle with governance override + permanent log, but bac_integrity_status remains Stale_Pending_VO until M02 is manually updated. |
| 3 | Time-only VOs (EOT) — no materialisation needed? | Confirmed. cost_impact = 0 routes directly to M03 BaselineExtension. No materialisation workflow. |
| 4 | What is the audit trail if approved VO cost and BAC change don't match exactly? | delta_variance field captures the gap. Flagged if > ₹10,000. Decision Queue item for PMO Director review. BACIntegrityLedger records both expected and actual BAC delta permanently. |
