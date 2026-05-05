---
artefact: EPCC_BuildExecutionPlan_v1_0a
round: 31 (in-place patched R37 — stamp refresh only; no plan content change)
date: 2026-05-04
author: Monish (with Claude assist)
parent_specs: EPCC_BuildArchitecture_Spec_v1_0.md (Round 30; v1.0a R37 patch), EPCC_BuildArchitecture_Brief_v1_0.md (Round 23)
x8_version: v0.8
x9_version: v0.5
status: LOCKED
type: Build Execution Living Document
references_locked: All OQ-1 BuildArchitecture decisions (1.1-1.10) per CLAUDE.md §4; Cadence C1 + C1b per spec-protocol.md; ES-DB-001 schema-per-tenant per architecture.md §Multi-Tenancy
---

# EPCC Build Execution Plan — v1.0a

> **Type.** Build Execution Living Document. Governs the round-by-round sequence from Round 32 to Phase 1 + Platform completion. Living: updated as rounds execute, milestones gate, and audit findings emerge.
>
> **Authority.** All decisions in this plan honour `CLAUDE.md` §4 Locked Decisions, `EPCC_BuildArchitecture_Spec_v1_0` (R30 lock), and `spec-protocol.md` Cadence C1 + C1b.
>
> **Bottom line.** Spec-track and build-track run **in parallel** from Round 33 onward. First end-to-end demo at Round 38 (Week 6). Phase 1 minimum-viable system at Round 73 (Week 27). Phase 1 functional at Week 35. Phase 1 + Platform complete at Week 50.

---

## CHANGE LOG

| Version | Date | Author | Changes |
|---|---|---|---|
| v1.0a | 2026-05-04 | Monish (with Claude assist) | **R37 in-place patch (stamp refresh).** M6: x8_version v0.6a → v0.8; x9_version v0.4 → v0.5 (post-cascade per spec-protocol §In-Place Patch Convention). All §8 decisions and plan content unchanged. parent_specs reference updated to BuildArch Spec v1.0a (R37 stamp refresh). |
| v1.0 | 2026-05-04 | Monish (with Claude assist) | Initial lock. Locks dual-track architecture (spec-track + build-track in parallel), foundation set (10 modules: M34, M01, M02, M03, M04, M05, M06, M07, M08, M11), Phase 1 cutoff (33 modules), Phase 2 deferred (8 modules), revised round sequence R32-R51 for foundation + R52-R85 for Phase 1 secondary modules + R86+ for Platform features, audit cadence (after R45/R51/R65/R73), demo audience escalation (internal R38 → KDMC stakeholders R45 → external review R51), hire timeline (after G-2 Week 6). All §8 decisions confirmed. |

---

## §1 — Current State (post-R31 M05 Brief)

| Item | State | Reference |
|---|---|---|
| Build Architecture Spec v1.0 | LOCKED | `e415856` (R30) |
| M05 Brief v1.0 | LOCKED | `60d8171` (R31) |
| `main` HEAD at plan lock | post-`60d8171` | — |
| Modules with full Spec (Brief→Spec→Wireframes→Workflows complete) | 6 (M34, M01, M02, M03, M04, M06) | CLAUDE.md §3 |
| Modules with Brief only | 1 (M05) | This plan §3 |
| Lines of application code | **0** | — |
| Locked decisions in CLAUDE.md §4 | 27 | — |
| Round 29 audit findings open | 0 critical / 0 high / 0 medium / ~1 residual low | CLAUDE.md §4.1 |

---

## §2 — Dual-Track Architecture

### §2a Track A — Spec-Track

**Purpose:** Lock foundation + deepening module specs ahead of code that depends on them.

**Cadence:** C1 for Specs (one at a time per spec-protocol.md). C1b for Briefs / Wireframes / Workflows where peer modules permit batching (no upstream→downstream dependency in batch).

