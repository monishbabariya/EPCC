# EPCC — Master Version Log
## Version 1.1
**Owner:** PMO Director
**Created:** 2026-05-03 | **Last Reconciled:** 2026-05-03 (Round 18 lock — Rounds 1–18 catch-up)
**Status:** Living Document
**Update Frequency:** On every artefact creation, modification, or status change.

---

## 1. PURPOSE

Single source of truth for the version, status, and ownership of every EPCC artefact. Replaces all per-file change logs (per Improvement I1).

---

## 2. STATUS ENUM

| Status | Meaning |
|---|---|
| `Draft` | In active authorship — not yet ready for review |
| `Review` | Submitted to PMO Director for review |
| `Locked` | Reviewed + approved. Cannot change without Major version bump |
| `Archived` | Superseded by a newer version. Read-only reference. |
| `Deprecated` | No longer applicable. Retained for audit trail only. |

---

## 3. CURRENT REGISTRY STATE — 2026-05-03 (post Round 18)

### 3.1 Governance Files (00_Governance)

| File | Type | Version | Status | Author | Last Updated | Notes |
|---|---|---|---|---|---|---|
| EPCC_NamingConvention_v1_0.md | Standards | v1.0 | Locked | PMO Dir | 2026-05-03 | Initial creation, Round 0 |
| EPCC_FolderIndex_v1_0.md | Standards | v1.0 | Locked | PMO Dir | 2026-05-03 | Initial creation, Round 0 |
| EPCC_VersionLog_v1_0.md | Log | v1.0 | Living | PMO Dir | 2026-05-03 | This file |
| EPCC_ModuleRegistry_v1_0.md | Registry | — | Pending | PMO Dir | — | Will replace legacy v1.0 after audit acceptance |
| EPCC_StandardsMemory_v1_0.md | Standards | — | Pending | PMO Dir | — | Consolidation of legacy v5.3 + amendments — will be created in Round N |
| EPCC_LegacyManifest_v1_0.md | Manifest | v1.0 | Locked | PMO Dir | 2026-05-03 | Initial creation, Round 0 |
| EPCC_DevSkillsRequired_v1_0.md | Reference | v1.0 | Locked | PMO Dir | 2026-05-03 | Initial creation, Round 0 |

### 3.2 Audit Files (12_Audits)

| File | Round | Version | Status | Author | Last Updated |
|---|---|---|---|---|---|
| AUDIT_Round00_ExistingSpecs_v1_0.md | 00 | v1.0 | Locked | PMO Dir | 2026-05-03 |

### 3.3 Strategic Layer (01_Strategic)

| File | Type | Version | Status | Notes |
|---|---|---|---|---|
| PIOE_PortfolioInvestmentOptimisation_Brief_v1_0.md | Brief | — | Pending | Round TBD |
| PIOE_PortfolioInvestmentOptimisation_Spec_v1_0.md | Spec | — | Pending | Re-issue of legacy v2.1 |
| PIOE_PortfolioInvestmentOptimisation_Wireframes_v1_0.html | Wireframes | — | Pending | — |
| PIOE_PortfolioInvestmentOptimisation_Workflows_v1_0.md | Workflows | — | Pending | — |

### 3.4 L1 Command (02_L1_Command)

| File | Type | Version | Status | Notes |
|---|---|---|---|---|
| M34_SystemAdminRBAC_*_v1_0.* | Brief/Spec/WF/WL | v1.0 | **Locked** | Rounds 1–4 (foundation) |
| M01_ProjectRegistry_*_v1_0.* + v1.1 + v1.2 cascade notes | Brief/Spec/WF/WL + cascade notes | v1.0 (full) + v1.1 (cascade note) + v1.2 (cascade note) | **Locked** | Rounds 5b–8 + Round 16 + Round 18 audit (v1.1 cascade backfilled). v1.1 adds `Project.min_wbs_depth`; v1.2 removes `Project.reporting_period_type` (ownership → M03) |
| M23_BGInsuranceTracker_*_v1_0.* | Brief/Spec/WF/WL | — | Pending | New (was unspecced) |

### 3.5 L2 Planning (03_L2_Planning)

