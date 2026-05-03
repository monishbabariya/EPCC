# M02 — Structure & WBS
## Spec v1.0
**Status:** Locked
**Locked:** Yes
**Author:** PMO Director / System Architect
**Created:** 2026-05-03 | **Last Updated:** 2026-05-03
**Last Audited:** v1.0 on 2026-05-03
**Reference Standards:** EPCC_NamingConvention_v1_0.md, X8_GlossaryENUMs_v0_3.md, M34_SystemAdminRBAC_Spec_v1_0.md, M01_ProjectRegistry_Spec_v1_0.md
**Layer:** L2 Control — Planning & Structure
**Phase:** 1 — Foundational
**Build Priority:** 🔴 Critical (precedes M03, M04, M06, M07)
**Folder:** /03_L2_Planning/
**Re-Issue Of:** Legacy M02_Structure_WBS_v2.0 (base) + v2.1 (amendment) — consolidated standalone

---

## CHANGE LOG

| Version | Date | Change Summary |
|---|---|---|
| v1.0 | 2026-05-03 | Initial standalone consolidated spec. Re-issued from legacy v2.0 + v2.1 amendment. All 10 OQ-1 decisions locked. Three-tier template model (System_Default → Tenant_Standard → Project_Template). 5-ID chain validation per ES-DI-001. BAC integrity workflow (Confirmed / Stale_Pending_VO). Single-owner rule applied (BACIntegrityLedger owned by M02; M07 reads via API). |

---

## BLOCK 1 — IDENTITY

```
Module ID                : M02
Module Name              : Structure & WBS
Layer                    : L2 Control — Planning & Structure
Decision It Enables      : Is the project's work decomposition (WBS) and
                           commercial decomposition (BOQ within Packages)
                           complete, internally consistent, role-appropriately
                           visible, and BAC-integrity-tracked — providing every
                           other module with the structural backbone for
                           schedule, progress, cost, and EVM?

Primary User             : QS_MANAGER + PLANNING_ENGINEER
Secondary Users          : PMO_DIRECTOR (template + governance),
                           PROJECT_DIRECTOR (project-scoped CRUD),
                           FINANCE_LEAD (rate + financial reads),
                           SITE_MANAGER (read-only own packages)
Module Icon              : LayoutGrid (Lucide)
Navigation Section       : L2 Control — Planning & Structure
```

---

## BLOCK 2 — SCOPE BOUNDARY

### INCLUDES

| Capability | Description |
|---|---|
| WBS hierarchy | Variable depth via `parent_id` self-reference. Project-configurable minimum (sector default) per OQ-1.1. |
| Package master | Work packages within project — contractual + execution units |
| BOQ master | Bill of Quantities items with quantity + actual rate |
| BOQ ↔ WBS many-to-many | `BOQWBSMap` junction with `is_primary_wbs=true` constraint per BOQ |
| Unit master | 3-tier governance: Standard_Core (locked) / Domain_Specific (PMO_DIR) / Custom (PROJECT_DIR own) |
| **Three-tier package templates** | System_Default (Anthropic ships) → Tenant_Standard (PMO validates) → Project_Template (per-project customisation). **Copy-down only; no upward promotion.** |
| Package template versioning | Per-tier with delta tracking; PMO can lock a Tenant_Standard version |
| CSV bulk import | Modal-gated per session: `Create_Only` OR `Create_And_Update` (sparse update). All-or-nothing commit. |
| Role-controlled rate display | Field-level permission with 3 spike formulas: `Loaded`, `Indexed`, `Flat_Redacted` |
| BAC computation per package | `bac_amount = SUM(BOQItem.actual_rate × quantity)` per package |
| BAC integrity tracking | `bac_integrity_status` ENUM: `Confirmed / Stale_Pending_VO` (locked at 2 values per OQ-1.2) |
| BACIntegrityLedger | Append-only, immutable forensic record. **Owned by M02; read by M07 via API only.** |
| VO materialisation receiving-end | M05 triggers; M02 executes BOQ updates per Option A/B/C; confirms back to M05/M07 |
| 5-ID chain validation | `BOQ_ID → WBS_ID → PKG_ID → CONTRACT_ID → PHASE_ID` per ES-DI-001. PHASE_ID = snapshot of `Project.current_phase` at BOQ creation |
| BOQ origin tracking | `boq_origin` ENUM: `Manual / CSV_Import / VO_Materialisation / Template_Applied / HDI_Seed` |
| WBS code generation | Auto-generated dotted notation (e.g., `3.1.2`); UI drag-and-drop reorders + reassigns codes |
| `IDGovernanceLog` | Audit log for 5-ID chain creation and validation events |

### EXCLUDES

| Excluded | Where It Lives |
|---|---|
| Schedule (planned dates, baselines, S-curves, PV) | M03 Planning |
| Actual cost transactions, RA bills, sub-contracts | M06 Financial |
| Rate sourcing (CPWD DSR, market rates) | External; M06 stores actuals |
| Progress capture (% complete, NCRs, DLP) | M04 Execution |
| EVM (CPI, SPI, EAC, ETC, VAC, TCPI) | M07 EVM Engine |
| VO trigger workflow (initiation, approval, SLA) | M05 Risk & Change |
| EAC suspension logic during VO materialisation | M07 EVM Engine |
| Stage gate decisions tied to baseline lock | M08 Gate Control |
| Document storage (drawings, specs, BOQs as PDFs) | M12 Document Control + MinIO |
| QS measurement book entries | M14 QS Measurement Book |
| Tendering workflow + BOQ pricing strategy | M29 Tendering & Award |
| BIM model integration | PF02 BIM Integration (Phase 4) |
| Unit conversion (m↔ft, kg↔ton) | Out of v1.0 scope per OQ-1.9 |

---

## BLOCK 3 — DATA ARCHITECTURE

### 3a. Entity Overview

| Entity | Description | Cardinality | Schema Owner |
|---|---|---|---|
| `WBSNode` | Hierarchical work breakdown with parent_id self-reference | Many per project | M02 |
| `Package` | Work package within project | Many per project | M02 |
| `BOQItem` | Bill of Quantities line item | Many per package | M02 |
| `BOQWBSMap` | M:N junction; one WBS marked primary per BOQ | Many | M02 |
| `UnitMaster` | 3-tier governed units (Standard_Core / Domain_Specific / Custom) | System + tenant + project tiers | M02 |
| `PackageTemplate` | Three-tier reusable package skeleton | Many | M02 |
| `PackageTemplateVersion` | Versioned snapshots with delta tracking | Many per template | M02 |
| `PackageTemplateBOQ` | BOQ items within template (skeleton) | Many per template version | M02 |
| `BACIntegrityLedger` | **Append-only, immutable** audit of BAC changes | Many per package | M02 (M07 reads via API) |
| `IDGovernanceLog` | 5-ID chain creation + validation audit | Many per BOQ | M02 |
| `CSVImportSession` | Per-session import metadata | Many per project | M02 |
| `CSVImportRecord` | Per-row audit of CSV import | Many per session | M02 |

