# M02 — Structure & WBS
## Brief v1.0a
**Status:** LOCKED _(grandfathered: original was "Draft — Pending Review"; Brief approved at Round 9 → Spec/Wireframes/Workflows all locked; M02 module COMPLETE per CLAUDE.md §3)_
**Author:** Monish (with Claude assist) _(grandfathered: PMO Director / System Architect)_
**Created:** 2026-05-03 | **Last Updated:** 2026-05-04 (v1.0a in-place patch — Round 29 audit medium-cleanup, M20)
**Last Audited:** v1.0a on 2026-05-04
**Reference Standards:** EPCC_NamingConvention_v1_0.md, X8_GlossaryENUMs_v0_2.md _(historical at lock; current X8 v0.6a)_, M34_SystemAdminRBAC_Spec_v1_0.md, M01_ProjectRegistry_Spec_v1_0.md (+ v1_1/v1_2/v1_3/v1_4 cascade notes)
**Folder:** /03_L2_Planning/ _(aspirational; canonical placement is `SystemAdmin/Modules/` per Round 18 audit)_
**Phase:** 1 (Foundational — third module after M34 + M01)
**Re-Issue Of:** Legacy M02_Structure_WBS_v2.0 (base) + v2.1 (amendment) — consolidated standalone

---

## CHANGE LOG

| Patch | Date       | Author                      | Changes |
|-------|------------|-----------------------------|---------|
| v1.0a | 2026-05-04 | Monish (with Claude assist) | M20 in-place patch (Round 29 audit medium-cleanup): **Status** corrected "Draft — Pending Review" → "LOCKED" (Brief approved Round 9, Spec Round 10, Wireframes Round 11, Workflows Round 12 — module COMPLETE); author canonicalised; `Last Updated` + `Last Audited` refreshed; `Reference Standards` historical-at-lock annotation added; M01 reference extended with v1_1/v1_2/v1_3/v1_4 cascade notes; `Folder` field annotated. No content/scope change. |

---

## 1. IDENTITY

| Attribute | Value |
|---|---|
| Module ID | M02 |
| Module Name | Structure & WBS |
| Layer | L2 Control — Planning & Structure |
| Phase | Phase 1 — Foundational |
| Build Weeks | 6 (estimate; module is dense) |
| Spec Status | Brief (this) → Spec → Wireframes → Workflows |
| Priority | 🔴 Critical — every execution module (M03, M04, M06, M07) depends on M02 entities |

---

## 2. DECISION IT ENABLES

> Is the project's work decomposition (WBS) and commercial decomposition (BOQ within Packages) complete, internally consistent, role-appropriately visible, and BAC-integrity-tracked — providing every other module with the structural backbone for schedule, progress, cost, and EVM?

---

## 3. SCOPE — INCLUDES

| Capability | Description |
|---|---|
| WBS hierarchy | Variable depth via `parent_id` self-reference. System minimum: 4 levels. User-extensible. |
| Package master | Work packages within project — contractual + execution units |
| BOQ master | Bill of Quantities items with quantity + actual rate (rate display role-controlled) |
| BOQ ↔ WBS many-to-many mapping | `BOQWBSMap` junction with primary WBS designation |
| Unit master | 3-tier governance: Standard_Core (locked) / Domain_Specific (PMO_DIR) / Custom (project) |
| Package templates | User-defined + system-shipped, versioned with delta tracking |
| CSV bulk import | Modal-gated per session: `Create_Only` OR `Create_And_Update`. All-or-nothing. |
| Role-controlled rate display | Three spike formulas: Loaded / Indexed / Flat_Redacted. Field-level permission. |
| BAC computation per package | `bac_amount = SUM(BOQItem.actual_rate × quantity)` per package |
| BAC integrity tracking (v2.1) | `bac_integrity_status` flag — Confirmed vs Stale_Pending_VO |
| BACIntegrityLedger | Append-only audit of every BAC change (forensic record) |
| VO materialisation receiving-end | M05 triggers; M02 executes BOQ updates; confirms back to M05/M07 |
| 5-ID chain validation | `BOQ_ID → WBS_ID → PKG_ID → CONTRACT_ID → PHASE_ID` per ES-DI-001 |
| BOQ origin tracking | `boq_origin` ENUM: Manual / CSV_Import / VO_Materialisation / Template_Applied |
| WBS code generation | Auto-generated dotted notation (e.g., `3.1.2`) based on parent + sibling sequence |