| Module | Status | Notes |
|---|---|---|
| M02 StructureWBS | **Locked** v1.0 | Rounds 9–12 |
| M03 PlanningMilestones | **Locked** Spec v1.1 / Brief v1.1 / Wireframes v1.0 / Workflows v1.0 | Rounds 15–18. Spec v1.1 cascade in Round 18 added Appendix C (28 audit events) + BR-03-033 (CP transactionality) + BR-03-034 (reporting_period_type atomic rollback) |
| M12 DocumentControl | Pending | New (Phase 1 critical, was unspecced) |
| M14 QSMeasurementBook | Pending | New (Phase 1 critical, was unspecced) |
| M27 DesignControl | Pending | New (proposed v2.3) |
| M28 InterfaceManagement | Pending | New (proposed v2.3) |

### 3.6 L2 Execution (04_L2_Execution)

| Module | Status | Notes |
|---|---|---|
| M04 ExecutionCapture | Pending | Re-issue of legacy v2.2 (currently amendment file) |
| M15 HandoverManagement | Pending | Re-issue of legacy v1.0 |
| M16 SiteDiary | Pending | New |
| M20 LabourWorkforce | Pending | New |

### 3.7 L2 RiskCommercial (05_L2_RiskCommercial)

| Module | Status | Notes |
|---|---|---|
| M05 RiskChange | Pending | Re-issue of legacy v2.3 (currently amendment file) |
| M06 FinancialControl | Pending | Re-issue of legacy v2.1 |
| M13 CorrespondenceRegister | Pending | New |
| M17 AssetEquipmentRegister | Pending | New |
| M19 ClaimsManagement | Pending | New |
| M29 TenderingAward | Pending | New (proposed v2.3) |
| M30 VendorMasterPQ | Pending | New (proposed v2.3) |

### 3.8 L2 Compliance (06_L2_Compliance)

| Module | Status | Notes |
|---|---|---|
| M08 GateControl | Pending | Re-issue of legacy v2.1 |
| M09 ComplianceTracker | Pending | Re-issue of legacy v2.1 |
| M21 TrainingCompetency | Pending | New |
| M24 ClinicalOperationalReadiness | Pending | New (proposed v2.3) |
| M31 HSESafetyManagement | Pending | New (proposed v2.3) |

### 3.9 L2 Performance (07_L2_Performance)

| Module | Status | Notes |
|---|---|---|
| M07 EVMEngine | Pending | Re-issue of legacy v3.0 |

### 3.10 L3 Intelligence (08_L3_Intelligence)

| Module | Status | Notes |
|---|---|---|
| M10 EPCCCommand | Pending | Re-issue of legacy v2.2 |
| M11 ActionRegister | Pending | Re-issue of legacy v1.0 |
| M18 LenderInvestorReporting | Pending | New |
| M22 LessonsLearned | Pending | New (Phase 3) |
| M26 AIPortfolioIntelligence | Pending | New (Phase 3) |
| M32 BenefitRealization | Pending | New (proposed v2.3) |
| M33 StakeholderRegister | Pending | New (proposed v2.3) |

### 3.11 Platform Features (09_Platform_Features)

| Feature | Status | Notes |
|---|---|---|
| PF01 MobileFieldPlatform | Pending | Promoted to Phase 1 in v2.3 |
| PF02 BIMIntegration | Pending | Phase 4 |
| PF03 ExternalPartyPortal | Pending | Phase 3 |
| PF04 AccountingIntegration | Pending | Phase 2 |
| PF05 OfflineCapture | Pending | Subsumed in PF01 per registry |
| PF06 WhatsAppBot | Pending | Phase 3 |

### 3.12 Cross-Cutting (10_CrossCutting)

| Doc | Status | Trigger / Current Version |
|---|---|---|
| X1 RBACMatrix | Roadmap | M34 spec is source of truth until X1 lands |
| X2 DataDictionary | Roadmap (renamed → Decision Queue Catalogue) | After all Phase 1 specs lock |
| X3 IntegrationMap | Roadmap (renamed → Audit Event Catalogue) | After all Phase 1 specs lock. M03 Spec v1.1 Appendix C is interim source of truth for M03 audit events |
| X4 OutputCatalog | Roadmap (renamed → API Surface Index) | After all Phase 1 specs lock |
| X5 FormInventory | Roadmap (renamed → Speed Tier Inventory) | After all wireframes complete |
| X6 WorkflowDiagrams | Roadmap (renamed → Integration Point Map) | After all Phase 1 specs lock |
| X7 DecisionQueueSchema | Roadmap (renamed → Standards Memory) | After all Phase 1 specs lock |
| X8 GlossaryENUMs | **Living — current v0.4** | Updated continuously per I3. Bumped v0.1 → v0.2 (M01) → v0.3 (M02) → v0.4 (M03) |
| X9 VisualisationStandards | **Living — current v0.2** | Decision-First Principle locked v0.1; library + role views locked v0.2 |