**Sequencing rule:** Dependency-first. M07 cannot lock before M02/M03/M04 (BAC/PV/EV inputs). M08 cannot lock before M07 (consumes EVM signals) and M06 (financial signals). Etc.

**Per-module artefact gate:** No build slice for module X starts until X's full 4-artefact set is LOCKED (Brief + Spec + Wireframes + Workflows). This was the user's plan-patch correction; it's the right discipline. Wireframes lock the rendered contract; Workflows lock runtime contracts.

### §2b Track B — Build-Track

**Purpose:** Convert locked specs into running, tested, deployable code.

**Cadence:** Each round = one thin slice OR one module-deepening lap with explicit acceptance criteria from that module's Spec Block 6 (or equivalent).

**Sequencing rule:** Per locked OQ-1.3 — thin slice (M34 → M01) first, then module deepening dependency-first.

### §2c Track Interleaving Rule

```
Spec-track and build-track run independently on the same round-number sequence.

A round is one OR the other (not both):
  Spec round  → produces an artefact in `SystemAdmin/` or `System Specs/`
  Build round → produces code in `apps/`, `packages/`, `infra/`, `scripts/`, `docs/adr/`

Constraint: a build round for module X requires X's full 4-artefact spec set LOCKED on `main`.
```

The rounds that violate this constraint (build-rounds before all 4 spec artefacts) do not exist in this plan. Round numbering is monotonic; track is identified by commit message convention (`spec(...)` vs `feat(...)` vs `chore(...)` vs `audit(...)`).

---

## §3 — Round-by-Round Sequence (R32 — R85)

### §3a Foundation Phase (R32 — R51)

10-module foundation: M34, M01, M02, M03, M04, M05, M06, M07, M08, M11. Build-track foundation = M34+M01 thin slice + 6 deep slices (M02+M03 / M04 / M06 / M05 / M07 / M08).

