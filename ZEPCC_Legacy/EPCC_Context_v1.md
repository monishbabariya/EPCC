# EPCC — Conversation Context File
## For Reuse in a New Chat Session
**Compiled:** 2026-04-30
**Purpose:** Restore full EPCC design context without repeating the conversation
**Instruction for new chat:** "Read this file and the referenced spec files. We are continuing the EPCC module specification project. The current state is described in Section 7."

---

## 1. WHAT WE ARE BUILDING

**Enterprise Portfolio Command Center (EPCC)**
A software product — not a spreadsheet system. A consequence-driven, closed-loop decision system for healthcare infrastructure project management in India.

**Governing definition:**
> EPCC is a system where Data → Insight → Trigger → Decision → Impact → Feedback → Data. Every feature must reduce decision delay, reduce ambiguity, or reduce dependency friction. If it does none of these, it does not belong in EPCC.

**Design philosophy source:** A philosophy document (`EPCC Behavioral Architecture for Healthcare EPC`) was reviewed. Its philosophy was adopted. Its database schemas were rejected as too thin. We rebuilt the data architecture from scratch using module specs.

**Pilot reference project:** KDMC 150-Bed Maternity, Cancer & Cardiology Hospital. Project code: `KDMC-001-DBOT`. Contract value ₹190 Cr. Month 13 of 35. CPI 1.34, SPI 0.93. 18 STOP gates active. The KDMC Excel workbook (`KDMC_CC_Transformed.xlsm`) is the domain model reference — not the product.

---

## 2. TECH STACK (LOCKED)

| Layer | Tool | Notes |
|-------|------|-------|
| Database (OLTP) | PostgreSQL | Multi-project, multi-portfolio from day one |
| Analytics (OLAP) | DuckDB | Inside Python, no separate server |
| Backend | Python + FastAPI | AI-assisted build |
| Frontend (operational) | React + TypeScript + Tailwind | Custom governance logic |
| Frontend (C-suite) | Power BI | Reporting only — cannot enforce rules |
| Data Lake | MinIO (on-prem) → S3 (cloud) | Identical API — zero migration cost |
| Containers | Docker + Docker Compose | On-prem now → Kubernetes/cloud later |
| Notifications | WhatsApp Business API (Meta official) + in-app | Third-party (Twilio/Gupshup) as integration layer only |
| ETL | Async Python + Cron (now) → Airflow (at scale) | |
| Auth | JWT + RBAC | Role-based from day one |
| Statistical engine | numpy + scipy | Holt's ES, OLS, SPC — in Python |
| Monte Carlo | numpy + scipy | Internal — no external tool dependency |

**Removed from stack:** Retool. Power BI is reporting only — not decision enforcement.

**Deployment:** On-premises now. Cloud later. Containerised from day one for portability.

---

## 3. MODULE SPEC PROCESS (HOW WE WORKED)

Each module spec follows this exact 10-block template. Every block must be complete before a module is locked. No open questions permitted at lock.

```
BLOCK 1  — Identity (Module ID, Name, Layer, Decision It Enables, Users)
BLOCK 2  — Scope Boundary (INCLUDES | EXCLUDES table)
BLOCK 3  — Data Architecture (entities + fields + source types)
BLOCK 4  — Data Population Rules (role permissions + entry methods + mandatory/optional)
BLOCK 5  — Filters & Views
BLOCK 6  — Business Rules (Rule ID | Trigger | Logic | Output | Speed Tier 🔴🟡🟢)
BLOCK 7  — Integration Points (Direction | Module | Data | Trigger | Speed Tier)
BLOCK 8  — Governance & Audit
BLOCK 9  — Explicit Exclusions
BLOCK 10 — Open Questions (must reach zero before module is locked)
```

**Speed tiers on every business rule:**
- 🔴 Real-time: executes immediately
- 🟡 2–4hr: medium loop (risk detection)
- 🟢 24hr: slow loop (daily reality update)

**Source types on every field — only four permitted:**
- `INPUT` — user enters
- `CALC` — system computes, never user-editable
- `LINK` — read from another module, read-only here
- `SYSTEM` — auto-generated (timestamps, IDs, audit)

---

## 4. ALL FILES PRODUCED