### 3.13 System Utilities (11_System_Utilities)

| Utility | Status | Notes |
|---|---|---|
| HDI HistoricalDataImport | Pending | Re-issue of legacy v1.0 — must be added to registry per audit finding |

---

## 4. CHANGE LOG (this file's own history)

| Date | Version | Change |
|---|---|---|
| 2026-05-03 | v1.0 | Initial creation. All artefacts inventoried. 70+ artefacts pending. |
| 2026-05-03 | v1.1 | Round 18 reconciliation pass. §3 registry state aligned with actual locked artefacts (M34 R1–4, M01 R5b–8+R16, M02 R9–12, M03 R15–18 + Spec v1.1 cascade). §6 activity log catch-up entry consolidated for Rounds 1–18. §7 next-round preview refreshed to reflect Round 19 readiness. §3.12 cross-cutting expanded with X9 living-doc row + X8 version trail. Activity log was last updated at Round 0; gap acknowledged and back-filled at the round level (per-artefact granularity preserved in CLAUDE.md §3 status table and per-artefact change logs). |
| 2026-05-03 | v1.2 | Round 18 audit pass — corrections from 3-axis audit (cross-references, conformance, locked-decisions). Backfilled M01 v1.1 cascade note (`Project.min_wbs_depth`) — closed an architectural gap where M02 BR-02-001/032 referenced an M01 field that didn't exist. Fixed M03 Spec v1.1 + M03 Brief v1.1 stale Reference Standards lines (X8 v0.3→v0.4, X9 v0.1→v0.2, M01 v1.2-file-doesn't-exist → v1.0+cascade-notes). Added retro audit stamps to all 4 wireframes (M34/M01/M02/M03). Fixed cross-cutting-standards.md role taxonomy (added missing ANALYST; corrected external role names to M34 ENUMs). Amended spec-protocol.md to lock 3 audit-stamp formats (YAML / markdown-bold / HTML-comment) + cascade-vs-re-issue decision rule. Amended naming-folders.md to lock canonical placement at `SystemAdmin/{Modules,Cross-link files}/` + downgrade 13-folder hierarchy to aspirational. CLAUDE.md locked-decisions table gained 4 new rows. |

---

## 5. UPDATE PROTOCOL

When any artefact is created, modified, or status-changed:

1. Author updates the relevant row in section 3.
2. Author appends a row to section 6 (Activity Log).
3. Author updates the file's `Last Updated` timestamp here.
4. PMO Director approves on next review.

---

## 6. ACTIVITY LOG (append-only, latest first)