| # | Round | Track | Deliverable | Gate / Acceptance | Calendar |
|---|---|---|---|---|---|
| 1 | **R32** | Spec | M13 CorrespondenceMeetingRegister Brief v1.0 (C1b batch with M05) | All M13 OQ-1 + OQ-2 closed; correspondence ↔ M05 ↔ M11 contracts defined | Week 1 |
| 2 | **R33** | Spec | M05 Spec v1.0 + X8 v0.7 cascade scaffold | All M05 entities + BRs + 30 audit events locked; X8 v0.7 ENUMs scaffolded | Week 2 |
| 3 | **R34** | Spec | M13 Spec v1.0 + X8/X9 audit pass for M05+M13 batch | M13 entities + BRs locked; X8/X9 cascades for both modules audited | Week 2 |
| 4 | **R35** | Spec | M05 + M13 Wireframes (C1b batch) | Both Wireframes locked; role-default views per X9 | Week 3 |
| 5 | **R36** | Spec | M05 + M13 Workflows (C1b batch) | Both Workflows locked; M05 + M13 build-ready | Week 3 |
| 6 | **R37** | Build | Monorepo scaffold + 10 ADRs + CI workflow YAML + Docker Compose stack + Keycloak realm seed | Empty CI green on `main`; `make up` boots local stack; ADR-001 to ADR-010 committed | Week 4 |
| 7 | **R38** | Build | ENUM codegen pipeline live + first generated files | `scripts/codegen-enums.py --check` passes on `main`; X8 v0.6a → Python + TS round-trip clean | Week 4 |
| 8 | **R39** | Build | M34 thin slice scaffold (auth + Keycloak integration + 17-role seed + MFA setup) | AC-1, AC-2, AC-3 pass | Week 5 |
| 9 | **R40** | Build | M34 thin slice complete (AC-7 BR-tagged tests pass) | All M34 active-scope BRs (~10) tested; CI Stage 5 green | Week 5 |
| 10 | **R41** | Build | M01 thin slice scaffold (project create + read + tenant_id middleware live) | AC-4, AC-5, AC-6 pass; Postgres search_path routing verified | Week 6 |
| 11 | **R42** ⭐ | Build | M01 thin slice complete + **First End-to-End Demo (G-2)** | AC-8, AC-9, AC-10 pass; CI all 8 stages green on `main`; demo recorded | Week 6 |
| 12 | **R43** | Spec | M07 EVMEngine Brief v1.0 | All M07 OQ-1 closed; EAC algorithm choice locked; risk-adjusted EAC consumes M05 RISK_ADJUSTED_EAC_DELTA event | Week 7 |
| 13 | **R44** | Build | M02 deepening start (BOQ + BAC + Packages + BACIntegrityLedger) | All M02 active-scope BRs tested; CSVImport flow verified | Week 7 |
| 14 | **R45** | Spec | M07 Spec v1.0 + X8 v0.8 cascade scaffold | EVM metrics fully specced; X8 v0.8 ENUMs scaffolded | Week 8 |
| 15 | **R46** | Build | M02 deepening complete + M03 deepening start (Schedule + Baseline + Milestones + PV) | M02 BRs all green; M03 schedule create works | Week 8-9 |
| 16 | **R47** | Spec | M07 Wireframes | EVM dashboard + S-curve role views per X9 | Week 9 |
| 17 | **R48** | Spec | M07 Workflows | All M07 runtime flows + BR coverage matrix | Week 10 |
| 18 | **R49** | Build | M03 deepening complete | All M03 BRs green; PV S-curve renders; BaselineExtension flow tested | Week 10 |
| 19 | **R50** | Spec | M08 GateControl Brief v1.0 | All M08 OQ-1 closed; SG-passage trigger contract for M06 retention defined | Week 11 |
| 20 | **R51** | Build | M04 deepening start (Progress + NCR + Material + Contractor scoring) | ProgressEntry 3-state flow; NCR severity 4-tier; photo stub functional | Week 11 |
| 21 | **R52** | Spec | M08 Spec v1.0 + X8 v0.9 cascade scaffold | All 12 stage-gate transitions specced; X8 v0.9 scaffolded | Week 12 |
| 22 | **R53** | Build | M04 deepening complete | All M04 BRs green; NCR signals to M05 stub firing | Week 12 |
| 23 | **R54** | Spec | M08 Wireframes | Stage gate UI + role-default views | Week 13 |
| 24 | **R55** | Spec | M08 Workflows | All M08 runtime flows + cascade integration | Week 13 |
| 25 | **R56** | Build | M06 deepening start (Cost ledger + RA bills + Retention + Forex) | RA bill state machine end-to-end; tranched retention flows | Week 14 |
| 26 | **R57** | Build | M06 deepening complete + **Cost Ledger Live Demo (G-3)** + extend to KDMC stakeholders + advisor | Real KDMC pilot data flows: progress → milestone → RA bill → cost ledger; dual sign-off + retention working | Week 14 |
| 27 | **R58** | Spec | M11 ActionRegister Brief v1.0 | Decision Queue trigger taxonomy locked across M01-M08 + M14 + HDI | Week 15 |
| 28 | **R59** | Build | M05 deepening start (Risk + VO + EOT) | Risk register + 5×5 heatmap; VO lifecycle; EOT workflow | Week 15 |
| 29 | **R60** | Spec | M11 Spec v1.0 | All M11 entities + BRs locked | Week 16 |
| 30 | **R61** | Build | M05 deepening complete (LD + Contingency + EWN) | LD flow to M06 LD_ELIGIBLE_AMOUNT firing; Contingency drawdown live | Week 16 |
| 31 | **R62** | Spec | M11 Wireframes + Workflows (C1b batch — both small artefacts) | M11 build-ready | Week 17 |
| 32 | **R63** | Build | M07 deepening start (EVM Engine — full implementation) | EVM metrics computed from real progress + cost data | Week 17 |
| 33 | **R64** ⭐ | Build | M07 deepening complete + **EVM Engine Live Demo (G-4)** | EVM dashboard shows CPI, SPI, EAC computed from KDMC actuals | Week 18 |
| 34 | **R65** | Build | M08 deepening start (Stage Gate engine) | SG-passage events fire; M06 retention release reacts | Week 18-19 |
| 35 | **R66** ⭐ | Build | M08 deepening complete + **Stage Gates Live Demo (G-5)** | SG-9 passage triggers M06 tranche-1 retention release; full SG-0 to SG-11 chain | Week 19-20 |
| 36 | **R67** | Build | M11 ActionRegister deepening start | All Decision Queue triggers from all modules surface in central queue | Week 20 |
| 37 | **R68** ⭐ | Build | M11 deepening complete + **Foundation 10 Modules Complete (G-6)** | SLA monitors fire; full minimum-viable EPMO operational | Week 21 |

