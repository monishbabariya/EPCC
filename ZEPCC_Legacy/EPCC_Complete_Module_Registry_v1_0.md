# EPCC — Complete Module Registry
## Version 1.0
**Owner:** PMO Director / System Architect
**Created:** 2026-05-02
**Purpose:** Definitive registry of all modules in the EPCC system — existing, approved,
             and planned — across all phases. This is the single reference document for
             product roadmap decisions and build sequencing.
**Status:** Draft — Pending PMO Director Review

---

## CHANGE LOG

| Version | Date | Change Summary |
|---------|------|----------------|
| v1.0 | 2026-05-02 | Initial registry. 28 modules across 4 phases + 6 platform features. Based on gap analysis completed 2026-05-02. |

---

## SYSTEM ARCHITECTURE OVERVIEW

### Layer Definitions

| Layer | Role | Description |
|---|---|---|
| Strategic | Pre-investment intelligence | Portfolio selection, investment optimisation before project starts |
| L1 Command | System of record | Master data, contracts, authorisation — source of truth |
| L2 Control | Execution governance | All modules that track, measure, and control project delivery |
| L3 Intelligence | Insight and command | Dashboards, analytics, reporting, AI — consume but never write to source data |
| Platform | Cross-cutting capability | Features that serve all modules rather than being modules themselves |

### Navigation Structure (Final State — all phases complete)

```
EPCC Navigation
├── STRATEGIC
│   └── PIOE — Portfolio Investment Optimisation Engine
│
├── L1 COMMAND
│   ├── M01 — Project Registry
│   └── M23 — BG & Insurance Tracker (M01 sub-module)
│
├── L2 CONTROL — PLANNING & STRUCTURE
│   ├── M02 — Structure & WBS
│   ├── M03 — Planning & Milestones
│   ├── M12 — Document Control
│   └── M14 — QS Measurement Book
│
├── L2 CONTROL — EXECUTION
│   ├── M04 — Execution Capture
│   ├── M15 — Handover Management
│   ├── M16 — Site Diary
│   └── M20 — Labour & Workforce Management
│
├── L2 CONTROL — RISK & COMMERCIAL
│   ├── M05 — Risk & Change Control
│   ├── M06 — Financial Control
│   ├── M13 — Correspondence & Meeting Register
│   ├── M17 — Asset & Equipment Register
│   └── M19 — Claims Management
│
├── L2 CONTROL — GOVERNANCE & COMPLIANCE
│   ├── M08 — Gate Control
│   ├── M09 — Compliance Tracker
│   └── M21 — Training & Competency
│
├── L2 CONTROL — PERFORMANCE
│   └── M07 — EVM Engine
│
└── L3 INTELLIGENCE & COMMAND
    ├── M10 — EPCC Command
    ├── M11 — Action Register
    ├── M18 — Lender & Investor Reporting
    ├── M22 — Lessons Learned & Knowledge Base
    └── M26 — AI Portfolio Intelligence
```

---

## COMPLETE MODULE TABLE

### STRATEGIC LAYER

| ID | Module Name | Status | Phase | Layer | Decision It Enables | Spec Version | Build Weeks | Dependencies |
|---|---|---|---|---|---|---|---|---|
| PIOE | Portfolio Investment Optimisation Engine | Spec Complete | Phase 1 | Strategic | Which projects to invest in, in what sequence, to maximise portfolio IRR subject to capital/resource/regulatory constraints? | v2.1 | 8 | M01 (for push to M08) |

---

### L1 COMMAND LAYER

| ID | Module Name | Status | Phase | Layer | Decision It Enables | Spec Version | Build Weeks | Dependencies |
|---|---|---|---|---|---|---|---|---|
| M01 | Project Registry | Spec Complete | Phase 1 | L1 Command | Is this project authorised to exist in the portfolio, and are its foundational parameters — identity, contract, parties, dates, value, thresholds — correctly established as the master reference for all downstream modules? | v2.1 | 4 | None — foundation |
| M23 | BG & Insurance Tracker | Not Specced | Phase 2 | L1 Command (M01 sub-module) | Are all bank guarantees and insurance certificates current, and is the PMO alerted with sufficient lead time before any financial instrument expires? | — | 1 | M01 |

