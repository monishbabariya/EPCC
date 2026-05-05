# X8 — Glossary & ENUMs
## Cross-Cutting Document v0.8 (LIVING)
**Owner:** PMO Director / System Architect
**Created:** 2026-05-03 (v0.1) | **Updated:** 2026-05-04 (v0.8)
**Status:** Living — appended on every module spec lock
**Source modules locked into this version:** M34, M01, M02, M03, M04, M05, M06, **M13** (NEW v0.8)
**Folder:** SystemAdmin/Cross-link files/ (per Round 18 audit canonical placement)
**Version bump rationale:** Minor version bump (v0.7 → v0.8) — adds 14 new ENUMs from M13 lock + 29 new audit event types (§4.12 extension) + 8 new Decision Queue trigger types (new §4.18 M13_DecisionQueueTriggerType ENUM). Substantive cascade per spec-protocol.md §Cascade-vs-Re-issue rule. New filename per minor-version-bump convention; v0.7 content preserved historically.

**M05+M13 batch X8 audit pass (Round 34 task Deliverable B1):** All M05 Spec v1.0 (R33) ENUM references §3.73-§3.88 verified present in v0.7; carried forward intact. All M05 Spec audit events (33) verified in v0.7 §4.12; carried forward intact. All M05 Spec DQ triggers (10) verified in v0.7 §4.17 (M05_DecisionQueueTriggerType); carried forward intact. **0 audit gaps found.**

---

## IN-PLACE PATCH CHANGE LOG

(no in-place patches yet on v0.8; reserved for future letter-suffix patches)

---

## CHANGES IN v0.8

| # | Change | Driven By |
|---|---|---|
| 1 | Added `CorrespondenceDirection` ENUM (§3.89) — 2 values | M13 Spec Block 3b.1 (Correspondence.direction) per OQ-1.3 |
| 2 | Added `CorrespondenceType` ENUM (§3.90) — 9 values | M13 Spec Block 3b.1 (Correspondence.correspondence_type) |
| 3 | Added `ContractualWeight` ENUM (§3.91) — 4 values | M13 Spec Block 3b.1 (Correspondence.contractual_weight) |
| 4 | Added `CorrespondenceResponseStatus` ENUM (§3.92) — 5 values | M13 Spec Block 3b.1 (Correspondence.response_status) |
| 5 | Added `SiteInstructionComplianceStatus` ENUM (§3.93) — 5 values | M13 Spec Block 3b.1 (Correspondence.compliance_status for Site_Instruction type) |
| 6 | Added `MeetingType` ENUM (§3.94) — 8 values | M13 Spec Block 3b.5 (MeetingRegister.meeting_type) |
| 7 | Added `MinutesStatus` ENUM (§3.95) — 4 values | M13 Spec Block 3b.5 (MeetingRegister.minutes_status) |
| 8 | Added `MinutesEntryType` ENUM (§3.96) — 7 values | M13 Spec Block 3b.6 (MinutesEntry.entry_type) per OQ-1.4 |
| 9 | Added `ActionItemSource` ENUM (§3.97) — 5 values | M13 Spec Block 3b.8 (ActionItem.source) |
| 10 | Added `ActionItemStatus` ENUM (§3.98) — 6 values | M13 Spec Block 3b.8 (ActionItem.status) |
| 11 | Added `RFIStatus` ENUM (§3.99) — 4 values | M13 Spec Block 3b.9 (RFI.status) |
| 12 | Added `TransmittalPurpose` ENUM (§3.100) — 6 values | M13 Spec Block 3b.11 (Transmittal.transmittal_purpose) |
| 13 | Added `TransmittalStatus` ENUM (§3.101) — 4 values | M13 Spec Block 3b.11 (Transmittal.status) |
| 14 | Added `AcknowledgementMethod` ENUM (§3.102) — 4 values | M13 Spec Block 3b.12 (DistributionList.acknowledgement_method) |
| 15 | §4.12 `AuditEventType` extended with 29 new M13-owned event types (Block 8b of M13 Spec) | M13 Spec Block 8b |
| 16 | §4.18 NEW: `M13_DecisionQueueTriggerType` (M13-owned) — 8 trigger types (Block 8c of M13 Spec) | M13 Spec Block 8c |
| 17 | §6 Reserved Fields: 5 M13 append-only ledger exemptions added | M13 Spec Block 3a + OQ-2.2 |

