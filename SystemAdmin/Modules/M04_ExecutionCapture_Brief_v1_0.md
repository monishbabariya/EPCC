---
artefact: M04_ExecutionCapture_Brief_v1_0
round: 19
date: 2026-05-03
author: Monish (with Claude assist)
x8_version: v0.4
x9_version: v0.2
status: LOCKED
prior_version: ZEPCC_Legacy/M04_Execution_Capture_v2_2.md (amendment-only — base v2.0/v2.1 not in legacy)
---

# M04 — Execution Capture — Brief v1.0

## Purpose

M04 is the **execution-stack data producer** — the module where physical site reality enters EPCC. It captures progress against schedule (% complete per WBS node), construction non-conformances (NCRs), material receipts at site, and contractor performance scoring. M04 is the foundational consumer of M01 (project frame) + M02 (WBS) + M03 (schedule) and the foundational producer for M06 (billing), M07 (Earned Value), and M14 (measurement book).

**Decision M04 enables:** *"Is what's actually happening on site matching what was planned, and where it isn't, what is the commercial and schedule consequence?"*

## Scope (this round)

This Brief locks the eight OQ-1 architectural decisions and five OQ-2 pattern defaults that the M04 Spec (Round 20) will rest on. **All thirteen are CLOSED** in this Brief — the Spec can be authored without re-opening any of them.

**In scope:**
- ProgressEntry (WBS-node grain) with three-state approval flow
- ConstructionNCR (4-tier severity, contractor-attributable, LD-signal-emitting)
- MaterialReceipt (site goods receipt; feeds M03 procurement timing + M06 GRN trigger)
- ContractorPerformanceScore (Phase 1 implementation; M30 takes over Phase 2)

**Explicitly NOT in scope (decided OQ-1.1 = B):**
- DLPRegister + DLPDefect → moved to **M15 HandoverManagement** (DLP is a handover-period concern; lives where the rest of the handover lifecycle lives)
- HSE incidents → moved to **M31 HSESafetyManagement** (safety has its own governance system; HSE-in-M04 was a legacy bundle)
- BOQ-item-grain measurement → **M14 QSMeasurementBook** (single-owner: M04 reports % at WBS-node grain for EVM; M14 owns BOQ-line measurement for billing)
- Document/photo storage → **M12 DocumentControl** (M04 stores `document_id` references, not URLs)
- Daily site diary → **M16 SiteDiary** (separate registry entry already exists)

## Prior Art

**Legacy reference:** `ZEPCC_Legacy/M04_Execution_Capture_v2_2.md`

Caveat: only the v2.2 amendment file exists in legacy (added DLPRegister + DLPDefect). The v2.0 / v2.1 base specs are not in `ZEPCC_Legacy/`. The full M04 scope was reverse-engineered from:
- v2.2 amendment (DLP + ProgressEntryApproval reference to v2.1)
- M01 / M02 / M03 cross-references (what they SEND TO and RECEIVE FROM M04)
- M07 v3.0 legacy (what M07 expects M04 to expose)

**Key drift from legacy:**

| Legacy (v2.2) | This Brief (v1.0) | Why |
|---|---|---|
| ProgressEntryApproval two-state (Draft → Approved) | Three-state (Draft → Submitted → Approved) | OQ-1.3 — separate contractor declaration from EPCC acceptance for billing-dispute audit trail |
| DLPRegister + DLPDefect inside M04 | Moved to M15 HandoverManagement | OQ-1.1 — single-owner discipline; handover concerns live in handover module |
| HSE incidents inside M04 | Moved to M31 HSESafetyManagement | OQ-1.1 — safety has its own governance system |
| Photo URLs stored directly on entities | M12 `document_id` references (with MinIO direct-URL stub until M12 lands) | OQ-1.7 — single-owner for document storage |
| Approval authority undefined in legacy | QS_MANAGER ≤ ₹50 lakh; QS_MANAGER + PROJECT_DIRECTOR > ₹50 lakh (configurable) | OQ-1.4 — explicit dual sign-off threshold |
| NCR severity tiers — implicit | Locked at 4 tiers (Critical/High/Medium/Low) — symmetric with DLPDefect + Severity ENUM (X8) | OQ-1.5 |

---

## OQ-1 — Design Decisions Required From User

> All eight decisions are **CLOSED** in this Brief. The M04 Spec (Round 20) will reference these by ID without re-opening.