---

### L2 CONTROL — PLANNING & STRUCTURE

| ID | Module Name | Status | Phase | Layer | Decision It Enables | Spec Version | Build Weeks | Dependencies |
|---|---|---|---|---|---|---|---|---|
| M02 | Structure & WBS | Spec Complete | Phase 1 | L2 Control | Is the project's work breakdown structure, cost structure, and BOQ correctly defined and governed as the basis for all progress and financial measurement? | v2.0 | 4 | M01 |
| M03 | Planning & Milestones | Spec Complete | Phase 1 | L2 Control | Is the project schedule — baseline, milestones, procurement plan, resource allocation — correctly established and tracked such that schedule variances are detected before they become unrecoverable? | v2.3 | 5 | M01, M02 |
| M12 | Document Control | Not Specced | Phase 1 | L2 Control | What is the current approved revision of every drawing? Has every RFI been responded to within SLA? Have all contractor submittals been reviewed and approved? Is there an auditable record of every document issued to and from the project? | — | 6 | M01, M02 |
| M14 | QS Measurement Book | Not Specced | Phase 1 | L2 Control | What physical measurements underlie each billing claim, and is there a jointly agreed, auditable chain from field measurement to BOQ rate to billed amount that eliminates billing disputes? | — | 6 | M01, M02, M06 |

---

### L2 CONTROL — EXECUTION

| ID | Module Name | Status | Phase | Layer | Decision It Enables | Spec Version | Build Weeks | Dependencies |
|---|---|---|---|---|---|---|---|---|
| M04 | Execution Capture | Spec Complete | Phase 1 | L2 Control | Is the work being executed at the quality, safety, and pace specified — and is every departure from specification detected, recorded, and formally resolved? | v2.2 | 6 | M01, M02, M03 |
| M15 | Handover Management | Spec Complete | Phase 1 | L2 Control | Has every system been commissioned, every document transferred, every A-list item resolved, and every statutory approval received — such that the Handover Certificate can be issued without legal exposure and the DLP period begins with an agreed, defined baseline? | v1.0 | 6 | M01, M02, M03, M04, M08, M09 |
| M16 | Site Diary | Not Specced | Phase 2 | L2 Control | What happened on site today — what work was done, what conditions prevailed, what instructions were received, what caused any delay — and is this record contemporaneous, authenticated, and contractually defensible as evidence in any future claim? | — | 3 | M01, M04 |
| M20 | Labour & Workforce Management | Not Specced | Phase 2 | L2 Control | How many workers are deployed by which contractor in which trade on which package today, and does this match the planned deployment — and is BOCW and safety compliance maintained for the entire workforce? | — | 4 | M01, M02, M04 |

---

### L2 CONTROL — RISK & COMMERCIAL

| ID | Module Name | Status | Phase | Layer | Decision It Enables | Spec Version | Build Weeks | Dependencies |
|---|---|---|---|---|---|---|---|---|
| M05 | Risk & Change Control | Spec Complete | Phase 1 | L2 Control | What risks and issues threaten project delivery, what is the financial and schedule exposure, and have all scope changes been formally governed, priced, and approved before execution? | v2.3 | 6 | M01, M02, M03, M06 |
| M06 | Financial Control | Spec Complete | Phase 1 | L2 Control | Is the project financially controlled — is every cost budgeted, committed, accrued, and paid — and is cash flow, billing, sub-contract management, and retention governed with sufficient granularity to prevent financial surprises? | v2.1 | 6 | M01, M02, M04, M05 |
| M13 | Correspondence & Meeting Register | Not Specced | Phase 1 | L2 Control | Is there a complete, searchable, date-stamped register of every formal letter, notice, and meeting minute exchanged on the project — with formal acknowledgment of receipt — such that no party can later claim they were not notified or not in agreement? | — | 4 | M01 |
| M17 | Asset & Equipment Register | Not Specced | Phase 2 | L2 Control | Is every piece of installed equipment tracked from delivery through installation, commissioning, warranty, and handover — with serial numbers, commissioning certificates, and warranty expiry dates — such that the NABH assessor's equipment register requirement is fully met? | — | 4 | M01, M04, M15 |
| M19 | Claims Management | Not Specced | Phase 2 | L2 Control | What contractual claims — Extension of Time, Loss & Expense, quantum disputes — have been formally raised, what is the financial exposure, and what is the status of each claim through resolution, arbitration, or settlement? | — | 5 | M01, M05, M13 |