### 3b. Entity: `WBSNode`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `wbs_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | FK → M34.Tenant | LINK → M34.Tenant |
| `project_id` | UUID | Y | FK → M01.Project | LINK → M01.Project |
| `wbs_code` | VARCHAR(100) | Y | Auto-generated dotted notation per OQ-1.8. e.g., `3.1.2`. Unique within project. | SYSTEM |
| `wbs_name` | VARCHAR(300) | Y | Min 3 chars | INPUT |
| `parent_id` | UUID | N | FK → WBSNode (self-reference). NULL = root. | LINK → WBSNode |
| `wbs_level` | INTEGER | Y | Auto-calculated: 0 for root, +1 per parent. | CALC |
| `position_in_parent` | INTEGER | Y | Sibling ordering. Auto-assigned on create; reassigned on drag-reorder. | SYSTEM |
| `package_id` | UUID | N | FK → Package. WBS leaf nodes typically map to packages. | LINK → Package |
| `activity_type` | ENUM | N | `Civil / Structural / MEP / HVAC / Electrical / Plumbing / Medical_Equipment / Landscape / Commissioning / Indirect / Other`. CodeMaster Discipline. | INPUT |
| `description` | TEXT | N | Max 2000 chars | INPUT |
| `is_baseline_locked` | BOOLEAN | Y | Default false. Set true when M03 baseline locks at SG-6. | SYSTEM (from M08 signal) |
| `baseline_locked_at` | TIMESTAMP | N | Auto on lock | SYSTEM |
| `created_by` | UUID | Y | — | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_by` | UUID | Y | Auto | LINK → M34.User |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true. Soft-delete blocked if child WBS or BOQ exists. | SYSTEM |

**Composite uniqueness:** (`tenant_id`, `project_id`, `wbs_code`). FK index on `parent_id` for tree queries.

---

### 3c. Entity: `Package`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `package_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | FK → M01.Project | LINK → M01.Project |
| `package_code` | VARCHAR(30) | Y | Format: `PKG-{seq}` auto-increment per project; PMO_DIRECTOR can override. Unique within project. | SYSTEM (with override) |
| `package_name` | VARCHAR(200) | Y | Min 3 chars | INPUT |
| `package_type` | ENUM | Y | `Civil / Structural / MEP / HVAC / Medical_Equipment / Specialist / Indirect / Mixed` | INPUT |
| `contract_id` | UUID | Y | FK → M01.Contract. Determines commercial governance. | LINK → M01.Contract |
| `applied_template_id` | UUID | N | FK → PackageTemplate if package was created from a template | LINK → PackageTemplate |
| `applied_template_version_id` | UUID | N | FK → PackageTemplateVersion | LINK → PackageTemplateVersion |
| `bac_amount` | DECIMAL(15,2) | Y | Auto = SUM(BOQItem.actual_amount). Recalculated on BOQ change UNLESS bac_integrity_status = Stale_Pending_VO. | CALC |
| `bac_integrity_status` | ENUM | Y | Per X8 §3.27 `BACIntegrityStatus`: `Confirmed / Stale_Pending_VO`. Default `Confirmed`. | SYSTEM |
| `pending_vo_id` | UUID | N | FK → M05.VariationOrder. Populated when bac_integrity_status = Stale_Pending_VO. | LINK → M05.VariationOrder |
| `bac_stale_since` | TIMESTAMP | N | Set when bac_integrity_status → Stale_Pending_VO. Cleared on Confirmed. | SYSTEM |
| `last_bac_confirmed_at` | TIMESTAMP | Y | Updated each time bac_integrity_status → Confirmed. Default = created_at. | SYSTEM |
| `bac_version` | INTEGER | Y | Auto-increment on every confirmed BAC change. Starts at 1. | SYSTEM |
| `package_status` | ENUM | Y | Per X8 §3.5 `RecordStatus`: `Draft / Active / Suspended / Archived / Deleted`. Default `Draft`. | SYSTEM |
| `description` | TEXT | N | Max 2000 chars | INPUT |
| `created_by` | UUID | Y | — | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_by` | UUID | Y | Auto | LINK → M34.User |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true. Soft-delete blocked if BOQ items exist. | SYSTEM |

**Composite uniqueness:** (`tenant_id`, `project_id`, `package_code`).

---

### 3d. Entity: `BOQItem`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `boq_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | — | LINK → M01.Project |
| `package_id` | UUID | Y | FK → Package | LINK → Package |
| `contract_id` | UUID | Y | FK → M01.Contract (denormalised from package for ID chain) | LINK → M01.Contract |
| `phase_at_creation` | ENUM | Y | Per X8 §3.9 `Phase`. Snapshot of Project.current_phase at BOQ creation. **Immutable.** Per OQ-1.4. | SYSTEM (snapshot) |
| `boq_code` | VARCHAR(50) | Y | Format: `{PKG_CODE}-{seq}` auto-generated. Unique within package. | SYSTEM |
| `boq_description` | TEXT | Y | Min 10 chars; max 2000 chars | INPUT |
| `unit_master_id` | UUID | Y | FK → UnitMaster (must be active in tier-resolution: Standard_Core or current tenant's Domain_Specific or current project's Custom) | LINK → UnitMaster |
| `quantity` | DECIMAL(15,4) | Y | > 0 | INPUT |
| `actual_rate` | DECIMAL(15,4) | Y | > 0. **Field-level permission applies to read.** | INPUT |
| `actual_amount` | DECIMAL(15,2) | Y | Auto = quantity × actual_rate | CALC |
| `boq_origin` | ENUM | Y | Per X8 §3.28 `BOQOrigin`: `Manual / CSV_Import / VO_Materialisation / Template_Applied / HDI_Seed` | SYSTEM |
| `source_template_version_id` | UUID | N | FK → PackageTemplateVersion if boq_origin=Template_Applied | LINK → PackageTemplateVersion |
| `source_csv_session_id` | UUID | N | FK → CSVImportSession if boq_origin=CSV_Import | LINK → CSVImportSession |
| `source_vo_id` | UUID | N | FK → M05.VariationOrder if boq_origin=VO_Materialisation | LINK → M05.VariationOrder |
| `source_materialisation_id` | UUID | N | FK → M05.VOBOQMaterialisation | LINK → M05.VOBOQMaterialisation |
| `source_hdi_session_id` | UUID | N | FK → HDI session id | LINK → HDI |
| `pending_vo_materialisation_id` | UUID | N | FK → M05.VOBOQMaterialisation. Set when item is under VO materialisation review. | LINK → M05.VOBOQMaterialisation |
| `bac_contribution_confirmed` | BOOLEAN | Y | Default true. Set false when item under VO materialisation. Set true on materialisation completion. | SYSTEM |
| `created_by` | UUID | Y | — | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_by` | UUID | Y | Auto | LINK → M34.User |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |

**Composite uniqueness:** (`tenant_id`, `project_id`, `package_id`, `boq_code`).

**Field-level permission:** `actual_rate` and `actual_amount` are role-tiered (see Block 4a).

---

### 3e. Entity: `BOQWBSMap`

Many-to-many junction. Each BOQ has exactly one WBS marked `is_primary_wbs=true`.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `map_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | — | LINK → M01.Project |
| `boq_id` | UUID | Y | FK → BOQItem | LINK → BOQItem |
| `wbs_id` | UUID | Y | FK → WBSNode (must be in same project) | LINK → WBSNode |
| `is_primary_wbs` | BOOLEAN | Y | Exactly one `true` per boq_id (enforced by trigger or BR-02-005) | INPUT |
| `allocation_pct` | DECIMAL(5,4) | N | If BOQ split across multiple WBS, percentage allocated to this WBS. Sum across BOQ = 1.0000. NULL on primary-only mappings. | INPUT |
| `created_by` | UUID | Y | — | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |

**Composite uniqueness:** (`tenant_id`, `boq_id`, `wbs_id`).
**Append-only audit (no soft delete or update):** if mapping changes, delete and recreate.

---