---

## 4. SCOPE — EXCLUDES

| Excluded | Where It Lives |
|---|---|
| Schedule (planned dates, baselines, S-curves, PV) | M03 Planning |
| Actual cost transactions, RA bills, sub-contracts | M06 Financial |
| Rate sourcing (CPWD DSR, market rates) — only stored rates here | M06 + external |
| Progress capture (% complete, NCRs, DLP) | M04 Execution |
| EVM (CPI, SPI, EAC, ETC, VAC, TCPI) | M07 EVM Engine |
| VO trigger workflow (initiation, approval, SLA) | M05 Risk & Change |
| EAC suspension logic during VO materialisation | M07 EVM Engine |
| Stage gate decisions tied to baseline lock | M08 Gate Control |
| Document storage (drawings, specs, BOQs as PDFs) | M12 Document Control + MinIO |
| QS measurement book entries | M14 QS Measurement Book |
| Tendering workflow + BOQ pricing strategy | M29 Tendering & Award |
| BIM model integration | PF02 BIM Integration (Phase 4) |

---

## 5. ENTITY LIST

| Entity | Purpose | Schema Owner |
|---|---|---|
| `WBSNode` | Hierarchical work breakdown structure with parent_id self-reference | M02 |
| `Package` | Work package within project (contractual + execution unit) | M02 |
| `BOQItem` | Bill of Quantities line item with rate + quantity + BAC contribution | M02 |
| `BOQWBSMap` | Many-to-many junction; one WBS marked `is_primary_wbs=true` per BOQ | M02 |
| `UnitMaster` | 3-tier governed list of measurement units | M02 (system + tenant + project tier) |
| `PackageTemplate` | Reusable package structure for replication across projects | M02 |
| `PackageTemplateVersion` | Versioned snapshots of package templates with delta tracking | M02 |
| `BACIntegrityLedger` | **Append-only** audit of every BAC change. **Owned by M02; read-only from M07.** | M02 |
| `IDGovernanceLog` | 5-ID chain validation log per ES-DI-001 | M02 |
| `CSVImportSession` | Per-session import metadata (mode, validation report, commit status) | M02 |
| `CSVImportRecord` | Per-row audit of CSV import (created/updated/failed/skipped) | M02 |

---

## 6. ROLES THAT TOUCH THIS MODULE

References M34 canonical taxonomy. Field-level rate visibility is role-tiered (per legacy + audit fix F-014):

| Role | Capability | Rate Visibility |
|---|---|---|
| `SYSTEM_ADMIN` | Standard_Core unit master edit | Actual rate |
| `PMO_DIRECTOR` | Full WBS/BOQ CRUD; Domain_Specific units; package template promotion | **Actual rate** |
| `PORTFOLIO_MANAGER` | View all projects' WBS/BOQ structure (no edits cross-project) | Spiked rate (Loaded) |
| `PROJECT_DIRECTOR` | Edit own project WBS/BOQ; Custom unit master per project | Spiked rate (Loaded) |
| `PLANNING_ENGINEER` | Edit WBS structure (own project); read BOQ | Spiked rate (Indexed) |
| `QS_MANAGER` | Edit BOQ items (quantities); execute VO materialisation; CSV import | Spiked rate (Indexed) |
| `FINANCE_LEAD` | Read full BOQ with rates for financial analysis | **Actual rate** |
| `PROCUREMENT_OFFICER` | Read package + BOQ structure for tender preparation | Spiked rate (Loaded) |
| `SITE_MANAGER` | Read-only WBS + BOQ (own packages) | `[RESTRICTED]` (Flat_Redacted) |
| `COMPLIANCE_MANAGER` | Read structure for compliance scope mapping | Spiked rate (Loaded) |
| `READ_ONLY` | Read-only structure | `[RESTRICTED]` |
| `EXTERNAL_AUDITOR` | Read with audit trail access | **Actual rate** (with audit log) |

**Three spike formulas (locked from legacy):**
- `Loaded` — actual rate × loaded factor (e.g., +15% indirect)
- `Indexed` — actual rate × indexing factor (CPI-style)
- `Flat_Redacted` — display literal `[RESTRICTED]`

---

## 7. DEPENDENCIES — IN