---

## SECTIONS UNCHANGED FROM v0.7

§1 (Naming Conventions), §2 (Versioning Discipline), §3.1 — §3.88 (existing system + M01-M06+M05 ENUMs), §4.1 — §4.11 (M34-owned base), §4.13-§4.17 (existing per-module DQ ENUMs), §5 (ENUM Reference Patterns), §7 (Glossary).

For full content of unchanged sections, refer to `X8_GlossaryENUMs_v0_7.md` (preserved historically).

---

## §3 ENUM CATALOGUE (M13 NEW v0.8 — additive)

### 3.1 — 3.88 *Unchanged from v0.7.*

[All M34 + M01 + M02 + M03 + M04 + M06 + M05 ENUMs — see `X8_GlossaryENUMs_v0_7.md`. Last v0.7 ENUM: §3.88 `LDStatus` (M05-owned).]

---

### 3.89 `CorrespondenceDirection` (M13-owned) — **NEW v0.8**

Per M13 Brief OQ-1.3=A (single Correspondence entity with direction ENUM) + Spec Block 3b.1.

```
ENUM CorrespondenceDirection {
  Incoming                  // From external party (client, contractor, regulator) to internal
  Outgoing                  // From internal to external party
}
```

**Anti-drift note:** Single ENUM avoids splitting Correspondence into Incoming/Outgoing tables (would force duplicate logic). UI filter splits views by direction; same backend entity.

---

### 3.90 `CorrespondenceType` (M13-owned) — **NEW v0.8**

Per M13 Spec Block 3b.1 `Correspondence.correspondence_type`. Site Instructions modelled as a CorrespondenceType (not a separate entity per OQ-1.3 single-entity lock).

```
ENUM CorrespondenceType {
  Letter                    // Formal letter (printed/scanned)
  Notice                    // Contractual notice with response obligation (drives NoticeTracker view)
  Instruction               // General instruction (not site-specific)
  RFI_Reference             // Reference to RFI entity (RFI itself is separate entity)
  Email_Formal              // Email with contractual weight (not casual chat)
  Site_Instruction          // Formal instruction on site (compliance_deadline + compliance_status fields populated)
  Regulatory                // From or to regulatory authority (M09 cross-link)
  Legal                     // Legal correspondence (M19 Phase 2 absorbs into claims documentation)
  Transmittal_Reference     // Reference to Transmittal entity (Transmittal itself is separate entity)
}
```

---

### 3.91 `ContractualWeight` (M13-owned) — **NEW v0.8**

Per M13 Spec Block 3b.1 `Correspondence.contractual_weight`. Drives NoticeTracker SLA logic (only `Formal_Notice` and `Contractual` weights trigger BR-13-006/007 SLA sweep).

```
ENUM ContractualWeight {
  Non_Contractual           // Information only; no SLA tracking
  Contractual               // Carries contractual weight; SLA tracked
  Formal_Notice             // Highest contractual weight; strict SLA enforcement; legal-evidence
  Without_Prejudice         // Marked "without prejudice"; preserves legal flexibility
}
```

---

### 3.92 `CorrespondenceResponseStatus` (M13-owned) — **NEW v0.8**

Per M13 Spec Block 3b.1 `Correspondence.response_status`.

```
ENUM CorrespondenceResponseStatus {
  Not_Required              // response_required = false
  Pending                   // Awaiting response within SLA window
  Responded                 // Response received (responded_via_correspondence_id populated)
  Overdue                   // Past response_due_date without response (BR-13-007)
  Escalated                 // Manually escalated by PMO_DIRECTOR
}
```

---

### 3.93 `SiteInstructionComplianceStatus` (M13-owned) — **NEW v0.8**

Per M13 Spec Block 3b.1. Applies only when `correspondence_type = Site_Instruction`.

```
ENUM SiteInstructionComplianceStatus {
  Pending                   // Just issued; awaiting contractor response
  In_Progress               // Contractor has acknowledged; remediation underway
  Complied                  // Contractor confirmed compliance within deadline
  Non_Complied              // Past compliance_deadline without compliance (BR-13-022 emits NCR-basis assessment to M05)
  Disputed                  // Contractor disputes the instruction (escalates to PMO_DIRECTOR review)
}
```

---

### 3.94 `MeetingType` (M13-owned) — **NEW v0.8**