### 3f. Entity: `UnitMaster`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `unit_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | N | NULL = Standard_Core (system-wide). Set for Domain_Specific (tenant) or Custom (project). | LINK → M34.Tenant |
| `project_id` | UUID | N | NULL unless tier=Custom. Set for project-scoped Custom units. | LINK → M01.Project |
| `unit_code` | VARCHAR(20) | Y | e.g., `kg`, `m3`, `nos`, `LS` (lump sum). Lowercase preferred. | INPUT |
| `unit_label` | VARCHAR(100) | Y | Display name e.g., "Kilogram", "Cubic Metre" | INPUT |
| `unit_tier` | ENUM | Y | `Standard_Core / Domain_Specific / Custom` | INPUT |
| `category` | ENUM | Y | `Mass / Volume / Length / Area / Count / Time / Currency / LumpSum / Other` | INPUT |
| `unit_system` | ENUM | Y | `Metric / Imperial`. v1.0 ships Metric only per OQ-1.9. | SYSTEM |
| `description` | TEXT | N | — | INPUT |
| `created_by` | UUID | Y | Standard_Core: SEED; others: User | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |

**Composite uniqueness:** (`tenant_id`, `project_id`, `unit_code`) where NULL is treated as a single value per tier.

**Tier resolution at BOQ creation:** Lookup order — Custom (project-scoped) → Domain_Specific (tenant-scoped) → Standard_Core (system-wide). First match wins.

**Permission mapping:**
- `Standard_Core` editable only by `SYSTEM_ADMIN`
- `Domain_Specific` editable by `PMO_DIRECTOR` within tenant
- `Custom` editable by `PROJECT_DIRECTOR` on own project

---

### 3g. Entity: `PackageTemplate`

**Three-tier model per OQ-1.5.** Copy-down only; no upward promotion.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `template_id` | UUID | Y | Auto-generated | SYSTEM |
| `template_tier` | ENUM | Y | Per X8 §3.30 `PackageTemplateTier`: `System_Default / Tenant_Standard / Project_Template` | SYSTEM |
| `tenant_id` | UUID | N | NULL for System_Default; set for Tenant_Standard and Project_Template | LINK → M34.Tenant |
| `project_id` | UUID | N | NULL unless tier=Project_Template | LINK → M01.Project |
| `parent_template_id` | UUID | N | FK → PackageTemplate. Set when this template was copied FROM another template (lineage). | LINK → PackageTemplate |
| `template_code` | VARCHAR(50) | Y | e.g., `Hospital_DBOT_Civil`. Unique within tier-scope. | INPUT |
| `template_name` | VARCHAR(200) | Y | Display name | INPUT |
| `description` | TEXT | N | Max 2000 chars | INPUT |
| `package_type` | ENUM | Y | Same as Package.package_type | INPUT |
| `applicable_sectors` | JSONB | Y | Array of `SectorTopLevel` values e.g., `["Healthcare"]` | INPUT |
| `applicable_sub_types` | JSONB | N | Array of CodeMaster sector_sub_type codes | INPUT |
| `current_version_id` | UUID | N | FK → PackageTemplateVersion (the active version) | LINK → PackageTemplateVersion |
| `created_by` | UUID | Y | — | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_by` | UUID | Y | Auto | LINK → M34.User |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |

**Composite uniqueness:** (`template_tier`, `tenant_id`, `project_id`, `template_code`).

**Promotion direction enforcement (BR-02-035):**
- `System_Default` parent_template_id MUST be NULL
- `Tenant_Standard` parent_template_id MUST reference a `System_Default` (or be NULL for greenfield Tenant Standards)
- `Project_Template` parent_template_id MUST reference a `Tenant_Standard` (or be NULL for greenfield)
- **NEVER:** Tenant_Standard.parent_template_id → Project_Template (forbidden upward reference)
- **NEVER:** Project_Template.parent_template_id → System_Default (must go through Tenant_Standard tier)

---

### 3h. Entity: `PackageTemplateVersion`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `version_id` | UUID | Y | Auto-generated | SYSTEM |
| `template_id` | UUID | Y | FK → PackageTemplate | LINK → PackageTemplate |
| `version_number` | INTEGER | Y | Auto-increment per template_id | SYSTEM |
| `version_label` | VARCHAR(50) | N | Optional human-readable e.g., "v1.0", "Q4-2026-rates" | INPUT |
| `change_summary` | TEXT | Y | Min 30 chars. Required for every version after v1. | INPUT |
| `delta_from_previous` | JSONB | N | Auto-computed delta vs previous version (added/modified/removed BOQ items) | CALC |
| `lock_state` | ENUM | Y | Per X8 §3.6 `LockState`: `Unlocked / Pending_Review / Locked / Archived`. Default `Unlocked`. | SYSTEM |
| `locked_by` | UUID | N | FK → M34.User. Required if lock_state = Locked. Must be PMO_DIRECTOR for Tenant_Standard. | LINK → M34.User |
| `locked_at` | TIMESTAMP | N | Auto on lock | SYSTEM |
| `pmo_validated` | BOOLEAN | Y | Default false. PMO_DIRECTOR sets true on quality validation. Required true for Tenant_Standard before any project applies it. | INPUT |
| `created_by` | UUID | Y | — | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |

**Composite uniqueness:** (`template_id`, `version_number`).

**Locked versions are immutable:** once `lock_state = Locked`, no field on this version or its child PackageTemplateBOQ rows can change. Edits force a new version via copy.

---

### 3i. Entity: `PackageTemplateBOQ`

BOQ skeleton items within a template version.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `template_boq_id` | UUID | Y | Auto-generated | SYSTEM |
| `version_id` | UUID | Y | FK → PackageTemplateVersion | LINK → PackageTemplateVersion |
| `sequence` | INTEGER | Y | Auto-assigned, drag-reorderable | SYSTEM |
| `boq_description` | TEXT | Y | Min 10 chars | INPUT |
| `unit_master_id` | UUID | Y | FK → UnitMaster (Standard_Core only — to ensure cross-tenant compatibility) | LINK → UnitMaster |
| `default_quantity` | DECIMAL(15,4) | N | Indicative quantity. NULL means quantity must be entered when applied. | INPUT |
| `default_actual_rate` | DECIMAL(15,4) | N | Indicative basic rate. NULL means rate must be entered when applied. PMO_DIRECTOR is encouraged to set this for Tenant_Standards based on company experience. | INPUT |
| `is_optional` | BOOLEAN | Y | Default false. If true, applying tenant can choose to skip this item. | INPUT |
| `notes` | TEXT | N | Notes for users applying the template | INPUT |

**Application behaviour:** When a Package is created from a Tenant_Standard template, all PackageTemplateBOQ rows are copied to BOQItem with:
- `quantity` = `default_quantity` (or 0 if NULL — user must enter)
- `actual_rate` = `default_actual_rate` (or 0 if NULL — user must enter)
- `boq_origin` = `Template_Applied`
- `source_template_version_id` = applied version_id

---

### 3j. Entity: `BACIntegrityLedger` (immutable, append-only)

**Owned by M02 per OQ-1.10 single-owner rule.** M07 reads via `GET /internal/v1/m02/bac-ledger?package_id=X` API.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `ledger_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | — | LINK → M01.Project |
| `package_id` | UUID | Y | FK → Package | LINK → Package |
| `change_type` | ENUM | Y | `VO_Materialisation / Baseline_Revision / Correction / Initial_BAC / Template_Applied / CSV_Import / HDI_Seed` | SYSTEM |
| `trigger_entity` | VARCHAR(50) | Y | e.g., "VOBOQMaterialisation", "BaselineExtension", "BOQItem_Manual" | SYSTEM |
| `trigger_id` | UUID | Y | FK → the trigger entity record | LINK |
| `old_bac` | DECIMAL(15,2) | Y | Package BAC before this change | SYSTEM |
| `new_bac` | DECIMAL(15,2) | Y | Package BAC after this change | CALC |
| `bac_delta` | DECIMAL(15,2) | Y | new_bac − old_bac | CALC |
| `bac_version_after` | INTEGER | Y | Package.bac_version after this change | SYSTEM |
| `changed_by` | UUID | Y | FK → User who triggered the change | LINK → M34.User |
| `changed_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `audit_note` | TEXT | N | Auto-populated for VO: "VO {vo_code}: option {A/B/C}" | SYSTEM or INPUT |

**IMMUTABILITY ENFORCED AT DB LEVEL:**
- No `is_active`, no `updated_at`, no soft-delete fields
- DB migration: `REVOKE UPDATE, DELETE ON bac_integrity_ledger FROM app_role`
- Append-only via INSERT only

---

### 3k. Entity: `IDGovernanceLog`

5-ID chain creation + validation audit per ES-DI-001.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `log_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | — | LINK → M01.Project |
| `boq_id` | UUID | Y | FK → BOQItem | LINK → BOQItem |
| `wbs_id` | UUID | Y | — | LINK → WBSNode |
| `package_id` | UUID | Y | — | LINK → Package |
| `contract_id` | UUID | Y | — | LINK → M01.Contract |
| `phase_at_creation` | VARCHAR(50) | Y | Phase enum string snapshot | SYSTEM |
| `chain_validation_status` | ENUM | Y | `Passed / Failed` | SYSTEM |
| `chain_failure_reason` | TEXT | N | Required if Failed | SYSTEM |
| `created_by` | UUID | Y | — | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |

