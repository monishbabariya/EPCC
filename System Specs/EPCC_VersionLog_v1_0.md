# EPCC — Master Version Log
## Version 1.1
**Owner:** PMO Director
**Created:** 2026-05-03 | **Last Reconciled:** 2026-05-04 (R31 plan lock — §7 NEXT ROUND PREVIEW replaced with revised round sequence per `EPCC_BuildExecutionPlan_v1_0.md`)
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

## 3. CURRENT REGISTRY STATE — 2026-05-04 (post Round 29 medium-cleanup sweep)

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
| _(Round 18 audit — see CHANGE LOG row v1.2 below + per-artefact retro stamps; no separate audit file produced)_ | 18 | inline | Locked | Monish (with Claude assist) | 2026-05-03 |
| _(Round 29 audit — see Round 29 PR series #4-#11 commit messages + this file's Living-doc CHANGE LOG; no separate audit file produced)_ | 29 | inline | Locked | Monish (with Claude assist) | 2026-05-04 |

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
| M01_ProjectRegistry_*_v1_0.* + v1.0a/v1.1/v1.2/v1.3/v1.4 cascade notes | Brief/Spec/WF/WL + cascade notes | v1.0 + v1.0a in-place patch R29 + v1.1/v1.2/v1.3/v1.4 cascade notes | **Locked** | Rounds 5b–8 + R16 + R18 audit (v1.1 backfilled) + R28 (v1.3) + R29 (v1.4 + Brief v1.0a + Spec v1.0a + Workflows v1.0b). v1.1 = `Project.min_wbs_depth` add; v1.2 = `Project.reporting_period_type` remove (→ M03); v1.3 = `Contract.dlp_retention_split_pct` add + BR-01-036; v1.4 = X8 ENUM refs + Block 4a canonicalisation |
| M23_BGInsuranceTracker_*_v1_0.* | Brief/Spec/WF/WL | — | Pending | New (was unspecced) |

### 3.5 L2 Planning (03_L2_Planning)

| Module | Status | Notes |
|---|---|---|
| M02 StructureWBS | **Locked** Brief v1.0a + Spec v1.0a + Wireframes v1.0 + Workflows v1.0b + v1.1 cascade note | Rounds 9–12 + R29 medium-cleanup (Brief v1.0a, Spec v1.0a, Workflows v1.0b in-place patches; v1.1 cascade adds X8 ENUM refs + ANALYST rate-matrix row) |
| M03 PlanningMilestones | **Locked** Brief v1.1a + Spec v1.1b + Wireframes v1.0 + Workflows v1.0 + v1.2/v1.3 cascade notes | Rounds 15–18 + R28 (v1.2 cascade — `MILESTONE_ACHIEVED_FINANCIAL`) + R29 (v1.1a Spec H7 forward-pointer + v1.1b Spec second-order ref refresh + Brief v1.1a + v1.3 cascade adds ANALYST + EXTERNAL_AUDITOR columns to Block 4a). Spec v1.1 R18 cascade added Appendix C (28 audit events) + BR-03-033 + BR-03-034 |
| M12 DocumentControl | Pending | New (Phase 1 critical, was unspecced) |
| M14 QSMeasurementBook | Pending | New (Phase 1 critical, was unspecced) |
| M27 DesignControl | Pending | New (proposed v2.3) |
| M28 InterfaceManagement | Pending | New (proposed v2.3) |

### 3.6 L2 Execution (04_L2_Execution)

| Module | Status | Notes |
|---|---|---|
| M04 ExecutionCapture | ✅ **Complete** — R19 Brief v1.0, R20 Spec v1.0 (+ v1.0a R29 patch), R21 Wireframes v1.0, R22 Workflows v1.0 | Re-issue of legacy v2.2 |
| M15 HandoverManagement | Pending | Re-issue of legacy v1.0 |
| M16 SiteDiary | Pending | New |
| M20 LabourWorkforce | Pending | New |

### 3.7 L2 RiskCommercial (05_L2_RiskCommercial)

| Module | Status | Notes |
|---|---|---|
| M05 RiskChange | Pending | Re-issue of legacy v2.3 (currently amendment file) |
| M06 FinancialControl | ✅ **Complete** — R24 Brief v1.0, R25 Spec v1.0 (+ v1.0a R27 audit-correction + v1.0b R29 in-place patch), **R29 Wireframes v1.1** (re-issued from v1.0 R26 — C3 SG_9/SG_11 fix + H17/H18 BGType canonicalisation), R27 Workflows v1.0 (+ v1.0a R29 H3/H4 stamp refresh + v1.0b R29 medium-cleanup wireframe filename refresh) + v1.1 cascade note R29 (SG_11_PASSAGE stub removed per H6 Option B) | Re-issue of legacy v2.1 |
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
| X8 GlossaryENUMs | **Living — current v0.6a** | Updated continuously per I3. Bumped v0.1 → v0.2 (M01) → v0.3 (M02) → v0.4 (M03) → v0.5 (M04) → v0.6 (M06) → v0.6a (R29 PR #4 in-place patch — H1: MILESTONE_ACHIEVED_FINANCIAL added to §4.12). Filename retained as `_v0_6.md` per in-place patch convention. |
| X9 VisualisationStandards | **Living — current v0.4** | Decision-First Principle locked v0.1; library + role views locked v0.2; M04 §13.3.4 rewrite locked v0.3; M06 §13.3.6 5→8 roles + Capital Funnel flagship annotation locked v0.4. Reference Standards refreshed R29 medium-cleanup (M28 — cross-ref hygiene). |

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
| 2026-05-04 | — | Round 28 — M06 cascade pass — X8 v0.6 + X9 v0.4 + M01 v1.3 cascade note + M03 v1.2 cascade note + naming-folders.md exemption-list refresh (via /build-module Phase 5 cascade-detector + Phase 5b lock-decision batch) | Locked | Monish (with Claude assist) | **Phase 5 cascade-detector subagent run on M06 Brief/Spec/Wireframes/Workflows surfaced 6 cascades; user approved all (option A — apply all blockers + minor).** **(1) X8 v0.6** — 13 new M06 ENUMs catalogued (CostLedgerEntryState, PurchaseOrderStatus, RABillStatus, RABillTriggerSource, GRNMatchStatus, VendorInvoiceStatus, InvoiceMatchMode, InvoiceMatchStatus, PaymentEvidenceStatus, RetentionReleaseType, RetentionReleaseStatus, ExchangeRateTier, BGType); §4.12 AuditEventType extended with 43 M06 events; new §4.17 M06_DecisionQueueTriggerType (12 values); §6 reserved-fields exemption list extended with 4 M06 ledgers (CostLedgerEntry, RABillAuditLog, PaymentEvidenceLedger, ForexRateLog); **§3.10 StageGate description refreshed** — SG_9 = "Substantial / Practical Completion (clinical commissioning ready)" + SG_11 = "DLP End / Operations Handover" (sequence unchanged; description text only — pre-empts M08 reopening). Brief→Spec ENUM-count delta noted: PaymentWorkflowStep + BACIntegrityWarningSource anticipated by Brief §9 were NOT introduced (collapsed into PaymentEvidenceStatus + boolean flag). **(2) X9 v0.4** — zero new chart types (Capital Funnel = 1st named flagship instance of existing §11 Pipeline Funnel pattern); §13.3.6 row expanded 5→8 roles (added QS_MANAGER, EXTERNAL_AUDITOR, READ_ONLY) for parity with M06 Spec Block 5; §9.5.1 annotated as flagship instance. **(3) M01 v1.3 cascade note** — `Contract.dlp_retention_split_pct DECIMAL(5,4) DEFAULT 0.5000` field added + new BR-01-036 (PMO_DIRECTOR-edit only with justification ≥100 chars) + new audit event `CONTRACT_DLP_SPLIT_EDITED`; consumed by M06 BR-06-027 + BR-06-045. **(4) M03 v1.2 cascade note** — new audit event `MILESTONE_ACHIEVED_FINANCIAL` (emit hook on Milestone.status → Achieved when milestone_type = Financial) + new BR-03-035 (atomic emit governance per BR-03-034) + Block 7 SENDS TO M06 entry; consumed by M06 BR-06-010 + WF-06-005 milestone-RA Bill creation. **(5) naming-folders.md exemption-list refresh** — fixed M04 v0.5 backlog drift (4 ledgers from Round 22 never propagated to rule file) + added 4 M06 ledgers; list grows 7 → 15 entries; added "Source of truth: X8 §6" footnote so future drift is impossible. **(6) cross-cutting-standards.md, re-entry-protocol.md, CLAUDE.md** all updated to X8 v0.6 + X9 v0.4 paths; CLAUDE.md locked-decisions table grew with 7 M06-derived rows (Financial Control state machine, RA Bill trigger sources, Retention release, Multi-currency, BG tracking, SG_9/SG_11 descriptions, Capital Funnel flagship). No M02 / M04 / M34 cascades — verified all consumed contracts already locked-from-authoring in source modules. **Renumbering note:** rounds 23-27 in pre-merge draft commits renumbered to 24-28 post-merge to avoid collision with main's Round 23 = EPCC_BuildArchitecture Brief. Branch: draft/build-m06. |
| 2026-05-03 | — | Round 27 — M06 FinancialControl Workflows v1.0 + Spec v1.0a audit correction (via /build-module pipeline, iter 1 + 2 audit-correction fixes) | Locked | Monish (with Claude assist) | **M06 module COMPLETE — first end-to-end /build-module pipeline run.** Workflows authored by drafter subagent; auditor ACCEPT 0/20 fails at iter 1. **14 workflows** covering all **47 BRs** (zero NON_RUNTIME, zero orphans), all **43 audit events emitted**, all **12 Decision Queue triggers raised**. SG-9 + SG-11 stage-gate couplings documented. 2 audit-correction fixes applied pre-lock per user direction: **(1) Stage Gate naming disambiguation** — tranche-1 (Substantial Completion) trigger renamed `SG_11_PASSAGE` → `SG_9_PASSAGE` across both Spec and Workflows; tranche-2 retains `SG_11_PASSAGE`; both `/sg9-passage` and `/sg11-passage` endpoints exposed for M08. **Spec patched to v1.0a in-place** (audit-correction note in CHANGE LOG; not a version bump). **(2) WF-06-013 M12 doc-migration trace** — added explicit step 8. 14 mermaid blocks all valid. Cascades pending Phase 5 detection: X8 v0.6 + M01 v1.3 + M03 v1.2. Pre-merge round number was 26 (renumbered to 27 post-merge). Branch: draft/build-m06. |
| 2026-05-03 | — | Round 26 — M06 FinancialControl Wireframes v1.0 (via /build-module pipeline, iter 1 + 3 cosmetic fixes) | Locked | Monish (with Claude assist) | Wireframes authored by drafter subagent; auditor ACCEPT 0/17 fails at iter 1. 3 cosmetic fixes applied pre-lock per user direction: (1) `note:` field moved out of Format C 7-field stamp into a separate HTML comment; (2) `variance_table_with_pattern_classifier` annotation normalised to X9 OQ-1.10 tabular fallback; (3) `tabular_immutable_ledger` annotation normalised to X9 OQ-1.10 tabular fallback. Single HTML file, 1015 lines, 100 KB. **8/8 roles** rendered. **15 charts** total — Capital Funnel (4-stage pipeline, 5 instances) is the **1st named instance of X9 §11 / §9.5.1 flagship pipeline pattern**. Tailwind CDN only; 0 external JS imports (D3 lock honored). Spike Formula rate-display matrix per BR-02-008 verified end-to-end across all 4 role tiers. KDMC mock data: ₹68.4 Cr BAC, L&T contractor, multi-currency forex (USD LINAC + EUR CT/MRI). Pre-merge round number was 25 (renumbered to 26 post-merge). Branch: draft/build-m06. |
| 2026-05-03 | — | Round 25 — M06 FinancialControl Spec v1.0 (via /build-module pipeline, iter 1 + 3 cosmetic fixes) | Locked | Monish (with Claude assist) | Spec authored by drafter subagent; auditor ACCEPT 0/26 fails at iter 1. 3 cosmetic discrepancies flagged in notes_for_user_review (Appendix A header count 28→43, CHANGE LOG entity count 16→17, GRN.qc_decision_at_emit ENUM citation) — all 3 patched inline before lock per user direction. **17 entities** (4 append-only ledgers DB-level UPDATE/DELETE forbidden), **47 BRs** (BR-06-001..047), **17 DPRs**, **43 audit events** (Appendix A locked from authoring), **13 integration points** (5 active + 8 stub contracts for M05/M07/M08/M09/M11/M12/M15/M23). 0 open questions in Block 10. Cascade implications: X8 v0.6 (13 new ENUMs + 12 DQ trigger types + 28 audit-event extension + 4 reserved-field exemptions); M01 v1.3 cascade note (Contract.dlp_retention_split_pct DECIMAL(5,4) DEFAULT 0.5000); M03 minor cascade (MILESTONE_ACHIEVED_FINANCIAL emit hook for Financial milestones). Pre-merge round number was 24 (renumbered to 25 post-merge). Branch: draft/build-m06. |
| 2026-05-03 | — | Round 24 — M06 FinancialControl Brief v1.0 (via /build-module pipeline, iter 1) | Locked | Monish (with Claude assist) | First artefact authored via the new /build-module multi-agent pipeline (drafter subagent + independent auditor subagent + user OQ pause). Auditor verdict ACCEPT at iter 1 (0/17 fails). 11 OQ-1 user decisions + 6 OQ-2 pattern defaults — all CLOSED in §8 with locked answers. Notable resolutions: 1.6=B multi-currency from v1.0 (KDMC pilot stays INR but system supports future foreign-currency equipment imports); 1.3=B both progress AND milestone billing triggers (DBOT pattern); 1.7=C split scope (EPCC 2/3-way match; external accounting executes payment); 1.8=C tranched retention with dual sign-off → triggers M01 v1.3 cascade for `Contract.dlp_retention_split_pct`. 11 ENUMs proposed for X8 v0.6 cascade in Spec round. Pre-merge round number was 23 (renumbered to 24 post-merge to avoid collision with Round 23 = EPCC_BuildArchitecture Brief). Branch: draft/build-m06. |
| 2026-05-03 | — | Round 23 — EPCC_BuildArchitecture_Brief_v1_0 | Draft | Monish (with Claude assist) | Round 23 opened to lock the build architecture before any code lands for M34/M01/M02/M03/M04. Brief surfaces 10 OQ-1 user decisions (repo strategy, branch model, sequencing, OIDC choice, multi-tenancy, pilot seed, CI host, prod hosting deferral, BR-tagged tests, ENUM codegen) + ~30 OQ-2 pattern defaults. Recommends monorepo on `main` (not a separate `Code` branch) with feature branches per module, thin vertical slice (M34 → M01 demo) before module deepening. New §7a "Change Management" details cascade-cost matrix + 10 built-in flexibility mechanisms (code mirrors spec layout, X8 codegen, OpenAPI codegen, BR-tagged tests, etc.) and honest list of where flexibility has limits. Brief has zero prescription — all 10 OQ-1 + OQ-2 awaiting Monish lock before downstream Spec lock. Format A (YAML frontmatter) per Round 18 audit decision. **Note (post-merge):** main's NEXT ROUND PREVIEW originally projected Build Architecture Spec at Round 24 + scaffold/codegen/thin-slices through Round 29 — these are pushed to Rounds 29+ post-merge since Rounds 24-28 are now occupied by M06 module work that landed in parallel. |
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

> **Note:** Round sequence revised at R31 plan-lock (`EPCC_BuildExecutionPlan_v1_0.md`). Spec-track and build-track run in parallel from R37 onward. Per-module gate: full Brief→Spec→Wireframes→Workflows LOCKED before that module's build slice. Single round-numbering sequence (monotonic); track identified by commit-message convention. Source of truth for live round sequence: `System Specs/EPCC_BuildExecutionPlan_v1_0.md` §3 — this preview is a snapshot.

### Past rounds (R23-R31)

| Round | Artefact | Status |
|---|---|---|
| 23 | EPCC_BuildArchitecture_Brief_v1_0 | **Locked** (R30 Spec follow-up) |
| 24 | M06 FinancialControl Brief v1.0 | **Locked** |
| 25 | M06 FinancialControl Spec v1.0 (+ v1.0a R27 audit-correction + v1.0b R29 in-place patch) | **Locked** |
| 26 | M06 FinancialControl Wireframes v1.0 (re-issued to v1.1 R29 PR #7) | **Locked → Re-issued R29** |
| 27 | M06 FinancialControl Workflows v1.0 (+ v1.0a R29 stamp refresh + v1.0b R29 medium-cleanup) + Spec v1.0a audit correction | **Locked** |
| 28 | M06 cascade pass — X8 v0.6 + X9 v0.4 + M01 v1.3 + M03 v1.2 + naming-folders refresh | **Locked** |
| 29 | **Audit pass** — 4 PR series (PR #4 remediation + PR #5 high-mechanical + PR #6 cascade-notes + PR #7 wireframe-reissue + PR #8 medium-cleanup) closing all CRITICAL/HIGH/MEDIUM and reconciling LOWs | **Locked** |
| 30 | EPCC_BuildArchitecture_Spec_v1_0 | **Locked** |
| 31 | M05_RiskChangeControl_Brief_v1_0 + EPCC_BuildExecutionPlan_v1_0 (governance lock) | **Locked** |

### Foundation Phase preview (R32-R51)

Per Build Execution Plan §3a. C1 cadence on Specs; C1b on Wireframes/Workflows where peer modules permit.

| Round | Track | Artefact | Calendar |
|---|---|---|---|
| 32 | Spec | M13 CorrespondenceMeetingRegister Brief v1.0 (C1b batch with M05) | Week 1 |
| 33 | Spec | M05 Spec v1.0 + X8 v0.7 cascade scaffold | Week 2 |
| 34 | Spec | M13 Spec v1.0 + X8/X9 audit pass for M05+M13 batch | Week 2 |
| 35 | Spec | M05 + M13 Wireframes (C1b batch) | Week 3 |
| 36 | Spec | M05 + M13 Workflows (C1b batch) | Week 3 |
| 37 | Build | Monorepo scaffold + 10 ADRs + CI workflow + Docker Compose + Keycloak realm seed | Week 4 |
| 38 | Build | ENUM codegen pipeline live | Week 4 |
| 39 | Build | M34 thin slice scaffold | Week 5 |
| 40 | Build | M34 thin slice complete (AC-1/2/3/7) | Week 5 |
| 41 | Build | M01 thin slice scaffold | Week 6 |
| **42** ⭐ | Build | **M01 thin slice complete + First End-to-End Demo (G-2, internal)** | Week 6 |
| 43 | Spec | M07 EVMEngine Brief v1.0 | Week 7 |
| 44 | Build | M02 deepening start | Week 7 |
| 45 | Spec | M07 Spec v1.0 + X8 v0.8 cascade scaffold | Week 8 |
| 46 | Build | M02 deepening complete + M03 deepening start | Week 8-9 |
| 47-48 | Spec | M07 Wireframes + Workflows | Week 9-10 |
| 49 | Build | M03 deepening complete | Week 10 |
| 50 | Spec | M08 GateControl Brief v1.0 | Week 11 |
| 51 | Build | M04 deepening start | Week 11 |
| 52-55 | Spec + Build | M08 Spec + Wireframes + Workflows + M04 deepening complete | Week 12-13 |
| 56 | Build | M06 deepening start | Week 14 |
| **57** ⭐ | Build | **M06 deepening complete + Cost Ledger Live Demo (G-3, KDMC stakeholders)** | Week 14 |

### Phase 1 Foundation cap (R58-R68)

| Round | Track | Artefact | Calendar |
|---|---|---|---|
| 58-62 | Spec + Build | M11 Brief + Spec + Wireframes + Workflows + M05 deepening complete | Week 15-17 |
| 63 | Build | M07 deepening start | Week 17 |
| **64** ⭐ | Build | **M07 deepening complete + EVM Engine Live Demo (G-4, KDMC stakeholders)** | Week 18 |
| 65 | Build | M08 deepening start | Week 18-19 |
| **66** ⭐ | Build | **M08 deepening complete + Stage Gates Live Demo (G-5, KDMC stakeholders)** | Week 19-20 |
| 67 | Build | M11 ActionRegister deepening | Week 20 |
| **68** ⭐ | Build | **M11 deepening complete + Foundation 10 Modules Complete (G-6, lender + external review)** | Week 21 |

### Phase 1 Secondary preview (R69-R85+)

| Round | Track | Artefact | Calendar |
|---|---|---|---|
| 69-72 | Spec + Build | M14 QSMeasurementBook full cycle | Week 22-23 |
| 73 | Build | M12 DocumentControl deepening + M04 photo migration | Week 24 |
| 74-75 | Spec + Build | HDI v1.0 (full KDMC migration) | Week 25-26 |
| **76** ⭐ | Build | **Phase 1 MVP Demo (G-7, lender + KDMC + external review)** | Week 27 |
| 77-85 | Spec + Build | Phase 1 secondary modules (M09, M22, M27, M28, M30, M31, M32, M33, M16, M20, M21, M23, M24, M25, M26, M10, M29, M17, M18) — 19 modules | Week 28-34 |
| **86+** ⭐ | — | **Phase 1 Functional System (G-8, 33 modules)** | Week 35 |

### Phase 2 preview (R87+)

Phase 2 deferred 8 modules (M19, M15, PF01-PF06) + production hardening. Calendar Week 36-50.

| **95+** ⭐ | — | **Phase 1 + Platform Complete (G-9; Phase 2 entry gate)** | Week 50 |

### Audit rounds (inserted per cadence)

Per Build Execution Plan §7. Branches `audit/round-{N}-{theme}`, ~1-2 weeks each, calendar-absorbed.

| Audit | Trigger | Scope |
|---|---|---|
| Audit/R45+ | After Cost Ledger Demo (G-3) | M02 + M03 + M06 contract integrity |
| Audit/R51+ | After Foundation 10 Complete (G-6) | M07 ↔ M08 ↔ M06 commercial-loop audit |
| Audit/R65+ | After M14 + M12 + HDI v1.0 | KDMC migration verification |
| Audit/R73+ | After Phase 1 MVP (G-7) | Full system audit pre-secondary-modules |
| Audit/R85+ | After Phase 1 Functional (G-8) | Pre-Phase-2 audit |

---

*v1.0 — Living document. Updated on every artefact event. Single source of truth for version, status, and ownership.*