Per M13 Spec Block 3b.5 `MeetingRegister.meeting_type`.

```
ENUM MeetingType {
  Kickoff                   // Project kickoff meeting (contractually-required at SG-5)
  Site_Progress             // Regular site progress meeting (typically weekly)
  Technical                 // Technical review meeting (design / engineering / specifications)
  Contractual               // Contract administration meeting (commercial deliberations)
  Subcontractor             // Subcontractor coordination meeting
  Regulatory                // Meeting with regulatory authority (NABH, AERB, PCB, etc.)
  Board                     // Board / steering committee meeting (portfolio-level)
  Closeout                  // Project closeout meeting (typically at SG-11)
}
```

---

### 3.95 `MinutesStatus` (M13-owned) — **NEW v0.8**

Per M13 Spec Block 3b.5 `MeetingRegister.minutes_status`. State machine.

```
ENUM MinutesStatus {
  Draft                     // Just drafted by minutes_drafted_by_user_id
  Circulated                // Circulated to attendees for review
  Approved                  // Approved by PMO_DIRECTOR or PROJECT_DIRECTOR (BR-13-013)
  Disputed                  // Disputed by an attendee; minutes_dispute_note required (BR-13-015)
}
```

**State transitions:** `Draft → Circulated → Approved` (happy path); `Circulated → Disputed → Approved` (after PMO override resolution).

---

### 3.96 `MinutesEntryType` (M13-owned) — **NEW v0.8**

Per M13 Brief OQ-1.4=B (structured line-items lock) + Spec Block 3b.6.

```
ENUM MinutesEntryType {
  Agenda                    // Pre-meeting agenda item (recorded in minutes for completeness)
  Decision                  // Decision made in meeting
  Action                    // Action item assigned (auto-creates ActionItem row per BR-13-014)
  Discussion                // Discussion topic (no decision/action)
  Risk_Noted                // Risk identified; may be promoted to M05.Risk via PROMOTE_RISK_NOTED_TO_M05 (BR-13-019, one-way)
  Information               // Information shared (no decision required)
  Question                  // Question raised (may flow to RFI as separate entity)
}
```

---

### 3.97 `ActionItemSource` (M13-owned) — **NEW v0.8**

Per M13 Spec Block 3b.8 `ActionItem.source`. Drives source FK population pattern.

```
ENUM ActionItemSource {
  Meeting                   // From MinutesEntry where entry_type=Action (auto-created per BR-13-014); source_meeting_id + source_minutes_entry_id populated
  Site_Instruction          // From Correspondence where correspondence_type=Site_Instruction; source_correspondence_id populated
  RFI                       // From RFI requiring follow-up; source_rfi_id populated
  Correspondence            // From general Correspondence requiring action; source_correspondence_id populated
  Manual                    // Standalone (no source entity)
}
```

---

### 3.98 `ActionItemStatus` (M13-owned) — **NEW v0.8**

Per M13 Spec Block 3b.8 `ActionItem.status`.

```
ENUM ActionItemStatus {
  Open                      // Just created; not yet started
  In_Progress               // Owner has acknowledged; work underway
  Completed                 // Owner marks complete; closed_at set
  Overdue                   // Past due_date without status=Completed (BR-13-016 sweep sets)
  Cancelled                 // Cancelled (closure_note ≥ 50 chars required)
  Deferred                  // Deferred to later (closure_note ≥ 50 chars required; new due_date may be set on reactivation)
}
```

---

### 3.99 `RFIStatus` (M13-owned) — **NEW v0.8**

Per M13 Spec Block 3b.9 `RFI.status`. State machine.

```
ENUM RFIStatus {
  Open                      // Just raised; awaiting response
  Responded                 // Response received (response_text + responded_by_user_id + responded_at populated per BR-13-019)
  Closed                    // Final state (PMO_DIRECTOR or PROJECT_DIRECTOR closes after acceptance)
  Overdue                   // Past response_due_date without response (BR-13-020 sweep sets)
}
```

**Reopen rule:** Closed → Open requires PMO_DIRECTOR per BR-13-021.

---

### 3.100 `TransmittalPurpose` (M13-owned) — **NEW v0.8**

Per M13 Spec Block 3b.11 `Transmittal.transmittal_purpose`.

