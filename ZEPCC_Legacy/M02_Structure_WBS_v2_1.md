# M02 — Structure & WBS
## Module Specification v2.1
## AMENDMENT — Changed Blocks Only
**Status:** Draft — Pending Review | **Locked:** No
**Spec Author:** PMO Director | **Date:** 2026-05-02
**Reference Standards:** EPCC_Standards_Memory_v5_0.md
**Base Version:** M02_Structure_WBS_v2.0
**Amendment Scope:** GAP-02 resolution — BAC integrity status field on Package.
                     BACIntegrityLedger entity (owned jointly with M07). Materialisation
                     workflow receiving-end rules. ID chain validation extended.

> **HOW TO READ THIS FILE:**
> This is an amendment document. All blocks not listed here remain
> unchanged from M02_Structure_WBS_v2.0.
> Apply these changes on top of v2.0 to produce the complete v2.1 spec.

---

## CHANGE LOG

| Version | Date | Change Summary |
|---------|------|---------------|
| v2.0 | 2026-04-30 | Full spec: BOQ-WBS many-to-many; unit master 3-tier; template versioning; CSV import |
| v2.1 | 2026-05-02 | GAP-02: bac_integrity_status added to Package entity. bac_integrity_status added to BOQItem. VOBOQMaterialisation receiving-end workflow added. BR-02-028 through BR-02-034 added. Block 7 updated with M05 and M07 integration. |

---

## BLOCK 2 — Scope Boundary (Updated)

**ADDITIONS to INCLUDES:**

| INCLUDES (New) | Rationale |
|----------------|-----------|
| BAC integrity status tracking per package — `bac_integrity_status` field | GAP-02: M02 is the source of BAC. M02 must signal when BAC is stale due to pending VO materialisation. |
| VOBOQMaterialisation receiving-end workflow — QS updates BOQ and confirms to M05/M07 | GAP-02: M02 executes the actual BOQ update when QS Manager acts. Confirms completion back to M05. |
| `BACIntegrityLedger` — append-only audit of every BAC change | GAP-02: Permanent forensic record of every BAC mutation. |

**ADDITION to EXCLUDES:**

| EXCLUDES (Clarification) |
|--------------------------|
| Initiating the VO materialisation workflow → M05 owns trigger, workflow creation, and SLA governance |
| EAC suspension logic → M07 owns EAC calculations and suspension |

---

## BLOCK 3 — Data Architecture (Amendment)

### 3a. New and Updated Entities

| Entity | Change | Description |
|--------|--------|-------------|
| `Package` | Updated | `bac_integrity_status` field added |
| `BOQItem` | Updated | `pending_vo_id` field added — links to VO that is pending materialisation |
| `BACIntegrityLedger` | New | Append-only audit trail of every BAC change. Jointly referenced by M07 but owned here as M02 is the source of BAC. |

---

### 3b. Updated Fields — Entity: `Package`

**Fields ADDED to existing Package entity:**

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `bac_integrity_status` | ENUM | Y | **(NEW)** `Confirmed / Stale_Pending_VO`. Default = `Confirmed` at package creation. | SYSTEM |
| `pending_vo_id` | UUID | N | **(NEW)** FK → M05 VariationOrder. Populated when bac_integrity_status = Stale_Pending_VO. Cleared on Confirmed. | LINK → M05 VariationOrder |
| `bac_stale_since` | TIMESTAMP | N | **(NEW)** Populated when bac_integrity_status transitions to Stale_Pending_VO. Cleared on Confirmed. | SYSTEM |
| `last_bac_confirmed_at` | TIMESTAMP | Y | **(NEW)** Timestamp of last BAC confirmation. Updated each time bac_integrity_status → Confirmed. | SYSTEM |
| `bac_version` | INTEGER | Y | **(NEW)** Increments every time BAC changes. Starts at 1 on package creation. Enables M07 to detect BAC changes without full recalculation. | SYSTEM |

---

### 3b. Updated Fields — Entity: `BOQItem`

