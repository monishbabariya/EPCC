# EPCC — Master Version Log
## Version 1.0
**Owner:** PMO Director
**Created:** 2026-05-03 | **Status:** Living Document
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

## 3. CURRENT REGISTRY STATE — 2026-05-03

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
| M01_ProjectRegistry_*_v1_0.* | Brief/Spec/WF/WL | — | Pending | Re-issue of legacy v2.1 |
| M23_BGInsuranceTracker_*_v1_0.* | Brief/Spec/WF/WL | — | Pending | New (was unspecced) |
| M34_SystemAdminRBAC_*_v1_0.* | Brief/Spec/WF/WL | — | Pending | **Round 1 priority — RBAC must precede all** |

### 3.5 L2 Planning (03_L2_Planning)

| Module | Status | Notes |
|---|---|---|
| M02 StructureWBS | Pending | Re-issue of legacy v2.1 (currently amendment file) |
| M03 PlanningMilestones | Pending | Re-issue of legacy v2.3 |
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

| Doc | Status | Trigger |
|---|---|---|
| X1 RBACMatrix | Pending | After M34 spec locks |
| X2 DataDictionary | Pending | After all Phase 1 specs lock |
| X3 IntegrationMap | Pending | After all Phase 1 specs lock |
| X4 OutputCatalog | Pending | After all Phase 1 specs lock |
| X5 FormInventory | Pending | After all wireframes complete |
| X6 WorkflowDiagrams | Pending | After all Phase 1 specs lock |
| X7 DecisionQueueSchema | Pending | After all Phase 1 specs lock |
| X8 GlossaryENUMs | **Living** | Updated continuously per I3 |

### 3.13 System Utilities (11_System_Utilities)

| Utility | Status | Notes |
|---|---|---|
| HDI HistoricalDataImport | Pending | Re-issue of legacy v1.0 — must be added to registry per audit finding |

---

## 4. CHANGE LOG (this file's own history)

| Date | Version | Change |
|---|---|---|
| 2026-05-03 | v1.0 | Initial creation. All artefacts inventoried. 70+ artefacts pending. |

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
| 2026-05-03 | — | Round 0 (5 files) | Created | PMO Dir | Foundation files. Round 0 fired per v2.7 plan. |

---

## 7. NEXT ROUND PREVIEW

| Round | Artefact | Status |
|---|---|---|
| 1 | M34_SystemAdminRBAC_Brief_v1_0.md | Awaiting Round 0 sign-off |
| 2 | M34_SystemAdminRBAC_Spec_v1_0.md | Awaiting Round 1 |
| 3 | M34_SystemAdminRBAC_Wireframes_v1_0.html | Awaiting Round 2 |
| 4 | X1_RBACMatrix_v1_0.md | Awaiting Round 3 |

---

*v1.0 — Living document. Updated on every artefact event. Single source of truth for version, status, and ownership.*
