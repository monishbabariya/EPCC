# EPCC — Folder Index
## Version 1.0
**Owner:** PMO Director / System Architect
**Created:** 2026-05-03 | **Status:** Locked

---

## 1. CANONICAL HIERARCHY

```
/EPCC_System/
│
├── 00_Governance/
│   ├── EPCC_NamingConvention_v1_0.md
│   ├── EPCC_FolderIndex_v1_0.md
│   ├── EPCC_VersionLog_v1_0.md            ← MASTER VERSION TRACKER
│   ├── EPCC_ModuleRegistry_v1_0.md
│   ├── EPCC_StandardsMemory_v1_0.md
│   ├── EPCC_LegacyManifest_v1_0.md
│   ├── EPCC_DevSkillsRequired_v1_0.md
│   └── Archive/                            ← superseded files (never deleted)
│
├── 01_Strategic/
│   └── PIOE_PortfolioInvestmentOptimisation_*
│
├── 02_L1_Command/
│   ├── M01_ProjectRegistry_*
│   ├── M23_BGInsuranceTracker_*
│   └── M34_SystemAdminRBAC_*
│
├── 03_L2_Planning/
│   ├── M02_StructureWBS_*
│   ├── M03_PlanningMilestones_*
│   ├── M12_DocumentControl_*
│   ├── M14_QSMeasurementBook_*
│   ├── M27_DesignControl_*
│   └── M28_InterfaceManagement_*
│
├── 04_L2_Execution/
│   ├── M04_ExecutionCapture_*
│   ├── M15_HandoverManagement_*
│   ├── M16_SiteDiary_*
│   └── M20_LabourWorkforce_*
│
├── 05_L2_RiskCommercial/
│   ├── M05_RiskChange_*
│   ├── M06_FinancialControl_*
│   ├── M13_CorrespondenceRegister_*
│   ├── M17_AssetEquipmentRegister_*
│   ├── M19_ClaimsManagement_*
│   ├── M29_TenderingAward_*
│   └── M30_VendorMasterPQ_*
│
├── 06_L2_Compliance/
│   ├── M08_GateControl_*
│   ├── M09_ComplianceTracker_*
│   ├── M21_TrainingCompetency_*
│   ├── M24_ClinicalOperationalReadiness_*
│   └── M31_HSESafetyManagement_*
│
├── 07_L2_Performance/
│   └── M07_EVMEngine_*
│
├── 08_L3_Intelligence/
│   ├── M10_EPCCCommand_*
│   ├── M11_ActionRegister_*
│   ├── M18_LenderInvestorReporting_*
│   ├── M22_LessonsLearned_*
│   ├── M26_AIPortfolioIntelligence_*
│   ├── M32_BenefitRealization_*
│   └── M33_StakeholderRegister_*
│
├── 09_Platform_Features/
│   ├── PF01_MobileFieldPlatform_*
│   ├── PF02_BIMIntegration_*
│   ├── PF03_ExternalPartyPortal_*
│   ├── PF04_AccountingIntegration_*
│   ├── PF05_OfflineCapture_*
│   └── PF06_WhatsAppBot_*
│
├── 10_CrossCutting/
│   ├── X1_RBACMatrix_v1_0.md
│   ├── X2_DataDictionary_v1_0.md
│   ├── X3_IntegrationMap_v1_0.md
│   ├── X4_OutputCatalog_v1_0.md
│   ├── X5_FormInventory_v1_0.md
│   ├── X6_WorkflowDiagrams_v1_0.md
│   ├── X7_DecisionQueueSchema_v1_0.md
│   └── X8_GlossaryENUMs_v1_0.md
│
├── 11_System_Utilities/
│   └── HDI_HistoricalDataImport_*
│
└── 12_Audits/
    ├── AUDIT_Round00_ExistingSpecs_v1_0.md
    ├── AUDIT_Round01_M34Brief_v1_0.md
    └── ...
```

---

## 2. PER-FOLDER OWNERSHIP RULES

| Folder | Contains | Update Authority |
|---|---|---|
| `00_Governance` | System-wide files only. No module specs. | PMO Director only |
| `01_Strategic` | PIOE family (Brief, Spec, Wireframes, Workflows) | PMO Director |
| `02_L1_Command` | L1 Command modules | PMO Director |
| `03_L2_Planning` | L2 Control — Planning & Structure | PMO Director |
| `04_L2_Execution` | L2 Control — Execution | PMO Director |
| `05_L2_RiskCommercial` | L2 Control — Risk, Financial, Commercial | PMO Director |
| `06_L2_Compliance` | L2 Control — Governance & Compliance | PMO Director |
| `07_L2_Performance` | L2 Control — EVM | PMO Director |
| `08_L3_Intelligence` | L3 Dashboards, Reporting, Intelligence | PMO Director |
| `09_Platform_Features` | Cross-cutting platform features | PMO Director |
| `10_CrossCutting` | RBAC, DataDict, Integration, Output, Workflow, Glossary | PMO Director |
| `11_System_Utilities` | Non-module system utilities (HDI, future utilities) | PMO Director |
| `12_Audits` | All audit reports — append only, never modified | PMO Director |

---

## 3. FILE-PER-FOLDER MINIMA

Each module folder must contain (at least), once Phase 1 is complete:

```
{ID}_{Name}_Brief_v1_0.md           ← lightweight brief (1 page)
{ID}_{Name}_Spec_v1_0.md             ← full 10-block spec
{ID}_{Name}_Wireframes_v1_0.html     ← per-role HTML wireframes
{ID}_{Name}_Workflows_v1_0.md        ← Mermaid workflow diagrams
```

Optional:
```
{ID}_{Name}_OpenQuestions_v1_0.md    ← living open question log (only if questions remain)
{ID}_{Name}_Notes_v1_0.md            ← design notes / rationale
```

---

## 4. INDEX FILE PER FOLDER (per I10)

Every folder must contain `_INDEX_v1_0.md` listing all files + status:

```
| File | Type | Version | Status | Last Updated |
|------|------|---------|--------|--------------|
| M01_ProjectRegistry_Brief_v1_0.md | Brief | v1.0 | Locked | 2026-05-03 |
| M01_ProjectRegistry_Spec_v1_0.md | Spec | v1.0 | Locked | 2026-05-03 |
```

Index files are auto-generated/regenerated whenever VersionLog updates.

---

## 5. RULES

| Rule | Statement |
|---|---|
| **F1** | Files live in exactly one folder. No copies. |
| **F2** | If a file logically spans two domains, place it in the most authoritative folder and reference from the other. |
| **F3** | Cross-cutting docs (X1–X8) live in `10_CrossCutting/`. They are not module-specific. |
| **F4** | HDI lives in `11_System_Utilities/` because it is a system utility, not a module (no M-number assigned per existing spec). |
| **F5** | Audit reports are append-only. Once dated, never edited. New findings = new audit file. |
| **F6** | Archive folder is read-only after first move. |

---

## 6. NAVIGATION

Every artefact references peer artefacts using **relative folder paths**:

```
See: ../03_L2_Planning/M02_StructureWBS_Spec_v1_0.md
```

Absolute paths are forbidden — they break when the folder is relocated.

---

*v1.0 — locked. Folder moves require PMO Director approval and update to VersionLog + LegacyManifest.*