### OQ-1.1 — Module scope decomposition

**Question:** What does M04 ExecutionCapture include, and what gets split to neighbouring modules?

**Options:**
- A. Keep all six legacy concerns bundled (progress + NCR + DLP + materials + HSE + contractor scoring)
- B. Slim core (progress + NCR + materials + contractor scoring); DLP → M15; HSE → M31
- C. Slim core + decision deferred until M15 / M31 are ready

**Resolution:** **B (LOCKED).** M04 stays focused on the EV-feeding loop. DLP and HSE have separate registry homes; bundling them into M04 was a legacy artefact. Each will be properly specced in their own brief later.

**Cascade impact:**
- M15 HandoverManagement Brief (future round) will absorb DLPRegister + DLPDefect + the v2.2 amendment content
- M31 HSESafetyManagement Brief (future round) will absorb HSE incident capture
- M04 v1.0 Spec is materially smaller than legacy v2.2 — easier to lock cleanly
- No active cascade to M01/M02/M03 (their integration points to M04 cover only progress + materials + contractor scoring already)

**Status:** CLOSED

---

### OQ-1.2 — Progress measurement methods + grain

**Question:** What progress measurement methods does M04 support, and at what grain?

**Options:**
- A. 4 methods (Units / Steps / Milestone / Subjective_Estimate) at WBS-node grain only
- B. 4 methods at WBS + BOQ-item grain (granular for QS)
- C. 4 methods at WBS-node grain; M14 QSMeasurementBook owns BOQ-item grain

**Resolution:** **C (LOCKED).** Single-owner discipline (F-005). M04 measures progress at WBS-node grain — feeds M07 EVM correctly. M14 (when built) owns BOQ-item-grain measurement for billing.

**Cascade impact:**
- New X8 ENUM **`ProgressMeasurementMethod`** = `Units / Steps / Milestone / Subjective_Estimate` (proposed v0.5 cascade)
- New X8 ENUM **`EVConfidence`** = `High / Low / Fallback / Derived` (carried from legacy M07 v3.0; locked here for forward-traceability)
- M14 Brief (future round) must cite OQ-1.2 = C explicitly to confirm the grain split

**Status:** CLOSED

---

### OQ-1.3 — Progress entry approval flow

**Question:** Two-state (Draft → Approved) or three-state (Draft → Submitted → Approved) approval?

**Options:**
- A. Two-state (legacy v2.1 amendment)
- B. Three-state — explicit Submitted handoff between contractor and EPCC

**Resolution:** **B (LOCKED).** Three-state captures the contractor-declares vs EPCC-accepts boundary, which matters for billing disputes (M06) and EVM provenance (M07). Two-state conflates them.

**Cascade impact:**
- New X8 ENUM **`ProgressApprovalStatus`** = `Draft / Submitted / Approved / Rejected` (v0.5 cascade)
- M07 v3.0 legacy referenced `progress_approval_status` Draft/Approved — the Spec must note that legacy v3.0 was authored against a 2-state model and now consumes the 3-state model unchanged (Approved still means Approved; Draft still means "do not consume for EV"; Submitted is invisible to M07 for EV computation but visible for audit)
- M06 reads the Approved transition for billing trigger; Rejected re-opens the cycle
- New BR around 24/48hr SLAs for contractor → submitted, submitted → approved transitions

**Status:** CLOSED

---

### OQ-1.4 — Approval authority

**Question:** Who Approves a progress entry?

**Options:**
- A. PROJECT_DIRECTOR only
- B. QS_MANAGER alone (single sign-off)
- C. QS_MANAGER alone ≤ threshold; QS_MANAGER + PROJECT_DIRECTOR > threshold (dual sign-off)
- D. Configurable per project

**Resolution:** **C (LOCKED).** Threshold defaults to **₹50 lakh of WBS-node BAC slice** (configurable per project in `Project.dual_signoff_threshold_inr` field — pending M01 v1.3 cascade note OR ProjectConfig table to be specced in M04). Below threshold: QS_MANAGER alone. Above threshold: dual sign-off.

**Cascade impact:**
- M01 v1.3 cascade note **OR** M04-owned `ProjectExecutionConfig` entity (decision deferred to Spec round). Recommend latter to avoid further M01 cascade.
- M07 EV computation reads `ProgressEntry.approved_at` regardless of which path approved it — single approval surface, dual-pathway internally
- M06 billing trigger fires on `Approved` regardless of single/dual path