**Append-only.** No updates.

---

### 3l. Entity: `CSVImportSession`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `session_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | LINK → M34.Tenant |
| `project_id` | UUID | Y | — | LINK → M01.Project |
| `import_target` | ENUM | Y | `BOQItem / WBSNode / Package` | INPUT |
| `import_mode` | ENUM | Y | `Create_Only / Create_And_Update`. **No default** — user must explicitly select per OQ-1.6. | INPUT |
| `source_file_name` | VARCHAR(300) | Y | Original CSV filename | SYSTEM |
| `source_file_size_bytes` | BIGINT | Y | Max 20 MB per OQ-2.7 | SYSTEM |
| `total_rows` | INTEGER | Y | After header strip. Max 50,000. | SYSTEM |
| `validation_status` | ENUM | Y | `Pending / Valid / Invalid` | SYSTEM |
| `validation_report` | JSONB | N | Per-row pass/fail summary | SYSTEM |
| `commit_status` | ENUM | Y | `Not_Committed / Committed / Rolled_Back` | SYSTEM |
| `committed_at` | TIMESTAMP | N | Auto on commit | SYSTEM |
| `committed_by` | UUID | N | FK → User | LINK → M34.User |
| `created_by` | UUID | Y | — | LINK → M34.User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |

---

### 3m. Entity: `CSVImportRecord`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `record_id` | UUID | Y | Auto-generated | SYSTEM |
| `session_id` | UUID | Y | FK → CSVImportSession | LINK → CSVImportSession |
| `row_number` | INTEGER | Y | 1-indexed source row | SYSTEM |
| `action` | ENUM | Y | `Created / Updated / Failed / Skipped_Duplicate` | SYSTEM |
| `target_record_id` | UUID | N | FK to created/updated entity. NULL if Failed/Skipped. | SYSTEM |
| `failure_reason` | TEXT | N | Required if action = Failed | SYSTEM |
| `changed_fields` | JSONB | N | If Updated — which fields changed and from/to | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |

**Append-only.**

---

## BLOCK 4 — DATA POPULATION RULES

### 4a. Role × Action Permission Matrix

References M34 canonical role names. **`actual_rate` and `actual_amount` field-level permission applies on read** — different roles see different formulas.

| Action | SYSTEM_ADMIN | PMO_DIRECTOR | PORTFOLIO_MGR | PROJECT_DIR | PLANNING_ENG | QS_MANAGER | FINANCE_LEAD | PROCUREMENT | SITE_MGR | OTHERS | READ_ONLY |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Create WBS | ❌ | ✅ | ❌ | ✅ (own) | ✅ (own) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Edit WBS | ❌ | ✅ | ❌ | ✅ (own) | ✅ (own) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Reorder WBS | ❌ | ✅ | ❌ | ✅ (own) | ✅ (own) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Soft-delete WBS | ❌ | ✅ | ❌ | ✅ (own) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Create Package | ❌ | ✅ | ❌ | ✅ (own) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Edit Package | ❌ | ✅ | ❌ | ✅ (own) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Apply Template to Project | ❌ | ✅ | ❌ | ✅ (own) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Create BOQ Item | ❌ | ✅ | ❌ | ✅ (own) | ❌ | ✅ (own) | ❌ | ❌ | ❌ | ❌ | ❌ |
| Edit BOQ quantity | ❌ | ✅ | ❌ | ✅ (own) | ❌ | ✅ (own) | ❌ | ❌ | ❌ | ❌ | ❌ |
| Edit BOQ rate | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **View actual rate** | ✅ | ✅ | ❌ (Loaded) | ❌ (Loaded) | ❌ (Indexed) | ❌ (Indexed) | ✅ | ❌ (Loaded) | ❌ (Redacted) | ❌ (Redacted) | ❌ (Redacted) |
| CSV import (Create_Only) | ❌ | ✅ | ❌ | ✅ (own) | ❌ | ✅ (own) | ❌ | ❌ | ❌ | ❌ | ❌ |
| CSV import (Create_And_Update) | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Edit Standard_Core unit | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Edit Domain_Specific unit | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Edit Custom unit (project) | ❌ | ❌ | ❌ | ✅ (own) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Create Tenant_Standard template | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Validate Tenant_Standard (pmo_validated=true) | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Lock Tenant_Standard version | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Create Project_Template | ❌ | ✅ | ❌ | ✅ (own) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| View BACIntegrityLedger | ✅ | ✅ | ❌ | ✅ (own, summary) | ❌ | ❌ | ✅ (own) | ❌ | ❌ | ❌ | ❌ |
| Read all WBS / BOQ structure | ✅ | ✅ | ✅ | ✅ (own) | ✅ (own) | ✅ (own) | ✅ | ✅ (own) | ✅ (own pkgs) | ✅ (own) | ✅ (own) |

**Rate display formula assignment (per OQ-1.3):**

| Role | Formula | Display Result |
|---|---|---|
| `SYSTEM_ADMIN`, `PMO_DIRECTOR`, `FINANCE_LEAD`, `EXTERNAL_AUDITOR` | None | Actual rate shown |
| `PORTFOLIO_MANAGER`, `PROJECT_DIRECTOR`, `PROCUREMENT_OFFICER`, `COMPLIANCE_MANAGER` | `Loaded` | Rate × loaded factor (default +15%) |
| `PLANNING_ENGINEER`, `QS_MANAGER` | `Indexed` | Rate × indexing factor (CPI-style; tenant-configurable, default +8%) |
| `SITE_MANAGER`, `READ_ONLY` | `Flat_Redacted` | Literal `[RESTRICTED]` |

**Spike factor configuration:** stored in tenant feature flags (M34) — `M02_LOADED_FACTOR` (default 1.15) and `M02_INDEXED_FACTOR` (default 1.08).

---

### 4b. Mandatory Fields at Creation

**WBSNode:** `tenant_id, project_id, wbs_name, parent_id (or null for root)`
**Package:** `tenant_id, project_id, package_name, package_type, contract_id`
**BOQItem:** `tenant_id, project_id, package_id, contract_id, boq_description, unit_master_id, quantity, actual_rate`
**BOQWBSMap:** `boq_id, wbs_id, is_primary_wbs` (exactly one true per boq_id)