---

### L2 CONTROL — GOVERNANCE & COMPLIANCE

| ID | Module Name | Status | Phase | Layer | Decision It Enables | Spec Version | Build Weeks | Dependencies |
|---|---|---|---|---|---|---|---|---|
| M08 | Gate Control | Spec Complete | Phase 1 | L2 Control (Governance) | Has the project met every criterion — financial, technical, statutory, quality, safety, compliance — required to advance to the next phase, and is the GO/NO-GO decision documented, governed, and irreversible? | v2.1 | 5 | M01, M02, M03, M04, M05, M06, M07, M09 |
| M09 | Compliance Tracker | Spec Complete | Phase 1 | L2 Control | Have all statutory approvals, NABH requirements, regulatory licences, and safety certifications been obtained — and is the operational readiness of the facility sufficient to support revenue commencement within the target timeline? | v2.1 | 5 | M01, M08 |
| M21 | Training & Competency | Not Specced | Phase 3 | L2 Control | Does every person working on the project hold the certifications and competencies required for their role — and is the PMO alerted before any certification expires? | — | 3 | M01, M04 |

---

### L2 CONTROL — PERFORMANCE

| ID | Module Name | Status | Phase | Layer | Decision It Enables | Spec Version | Build Weeks | Dependencies |
|---|---|---|---|---|---|---|---|---|
| M07 | EVM Engine | Spec Complete | Phase 1 | L2 Control (Performance) | Is the project delivering value for money — and if current performance continues, where will it finish on cost and time? At what point can a threshold breach be detected and corrected before it becomes unrecoverable? | v3.0 | 6 | M01, M02, M03, M04, M05, M06 |

---

### L3 INTELLIGENCE & COMMAND LAYER

| ID | Module Name | Status | Phase | Layer | Decision It Enables | Spec Version | Build Weeks | Dependencies |
|---|---|---|---|---|---|---|---|---|
| M10 | EPCC Command | Spec Complete | Phase 1 | L3 Intelligence | What is the current health of every project in the portfolio — and what decisions need to be made today to prevent a project from deteriorating beyond recovery? | v2.2 | 6 | All M01–M09 |
| M11 | Action Register | Spec Complete | Phase 1 | L3 Command | What follow-up actions have been assigned to whom, on which project, by when — and which ones are overdue? | v1.0 | 2 | M01, M10 |
| M18 | Lender & Investor Reporting | Not Specced | Phase 2 | L3 Intelligence | Has the lender/investor received a structured, governed, tamper-proof monthly progress report in the format their loan agreement requires — without the PMO manually assembling data from multiple sources? | — | 3 | M01, M06, M07, M09, M10 |
| M22 | Lessons Learned & Knowledge Base | Not Specced | Phase 3 | L3 Intelligence | What patterns, failures, and insights from completed and live projects should inform how the next project is planned, contracted, and executed — and is this knowledge retrievable and acted upon? | — | 4 | All modules (read-only) |
| M26 | AI Portfolio Intelligence | Not Specced | Phase 3 | L3 Intelligence | What patterns in EPCC's own historical data predict project outcomes — and can the system proactively warn the PMO when a project's trajectory matches the signature of a previous project that failed? | — | 8 | M07, M10, M22, ≥ 5 completed projects worth of data |

---

## PLATFORM FEATURES
*(Not standalone modules — cross-cutting capabilities that serve multiple modules)*