### §3b Phase 1 Secondary (R69 — R85)

After foundation, the remaining 23 Phase 1 modules deepen via dependency-first ordering. Both tracks continue interleaving.

| # | Round | Track | Deliverable | Calendar |
|---|---|---|---|---|
| 38 | **R69-R72** | Spec + Build | M14 QSMeasurementBook full cycle (Brief → Spec → Wireframes → Workflows → deepening) | Week 22-23 |
| 39 | **R73** | Build | M12 DocumentControl deepening + M04 photo stub migration | Week 24 |
| 40 | **R74-R75** | Spec + Build | HDI v1.0 (full KDMC workbook → EPCC migration) | Week 25-26 |
| 41 | **R76** ⭐ | Build | **Phase 1 MVP Demo (G-7)** | Week 27 |
| 42 | **R77-R85** | Spec + Build | Phase 1 secondary modules: M09 ComplianceTracker, M22 LessonsLearned, M27 DesignControl, M28 InterfaceManagement, M30 VendorMasterPQ, M31 HSESafety, M32 BenefitRealization, M33 StakeholderRegister, M16 SiteDiary, M20 LabourWorkforce, M21 TrainingCompetency, M23 BGInsuranceTracker, M24 ClinicalOperationalReadiness, M25 (placeholder), M26 AIPortfolioIntelligence, M10 EPCCCommand, M29 TenderingAward, M17 AssetEquipmentRegister, M18 LenderInvestorReporting | Weeks 28-35 |
| 43 | **R86+** | Build | **Phase 1 Functional (33 modules) (G-8)** | Week 35 |

### §3c Phase 2 (R87+)

After Phase 1 functional, Phase 2 modules + platform features (PF01-PF06) + production hardening. Calendar Weeks 36-50.

Phase 2 deferred modules (per §6):
- M19 ClaimsManagement (formal claims; needs M05 Phase 1 + portal)
- M15 HandoverManagement (DLP-end retention path)
- PF01 MobileFieldPlatform
- PF02 BIMIntegration
- PF03 ExternalPartyPortal
- PF04 AccountingIntegration
- PF05 OfflineCapture (subsumed in PF01)
- PF06 WhatsAppBot

---

## §4 — Calendar / Weeks Projection