---

### 4c. Entry Methods

| Field group | Method |
|---|---|
| WBS hierarchy | Tree builder with drag-drop reorder + indent/outdent. Right-click "Insert child" / "Insert sibling". |
| Package master | Form (single-screen) + "Apply template" button to instantiate from Tenant_Standard |
| BOQ items | Inline-editable table within package. Columns: code (auto), description, unit (dropdown from tier-resolved UnitMaster), quantity, rate (role-tiered display), amount (calc). |
| BOQ-WBS mapping | Two-pane: BOQ list (left), WBS tree (right). Drag BOQ onto WBS to map. Indicator shows primary WBS. |
| Unit master | Tabular editor with tier filter |
| Template apply | Wizard: select template tier → version → confirm BOQ defaults |
| CSV import | Modal-gated: select target (BOQ/WBS/Package) → mode (Create_Only / Create_And_Update — **no default**) → upload → preview validation → commit |

---

### 4d. Default Values

| Field | Default | Source |
|---|---|---|
| `Package.bac_integrity_status` | `Confirmed` | OQ-1.2 |
| `Package.bac_version` | 1 | — |
| `BOQItem.boq_origin` | `Manual` (unless created via template/CSV/VO/HDI flows) | OQ-1.7 |
| `BOQItem.bac_contribution_confirmed` | `true` | — |
| `WBSNode.position_in_parent` | max(siblings)+1 | OQ-1.8 |
| `Loaded factor` | 1.15 (+15%) | Tenant feature flag |
| `Indexed factor` | 1.08 (+8%) | Tenant feature flag |
| CSV file size limit | 20 MB / 50,000 rows | OQ-2.7 |

---

## BLOCK 5 — FILTERS AND VIEWS

### 5a. WBS Tree View (default)

```
Tree control with expand/collapse. Each node shows:
  wbs_code · wbs_name · activity_type · child count · BAC roll-up
Filters: activity_type | baseline_locked | depth
Drag-drop reorder (PMO/PROJECT_DIRECTOR/PLANNING_ENGINEER only)
Auto-render flat-table view for ≥6-level deep WBS
```

### 5b. Package Master List

```
Table: package_code | package_name | package_type | contract | bac_amount | bac_integrity | template applied | status
Filters: package_type | contract | bac_integrity_status | template lineage
Highlight: rows with bac_integrity_status = Stale_Pending_VO (amber border)
Bulk actions: PMO_DIRECTOR can bulk-archive
```

### 5c. BOQ Within Package View

```
Inline-editable table with role-tiered rate column:
  boq_code | description | unit | quantity | rate | amount | origin | wbs_links
Filter: unit_tier | boq_origin | bac_contribution_confirmed
Sort default: boq_code ASC
```

### 5d. BOQ-WBS Mapping View

```
Two-pane:
  Left  : BOQ list (current package)
  Right : WBS tree (project-wide)
Visual: lines connecting BOQ ↔ WBS. Primary WBS highlighted.
Action: drag BOQ onto WBS to add mapping; click line to set primary.
```

### 5e. Unit Master Editor

```
Tier filter: All / Standard_Core / Domain_Specific (tenant) / Custom (project)
Editable rows per tier permission. Standard_Core marked read-only.
Sort: category → unit_code
```

### 5f. Package Template Library

```
Three tabs: System_Default | Tenant_Standard | Project_Template

System_Default tab:
  Read-only list of system-shipped templates
  Action per template: "Copy to Tenant Standard" (PMO_DIRECTOR)

Tenant_Standard tab:
  List with version count, last_updated, pmo_validated badge, lock status
  Action: View versions, Edit current, Lock version, Apply to project

Project_Template tab:
  List of project-scoped templates
  Action: View, Edit (own project), Apply to package
```

### 5g. CSV Import Wizard

```
Step 1: Target selection (BOQ / WBS / Package)
Step 2: Mode selection — REQUIRED, no default per OQ-1.6:
  [ ] Create_Only — fail on duplicate
  [ ] Create_And_Update — sparse update on match
Step 3: File upload (max 20 MB / 50,000 rows)
Step 4: Preview validation report (per-row pass/fail; downloadable)
Step 5: Confirm commit (all-or-nothing)
```

### 5h. BAC Integrity Dashboard (PMO_DIRECTOR / FINANCE_LEAD)

```
KPI strip:
  Total packages | Confirmed | Stale_Pending_VO | Avg days stale
Table: package | bac_amount | integrity_status | stale_since | pending_vo
Drill: Click package → BACIntegrityLedger trail
```

---