```
ENUM TransmittalPurpose {
  Drawing_Issue             // Issuing drawings (initial release or revision)
  Specification_Update      // Specification document update
  BOQ_Revision              // BOQ document revision (typically post-VO materialisation)
  Submittal                 // Submittal to client/designer for approval (M27 DesignControl future)
  Information               // Transmittal of information-only documents
  Approval_Request          // Transmittal requesting formal approval
}
```

---

### 3.101 `TransmittalStatus` (M13-owned) — **NEW v0.8**

Per M13 Spec Block 3b.11 `Transmittal.status`.

```
ENUM TransmittalStatus {
  Sent                      // Just sent; awaiting recipient acknowledgement
  Acknowledged_Partial      // Some recipients acknowledged (per DistributionList rows)
  Acknowledged_Full         // All recipients acknowledged
  Closed                    // Final state (closed_at set)
}
```

---

### 3.102 `AcknowledgementMethod` (M13-owned) — **NEW v0.8**

Per M13 Spec Block 3b.12 `DistributionList.acknowledgement_method`.

```
ENUM AcknowledgementMethod {
  System_Click              // Recipient clicked Acknowledge in the system UI (strongest evidence)
  Email_Reply               // Recipient replied via email (parsed/captured)
  Verbal_Recorded           // Verbal acknowledgement recorded by sender (with audit timestamp)
  Physical_Signature        // Physical signature captured (paper acknowledgement; document_id FK to scanned copy)
}
```

---

## §4 — M34-OWNED ENUMs (extended in v0.8)

[§4.1 through §4.11 unchanged from v0.6a — see prior versions.]

### §4.12 `AuditEventType` — extended in v0.8

**M13-owned event types — NEW v0.8 (29 events from M13 Spec Block 8b):**

```
CORRESPONDENCE_CREATED                      // BR-13-002..005
CORRESPONDENCE_CLASSIFIED                   // (type/contractual_weight change)
CORRESPONDENCE_SENT                         // (outgoing transmission timestamp)
CORRESPONDENCE_RESPONDED                    // BR-13-008
CORRESPONDENCE_M05_FLAGGED                  // BR-13-009 + BR-13-010
CORRESPONDENCE_ARCHIVED                     // (soft-delete)
NOTICE_SLA_WARNING                          // BR-13-006
NOTICE_SLA_BREACH                           // BR-13-007
NOTICE_SLA_OVERDUE_RESOLVED                 // (responded after breach)
MEETING_SCHEDULED                           // (MeetingRegister.create)
MEETING_HELD                                // (meeting_end_time recorded)
MINUTES_DRAFTED                             // (status -> Draft in progress)
MINUTES_CIRCULATED                          // (status -> Circulated)
MEETING_MINUTES_APPROVED                    // BR-13-013
MEETING_MINUTES_DISPUTED                    // BR-13-015
MINUTES_ENTRY_ADDED                         // (MinutesEntry.create)
RISK_PROMOTED_FROM_MINUTES                  // BR-13-011
ACTION_ITEM_CREATED                         // BR-13-014
ACTION_ITEM_OWNER_NOTIFIED                  // (post-create)
ACTION_ITEM_OVERDUE                         // BR-13-016
RFI_RAISED                                  // BR-13-018
RFI_RESPONDED                               // BR-13-019
RFI_CLOSED                                  // (status -> Closed)
RFI_RESPONSE_OVERDUE                        // BR-13-020
RFI_IMPACT_FLAGGED                          // BR-13-012
SITE_INSTRUCTION_NON_COMPLIED               // BR-13-022
DISTRIBUTION_SENT                           // BR-13-023
ACKNOWLEDGEMENT_RECORDED                    // (recipient acknowledges)
ACKNOWLEDGEMENT_OVERDUE                     // BR-13-024
PROJECT_CORRESPONDENCE_INITIALISED          // BR-13-001
```

**Total M13 event types: 30 events** (29 listed in Block 8b + 1 PROJECT_CORRESPONDENCE_INITIALISED at BR-13-001).