**Status:** CLOSED

---

### OQ-1.5 — Construction NCR severity tiers

**Question:** How many severity tiers for ConstructionNCR?

**Options:**
- A. 4-tier (Critical / High / Medium / Low) — matches DLPDefect + X8 Severity ENUM
- B. 3-tier (Critical / Major / Minor) — common Indian construction practice

**Resolution:** **A (LOCKED).** Symmetry with DLPDefect (when M15 specs it later) and with the system-wide `Severity` ENUM in X8 v0.4. Single mental model across the platform.

**Cascade impact:**
- Reuse existing X8 `Severity` ENUM — no new ENUM needed (deprecates one open question)
- LD-eligibility logic in M05 (when built) will key off this 4-tier severity

**Status:** CLOSED

---

### OQ-1.6 — NCR commercial coupling

**Question:** Does a Critical/High NCR auto-affect M05 LD calculation, or only via PMO-flagged designation?

**Options:**
- A. Auto-feed M05 LD calc when severity = Critical/High AND not closed within X days
- B. M04 reports all NCRs faithfully; M05 owns the LD-eligibility decision

**Resolution:** **B (LOCKED).** Separation of duties. M04 captures faithfully; M05 (when built) decides commercial consequence. Auto-coupling creates fragile spec interlocks.

**Cascade impact:**
- M04 emits `NCR_RAISED` and `NCR_STATUS_CHANGED` audit events to M05 (when M05 specced)
- M05 Spec (future round) must define LD-eligibility rules, not M04
- No M04 BR for "auto-impose LD" — M04 has zero commercial logic

**Status:** CLOSED

---

### OQ-1.7 — Photo evidence storage

**Question:** Where do progress / NCR / material-receipt photos live?

**Options:**
- A. MinIO direct URLs stored on M04 entity fields (legacy implicit pattern)
- B. M12 DocumentControl `document_id` references (single-owner for document storage)

**Resolution:** **B (LOCKED) with stub allowance.** Final design uses `document_id` FK to M12. Until M12 is specced + built, M04 v1.0 carries a `photo_urls JSONB` field that stores MinIO URLs directly **as a documented stub**. Spec v1.1 cascade (when M12 lands) will migrate URLs → document_id and add a one-time migration script.

**Cascade impact:**
- M12 Brief (future round) must accept incoming migration from M04 stub field
- Migration script: `20260XXX_M12_absorb_M04_photo_urls.py` — drafted in M04 Spec but executed when M12 is live
- M04 Spec audit-events catalogue includes `PHOTO_ATTACHED` event for the stub period

**Status:** CLOSED

---

### OQ-1.8 — Role-default views per X9 v0.2 §13.3.3

**Question:** What is each role's primary + secondary chart view in M04?

**Options:**
- (a) Mapping below
- (b) Different mapping

**Resolution:** **Mapping (a) LOCKED:**