| Week | Major Outputs | Demo / Milestone |
|---|---|---|
| Week 1 | R32 M13 Brief | — |
| Week 2 | R33 M05 Spec + R34 M13 Spec | — |
| Week 3 | R35 M05+M13 Wireframes + R36 M05+M13 Workflows | — |
| Week 4 | R37 Scaffold + R38 ENUM codegen | Empty CI green |
| Week 5 | R39 M34 thin slice scaffold + R40 M34 complete | — |
| **Week 6** | R41 M01 scaffold + **R42 ⭐ FIRST DEMO (G-2)** | **🎯 First End-to-End Demo** (internal) |
| Week 7 | R43 M07 Brief + R44 M02 deepening start | — |
| Week 8 | R45 M07 Spec + R46 M02 done + M03 start | — |
| Weeks 9-10 | R47-R49 (M07 Wireframes + Workflows + M03 done) | — |
| Week 11 | R50 M08 Brief + R51 M04 deepening start | — |
| Weeks 12-13 | R52-R55 (M08 Spec + Wireframes + Workflows + M04 done) | — |
| **Week 14** | R56-R57 (M06 deepening done) → **🎯 Cost Ledger Live (G-3)** — extend demo to KDMC stakeholders + advisor | **🎯 Cost Ledger Live** |
| Weeks 15-16 | R58-R61 (M11 Brief + Spec + M05 deepening done) | — |
| Week 17 | R62-R63 (M11 Wireframes/Workflows + M07 deepening start) | — |
| **Week 18** | R64 ⭐ M07 deepening complete | **🎯 EVM Engine Live (G-4)** |
| Weeks 19-20 | R65-R66 (M08 deepening done) | **🎯 Stage Gates Live (G-5)** |
| **Week 21** | R67-R68 (M11 deepening done) → **🎯 Foundation 10 Modules Complete (G-6)** — extend demo to lender / external review | **🎯 Foundation Complete + External Review** |
| Weeks 22-26 | R69-R75 (M14 + M12 + HDI v1.0) | — |
| **Week 27** | R76 ⭐ **🎯 Phase 1 MVP Demo (G-7)** — full KDMC pilot data | **🎯 Phase 1 MVP** |
| Weeks 28-34 | R77-R85 (Phase 1 secondary modules — 16 modules) | — |
| **Week 35** | **🎯 Phase 1 Functional System (G-8)** — 33 modules complete | — |
| Weeks 36-50 | Platform features (PF01-PF06) + Phase 2 deferred modules + production hardening | — |
| **Week 50** | **🎯 Phase 1 + Platform Complete (Phase 2 ready)** | — |

---

## §5 — Decision Gates & Milestones

| Gate ID | Trigger | Acceptance | Demo Audience |
|---|---|---|---|
| **G-1** Foundation Specs Locked | After R55 M08 Workflows | M34, M01, M02, M03, M04, M05, M06, M07, M08, M11, M13 all have full 4-artefact spec set LOCKED | Internal |
| **G-2** First Demo (M34+M01 thin slice) | R42 / Week 6 | All 10 acceptance criteria (AC-1 to AC-10) pass; CI 8 stages green on `main` | Internal (Monish review) |
| **G-3** Cost Ledger Live | R57 / Week 14 | Real KDMC pilot data flows: progress → milestone → RA bill → cost ledger; dual sign-off + retention working | **KDMC stakeholders + advisor** |
| **G-4** EVM Engine Live | R64 / Week 18 | EVM metrics (CPI, SPI, EAC, ETC, TCPI, VAC) computed from real data + match manual recompute on KDMC sample | KDMC stakeholders |
| **G-5** Stage Gates Live | R66 / Week 19-20 | SG-9 passage triggers M06 tranche-1 release; SG-11 triggers M15 DLP signal → M06 tranche-2 (Phase 2 stub); full chain auditable | KDMC stakeholders |
| **G-6** Foundation Complete (10 modules) | R68 / Week 21 | All foundation BRs green; SLA monitors fire; full minimum-viable EPMO operational | **Lender / external review** |
| **G-7** Phase 1 MVP | R76 / Week 27 | All 14 foundation+secondary modules running with full KDMC data via HDI; PMO dashboard operational | Lender + KDMC + external review |
| **G-8** Phase 1 Functional | R85+ / Week 35 | All 33 Phase 1 modules at module-deepening complete state | Phase 2 readiness gate |
| **G-9** Phase 1 + Platform | R95+ / Week 50 | All 33 Phase 1 modules + Phase 2 deferred (8 modules) operational | Phase 2 entry |