## BLOCK 6 — BUSINESS RULES

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---|---|---|---|---|
| BR-02-001 | WBS create | Validate: unique wbs_code within project; parent_id resolves to active WBSNode in same project; resulting depth ≥ Project.min_wbs_depth (per OQ-1.1) | Block save if duplicate, invalid parent, or depth < min | 🔴 Real-time |
| BR-02-002 | WBS create | Auto-generate wbs_code = `{parent.wbs_code}.{max_sibling_position+1}` per OQ-1.8 | Persist generated code | 🔴 Real-time |
| BR-02-003 | WBS reorder (drag) | Update position_in_parent + reassign wbs_code for moved node + cascading children | Persist new tree state. Audit log entry. | 🔴 Real-time |
| BR-02-004 | BOQ create | Validate 5-ID chain per ES-DI-001: BOQ_ID + WBS_ID (via BOQWBSMap primary) + PKG_ID + CONTRACT_ID + PHASE_ID. PHASE_ID = snapshot of Project.current_phase per OQ-1.4. | Block save if any chain link missing/invalid. Create IDGovernanceLog entry. | 🔴 Real-time |
| BR-02-005 | BOQWBSMap create/update | Verify exactly one row per boq_id has is_primary_wbs=true | Block save if zero or multiple primaries | 🔴 Real-time |
| BR-02-006 | BOQ save | Auto-calculate actual_amount = quantity × actual_rate | Persist | 🔴 Real-time |
| BR-02-007 | BOQ save | Recalculate Package.bac_amount = SUM(boqs.actual_amount) where bac_contribution_confirmed=true | Update package; increment bac_version (only if bac_integrity_status = Confirmed) | 🔴 Real-time |
| BR-02-008 | BOQ rate read (any role except SYSTEM_ADMIN/PMO_DIRECTOR/FINANCE_LEAD/EXTERNAL_AUDITOR) | Apply spike formula per role mapping (Loaded / Indexed / Flat_Redacted) at API serialiser. **Never expose actual_rate to unauthorised roles.** | Return spiked rate value | 🔴 Real-time |
| BR-02-009 | Package.bac_integrity_status = Stale_Pending_VO | M02 receives signal from M05 (BR-05-028) | Set Package.bac_integrity_status=Stale_Pending_VO; pending_vo_id; bac_stale_since=NOW(). For BOQ items in VO scope: bac_contribution_confirmed=false; pending_vo_materialisation_id set. **Suspend BAC recalculation during this state.** | 🔴 Real-time |
| BR-02-010 | QS Manager initiates VO materialisation (M05 sends In_Progress) | M02 receives instruction | Unlock affected BOQItems for editing (bac_contribution_confirmed=false renders them editable). Defer BAC recalc until materialisation completion. | 🔴 Real-time |
| BR-02-011 | Materialisation Option A: Quantity Revision submitted | QS updates BOQ quantities for VO scope | Validate: all updated items new_quantity > 0. Auto-recalc actual_amount per item. | 🔴 Real-time |
| BR-02-012 | Materialisation Option B: New BOQ Items submitted | QS creates new BOQ items | Validate: all new items pass full 5-ID chain (BR-02-004). All items have actual_rate > 0 and quantity > 0. boq_origin=VO_Materialisation. Create IDGovernanceLog entries. | 🔴 Real-time |
| BR-02-013 | Materialisation Option C: Split (revisions + new items) | Combination of A + B | Apply A logic to revised + B logic to new. **All-or-nothing transaction.** If any item fails, roll back all changes; show error list. | 🔴 Real-time |
| BR-02-014 | Materialisation submitted and all validations pass | Final commit | (1) Recalc Package.bac_amount + increment bac_version. (2) Set bac_integrity_status=Confirmed. Clear pending_vo_id, bac_stale_since. (3) Set bac_contribution_confirmed=true on affected BOQs. (4) Insert BACIntegrityLedger entry: change_type=VO_Materialisation, trigger_id=materialisation_id, old/new BAC. (5) Send confirmation to M05 + M07 + M06 with new bac_snapshot, bac_version. | 🔴 Real-time |
| BR-02-015 | UnitMaster lookup at BOQ creation | Resolve unit_master_id from input unit_code | Tier order: project Custom → tenant Domain_Specific → Standard_Core. First match wins. Block if no match. | 🔴 Real-time |
| BR-02-016 | Standard_Core unit edit attempt | Any non-SYSTEM_ADMIN edits a Standard_Core row | Block 403. Audit log: UNAUTHORISED_STANDARD_CORE_EDIT_ATTEMPT. | 🔴 Real-time |
| BR-02-017 | Tenant_Standard template create | PMO_DIRECTOR copies from System_Default OR creates greenfield | Persist with template_tier=Tenant_Standard, parent_template_id (if copied), tenant_id set. pmo_validated=false initially. | 🔴 Real-time |
| BR-02-018 | Tenant_Standard apply to project | PROJECT_DIRECTOR or PMO_DIRECTOR applies | Validate: pmo_validated=true on the version being applied. Block if not validated. | 🔴 Real-time |
| BR-02-019 | Project_Template create | Cannot have parent_template_id pointing to another Project_Template | Block save if violated | 🔴 Real-time |
| BR-02-020 | Tenant_Standard create | parent_template_id, if set, must reference a System_Default template (not Project_Template) | Block save if upward reference attempted | 🔴 Real-time |
| BR-02-021 | Template version lock | PMO_DIRECTOR sets lock_state=Locked on Tenant_Standard version | Validate: pmo_validated=true. Set locked_by, locked_at. After lock, no field on version or its child PackageTemplateBOQ rows can change (DB constraint). | 🔴 Real-time |
| BR-02-022 | Template version edit attempt on Locked version | Any user tries to edit | Block. Force "Create new version" workflow. | 🔴 Real-time |
| BR-02-023 | Apply template to package | Template versions copy: Each PackageTemplateBOQ → BOQItem with default_quantity (or 0), default_actual_rate (or 0), boq_origin=Template_Applied, source_template_version_id set | Insert BOQ rows in single transaction. | 🔴 Real-time |
| BR-02-024 | CSV import session create | Validate file ≤ 20 MB and ≤ 50,000 rows. Mode must be explicitly selected (Create_Only or Create_And_Update). | Block if oversized or no mode selected | 🔴 Real-time |
| BR-02-025 | CSV import preview | Run validation per row. Generate validation_report JSON with per-row status. | Persist on session record. Show preview to user. | 🔴 Real-time |
| BR-02-026 | CSV import commit (Create_Only mode) | All rows must pass validation; any failure aborts entire import | All-or-nothing transaction | 🔴 Real-time |
| BR-02-027 | CSV import commit (Create_And_Update mode) | Existing match by code → sparse update (only columns present in CSV); new rows → create. All rows must pass validation. | All-or-nothing transaction. CSVImportRecord rows record per-row action + changed_fields. | 🔴 Real-time |
| BR-02-028 | BACIntegrityLedger insert | Any BAC change | Insert ledger row with old_bac, new_bac, bac_delta, bac_version_after, change_type, trigger entity ref. **DB-level UPDATE/DELETE forbidden** on this table. | 🔴 Real-time |
| BR-02-029 | M07 reads BACIntegrityLedger | M07 calls `GET /internal/v1/m02/bac-ledger?package_id=X` | Return ledger entries for package, ordered by changed_at DESC. M07 does NOT directly query M02 DB tables (per OQ-1.10). | LINK |
| BR-02-030 | Package soft-delete attempt | Check existence of active BOQ items, BOQWBSMaps, dependencies in M03/M04/M06 | Block if children exist. Force "Suspend" or "Archive" instead. | 🔴 Real-time |
| BR-02-031 | WBSNode soft-delete attempt | Check active children WBS + BOQ mappings | Block if active children. Force user to clear children first. | 🔴 Real-time |
| BR-02-032 | Project.min_wbs_depth change | PMO_DIRECTOR edits project's min depth | Validate: change does not violate existing WBS structure. Audit log entry. | 🔴 Real-time |
| BR-02-033 | Concurrent VO materialisation guard | A package already in Stale_Pending_VO state receives second Stale signal | Block. Second VO's materialisation queues until first completes (returns to Confirmed). M05 receives Pending_Queue status. | 🔴 Real-time |
| BR-02-034 | Baseline lock signal from M08 (SG-6 passed) | All WBSNode and Package within project frozen | Set is_baseline_locked=true on all WBSNode + Package. After lock: edits require VO workflow (M05) or BaselineExtension (M03). | 🔴 Real-time |
| BR-02-035 | Template lineage validation | On every PackageTemplate insert/update | Enforce: System_Default.parent_template_id IS NULL. Tenant_Standard.parent_template_id either NULL or refs System_Default. Project_Template.parent_template_id either NULL or refs Tenant_Standard. **Forbid upward references.** | 🔴 Real-time |
| BR-02-036 | BOQ Item creation via VO_Materialisation (Option B) | BR-02-004 + extra rule | New item must have boq_origin=VO_Materialisation, source_vo_id, source_materialisation_id, and pass full 5-ID chain validation. | 🔴 Real-time |
| BR-02-037 | BOQ deletion during VO materialisation (soft) | QS soft-deletes BOQ during materialisation | Allowed — reduces BAC. Captured in BACIntegrityLedger. If BAC delta variance > ₹10,000 vs approved VO cost_impact: alert PMO_DIRECTOR (signal to M05 BR-05-032). | 🔴 Real-time |
| BR-02-038 | UnitMaster soft-delete | Standard_Core: blocked. Domain_Specific: PMO_DIRECTOR allowed if no BOQ references. Custom: PROJECT_DIRECTOR allowed if no BOQ references. | Block if active references | 🔴 Real-time |

---

## BLOCK 7 — INTEGRATION POINTS

