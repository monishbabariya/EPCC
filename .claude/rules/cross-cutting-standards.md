# Cross-Cutting Standards — X1–X9

> **Purpose:** Index and rules for the X-series living documents. X8 (ENUMs) and X9 (Visualisation) are the most active. All others are roadmap.

---

## X-Series Map

| Doc | Topic | Status | Source of Truth |
|---|---|---|---|
| X1 | RBAC Matrix (consolidated role × action) | Roadmap | M34 spec until built |
| X2 | Decision Queue Catalogue | Roadmap | Per-module spec until built |
| X3 | Audit Event Catalogue | Roadmap | Per-module spec until built |
| X4 | API Surface Index | Roadmap | Per-module spec until built |
| X5 | Speed Tier Inventory | Roadmap | — |
| X6 | Integration Point Map | Roadmap | Per-module §7 until built |
| X7 | Standards Memory v1.0 | Roadmap | This rules folder until built |
| **X8** | **Glossary ENUMs** | **LIVING (current v0.8 — R34 lock)** | `SystemAdmin/Cross-link files/X8_GlossaryENUMs_v0_8.md` |
| **X9** | **Visualisation Standards** | **LIVING (current v0.5 — R34 in-place patch; filename retains v0_4)** | `SystemAdmin/Cross-link files/X9_VisualisationStandards_Spec_v0_4.md` _(content version v0.5; filename retained per in-place patch convention)_ |

---

## X8 — ENUM Discipline

### Locked ENUMs by Module (current v0.8)

| ENUM | Owner | Locked In |
|---|---|---|
| Severity (Critical/High/Medium/Low/Info) | System | v0.1 |
| RAGStatus (Green/Amber/Red) | System | v0.1 |
| HealthBand | System | v0.1 |
| SpeedTier | System | v0.1 |
| RecordStatus (Draft/Active/Suspended/Archived/Deleted) | System | v0.1 |
| LockState | System | v0.1 |
| UserStatus | M34 | v0.1 |
| ProjectStatus | M01 | v0.2 |
| Phase (10-value Pre_Investment → Closed) | M01 | v0.2 |
| StageGate (SG_0 to SG_11) | System | v0.1 |
| GatePassageOutcome | System | v0.1 |
| DataSource, Currency, BillableState | System | v0.1 |
| DeliveryModel (no Hybrid) | M01 | v0.2 |
| SectorTopLevel (5 values) | M01 | v0.2 |
| PartyType, PartyRole, ContractRole, ContractType | M01 | v0.2 |
| ScenarioActive (Base/Best/Worst) | M01 | v0.2 |
| KPIName, KPIDirection | M01 | v0.2 |
| Region | M01 | v0.2 |
| BACIntegrityStatus, BOQOrigin, BOQRateSpikeFormula | M02 | v0.3 |
| PackageTemplateTier | M02 | v0.3 |
| BACChangeType, UnitTier, UnitCategory, UnitSystem, PackageType | M02 | v0.3 |
| ChainValidationStatus, CSVImportMode, CSVImportTarget, CSVImportRecordAction | M02 | v0.3 |
| (M03 ENUMs — 12 new) | M03 | v0.4 |
| ProgressMeasurementMethod (Units/Steps/Milestone/Subjective_Estimate) | M04 | v0.5 |
| ProgressApprovalStatus (Draft/Submitted/Approved/Rejected) | M04 | v0.5 |
| EVConfidence (High/Low/Fallback/Derived — Fallback/Derived M07-written) | M04 | v0.5 |
| NCRStatus (7-state lifecycle) | M04 | v0.5 |
| NCRRootCauseCategory (Workmanship/Material/Design/Procedure/Other) | M04 | v0.5 |
| MaterialReceiptStatus, MaterialQCStatus, MaterialQCDecision | M04 | v0.5 |
| CostLedgerEntryState (4-state Budgeted→Committed→Accrued→Paid) | M06 | v0.6 |
| PurchaseOrderStatus, RABillStatus, RABillTriggerSource | M06 | v0.6 |
| GRNMatchStatus | M06 | v0.6 |
| VendorInvoiceStatus, InvoiceMatchMode, InvoiceMatchStatus | M06 | v0.6 |
| PaymentEvidenceStatus | M06 | v0.6 |
| RetentionReleaseType, RetentionReleaseStatus | M06 | v0.6 |
| ExchangeRateTier (RBI_Reference / Bank_Transaction) | M06 | v0.6 |
| BGType (BGStub-pattern; migrates to M23 in Phase 2) | M06 | v0.6 |
| StageGate description refresh (SG_9 + SG_11; sequence unchanged) | System | v0.6 (refreshed) |
| RiskCategory (8 values: Strategic / Financial / Operational / Regulatory / Clinical / Market / ESG / Force_Majeure) | M05 | v0.7 |
| RiskRAGStatus (Green 1-4 / Amber 5-12 / Red 13-25; derived) | M05 | v0.7 |
| RiskStatus (Draft / Active / Mitigating / Closed / Reopened / Withdrawn) | M05 | v0.7 |
| RiskResponseStrategy (ARTA: Avoid / Reduce / Transfer / Accept) | M05 | v0.7 |
| ChangeItemType, ChangeItemStatus | M05 | v0.7 |
| VariationOrderType, VOCause | M05 | v0.7 |
| VOStatus (7-state: Draft / Assessed / Submitted / Approved / Materialised / Closed / Rejected) | M05 | v0.7 |
| VOApprovalLevel (Single / Dual), VOMaterialisationStatus | M05 | v0.7 |
| EOTClaimBasis, EOTStatus (5-state: Claim_Raised / Under_Assessment / Granted / Rejected / Withdrawn) | M05 | v0.7 |
| EWNStatus (Active / Closed / Lapsed) | M05 | v0.7 |
| ContingencyDrawdownStatus (Requested / Approved / Rejected / Reversed) | M05 | v0.7 |
| LDStatus (Not_Started / Accruing / Cap_Reached / Waived) | M05 | v0.7 |
| CorrespondenceDirection (Incoming / Outgoing) | M13 | v0.8 |
| CorrespondenceType (9 values incl. Site_Instruction, Notice, RFI_Reference, Transmittal_Reference) | M13 | v0.8 |
| ContractualWeight (Non_Contractual / Contractual / Formal_Notice / Without_Prejudice) | M13 | v0.8 |
| CorrespondenceResponseStatus, SiteInstructionComplianceStatus | M13 | v0.8 |
| MeetingType (8 values), MinutesStatus (Draft / Circulated / Approved / Disputed) | M13 | v0.8 |
| MinutesEntryType (7 values incl. Risk_Noted promotable to M05) | M13 | v0.8 |
| ActionItemSource, ActionItemStatus | M13 | v0.8 |
| RFIStatus (Open / Responded / Closed / Overdue) | M13 | v0.8 |
| TransmittalPurpose, TransmittalStatus | M13 | v0.8 |
| AcknowledgementMethod (System_Click / Email_Reply / Verbal_Recorded / Physical_Signature) | M13 | v0.8 |