| ID | Feature | Status | Phase | Scope | Build Weeks | Enables |
|---|---|---|---|---|---|---|
| PF01 | Mobile Field Platform | Not Specced | Phase 2 | PWA or React Native app for M04 field data capture: progress %, HSE incidents, QA checklists, M16 site diary, M15 punch list on-site. Offline-first with sync on connectivity restore. | 12 | Eliminates retrospective data entry. Field data quality improvement. |
| PF02 | BIM Integration | Not Specced | Phase 4 | Read-only linkage between M02 WBS/BOQ items and BIM model element IDs. M04 progress mapped to model. M12 drawings linked to model sheets. | 8 | Quantity verification, 4D scheduling, visual progress |
| PF03 | External Party Portal | Not Specced | Phase 3 | Read-only, role-scoped portal for clients, lenders, and NABH assessors. Renders M10 dashboard subsets, M18 lender reports, M09 compliance status. | 8 | Eliminates PDF-based reporting to external stakeholders |
| PF04 | Accounting System Integration | Not Specced | Phase 2 | Structured export of M06 financial data in Tally/SAP format. One-way export (EPCC → accounting system). Not a live sync. | 3 | Finance Lead no longer manually re-enters M06 data into Tally |
| PF05 | Offline Data Capture | Part of PF01 | Phase 2 | Service worker + local IndexedDB for M04 and M16 data entry when connectivity is unavailable. Sync queue on reconnect with `captured_at` timestamp (M04 v2.1). | Included in PF01 | Site data entry without internet dependency |
| PF06 | WhatsApp Bot Interface | Not Specced | Phase 3 | Two-way WhatsApp integration: receive decision queue items via WhatsApp, respond with approval/rejection via WhatsApp message, trigger site diary entry via voice-to-text. | 4 | Faster response from PMO Director on site or in meetings |

---

## PHASE ROADMAP

### Phase 1 — Production Ready (Before First Live Project at SG-1)
*All Phase 1 modules must be complete before the first project reaches SG-4 (project kick-off).*

| ID | Module | Build Weeks | Sequence Note |
|---|---|---|---|
| M01 | Project Registry | 4 | First to build — everything depends on it |
| M02 | Structure & WBS | 4 | Depends on M01 |
| M03 | Planning & Milestones | 5 | Depends on M01, M02 |
| M08 | Gate Control | 5 | Build in parallel with M01–M03; critical path |
| M04 | Execution Capture | 6 | Depends on M01–M03 |
| M05 | Risk & Change | 6 | Depends on M01, M02, M03 |
| M06 | Financial Control | 6 | Depends on M01, M02, M04, M05 |
| M07 | EVM Engine | 6 | Depends on M01–M06 |
| M09 | Compliance Tracker | 5 | Depends on M01, M08 |
| M10 | EPCC Command | 6 | Depends on all above |
| M11 | Action Register | 2 | Depends on M01, M10 |
| M12 | Document Control | 6 | Can build in parallel with M04–M06 |
| M13 | Correspondence & MOM | 4 | Can build in parallel with M05–M07 |
| M14 | QS Measurement Book | 6 | Depends on M02, M06 |
| M15 | Handover Management | 6 | Depends on M04, M08, M09 |
| PIOE | Investment Optimisation | 8 | Can build in parallel — feeds M08 SG-2/SG-3 |

**Phase 1 total: ~50 weeks (development), compressed to ~30 weeks with parallel tracks and 3-4 developers.**

### Phase 2 — Operational Enhancement (3–6 months post go-live)

| ID | Module/Feature | Build Weeks | Priority Driver |
|---|---|---|---|
| M16 | Site Diary | 3 | Legal defensibility for claims |
| M17 | Asset & Equipment Register | 4 | NABH accreditation requirement |
| M18 | Lender & Investor Reporting | 3 | Revenue driver — unlocks bank-financed projects |
| M19 | Claims Management | 5 | Commercial protection — dispute resolution |
| M20 | Labour & Workforce Management | 4 | BOCW compliance, site safety |
| M23 | BG & Insurance Tracker | 1 | Low effort, high financial risk protection |
| PF01 | Mobile Field Platform | 12 | Highest user impact — field data quality |
| PF04 | Accounting Integration | 3 | Finance team productivity |