[Other modules' event types (M01-M06, M05) unchanged from v0.7.]

---

### §4.18 `M13_DecisionQueueTriggerType` (NEW v0.8) — M13-owned

8 trigger types per M13 Spec Block 8c. All UPPER_SNAKE_CASE per `naming-folders.md`.

```
ENUM M13_DecisionQueueTriggerType {
  NOTICE_SLA_WARNING                       // 80% of response window elapsed (BR-13-006)
  NOTICE_SLA_BREACH                        // 100% breached (BR-13-007)
  RFI_RESPONSE_OVERDUE                     // RFI Open > rfi_sla_days (BR-13-020)
  MEETING_MINUTES_NOT_CIRCULATED           // Meeting end + 48hr without circulated minutes (BR-13-017)
  ACTION_ITEM_OVERDUE                      // ActionItem due_date past + status not Closed (BR-13-016)
  MEETING_MINUTES_DISPUTED                 // minutes_status=Disputed (BR-13-015)
  SITE_INSTRUCTION_NON_COMPLIED            // compliance_status auto-set to Non_Complied past deadline (BR-13-022)
  ACKNOWLEDGEMENT_OVERDUE                  // Distribution sent + acknowledgement_timeout_days without acknowledgement (BR-13-024)
}
```

[Other modules' Decision Queue trigger ENUMs (§4.13 M01_DecisionQueueTriggerType, §4.17 M05_DecisionQueueTriggerType, etc.) unchanged from v0.7.]

---

## §5 — ENUM Reference Patterns (unchanged from v0.7)

[See prior versions.]

---

## §6 — Reserved Fields (extended in v0.8 — M13 append-only ledger exemptions added)

Append-only entities (DB-level UPDATE/DELETE forbidden — no `updated_by`, `updated_at`, `is_active`):

[All v0.7 entries unchanged: M02 BACIntegrityLedger / IDGovernanceLog / CSVImportRecord; M01 ProjectPhaseHistory / ProjectStatusHistory; M34 LoginAttempt / SystemAuditLog; M03 Baseline / BaselineExtension / PVProfileSnapshot; M04 ProgressEntryAudit / NCRStatusLog / MaterialReceiptLedger / ContractorPerformanceScoreLog; M06 CostLedgerEntry / RABillAuditLog / PaymentEvidenceLedger / ForexRateLog; M05 RiskStatusLog / VOStatusLog / EOTStatusLog / ContingencyDrawdownLog / LDExposureLog.]

**M13 NEW v0.8 (5 entities):**

| Module | Entity | Why Append-Only |
|---|---|---|
| **M13** | **CorrespondenceStatusLog** | **NEW v0.8 — Append-only per M13 Spec Block 3b.2 + OQ-2.2** |
| **M13** | **NoticeSLAEvent** | **NEW v0.8 — Append-only per M13 Spec Block 3b.4 + OQ-2.2** |
| **M13** | **MeetingMinutesAuditLog** | **NEW v0.8 — Append-only per M13 Spec Block 3b.7 + OQ-2.2** |
| **M13** | **RFIStatusLog** | **NEW v0.8 — Append-only per M13 Spec Block 3b.10 + OQ-2.2** |
| **M13** | **DistributionList** | **NEW v0.8 — Partial append-only per M13 Spec Block 3b.12 (received_at mutable until acknowledged_at set; row immutable thereafter for legal-evidence integrity)** |

**Total append-only entities: 28** (was 23 in v0.7; +5 from M13 in v0.8).

---

## §7 — Glossary (unchanged from v0.7; new v0.8 terms added)

[See prior versions for ARTA, EAC, EVM, EOT, EWN, LD, PV, RA Bill, VO, etc.]

**New v0.8 glossary terms (M13-driven):**

- **Notice (Contractual).** Formal correspondence with contractual weight that obligates response within a defined SLA window. M13 tracks notices via the `NoticeTracker` sub-view (Correspondence with `correspondence_type = Notice` AND `contractual_weight IN (Formal_Notice, Contractual)`). SLA escalation: 50% / 80% / 100% thresholds emit Decision Queue triggers per BR-13-006/007.

- **RFI (Request for Information).** Formal request for clarification raised by a project participant (typically contractor) to the project's information owner (typically client/designer). M13 owns RFI metadata + lifecycle (Open → Responded → Closed); M12 owns attachment blobs. SLA-bound (default 14 days per `ProjectCorrespondenceConfig.rfi_sla_days`).

- **Site Instruction.** Formal instruction issued on site by employer's representative to contractor. Modelled in M13 as `Correspondence` with `correspondence_type = Site_Instruction` (per OQ-1.3 single-entity lock). Has `compliance_deadline` + `compliance_status` fields. Non-compliance past deadline emits cross-module event to M05 for potential NCR-basis assessment.

- **Transmittal.** Formal package transmission of multiple documents (drawings, specifications, BOQ revisions) with explicit recipient list and acknowledgement tracking. Distinct from individual Correspondence in that it bundles multiple `document_id` references for a single contractual delivery.

- **Distribution List.** Per-recipient receipt + acknowledgement ledger for Correspondence / Meeting / Transmittal / RFI. Captures `recipient_user_id` OR `recipient_party_id` OR `recipient_email`, `received_at`, `acknowledged_at`, `acknowledgement_method`. Append-only post-acknowledgement (legal evidence integrity).

- **Minutes Entry.** Structured line-item within a meeting's minutes (per M13 OQ-1.4=B lock). Each entry has an `entry_type` ENUM (Agenda / Decision / Action / Discussion / Risk_Noted / Information / Question). Action entries auto-create `ActionItem` rows; Risk_Noted entries may be promoted to `M05.Risk` (one-way; PROJECT_DIRECTOR / PMO_DIRECTOR authority).

- **Action Item.** Discrete, time-bounded task with explicit owner (User OR Party FK; CHECK exactly-one-populated per OQ-1.5). Auto-emitted to M11 ActionRegister Decision Queue. Lifecycle: Open → In_Progress → Completed (or Overdue / Cancelled / Deferred). Daily SLA sweep emits `ACTION_ITEM_OVERDUE` trigger past `due_date`.

---

## M05+M13 Batch Audit Pass Verification (Round 34 task Deliverable B1)

Per Round 34 task spec: "Audit pass verification — check these against M05 Spec v1.0".

| Audit Check | Result |
|---|---|
| Every ENUM used in M05 Spec Block 3b has an entry in X8 v0.7 §3.73-§3.88 | ✅ **PASS** — all 16 M05 ENUMs (RiskCategory, RiskRAGStatus, RiskStatus, RiskResponseStrategy, ChangeItemType, ChangeItemStatus, VariationOrderType, VOCause, VOStatus, VOApprovalLevel, VOMaterialisationStatus, EOTClaimBasis, EOTStatus, EWNStatus, ContingencyDrawdownStatus, LDStatus) verified at §3.73-§3.88; carried forward intact to v0.8 |
| Every audit event in M05 Spec Block 8b exists in X8 v0.7 §4.12 | ✅ **PASS** — all 33 M05 events verified in v0.7 §4.12 M05 section; carried forward intact |
| Every DQ trigger in M05 Spec Block 8c exists in X8 v0.7 §4.17 | ✅ **PASS** — all 10 M05 DQ triggers verified in v0.7 §4.17 M05_DecisionQueueTriggerType ENUM; carried forward intact |
| **0 audit gaps found between M05 Spec v1.0 and X8 v0.7.** | ✅ **PASS** |

Per Round 34 task spec: "Forbidden chart types check: verify M05 Spec and M13 Spec do not reference any forbidden chart types (3D, radar, dual-axis, gauge, pie >6 segments)".

| Forbidden chart check | M05 Spec result | M13 Spec result |
|---|---|---|
| 3D charts | ✅ None referenced | ✅ None referenced |
| Radar charts | ✅ None referenced | ✅ None referenced |
| Dual-axis charts | ✅ None referenced | ✅ None referenced |
| Gauge charts | ⚠️ M05 Block 5d "LD Exposure dashboard" mentions cumulative + cap — implementable as **horizontal bar with cap-marker** (not a gauge); confirm in X9 v0.5 chart catalogue audit | ✅ None referenced |
| Pie charts > 6 segments | ✅ None referenced | ✅ None referenced |

**Note on gauge:** M05 Spec Block 5d describes "LD Exposure dashboard" with cumulative + cap. Implementation should use horizontal bar + cap marker (per X9 v0.4 Tier 1 chart catalogue) — NOT a gauge chart. Will explicitly clarify in M05 Wireframes (R35) authoring per X9 dual-encode + forbidden-anti-pattern rules.

---

*v0.8 — LOCKED 2026-05-04 (Round 34). Source modules: M34, M01, M02, M03, M04, M05, M06, M13 (NEW v0.8). Next bump: v0.9 anticipated at M07 EVMEngine Spec lock (Round 45).*