### Module Spec Files
| File | Module | Latest Version |
|------|--------|---------------|
| `M01_Project_Registry_v2.1.md` | Project Registry | v2.1 |
| `M02_Structure_WBS_v2.md` | Structure & WBS | v2.0 |
| `M03_Planning_Milestones_v2.3.md` | Planning & Milestones | v2.3 |
| `M04_Execution_Capture_v2.md` | Execution Capture | v2.0 |
| `M05_Risk_Change_v2.2.md` | Risk & Change Control | v2.2 |
| `M06_Financial_Control_v2.md` | Financial Control | v2.0 |
| `M07_EVM_Engine_v2.md` | EVM Engine | v2.0 |
| `M08_Gate_Control_v2.md` | Gate Control | v2.0 |
| `M09_Compliance_v2.md` | Compliance Tracker | v2.0 |
| `M10_EPCC_Command_v1.md` | EPCC Command | v1.0 (Block 10 pending) |

### Standards and Memory Files
| File | Purpose |
|------|---------|
| `EPCC_Standards_Memory_v4.0.md` | Master standards + all locked decisions (to be updated to v4.1) |
| `EPCC_Context_v1.md` | This file — conversation context for new chat reuse |

---

## 5. KEY DESIGN DECISIONS (ALL LOCKED)

### System-Wide
- **Geography:** 6-digit Indian pincode → embedded PincodeMaster table resolves state/city/district. No external API. No free-text state fields.
- **Project ID:** UUID auto-generated (SYSTEM). Human-readable `project_code` = INPUT (format: `[CLIENT]-[SEQ]-[TYPE]`, e.g. `KDMC-001-DBOT`).
- **Soft delete everywhere:** No hard deletes. `is_active = false` + timestamp + user. Permanent audit trail.
- **Consequence model:** Act within SLA → gate clears. Ignore SLA → auto-escalate → forced decision → governance breach logged. Not reward-driven.
- **Multi-portfolio, multi-program:** Hierarchy: `Portfolio → Program → Project` (all mandatory).
- **Accounting integration:** Agnostic stub (free-text `accounting_system` field). No vendor lock-in. EPCC functions without it. Connect Tally/Zoho/SAP later.

### M01 — Project Registry
- Multiple contracts per project. `contract_role` ENUM: Primary/Secondary/Specialist.
- Party master is global shared table. Risk diversification rule: party assigned to second active project in same category → PMO Director approval required.
- Report date change triggers full recalculation cascade (🔴 Real-time). Sequence: project_month → pct_time_elapsed → M03 PV → M07 EVM → M01 RAG → M10 cards.

### M02 — Structure & WBS
- WBS depth: variable via parent_id self-reference. Minimum 4 levels (KDMC standard). User-extensible upward.
- BOQ–WBS: Many-to-many both ways via `BOQWBSMap`. Each BOQ item must have exactly one primary WBS node (`is_primary_wbs = true`).
- BOQ split: structure + quantity in M02. Pricing (actual rate) in M06. Rate display is role-controlled at API level.
  - PMO Director / Finance Lead → actual rate
  - Project Director / Planning / QS → spiked rate (formula-obfuscated)
  - Site Manager / Read-Only → `[RESTRICTED]`
  - Three spike formulas: `Loaded / Indexed / Flat_Redacted`
- Unit master: 3-tier (Standard Core locked / Domain-Specific configurable / Custom governed via approval).
- Package templates: user-defined with optional system-shipped templates. Versioned. Delta tracked.
- CSV import: mandatory modal per session — Create_Only or Create_And_Update. No default. All-or-nothing.