**Fields ADDED to existing BOQItem entity:**

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `pending_vo_materialisation_id` | UUID | N | **(NEW)** FK → M05 VOBOQMaterialisation. Set when a VO materialisation is in-progress or pending for this item. Cleared on Confirmed. | LINK → M05 VOBOQMaterialisation |
| `bac_contribution_confirmed` | BOOLEAN | Y | **(NEW)** Default true. Set false when this item's quantity/rate is under VO materialisation review. Set true on materialisation completion. | SYSTEM |

---

### 3b. New Entity Fields — `BACIntegrityLedger`

*(Owned by M02 — M07 reads this. Same entity defined in Standards Memory §7.90 and M07 v3.0 for reference.)*

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `ledger_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | LINK → M01 Project |
| `package_id` | UUID | Y | — | LINK → Package |
| `change_type` | ENUM | Y | `VO_Materialisation / Baseline_Revision / Correction / Initial_BAC` | SYSTEM |
| `trigger_entity` | VARCHAR(50) | Y | e.g., "VOBOQMaterialisation", "BaselineExtension", "BOQItem_Manual" | SYSTEM |
| `trigger_id` | UUID | Y | FK → the trigger entity record | LINK |
| `old_bac` | DECIMAL(15,2) | Y | Package BAC before this change. Captured at trigger time. | SYSTEM |
| `new_bac` | DECIMAL(15,2) | Y | Package BAC after this change — confirmed. | CALC |
| `bac_delta` | DECIMAL(15,2) | Y | CALC = new_bac − old_bac | CALC |
| `changed_by` | UUID | Y | FK → Users | LINK → Users |
| `changed_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `audit_note` | TEXT | N | Free text context. Auto-populated for VO materialisation: "VO {vo_code}: option {A/B/C}" | SYSTEM or INPUT |

**BACIntegrityLedger is IMMUTABLE.** No `is_active`, no `updated_at`, no soft delete. Append-only.
Written once on every BAC change. Never modified.

---

## BLOCK 6 — Business Rules (Amendment — new rules v2.1)

*All existing rules BR-02-001 through BR-02-027 from v2.0 remain in force.*
*The following rules are ADDED in v2.1:*

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---------|---------|-------|--------|------------|
| BR-02-028 | M05 sends `bac_integrity_status = Stale_Pending_VO` signal for affected package_ids | Received from M05 on VO approval with cost_impact > 0 | For each affected package: set `Package.bac_integrity_status = Stale_Pending_VO`. Set `Package.pending_vo_id = vo_id`. Set `Package.bac_stale_since = NOW()`. Set `BOQItem.bac_contribution_confirmed = false` for items within VO scope. Set `BOQItem.pending_vo_materialisation_id = materialisation_id`. | 🔴 Real-time |
| BR-02-029 | QS Manager initiates BOQ update for VOBOQMaterialisation (In_Progress) | Received from M05 when QS starts materialisation | Unlock affected BOQItems for editing (bac_contribution_confirmed = false = editable). Package BAC recalculation deferred during materialisation (do not update BAC mid-edit — only on finalisation). | 🔴 Real-time |
| BR-02-030 | QS Manager submits materialisation — Option A (Quantity Revision) | BOQ item quantities updated for VO scope | Validate: all updated items have new_quantity > 0. Auto-recalculate `actual_amount = actual_rate × new_quantity` for each item. Auto-recalculate Package BAC = sum of all actual_amounts. BAC change = new_bac − old_bac. | 🔴 Real-time |
| BR-02-031 | QS Manager submits materialisation — Option B (New BOQ Items) | New BOQ items created for VO scope | Validate: all new items have complete ID chain (BOQ_ID → WBS_ID → PKG_ID → CONTRACT_ID → PHASE_ID per ES-DI-001). All new items must have `actual_rate > 0` and `quantity > 0`. Auto-create IDGovernanceLog entries for new items. Package BAC = sum including new items. | 🔴 Real-time |
| BR-02-032 | QS Manager submits materialisation — Option C (Split) | Combination of BR-02-030 and BR-02-031 | Apply Option A logic to revised items AND Option B logic to new items. Validate all in one transaction. All-or-nothing commit: if any item fails validation → roll back all changes, show error list. | 🔴 Real-time |
| BR-02-033 | Materialisation submitted and all validations pass | BOQ updates complete | (1) Recalculate Package.bac_amount. Increment Package.bac_version. (2) Set Package.bac_integrity_status = Confirmed. Clear Package.pending_vo_id and Package.bac_stale_since. Set Package.last_bac_confirmed_at = NOW(). (3) Set all affected BOQItem.bac_contribution_confirmed = true. Clear BOQItem.pending_vo_materialisation_id. (4) Write BACIntegrityLedger entry. (5) Callback to M05: send cost_impact_materialised + new_bac_snapshot + affected_boq_ids. (6) Signal to M07: bac_integrity_status = Confirmed + new BAC values. | 🔴 Real-time |
| BR-02-034 | Package.bac_amount recalculation | Any BOQ item add/edit/quantity change within a package | Recalculate Package.bac_amount = SUM(actual_amount for all active BOQ items in package). If Package.bac_integrity_status = Stale_Pending_VO: do NOT signal M07 yet (materialisation not complete). Only signal M07 on Confirmed state (BR-02-033). | 🔴 Real-time |