### §5a Re-open Triggers per Gate

Per CLAUDE.md §4 "Locked Decisions — Do Not Revisit", gates do not re-open without explicit trigger:

| Gate | Re-open Trigger |
|---|---|
| G-1 | Cross-module contract drift discovered during build (cascade note + PR) |
| G-2 | AC failure during R42 — fix-and-retry loop |
| G-3 | Data integrity break; BACIntegrityLedger drift |
| G-4 | EVM math doesn't match expected output (recompute audit) |
| G-5 | M08 ↔ M06 contract drifts |
| G-6 | SLA monitor failures; Decision Queue overflow |
| G-7 | KDMC migration data loss / corruption |
| G-8 | Phase 2 readiness gate; user decision to advance |
| G-9 | Phase 2 entry; user decision |

---

## §6 — Phase 1 vs Phase 2 Cutoff (locked §8.6)

### §6a Phase 1 — 33 modules

| Layer | Modules |
|---|---|
| L0 Strategic | M16 SiteDiary, M17 AssetEquipmentRegister, M18 LenderInvestorReporting (defer M19 ClaimsManagement to Phase 2) |
| L1 Command | M01 ProjectRegistry, M23 BGInsuranceTracker, M24 ClinicalOperationalReadiness, M28 InterfaceManagement |
| L2 Planning | M02 StructureWBS, M03 PlanningMilestones |
| L2 Execution | M04 ExecutionCapture, M14 QSMeasurementBook, M27 DesignControl, M12 DocumentControl, M13 CorrespondenceMeetingRegister |
| L2 Risk/Commercial | M05 RiskChangeControl, M06 FinancialControl, M22 LessonsLearned |
| L2 Compliance | M09 ComplianceTracker, M25, M30 VendorMasterPQ, M31 HSESafetyManagement |
| L2 Performance | M07 EVMEngine, M26 AIPortfolioIntelligence, M32 BenefitRealization |
| L3 Intelligence | M08 GateControl, M10 EPCCCommand, M11 ActionRegister, M29 TenderingAward, M33 StakeholderRegister (defer M15 HandoverManagement to Phase 2) |
| Workforce | M20 LabourWorkforce, M21 TrainingCompetency |
| System | M34 SystemAdminRBAC, HDI HistoricalDataImport |

**Total Phase 1: 33 modules.**

### §6b Phase 2 — 8 modules

| Module | Reason for Deferral |
|---|---|
| M19 ClaimsManagement | Formal claims work; needs M05 Phase 1 stable + PF03 ExternalPartyPortal for client sign-off |
| M15 HandoverManagement | DLP-end retention release path; per M06 v1.1 cascade note (R29 H6 Option B); needs Phase 1 M06+M08 stable first |
| PF01 MobileFieldPlatform | Phase 2 mobile track |
| PF02 BIMIntegration | Phase 2 BIM integration |
| PF03 ExternalPartyPortal | Phase 2 portal access (CLIENT_VIEWER, LENDER_VIEWER, NABH_ASSESSOR, CONTRACTOR_LIMITED) |
| PF04 AccountingIntegration | Phase 2 ERP integration |
| PF05 OfflineCapture | Subsumed in PF01 per legacy registry |
| PF06 WhatsAppBot | Phase 2 conversational interface |

**Audit registry note:** `architecture.md` Module Registry currently shows 39 modules (M-modules + PF + HDI). VersionLog adds M20 + M21 = **41 total**. Architecture.md has a 2-module omission (M20, M21) flagged for a future audit round; not blocking this plan.

---

## §7 — Audit Cadence (locked §8.8)

Per Round 29 precedent: audit rounds insert as `audit/round-{N}-{theme}` branches, ~1-2 weeks each, calendar-absorbed.