**Phase 2 total: ~35 developer-weeks.**

### Phase 3 — Strategic Intelligence (12–18 months post go-live)

| ID | Module/Feature | Build Weeks | Priority Driver |
|---|---|---|---|
| M21 | Training & Competency | 3 | Regulatory compliance, NABH |
| M22 | Lessons Learned | 4 | Institutional knowledge retention |
| M26 | AI Portfolio Intelligence | 8 | Requires ≥ 5 completed projects of data |
| PF03 | External Party Portal | 8 | Client experience, lender engagement |
| PF06 | WhatsApp Bot Interface | 4 | PMO productivity, mobile governance |

**Phase 3 total: ~27 developer-weeks.**

### Phase 4 — Frontier Capabilities (24+ months)

| ID | Module/Feature | Build Weeks | Priority Driver |
|---|---|---|---|
| PF02 | BIM Integration | 8 | Industry direction — BIM mandates coming |
| PF05 | Offline Mode (if not in Phase 2) | Included in PF01 | — |

**Phase 4 total: ~8 developer-weeks.**

---

## MODULE DEPENDENCY MAP

```
PIOE ──────────────────────────────────────────────────────────► M08 (SG-2/SG-3 input)

M01 (Foundation)
 ├── M02 ──── M03 ──── M04 ──────────────────────────────────► M07
 │    │        │        │                                        │
 │    │        │        ├── M06 ──── M14 (QS Meas)              │
 │    │        │        │    └── M18 (Lender Reporting) ◄───────┤
 │    │        │        │                                        │
 │    │        │        ├── M05 ──── M19 (Claims)                │
 │    │        │        │    └── M13 (Correspondence)            │
 │    │        │        │                                        │
 │    │        │        ├── M15 (Handover) ◄─────────────── M09 ◄┘
 │    │        │        │    └── triggers SG-11 → M04 DLP
 │    │        │        │
 │    │        │        ├── M16 (Site Diary)
 │    │        │        └── M20 (Labour)
 │    │        │
 │    │        └── M12 (Document Control)
 │    │
 │    └── M17 (Asset Register)
 │
 ├── M08 (Gate Control) ◄─── M04, M05, M06, M07, M09, M15
 │
 └── M11 (Action Register)
      └── M10 (EPCC Command) ◄─── all modules
           ├── M22 (Lessons Learned) ◄─── M10
           └── M26 (AI Intelligence) ◄─── M10 + historical data
```

---

## SUMMARY COUNTS

| Category | Count |
|---|---|
| Total modules (PIOE + M01–M26) | 27 |
| Platform features (PF01–PF06) | 6 |
| **Total system items** | **33** |
| Phase 1 (must build first) | 16 modules |
| Phase 2 (first enhancement wave) | 8 modules/features |
| Phase 3 (intelligence layer) | 5 modules/features |
| Phase 4 (frontier) | 1 platform feature |
| Specs complete and locked | 11 (PIOE, M01–M11) |
| Specs complete, pending review | 1 (M15) |
| Not yet specced | 15 |

---

## NOTES ON SPEC STATUS

Modules with "Spec Complete" status have full 10-block specifications with zero open questions. They are ready for developer implementation. All are in the EPCC project knowledge base.

Modules with "Not Specced" status require a full 10-block specification before development begins. The module registry entry above provides the decision it enables and dependencies — sufficient to begin spec writing.

Build weeks are estimates for a single experienced full-stack developer per module (FastAPI backend + React frontend + tests). Parallel development with 3–4 developers can compress the Phase 1 timeline significantly.

---

*Registry v1.0 — pending PMO Director review.*
*Update when new modules are specced or phase decisions are made.*
*Memory file update required: §7.140 — Complete Module Registry v1.0.*