| From | Data Required | Trigger |
|---|---|---|
| M34 | Authentication context, role, project scope | Every API call |
| M34 | CodeMaster: SectorSubType (for template selection), Discipline, DocumentType | Form rendering |
| M34 | Field-level permission check for rate display (which spike formula) | Every BOQ read |
| M01 | `project_id`, `tenant_id`, `current_phase`, `project_status` | On project activation |
| M01 | `contract_id`(s) per project for ID chain | On contract create |
| M05 | `bac_integrity_status = Stale_Pending_VO` signal + `vo_id`, `affected_package_ids`, `materialisation_id` | On VO approval (cost_impact > 0) |
| M05 | Materialisation option (A/B/C) and scope when QS starts work | On materialisation In_Progress |

---

## 8. DEPENDENCIES — OUT

| To | Data Provided | Trigger |
|---|---|---|
| M03 Planning | `wbs_id`, `activity_type`, `package_id` per WBS node | On WBS creation + baseline lock |
| M03 Planning | `procurement_schedule_id` linkage on packages | On package creation |
| M04 Execution | `wbs_id` list (for progress capture grain) | On WBS creation |
| M06 Financial | `boq_id`, `wbs_id`, `package_id`, `actual_rate`, `actual_amount`, `bac_version` | On every BOQ save |
| M07 EVM Engine | `package_id`, `bac_amount`, `bac_integrity_status`, `bac_version` | On BAC recalc + integrity status change |
| M05 Risk & Change | Materialisation completion: `cost_impact_materialised`, `new_bac_snapshot`, `affected_boq_ids` | On BR-02-033 (materialisation complete) |
| M08 Gate Control | Baseline lock signal (BOQ + WBS frozen) at SG-6 | On baseline lock |
| M09 Compliance | Package list per project for compliance scope mapping | On package creation |
| M10 EPCC Command | Package count, BAC totals per project | On any structural change |
| M11 Action Register | Decision queue items for BAC integrity issues | When triggered |
| M14 QS Measurement Book | BOQ master for measurement reference | On BOQ create + edit |

---

## 9. CRITICAL OPEN QUESTIONS

### OQ-1 (Design — your decision required)

#### OQ-1.1 — WBS Minimum Depth: System-wide vs Project-configurable?

**Question:** Legacy says "Minimum 4 levels (KDMC standard)". Is 4 a system-wide hard floor or a per-project default?

**Options:**
- **A** System-wide hard floor of 4 levels (cannot create WBS shallower; aligns with KDMC pattern)
- **B** Per-project configurable (sector-driven default: Healthcare=4, Infrastructure=5, Residential=3)
- **C** No minimum — purely user discretion (KDMC just happens to use 4)

**My read:** WBS depth correlates with control granularity. A 2-level WBS produces meaningless EVM. Industry practice for healthcare construction is 4–6 levels. A floor prevents pathological structures.

**Recommendation:** **B — Per-project configurable, sector-driven default.** Add `min_wbs_depth` field to Project entity (M01 v1.1) defaulting from sector. Healthcare = 4; PMO_DIRECTOR can override per project with reason ≥ 100 chars.

---

#### OQ-1.2 — `bac_integrity_status` ENUM: 2 values or extensible?

**Question:** Legacy v2.1 introduces `bac_integrity_status ENUM { Confirmed / Stale_Pending_VO }`. Are these the only ever-needed states, or should we anticipate more?

**Options:**
- **A** Lock at 2 values — simple, matches current need
- **B** Extend to 4: `Confirmed / Stale_Pending_VO / Stale_Pending_Correction / Stale_Pending_Baseline_Revision` — anticipates other BAC mutation paths
- **C** Add `Locked_During_Audit` for the future external auditor read — anticipates EXTERNAL_AUDITOR workflow

**My read:** Premature flexibility creates surface area for bugs. Today, only VO materialisation creates "stale" BAC. Baseline revisions are M03's concern; corrections are SYSTEM_ADMIN edge cases (HDI window). Audit pause is hypothetical.

**Recommendation:** **A — Lock 2 values.** Add new states only when the trigger is formally specified. Add to X8 v0.3 as `BACIntegrityStatus` ENUM.

---

#### OQ-1.3 — Spike Formula Naming: Keep legacy or rename?

**Question:** Legacy spike formulas: `Loaded / Indexed / Flat_Redacted`. Names are slightly opaque.