| Audit Round | Trigger | Scope |
|---|---|---|
| **Audit/R45+** | After Cost Ledger Demo (G-3) | M02 + M03 + M06 contract integrity; cascade notes if implementation drifted from spec |
| **Audit/R51+** | After Foundation 10 Complete (G-6) | M07 ↔ M08 ↔ M06 commercial-loop audit; verify EVM math + stage-gate triggers match spec |
| **Audit/R65+** | After M14 + M12 + HDI v1.0 | KDMC migration verification; BOQ-grain ↔ WBS-grain handoff; pre-Phase-1-MVP audit |
| **Audit/R73+** | After Phase 1 MVP (G-7) | Full system audit pre-secondary-modules |
| **Audit/R85+** | After Phase 1 Functional (G-8) | Pre-Phase-2 audit |

---

## §8 — Demo Audience Escalation (locked §8.5)

| Milestone | Audience | Why |
|---|---|---|
| G-2 First Demo (R42 / W6) | **Internal only** (Monish + AI assist) | Thin slice = mock-quality KDMC seed; UI functional not polished |
| G-3 Cost Ledger Live (R57 / W14) | **KDMC stakeholders + advisor** | Real commercial value visible; stakeholder credibility maximised |
| G-4 EVM Live (R64 / W18) | KDMC stakeholders | Continuation of G-3 audience |
| G-5 Stage Gates Live (R66 / W19-20) | KDMC stakeholders | Continuation |
| G-6 Foundation Complete (R68 / W21) | **Lender / external review** | Full minimum-viable EPMO; defensible against external scrutiny |
| G-7 Phase 1 MVP (R76 / W27) | Lender + KDMC + external | Full pilot data via HDI |
| G-8 Phase 1 Functional (R85 / W35) | All stakeholders | Production-ready validation |

---

## §9 — Hire Timeline (locked §8.7)

| Trigger | Role | Calendar | Why |
|---|---|---|---|
| G-2 First Demo (R42 / W6) | First contract developer (full-stack) | Week 6 | Working system to onboard against; spec-only state is unhireable |
| G-3 Cost Ledger Live (R57 / W14) | First QA / test engineer | Week 14 | BR-tagged-test discipline + 200+ BRs needs dedicated test ownership |
| G-5 Stage Gates Live (R66 / W19-20) | DevOps / SRE | Week 19-20 | Multi-tenant production prep; ES-DR-002 backup discipline; observability stack |
| G-6 Foundation Complete (R68 / W21) | Second developer | Week 21 | Spec-track + build-track parallel becomes 2-engineer concern |
| G-7 Phase 1 MVP (R76 / W27) | UX designer + full-time PMO operator | Week 27 | Production-grade UI polish + KDMC operator shadowing |

**If cash is tight:** defer first hire to G-3 (Week 14). Cost Ledger Live = strongest fundraising / hiring proof point.

---

## §10 — Risk Management (carry-forward from §6 of original plan + corrections)

### §10a Anticipated Failure Modes

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Spec found wrong during code | High (70%+) | Low-Medium (cascade-note pattern in place) | `feat/{module}-cascade-{version}` branch + code change in same PR; CI Stage 5 BR-tagged-test gate detects drift |
| Round 29-style audit needed | Medium (40%) | Medium (5 PR audit cycle adds 1-2 weeks) | Audit early per slice per §7; don't accumulate |
| Keycloak operational burden | Medium | Medium | If burden > 4 hrs/month at end of B-2, revisit OQ-1.4 with Auth0 fallback ADR-004 amendment |
| Schema-per-tenant performance issue | Low (single pilot) | Low | ES-DB-001 §7.137 trigger: >50 tenants. N/A at pilot |
| KDMC workbook→EPCC migration error | Medium | High (could block Phase 1 MVP) | HDI v0.1 prototype at R37 is a smoke test; full HDI v1.0 at R74-R75 isolated as own slice |
| C1b cadence breakdown under pressure | Low | Medium | C1b applies to peer modules; if peer-pressure breaks, revert to C1 |
| Test coverage drops below floor | Medium | High (CI Stage 4 blocks merge) | 80% line coverage floor enforced; backfill tests as part of cascade PRs |
| Wireframe ↔ code drift | High | Low (acknowledged limit) | Manual sync per cascade; v1.0 acceptance |
| Single-developer bottleneck | Certain | Variable | AI assist on both tracks; review-cycle is the constrained resource; first hire after G-2 |
| Vendor library breaking changes | Medium per major bump | Low (pinned versions) | All major versions pinned per Build Arch Spec Block 3b; bumps require ADR |

