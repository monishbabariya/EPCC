---
artefact: M06_FinancialControl_Brief_v1_0
round: 24
date: 2026-05-03
author: Monish (with Claude assist)
x8_version: v0.5
x9_version: v0.3
status: LOCKED
prior_version: ZEPCC_Legacy/M06_Financial_Control_v2_1.md
locked_at: 2026-05-03 (Round 24 user confirmation; pre-merge round number was 23 — renumbered to 24 post-merge to avoid collision with main's Round 23 = EPCC_BuildArchitecture Brief)
---

# M06 FinancialControl — Brief v1.0

## 1. Purpose

M06 owns the project's actual-cost ledger and the four-state financial-control pipeline (`Budgeted → Committed → Accrued → Paid`) locked in `architecture.md`. It enables the FINANCE_LEAD to answer: **at this report date, where exactly is each rupee of the BAC inside the funnel, and what is the headroom remaining at each state?** Every other module is a producer or reader of the M06 ledger — M07 EVM consumes AC, M10 Command surfaces aggregates, M01 reads payment status into project RAG. M06 is the single legal source of truth for AC.

## 2. Scope (this round)

### In Scope

- `CostLedgerEntry` — the AC backbone, one immutable row per state-transition event. Drives M07 AC, M10 cash position.
- Four-state pipeline machine — `Budgeted → Committed → Accrued → Paid` (architecture.md locked).
- `PurchaseOrder` — vendor identity (the M03 → M06 ownership boundary explicitly locked in M03 BR-03-022 + Block 9). Contains rate, currency, and payment terms.
- `RABill` — contractor running-account bill, triggered on M04 `BILLING_TRIGGER_READY` (M04 BR-04-012). Drives Accrued.
- `GRNLedger` — material goods-received-note, driven by M04 `MATERIAL_GRN_EMITTED` (M04 BR-04-028). Drives material Committed→Accrued.
- `RetentionLedger` — withheld retention amounts; tranches for SG-11 (substantial completion) vs DLP-end release. Per legacy v2.1, DLP-end release is gated by M04 (`DLPRegister.open_defect_count`) and M09 (Non_Compliance count).
- `Cashflow forecast` — projected AC × period × WBS. Period boundaries read from M03 `LookAheadConfig.reporting_period_type` (per M01 v1.2 cascade — M03 owns the field).
- `VOIngestion` — receives Approved VO commitments from M05 (when built); creates Committed entries; respects M02 BACIntegrityLedger contract.
- Decision Queue triggers — capital-headroom breach, BG expiry, retention-release blocking, payment SLA breach, forex deviation.
- Audit-events catalogue (locked from authoring per Round 18 cascade-pattern discipline).
- Append-only ledgers with DB-level UPDATE/DELETE forbidden (same pattern as M02 BACIntegrityLedger / M04 ProgressEntryAudit).

### Out of Scope (paired with owning module)

- BAC computation per package — owned by **M02** (M06 reads `Package.bac_amount` via internal API; never duplicates).
- BACIntegrityStatus / Stale_Pending_VO mechanics — owned by **M02** (M06 reads, never writes).
- Approved progress percentage — owned by **M04** (M06 receives `BILLING_TRIGGER_READY` signal).
- VO initiation, approval, monetary impact decision — owned by **M05** (M06 receives Approved VO cost-impact signal).
- LD calculation, risk buffer, contingency draw — owned by **M05**.
- EVM computation (CPI/SPI/EAC/ETC/VAC/TCPI) — owned by **M07** (M06 supplies AC; M07 computes).
- Stage-gate decisions and SG-11 passage signal — owned by **M08**.
- DLP defect register and resolution — owned by **M15** HandoverManagement (per M04 OQ-1.1=B re-scope; legacy v2.1 still cited M04 — drift).
- DLP compliance Non_Compliance observations — owned by **M09**.
- BG / insurance certificate identity, expiry tracking, claim workflow — owned by **M23** BGInsuranceTracker (Phase 2). M06 reads BG `is_active` + `coverage_amount` for retention/payment-hold decisioning, but does not own BG records.
- Tendering, vendor pre-qualification — **M29** + **M30** (Phase 2). M06 PurchaseOrder references `Party` from M01 only.
- Document storage (invoices, debit notes, FEMA forms) — **M12 DocumentControl** (when built). M06 stores `document_id` references; MinIO direct-URL stub until M12 lands (same pattern as M04 Block 3b).
- Tax computation engine (GST input credit reconciliation, TDS) — out of v1.0 scope; M06 records GST as captured at PO/invoice; reconciliation deferred to a Phase 2 `TaxLedger` module (legacy v2.1 referenced TaxLedgerEntry — surface as OQ-1).
- Accounting-system bidirectional sync (Tally/SAP/Zoho) — out of v1.0 scope per `accounting_system` field on M01 Project (free-text stub, no integration).

## 3. Prior Art

**Legacy file:** `ZEPCC_Legacy/M06_Financial_Control_v2_1.md` (amendment only — references base v2.0 entities `CommitmentLedger`, `PurchaseOrder`, `RetentionLedger`, `ForexVariation` not present on disk; v2.1 adds `ForexRateMaster` + DLP-release gating).

**Drifts vs current locked state (must be reconciled in Spec):**

| # | Drift | Current Locked Position | Resolution |
|---|---|---|---|
| 1 | Legacy v2.1 routes DLP-defect signals from **M04** DLPRegister | M04 v1.0 (Round 20) excluded DLP — moved to **M15 HandoverManagement** per M04 OQ-1.1=B | M06 v1.0 must consume DLP signals from M15 (when built) — STUB until M15 lands. Same pattern M04 used for M12. |
| 2 | Legacy v2.1 mentions free-text exchange rate; v2.1 amends to ForexRateMaster | Locked-decisions table demands no inline ENUMs and Single-Owner | OQ-1: keep ForexRateMaster in v1.0 vs defer to v1.1. Recommendation: keep, but the entity owns the new `ExchangeRateTier` ENUM (X8 cascade required). |
| 3 | Legacy v2.1 has no audit-events catalogue (locked-from-authoring discipline) | Round 18 cascade-pattern discipline (M03 Appendix C, M04 Appendix A) demands the catalogue at lock time | M06 Spec must ship Appendix A — Audit Events Catalogue (proposed ~25 events). |
| 4 | Legacy v2.1 silent on append-only DB-level enforcement | M02 BACIntegrityLedger + M04 ledgers (4) have explicit `REVOKE UPDATE, DELETE` DB-level enforcement | M06 v1.0 must declare CostLedgerEntry, RetentionLedger, GRNLedger, RABillLedger as append-only with DB-level enforcement (OQ-2). |
| 5 | Legacy v2.1 references `Stale_Pending_VO` flow superficially | M02 v1.0 BAC integrity is fully locked: `bac_integrity_status ENUM (Confirmed / Stale_Pending_VO)`, `pending_vo_id`, M02 owns BACIntegrityLedger | M06 must read M02 BACIntegrityLedger via internal API only (never DB read), and pause new Committed entries against a package that is `Stale_Pending_VO`. Surface as OQ-1. |
| 6 | Legacy v2.1 implicitly assumes M04 `BILLING_TRIGGER_READY` exists | M04 v1.0 BR-04-012 + Appendix A confirm the event is locked-from-authoring | No drift — M06 consumes per locked contract. |
| 7 | Legacy v2.1 references `reporting_period_type` on Project | Removed by M01 v1.2 cascade — now on `LookAheadConfig` (M03-owned) | M06 reads via M03 internal API per F-005. Surface as OQ-2. |
| 8 | Legacy v2.1 has 4 unresolved questions; spec was DRAFT | Phase-1 cadence (C1) requires zero open questions before lock | All 4 legacy items either re-raised here as OQ-1/OQ-2 or marked deferred (Block 10). |

## 4. Predecessor Integration

| Predecessor | What M06 consumes | Mechanism | Speed Tier |
|---|---|---|---|
| M34 | Auth, role, project scope; FINANCE_LEAD MFA enforcement; field-level rate spike formulas (X9 §13.3.6 + cross-cutting-standards.md role mapping); audit log shell | Internal API per F-005 + middleware | T1 (real-time) |
| M01 | `project_id`; per-contract `contract_value_basic`, `gst_rate`, `contract_value_incl_gst`, `mobilisation_advance_pct`, `material_advance_pct`, `retention_pct`, `retention_release_after_dlp`, `dlp_term_days`, `ld_rate_per_week`, `ld_cap_pct`, `risk_buffer_pct`, `payment_credit_days`, `escalation_clause_enabled`, `warranty_period_years`; `Party` master for vendor identity on PurchaseOrder; `KPIThreshold` (Margin band) for RAG | Internal API per F-005 | T1 |
| M02 | `Package.bac_amount` (per-package BAC); `Package.bac_integrity_status` + `pending_vo_id` (block new Committed if Stale_Pending_VO — see OQ-1.4); `BOQItem.actual_rate` + `quantity` (cost basis for accrual at item grain); `BACIntegrityLedger` (read-only audit consumption) | Internal API per F-005 (NEVER DB read) | T1 |
| M03 | `LookAheadConfig.reporting_period_type` (cashflow period boundaries — M01 v1.2 cascade); `PVProfile` per WBS per period (cashflow forecast aligns AC to PV cadence); `ProcurementScheduleItem` (linkage for PurchaseOrder → procurement timing — `m06_po_id` field already exists on M03 ProcurementScheduleItem per M03 Block 3); `Milestone` (financial milestone billing trigger — see OQ-1.3) | Internal API per F-005 + cron/event mix | T1 + T2 (cashflow regen on report_date change) |
| M04 | `BILLING_TRIGGER_READY` event (Approved ProgressEntry per BR-04-012) — drives RABill creation; `MATERIAL_GRN_EMITTED` event (Accepted MaterialReceipt per BR-04-028) — drives GRNLedger entry + Committed→Accrued for material; `entry_value_inr` from approved progress (rate × % × quantity already pre-computed by M04) | Event subscription (internal pub/sub) | T1 (real-time) |

**Future (when built — STUB at M06 v1.0 lock):**

- M05 — Approved VO cost-impact signal (`VO_APPROVED_COST_IMPACT`) → CostLedgerEntry Committed; LD assessment (`LD_ELIGIBLE_AMOUNT`) → CostLedgerEntry deduction tracker.
- M07 — M06 sends AC per WBS per period via internal API; M07 reads (no event needed).
- M08 — `SG_11_PASSAGE` event → RetentionLedger.dlp_period_start populated.
- M15 — `DLP_DEFECT_COUNT_CHANGED` event → RetentionLedger.dlp_release_eligible recompute.
- M09 — `NON_COMPLIANCE_COUNT_CHANGED` event → RetentionLedger.dlp_release_eligible recompute.
- M23 — BG `is_active` + `coverage_amount` reads for payment-hold decisioning.
- M12 — document_id references replace MinIO direct-URL stubs (one-time migration cascade event same pattern as M04 → M12 photos).

## 5. OQ-1 — Design Decisions Required From User

### OQ-1.1 — CostLedgerEntry state machine: exact 4 states, or sub-state for "Approved" between Committed and Accrued?

**Question:** Should `CostLedgerEntry` follow the exact 4-state pipeline locked in `architecture.md` (`Budgeted → Committed → Accrued → Paid`), or introduce an `Approved` sub-state between Committed (PO issued) and Accrued (work delivered + accepted)?

**Options:**
- **A.** Exactly 4 states per architecture.md. Approval workflow lives on the parent entity (PurchaseOrder.status, RABill.status), not on CostLedgerEntry. Each state-transition emits one ledger row. Simpler ledger; mirrors X9 §9.5.1 Capital Funnel layer count exactly (4 layers).
- **B.** 5 states: `Budgeted → Committed → Approved → Accrued → Paid`. Adds an explicit "PO approved by PMO + Finance" gate before commitment fully counts. Better governance; breaks Capital Funnel layer count (X9 §9.5.1 specifies 4).
- **C.** 4 states + an `is_approved` BOOLEAN per ledger row. Hybrid — keeps state count but exposes governance flag. Risk: two sources of truth for "approved" (entity status vs ledger boolean).

**Recommendation:** **A.** The 4-state machine is locked in architecture.md and X9 §9.5.1 has a hard rule of exactly 4 funnel layers. PO/RABill approval governance belongs on those entities, not on the ledger. The ledger is the immutable financial spine — adding states inflates audit complexity for the same governance outcome already enforced by entity-level workflow.

**Cascade impact:** Locks CostLedgerEntry state ENUM (X8 v0.6 cascade — `CostLedgerEntryState`, 4 values). Confirms X9 §9.5.1 Capital Funnel layer set unchanged.

**Status:** OPEN

---

### OQ-1.2 — RABill grain: per Approved ProgressEntry, per package per period, or per project per period?

**Question:** When M04 emits `BILLING_TRIGGER_READY` for an Approved ProgressEntry, what is the RABill grain — one RABill per progress entry (fine), one per package per period (medium), or one per project per period (coarse, traditional Indian construction practice)?

**Options:**
- **A.** Per ProgressEntry (1:1 with M04 trigger). Maximum traceability; immediate. Risk: contractor side typically batches RA bills per month — high friction with industry workflow.
- **B.** Per (Package × Period). M06 buffers `BILLING_TRIGGER_READY` events; at period close (M03 reporting_period_type) generates one RABill per package. Matches industry; aligns with package-level vendor contracts. Most common in Indian EPC/DBOT.
- **C.** Per (Project × Period). Single mega-RA bill per project per month. Simplest for small projects; loses package-level traceability and conflicts with M01's multi-contract-per-project model.

**Recommendation:** **B.** The KDMC pilot operates monthly RA bills per package (legacy v2.1 implies this). Package-level grain is the natural intersection of M04 (Approved entries) and M01 (Contract per Package). Per-ProgressEntry granularity inflates RA bill count 10–50× without commercial value. Per-project conflicts with multi-contract reality.

**Cascade impact:** Drives RABill schema (FK to package_id mandatory, project_id+period composite uniqueness). Defines a buffer entity `RABillCandidate` (Approved entries waiting for period close). Affects M04 → M06 event handler design.

**Status:** OPEN

---

### OQ-1.3 — Milestone-driven billing — does M06 also accrue against M03 `Milestone` of type `Financial`?

**Question:** M03 owns `Milestone` with type ENUM including `Financial` (X8 §3.45). For DBOT projects, payment is sometimes milestone-driven (e.g., 20% on foundation completion, 40% on superstructure). Should M06 RABill creation also be triggered by M03 `Milestone.status → Achieved` for milestones of `MilestoneType=Financial`?

**Options:**
- **A.** No. RA bills are exclusively driven by M04 `BILLING_TRIGGER_READY`. Milestone-based payments are commercial construct — handle as a separate `MilestonePaymentClaim` entity in v1.1 or as configuration on the Contract entity. v1.0 stays clean.
- **B.** Yes — second trigger source. M06 listens to both M04 events AND M03 milestone-achieved events. RABill.trigger_source ENUM = `Progress / Milestone`. Adds complexity but matches DBOT reality directly.
- **C.** Yes, but milestone-only — for DBOT contracts, RA bills are driven *only* by M03 milestones (M04 progress entries become informational, not billable). Per-contract `billing_trigger_mode` ENUM on M01 Contract.

**Recommendation:** **B.** The KDMC pilot is DBOT (₹68.4 Cr); milestone-based payment is the commercial reality. Option A defers a known requirement (negative cascade — surfaces in M06 v1.1 anyway). Option C silently breaks EPC contracts that ARE progress-driven. B is the pragmatic both-and. Cascade impact is bounded — a new ENUM and a second event subscriber, no new entity.

**Cascade impact:** New ENUM `RABillTriggerSource` (X8 v0.6). New event subscription M03 → M06 (`MILESTONE_ACHIEVED_FINANCIAL`). RABill schema gains `trigger_source` + `triggering_milestone_id` (nullable). M03 spec needs an explicit emit hook on Milestone.status → Achieved for type=Financial — minor cascade, not full re-issue (per Round 18 cascade-pattern rule).

**Status:** OPEN

---

### OQ-1.4 — Stale_Pending_VO behaviour on M06 — block new Committed entries, or only flag?

**Question:** When M02 reports `Package.bac_integrity_status = Stale_Pending_VO` (a VO is in flight against the package), should M06 block the creation of new `Committed` CostLedgerEntry rows against that package, or only flag them with a warning indicator?

**Options:**
- **A.** Block. Hard stop at M06 API gate — caller receives `409 Conflict` with `bac_integrity_status` reason. Maximum integrity; respects the spirit of M02 BACIntegrityLedger immutability. Risk: business continuity — vendors keep delivering and committing during VO review, so blocking pauses real ops.
- **B.** Flag-only. New Committed rows persist with `bac_integrity_warning_flag=true`; M02 BACIntegrityLedger references each. Allows ops continuity. Risk: race conditions where VO materialisation changes BAC but commitments locked at old rate.
- **C.** Hybrid threshold — block if cumulative new commitment > 10% of package BAC during stale period; flag below. Smart but adds a tunable that needs governance.

**Recommendation:** **B.** M02 BAC integrity is forensic — the question it answers is "do we know what the BAC really is?" The answer to commitments during VO review is operational ("can we keep paying vendors?"), and the answer there is yes. The flag is the audit hook; the commitment ledger preserves the row; M02 + M07 reconcile when the VO materialises. Option A creates a perverse incentive (rush VOs).

**Cascade impact:** Adds `bac_integrity_warning_flag` to CostLedgerEntry. Confirms M02 → M06 event subscription on `BAC_INTEGRITY_STATUS_CHANGED`. No M02 spec change.

**Status:** OPEN

---

### OQ-1.5 — Cashflow forecast horizon and grain

**Question:** What horizon and grain should the cashflow forecast cover — full project lifetime (planned_start to planned_end), rolling 12-month window, or driven by M03 reporting_period_type?

**Options:**
- **A.** Full project lifetime, period-grain = `M03 LookAheadConfig.reporting_period_type` (Monthly default). One CashflowForecast row per (WBS × period) for the entire planned duration. Fully aligns with M03 PVProfile (per-WBS-per-period) for direct EVM consumption by M07.
- **B.** Rolling 12-month from report_date. Cheaper compute, smaller dataset. Loses long-tail visibility on multi-year DBOT projects (KDMC is ~3 years).
- **C.** Two-tier: rolling 12-month at fine grain + project-lifetime at quarterly grain. Better for visualisation but two storage models — added complexity.

**Recommendation:** **A.** The M03 PVProfile is already per-WBS-per-period for the full lifetime; M06 cashflow forecast is the AC mirror of it. Symmetry with M03 is the cheapest design. Storage cost trivial (KDMC: ~30 WBS × 36 months = 1080 rows). M07 needs the symmetry to compute EVM.

**Cascade impact:** Cashflow regeneration is a heavy operation — must be guarded by atomic transaction same as M03 BR-03-034 (PV regen) and triggered on report_date change OR `reporting_period_type` change OR Approved progress that shifts forecast. Adds Decision Queue trigger `CASHFLOW_REGEN_FAILED`.

**Status:** OPEN

---

### OQ-1.6 — Currency handling in v1.0

**Question:** Should v1.0 ship single-currency (₹ INR only) or multi-currency with the legacy v2.1 ForexRateMaster + ForexVariation pattern intact?

**Options:**
- **A.** Single-currency v1.0 (₹ INR only). Defer ForexRateMaster + ForexVariation + multi-currency PO to v1.1. Faster lock; KDMC pilot is INR-only. Risk: medical-equipment imports (LINAC, MRI, CT) on healthcare projects are routinely USD/EUR — KDMC v2 will need it.
- **B.** Multi-currency in v1.0 with full ForexRateMaster (legacy v2.1 design — RBI_Reference + Bank_Transaction tiers, lock-after-24hr, deviation gate). Ship-ready for healthcare reality. Adds ~6 BRs + 1 entity + 2 ENUMs.
- **C.** Multi-currency hooks (currency_code field + is_multi_currency bool on Project) but ForexRateMaster deferred. Schema is forward-compatible; logic stub returns 1.0 rate. Worst-of-both — ships partial complexity without payoff.

**Recommendation:** **B.** Healthcare-infrastructure (the EPCC core domain) imports tens of crores of medical equipment per project. KDMC pilot itself has Cancer + Cardiology equipment — almost certainly USD/EUR sourced. Deferring forex creates a guaranteed v1.1 cascade with messy migration of existing INR-only entries. Legacy v2.1 already designed it; adopt with audit fixes (append-only enforcement on ForexRateMaster).

**Cascade impact:** New ENUMs `Currency` (extend X8 §3.13 if not already there — it is), `ExchangeRateTier` (RBI_Reference / Bank_Transaction). New entity ForexRateMaster. ~6 BRs (legacy BR-06-033 to BR-06-039 — re-numbered). ForexRateMaster append-only enforcement at DB level. PMO_DIRECTOR approval gate for >5% deviation → Decision Queue trigger.

**Status:** OPEN

---

### OQ-1.7 — Payment-side workflow scope: AC-only, or full Payment cycle (PO release → Vendor invoice → GRN-match → Payment)?

**Question:** Does v1.0 just record AC at the four states, or implement the full payment workflow (vendor invoice receipt → 2/3-way GRN match → payment release → bank confirmation)?

**Options:**
- **A.** AC-only. M06 records `Paid` ledger entries when finance team manually flips the state. No workflow inside EPCC. Vendor invoices, payment runs, bank confirmations live in the external accounting system (Tally/SAP — already an M01 stub field). Lightweight; ships faster.
- **B.** Full payment workflow. M06 owns vendor invoice receipt + 2/3-way match (PO ↔ GRN ↔ Invoice) + payment release approval + bank confirmation upload. Adds ~3 entities, ~10 BRs, ~6 ENUMs. Treats EPCC as the payment system. Risk: scope creep into accounting territory; M01 explicitly excludes accounting integration.
- **C.** Middle ground — vendor invoice receipt + 2/3-way match (the matching logic that requires GRN + PO context which only EPCC has), but payment release stays manual / external. Adds ~2 entities. The match logic can't easily live elsewhere because GRN is M06-owned and PO is M06-owned.

**Recommendation:** **C.** The 2/3-way match logic is a proper EPCC concern because EPCC owns both PO terms (M06) and GRN (M06 via M04). External accounting systems can't see the GRN context. But payment release approval (signature workflow, bank file generation) is the accounting system's job. C draws the boundary at "evidence assembly" — EPCC assembles, accounting executes. Lightweight enough to ship; complete enough to enable the Capital Funnel.

**Cascade impact:** New entities `VendorInvoice`, `InvoiceMatchResult`. New ENUMs `InvoiceMatchStatus` (3-way_pass / 3-way_fail_quantity / 3-way_fail_rate / 2-way_pass / Pending), `VendorInvoiceStatus`. Decision Queue trigger `INVOICE_MATCH_FAILED`. PaymentRelease entity OUT (owned by external accounting). `Paid` state-transition driven by manual confirmation upload + finance-team flip (no automation in v1.0).

**Status:** OPEN

---

### OQ-1.8 — Retention release authority and tranche structure

**Question:** Retention release is the single highest-stakes financial event (₹3+ crore on a KDMC-sized project). What tranche structure and approval authority?

**Options:**
- **A.** Single tranche at SG-11 + DLP-end. All retention released together at DLP-end (subject to M15 + M09 zero-defect / zero-non-compliance gates). Simplest. Legacy v2.1 OQ #4 lands here ("not permitted partial").
- **B.** Two tranches per legacy v2.1: split (e.g., 50/50) — half at SG-11 (substantial completion), half at DLP-end. Configured per-Contract via `dlp_retention_split_pct` field on M01 Contract (legacy v2.1 BR-06-046 mentioned this). Matches Indian construction industry standard.
- **C.** Configurable tranches (1, 2, or N) per contract — `RetentionTrancheConfig` sub-entity per Contract with release_event (SG_11 / DLP_END / CUSTOM_DATE) + percentage. Maximum flexibility; over-engineered for v1.0.

**Recommendation:** **B.** Two-tranche is the Indian healthcare construction norm and the KDMC pilot's commercial structure. Option A ignores industry; Option C ships configuration that nobody uses in Phase 1. B requires one new field on M01 Contract (`dlp_retention_split_pct`, default 0.50) — that's an M01 cascade note (small change → cascade pattern per Round 18 audit), not a re-issue. Each tranche release governed by Finance Lead initiation + PMO Director approval (5-step PaymentWorkflow per legacy).

**Cascade impact:** **M01 v1.3 cascade note** — adds `Contract.dlp_retention_split_pct DECIMAL(5,4) DEFAULT 0.5000`. RetentionLedger has two release events (`Substantial_Completion`, `DLP_End`). Pre-condition checks per legacy v2.1 BR-06-043 (DLP-end gated by M15 + M09 zero-counts). PMO override path with ≥200-char justification (legacy BR-06-045). New ENUM `RetentionReleaseType` (X8 v0.6).

**Status:** OPEN

---

### OQ-1.9 — Bank Guarantee read-side: track in M06, or strict M23 boundary?

**Question:** BG identity (number, issuing bank, expiry, coverage amount) is owned by M23 BGInsuranceTracker (Phase 2). But M06 needs BG status for several decisions (retention-release-allowed-without-BG-replacement, payment-hold-on-expired-BG). What's the v1.0 approach?

**Options:**
- **A.** Strict M23 boundary — M06 v1.0 has a stub `bg_status` enum field (Active / Expired / Not_Applicable) updated by manual finance-team input until M23 lands. No BG entity inside M06.
- **B.** M06 owns minimal BG records (BG number, issuing bank, expiry, coverage amount, is_active) until M23 ships, then migrates. Same pattern M04 used for photos (MinIO stub until M12).
- **C.** No BG handling at v1.0 — defer all BG-aware decisions to M23 launch. Risk: some retention/payment decisions will be wrong (released against expired BG).

**Recommendation:** **B.** This is the same pattern locked for M04 → M12 photo handling — own the minimal stub now, design the migration cascade event up front. The Capital Funnel and retention release flows MUST be BG-aware to be useful; A creates a fragile manual process; C creates known wrong decisions. Stub entity `BGStub` with a one-time migration cascade event drafted in Spec Appendix C (same pattern as M04 Spec Appendix C).

**Cascade impact:** Lightweight `BGStub` entity (5 fields). M23 migration cascade event documented at v1.0 lock. PaymentWorkflow + RetentionLedger read `BGStub.is_active` + `expiry_date`. Decision Queue trigger `BG_EXPIRING_SOON` (90/30/7-day thresholds).

**Status:** OPEN

---

### OQ-1.10 — Decision Queue trigger thresholds (concrete numbers required)

**Question:** What are the concrete thresholds for M06's Decision Queue triggers?

**Sub-questions (each independently OPEN):**

1. **Capital headroom (Committed approaching Budgeted):** amber at what %? red at what %?
2. **Payment SLA breach:** vendor invoice approved-to-paid > N days? (Default M01 Contract.payment_credit_days = 30, but trigger at +X days delay?)
3. **Forex deviation from RBI reference rate** (if OQ-1.6=B): legacy v2.1 says >5%. Confirm or adjust?
4. **BG expiry warning** (if OQ-1.9=B): at how many days before expiry?
5. **Retention release blocked:** trigger at what stale-period (days since dlp_release_eligible became true but not yet released)?
6. **Cost overrun on package** (Accrued > BAC): amber at what %? red at what %?

**Options (umbrella):**
- **A.** Adopt legacy v2.1 numbers where given (forex >5%, capital amber 95% / red 100% from X9 §9.5.1 thresholds locked); set rest at industry-default tunables in `ProjectExecutionConfig`-equivalent on M06 (`M06FinancialConfig`).
- **B.** Lock single set of system-wide defaults; no per-project tunability.
- **C.** Surface each threshold as separate OQ-2 in Spec round (defer numerical decisions).

**Recommendation:** **A.** Reuse the M04 ProjectExecutionConfig pattern (per-project tunable settings with PMO_DIRECTOR-edit + audit). Adopt legacy v2.1 numbers as defaults. The Brief should NOT silently lock thresholds; the Spec should ship `M06FinancialConfig` with table of defaults + PMO override path.

**Cascade impact:** New entity `M06FinancialConfig` (~10 fields, all tunables). One PMO_DIRECTOR-only edit BR with justification ≥100 chars (M04 pattern). Audit event `M06_CONFIG_EDITED`.

**Status:** OPEN

---

### OQ-1.11 — Tax handling scope: GST-only-record, or full GST input-credit + TDS?

**Question:** How much tax logic in v1.0?

**Options:**
- **A.** Record-only. M06 stores GST rate (from M01 Contract.gst_rate) and GST amount on each PO/invoice/RA bill. No reconciliation, no TDS. Tax compliance happens externally in Tally/SAP.
- **B.** GST input-credit reconciliation (the gst_input_credit ledger) + TDS deduction at payment release. Significant complexity (~3 entities, ~15 BRs, requires CIN + TAN tracking on Party). Genuinely useful in India but huge scope expansion.
- **C.** Phased — record-only in v1.0; explicit TaxLedger module roadmap stub at Spec Block 9 (Exclusions). Tax compliance integration in Phase 2.

**Recommendation:** **C.** v1.0 must record what's seen on invoices (GST rate, GST amount, TDS-deducted-at-source if visible) but not do reconciliation. Reconciliation is an entire module. Naming the future `TaxLedger` module in Block 9 keeps the scope-discipline trail honest (same pattern M04 used for DLP→M15, HSE→M31).

**Cascade impact:** Block 9 records future module reference. No new ENUMs in v1.0 specific to tax. CostLedgerEntry has `gst_amount_inr DECIMAL(15,2)` and `tds_amount_inr DECIMAL(15,2)` fields.

**Status:** OPEN

---

## 6. OQ-2 — Pattern Defaults

### OQ-2.1 — Append-only ledger list with DB-level UPDATE/DELETE forbidden

**Default:** Following ledgers append-only (REVOKE UPDATE, DELETE; INSERT + SELECT only):
1. `CostLedgerEntry` — every state transition; the AC backbone
2. `RABillLedger` — every RA bill state change (Draft → Submitted → Approved → Paid)
3. `GRNLedger` — every GRN event (Received → QC → Accepted → emitted)
4. `RetentionLedger` — every retention withholding + release event (tranche-level)
5. `ForexRateMaster` (if OQ-1.6=B) — rate entries become immutable after 24hr
6. `PaymentWorkflowLog` — every state transition in the 5-step payment workflow
7. `M06ConfigChangeLog` (if OQ-1.10=A) — every config edit

**Reasoning:** Mirrors M02 BACIntegrityLedger and M04 four-ledger pattern (Round 18 cascade-pattern discipline). DB-level enforcement closes any forensic-tampering gap at source, not at app layer.

**Override risk:** If user prefers app-layer-only (no DB REVOKE), forensic integrity weakens to "trust the app server" — same flaw discovered in audit Round 0. Strongly recommend default.

**Status:** OPEN

---

### OQ-2.2 — Audit-events catalogue locked from authoring

**Default:** M06 Spec ships **Appendix A — Audit Events Catalogue** at lock time, naming all UPPER_SNAKE_CASE event constants per Round 18 cascade-pattern (M03 + M04 precedent). Estimated ~28 events:

```
COST_LEDGER_ENTRY_CREATED, COST_LEDGER_STATE_TRANSITIONED,
PURCHASE_ORDER_CREATED, PURCHASE_ORDER_AMENDED, PURCHASE_ORDER_CANCELLED,
RA_BILL_CANDIDATE_BUFFERED, RA_BILL_GENERATED, RA_BILL_SUBMITTED,
RA_BILL_APPROVED, RA_BILL_PAID,
GRN_RECEIVED, GRN_LINKED_TO_PO, GRN_INVOICE_MATCHED,
VENDOR_INVOICE_RECEIVED, INVOICE_MATCH_PASSED, INVOICE_MATCH_FAILED,
RETENTION_WITHHELD, RETENTION_TRANCHE_RELEASED,
DLP_RELEASE_PRECONDITION_MET, DLP_RELEASE_PRECONDITION_BLOCKED,
DLP_RELEASE_PMO_OVERRIDE,
FOREX_RATE_ENTERED, FOREX_RATE_LOCKED, FOREX_RATE_PMO_APPROVED,
FOREX_DEVIATION_REVIEW, FOREX_VARIATION_COMPUTED,
CASHFLOW_REGENERATED, CASHFLOW_REGEN_FAILED,
M06_CONFIG_EDITED,
BG_STATUS_UPDATED, BG_EXPIRING_SOON,
BAC_INTEGRITY_WARNING_FLAGGED
```

**Reasoning:** Round 18 audit confirmed locked-from-authoring is now the standard for spec lock. Catalogue source-of-truth until X3 (Audit Event Catalogue) lands.

**Override risk:** Floating event names → drift across modules → hard-to-trace audit queries. Same discipline that locked M04's 22 events.

**Status:** OPEN

---

### OQ-2.3 — Speed-tier mapping per event class

**Default:**
- T1 (real-time, < 2 sec): all CostLedgerEntry transitions, RA bill state changes, GRN events, retention release, payment workflow steps, BAC-integrity-status-changed reads, forex deviation gate.
- T2 (2–4 hr): cashflow regeneration on report_date change, monthly RA bill generation cron (period-close), config edits.
- T3 (24 hr): BG expiry sweep, capital headroom advisory, retention release stale check.

**Reasoning:** Mirrors M03 + M04 speed-tier patterns. T1 is reserved for transactional integrity; cashflow regen is heavyweight and acceptable as T2.

**Override risk:** If cashflow regen is forced T1, peak-load report_date changes risk DB lock contention. If BG expiry stays T2 instead of T3, alert noise increases without value.

**Status:** OPEN

---

### OQ-2.4 — Reading `reporting_period_type` from M03

**Default:** M06 reads `LookAheadConfig.reporting_period_type` via M03 internal API on every cashflow regeneration (per M01 v1.2 cascade — M03 owns the field). Cached for the duration of a single regen job; never stored as a denormalised field on M06 entities.

**Reasoning:** Single-Owner rule (F-005). Caching scope is the regen job to avoid 100s of API calls during a single cashflow rebuild. Storing it on M06 entities would re-create the M01 v1.2 problem.

**Override risk:** If denormalised onto M06, future M03 spec changes break the contract silently. If not cached at all, regen perf degrades.

**Status:** OPEN

---

### OQ-2.5 — Photo / document references stub

**Default:** Same pattern as M04 Spec Block 3b — entities that need document references (e.g., FEMA Form A2 for forex Bank_Transaction tier; vendor invoice PDF; bank debit advice for payment confirmation) carry both `document_id` JSONB (target — M12 reference) and `document_url` JSONB (MinIO direct URL stub) until M12 lands. One-time migration cascade event documented in Spec Appendix C: `20260XXX_M12_absorb_M06_document_urls.py`.

**Reasoning:** Direct copy of M04 → M12 pattern. The discipline is already in cross-cutting practice.

**Override risk:** Skipping the migration cascade definition at lock time creates a known-unknown when M12 ships.

**Status:** OPEN

---

### OQ-2.6 — Single-currency vs multi-currency in stub period (if OQ-1.6=A or C)

**Default:** If OQ-1.6=A or C, all monetary fields stay `DECIMAL(15,2) INR`; multi-currency hooks (`po_currency`, `po_amount_foreign`, etc.) are NOT shipped in v1.0 schema even as nullable fields. Adding them later is a clean migration.

**Reasoning:** Half-baked schema (Option C in OQ-1.6) is the worst pattern. Keep schema clean; migrate cleanly when needed.

**Override risk:** N/A if OQ-1.6=B (multi-currency at v1.0).

**Status:** OPEN

---

## 7. Design Sketch (plain language)

M06 is the **financial nervous system** of the project. It does one job, four times per rupee: track when each rupee moves from `Budgeted` (M02 says it exists) → `Committed` (a PO is signed) → `Accrued` (work is delivered + accepted by M04) → `Paid` (cash leaves the bank). That's the **Capital Funnel** — the X9 §9.5.1 flagship pattern, the FINANCE_LEAD's primary view.

Two events do most of the heavy lifting: `BILLING_TRIGGER_READY` (M04 → M06, on Approved progress) and `MATERIAL_GRN_EMITTED` (M04 → M06, on accepted material). Each fires a state transition in CostLedgerEntry. RABill is the contractor-facing artefact assembled at period close (per OQ-1.2=B); GRNLedger is the vendor-side artefact assembled per receipt.

PurchaseOrder is the contract-with-vendor. M03's `ProcurementScheduleItem` already has a forward-pointing `m06_po_id` field (per M03 Block 3) — when M06 issues a PO, it back-fills that pointer. M03 owns timing; M06 owns identity + commercial terms (locked in M03 Block 9).

RetentionLedger is the highest-stakes ledger: it withholds 5–10% of every approved RA bill, holds it through SG-11 (substantial completion) → DLP period → DLP-end. The DLP-end release is gated by zero open defects (M15 — re-routed from legacy v2.1's M04 reference) and zero open Non_Compliance observations (M09). Both signals stub until those modules land.

**Role views (X9 §13.3.6 locked):**

| Role | Primary view | Decision the view answers |
|---|---|---|
| FINANCE_LEAD | Capital Funnel ⭐ | Do I have headroom to commit more capital this period? |
| PMO_DIRECTOR | Capital Funnel + Margin by Package | Are any packages running unprofitable? |
| PROJECT_DIRECTOR | Capital Funnel (own project) + RA bills due | What's outstanding on my project this week? |
| PROCUREMENT_OFFICER | Vendor outstanding bar + PO status | Who am I paying late? |
| SITE_MANAGER | Capital Funnel (% only, ₹ values redacted) | Subset awareness without commercial visibility |

The **Capital Funnel** has FINANCE_LEAD seeing actual rates (per X9 cross-cutting role mapping), PROJECT_DIRECTOR seeing Loaded × 1.15 spike, SITE_MANAGER seeing `[RESTRICTED]` for ₹ values but full structure. Same field-level rate display rules locked since M02 OQ-2.11.

**Stub-period reality:** M05 (VO impacts), M07 (EVM), M08 (gates), M15 (DLP defects), M09 (Non_Compliance), M23 (BG identity), M12 (documents) — none built. M06 v1.0 ships with all signal-receivers as STUB endpoints + a clearly-documented migration cascade per receiver, mirroring M04's M12-stub pattern.

## 8. Open Items Tracker

| ID | Topic | Type | Status |
|---|---|---|---|
| OQ-1.1 | CostLedgerEntry state machine | User Decision | **CLOSED — A** (4-state locked: Budgeted → Committed → Accrued → Paid) |
| OQ-1.2 | RABill grain | User Decision | **CLOSED — B** (per Package × Period — KDMC monthly RA pattern) |
| OQ-1.3 | Milestone-driven billing | User Decision | **CLOSED — B** (both progress + milestone triggers) — user note: "milestone payment is very common in DBOT projects" |
| OQ-1.4 | Stale_Pending_VO behaviour | User Decision | **CLOSED — B** (flag, don't block; M02+M07 reconcile on VO materialisation) |
| OQ-1.5 | Cashflow forecast horizon + grain | User Decision | **CLOSED — A** (full lifetime, per-WBS-per-period — mirrors M03 PVProfile) |
| OQ-1.6 | Currency handling | User Decision | **CLOSED — B** (multi-currency v1.0 with ForexRateMaster) — user note: "INR in case of KDMC but need not be in other projects" → KDMC pilot may not exercise forex paths but system must support future projects with foreign-currency equipment imports |
| OQ-1.7 | Payment-side scope | User Decision | **CLOSED — C** (split: EPCC owns 2/3-way match; accounting executes payment) — user note: "C is appropriate" |
| OQ-1.8 | Retention release authority + tranches | User Decision | **CLOSED — C** (tranched + dual sign-off; triggers M01 v1.3 cascade for `Contract.dlp_retention_split_pct`) |
| OQ-1.9 | Bank Guarantee handling | User Decision | **CLOSED — B** (BGStub pattern; mirrors M04 → M12 photo-stub precedent; migrate when M23 Phase 2 lands) |
| OQ-1.10 | Decision Queue thresholds | User Decision | **CLOSED — A** (M06FinancialConfig per-project tunables; mirrors M04 ProjectExecutionConfig) |
| OQ-1.11 | Tax scope | User Decision | **CLOSED — C** (invoice-record-only; reconciliation deferred to future TaxLedger module) |
| OQ-2.1 | Append-only ledger list | Pattern Default | **CLOSED — Confirmed** (4 ledgers: CostLedgerEntry, RABillAuditLog, PaymentEvidenceLedger, ForexRateLog) |
| OQ-2.2 | Audit-events catalogue from authoring | Pattern Default | **CLOSED — Confirmed** (Spec Appendix A locks ~28 event names; per Round 18 cascade-pattern discipline) |
| OQ-2.3 | Speed-tier mapping | Pattern Default | **CLOSED — Confirmed** (T1 transactional, T2 cashflow regen, T3 batch) |
| OQ-2.4 | reporting_period_type cache scope | Pattern Default | **CLOSED — Confirmed** (M03 internal API; cache for regen job duration; no denormalised storage) |
| OQ-2.5 | Document references stub pattern | Pattern Default | **CLOSED — Confirmed** (`document_url` MinIO + `document_id` M12 target; same migration as M04 → M12) |
| OQ-2.6 | Schema-clean rule for single-currency | Pattern Default | **CLOSED — N/A** (OQ-1.6=B; multi-currency shipped, this rule does not apply) |

**Lock criterion:** All OPEN → CLOSED before Brief is marked LOCKED.

## 9. Anticipated Cascades (for Spec round)

- **X8 v0.6 cascade — new ENUMs (count depends on OQ-1 outcomes):**
  - `CostLedgerEntryState` (4 values per OQ-1.1=A) — system-wide
  - `RABillStatus` (~5 values: Draft / Submitted / Approved / Paid / Rejected) — M06-owned
  - `RABillTriggerSource` (Progress / Milestone) if OQ-1.3=B — M06-owned
  - `GRNStatus` (Received / In_QC / Accepted / Rejected / Linked / Matched) — M06-owned
  - `RetentionReleaseType` (Substantial_Completion / DLP_End / PMO_Override) if OQ-1.8=B — M06-owned
  - `ExchangeRateTier` (RBI_Reference / Bank_Transaction) if OQ-1.6=B — M06-owned
  - `VendorInvoiceStatus` (~5 values) if OQ-1.7=C — M06-owned
  - `InvoiceMatchStatus` (~5 values) if OQ-1.7=C — M06-owned
  - `PaymentWorkflowStep` (5 values) — M06-owned
  - `BACIntegrityWarningSource` (M02_VO_Pending / Manual_Override) — small, M06-owned
  - **M06 Decision Queue trigger types** (~6 triggers per OQ-1.10): `CAPITAL_HEADROOM_BREACH`, `PAYMENT_SLA_BREACH`, `FOREX_DEVIATION_APPROVAL`, `BG_EXPIRING_SOON`, `RETENTION_RELEASE_BLOCKED_DLP`, `INVOICE_MATCH_FAILED`, `BAC_INTEGRITY_WARNING`, `CASHFLOW_REGEN_FAILED`.
  - X8 §6 reserved-fields exemption list extended with M06 append-only ledgers.

- **M01 v1.3 cascade note** (if OQ-1.8=B): adds `Contract.dlp_retention_split_pct DECIMAL(5,4) DEFAULT 0.5000` field. Cascade note (small change → cascade pattern per Round 18 audit), NOT full re-issue. M01 spec gains BR-01-036 (PMO-edit + justification ≥100 chars).

- **M03 minor cascade** (if OQ-1.3=B): M03 Spec gains explicit emit hook on `Milestone.status → Achieved` for type=Financial — `MILESTONE_ACHIEVED_FINANCIAL` event. Block 7 SENDS TO M06 entry added. Cascade note pattern, not re-issue.

- **X9 v0.4 cascade** (likely): §13.3.6 row already exists at v0.3 lock; M06 wireframes will validate. May need refinement after Wireframes round.

- **M04 read-side confirmation**: M04 BR-04-012 (BILLING_TRIGGER_READY) and BR-04-028 (MATERIAL_GRN_EMITTED) are locked-from-authoring; M06 Spec must explicitly cite each in Block 7 RECEIVES FROM. No M04 cascade.

## 10. Out-of-Scope Decisions (deferred)

- **Tax reconciliation engine (TaxLedger module)** — referenced as future module in Spec Block 9 per OQ-1.11=C recommendation. Phase 2.
- **Accounting-system bidirectional sync (Tally/SAP/Zoho)** — out of v1.0 per M01 design (`accounting_system` is free-text stub). Phase 2.
- **PaymentRelease automation (bank file generation, payment approval signature workflow)** — owned by external accounting system per OQ-1.7=C boundary.
- **BG identity master (number, issuing bank details, claim workflow)** — M23 BGInsuranceTracker (Phase 2). M06 ships `BGStub` per OQ-1.9=B.
- **Vendor pre-qualification, scorecards, blacklist** — M30 VendorMasterPQ (Phase 2). M06 references `Party` from M01 only.
- **Multi-tenant currency localisation (e.g., AED for Gulf-region tenants)** — out of v1.0 even if OQ-1.6=B (which is INR + USD/EUR for medical equipment imports only).
- **Schedule re-baselining triggered by VO** — M03 v1.0 explicitly excludes schedule re-baselining; M06 inherits this constraint.
- **Working capital optimisation, capital allocation MILP** — L1 Strategic concern (M16/M17/M18/M19); M06 surfaces inputs to those modules but doesn't compute.

---

*v1.0 Brief — DRAFT. Awaiting Monish OQ-1 closure (11 user decisions + 6 pattern defaults). Lock criterion: all 17 OPEN items → CLOSED.*