**Options:**
- **A** Keep legacy names (industry-internal jargon already in use)
- **B** Rename for clarity: `Multiplier / Index_Adjusted / Redacted`
- **C** Add 4th: `Bucketed` — show rate in ranges (e.g., "₹500–700/m²") for partial transparency

**My read:** Names matter for developer clarity but the user never sees them — these are formula references. "Loaded" has specific construction meaning (loaded with overheads/profit). Keep.

**Recommendation:** **A — Keep legacy.** Document them clearly in Block 6 BR. Add to X8 v0.3 as `BOQRateSpikeFormula` ENUM.

---

#### OQ-1.4 — 5-ID Chain `PHASE_ID`: What does it reference?

**Question:** ES-DI-001 mandates 5-ID chain: `BOQ_ID → WBS_ID → PKG_ID → CONTRACT_ID → PHASE_ID`. After X8 v0.2 changed Phase enum (5-value → 10-value), what does PHASE_ID mean now?

**Options:**
- **A** Phase enum value (e.g., `Construction`, `Equipment`) — captures which phase the BOQ item was created during
- **B** Reference to Project.current_phase at BOQ creation time — historical, immutable post-creation
- **C** Reference to a `ProjectPhaseHistory` row — full traceability to the specific phase transition

**My read:** Option A is simplest. Option C is heaviest but most auditable. Option B is the legacy implicit interpretation.

**Recommendation:** **B — Snapshot Project.current_phase at creation.** Stored as denormalised string field on BOQItem (`phase_at_creation ENUM`). Immutable. Provides audit traceability without joining to a history table for every read.

---

#### OQ-1.5 — Package Template Promotion: Who promotes user → system?

**Question:** Legacy says "Package templates: user-defined with optional system-shipped templates." If a PROJECT_DIRECTOR creates a great Hospital_DBOT package template, can it be promoted to system-shipped (visible to all tenants/projects)?

**Options:**
- **A** No promotion — system-shipped templates only via release. User templates stay tenant-scoped.
- **B** Promotion via SYSTEM_ADMIN approval workflow — user template → system_shipped flag = true
- **C** Promotion via PMO_DIRECTOR (within tenant) → tenant-shipped only. SYSTEM_ADMIN promotes tenant → system.

**My read:** Cross-tenant template sharing is a future product feature, not a v1.0 concern. v1.0 should keep templates tenant-scoped. System-shipped templates ship via release.

**Recommendation:** **A — No promotion in v1.0.** System-shipped templates ship via Alembic seed migrations. User templates remain tenant-scoped. Revisit in Phase 3+.

---

#### OQ-1.6 — CSV Import `Create_And_Update` Conflict Resolution

**Question:** Legacy CSV import has two modes: `Create_Only` and `Create_And_Update`. In `Create_And_Update` mode, when a row matches an existing BOQ item by code, what fields are updated?

**Options:**
- **A** Update all fields except auto/SYSTEM (created_by, created_at, etc.)
- **B** Update only specified columns in CSV (sparse update)
- **C** Update all editable fields, but flag any quantity/rate change > 10% for PMO_DIRECTOR review before commit
- **D** Field-by-field configurable per import session (overhead)

**My read:** Sparse update (B) is what users typically want — they update one column without touching others. But legacy spec said "all-or-nothing" — that's about success/failure of the whole import, not about per-field updates.

**Recommendation:** **B — Sparse update.** Only columns present in CSV are updated. Empty cells leave existing values unchanged. CSV must include `boq_code` (key) + at least one update column. Audit log records every changed field per row.

---

#### OQ-1.7 — `boq_origin` ENUM Values

**Question:** Legacy v2.1 introduces `boq_origin ENUM { Manual / CSV_Import / VO_Materialisation / Template_Applied }`. Should we add more for future tracking?

**Options:**
- **A** Lock at 4 values per legacy
- **B** Add `BIM_Sync` (Phase 4 BIM integration) and `External_API_Import`
- **C** Add `HDI_Seed` for historical data import (HDI utility)