| Date | Time | Artefact | Action | Author | Note |
|---|---|---|---|---|---|
| 2026-05-03 | — | Round 24 — M06 FinancialControl Spec v1.0 (via /build-module pipeline, iter 1 + 3 cosmetic fixes) | Locked | Monish (with Claude assist) | Spec authored by drafter subagent; auditor ACCEPT 0/26 fails at iter 1. 3 cosmetic discrepancies flagged in notes_for_user_review (Appendix A header count 28→43, CHANGE LOG entity count 16→17, GRN.qc_decision_at_emit ENUM citation) — all 3 patched inline before lock per user direction. **17 entities** (4 append-only ledgers DB-level UPDATE/DELETE forbidden), **47 BRs** (BR-06-001..047), **17 DPRs**, **43 audit events** (Appendix A locked from authoring), **13 integration points** (5 active + 8 stub contracts for M05/M07/M08/M09/M11/M12/M15/M23). 0 open questions in Block 10. Cascade implications: X8 v0.6 (13 new ENUMs + 12 DQ trigger types + 28 audit-event extension + 4 reserved-field exemptions); M01 v1.3 cascade note (Contract.dlp_retention_split_pct DECIMAL(5,4) DEFAULT 0.5000); M03 minor cascade (MILESTONE_ACHIEVED_FINANCIAL emit hook for Financial milestones). Branch: draft/build-m06. |
| 2026-05-03 | — | Round 23 — M06 FinancialControl Brief v1.0 (via /build-module pipeline, iter 1) | Locked | Monish (with Claude assist) | First artefact authored via the new /build-module multi-agent pipeline (drafter subagent + independent auditor subagent + user OQ pause). Auditor verdict ACCEPT at iter 1 (0/17 fails). 11 OQ-1 user decisions + 6 OQ-2 pattern defaults — all CLOSED in §8 with locked answers. Notable resolutions: 1.6=B multi-currency from v1.0 (KDMC pilot stays INR but system supports future foreign-currency equipment imports); 1.3=B both progress AND milestone billing triggers (DBOT pattern); 1.7=C split scope (EPCC 2/3-way match; external accounting executes payment); 1.8=C tranched retention with dual sign-off → triggers M01 v1.3 cascade for `Contract.dlp_retention_split_pct`. 11 ENUMs proposed for X8 v0.6 cascade in Spec round (CostLedgerEntryState, RABillStatus, RABillTriggerSource, GRNStatus, RetentionReleaseType, ExchangeRateTier, VendorInvoiceStatus, InvoiceMatchStatus, PaymentWorkflowStep, BACIntegrityWarningSource, M06_DecisionQueueTriggerType). Branch: draft/build-m06. |
| 2026-05-03 | — | Round 22 — M04 ExecutionCapture Workflows v1.0 | Locked | Monish (with Claude assist) | M04 Workflows v1.0 LOCKED. **M04 module COMPLETE** (4/4 artefacts). 9 workflows covering all 39 BRs from Spec — zero orphans in BR Coverage Matrix. WF-04-001 ProgressEntry create/submit, WF-04-002 approval (single + dual paths), WF-04-003 NCR lifecycle, WF-04-004 NCR daily sweep, WF-04-005 MaterialReceipt + QC + GRN, WF-04-006 ContractorPerformanceScore quarterly batch, WF-04-007 ProjectExecutionConfig auto-create + edit, WF-04-008 Photo migration to M12, WF-04-009 NCR → M05 LD signal. Mermaid flows + step-by-step + audit events + failure-mode tables per WF. References M04 Spec v1.0 Appendix A + X8 v0.5 §4.12 (34 named events). |
| 2026-05-03 | — | Round 21 — M04 ExecutionCapture Wireframes v1.0 | Locked | Monish (with Claude assist) | M04 Wireframes v1.0 LOCKED. Single HTML file with 7 role-default views per X9 v0.3 §13.3.4: SITE_MANAGER (today's progress entries + 4-week look-ahead Gantt), PROJECT_DIRECTOR (% complete heatmap + NCR pipeline funnel), QS_MANAGER ⭐ (Pending approvals queue + measurement variance — M04's primary QS surface), PMO_DIRECTOR (NCR pipeline funnel + material receipts variance), PROCUREMENT_OFFICER (receipts log + long-lead tracking), ANALYST (S-curve trend + NCR rate trend), READ_ONLY (status-badge card). Tailwind CDN, no framework deps (D3 lock). Inline JS for role tab toggling. KDMC-001-DBOT mock data throughout. Format C audit stamp (HTML comment block) per Round 18 audit decision. NCR pipeline funnel rendered as 8th instance of X9 §11 flagship pattern. |
| 2026-05-03 | — | Round 20 — X8 v0.5 + X9 v0.3 cascades (M04 sub-deliverables) | Locked | Monish (with Claude assist) | X8 v0.5 LOCKED — 8 new M04 ENUMs (ProgressMeasurementMethod, ProgressApprovalStatus, EVConfidence, NCRStatus, NCRRootCauseCategory, MaterialReceiptStatus, MaterialQCStatus, MaterialQCDecision). M04 audit events (22) and Decision Queue triggers (8) catalogued. M04 append-only ledgers (4) added to reserved-fields exemption list. X9 v0.3 LOCKED — §13.3.4 rewritten per M04 Brief OQ-1.8 + Spec Block 5: scope-decomposition cleanup (HSE→M31, BOQ-grain→M14, COMPLIANCE_MANAGER row dropped); 7-role mapping added (PROCUREMENT_OFFICER, ANALYST, READ_ONLY rows new); QS_MANAGER primary view = "Pending approvals queue" (M04's true QS-facing surface). NCR pipeline funnel confirmed as 8th instance of §11 flagship pipeline pattern. cross-cutting-standards.md updated. CLAUDE.md cross-cutting table updated. Round 20 fully closed. |
| 2026-05-03 | — | Round 20 — M04 ExecutionCapture Spec v1.0 | Locked | Monish (with Claude assist) | M04 Spec v1.0 LOCKED. 10 entities (4 append-only ledgers with DB-level UPDATE/DELETE forbidden). 39 BRs covering ProgressEntry 3-state lifecycle, ConstructionNCR 4-tier severity, MaterialReceipt with QC + GRN signal, ContractorPerformanceScore quarterly batch, ProjectExecutionConfig (resolves OQ-2.6 — execution-tunables live in M04, not M01). Appendix A locks 22 audit event names from authoring (per Round 18 cascade-pattern discipline). Photo storage stubbed (MinIO direct URLs) with Appendix C migration script drafted for M12 lock. Block 10 has 6 questions all RESOLVED. X8 v0.5 + X9 v0.3 cascades remain pending as Round 20 sub-deliverables. |
| 2026-05-03 | — | Round 19 — M04 ExecutionCapture Brief v1.0 | Locked | Monish (with Claude assist) | M04 Brief LOCKED with all 13 OQ items CLOSED in-Brief (8 OQ-1 + 5 OQ-2). Sequencing pivot from M07-first to M04-first after Monish challenged the dependency-first principle — M04 reads only locked modules (M01/M02/M03), no guessed contracts. Scope decomposed (OQ-1.1=B): DLP→M15, HSE→M31, BOQ-grain→M14, document storage→M12, daily diary→M16. Three-state approval flow + 4-tier NCR severity + dual sign-off above ₹50L threshold. Photo storage stubbed via MinIO until M12 lands. Brief uses Format A (YAML frontmatter) per Round 18 audit decision. Spec Round 20 ready — anticipates X8 v0.5 cascade (6 new ENUMs) + X9 v0.3 cascade (M04 row in §13.3.3 role-default views). |
| 2026-05-03 | — | Round 18 audit — corrections + rule amendments + M01 v1.1 cascade backfill | Audit Pass | Monish (with Claude assist) | 3-axis audit (cross-refs / conformance / locked decisions) surfaced 11 issues. All addressed in one pass. Created `M01_ProjectRegistry_v1_1_CascadeNote.md` documenting `Project.min_wbs_depth` field add (closes M02→M01 architectural gap). Refreshed M03 Spec + Brief Reference Standards. Added retro stamps to 4 wireframes. Fixed cross-cutting-standards.md (ANALYST + external role names). Amended `.claude/rules/spec-protocol.md` (3 stamp formats + cascade-vs-re-issue rule) and `.claude/rules/naming-folders.md` (canonical placement, 13-folder downgraded). 4 new rows in CLAUDE.md locked-decisions table. |
| 2026-05-03 | — | Round 18 — M03 Workflows v1.0 + M03 Spec v1.1 cascade | Locked | Monish (with Claude assist) | M03 module COMPLETE. Workflows v1.0 with 9 flows + 34/34 BR coverage matrix locked. Spec v1.0 → v1.1 cascade absorbed Appendix C (28 audit events), BR-03-033 (critical-path transactionality), BR-03-034 (reporting_period_type atomic rollback). File renamed via `git mv` preserving history. CLAUDE.md §3 row + re-entry-protocol.md canonical-source table updated. |
| 2026-05-03 | — | Rounds 1–17 (reconciliation catch-up) | Reconciled | Monish (with Claude assist) | Activity log was last updated at Round 0; this consolidation entry covers the full Round 1–17 span. Module deliverables: M34 (R1–4 — foundation: Brief, Spec, Wireframes, Workflows v1.0), M01 (R5b–8 — Brief, Spec, Wireframes, Workflows v1.0; R16 cascade absorbing M02 OQ-1.1=B → Project.min_wbs_depth pending v1.1), M02 (R9–12 — Brief, Spec, Wireframes, Workflows v1.0). Cross-cutting: X8 v0.1 → v0.2 (M01) → v0.3 (M02) → v0.4 (M03); X9 Brief v0.1 → Spec v0.1 → Spec v0.2. Per-artefact granularity in CLAUDE.md §3 status table. |
| 2026-05-03 | — | Round 0 (5 files) | Created | PMO Dir | Foundation files. Round 0 fired per v2.7 plan. |

---

## 7. NEXT ROUND PREVIEW

| Round | Artefact | Status |
|---|---|---|
| 19 | TBD — next module Brief (candidates: M07 EVMEngine, M27 DesignControl, M12 DocumentControl, M14 QSMeasurementBook) | Awaiting Monish's Round 19 module pick |
| (separate cascade) | M01 Spec v1.1 — add `Project.min_wbs_depth` field per M02 OQ-1.1=B | Pending — independent of Round 19 sequence |

---

*v1.0 — Living document. Updated on every artefact event. Single source of truth for version, status, and ownership.*
