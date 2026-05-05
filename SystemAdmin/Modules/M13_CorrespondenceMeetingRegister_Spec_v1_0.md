---
artefact: M13_CorrespondenceMeetingRegister_Spec_v1_0
round: 34
date: 2026-05-04
author: Monish (with Claude assist)
parent_brief: M13_CorrespondenceMeetingRegister_Brief_v1_0 (Round 32)
x8_version: v0.8
x9_version: v0.5
status: LOCKED
type: Module Spec (10-block)
re_issue_of: n/a (NEW module — no legacy v2.x predecessor)
references_locked: All M13 Brief OQ-1.1-1.8 + OQ-2.1-2.5; M05 Spec v1.0 (R33) batch partner — Correspondence triggers M05 EOT/VO claim assessment; M11 ActionRegister forward constraint (Decision Queue); M12 DocumentControl forward constraint (document_id FK); M01 Contract financial parameters (notice SLA periods); M03 Milestone IDs for RFI affected_milestones; M04 NCR cross-reference (Site Instruction linkage)
---

# M13 — Correspondence & Meeting Register — Spec v1.0

## CHANGE LOG

| Version | Date | Author | Change Summary |
|---|---|---|---|
| v1.0 | 2026-05-04 | Monish (with Claude assist) | Initial standalone consolidated spec (Round 34). All 13 M13 Brief v1.0 OQ items embedded as locked. Slim-core scope per OQ-1.1=B (Correspondence + Notices + Meetings + Actions + RFIs + Transmittals; document storage to M12; action SLA to M11; commercial deliberation to M05). 13 entities including 5 append-only ledgers (CorrespondenceStatusLog, NoticeSLAEvent, MeetingMinutesAuditLog, RFIStatusLog, DistributionList) with DB-level UPDATE/DELETE forbidden. 24 BRs (BR-13-001..024). 24 audit events (Appendix A locked from authoring per OQ-2.1). 7 Decision Queue triggers (Block 8c). All parent contracts honoured: M05 batch partner (Correspondence with type=Notice/Claim → triggers M05 EOT/VO assessment via M05 internal API per OQ-1.1); M11 ActionRegister forward constraint (M13 emits ActionItem + 7 DQ trigger types); M12 DocumentControl forward constraint (document_id FK with M12-stub interim pattern); M01 Contract notice SLA periods read for response_due_date computation; M03 Milestone IDs for RFI affected_milestones[]; M04 NCR cross-reference (Site Instruction linkage via CorrespondenceType=Site_Instruction). 0 open questions in Block 10. |

---

## BLOCK 1 — IDENTITY

```
Module ID                : M13
Module Name              : Correspondence & Meeting Register
Layer                    : L2 — Risk / Commercial (paper-trail layer)
Phase                    : 1 — Foundational (precedes M11 ActionRegister; consumed by M05/M19)
Build Weeks              : 3 (estimate; module dense — 13 entities, 24 BRs, SLA computations)
Decision It Enables      : "Are all formal communications — letters, instructions,
                            meeting minutes, action items — captured, tracked, responded
                            to within contractual timelines, and available as an auditable
                            record for claims, disputes, and governance?"
Primary User             : PROJECT_DIRECTOR (notice tracker, meeting calendar, action item oversight)
Secondary Users          : PMO_DIRECTOR (notice SLA breach dashboard, acknowledgement audit),
                            PORTFOLIO_MANAGER (portfolio correspondence rollup),
                            PLANNING_ENGINEER (open RFIs, pending action items),
                            QS_MANAGER (action item queue, meeting prep, notices→VOs),
                            SITE_MANAGER (daily inbound correspondence, RFI raise, today's meetings),
                            COMPLIANCE_MANAGER (regulatory notices, M09 cross-link),
                            PROCUREMENT_OFFICER (vendor correspondence + transmittals + vendor RFIs),
                            ANALYST (correspondence trends, RFI response-time analysis)
Folder                   : SystemAdmin/Modules/
Re-Issue Of              : n/a (NEW module — no legacy v2.x predecessor)
Source Brief             : M13_CorrespondenceMeetingRegister_Brief_v1_0 (Round 32)
Cadence                  : C1 (Spec; one artefact at a time per spec-protocol.md)
Round Date               : 2026-05-04 (Round 34)
C1b Batch Partner        : M05 RiskChangeControl (peer module same layer; batch in Wireframes R35 + Workflows R36)
```

### Decisions It Enables (downstream rounds)