---

### Updated Rule — BR-02-009 (Package BAC — updated)

```
BR-02-009 (Package BAC auto-recalculation) — Updated in v2.1:
  Trigger: BOQ item saved (add/edit/delete within package)
  Logic:   Package.bac_amount = SUM(actual_amount) for all active BOQ items in package.
           Package.bac_version incremented.
  Output:  Updated Package.bac_amount.

  ADDITIONAL ROUTING LOGIC (NEW v2.1):
    IF Package.bac_integrity_status = Confirmed:
      → Signal M07 immediately: new BAC value (🔴 Real-time)
    IF Package.bac_integrity_status = Stale_Pending_VO:
      → Do NOT signal M07 yet.
      → BAC recalculation recorded internally only.
      → M07 will receive updated BAC when materialisation completes (BR-02-033).

  Rationale: Prevents M07 from computing EAC on a partially-updated BAC
             during the materialisation workflow.
```

---

### Updated Rule — BR-02-004 (ID Chain Validation — extended for materialisation)

```
BR-02-004 (ID chain completeness) — Updated in v2.1:
  All existing validation unchanged.

  ADDITIONAL RULE FOR MATERIALISATION-CREATED BOQ ITEMS (NEW v2.1):
    New BOQ items created via VOBOQMaterialisation (Option B or C) must:
      (1) Have VO-origin tag: boq_origin = 'VO_Materialisation' (new ENUM value added to BOQ origin field)
      (2) Have materialisation_id linked (from VOBOQMaterialisation)
      (3) Pass full 5-ID chain validation before materialisation can be submitted
    
    If any new BOQ item fails ID chain validation:
      → Full materialisation submission blocked (all-or-nothing per BR-02-032)
      → Error list shown: which items failed which chain link
      → QS Manager must resolve all errors before re-submitting
```

---

## BLOCK 7 — Integration Points (Amendment)

**UPDATED/NEW integration points for v2.1:**