---

## §11 — Locked Decisions Summary (§8.1 — §8.9)

| # | Decision | Locked Answer |
|---|---|---|
| 8.1 | Dual-track approach | ✅ Spec-track + build-track parallel from R37 |
| 8.2 | Foundation set | ✅ 10 modules: M34, M01, M02, M03, M04, M05, M06, M07, M08, M11 |
| 8.3 | Round numbering | ✅ Single sequence (monotonic R32, R33, R34...); track identified by commit message convention |
| 8.4 | Slice 2 modules | ✅ M02 + M03 (Slice 2 deepening per §3a) |
| 8.5 | First demo audience | ✅ Internal-only at R42; KDMC stakeholders + advisor at R57 (G-3); lender / external review at R68 (G-6) |
| 8.6 | Phase 1 cutoff | ✅ 33 modules in Phase 1 / 8 modules deferred to Phase 2 (per §6) |
| 8.7 | Hire timeline | ✅ First hire after G-2 (Week 6) — full-stack developer; subsequent hires per §9 |
| 8.8 | Audit cadence | ✅ After R45 (G-3) / R51 (G-6 entry) / R65 (pre-MVP) / R73 (post-MVP) / R85 (pre-Phase-2) |
| 8.9 | Plan governance | ✅ Locked as `EPCC_BuildExecutionPlan_v1_0.md` (this file) |

---

## §12 — What Counts as "Done" Per Round

Each round produces:

**Spec round:**
- File on disk in `SystemAdmin/` or `System Specs/` with appropriate audit stamp (Format A or B per spec-protocol.md)
- Status: LOCKED
- All quality gates per spec-protocol.md and per-artefact-type rules pass
- Commit message: `spec(M{XX}): {Name} {Type} v{X}.{Y} — Round {N}` or `chore(spec): ...`

**Build round:**
- Code in `apps/`, `packages/`, `infra/`, `scripts/`, or `docs/`
- All 8 CI stages green on the round's branch (or `main` for governance)
- BR-tagged tests for active-scope BRs all present and passing
- Acceptance criteria from corresponding spec Block 6 (or equivalent) all pass
- Commit message: `feat(M{XX}): {description} — Round {N}` or `feat(scaffold): ...`

**Audit round:**
- Findings catalogue + remediation PR series per Round 29 precedent
- Branch: `audit/round-{N}-{theme}`
- Closing commit references all closed findings

---

## §13 — Living-Document Update Protocol

This plan is a Living Document. Updates land via direct commit to `main` with commit message:

```
chore(plan): EPCC_BuildExecutionPlan v1.0 — {what changed}
```

Triggers for plan update:
- Round delivered → update §3 with actual completion date and any deviation notes
- Gate passed → update §5 with pass/fail + any AC failures resolved
- Hire made → update §9 with name + role start date
- Audit complete → update §7 with findings count
- Calendar slips > 1 week → update §4 + flag to Monish
- Locked decision changes (§11) → require new round + governance commit

Major revision (v2.0) only on:
- Phase 1 cutoff change
- Track architecture change
- Foundation set change

---

*v1.0 — Plan LOCKED 2026-05-04. Round 32 (M13 Brief) authorised to dispatch on plan commit. Single source of truth for round-by-round execution from R32 to G-9 (Phase 1 + Platform Complete).*