### Anti-Drift Rules (LOCKED)

- Every spec references X8 — never redefines ENUMs inline
- New ENUM values require X8 version bump + change log entry
- Deprecated ENUMs marked DEPRECATED (never deleted)

---

## X9 — Visualisation (current v0.4)

**Decision-First Principle (FOUNDATIONAL):** every chart answers ONE decision in ONE sentence.

### Locked library choices

- **Primary library:** Recharts (OQ-1.1)
- **Gantt:** frappe-gantt (OQ-1.2)
- **Network:** react-flow (OQ-1.3)
- **Versions pinned:** Recharts 3.x, frappe-gantt 0.7.x, react-flow 12.x

### Locked design rules

- Rate display at API serialiser, not client (OQ-1.5)
- Dual-encode + opt-in alt palette (OQ-1.6)
- PNG + CSV + URL exports (OQ-1.7)
- No real-time WebSocket in v1.0 (OQ-1.8)
- Hybrid drill-down — zoom in-place; entity drill = new view (OQ-1.9)
- Tabular fallback for all charts (OQ-1.10)

### Pipeline Funnel as flagship pattern

9 module implementations: **M06 Capital Funnel (1st named flagship instance — X9 §9.5.1 v0.4 annotation)**, M04 NCR, M05 Risk, M05 VO, M09 Compliance, M11 Action, M15 Defect, **M13 Notice SLA Breach (X9 v0.5 §9.5.7)**, HDI Import.

### Anti-Patterns Forbidden

3D charts, radar, dual-axis, gauge, pie > 6 slices.

### Role-Based Default Views (LOCKED — Level 1)

No personalisation in v1.0. No tenant override of role defaults (system-wide consistency).

---

## Spike Formula Role Mapping (M02 BR-02-008)

| Role | Formula | Display |
|---|---|---|
| SYSTEM_ADMIN, PMO_DIRECTOR, FINANCE_LEAD, EXTERNAL_AUDITOR | None | Actual rate |
| PORTFOLIO_MANAGER, PROJECT_DIRECTOR, PROCUREMENT_OFFICER, COMPLIANCE_MANAGER | Loaded | × 1.15 (default) |
| PLANNING_ENGINEER, QS_MANAGER | Indexed | × 1.08 (default) |
| SITE_MANAGER, READ_ONLY | Flat_Redacted | `[RESTRICTED]` |

---

## 17 Canonical Roles (M34)

> Authoritative source: `SystemAdmin/M34_SystemAdminRBAC_Spec_v1_0.md` Block 3 "Locked Role Taxonomy v1.0". Names below match the M34 ENUMs exactly.

**Internal (13):** `SYSTEM_ADMIN`, `PMO_DIRECTOR`, `PORTFOLIO_MANAGER`, `PROJECT_DIRECTOR`, `PLANNING_ENGINEER`, `QS_MANAGER`, `FINANCE_LEAD`, `PROCUREMENT_OFFICER`, `SITE_MANAGER`, `COMPLIANCE_MANAGER`, `ANALYST`, `READ_ONLY`, `EXTERNAL_AUDITOR`.

**External (4):** `CLIENT_VIEWER`, `LENDER_VIEWER`, `NABH_ASSESSOR`, `CONTRACTOR_LIMITED` (all Phase 2 — gated by PF03 ExternalPartyPortal).

**MFA-required (5):** `SYSTEM_ADMIN`, `PMO_DIRECTOR`, `PORTFOLIO_MANAGER`, `FINANCE_LEAD`, `EXTERNAL_AUDITOR`.

---

## Patch Notes — 2026-05-04 (Round 37 Pre-Build Audit)

- **H9 / H10** — X8 status + source-of-truth path bumped to v0.8
- **H11** — M05 ENUMs (16, §3.73-§3.88, v0.7) + M13 ENUMs (14, §3.89-§3.102, v0.8) added to Locked ENUMs table
- **H12** — X9 status bumped to v0.5 (R34 in-place patch; filename retained v0_4)
- **M1** — Pipeline Funnel module count updated 8 → 9 (M13 Notice SLA Breach Funnel added)