| Direction | Module | Data Exchanged | Trigger | Speed Tier |
|-----------|--------|---------------|---------|------------|
| RECEIVES FROM | M05 Risk & Change | **(NEW v2.1)** `bac_integrity_status = Stale_Pending_VO` signal, `vo_id`, `affected_package_ids`, `materialisation_id`, `cost_impact_approved` | On VO approval with cost_impact > 0 (BR-05-028 fires → M02 receives) | 🔴 Real-time |
| RECEIVES FROM | M05 Risk & Change | **(NEW v2.1)** Materialisation option and scope — instruction for QS to proceed | On VOBOQMaterialisation status → In_Progress | 🔴 Real-time |
| SENDS TO | M05 Risk & Change | **(NEW v2.1)** Materialisation completion confirmation: `cost_impact_materialised`, `new_bac_snapshot`, `affected_boq_ids` | On BR-02-033 (materialisation complete) | 🔴 Real-time |
| SENDS TO | M07 EVM Engine | `package_id`, `bac_amount` — existing signal on BAC recalculation | On every BOQ item save (only when bac_integrity_status = Confirmed — updated per BR-02-009) | 🔴 Real-time |
| SENDS TO | M07 EVM Engine | **(NEW v2.1)** `bac_integrity_status` change: Stale_Pending_VO (on receipt of M05 signal) and Confirmed (on materialisation completion). `bac_version` increment. | On BR-02-028 (Stale) and BR-02-033 (Confirmed) | 🔴 Real-time |
| SENDS TO | M03 Planning | `wbs_id`, `activity_type`, `package_id` — on WBS creation (unchanged) | On baseline lock | 🔴 Real-time |
| SENDS TO | M06 Financial | `boq_id`, `wbs_id`, `package_id`, `actual_rate`, `actual_amount` — unchanged. **NEW: also sends `bac_version` on BAC change so M06 CostBudget stays synchronised.** | On BOQ item save | 🔴 Real-time |

---

## BLOCK 8 — Governance & Audit (Amendment)

New audit entries for BAC integrity tracking:

| Action | Logged | Field-Level Detail | Visible To | Retention |
|--------|--------|--------------------|-----------|-----------|
| Package.bac_integrity_status → Stale_Pending_VO | Yes | package_id, vo_id, bac_at_stale_time, stale_since | PMO Director, Finance Lead | Permanent |
| BOQ items unlocked for materialisation editing | Yes | package_id, materialisation_id, count_of_items_unlocked | PMO Director, QS Manager | Permanent |
| Materialisation BOQ update submitted | Yes | option_selected, items_modified count, items_created count, new_bac, bac_delta | PMO Director, Finance Lead | Permanent |
| Package.bac_integrity_status → Confirmed | Yes | package_id, old_bac, new_bac, bac_delta, confirmed_by, materialisation_id | PMO Director, Finance Lead | Permanent |
| BACIntegrityLedger entry created | Yes | Full ledger entry | PMO Director, Finance Lead, System Admin | Permanent |
| ID chain validation failure during materialisation | Yes | failed_items, missing_chain_links, QS Manager notified | PMO Director, QS Manager | Project lifetime |

---

## BLOCK 9 — Explicit Exclusions (Amendment — additions)

**Added to existing exclusions:**

```
[ ] Trigger the VO materialisation workflow (create VOBOQMaterialisation)  → M05
[ ] SLA governance of materialisation workflow                              → M05 + DecisionQueue
[ ] Suspending or lifting EAC calculations in M07                          → M07 owns EAC logic
[ ] Displaying bac_integrity_status on portfolio dashboard                  → M10 reads M02 via M07 summary
```

---

## BLOCK 10 — Open Questions

**All questions resolved. Zero open questions.**

| # | Question | Resolution |
|---|----------|-----------|
| 1 | Who can edit BOQ items during materialisation? | Only QS Manager (or PMO Director with override). System unlocks only items flagged in the materialisation scope. Other BOQ items remain read-only during this period. |
| 2 | What if QS deletes a BOQ item during materialisation instead of updating it? | Soft delete is permitted — it reduces BAC. The system treats this as a valid materialisation action. BACIntegrityLedger records the BAC reduction. If the deletion causes delta_variance > ₹10,000 vs approved VO cost, PMO Director alert is triggered (BR-05-032 in M05). |
| 3 | Can two concurrent VOs cause simultaneous BAC staleness on the same package? | Yes. Both VOs queue their materialisation workflows. The second VO's materialisation can only start after the first is Complete (bac_integrity_status returns to Confirmed). System enforces: a package with bac_integrity_status = Stale_Pending_VO cannot receive a second Stale signal until first is resolved. The second VO's workflow enters Pending_Queue state. |
| 4 | What is the `boq_origin` field — is it new? | Yes. BOQItem gets a new field `boq_origin` ENUM: `Manual / CSV_Import / VO_Materialisation / Template_Applied`. Default = Manual. This enables portfolio-level analytics on how much of BOQ came from VO scope additions. |
