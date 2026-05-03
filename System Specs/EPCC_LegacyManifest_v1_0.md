# EPCC — Legacy File Manifest
## Version 1.0
**Owner:** PMO Director
**Created:** 2026-05-03 | **Status:** Locked

---

## 1. PURPOSE

Map every legacy file (pre-v3.0 restart) to its new canonical filename and disposition. Preserves prior thinking. Prevents reference loss.

**Rule:** No legacy file is deleted. Every legacy file is either:
- **Archived** → moved to `/00_Governance/Archive/` with `_ARCHIVED_` suffix
- **Superseded** → replaced by new v1.0 spec, but archived for reference
- **Re-issued** → contents re-validated and re-issued under new naming

---

## 2. LEGACY → NEW FILE MAPPING

### 2.1 Module Specs

| Legacy Filename | Type | Disposition | New Filename | Status |
|---|---|---|---|---|
| M01_Project_Registry_v2.1.md | Spec | Re-issue | M01_ProjectRegistry_Spec_v1_0.md | Pending |
| M02_Structure_WBS_v2_1.md | Amendment | Re-issue (consolidate base + amend) | M02_StructureWBS_Spec_v1_0.md | Pending |
| M03_Planning_Milestones_v2.3.md | Spec | Re-issue | M03_PlanningMilestones_Spec_v1_0.md | Pending |
| M04_Execution_Capture_v2_2.md | Amendment | Re-issue (consolidate base + amend) | M04_ExecutionCapture_Spec_v1_0.md | Pending |
| M05_Risk_Change_v2_3.md | Amendment | Re-issue (consolidate base + amend) | M05_RiskChange_Spec_v1_0.md | Pending |
| M06_Financial_Control_v2_1.md | Spec | Re-issue | M06_FinancialControl_Spec_v1_0.md | Pending |
| M07_EVM_Engine_v3_0.md | Spec | Re-issue | M07_EVMEngine_Spec_v1_0.md | Pending |
| M08_Gate_Control_v2_1.md | Spec | Re-issue | M08_GateControl_Spec_v1_0.md | Pending |
| M09_Compliance_Tracker_v2_1.md | Spec | Re-issue | M09_ComplianceTracker_Spec_v1_0.md | Pending |
| M10_EPCC_Command_v2_2.md | Spec | Re-issue | M10_EPCCCommand_Spec_v1_0.md | Pending |
| M11_Action_Register_v1_0.md | Spec | Re-issue | M11_ActionRegister_Spec_v1_0.md | Pending |
| M15_Handover_Management_v1_0.md | Spec | Re-issue | M15_HandoverManagement_Spec_v1_0.md | Pending |
| PIOE_Spec_v2.md | Spec | Re-issue | PIOE_PortfolioInvestmentOptimisation_Spec_v1_0.md | Pending |
| PIOE_Spec_v2_1.md | Spec | Re-issue (use v2.1) | (same as above) | Pending |

### 2.2 System Documents

| Legacy Filename | Type | Disposition | New Filename | Status |
|---|---|---|---|---|
| EPCC_Standards_Memory.md | Standards | Re-issue (consolidate v2.0 → v5.3) | EPCC_StandardsMemory_v1_0.md | Pending |
| EPCC_Standards_Memory_v5_0.md | Standards | Archive | — | Archived |
| EPCC_Standards_Memory_v5_1.md | Standards | Archive | — | Archived |
| EPCC_Standards_Memory_v5_2.md | Standards | Archive | — | Archived |
| EPCC_Standards_Memory_v5_3.md | Standards | Source for v1.0 consolidation, then archive | — | Source |
| EPCC_Engineering_Standards_v1_2.md | Standards | Re-issue | EPCC_EngineeringStandards_v1_0.md | Pending |
| EPCC_Complete_Module_Registry_v1_0.md | Registry | Re-issue with v2.3 additions | EPCC_ModuleRegistry_v1_0.md | Pending |
| EPCC_UI_Design_System_v2_0.md | Standards | Re-issue | EPCC_UIDesignSystem_v1_0.md | Pending |
| EPCC_Deployment_Tier_Specification_v1_0.md | Standards | Re-issue | EPCC_DeploymentTier_v1_0.md | Pending |
| EPCC_Context_v1.md | Reference | Archive (content distributed into specs) | — | Archived |
| EPCC_HistoricalDataImport_v1_0.md | Spec | Re-issue under HDI prefix | HDI_HistoricalDataImport_Spec_v1_0.md | Pending |

### 2.3 Project Documents (read-only inputs)

| Legacy Filename | Type | Disposition |
|---|---|---|
| Project.md | Requirements | Reference only — drives M27/M28 design. Not re-issued. |
| EPMS_Blueprint_v2_Implementation_Ready.docx | Strategy | Reference only. Not re-issued. |
| 4410CONMEP00RPRTDBR_R1.pdf | MEP DBR | Reference only — input for KDMC project, not system spec. |
| KDMC_CC_Transformed.xlsm | Workbook | **Reference only** per U2-a. Replaced by EPCC. |

---

## 3. ARCHIVE FOLDER STRUCTURE

```
/00_Governance/Archive/
├── 2026_05_03_Round0_Legacy/
│   ├── M01_Project_Registry_v2.1_ARCHIVED.md
│   ├── M02_Structure_WBS_v2_1_ARCHIVED.md
│   ├── ...
│   ├── EPCC_Standards_Memory_v5_0_ARCHIVED.md
│   ├── EPCC_Standards_Memory_v5_1_ARCHIVED.md
│   ├── EPCC_Standards_Memory_v5_2_ARCHIVED.md
│   ├── EPCC_Standards_Memory_v5_3_ARCHIVED.md
│   └── EPCC_Context_v1_ARCHIVED.md
└── README.md  ← explains folder dating + disposition rule
```

---

## 4. AMENDMENT FILE CONSOLIDATION RULE

Several legacy specs are AMENDMENT files (M02 v2.1, M04 v2.2, M05 v2.3) — they describe only changed blocks relative to a base version. This is a structural inconsistency.

**Resolution:** During re-issue under v1.0:
1. Take the base version (e.g., M02 v2.0 if available, otherwise reconstruct from amendments)
2. Apply all amendments
3. Produce a single consolidated v1.0 spec — no amendment chains
4. The consolidated v1.0 is the only canonical version going forward
5. Future changes use Major/Minor versioning, never amendment files

This eliminates the "spec chain" problem flagged in Audit Round 00.

---

## 5. DISPOSITION ENUM

| Disposition | Meaning |
|---|---|
| `Re-issue` | Content carries forward into new v1.0 spec, possibly consolidated/refactored |
| `Archive` | Moved to Archive folder; not re-issued; retained for historical reference |
| `Superseded` | Replaced by a different artefact in new structure |
| `Reference only` | External input document; not part of EPCC artefact lifecycle |
| `Source` | Used as input for v1.0 creation; archived after consolidation |

---

## 6. PROCESSING ORDER

```
Step 1 (Round 0): Manifest created. Archive folder structure created.
Step 2 (per round): When new v1.0 spec is published:
  - Original legacy file moves to Archive
  - Filename gets _ARCHIVED suffix
  - VersionLog updated
  - This manifest updated with `Status = Archived`
Step 3: After all 23 modules re-issued, retire this manifest to Archive itself.
```

---

*v1.0 — locked. Updated as legacy files are processed during re-issue rounds.*