### M03 — Planning & Milestones
- Baseline model: Single immutable baseline locked at SG-6 + Approved Extensions (`BaselineExtension` entity). No baseline re-versioning.
- Extension cause categories: Scope_Addition / Design_Change / Force_Majeure / Client_Delay / Contractor_Delay / Neutral_Event.
- `Neutral_Event`: requires contract clause reference + evidence. If contract clause blank → auto-reclassify to `Contractor_Delay` (Option A — contractor's supply chain risk).
- Billable flag and vendor performance flag auto-set by cause category. PMO Director can override with reason.
- PV distribution: S-curve with loading profiles (Civil = front-loaded, MEP = bell, Commissioning = back-loaded). System defaults, user overrides per activity.
- Look-ahead: filtered view of master schedule. Not a separate entity. N weeks configurable (default 4, range 2–12).
- Resource allocation: Role mandatory. Named person optional (confirmed when assigned).
- ResourceMaster: unified — Internal / Contractor / Consultant. Contractor/Consultant require party_id + contract_id from M01.
- Procurement split: M03 owns schedule (lead time, order/delivery/installation dates). M06 owns financial (vendor, PO value, payment).
- Schedule engine: inbuilt CPM algorithm. Also supports import from Primavera P6 and MSP via `ScheduleImport` entity. Post-baseline imports route through `BaselineExtension` workflow.
- Reporting period: Monthly (default) / Weekly / Daily / Event_Driven. Configurable per project.

### M04 — Execution Capture
- M04 is the only entry point for actual progress into the system.
- Progress measurement: method assigned per WBS node at M02 creation. Summary = Rollup (locked). Task = Units_Completed (default). Milestone = Milestone_Weighted (weighted avg of linked activities by planned duration). Subjective = supervisor override + min 30-char reason.
- No regression: pct_complete cannot decrease without supervisor approval + min 50-char reason (BR-04-001).
- Method lock: cannot change after first entry without PMO Director decision (BR-04-003).
- Rollup rule: parent EV derived from children weighted by BAC — M07 never independently computes parent EV (BR-04-020).
- Cadence: flexible entry. Default minimum 3 days. Critical path activities: 1 day. Overdue → Decision record.
- NCR lifecycle: Open → Response_Received → Remediation_In_Progress → Re_Inspection_Pending → Closed. Closure requires passed re-inspection. Critical/High NCRs block linked gate in M08.
- HSE: international classification (LTI / RWC / MTC / First_Aid / Near_Miss / Dangerous_Occurrence / Property_Damage) + BOCW regulatory fields. LTI + Dangerous_Occurrence → bocw_reportable = true. LTI → 0hr SLA immediate escalation.
- Contractor performance: composite score = Schedule(30%) + Quality(25%) + Safety(25%) + Procurement(10%) + PMO qualitative(10%). Qualitative missing → cap composite at 90%. Score < 50 → gate_eligibility_flag = false → blocks M08 gate. Feeds M01 Party master long-term rating.
- QA checklists: hybrid — system-shipped IS codes + NABH (locked, clone to modify) + user-defined (PMO Director approval).
- Material receipt: M04 owns physical receipt (quantity, condition, location). M06 owns GRN (financial). Linked via `material_receipt_id`. M03 actual_delivery_date confirmed only when M06 GRN created.
- Contractor scoring period: aligned with M03 reporting_period_type.

### M05 — Risk & Change Control
- Risk scoring: qualitative first (5×5 heat map). Red risks (score ≥ 15) auto-flagged for Monte Carlo.
- Risk categories: hybrid 3-tier (Core locked: Safety/Cost/Schedule/Quality/Regulatory; Domain subcategories configurable; Custom governed). Via `RiskCategoryMaster`.
- Risk materialisation: Risk → Issue with full lineage. Risk status → Materialised. Issue references source_risk_id.
- Contingency: every draw-down must link to specific Risk OR Issue. Unlinked blocked. PMO Director sole approver. Alerts: <30% balance → alert; <10% → critical + Board flag.
- Variation Order: Full 11-stage lifecycle (Draft → Arbitration). `vo_origin` ENUM: Risk_Driven / Issue_Driven / Proactive / Scope_Change / Client_Instruction. Risk_Driven requires risk_id. Issue_Driven requires issue_id. Others: no link required.
- EOT as VO type: approval auto-creates `BaselineExtension` in M03 with cause_category = Client_Delay.
- LD: fully auto-calculated from M03 contractor_delay_days × M01 ld_rate. No manual entry. Status = Draft until PMO Director reviews (pmo_reviewed = true) before → Notified. PMO can override calculated amount with reason (original preserved in audit).
- Monte Carlo: internal Python (numpy + scipy). Combined cost + schedule simulation. Captures delay → cost interdependency via `delay_cost_rate`. P50/P80/P90 outputs. Recommended contingency = P80 − P50.

### M06 — Financial Control
- 4-state cost tracking per package: Budgeted → Committed → Accrued → Paid. Budget-vs-Committed gap = primary risk indicator.
- RA Bill: hybrid billing method per package. Civil/MEP = % progress. Medical/Specialist = milestone. User configurable per package.
- Cashflow: full model (PV + payment terms + retention + advance recovery + TDS). Delayed payment tracking with interest accrual.
- Sub-contracts: full back-to-back. Both sides tracked (client in + sub-contractor out). `SubContractRetentionLedger` per sub-contract.
- GST + TDS: auto-calculated from M01 rates. Never user-editable. Not full tax ledger — that stays in accounting system.
- Package P&L: Revenue billed − Direct cost paid − Overhead allocated − Contingency consumed − LD paid. Overhead = BAC × overhead_pct (M01). Margin RAG: Green ≥ 20%; Amber 10–20%; Red < 10%; Critical < 0% → Board flag.
- Payment workflow: 5-step mandatory sequence. No step skippable. PMO Director only override with logged reason. Step 1: GRN Verified → Step 2: RA Bill Certified → Step 3: Deductions Calculated → Step 4: Finance Approved → Step 5: Payment Released.
- Accounting stub: `AccountingSync` entity. `accounting_system` = free text (no vendor lock-in). EPCC works without sync. Sync = Not_Applicable if no system connected.
- Multi-currency: `CurrencyMaster` + `ForexVariation`. Forex gain/loss > 5% → Decision record.
- Bank Guarantee: `BankGuarantee` entity. Performance/Advance/Retention/Warranty. Received or Issued direction. Expiry alerts: 60 days → notify; 30 days → amber; 14 days → Decision record; Expired → immediate.
- DBOT authority payments: `DBOTPaymentSchedule` entity. VGF, annuity, milestone grants. Linked to M03 milestones + M08 gates. IRR weight field.

### M07 — EVM Engine
- EV architectural boundary: M07 NEVER recomputes pct_complete. EV = pct_complete (M04) × BAC (M02). M04 enforces: No Regression (BR-04-001), Method Lock (BR-04-003), Rollup (BR-04-020).
- Subjective_Estimate EV flagged as low-confidence. Alert if > 15% of project EV.
- Recalculation: queued hybrid. Source changes (M03/M04/M06) → Standard queue → 4-hour cycle. M01 report date change → Immediate (bypasses queue). Multiple jobs same project same cycle → collapsed into one.
- EAC: three methods computed simultaneously. EAC_CPI (primary), EAC_SPI_CPI, EAC_ETC_Reestimate. PMO Director designates which feeds M10. ETC re-estimate persists until explicitly updated; flagged stale after 1 period.
- Portfolio EVM: absolute aggregation (ΣEV/ΣAC). Never average CPI. PMBOK-correct.
- Predictive breach detection: three-tier statistical engine.
  - Tier 1: Holt's Exponential Smoothing (α+β auto-optimised at ≥6 periods; fallback α=0.300, β=0.100).
  - Tier 2: OLS Linear Regression + R² confidence (High ≥0.80; Medium 0.60–0.79; Low <0.60).
  - Tier 3: SPC Control Charts ±3σ (activates at ≥8 periods). Out-of-control = point outside ±3σ OR 8 consecutive on same side.
- Trend analysis: CPI and SPI always on. EAC/TCPI/VAC/CV/SV = on-demand (PMO Director enables via `TrendConfig`).
- Plain language output for non-technical users (no statistics shown).

### M08 — Gate Control
- Gates: SG-0 to SG-11. Pre-project (SG-0/1): Documentary_Heavy. Pre-project (SG-2/3): MILP_Linked (IRR, NPV, DSCR, P80 cost, worst-case viability). MILP engine stubbed — `milp_run_id` field for future.
- Criteria: hybrid (system-verifiable auto-checked + documentary requires upload + named confirmation). Both required. Gate cannot pass without both.
- Override governance (tiered):
  - Conditional GO (1 criterion pending): PMO Director alone.
  - STOP Override (2+ failed): PMO Director + Portfolio Manager joint.
  - Gate Skip: NOT PERMITTED. API-blocked. Attempt = Critical ViolationLog entry.
- Conditional GO: mandatory `conditional_expiry_date`. Daily check: expiry passed + conditions unmet → auto-convert to STOP. `conditional_status` ENUM: Active/Met/Expired.
- Readiness: daily snapshot (% criteria met + days to gate + blocking list + trend). Alerts: <50% readiness with ≤14 days → Decision record. Declining 3 consecutive days → Decision record.
- Interface matrix: template-driven baseline (Hospital_DBOT_Interface_Standard + Infrastructure_EPC_Standard) + project-defined refinement. Critical interfaces block gate. Both discipline owners must formally sign off.
- Gate reopen: requires valid M05 Change Event ID. Ad-hoc reopens blocked. Prior passage preserved (is_active = false).
- Sector templates: system-shipped (locked) + user-created (PMO Director approval + versioning). Healthcare_NABH_DBOT auto-applied on healthcare project creation.
- Gate approval authority: configurable per gate per project. Authority types: PMO Director / Portfolio Manager / Board / Client_Authority / Lender / Regulatory_Body / Joint. Sequential enforcement.
- SG-6 passage: triggers M02 baseline lock + M03 baseline lock + M03 procurement activation.

### M09 — Compliance Tracker
- 4-level hierarchy: ComplianceCategory → ComplianceItem → ComplianceStandard → ComplianceClause (optional, for audit depth).
- NABH tracking: infrastructure-critical standards (≈80–100 items) from SG-4. Full standard tracking (≈600 standards) activates at SG-9.
- NABH pathways: Entry_Level / Pre_Accreditation / Full_Accreditation. Default at project initiation. Forward switches: PMO Director confirm. Backward switches: PMO Director approval + 100-char reason + ViolationLog entry.
- JCI: data-model ready (in `AccreditationFramework` table, is_active=false). Phase 2 — not active now. Zero rework when activated.
- Compliance timeline → M03 integration: grant date populates M03 milestone actual_date. Delays become schedule events → SPI impact → EVM recalculation.
- Operational readiness: parallel track in M09. Own score. Activates SG-7. Mandatory gate thresholds: SG-7 ≥40%, SG-9 ≥70%, SG-10 ≥90%. Feeds M08 as gate criterion.
- Resource readiness: per department per role. Recruitment % and training % tracked.
- Compliance checklists: tracking + guided compliance. Per-item: document name, format requirement, blank template URL, sample filled URL, compliance notes. Authority-specific variants. System-shipped (locked) + user-created (governed).
- Healthcare compliance items pre-loaded on project creation: NABH, AERB, Fire NOC, PCB CTE→CTO, MSEDCL, Building Permission, Lift Inspectorate, Electrical Inspector NOC, BOCW, Occupancy Certificate.

### M10 — EPCC Command
- M10 is a PURE READ-ONLY consumer. Never writes back to any upstream module. Never owns source data.
- Revenue readiness formula (locked from M09): RR = (L×0.30)+(O×0.25)+(C×0.15)+(S×0.15)+(E×0.10)+(IT×0.05). Hard caps: Licensing <80% → RR capped at 60%. Operational <70% → RR capped at 70%.
- Command views: role-based defaults + user customisable within permissions.
- Decision queue: priority-scored = SLA breach(40%) + financial impact(30%) + schedule impact(20%) + gate proximity(10%). Bands: Critical ≥75, High 50–74, Medium 25–49, Low <25. Critical unacknowledged >6hrs → auto-escalate.
- Revenue readiness display: waterfall + cap indicators. Cap reason auto-generated.
- Notifications: configurable multi-channel (in-app / WhatsApp / email) per user per severity. Critical = all channels, cannot be opted out. Quiet hours respected for non-Critical.
- Health index: 6-dimension composite 0–100. Default weights: EVM 25% / Schedule 20% / Cost 20% / Risk 15% / Quality 10% / Compliance 10%. PMO Director configurable with approval + version log. Health bands: Excellent 85+ / Good 70–84 / Watch 55–69 / At_Risk 40–54 / Critical <40.
- Benchmark: layered. Layer 1 = within-portfolio (primary). Layer 2 = external industry benchmark (secondary — for investor/board reporting).
- Executive Summary: screen (live, interactive) + PDF (frozen, timestamped, auditable artifact).
- WhatsApp: Meta official Business API (primary). Third-party (Twilio/Gupshup) as integration layer only, not core dependency.
- Health index weights: sector-specific system defaults + PMO Director configurable per project. Changes require approval + version log.

**Six additional M10 layers confirmed but not yet written into M10 v2.0 (next task):**
1. Data Confidence Score — per KPI confidence badge (High/Medium/Low) based on EV source quality, cadence breaches, missing rates, reconciliation status.
2. Decision Velocity Tracker — EPCC system's own performance metric (avg resolution time vs SLA, breach rate trend, decision backlog size).
3. Plain Language Narrative Engine — auto-generates 3–5 sentence board-readable interpretation per project per period.
4. Drill-Down Traceability — every KPI card hyperlinked to source record in source module. UI routing only, no new data entities.
5. Historical Replay — view portfolio state at any past period. Time-filter UI on existing snapshot entities.
6. Stakeholder Export Profiles — configurable PDF exports per stakeholder type (Client/Authority, Lender, Board, NABH Assessor). Information boundaries enforced.

---

## 6. GOVERNANCE STANDARDS (ALL LOCKED)

### Stage Gate System
```
Pre-Project: SG-0 → SG-1 → SG-2 → SG-3
Project:     SG-4 → SG-5 → SG-6 → SG-7 → SG-8 → SG-9 → SG-10 → SG-11
```
No gate skipped. All require formal approval. Override tiered. Gate skip = API-blocked permanently.

### Decision Escalation SLA (Standard — applies to every module)
| Time | Status | Action |
|------|--------|--------|
| 0–12 hrs | Normal | No action |
| 12–24 hrs | Attention | Reminder |
| 24–36 hrs | Risk | Escalate to next level |
| 36+ hrs | Critical | Auto-escalate to PMO Director + governance breach logged |

### EPMO Sizing (15–20 Projects)
PMO Director (1) + Portfolio Manager (1) + Project Controls Lead (1) + Planning Engineers (2) + Data Analyst (1) + Finance/Controls Specialist (1) + L&D/Capability (1) = 8–9 FTE total.

### Role Hierarchy (RBAC)
PMO Director → Portfolio Manager → Project Director → Finance Lead → Planning Engineer → QS Manager → Site Manager → Read-Only → System Admin

### 4-State Cost Tracking (Mandatory everywhere)
Budgeted → Committed → Accrued → Paid. Budget-vs-Committed gap = primary early warning indicator.

### 5-ID Governance Chain (Execution level)
Every data row: `BOQ_ID → WBS_ID → PKG_ID → CONTRACT_ID → PHASE_ID`. Zero orphan items. 100% valid chains required at gate passage.

---

## 7. CURRENT STATE — WHAT TO DO NEXT

### Immediate Next Action
**Write M10 v2.0** — incorporating:
1. Block 10 resolutions (all 4 confirmed — see Section 5, M10 decisions above)
2. Six additional layers (all 6 confirmed — see Section 5, M10 decisions above)

### After M10 v2.0
- Review M10 v2.0 (Block 10 must show zero open questions)
- Final review pass on all 10 module specs (confirm all Block 10s are zero)
- Update memory file to final version
- Move to Claude Code for implementation

### File to Update in Memory
`EPCC_Standards_Memory_v4.0.md` → update to `v4.1` with M10 Block 10 resolutions + 6 additional layers.

### Spec Files to Upload When Resuming
If resuming in a new chat, upload these files in order:
1. `EPCC_Context_v1.md` (this file) — for context
2. `EPCC_Standards_Memory_v4.1.md` — for design decisions
3. The specific module spec file(s) you are working on

---

## 8. NAMING CONVENTIONS (REFERENCE)

| ID Type | Format | Example |
|---------|--------|---------|
| Project ID | UUID (auto) | System-generated |
| Project Code | `[CLIENT]-[SEQ]-[TYPE]` | `KDMC-001-DBOT` |
| Package ID | `PKG-[##]` | `PKG-01` |
| WBS ID | `[L].[S].[T]` | `3.1.2` |
| BOQ ID | `BOQ-[###]` | `BOQ-001` |
| Risk ID | `RSK-[###]` | `RSK-001` |
| Issue ID | `ISS-[###]` | `ISS-001` |
| Gate ID | `SG-[#]` | `SG-6` |
| Decision ID | `DEC-[###]` | `DEC-001` |
| Phase | `DEV / DES / EPC / COM / OAM` | — |
| Contract Role | `Primary / Secondary / Specialist` | — |

---

## 9. FINANCIAL TERMS REFERENCE (KDMC — LOCKED IN M01)

| Parameter | Value | Source |
|-----------|-------|--------|
| Payment Terms | 15 days from invoice | Work Order Cl. 8.1 |
| Retention | 2% | Work Order Annexure V |
| Mobilisation Advance | 5% | Work Order Cl. 5.3 |
| DLP Period | 12 months | Work Order Cl. 12 |
| LD Rate | 0.5%/week | Work Order Cl. 9 |
| Max LD Cap | 10% of contract | Work Order Cl. 9 |
| Delay Interest | 2%/month | Work Order Cl. 8.2 |
| TDS Subcon | 1% (Sec 194C) | Work Order |
| TDS Professional | 10% (Sec 194J) | Work Order |
| Risk Buffer | 5% | Model assumption |
| GST Rate | 18% | Standard |
| Overhead % | 8% | Model assumption |
| Consultancy % | 3.5% | Model assumption |

---

*End of context file. Upload this file + `EPCC_Standards_Memory_v4.1.md` to restore full context in a new chat.*