| Direction | Module | Data Exchanged | Trigger | Speed Tier |
|---|---|---|---|---|
| RECEIVES FROM | M34 | Authentication context, role, project scope, **field-level rate display permission per role** | Every API call | 🔴 Real-time |
| RECEIVES FROM | M34 | CodeMaster: Discipline, DocumentType | Form rendering | LINK |
| RECEIVES FROM | M01 | `project_id`, `current_phase` (for PHASE_ID snapshot per OQ-1.4), `project_status`, `min_wbs_depth` | On project activation + phase transitions | 🔴 Real-time |
| RECEIVES FROM | M01 | `contract_id`(s) per project | On contract create | 🔴 Real-time |
| RECEIVES FROM | M05 | `bac_integrity_status=Stale_Pending_VO` signal + `vo_id`, `affected_package_ids`, `materialisation_id`, `cost_impact_approved` | On VO approval (cost_impact > 0); BR-05-028 | 🔴 Real-time |
| RECEIVES FROM | M05 | Materialisation option (A/B/C) and scope when QS starts work | On VOBOQMaterialisation status → In_Progress | 🔴 Real-time |
| RECEIVES FROM | M08 | Baseline lock signal at SG-6 | On gate passage | 🔴 Real-time |
| RECEIVES FROM | HDI | BOQ seed data with boq_origin=HDI_Seed | One-time HDI session | 🔴 Real-time |
| SENDS TO | M03 Planning | `wbs_id`, `activity_type`, `package_id` per WBS node | On WBS creation + baseline lock | 🔴 Real-time |
| SENDS TO | M03 Planning | `procurement_schedule_id` linkage on packages | On package creation | 🔴 Real-time |
| SENDS TO | M04 Execution | `wbs_id` list (for progress capture grain) | On WBS creation | 🔴 Real-time |
| SENDS TO | M06 Financial | `boq_id`, `wbs_id`, `package_id`, `actual_rate`, `actual_amount`, **`bac_version`** | On every BOQ save | 🔴 Real-time |
| SENDS TO | M07 EVM Engine | `package_id`, `bac_amount`, **`bac_integrity_status`**, **`bac_version`** | On BAC recalc + integrity status change | 🔴 Real-time |
| SENDS TO | M07 EVM Engine | BACIntegrityLedger entries (read via API: `GET /internal/v1/m02/bac-ledger`) | On M07 query | LINK |
| SENDS TO | M05 Risk & Change | Materialisation completion: `cost_impact_materialised`, `new_bac_snapshot`, `affected_boq_ids`, `bac_version` | On BR-02-014 (materialisation complete) | 🔴 Real-time |
| SENDS TO | M08 Gate Control | WBS + Package frozen state at SG-6 | On baseline lock | 🔴 Real-time |
| SENDS TO | M09 Compliance | Package list per project for compliance scope mapping | On package creation | 🔴 Real-time |
| SENDS TO | M10 EPCC Command | Package count, BAC totals per project | On any structural change | 🟡 2-4hr |
| SENDS TO | M11 Action Register | Decision queue items (BAC integrity issues) | When triggered | 🔴 Real-time |
| SENDS TO | M14 QS Measurement Book | BOQ master for measurement reference | On BOQ create/edit | 🔴 Real-time |

---

## BLOCK 8 — GOVERNANCE AND AUDIT

### 8a. Logged Events

| Action | Logged | Detail | Visible To | Retention |
|---|---|---|---|---|
| WBS create | Yes | All fields | PMO_DIR, PROJECT_DIR | Project lifetime |
| WBS reorder | Yes | from/to positions, code reassignments | PMO_DIR, PROJECT_DIR | Project lifetime |
| WBS soft-delete | Yes | Reason (or system-blocked) | PMO_DIR, PROJECT_DIR | Permanent |
| Package create | Yes | All fields, applied template if any | PMO_DIR, FINANCE_LEAD | Permanent |
| Package edit | Yes | from/to per field | PMO_DIR, FINANCE_LEAD | Project lifetime |
| BOQ create | Yes | All fields | PMO_DIR, PROJECT_DIR, QS_MANAGER | Project lifetime |
| BOQ rate change | Yes | from/to (full transparency to logged audience) | PMO_DIR, FINANCE_LEAD | Permanent |
| BOQ quantity change | Yes | from/to, reason if VO-driven | PMO_DIR, QS_MANAGER, FINANCE_LEAD | Permanent |
| BOQ-WBS mapping change | Yes | Old + new mapping | PMO_DIR, PROJECT_DIR | Project lifetime |
| Field-level rate access (audit-relevant role views actual rate) | Yes | actor_user, target_boq, formula_applied | PMO_DIR | 7 years |
| Standard_Core unit edit | Yes | Fully privileged event (forwarded to M34 SystemAuditLog) | SYSTEM_ADMIN | Permanent |
| Domain_Specific unit edit | Yes | from/to | PMO_DIR | Permanent |
| Custom unit edit | Yes | from/to | PROJECT_DIR | Project lifetime |
| Tenant_Standard template create/edit | Yes | All fields, version delta | PMO_DIR | Permanent |
| Tenant_Standard pmo_validated set true | Yes | Validator user, timestamp | PMO_DIR | Permanent |
| Tenant_Standard version lock | Yes | Locker, version | PMO_DIR | Permanent |
| Template applied to project | Yes | template_id, version_id, target package | PMO_DIR, PROJECT_DIR | Permanent |
| CSV import session | Yes | session_id, mode, file size, row count, commit/rollback status | PMO_DIR + initiator | Permanent |
| BACIntegrityLedger entry | Yes | **Append-only** by design (all BAC changes captured) | PMO_DIR, FINANCE_LEAD | **Permanent (forensic)** |
| IDGovernanceLog entry | Yes | 5-ID chain validation result per BOQ | PMO_DIR, audit reviewers | Permanent |
| Baseline lock at SG-6 | Yes | Signal source (M08), locked WBS count, locked Package count | PMO_DIR | Permanent |

### 8b. Immutability Rules

- **`BACIntegrityLedger`** — DB-level UPDATE and DELETE forbidden via `REVOKE`. INSERT-only via app role.
- **`IDGovernanceLog`** — Append-only. No updates.
- **`PackageTemplateVersion`** with `lock_state=Locked` — DB-level CHECK constraint or app-level guard prevents updates to version + child PackageTemplateBOQ rows.
- **`BOQItem.phase_at_creation`** — Snapshot field; immutable post-creation.
- **`BOQItem.boq_origin`** — Immutable post-creation (audit integrity).
- **`is_baseline_locked=true`** WBSNode and Package — Edits blocked; force VO (M05) or BaselineExtension (M03) workflow.

### 8c. Privacy

- BOQ `actual_rate` is sensitive financial data — never exposed in non-Finance/non-PMO roles' API responses
- API serialiser enforces field-level redaction; never depend on UI-only restriction
- Spike formulas applied at serialiser, not at DB or business-logic layer (defence-in-depth)

---

## BLOCK 9 — EXPLICIT EXCLUSIONS

```
This module does NOT:
─────────────────────────────────────────────────────────────────────
[ ] Schedule planning, dates, baselines, S-curves, PV         → M03
[ ] Actual cost transactions, RA bills, sub-contracts          → M06
[ ] Source CPWD DSR or market rates                            → External data; M06 stores actuals
[ ] Capture progress, NCRs, DLP defects                        → M04
[ ] Calculate EVM (CPI/SPI/EAC/ETC/VAC/TCPI)                  → M07
[ ] Trigger or approve VO workflows                            → M05
[ ] Suspend EAC during materialisation                         → M07
[ ] Approve stage gates                                        → M08
[ ] Track regulatory compliance                                → M09
[ ] Store project documents                                    → M12 + MinIO
[ ] Manage QS measurement book entries                         → M14
[ ] Run tendering / award workflow                             → M29
[ ] Integrate with BIM models                                  → PF02 (Phase 4)
[ ] Convert units between systems (m↔ft, kg↔ton)             → Out of v1.0 scope
[ ] Authenticate users / manage roles                          → M34
[ ] Promote Project_Template upward to Tenant_Standard         → Forbidden by BR-02-035 (copy-down only)
```

---

## BLOCK 10 — OPEN QUESTIONS

**All questions resolved. Zero open questions.**