**My read:** HDI seed is a real concern — HDI loads historical EVM data; if it ever needs to backfill BOQ items (currently it doesn't, but could), we'd need this. BIM and API are too speculative.

**Recommendation:** **C — Add `HDI_Seed`.** Lock at 5 values: Manual / CSV_Import / VO_Materialisation / Template_Applied / HDI_Seed. Add to X8 v0.3 as `BOQOrigin` ENUM. Future values via X8 version bump.

---

#### OQ-1.8 — WBS Code Format: User-input vs Auto-generated?

**Question:** Legacy uses dotted notation like `3.1.2`. Is this user-typed or system-generated based on parent + sibling order?

**Options:**
- **A** Auto-generated based on parent + position; user cannot override
- **B** User-typed; system validates format `^\d+(\.\d+)*$`
- **C** Hybrid: auto-generated default; PMO_DIRECTOR can manually override (with audit)

**My read:** Auto-generated prevents drift and gaps. Manual override is rare in practice. Hybrid adds complexity for low value.

**Recommendation:** **A — Auto-generated.** When a WBS node is created under parent `3.1`, system finds max sibling index and assigns `3.1.{max+1}`. Reorder via drag-and-drop in UI; system reassigns codes. WBS codes are display-only — internal references use UUIDs.

---

#### OQ-1.9 — Unit Conversion: Required in v1.0?

**Question:** UnitMaster is 3-tier (Standard_Core / Domain_Specific / Custom). Should the system support unit conversion (m ↔ ft, kg ↔ ton, m² ↔ sqft)?

**Options:**
- **A** No unit conversion — units are typed labels, no math conversion. BOQ items must be in consistent units within package.
- **B** Conversion factors stored on UnitMaster — system converts on read
- **C** Display-only conversion (UI shows secondary unit; calculations always in primary)

**My read:** Indian construction is metric-only in practice. Conversion adds complexity for negligible benefit in Phase 1. Imperial only enters if international consultants/equipment specs demand it.

**Recommendation:** **A — No conversion in v1.0.** Add `unit_system ENUM { Metric / Imperial }` to UnitMaster for future-proofing. v1.0 ships with Metric only. Phase 3+ revisits if international projects emerge.

---

#### OQ-1.10 — BACIntegrityLedger Single-Owner (F-005 fix)

**Question:** Legacy says `BACIntegrityLedger` is "Owned by M02 — M07 reads this. Same entity defined in Standards Memory §7.90 and M07 v3.0 for reference." Audit F-005 flagged this joint ownership as ambiguous.

**Options:**
- **A** M02 owns schema; M07 reads via internal API call (not direct DB access)
- **B** M02 owns schema; M07 reads directly via shared DB view
- **C** Move BACIntegrityLedger to a cross-cutting shared entity owned by neither (some "Audit" service)

**My read:** Per F-005 single-owner rule — every entity has exactly one owning module. M02 is the source of BAC mutations, so M02 owns the ledger. M07 consumes via the integration API (not direct DB read).

**Recommendation:** **A — M02 owns; M07 reads via integration.** Standards Memory v1.0 should remove the "joint" framing. M07 spec on re-issue calls M02 API to fetch ledger entries when needed. Eliminates schema ownership ambiguity.

---

### OQ-2 (Pattern — defaults proposed, you accept/reject)

| # | Question | Default (proposed) |
|---|---|---|
| OQ-2.1 | UUID primary keys | **Yes** — per X8 §6 |
| OQ-2.2 | Reserved fields on every entity | **Per X8 §6** (tenant_id, created_by/at, updated_by/at, is_active) |
| OQ-2.3 | Soft delete | **Standard pattern** — append-only entities (BACIntegrityLedger, IDGovernanceLog) exempt |
| OQ-2.4 | Package code format | **`PKG-{seq}`** with auto-increment; PMO_DIRECTOR can override at creation |
| OQ-2.5 | BOQ code format | **`{PKG_CODE}-{seq}`** auto-generated; e.g., `PKG-CIV-A-001` |
| OQ-2.6 | WBS depth UI rendering | **Tree view + flat-table toggle**; tree default for ≤ 5 levels, flat for ≥ 6 |
| OQ-2.7 | CSV import file size limit | **20 MB / 50,000 rows** — larger requires split |
| OQ-2.8 | CSV validation report | **Per-row pass/fail** with summary; downloadable as CSV |
| OQ-2.9 | Audit log retention | **Permanent** for BAC ledger entries; **7 years** for routine field edits |
| OQ-2.10 | BAC version increment | **On every BAC change** — auto by SYSTEM (already in v2.1) |
| OQ-2.11 | Field-level rate display permission | **API-layer enforcement** (not UI-only) — protects against client manipulation |
| OQ-2.12 | Package status enum | **Per X8 §3.5 RecordStatus** — Draft/Active/Suspended/Archived/Deleted |

---

## 10. REFERENCE TO EXISTING MODULES

M02 spec re-issue triggers:

| Module | Update on M02 Lock |
|---|---|
| M01 | Add `min_wbs_depth` to Project entity (per OQ-1.1) — minor v1.1 bump |
| M03 Planning | References M02 entities — major recalibration on re-issue (Round 13+) |
| M05 Risk & Change | Materialisation API contract finalised (Round 17+) |
| M06 Financial | bac_version sync field — minor adjustment in M06 re-issue |
| M07 EVM | Reads BACIntegrityLedger via API (not direct DB) per OQ-1.10 |
| M08 Gate Control | Baseline lock at SG-6 references M02 freeze state |
| M14 QS Measurement | Will reference BOQItem master (Phase 1 spec, depends on M02) |
| X8 v0.3 | Add: `BACIntegrityStatus`, `BOQOrigin`, `BOQRateSpikeFormula`, `WBSCodeStrategy` ENUMs |

---

## 11. DELIVERABLES UPON SPEC LOCK

1. `M02_StructureWBS_Spec_v1_0.md` — full 10-block consolidated spec
2. `M02_StructureWBS_Wireframes_v1_0.html` — WBS tree, BOQ table, package master, CSV import wizard, BAC integrity dashboard, role-tiered rate display
3. `M02_StructureWBS_Workflows_v1_0.md` — Mermaid: WBS creation, BOQ-WBS mapping, CSV import, VO materialisation receiving end, BAC integrity transition, package template apply
4. **Update X8 to v0.3** — 4 new ENUMs (BACIntegrityStatus, BOQOrigin, BOQRateSpikeFormula, WBSCodeStrategy)
5. **Update M01 to v1.1** — add `min_wbs_depth` to Project entity (if OQ-1.1 = B)

---

## 12. RISKS / NOTES

| Risk | Mitigation |
|---|---|
| BAC integrity workflow has 6+ business rules; complex to test | Round 11 workflow file dedicates a full Mermaid to materialisation flow |
| 5-ID chain validation cross-cuts M01 + M02 + (future) M05 | ES-DI-001 standard locked; CI lint catches missing IDs at PR time |
| Role-tiered rate display is enforced at API layer — not visible in spec UI | Spec Block 6 BR will explicitly call out API serialiser responsibility |
| CSV import all-or-nothing on 50k-row imports may fail silently if validation slow | Performance budget: validation < 2 sec per 1000 rows; preview shown before commit |
| Package template versioning + delta tracking is novel | Phase 1 ships v1.0 templates; deltas reviewed quarterly |
| BACIntegrityLedger immutability requires DB-level constraint (no UPDATE permission) | Migration creates table with `REVOKE UPDATE` for app role |

---

## 13. APPROVAL GATE

To proceed to Spec writing (Round 10), resolve:

```
OQ-1.1   WBS depth:                A / B / C        (reco: B — per-project configurable)
OQ-1.2   bac_integrity_status:     A / B / C        (reco: A — lock 2 values)
OQ-1.3   Spike formula names:      A / B / C        (reco: A — keep legacy)
OQ-1.4   PHASE_ID interpretation:  A / B / C        (reco: B — snapshot at creation)
OQ-1.5   Template promotion:       A / B / C        (reco: A — no promotion in v1.0)
OQ-1.6   CSV update conflict:      A / B / C / D    (reco: B — sparse update)
OQ-1.7   boq_origin values:        A / B / C        (reco: C — add HDI_Seed)
OQ-1.8   WBS code format:          A / B / C        (reco: A — auto-generated)
OQ-1.9   Unit conversion:          A / B / C        (reco: A — no conversion in v1.0)
OQ-1.10  BACIntegrityLedger owner: A / B / C        (reco: A — M02 owns, M07 API reads)

OQ-2 defaults: ACCEPT ALL / REJECT [list IDs] / MODIFY [specify]
```

---

## SHORTCUT REPLY

If you accept all my recommendations + OQ-2 defaults:

```
Use all your recommendations + ACCEPT OQ-2 defaults + GO Round 10
```

---

*v1.0 — Brief locked. Awaiting OQ resolutions to proceed to Spec.*