| Role | Primary view | Secondary view |
|---|---|---|
| `SITE_MANAGER` | Today's progress entries (data-entry surface, not chart) | 4-week look-ahead Gantt with site-relevant WBS slice (link to M03) |
| `PROJECT_DIRECTOR` | Project progress dashboard — % complete heatmap by WBS | NCR pipeline funnel (X9 flagship pattern §11) |
| `QS_MANAGER` | **Pending approvals queue** ⭐ (M04's primary QS surface) | Measurement variance — declared vs verified % delta |
| `PMO_DIRECTOR` | NCR pipeline funnel (X9 flagship §11) | Material receipts vs procurement schedule variance (link to M03) |
| `PROCUREMENT_OFFICER` | Material receipts log + receipt-vs-PO variance | Long-lead item tracking (link to M03) |
| `ANALYST` | Progress trend curves (S-curve actual vs planned) | NCR rate trend |
| `READ_ONLY` | Project progress card (status badges, no approval actions) | — |

**Cascade impact:**
- X9 v0.3 cascade — add M04 row to §13.3.3 role-default views table (cascade note pattern; surgical change)
- NCR pipeline funnel is the **eighth instance** of the flagship X9 pipeline pattern (per X9 v0.2 §11 list: M06 Capital Funnel, M04 NCR (this), M05 Risk, M05 VO, M09 Compliance, M11 Action, M15 Defect, HDI Import) — confirms M04's pattern as already locked in X9

**Status:** CLOSED

---

## OQ-2 — Pattern Defaults (Claude recommended; user confirmed)

### OQ-2.1 — Audit event naming discipline

**Default:** Lock the proposed audit event names in this Brief (Appendix A) so the Spec carries them as locked from authoring — avoids retro-cascade like the M03 Round 18 pattern.

**Reasoning:** M03 v1.1 cascade in Round 18 absorbed 26 retroactively-locked event names. Round 18 audit locked the principle: surgical changes → cascade note; substantive → re-issue. Authoring events as LOCKED in the Brief makes the Spec a re-statement, not a re-issue.

**Override risk:** None material. If user prefers to defer until X3 Audit Event Catalogue lands, names move from M04 Spec Appendix to X3 unchanged.

**Status:** CLOSED — proceed with lock-in-Brief

### OQ-2.2 — Append-only ledgers

**Default:** Following entities are append-only (DB-level UPDATE/DELETE forbidden — same pattern as M02 BACIntegrityLedger):
- `ProgressEntryAudit` — every state transition (Draft → Submitted → Approved → Rejected)
- `NCRStatusLog` — every NCR state transition + severity change
- `MaterialReceiptLedger` — every receipt event with QC decision
- `ContractorPerformanceScoreLog` — every quarterly score change with rationale

**Reasoning:** Provenance is the value. Audits / disputes need the unaltered trail.

**Status:** CLOSED

### OQ-2.3 — Photo evidence minimums + format

**Default:**
- Critical NCR: ≥ 2 photos required to save
- High NCR: ≥ 1 photo required
- Medium / Low NCR: photo encouraged, not required
- Material receipt with quantity > ₹10 lakh value: ≥ 1 photo required (covers high-value LINAC, MRI, etc. for KDMC)
- Format: JPEG / PNG, max 10 MB per file, max resolution 4K (auto-downscaled in storage)
- All photos via M12 (or MinIO stub per OQ-1.7)

**Reasoning:** Indian healthcare audit context — NABH inspectors often request photo evidence. ₹10 lakh threshold catches high-value medical equipment without overburdening routine consumables.

**Override risk:** Stricter thresholds = higher save friction; looser = thin evidence trail.

**Status:** CLOSED

### OQ-2.4 — Decision Queue SLA defaults

**Default:**

| Trigger | Severity | Owner | SLA |
|---|---|---|---|
| `NCR_OPEN_CRITICAL` | Critical | PROJECT_DIRECTOR | 24 hr |
| `NCR_OPEN_HIGH` | High | PROJECT_DIRECTOR | 48 hr |
| `PROGRESS_APPROVAL_PENDING` | Medium | QS_MANAGER | 48 hr |
| `MATERIAL_RECEIPT_QC_FAIL` | High | PROCUREMENT_OFFICER | 24 hr |
| `DUAL_SIGNOFF_PENDING` | Medium | PROJECT_DIRECTOR | 48 hr |
| `CONTRACTOR_SCORE_DECLINE` | Medium | PMO_DIRECTOR | 7 days (quarterly review) |

**Reasoning:** Aligns with M03 BR-03-016 (procurement SLAs) and Round 18 cascade-pattern Decision Queue conventions.

**Status:** CLOSED

### OQ-2.5 — Speed tier defaults

**Default:**

| Event class | Speed tier |
|---|---|
| Progress entry create / Submit / Approve / Reject | 🔴 Real-time |
| NCR create / status change | 🔴 Real-time |
| Material receipt create | 🔴 Real-time |
| Photo attachment | 🔴 Real-time |
| Daily NCR/material sweep (overdue checks) | 🟢 24 hr |
| Contractor performance score recalculation | 🟢 24 hr (quarterly batch) |
| M01 Party.long_term_rating cascade | 🟢 24 hr (quarterly batch — confirms M01 v1.0 BR-01-019 cadence) |

**Status:** CLOSED

---

## Design Sketch

### Core entities (Spec Round 20 will detail; Brief locks the shape)

| Entity | Cardinality | Owner | Purpose |
|---|---|---|---|
| `ProgressEntry` | Many per WBS node per period | M04 | The single source of truth for "what % of this WBS work is done." Three-state lifecycle with full audit trail. |
| `ProgressEntryAudit` | Many per ProgressEntry | M04 (append-only) | Every state transition recorded. Provenance for M07 EV computation + M06 billing. |
| `ProgressMeasurementConfig` | 1 per WBS node | M04 | Locks which measurement method (Units / Steps / Milestone / Subjective_Estimate) applies to this node. Cannot change after first ProgressEntry. |
| `ConstructionNCR` | Many per WBS node | M04 | Non-conformance during construction (pre-SG-11). 4-tier severity. Reports faithfully to M05 (when built); no LD logic in M04. |
| `NCRStatusLog` | Many per NCR | M04 (append-only) | Every state transition. |
| `MaterialReceipt` | Many per ProcurementScheduleItem (M03) | M04 | Goods receipt at site. Triggers M03 `actual_delivery_date` populate + M06 GRN signal (when built). |
| `MaterialReceiptLedger` | Many per receipt | M04 (append-only) | Every QC decision and receipt event. |
| `ContractorPerformanceScore` | 1 per Contractor (Party) per quarter | M04 (Phase 1) | Weighted score from progress adherence, NCR rate, material acceptance rate. Feeds M01.Party.long_term_rating quarterly. M30 takes ownership Phase 2. |
| `ContractorPerformanceScoreLog` | Many per score change | M04 (append-only) | Provenance trail for the rating cascade to M01. |

### State machines

**ProgressEntry:**
```
Draft ──(submit)──> Submitted ──(approve)──> Approved
  ▲                     │
  │                     └──(reject)──> Rejected ──(re-submit)──> Submitted
  └─(cancel by contractor before submit, never after)
```

**ConstructionNCR:**
```
Open ──(response)──> Response_Received ──(remediation_start)──> Remediation_In_Progress
                                                                       │
              ┌──(reinspection_pass)──> Closed                         │
              │                                                         │
Reinspection_Pending ◄────────(remediation_complete)───────────────────┘
              │
              └──(reinspection_fail)──> Remediation_In_Progress  (loop)
```

**MaterialReceipt:**
```
Received ──(qc_pass)──> Accepted ──(GRN_signal_to_M06)──> Closed
   │
   └──(qc_fail)──> Rejected ──(return)──> Closed
                       │
                       └──(rework_proposed)──> Conditional_Acceptance ──(re_qc_pass)──> Accepted
```

### Integration map

**M04 receives from:**

| From | Data | Trigger | Speed |
|---|---|---|---|
| M01 | `project_id`, `current_phase`, `report_date`, `contract_id`, `Party` (contractor identity), `min_wbs_depth` | On project state change | 🔴 |
| M02 | `wbs_id`, `package_id`, `bac_per_node`, `bac_integrity_status` | On WBS create/update | 🔴 |
| M03 | `wbs_id` planned dates, `procurement_schedule_item_id`, `latest_order_date`, `look_ahead_window_weeks` | On schedule create + look-ahead refresh | 🔴 |
| M34 | Auth, role, project scope, photo permissions per role | Every API call | 🔴 |

**M04 sends to:**

| To | Data | Trigger | Speed |
|---|---|---|---|
| M03 | `MaterialReceipt.actual_delivery_date` → ProcurementScheduleItem.actual_delivery_date | On material receipt | 🔴 |
| M03 | `ProgressEntry.actual_start` / `actual_finish` → ScheduleEntry.actual_* | On first/last Approved progress entry per WBS | 🔴 |
| M07 EVM (when built) | `pct_complete_reported` + `progress_approval_status` + `pct_complete_draft` per WBS | On every Approved progress entry | 🔴 |
| M05 Risk (when built) | `NCR_RAISED` + `NCR_STATUS_CHANGED` events | On NCR create + status change | 🔴 |
| M06 Financial (when built) | `Approved` progress milestone trigger; `MaterialReceipt` GRN signal | On approval + receipt | 🔴 |
| M01 | `Party.long_term_rating` update from contractor performance | Quarterly batch | 🟢 |
| M11 ActionRegister (when built) | Decision Queue triggers (NCR_OPEN_CRITICAL, etc.) | On condition match | 🔴 / 🟢 |

### What this Brief does NOT cover

- DLP scope (deferred to M15 HandoverManagement Brief)
- HSE scope (deferred to M31 HSESafetyManagement Brief)
- BOQ-item-grain measurement (deferred to M14 QSMeasurementBook Brief)
- Document storage internals (M12 DocumentControl owns)
- Daily site diary (M16 SiteDiary owns)
- Stage gate logic (M08 owns; M04 only reports state, M08 reads to gate-block)

---

## Open Items Tracker

| ID | Topic | Type | Status |
|---|---|---|---|
| OQ-1.1 | Module scope — slim core (B) | User Decision | **CLOSED** |
| OQ-1.2 | Methods + grain — WBS-node only (C) | User Decision | **CLOSED** |
| OQ-1.3 | Approval flow — three-state (B) | User Decision | **CLOSED** |
| OQ-1.4 | Approval authority — dual above ₹50L (C) | User Decision | **CLOSED** |
| OQ-1.5 | NCR severity — 4-tier (A) | User Decision | **CLOSED** |
| OQ-1.6 | NCR commercial coupling — separation of duties (B) | User Decision | **CLOSED** |
| OQ-1.7 | Photo storage — M12 with MinIO stub (B) | User Decision | **CLOSED** |
| OQ-1.8 | Role-default views — proposed mapping | User Decision | **CLOSED** |
| OQ-2.1 | Lock audit events in Brief | Pattern Default | **CLOSED** |
| OQ-2.2 | Append-only ledgers (4 entities) | Pattern Default | **CLOSED** |
| OQ-2.3 | Photo minimums + format | Pattern Default | **CLOSED** |
| OQ-2.4 | Decision Queue SLA defaults | Pattern Default | **CLOSED** |
| OQ-2.5 | Speed tier defaults | Pattern Default | **CLOSED** |

**Lock criterion met:** All 13 items CLOSED. Brief LOCKED.

---

## Cascade Notes (for Spec round 20)

The M04 Spec Round 20 will produce / require:

| Cascade | Type | Target | Notes |
|---|---|---|---|
| **X8 v0.5 cascade** | New ENUMs | `X8_GlossaryENUMs_v0_5.md` | Add: `ProgressMeasurementMethod` (4 values), `ProgressApprovalStatus` (4 values incl. Rejected), `EVConfidence` (4 values — carried forward from M07 v3.0 legacy for forward-traceability), `NCRStatus` (state machine), `MaterialReceiptStatus` (state machine), `MaterialQCDecision` enum |
| **X9 v0.3 cascade** | Role-default views update | `X9_VisualisationStandards_Spec_v0_3.md` | Add M04 row to §13.3.3 table per OQ-1.8. NCR pipeline funnel confirmed as 8th flagship-pattern instance (already in §11). |
| **M01 → M04 already locked** | Existing | M01 Spec already references M04 for `Party.long_term_rating` cascade and project soft-delete dependency check | No new M01 cascade. |
| **M04 Spec Appendix A — Audit Events Catalogue** | New section | M04 Spec | Per OQ-2.1 — lock event names from authoring. Estimated 18–22 events (3 ProgressEntry transitions × 4 audit hooks + 5 NCR + 4 Material + 2 Contractor scoring + system events). |
| **Project-config storage decision** | Spec-round decision | M04 Spec OQ-2.6 | OQ-1.4's ₹50L threshold needs a home: M01 v1.3 cascade note OR M04 `ProjectExecutionConfig` entity. Recommend latter — avoids further M01 churn. Spec round will surface as OQ-2.6 with my recommendation pre-set. |
| **Photo migration to M12** | Future cascade | M04 Spec v1.1 (when M12 lands) | One-time migration script drafted; executed when M12 v1.0 ready. |

### Modules unblocked by M04 lock

- **M14 QSMeasurementBook** — needs M04's WBS-grain progress before specifying BOQ-line measurement
- **M06 FinancialControl** — needs M04 Approved-progress trigger for billing milestone logic
- **M05 Risk & VO** — needs M04 NCR feed for LD-eligibility logic
- **M07 EVMEngine** — needs M04's `pct_complete_reported` + `progress_approval_status` for EV computation
- **M15 HandoverManagement** — needs M04 ConstructionNCR closed-set as pre-DLP baseline
- **M31 HSESafetyManagement** — independent of M04 lock, but M04 OQ-1.1 = B clears the scope boundary

---

*v1.0 — Brief LOCKED. All 13 OQ items CLOSED. Ready for Round 20 Spec authoring.*