| # | Question | Resolution |
|---|---|---|
| 1 | WBS minimum depth: system-wide vs per-project? | **Per-project, sector-driven default (OQ-1.1=B).** `Project.min_wbs_depth` field (M01 v1.1 minor bump). Healthcare default = 4. PMO override with reason ≥ 100 chars. |
| 2 | `bac_integrity_status` ENUM extensibility? | **Locked at 2 values (OQ-1.2=A).** `Confirmed / Stale_Pending_VO`. New states only when trigger formally specified. |
| 3 | Spike formula naming? | **Keep legacy (OQ-1.3=A).** `Loaded / Indexed / Flat_Redacted`. Industry jargon. |
| 4 | 5-ID chain `PHASE_ID` interpretation? | **Snapshot at BOQ creation (OQ-1.4=B).** `BOQItem.phase_at_creation` denormalised + immutable. |
| 5 | Package template promotion? | **Three-tier copy-down model (OQ-1.5=C refined).** System_Default (Anthropic) → Tenant_Standard (PMO validates) → Project_Template (per-project). **No upward promotion.** |
| 6 | CSV `Create_And_Update` conflict resolution? | **Sparse update (OQ-1.6=B).** Only CSV-present columns updated. Empty cells preserve existing values. |
| 7 | `boq_origin` ENUM values? | **5 values incl. HDI_Seed (OQ-1.7=C).** `Manual / CSV_Import / VO_Materialisation / Template_Applied / HDI_Seed`. |
| 8 | WBS code format? | **Auto-generated dotted notation (OQ-1.8=A).** UUIDs for internal refs; codes for display. Drag-reorder reassigns codes. |
| 9 | Unit conversion in v1.0? | **No conversion (OQ-1.9=A).** Metric-only. Future-proof field `unit_system`. |
| 10 | `BACIntegrityLedger` ownership? | **M02 owns; M07 reads via internal API (OQ-1.10=A).** Single-owner rule per F-005. Standards Memory v1.0 will remove "joint" framing. |
| 11 | Three-tier template promotion direction? | **Copy-down only (BR-02-035).** Tenant_Standard cannot reference Project_Template. Project_Template cannot promote to Tenant_Standard. |
| 12 | OQ-2.1 UUID PKs | **Yes, per X8 §6.** |
| 13 | OQ-2.2 Reserved fields | **Per X8 §6.** Append-only entities exempt. |
| 14 | OQ-2.4 Package code format | **`PKG-{seq}` auto with PMO override.** |
| 15 | OQ-2.5 BOQ code format | **`{PKG_CODE}-{seq}` auto.** |
| 16 | OQ-2.7 CSV file size limit | **20 MB / 50,000 rows.** |
| 17 | OQ-2.9 Audit log retention | **Permanent for BAC ledger; 7 years routine.** |
| 18 | OQ-2.11 Field-level rate enforcement | **API serialiser layer (not UI-only).** Defence-in-depth. |

---

## APPENDIX A — Migration Plan

```
Migration: 20260503_0020_m02_initial_schema.py
  - Creates: WBSNode, Package, BOQItem, BOQWBSMap, UnitMaster,
    PackageTemplate, PackageTemplateVersion, PackageTemplateBOQ,
    BACIntegrityLedger, IDGovernanceLog, CSVImportSession, CSVImportRecord
  - Enforces UPDATE/DELETE revocation on bac_integrity_ledger
  - Composite uniqueness constraints on all entity codes within scope
  - FK constraints to M01 + M34

Migration: 20260503_0021_m02_seed_unitmaster_standard_core.py
  - Seeds Standard_Core UnitMaster:
    - Mass: kg, g, mt, ton (metric)
    - Volume: m3, l, ml
    - Length: m, cm, mm
    - Area: m2, sqm
    - Count: nos, set, lot, doz
    - LumpSum: LS
    - Currency: INR (denominator)

Migration: 20260503_0022_m02_seed_system_templates.py
  - Seeds System_Default templates for KDMC pilot baseline:
    - Hospital_DBOT_Civil
    - Hospital_DBOT_MEP
    - Hospital_DBOT_HVAC
    - Hospital_DBOT_Medical_Equipment
    - Hospital_DBOT_Indirect
  - Each with v1 PackageTemplateVersion + sample PackageTemplateBOQ rows
```

---

## APPENDIX B — API Surface (sketch)

```
WBS:
  GET    /api/v1/projects/{p_id}/wbs                     ?depth&parent_id (tree or flat)
  POST   /api/v1/projects/{p_id}/wbs                     { name, parent_id, activity_type }
  PATCH  /api/v1/wbs/{wbs_id}
  DELETE /api/v1/wbs/{wbs_id}                           (soft delete; BR-02-031)
  POST   /api/v1/wbs/{wbs_id}/reorder                   { new_position }

Packages:
  GET    /api/v1/projects/{p_id}/packages
  POST   /api/v1/projects/{p_id}/packages                { name, type, contract_id }
  POST   /api/v1/projects/{p_id}/packages/from-template  { template_version_id }
  PATCH  /api/v1/packages/{pkg_id}
  DELETE /api/v1/packages/{pkg_id}                      (soft; BR-02-030)
  GET    /api/v1/packages/{pkg_id}/bac-ledger           (M07-internal also)

BOQ Items:
  GET    /api/v1/packages/{pkg_id}/boqs
  POST   /api/v1/packages/{pkg_id}/boqs                  { description, unit_master_id, quantity, actual_rate }
  PATCH  /api/v1/boqs/{boq_id}
  DELETE /api/v1/boqs/{boq_id}

BOQ-WBS Mapping:
  POST   /api/v1/boqs/{boq_id}/wbs-map                   { wbs_id, is_primary_wbs, allocation_pct? }
  DELETE /api/v1/boqs/{boq_id}/wbs-map/{map_id}

Unit Master:
  GET    /api/v1/units                                   ?tier=Standard_Core|Domain_Specific|Custom
  POST   /api/v1/units                                   { tier, unit_code, label, category }
  PATCH  /api/v1/units/{unit_id}

Package Templates:
  GET    /api/v1/templates                               ?tier=System_Default|Tenant_Standard|Project_Template
  POST   /api/v1/templates/copy-from/{source_id}         (PMO_DIR copy down)
  POST   /api/v1/templates/{tpl_id}/versions             (new version)
  POST   /api/v1/templates/versions/{ver_id}/validate    (PMO sets pmo_validated=true)
  POST   /api/v1/templates/versions/{ver_id}/lock        (PMO locks version)

CSV Import:
  POST   /api/v1/projects/{p_id}/csv-import              { target, mode } → returns session_id
  POST   /api/v1/csv-import/{session_id}/upload          (multipart file)
  GET    /api/v1/csv-import/{session_id}/preview         (validation report)
  POST   /api/v1/csv-import/{session_id}/commit
  POST   /api/v1/csv-import/{session_id}/rollback

Internal (M07 / M06 only):
  GET    /internal/v1/m02/bac-ledger                     ?package_id  (per OQ-1.10)
  GET    /internal/v1/m02/packages/{pkg_id}/bac-snapshot
```

---

## APPENDIX C — KDMC Reference Data Migration

Existing KDMC BOQ data (~12,000 line items in legacy workbook) imports as:

| Field | Migration source |
|---|---|
| `boq_origin` | `HDI_Seed` |
| `phase_at_creation` | Project's current_phase at HDI session time (snapshot) |
| `actual_rate` | From workbook BOQ sheet (PMO_DIRECTOR validates) |
| `quantity` | From workbook |
| `unit_master_id` | Resolved from workbook unit string against Standard_Core |
| `package_id` | Resolved against KDMC Package master (created prior to HDI) |
| Template lineage | Not applicable (HDI_Seed origin overrides Template_Applied) |

---

*v1.0 — Spec locked. Zero open questions. Ready for Round 11 (Wireframes).*