| Round | Artefact | Authority From This Spec |
|---|---|---|
| **R35** | M05 + M13 Wireframes (C1b batch) | Block 5 Filters & Views + role-default views per X9 v0.5 §13.3.13 (added in this round's Deliverable B) |
| **R36** | M05 + M13 Workflows (C1b batch) | Block 6 BR runtime flows + Block 8 audit-event emit hooks |
| **R58** | M11 ActionRegister Brief | Forward constraint — M11 must accept M13 ActionItem emit + 7 DQ trigger types |
| **Future** | M12 DocumentControl Spec | Forward constraint — M12 must accept M13 document_id allocation requests for Correspondence + RFI + Transmittal + MinutesEntry attachments |

---

## BLOCK 2 — SCOPE BOUNDARY

### 2a. INCLUDES

| # | Item | OQ Authority |
|---|---|---|
| 1 | **Correspondence Register** — single `Correspondence` entity per OQ-1.3 (direction = Incoming/Outgoing ENUM); all formal communication types (letters, notices, instructions, formal emails) | OQ-1.1, OQ-1.3 |
| 2 | **Notice Tracker** — subset/sub-view of Correspondence where type=Notice; SLA-bound with 50%/80%/100% threshold escalation per OQ-1.2 | OQ-1.2 |
| 3 | **Meeting Register** — meeting types (kickoff/site-progress/technical/contractual/subcontractor/regulatory/board/closeout); attendees via DistributionList; agenda + minutes | OQ-1.1 |
| 4 | **Structured Minutes** — `MinutesEntry` rows per meeting with type ENUM (Decision/Action/Discussion/Risk_Noted/Information/Question) per OQ-1.4 | OQ-1.4 |
| 5 | **Action Items** — auto-created from MinutesEntry rows where `entry_type = Action`; standalone creation also supported; owner = User OR Party FK per OQ-1.5 | OQ-1.5 |
| 6 | **RFI** (Request for Information) — full lifecycle (Open → Responded → Closed); SLA-bound; affected_milestones[] for M03 cross-link; metadata in M13, attachments in M12 per OQ-1.6 | OQ-1.6 |
| 7 | **Site Instruction** — Correspondence with `correspondence_type = Site_Instruction` (per OQ-1.3 single-entity model); compliance deadline + status tracking via Correspondence fields | OQ-1.3 |
| 8 | **Transmittal** — outgoing formal package transmissions; receipt-acknowledgement tracking via DistributionList | OQ-1.7 |
| 9 | **Distribution + Acknowledgement** — explicit `DistributionList` entity per OQ-1.7; per-recipient `received_at` + `acknowledged_at` + `acknowledgement_method` | OQ-1.7 |
| 10 | **M05 Cross-Module Trigger** — `triggers_m05` boolean field on Correspondence (PROJECT_DIRECTOR or PMO_DIRECTOR sets); fires `CORRESPONDENCE_M05_FLAGGED` event to M05 internal API per Brief §10 forward constraint + M05 batch | OQ-1.1 |
| 11 | **Risk_Noted Promotion** — `MinutesEntry` rows where `entry_type = Risk_Noted` may be promoted to `M05.Risk` via UI action (audited; one-way; cannot un-promote) | OQ-1.4 |
| 12 | **Action Item SLA Escalation** — overdue ActionItem auto-emits Decision Queue trigger to M11 (when built) per OQ-2.3 | OQ-2.3 |
| 13 | **Contractual Notice Period Defaults** — configurable per project via `ProjectCorrespondenceConfig` (notice_sla_warning_pct, rfi_sla_days, acknowledgement_timeout_days, meeting_minutes_circulation_hours, correspondence_retention_years) per OQ-2.5 | OQ-2.5 |

### 2b. EXCLUDES

| # | Item | Reason / Where Addressed |
|---|---|---|
| 1 | **Document storage internals** (file blobs, version control, redlines, watermarks) | M12 DocumentControl owns; M13 stores `document_id` references only (M12-stub interim pattern matching M04 photo stub) |
| 2 | **Variation Order + EOT processing** | M05 RiskChangeControl owns; M13 emits `CORRESPONDENCE_M05_FLAGGED` trigger; M05 decides commercial consequence |
| 3 | **Action SLA enforcement / Decision Queue routing** | M11 ActionRegister owns SLA escalation; M13 emits triggers |
| 4 | **Long-form claims documentation** (expert assessments, arbitration packets) | M19 ClaimsManagement Phase 2; M13 emits Correspondence chain export |
| 5 | **Site daily diary** (free-text day log) | M16 SiteDiary (separate Phase 1 module) |
| 6 | **Email integration / IMAP ingestion** | Phase 2 (manual entry only in v1.0; ingestion automation deferred until volume justifies) |
| 7 | **Speech-to-text meeting minutes** | Phase 2 |
| 8 | **Document review workflows** (approval routing, redlining) | M12 owns when built |
| 9 | **External-party portal access** (CLIENT_VIEWER, LENDER_VIEWER, etc.) | PF03 ExternalPartyPortal Phase 2 |
| 10 | **Drawing and submittal management** | M12 (drawings) + future module M27 DesignControl (submittals) |
| 11 | **Procurement-specific correspondence flows** (vendor PQ, tender clarifications) | M30 VendorMasterPQ + M29 TenderingAward (Phase 2) |
| 12 | **Legal proceedings and dispute management** | M19 Phase 2 |
| 13 | **Regulatory compliance enforcement** | M09 ComplianceTracker; M13 captures regulatory notices but doesn't enforce compliance |

### 2c. Hard Boundaries (must-not-cross during build)

1. **M13 never stores file BLOBs.** All attachments via `document_id` FK to M12 (or M12-stub MinIO direct URL during interim).
2. **M13 never makes commercial deliberation.** Notices flagged with `triggers_m05 = true` emit event to M05; M05 decides EOT/VO claim merit.
3. **M13 never enforces ActionItem SLAs.** M13 emits Decision Queue triggers to M11; M11 owns SLA escalation logic.
4. **`triggers_m05` flag is RBAC-restricted.** Only PROJECT_DIRECTOR or PMO_DIRECTOR can set `triggers_m05 = true` (BR-13-009). System enforces; API rejects with 403 for other roles.
5. **DistributionList is append-only on acknowledgement.** Once `acknowledged_at` is set, the row cannot be modified (legal evidence integrity).
6. **MinutesEntry promotion to M05.Risk is one-way.** Once a Risk_Noted entry is promoted, it cannot be un-promoted (only the resulting M05.Risk can be Withdrawn).
7. **Closed RFI cannot be reopened** without PMO_DIRECTOR authority (BR-13-022).

---

## BLOCK 3 — DATA ARCHITECTURE

### 3a. Entities (13 total per Brief §7)

| # | Entity | Cardinality | Owner | Purpose | Append-Only? |
|---|---|---|---|---|---|
| 1 | `Correspondence` | Many per project | M13 | Single source of truth for formal communications. Direction (Incoming/Outgoing), type classification (Letter/Notice/Instruction/RFI_Reference/Email_Formal/Site_Instruction/Regulatory/Legal/Transmittal_Reference), contractual reference, document_id FK to M12. Includes site instructions per OQ-1.3 single-entity lock. | No (state machine; soft-delete via is_active) |
| 2 | `CorrespondenceStatusLog` | Many per Correspondence | M13 | Every classification change + state transition + `triggers_m05` flag flips | **YES** |
| 3 | `NoticeTracker` | Sub-view of Correspondence (where `correspondence_type = Notice`) | M13 | SLA-bound view; tracks response window per contractual clause; auto-emits Decision Queue triggers at 50%/80%/100% thresholds | No (computed view) |
| 4 | `NoticeSLAEvent` | Many per NoticeTracker | M13 | Each SLA threshold crossed (50%/80%/100%) + breach event | **YES** |
| 5 | `MeetingRegister` | Many per project | M13 | Meeting types, location, datetime, agenda, chairperson; attendees via DistributionList | No (state machine) |
| 6 | `MinutesEntry` | Many per Meeting | M13 | Structured line-items with `entry_type` ENUM (Decision/Action/Discussion/Risk_Noted/Information/Question) per OQ-1.4 | No |
| 7 | `MeetingMinutesAuditLog` | Many per Meeting | M13 | Every minutes edit + line-item add/edit/delete operation; preserves intent of OQ-1.4 structured minutes | **YES** |
| 8 | `ActionItem` | Many per Meeting OR per Notice OR standalone | M13 | Action emitted to M11 ActionRegister; `owner_user_id` (NULLABLE FK M34) OR `owner_party_id` (NULLABLE FK M01) per OQ-1.5; CHECK constraint exactly-one-populated | No |
| 9 | `RFI` | Many per project | M13 | RFI lifecycle (Open → Responded → Closed); SLA-bound; `affected_milestones[]` array of M03.Milestone UUIDs; `attachment_document_ids[]` array of M12.Document FK refs (M12-stub interim) | No (state machine) |
| 10 | `RFIStatusLog` | Many per RFI | M13 | State transitions + response edits | **YES** |
| 11 | `Transmittal` | Many per project | M13 | Outgoing formal package transmissions (drawings, specifications, BOQ revisions); receipt-acknowledgement tracking via DistributionList | No (state machine) |
| 12 | `DistributionList` | Many per Correspondence/Notice/Minutes/Transmittal | M13 | Per-recipient receipt + acknowledgement record; `recipient_user_id` NULLABLE FK + `recipient_party_id` NULLABLE FK + `recipient_email` (free-text for non-system recipients) + `received_at` + `acknowledged_at` + `acknowledgement_method` | **YES** (on acknowledgement; received_at can be updated until acknowledged_at set) |
| 13 | `ProjectCorrespondenceConfig` | 1 per project | M13 | Per-project tunables per OQ-2.5 (5 fields) | No |

**Append-only ledgers:** 5 entities (CorrespondenceStatusLog, NoticeSLAEvent, MeetingMinutesAuditLog, RFIStatusLog, DistributionList — partial append-only). DB-level UPDATE/DELETE forbidden via `REVOKE UPDATE, DELETE` on these tables. Exception: `DistributionList` permits `received_at` update until `acknowledged_at` is set (then row becomes fully immutable per legal-evidence integrity).

### 3b. Field Schemas

#### 3b.1 — `Correspondence`

| Field | Type | Required | Validation Rule / Source |
|---|---|---|---|
| `id` | UUID | Y | Auto |
| `tenant_id`, `created_by`, `created_at`, `updated_by`, `updated_at`, `is_active` | — | Y | Reserved fields per `naming-folders.md` §Reserved Fields |
| `project_id` | UUID | Y | FK → `M01.Project` |
| `correspondence_code` | VARCHAR(20) | Y | Per-project sequential; format `COR-{NNNN}` |
| `direction` | ENUM | Y | Per X8 v0.8 §3.89 `CorrespondenceDirection` (Incoming / Outgoing) |
| `correspondence_type` | ENUM | Y | Per X8 v0.8 §3.90 `CorrespondenceType` (Letter / Notice / Instruction / RFI_Reference / Email_Formal / Site_Instruction / Regulatory / Legal / Transmittal_Reference) |
| `contractual_weight` | ENUM | Y | Per X8 v0.8 §3.91 `ContractualWeight` (Non_Contractual / Contractual / Formal_Notice / Without_Prejudice). `Formal_Notice` weight implies SLA tracking via NoticeTracker view |
| `subject` | VARCHAR(200) | Y | Min 10 chars |
| `body_summary` | TEXT | Y | Min 100 chars |
| `sender_user_id` | UUID | N | FK → `M34.User` (for outgoing OR if incoming sender is internal user) |
| `sender_party_id` | UUID | N | FK → `M01.Party` (for incoming from external party) |
| `sender_email` | VARCHAR(254) | N | Free-text for non-system senders |
| `sent_date` | DATE | Y | For outgoing: send date. For incoming: received date |
| `contractual_reference` | TEXT | N | Required if `correspondence_type IN (Notice, Site_Instruction)` per BR-13-002; ≥ 50 chars (clause text or contract section reference) |
| `parent_correspondence_id` | UUID | N | FK → `Correspondence` (self-FK for thread chaining; null for thread root) |
| `response_required` | BOOLEAN | Y | Default false. Auto-set to true if `correspondence_type IN (Notice, RFI_Reference, Site_Instruction)` |
| `response_due_date` | DATE | N | Required if `response_required = true`; auto-computed from `sent_date + applicable_sla_days` per BR-13-007 |
| `response_status` | ENUM | Y | Per X8 v0.8 §3.92 `CorrespondenceResponseStatus` (Not_Required / Pending / Responded / Overdue / Escalated) |
| `responded_at` | TIMESTAMP | N | Auto on response |
| `responded_by_user_id` | UUID | N | FK → `M34.User` |
| `responded_via_correspondence_id` | UUID | N | FK → `Correspondence` (the response is itself a Correspondence row in opposite direction) |
| `triggers_m05` | BOOLEAN | Y | Default false. Set true only by PROJECT_DIRECTOR or PMO_DIRECTOR per BR-13-009. Setting true fires `CORRESPONDENCE_M05_FLAGGED` event to M05 |
| `m05_trigger_reason` | TEXT | N | Required if `triggers_m05 = true`; ≥ 50 chars; describes which M05 entity (EOT/VO/Risk) is anticipated |
| `compliance_deadline` | DATE | N | Required if `correspondence_type = Site_Instruction`; instructs contractor to comply by this date |
| `compliance_status` | ENUM | N | Per X8 v0.8 §3.93 `SiteInstructionComplianceStatus` (Pending / In_Progress / Complied / Non_Complied / Disputed). Required if `correspondence_type = Site_Instruction` |
| `m04_ncr_id` | UUID | N | FK → `M04.ConstructionNCR` if Site Instruction is linked to a remediation of an NCR |
| `document_id` | UUID | N | FK → `M12.Document` (M12-stub: MinIO direct URL during interim; migration script in Spec Appendix C when M12 lands) |
| `archived_at` | TIMESTAMP | N | Set when `is_active → false`; soft delete (correspondence cannot be hard-deleted per BR-13-018) |

**Composite uniqueness:** `(tenant_id, project_id, correspondence_code)`.

#### 3b.2 — `CorrespondenceStatusLog` (append-only)

| Field | Type | Required | Validation / Source |
|---|---|---|---|
| `id` | UUID | Y | Auto |
| `tenant_id` | UUID | Y | Reserved |
| `correspondence_id` | UUID | Y | FK → `Correspondence` |
| `event_type` | ENUM | Y | Classification_Changed / Status_Transition / TriggersM05_Flipped / Archived |
| `from_value` | TEXT | N | JSON snapshot of old field value |
| `to_value` | TEXT | Y | JSON snapshot of new field value |
| `changed_by` | UUID | Y | FK → `M34.User` |
| `changed_at` | TIMESTAMP | Y | Auto |

DB constraints: `REVOKE UPDATE, DELETE FROM app_role`. No `updated_by`/`updated_at`/`is_active`.

#### 3b.3 — `NoticeTracker` (sub-view; not a separate table — view over `Correspondence` where `correspondence_type = Notice` AND `contractual_weight IN (Formal_Notice, Contractual)`)

Materialised view fields (read-only):
- `correspondence_id` (FK to source row)
- `notice_raised_at`
- `response_due_date`
- `sla_window_days` (from `ProjectCorrespondenceConfig`)
- `sla_warning_pct` (0.80 default per OQ-1.2)
- `sla_remaining_pct` (CALC; updated daily by background sweep)
- `sla_status` (CALC = Within / Warning / Breach)

#### 3b.4 — `NoticeSLAEvent` (append-only)

| Field | Type | Required | Validation / Source |
|---|---|---|---|
| `id` | UUID | Y | Auto |
| `tenant_id` | UUID | Y | Reserved |
| `correspondence_id` | UUID | Y | FK → `Correspondence` (with `correspondence_type = Notice`) |
| `event_type` | ENUM | Y | SLA_50_Crossed / SLA_80_Crossed / SLA_100_Breached |
| `triggered_at` | TIMESTAMP | Y | Auto |
| `triggered_by_sweep` | BOOLEAN | Y | Default true (background sweep emits); false if manually triggered by PMO override |
| `decision_queue_trigger_id` | UUID | N | FK to M11 Decision Queue row created (when M11 built) |

DB UPDATE/DELETE forbidden.

#### 3b.5 — `MeetingRegister`

| Field | Type | Required | Validation / Source |
|---|---|---|---|
| `id` | UUID | Y | Auto |
| `tenant_id`, `created_by`, `created_at`, `updated_by`, `updated_at`, `is_active` | — | Y | Reserved fields |
| `project_id` | UUID | Y | FK → `M01.Project` |
| `meeting_code` | VARCHAR(20) | Y | Per-project sequential; format `MTG-{NNNN}` |
| `meeting_type` | ENUM | Y | Per X8 v0.8 §3.94 `MeetingType` (Kickoff / Site_Progress / Technical / Contractual / Subcontractor / Regulatory / Board / Closeout) |
| `title` | VARCHAR(200) | Y | Min 10 chars |
| `meeting_date` | DATE | Y | — |
| `meeting_start_time` | TIME | Y | — |
| `meeting_end_time` | TIME | N | Set when meeting concludes |
| `location` | VARCHAR(200) | Y | Free-text (physical venue OR "Virtual — {platform}") |
| `chairperson_user_id` | UUID | Y | FK → `M34.User` |
| `agenda_text` | TEXT | Y | Min 50 chars |
| `minutes_status` | ENUM | Y | Per X8 v0.8 §3.95 `MinutesStatus` (Draft / Circulated / Approved / Disputed) |
| `minutes_drafted_by_user_id` | UUID | N | FK → `M34.User` |
| `minutes_drafted_at` | TIMESTAMP | N | Auto |
| `minutes_circulated_at` | TIMESTAMP | N | Auto on transition Draft → Circulated |
| `minutes_approved_by_user_id` | UUID | N | FK → `M34.User` (PMO_DIRECTOR or PROJECT_DIRECTOR per BR-13-013) |
| `minutes_approved_at` | TIMESTAMP | N | Auto on transition Circulated → Approved |
| `minutes_dispute_note` | TEXT | N | Required if `minutes_status = Disputed`; ≥ 100 chars |
| `minutes_document_id` | UUID | N | FK → `M12.Document` (final approved minutes PDF when M12 lands; M12-stub interim) |

#### 3b.6 — `MinutesEntry`

| Field | Type | Required | Validation / Source |
|---|---|---|---|
| `id` | UUID | Y | Auto |
| `tenant_id`, `created_by`, `created_at`, `updated_by`, `updated_at`, `is_active` | — | Y | Reserved fields |
| `meeting_id` | UUID | Y | FK → `MeetingRegister` |
| `entry_seq` | INTEGER | Y | Sequential within meeting (1, 2, 3, ...) |
| `entry_type` | ENUM | Y | Per X8 v0.8 §3.96 `MinutesEntryType` (Agenda / Decision / Action / Discussion / Risk_Noted / Information / Question) |
| `entry_text` | TEXT | Y | Min 30 chars |
| `referenced_correspondence_id` | UUID | N | FK → `Correspondence` (cross-link if entry references a specific letter/notice) |
| `referenced_milestone_id` | UUID | N | FK → `M03.Milestone` (if entry references a schedule milestone) |
| `promoted_to_m05_risk_id` | UUID | N | FK → `M05.Risk` (set if `entry_type = Risk_Noted` and PMO/PROJECT_DIRECTOR has promoted to M05.Risk per BR-13-019). One-way; not reversible. |
| `action_item_id` | UUID | N | FK → `ActionItem` (auto-set when `entry_type = Action` per BR-13-014) |

**Composite uniqueness:** `(tenant_id, meeting_id, entry_seq)`.

#### 3b.7 — `MeetingMinutesAuditLog` (append-only)

Standard append-only log: `id`, `tenant_id`, `meeting_id`, `event_type` (Minutes_Drafted / Entry_Added / Entry_Edited / Entry_Deleted / Status_Transition / Risk_Promoted / Approval), `from_value` (JSON), `to_value` (JSON), `changed_by`, `changed_at`. DB UPDATE/DELETE forbidden.

#### 3b.8 — `ActionItem`

| Field | Type | Required | Validation / Source |
|---|---|---|---|
| `id` | UUID | Y | Auto |
| `tenant_id`, `created_by`, `created_at`, `updated_by`, `updated_at`, `is_active` | — | Y | Reserved fields |
| `project_id` | UUID | Y | FK → `M01.Project` |
| `action_code` | VARCHAR(20) | Y | Per-project sequential; format `ACT-{NNNN}` |
| `source` | ENUM | Y | Per X8 v0.8 §3.97 `ActionItemSource` (Meeting / Site_Instruction / RFI / Correspondence / Manual) |
| `source_meeting_id` | UUID | N | FK → `MeetingRegister` (set if `source = Meeting`) |
| `source_minutes_entry_id` | UUID | N | FK → `MinutesEntry` (set if auto-created from MinutesEntry per BR-13-014) |
| `source_correspondence_id` | UUID | N | FK → `Correspondence` (set if `source IN (Site_Instruction, Correspondence)`) |
| `source_rfi_id` | UUID | N | FK → `RFI` (set if `source = RFI`) |
| `title` | VARCHAR(200) | Y | Min 10 chars |
| `description` | TEXT | Y | Min 50 chars |
| `owner_user_id` | UUID | N | FK → `M34.User` (if owner is internal user) |
| `owner_party_id` | UUID | N | FK → `M01.Party` (if owner is external party — contractor, consultant, regulator) |
| `due_date` | DATE | Y | — |
| `status` | ENUM | Y | Per X8 v0.8 §3.98 `ActionItemStatus` (Open / In_Progress / Completed / Overdue / Cancelled / Deferred) |
| `escalated_to_m11` | BOOLEAN | Y | Default false. System-set true on SLA breach per BR-13-016 |
| `sla_breach_date` | DATE | Y | CALC = `due_date + 1 day` (i.e., the date on which Open/In_Progress flips to Overdue) |
| `closed_at` | TIMESTAMP | N | Set on transition to Completed/Cancelled |
| `closure_note` | TEXT | N | Required if `status IN (Cancelled, Deferred)`; ≥ 50 chars |

**CHECK constraint:** exactly one of `owner_user_id`, `owner_party_id` populated (per OQ-1.5 lock). DB-level CHECK enforcement.

#### 3b.9 — `RFI`

| Field | Type | Required | Validation / Source |
|---|---|---|---|
| `id` | UUID | Y | Auto |
| `tenant_id`, `created_by`, `created_at`, `updated_by`, `updated_at`, `is_active` | — | Y | Reserved fields |
| `project_id` | UUID | Y | FK → `M01.Project` |
| `rfi_code` | VARCHAR(20) | Y | Per-project sequential; format `RFI-{NNNN}` |
| `subject` | VARCHAR(200) | Y | Min 10 chars |
| `question_text` | TEXT | Y | Min 100 chars |
| `raised_by_user_id` | UUID | Y | FK → `M34.User` |
| `raised_by_party_id` | UUID | N | FK → `M01.Party` (when raised by external party — typically contractor) |
| `raised_at` | TIMESTAMP | Y | Auto |
| `addressed_to` | TEXT | Y | Free-text — typically client/designer name |
| `response_due_date` | DATE | Y | CALC = `raised_at_date + ProjectCorrespondenceConfig.rfi_sla_days` (default 14) per BR-13-021 |
| `status` | ENUM | Y | Per X8 v0.8 §3.99 `RFIStatus` (Open / Responded / Closed / Overdue) |
| `response_text` | TEXT | N | Required when `status → Responded`; ≥ 50 chars |
| `responded_at` | TIMESTAMP | N | Auto on Responded transition |
| `responded_by_user_id` | UUID | N | FK → `M34.User` (QS_MANAGER, PROJECT_DIRECTOR, or PMO_DIRECTOR per Block 4a) |
| `closed_at` | TIMESTAMP | N | Auto on Closed transition |
| `affected_milestones` | JSONB array of UUID | N | Optional FK refs to `M03.Milestone` |
| `design_impact` | BOOLEAN | Y | Default false. Manual flag. |
| `cost_impact` | BOOLEAN | Y | Default false. If true → emit `RFI_IMPACT_FLAGGED` to M05 per BR-13-022 |
| `schedule_impact` | BOOLEAN | Y | Default false. If true → emit `RFI_IMPACT_FLAGGED` to M05 per BR-13-022 |
| `attachment_document_ids` | JSONB array of UUID | N | FK refs to `M12.Document` (M12-stub interim) |

#### 3b.10 — `RFIStatusLog` (append-only)

Standard append-only log per CorrespondenceStatusLog pattern: `id`, `tenant_id`, `rfi_id`, `event_type`, `from_value`, `to_value`, `changed_by`, `changed_at`.

#### 3b.11 — `Transmittal`

| Field | Type | Required | Validation / Source |
|---|---|---|---|
| `id` | UUID | Y | Auto |
| `tenant_id`, `created_by`, `created_at`, `updated_by`, `updated_at`, `is_active` | — | Y | Reserved fields |
| `project_id` | UUID | Y | FK → `M01.Project` |
| `transmittal_code` | VARCHAR(20) | Y | Per-project sequential; format `TRX-{NNNN}` |
| `subject` | VARCHAR(200) | Y | Min 10 chars |
| `transmittal_purpose` | ENUM | Y | Per X8 v0.8 §3.100 `TransmittalPurpose` (Drawing_Issue / Specification_Update / BOQ_Revision / Submittal / Information / Approval_Request) |
| `package_description` | TEXT | Y | Min 100 chars |
| `attachment_document_ids` | JSONB array of UUID | Y | At least 1 FK to `M12.Document` (M12-stub interim) |
| `sent_at` | TIMESTAMP | Y | Auto |
| `sent_by_user_id` | UUID | Y | FK → `M34.User` |
| `status` | ENUM | Y | Per X8 v0.8 §3.101 `TransmittalStatus` (Sent / Acknowledged_Partial / Acknowledged_Full / Closed) |
| `closed_at` | TIMESTAMP | N | Set on transition to Closed |

#### 3b.12 — `DistributionList` (append-only on acknowledgement)

| Field | Type | Required | Validation / Source |
|---|---|---|---|
| `id` | UUID | Y | Auto |
| `tenant_id` | UUID | Y | Reserved |
| `parent_entity_type` | ENUM | Y | Correspondence / MeetingRegister / Transmittal / RFI |
| `parent_entity_id` | UUID | Y | FK to parent (polymorphic; resolved by `parent_entity_type`) |
| `recipient_user_id` | UUID | N | FK → `M34.User` (for system recipients) |
| `recipient_party_id` | UUID | N | FK → `M01.Party` (for organisational recipients) |
| `recipient_email` | VARCHAR(254) | N | Free-text for non-system recipients |
| `received_at` | TIMESTAMP | N | Set when system records receipt (mutable until `acknowledged_at` is set) |
| `acknowledged_at` | TIMESTAMP | N | Set when recipient acknowledges (immutable once set per BR-13-024) |
| `acknowledgement_method` | ENUM | N | Per X8 v0.8 §3.102 `AcknowledgementMethod` (System_Click / Email_Reply / Verbal_Recorded / Physical_Signature) |
| `created_by`, `created_at` | — | Y | Reserved (no `updated_by`/`updated_at`/`is_active` once `acknowledged_at` set; effectively append-only post-acknowledgement) |

**CHECK constraint:** at least one of `recipient_user_id`, `recipient_party_id`, `recipient_email` populated. UNIQUE: `(parent_entity_type, parent_entity_id, recipient_user_id, recipient_party_id, recipient_email)` (one row per recipient per parent).

**DB-level rule:** UPDATE allowed on `received_at` only IF `acknowledged_at IS NULL`. Once `acknowledged_at` set, row becomes immutable (REVOKE UPDATE, DELETE).

#### 3b.13 — `ProjectCorrespondenceConfig`

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `id` | UUID | Y | Auto | — |
| `tenant_id`, `created_by`, `created_at`, `updated_by`, `updated_at`, `is_active` | — | Y | Reserved | — |
| `project_id` | UUID | Y | — | FK → `M01.Project`; UNIQUE |
| `notice_sla_warning_pct` | DECIMAL(5,4) | Y | 0.80 | OQ-1.2 lock |
| `rfi_sla_days` | INTEGER | Y | 14 | OQ-2.3 |
| `acknowledgement_timeout_days` | INTEGER | Y | 7 | OQ-2.3 |
| `meeting_minutes_circulation_hours` | INTEGER | Y | 48 | OQ-2.3 |
| `correspondence_retention_years` | INTEGER | Y | 7 | Aligns with Companies Act + DPDPA Class 2 Financial classification |

Edit permission: PROJECT_DIRECTOR + PMO_DIRECTOR (audited via M13 audit log).

---

## BLOCK 4 — DATA POPULATION RULES

### 4a. Role × Action Permission Matrix

| Action | SYS_ADMIN | PMO_DIR | PORTFOLIO | PROJ_DIR | PLAN_ENG | QS_MGR | FIN_LEAD | PROC | SITE_MGR | COMP_MGR | ANALYST | READ_ONLY | EXT_AUDIT |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RAISE_CORRESPONDENCE | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| CLASSIFY_CORRESPONDENCE | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| FLAG_M05_TRIGGER (`triggers_m05 = true`) | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| RESPOND_TO_CORRESPONDENCE | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| ARCHIVE_CORRESPONDENCE | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| RAISE_NOTICE | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| OVERRIDE_NOTICE_SLA | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| ISSUE_SITE_INSTRUCTION | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| RAISE_RFI | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| RESPOND_TO_RFI | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| CLOSE_RFI | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| REOPEN_RFI | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| SCHEDULE_MEETING | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| DRAFT_MINUTES | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| CIRCULATE_MINUTES (Draft → Circulated) | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| APPROVE_MINUTES (Circulated → Approved) | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| DISPUTE_MINUTES (any role; transition Circulated → Disputed) | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| RESOLVE_DISPUTED_MINUTES | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| ADD_MINUTES_ENTRY | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| PROMOTE_RISK_NOTED_TO_M05 | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| CREATE_ACTION_ITEM (manual) | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| UPDATE_ACTION_ITEM_STATUS | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| ESCALATE_ACTION_ITEM_TO_M11 | SYSTEM | (retry-only) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| CREATE_TRANSMITTAL | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| ACKNOWLEDGE_DISTRIBUTION (recipient action) | ✅ (system) | ✅ (recipient) | ✅ (recipient) | ✅ (recipient) | ✅ (recipient) | ✅ (recipient) | ✅ (recipient) | ✅ (recipient) | ✅ (recipient) | ✅ (recipient) | ❌ | ❌ | ❌ |
| EDIT_PROJECT_CORRESPONDENCE_CONFIG | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| VIEW_CORRESPONDENCE_REGISTER | ✅ | ✅ | ✅ | ✅ (own) | ✅ (own) | ✅ (own) | ✅ (M05-linked) | ✅ (vendor) | ✅ (own) | ✅ (regulatory) | ✅ | ✅ (status only) | ✅ |
| VIEW_NOTICE_TRACKER | ✅ | ✅ | ✅ | ✅ (own) | ✅ (own) | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ |
| VIEW_MEETING_REGISTER | ✅ | ✅ | ✅ | ✅ (own) | ✅ (own) | ✅ (own) | ❌ | ❌ | ✅ (own) | ✅ (own) | ✅ | ✅ (header only) | ✅ |
| VIEW_MEETING_MINUTES | ✅ | ✅ | ✅ | ✅ (own) | ✅ (own attendees) | ✅ (own attendees) | ❌ | ❌ | ✅ (own attendees) | ✅ (own attendees) | ✅ | ❌ | ✅ |
| VIEW_ACTION_ITEMS | ✅ | ✅ | ✅ | ✅ (own) | ✅ (own assigned) | ✅ (own assigned) | ❌ | ✅ (own assigned) | ✅ (own assigned) | ✅ (own assigned) | ✅ | ❌ | ✅ |
| VIEW_RFI_REGISTER | ✅ | ✅ | ✅ | ✅ (own) | ✅ (own) | ✅ (own) | ❌ | ✅ (vendor) | ✅ (own) | ❌ | ✅ | ✅ (status only) | ✅ |
| VIEW_TRANSMITTAL_LOG | ✅ | ✅ | ✅ | ✅ (own) | ✅ (own) | ❌ | ❌ | ✅ (own) | ❌ | ❌ | ✅ | ❌ | ✅ |

**Critical permission rules:**
- **`triggers_m05` flag is RBAC-restricted.** Only PROJECT_DIRECTOR or PMO_DIRECTOR can set true (BR-13-009). System enforces; API rejects with 403 for other roles.
- **APPROVE_MINUTES is PROJECT_DIRECTOR or PMO_DIRECTOR only.** Not PLANNING_ENGINEER or QS_MANAGER (per BR-13-013).
- **ISSUE_SITE_INSTRUCTION is PROJECT_DIRECTOR or PMO_DIRECTOR only.** Site Instructions carry contractual weight; restricted to senior roles.
- **REOPEN_RFI is PMO_DIRECTOR only** (per BR-13-022).
- **PROMOTE_RISK_NOTED_TO_M05 is PROJECT_DIRECTOR or PMO_DIRECTOR only** (per BR-13-019); one-way promotion; not reversible.
- **ESCALATE_ACTION_ITEM_TO_M11 is SYSTEM-only** (BR-13-016 daily sweep); PMO_DIRECTOR has retry permission only on system error.
- **External roles** (CLIENT_VIEWER, LENDER_VIEWER, NABH_ASSESSOR, CONTRACTOR_LIMITED) — NO ACCESS in Phase 1 (gated by PF03 Phase 2).

### 4b. Required Fields on Creation

| Entity | Mandatory at Create |
|---|---|
| `Correspondence` | `project_id`, `direction`, `correspondence_type`, `contractual_weight`, `subject`, `body_summary`, `sent_date`; `contractual_reference` if type ∈ (Notice, Site_Instruction); `compliance_deadline` + `compliance_status` if type=Site_Instruction |
| `MeetingRegister` | `project_id`, `meeting_type`, `title`, `meeting_date`, `meeting_start_time`, `location`, `chairperson_user_id`, `agenda_text`, `minutes_status` (defaults to Draft) |
| `MinutesEntry` | `meeting_id`, `entry_seq`, `entry_type`, `entry_text` |
| `ActionItem` | `project_id`, `source`, `title`, `description`, `due_date`, `status` (defaults to Open); CHECK exactly-one-populated of `owner_user_id`/`owner_party_id` |
| `RFI` | `project_id`, `subject`, `question_text`, `raised_by_user_id` (or `raised_by_party_id`), `addressed_to`, `response_due_date` (auto-computed), `status` (defaults to Open) |
| `Transmittal` | `project_id`, `subject`, `transmittal_purpose`, `package_description`, `attachment_document_ids[]` (≥1), `sent_by_user_id`, `status` (defaults to Sent) |
| `DistributionList` | `parent_entity_type`, `parent_entity_id`; CHECK at least one of `recipient_user_id`/`recipient_party_id`/`recipient_email` |
| `ProjectCorrespondenceConfig` | `project_id` (1 row per project; auto-created with defaults at project Activation per BR-13-001) |

### 4c. Default Values + Seed Data

| Item | Default |
|---|---|
| `Correspondence.response_required` | Auto-true if `correspondence_type IN (Notice, RFI_Reference, Site_Instruction)` |
| `Correspondence.response_due_date` | Auto-computed from `sent_date + applicable_sla_days` per BR-13-007 |
| `Correspondence.triggers_m05` | Default false; only PROJECT_DIRECTOR / PMO_DIRECTOR can set true (BR-13-009) |
| `MeetingRegister.minutes_status` | Defaults to `Draft` |
| `ActionItem.status` | Defaults to `Open` |
| `RFI.status` | Defaults to `Open` |
| `RFI.response_due_date` | Auto = `raised_at_date + ProjectCorrespondenceConfig.rfi_sla_days` (default 14) |
| `Transmittal.status` | Defaults to `Sent` |
| `ProjectCorrespondenceConfig` | Auto-created at project Activation with all OQ-2.5 defaults (BR-13-001) |

**KDMC pilot seed data (HDI v0.1 prototype):**
- 1 ProjectCorrespondenceConfig row with default values
- 3 sample Correspondence rows: 1 Incoming Letter (info), 1 Outgoing Notice (response_required=true), 1 Site Instruction (compliance_deadline set)
- 1 sample MeetingRegister (Site_Progress type) with 5 MinutesEntry rows (1 Decision, 2 Action, 1 Discussion, 1 Risk_Noted)
- 2 sample RFIs (1 Open, 1 Responded)
- DistributionList rows for each Correspondence + Meeting + Transmittal seeded

---

## BLOCK 5 — FILTERS & VIEWS

### 5a. Correspondence Register View

**Default sort:** `response_due_date ASC NULLS LAST` (overdue items first), then `sent_date DESC`.

**Filters:**
- `direction` (multi-select)
- `correspondence_type` (multi-select)
- `contractual_weight` (multi-select)
- `response_status` (multi-select; default: Pending + Overdue)
- `triggers_m05` (boolean)
- `parent_correspondence_id` (thread root filter — show all rows in a thread)
- `sent_date` range
- `compliance_status` (for Site Instructions)

**Role-default views per X9 v0.5 §13.3.13 (added in this round's Deliverable B):**
- **PROJECT_DIRECTOR primary:** Notice tracker (own project; SLA-warning + breach highlighted); Meeting calendar secondary
- **PMO_DIRECTOR primary:** Notice SLA breach dashboard (across all projects); Open RFI count by project + average response time secondary
- **PORTFOLIO_MANAGER primary:** Portfolio correspondence volume + breach rate (table)
- **PLANNING_ENGINEER primary:** Open RFIs (own project; affected_milestones impact view); Pending action items (own assigned) secondary
- **QS_MANAGER primary:** Pending action items (own assigned) + meeting prep queue; Notices linking to VOs (M05 cross-link) secondary
- **SITE_MANAGER primary:** Daily inbound correspondence + RFI raise UI (own project); Today's meeting agenda secondary
- **FINANCE_LEAD primary:** Notices linking to commercial impact (M05+M06 cross-link)
- **PROCUREMENT_OFFICER primary:** Vendor correspondence + transmittals; Pending vendor RFIs secondary
- **COMPLIANCE_MANAGER primary:** Regulatory notices + responses; Notices linking to compliance items (M09 cross-link) secondary
- **ANALYST primary:** Correspondence trend (volume by type per month); RFI response-time trend secondary
- **READ_ONLY:** Correspondence card (status badges + counts; no detail body)
- **EXTERNAL_AUDITOR:** Full correspondence read + meeting minutes + RFI history; Distribution + acknowledgement audit trail secondary

### 5b. Notice Tracker View (sub-view filter on Correspondence)

**Auto-applied filter:** `correspondence_type = Notice` AND `contractual_weight IN (Formal_Notice, Contractual)`.

**Display:** correspondence_code, subject, sent_date, response_due_date, sla_status (Within/Warning/Breach with RAG colour), responded_at, response_status. Sortable by `sla_remaining_pct ASC`.

**Notice SLA Breach Funnel** (X9 §11 flagship pattern instance — to be confirmed during X9 v0.5 audit pass): `Within → Warning (≥80%) → Breach (≥100%)` count + cumulative cost-of-delay-days.

### 5c. Meeting Register View

**Filters:** `meeting_type` (multi-select), `meeting_date` range, attendee (user_id or party_id), `minutes_status` (multi-select), chairperson_user_id.

### 5d. Action Item View

**Default sort:** `due_date ASC` (overdue flagged RED).

**Filters:** `status` (multi-select), `source` (multi-select), `owner_user_id`, `owner_party_id`, `due_date` range, `escalated_to_m11` (boolean).

**Per-role default:** PLANNING_ENGINEER + QS_MANAGER + SITE_MANAGER see "own assigned" by default (filter `owner_user_id = current_user_id`); PMO_DIRECTOR sees portfolio view.

### 5e. RFI Register View

**Filters:** `status` (multi-select), `design_impact`/`cost_impact`/`schedule_impact` flags, `raised_at` date range, `responded_by_user_id`.

### 5f. Transmittal Log View

**Filters:** `transmittal_purpose`, `status`, `sent_at` date range.

### 5g. Distribution + Acknowledgement Audit View

**Role:** EXTERNAL_AUDITOR primary; PMO_DIRECTOR secondary.

**Display:** Correspondence/Meeting/Transmittal → recipient list → received_at + acknowledged_at + acknowledgement_method timeline. Used for legal-evidence reconstruction.

---

## BLOCK 6 — BUSINESS RULES

24 BRs — `BR-13-001` through `BR-13-024`. Format: `BR-XX-YYY | Trigger | Rule | Result | Speed Tier`.

### 6a. Project Activation + Configuration

| BR | Trigger | Rule | Result | Speed |
|---|---|---|---|---|
| BR-13-001 | M01 Project Activation event | Auto-create `ProjectCorrespondenceConfig` row with OQ-2.5 defaults (notice_sla_warning_pct=0.80, rfi_sla_days=14, acknowledgement_timeout_days=7, meeting_minutes_circulation_hours=48, correspondence_retention_years=7); emit `PROJECT_CORRESPONDENCE_INITIALISED` audit event | Row persisted | 🔴 Real-time |

### 6b. Correspondence Lifecycle + Notice SLA

| BR | Trigger | Rule | Result | Speed |
|---|---|---|---|---|
| BR-13-002 | `Correspondence.create` where `correspondence_type IN (Notice, Site_Instruction)` | `contractual_reference` MUST be populated; ≥ 50 chars (clause text or contract section reference) | Block save otherwise | 🔴 Real-time |
| BR-13-003 | `Correspondence.create` where `correspondence_type = Site_Instruction` | `compliance_deadline` MUST be populated; `compliance_status` defaults to Pending | Block save otherwise | 🔴 Real-time |
| BR-13-004 | `Correspondence.create` | If `correspondence_type IN (Notice, RFI_Reference, Site_Instruction)`: auto-set `response_required = true` | Persist | 🔴 Real-time |
| BR-13-005 | `Correspondence.response_required = true` | `response_due_date` MUST be populated; auto-computed from `sent_date + applicable_sla_days` (per correspondence_type lookup; defaults from `M01.Contract` if specified, else from `ProjectCorrespondenceConfig`) | Block save otherwise | 🔴 Real-time |
| BR-13-006 | Daily Notice SLA sweep (🟢 24hr batch) | For each Correspondence with `response_required = true` AND `response_status = Pending` AND `correspondence_type = Notice` AND `contractual_weight IN (Formal_Notice, Contractual)`: compute `sla_remaining_pct = (response_due_date - today) / total_sla_days`. If 80% threshold crossed (sla_remaining_pct ≤ 0.20 = 80% elapsed): emit `NOTICE_SLA_WARNING` Decision Queue trigger to recipient (or PROJECT_DIRECTOR if external) per OQ-2.3; create `NoticeSLAEvent` row | DQ trigger raised; row persisted | 🟢 24hr (sweep emits 🔴) |
| BR-13-007 | Daily Notice SLA sweep | If `response_due_date < today` AND `response_status = Pending`: set `response_status = Overdue`; emit `NOTICE_SLA_BREACH` Decision Queue trigger High to PROJECT_DIRECTOR (24hr SLA to acknowledge); create `NoticeSLAEvent` row | DQ trigger raised; status updated | 🟢 24hr |
| BR-13-008 | `Correspondence.respond` action | `responded_via_correspondence_id` MUST point to a Correspondence with opposite `direction` AND same `parent_correspondence_id` (or this row as the parent); `responded_at` + `responded_by_user_id` auto-set; `response_status = Responded` | Persist | 🔴 Real-time |

### 6c. M05 Trigger + Risk Promotion

| BR | Trigger | Rule | Result | Speed |
|---|---|---|---|---|
| BR-13-009 | `Correspondence.triggers_m05 = true` write | Caller MUST be PROJECT_DIRECTOR or PMO_DIRECTOR. UI fields blocked for other roles; API rejects with 403 | Block write otherwise | 🔴 Real-time |
| BR-13-010 | `Correspondence.triggers_m05 = true` set | Emit `CORRESPONDENCE_M05_FLAGGED` event to M05 internal API with full Correspondence payload (correspondence_id, project_id, correspondence_type, contractual_weight, subject, m05_trigger_reason, sent_date); M05 evaluates whether to open EWN/VO/EOT (M05 owns the decision) | Event emitted; M05 acknowledges | 🔴 Real-time |
| BR-13-011 | `MinutesEntry` where `entry_type = Risk_Noted` and PMO/PROJECT_DIRECTOR triggers PROMOTE_RISK_NOTED_TO_M05 action | Create `M05.Risk` row with category derived from MinutesEntry text + RAISE_RISK action; populate `MinutesEntry.promoted_to_m05_risk_id`; promotion is one-way (not reversible). Emit `RISK_PROMOTED_FROM_MINUTES` audit event | Persist; M05.Risk created | 🔴 Real-time |
| BR-13-012 | `RFI.cost_impact = true OR schedule_impact = true` | Emit `RFI_IMPACT_FLAGGED` event to M05 internal API for assessment (M05 may open EWN/VO based on review) | Event emitted | 🔴 Real-time |

### 6d. Meeting + Minutes

| BR | Trigger | Rule | Result | Speed |
|---|---|---|---|---|
| BR-13-013 | `MeetingRegister.minutes_status → Approved` | Caller MUST be PMO_DIRECTOR or PROJECT_DIRECTOR; ALL `MinutesEntry` rows with `entry_type = Action` MUST have `action_item_id` populated (auto-created per BR-13-014); `minutes_approved_at` + `minutes_approved_by_user_id` auto-set | Block transition otherwise; emit `MEETING_MINUTES_APPROVED` | 🔴 Real-time |
| BR-13-014 | `MinutesEntry.create` where `entry_type = Action` | Auto-create `ActionItem` row with `source = Meeting`, `source_meeting_id = parent_meeting`, `source_minutes_entry_id = this`, `description = entry_text`; populate `MinutesEntry.action_item_id` | Both rows persisted | 🔴 Real-time |
| BR-13-015 | `MeetingRegister.minutes_status → Disputed` | `minutes_dispute_note` MUST be populated, ≥ 100 chars; emit `MEETING_MINUTES_DISPUTED` Decision Queue trigger Medium to PMO_DIRECTOR (48hr SLA to resolve); minutes cannot transition to Approved until dispute resolved by PMO override | Block save otherwise; DQ trigger raised | 🔴 Real-time |
| BR-13-016 | Daily ActionItem SLA sweep (🟢 24hr batch) | For each ActionItem with `status IN (Open, In_Progress)` AND `due_date < today`: set `status = Overdue` (if not already), set `escalated_to_m11 = true`, emit `ACTION_ITEM_OVERDUE` Decision Queue trigger Medium → escalating to High after 7 days | DQ trigger raised | 🟢 24hr |
| BR-13-017 | `MeetingRegister.minutes_circulated_at` not set within `ProjectCorrespondenceConfig.meeting_minutes_circulation_hours` (default 48) of `meeting_end_time` | Emit `MEETING_MINUTES_NOT_CIRCULATED` Decision Queue trigger Low to chairperson (24hr SLA) | DQ trigger raised | 🟢 24hr |

### 6e. RFI Lifecycle

| BR | Trigger | Rule | Result | Speed |
|---|---|---|---|---|
| BR-13-018 | `RFI.create` | `response_due_date` auto-computed = `raised_at_date + ProjectCorrespondenceConfig.rfi_sla_days` (default 14) | Persist | 🔴 Real-time |
| BR-13-019 | `RFI.status → Responded` | `response_text` MUST be populated, ≥ 50 chars; `responded_at` + `responded_by_user_id` auto-set | Block transition otherwise | 🔴 Real-time |
| BR-13-020 | Daily RFI SLA sweep (🟢 24hr batch) | For each RFI with `status = Open` AND `response_due_date < today`: set `status = Overdue`; emit `RFI_RESPONSE_OVERDUE` Decision Queue trigger Medium to PROJECT_DIRECTOR + PLANNING_ENGINEER (48hr SLA) | DQ trigger raised | 🟢 24hr |
| BR-13-021 | `RFI.status = Closed` reopen attempt | Caller MUST be PMO_DIRECTOR (per Block 4a REOPEN_RFI permission); audited via RFIStatusLog | Block reopen otherwise | 🔴 Real-time |

### 6f. Site Instruction Compliance

| BR | Trigger | Rule | Result | Speed |
|---|---|---|---|---|
| BR-13-022 | Daily Site Instruction sweep (🟢 24hr batch) | For each Correspondence with `correspondence_type = Site_Instruction` AND `compliance_status IN (Pending, In_Progress)` AND `compliance_deadline < today`: set `compliance_status = Non_Complied`; emit `SITE_INSTRUCTION_NON_COMPLIED` Decision Queue trigger High to PROJECT_DIRECTOR + PMO_DIRECTOR; emit cross-module event to M05 internal API for potential NCR-basis assessment | Status updated; both triggers raised | 🟢 24hr |

### 6g. Distribution + Acknowledgement

| BR | Trigger | Rule | Result | Speed |
|---|---|---|---|---|
| BR-13-023 | Distribution sent (Correspondence/Meeting/Transmittal/RFI created with DistributionList rows) | For each DistributionList row: emit `DISTRIBUTION_SENT` audit event; daily acknowledgement sweep checks (BR-13-024) | Events emitted | 🔴 Real-time |
| BR-13-024 | Daily Acknowledgement sweep (🟢 24hr batch) | For each DistributionList row with `received_at IS NOT NULL` AND `acknowledged_at IS NULL` AND `received_at + acknowledgement_timeout_days < today`: emit `ACKNOWLEDGEMENT_OVERDUE` Decision Queue trigger Medium to PROJECT_DIRECTOR (24hr SLA to chase recipient) | DQ trigger raised | 🟢 24hr |

---

## BLOCK 7 — INTEGRATION POINTS

### 7a. RECEIVES FROM

| From | Data | Trigger | Speed | Failure Handling |
|---|---|---|---|---|
| M01 | `Project.id`, `Contract.id`, `Party` (recipient identities for Correspondence + DistributionList), `Contract.notice_sla_default_days` (per-contract notice SLA tunables; defaults to ProjectCorrespondenceConfig if unspecified) | On Project Activation + Contract edit | 🔴 Real-time | If M01 Contract not yet Activated: block M13 entity create with reason `M01_CONTRACT_NOT_ACTIVATED` |
| M03 | `Milestone` IDs (for RFI.affected_milestones[] + MinutesEntry.referenced_milestone_id selection; read via M03 internal API) | On RFI raise + MinutesEntry create | 🔴 Real-time | — |
| M04 | `ConstructionNCR.id` reference (cross-link from Correspondence with `correspondence_type = Site_Instruction` and `m04_ncr_id` populated; read-only — M04 owns NCR row) | On Site Instruction create where remediating an NCR | 🔴 Real-time (read) | — |
| M12 DocumentControl (when built) | `document_id` allocation requests for attachments; M13 holds metadata, M12 holds blobs | On attachment upload (during M12-stub interim, MinIO direct URL stored in `document_id` field) | 🔴 Real-time | If M12 unavailable: M13 stores MinIO direct URL with stub flag; migration script in Spec Appendix C executes when M12 lands |
| M34 | Auth, role, project scope, MFA gate | Every API call | 🔴 Real-time | Standard auth flow |
| M11 ActionRegister (when built) | ActionItem status update back-events (when M11 marks closed) | On owner action via M11 UI | 🔴 Real-time | M11 stub interim; events queue locally |

### 7b. SENDS TO

| To | Data | Trigger | Speed | Failure Handling |
|---|---|---|---|---|
| **M05 RiskChangeControl** | `CORRESPONDENCE_M05_FLAGGED` event payload (correspondence_id, project_id, correspondence_type, contractual_weight, subject, m05_trigger_reason, sent_date) → M05 evaluates whether to open EWN/VO/EOT (per BR-13-010) | On `Correspondence.triggers_m05 → true` (BR-13-009 RBAC-restricted) | 🔴 Real-time | M05 batch partner (R33 Spec); if M05 internal API unavailable: M13 retries with exponential backoff |
| **M05** | `RFI_IMPACT_FLAGGED` event (rfi_id, project_id, cost_impact, schedule_impact, design_impact) → M05 reviews for potential EWN/VO (per BR-13-012) | On `RFI.cost_impact = true OR schedule_impact = true` | 🔴 Real-time | Same retry pattern |
| M05 | Cross-module event to M05 for SITE_INSTRUCTION_NON_COMPLIED (potential NCR-basis assessment per BR-13-022) | On Site Instruction non-compliance | 🟢 24hr (sweep emits 🔴) | — |
| **M11 ActionRegister** (when built) | ActionItem payload (action_id, project_id, source, source_meeting_id OR source_correspondence_id OR source_rfi_id, owner_user_id OR owner_party_id, due_date, severity); plus 7 Decision Queue trigger types (Block 8c) | On MinutesEntry type=Action create (BR-13-014) OR Notice/RFI/Action SLA threshold crossed (BR-13-006/007/016/020/022) | 🔴 / 🟡 / 🟢 per trigger | M11 stub interim; events queue locally until M11 lands |
| **M12 DocumentControl** (when built) | `DOCUMENT_REFERENCE_CREATE` event (m13_entity_type, m13_entity_id, document_id allocation request); M13 holds reference, M12 holds blob | On attachment upload | 🔴 Real-time | M12-stub interim |
| M03 PlanningMilestones | (read-only via M03 internal API; no events emitted to M03) | — | — | — |
| M09 ComplianceTracker (when built) | Cross-link of Correspondence with `correspondence_type = Regulatory` | On Regulatory correspondence create | 🔴 Real-time | M09 stub interim |
| M19 ClaimsManagement (Phase 2) | Full correspondence chain export for formal claim packets (M13 emits chain on request; M19 absorbs) | On request (Phase 2) | 🟡 1hr cache | — |
| PF03 ExternalPartyPortal (Phase 2) | Scoped read access to Correspondence + DistributionList (acknowledgement UI) per recipient party_id scope | On request (Phase 2) | — | — |

### 7c. Forward Constraints (forward to unbuilt modules)

Per CLAUDE.md §4 Carry-Forward + Brief §10 + this Spec:

| Module | Constraint Imposed by M13 v1.0 |
|---|---|
| **M11 ActionRegister** (R60 Spec) | MUST consume M13 ActionItem emit + 7 Decision Queue trigger types (NOTICE_SLA_WARNING, NOTICE_SLA_BREACH, ACTION_ITEM_OVERDUE, MEETING_MINUTES_NOT_CIRCULATED, MEETING_MINUTES_DISPUTED, RFI_RESPONSE_OVERDUE, SITE_INSTRUCTION_NON_COMPLIED, ACKNOWLEDGEMENT_OVERDUE — total 8 effective; 7 listed in Block 8c plus ACKNOWLEDGEMENT_OVERDUE per BR-13-024). M11 owns SLA escalation; M13 emits triggers |
| **M12 DocumentControl** (future round) | MUST accept M13 `document_id` allocation requests; provide blob storage; support M13 attachment patterns (Correspondence + RFI + Transmittal + MinutesEntry) |
| **M05 RiskChangeControl** | Already-locked (R33 Spec): M05 receives `CORRESPONDENCE_M05_FLAGGED` + `RFI_IMPACT_FLAGGED` + Site_Instruction non-compliance events. M05 owns commercial deliberation |
| **M09 ComplianceTracker** (future round) | MUST consume M13 regulatory notices + responses for compliance evidence |
| **M19 ClaimsManagement** (Phase 2) | Correspondence chain export for formal claim packets (M13 emits chain; M19 absorbs into claim documentation) |
| **PF03 ExternalPartyPortal** (Phase 2) | When built: external roles get scoped read access to Correspondence + DistributionList per their party_id scope |

---

## BLOCK 8 — GOVERNANCE & AUDIT

### 8a. Permission Reference

(Reference Block 4a Role × Action Permission Matrix.)

### 8b. Audit Event Catalogue (M13-owned, locked from authoring per OQ-2.1)

24 events across 7 sections. All events: append-only, 7-year retention (correspondence_retention_years default in ProjectCorrespondenceConfig; aligns with Companies Act + DPDPA Class 2 Financial classification).

| # | Event | Trigger BR | Severity |
|---|---|---|---|
| **§A.1 Correspondence events** | | | |
| 1 | `CORRESPONDENCE_CREATED` | BR-13-002..005 | Info |
| 2 | `CORRESPONDENCE_CLASSIFIED` | (type/contractual_weight change) | Info |
| 3 | `CORRESPONDENCE_SENT` | (outgoing transmission timestamp) | Info |
| 4 | `CORRESPONDENCE_RESPONDED` | BR-13-008 | Info |
| 5 | `CORRESPONDENCE_M05_FLAGGED` | BR-13-009 + BR-13-010 | High |
| 6 | `CORRESPONDENCE_ARCHIVED` | (soft-delete) | Info |
| **§A.2 Notice events** | | | |
| 7 | `NOTICE_SLA_WARNING` | BR-13-006 | Medium |
| 8 | `NOTICE_SLA_BREACH` | BR-13-007 | High |
| 9 | `NOTICE_SLA_OVERDUE_RESOLVED` | (responded after breach) | Info |
| **§A.3 Meeting events** | | | |
| 10 | `MEETING_SCHEDULED` | (MeetingRegister.create) | Info |
| 11 | `MEETING_HELD` | (meeting_end_time recorded) | Info |
| 12 | `MINUTES_DRAFTED` | (status → Draft in progress) | Info |
| 13 | `MINUTES_CIRCULATED` | (status → Circulated) | Info |
| 14 | `MEETING_MINUTES_APPROVED` | BR-13-013 | Info |
| 15 | `MEETING_MINUTES_DISPUTED` | BR-13-015 | Medium |
| 16 | `MINUTES_ENTRY_ADDED` | (MinutesEntry.create) | Info |
| 17 | `RISK_PROMOTED_FROM_MINUTES` | BR-13-011 | Medium |
| **§A.4 ActionItem events** | | | |
| 18 | `ACTION_ITEM_CREATED` | BR-13-014 | Info |
| 19 | `ACTION_ITEM_OWNER_NOTIFIED` | (post-create) | Info |
| 20 | `ACTION_ITEM_OVERDUE` | BR-13-016 | Medium → High escalating |
| **§A.5 RFI events** | | | |
| 21 | `RFI_RAISED` | BR-13-018 | Info |
| 22 | `RFI_RESPONDED` | BR-13-019 | Info |
| 23 | `RFI_CLOSED` | (status → Closed) | Info |
| 24 | `RFI_RESPONSE_OVERDUE` | BR-13-020 | Medium |
| 25 | `RFI_IMPACT_FLAGGED` | BR-13-012 | High |
| **§A.6 Site Instruction events** | | | |
| 26 | `SITE_INSTRUCTION_NON_COMPLIED` | BR-13-022 | High |
| **§A.7 Distribution + Acknowledgement events** | | | |
| 27 | `DISTRIBUTION_SENT` | BR-13-023 | Info |
| 28 | `ACKNOWLEDGEMENT_RECORDED` | (recipient acknowledges) | Info |
| 29 | `ACKNOWLEDGEMENT_OVERDUE` | BR-13-024 | Medium |

**Total: 29 events** (Brief estimated 22-26; refined to 29 during authoring with §A.5 RFI sub-events explicit).

### 8c. Decision Queue Trigger Catalogue (7 triggers per Brief OQ-2.3 + 1 added during authoring = 8 total)

All triggers UPPER_SNAKE_CASE per `naming-folders.md`. Registered with M11 ActionRegister (when built).

| # | Trigger | Severity | Owner | SLA | Source BR |
|---|---|---|---|---|---|
| 1 | `NOTICE_SLA_WARNING` (80% of response window elapsed) | Medium | Recipient (owner_user_id or PROJECT_DIRECTOR if external) | per remaining window | BR-13-006 |
| 2 | `NOTICE_SLA_BREACH` (100% breached) | High | PROJECT_DIRECTOR | 24 hr | BR-13-007 |
| 3 | `RFI_RESPONSE_OVERDUE` (RFI Open > rfi_sla_days) | Medium | PROJECT_DIRECTOR + PLANNING_ENGINEER | 48 hr | BR-13-020 |
| 4 | `MEETING_MINUTES_NOT_CIRCULATED` (Meeting end + 48hr without circulated minutes) | Low | Meeting chair (chairperson_user_id) | 24 hr | BR-13-017 |
| 5 | `ACTION_ITEM_OVERDUE` (action item due_date past, status not Closed) | Medium → High escalating | ActionItem.owner_user_id or PROJECT_DIRECTOR | per overdue duration | BR-13-016 |
| 6 | `MEETING_MINUTES_DISPUTED` (minutes_status = Disputed) | Medium | PMO_DIRECTOR | 48 hr | BR-13-015 |
| 7 | `SITE_INSTRUCTION_NON_COMPLIED` (compliance_status auto-set to Non_Complied past deadline) | High | PROJECT_DIRECTOR + PMO_DIRECTOR | 24 hr | BR-13-022 |
| 8 | `ACKNOWLEDGEMENT_OVERDUE` (Distribution sent + acknowledgement_timeout_days without recipient acknowledgement) | Medium | PROJECT_DIRECTOR | 24 hr | BR-13-024 |

### 8d. Speed Tier Defaults (per OQ-2.4)

| Event class | Speed tier |
|---|---|
| Correspondence create / classify / send | 🔴 Real-time |
| Notice SLA threshold crossed (any) | 🔴 Real-time (sweep emits 🔴; sweep schedule 🟢 24hr) |
| RFI create / respond / close | 🔴 Real-time |
| Meeting minutes save / line-item add / approve / dispute | 🔴 Real-time |
| ActionItem create (from MinutesEntry) | 🔴 Real-time |
| ActionItem owner notification | 🔴 Real-time |
| Daily Notice SLA sweep | 🟢 24 hr |
| Daily RFI SLA sweep | 🟢 24 hr |
| Daily ActionItem SLA sweep | 🟢 24 hr |
| Daily Site Instruction compliance sweep | 🟢 24 hr |
| Daily Acknowledgement timeout sweep | 🟢 24 hr |
| Correspondence volume trend recompute (ANALYST view) | 🟢 24 hr |

### 8e. DPDPA 2023 Data Classification

Per `ZEPCC_Legacy/EPCC_Standards_Memory_v5_3.md` §7.128 (ES-SEC-004):

| M13 Field Class | Examples | Treatment |
|---|---|---|
| Class 1 — PERSONAL | `recipient_user_id`, `recipient_email`, `sender_user_id`, `responded_by_user_id`, etc. (FK references; user PII lives in M34) | Standard — M34 owns PII; M13 only stores UUID FK. Free-text `recipient_email` MUST be encrypted at column level. |
| Class 2 — FINANCIAL | (none directly in M13; cross-links to M05/M06 financial entities are read-only references) | Standard treatment via cross-module references |
| Class 3 — OPERATIONAL | `correspondence_type`, `contractual_weight`, `response_status`, `meeting_type`, `minutes_status`, all dates, all status fields | Table-level TDE (default); 7-year retention per Companies Act |

---

## BLOCK 9 — EXPLICIT EXCLUSIONS

(See Block 2b for full list. Restated here for spec discipline.)

| # | Excluded | Reason | Where Addressed |
|---|---|---|---|
| 1 | Document storage (file blobs) | Single-owner: M12 owns blob layer; M13 stores `document_id` references only | M12 |
| 2 | Variation Order + EOT processing | Single-owner: M05 owns commercial deliberation; M13 emits trigger events | M05 |
| 3 | ActionItem SLA enforcement / Decision Queue routing | Single-owner: M11 owns SLA escalation; M13 emits triggers | M11 |
| 4 | Long-form claims documentation | M19 ClaimsManagement Phase 2 | M19 |
| 5 | Site daily diary (free-text day log) | M16 SiteDiary (separate Phase 1 module) | M16 |
| 6 | Email integration / IMAP ingestion | Phase 2 (manual entry only in v1.0) | Phase 2 |
| 7 | Speech-to-text meeting minutes | Phase 2 | Phase 2 |
| 8 | Document review workflows (approval routing, redlining) | M12 owns when built | M12 |
| 9 | External-party portal access | PF03 ExternalPartyPortal Phase 2 | PF03 |
| 10 | Drawing and submittal management | M12 (drawings) + future module M27 DesignControl | M12 + M27 |
| 11 | Procurement-specific correspondence flows | M30 VendorMasterPQ + M29 TenderingAward (Phase 2) | M30 + M29 |
| 12 | Legal proceedings and dispute management | M19 Phase 2 | M19 |
| 13 | Regulatory compliance enforcement | M09 ComplianceTracker; M13 captures regulatory notices but doesn't enforce compliance | M09 |
| 14 | Hard-delete of correspondence rows | Soft-delete only via `is_active = false`; per BR-13-018 evidence-integrity discipline | This Spec |

---

## BLOCK 10 — OPEN QUESTIONS

### 10a. OQ-1 Status (per Brief v1.0, all CLOSED)

| OQ-1 | Topic | Locked Answer | Where Embedded |
|---|---|---|---|
| 1.1 | Module scope decomposition | B (LOCKED) — Slim core; document storage→M12; action SLA→M11; commercial deliberation→M05; site diary→M16 | Block 2a + 2b |
| 1.2 | Notice SLA enforcement model | B (LOCKED) — Tiered escalation (50%/80%/100%) | BR-13-006/007 |
| 1.3 | Correspondence direction model | A (LOCKED) — Single Correspondence entity with direction ENUM | Block 3b.1 (single entity covers Site Instructions via correspondence_type=Site_Instruction) |
| 1.4 | Meeting minutes structure | B (LOCKED) — Structured MinutesEntry line-items | Block 3b.6 + BR-13-014 |
| 1.5 | Action item ownership model | C (LOCKED) — User OR Party FK with CHECK exactly-one-populated | Block 3b.8 (CHECK constraint) |
| 1.6 | RFI scope + lifecycle | A (LOCKED) — M13 metadata + M12 attachments | Block 3b.9 + Block 7a (M12 receive) |
| 1.7 | Distribution & acknowledgement | A (LOCKED) — Explicit DistributionList with acknowledgement audit | Block 3b.12 + BR-13-023/024 |
| 1.8 | Role-default views per X9 v0.4 §13.3 | Locked mapping (deferred to X9 v0.5 cascade — Deliverable B of this round, §13.3.13) | Block 5a |

### 10b. OQ-2 Status (per Brief v1.0, all CLOSED)

| OQ-2 | Topic | Locked Answer | Where Embedded |
|---|---|---|---|
| 2.1 | Audit event naming discipline | CLOSED — Lock event names in Brief Appendix A | Block 8b (29 events catalogued) |
| 2.2 | Append-only ledgers | CLOSED — 5 entities (CorrespondenceStatusLog, NoticeSLAEvent, MeetingMinutesAuditLog, RFIStatusLog, DistributionList) | Block 3a (column "Append-Only?") |
| 2.3 | Decision Queue SLA defaults | CLOSED — 8 triggers (Brief estimated 7; +1 ACKNOWLEDGEMENT_OVERDUE added during authoring) | Block 8c |
| 2.4 | Speed tier defaults | CLOSED — 12 event classes mapped | Block 8d |
| 2.5 | ProjectCorrespondenceConfig entity | CLOSED — 5 fields (notice_sla_warning_pct, rfi_sla_days, acknowledgement_timeout_days, meeting_minutes_circulation_hours, correspondence_retention_years) | Block 3b.13 |

### 10c. Open Questions Surfaced During Authoring

**None.** All questions encountered during this Spec authoring resolved via Brief v1.0 / CLAUDE.md / parent module Specs / R33 M05 batch partner Spec. Block 10 closes at zero per spec-protocol.md §10-Block Spec Template lock rule.

**Zero open questions. M13 CorrespondenceMeetingRegister ready for Round 34 lock.**

---

*v1.0 — Spec LOCKED 2026-05-04 (Round 34). M05 + M13 batch ready for Round 35 (Wireframes; C1b batch) + Round 36 (Workflows; C1b batch) per Build Execution Plan §3a.*
