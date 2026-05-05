# M13 — Correspondence & Meeting Register — Brief v1.0

**Artefact:** M13_CorrespondenceMeetingRegister_Brief_v1_0
**Round:** 32
**Date:** 2026-05-04
**Author:** Monish (with Claude assist)
**Status:** LOCKED
**Last Updated:** 2026-05-04
**Last Audited:** v1.0 on 2026-05-04
**Reference Standards:** X8_GlossaryENUMs_v0_6a.md, X9_VisualisationStandards_Spec_v0_4.md, M34_SystemAdminRBAC_Spec_v1_0a.md, M01_ProjectRegistry_Spec_v1_0a.md (+ v1_1/v1_2/v1_3/v1_4 cascade notes), M02_StructureWBS_Spec_v1_0a.md (+ v1_1 cascade note), M03_PlanningMilestones_Spec_v1_1b.md (+ v1_2/v1_3 cascade notes), M04_ExecutionCapture_Spec_v1_0a.md, M05_RiskChangeControl_Brief_v1_0.md (C1b batch partner), M06_FinancialControl_Spec_v1_0b.md (+ v1_1 cascade note)
**Layer:** L2 Execution — Document & Communication Control
**Phase:** 1 — Foundational (gates M11 ActionRegister; consumed by M05/M19)
**Build Priority:** 🟠 High (precedes M11 deepening; peer of M05; consumed by M19 Phase 2)
**Folder:** SystemAdmin/Modules/
**C1b Batch Partner:** M05 RiskChangeControl (peer module, same layer, no upstream→downstream dependency)

---

## 1. Purpose

M13 is the **system-of-record for project communications**. It captures every formal letter, instruction, RFI, meeting minute, and action item across the project lifecycle — and tracks contractual response obligations against time-bound clauses.

In Indian EPC delivery, communications are evidence. Notice timelines (NEC4 Clause 8.4, FIDIC Clause 1.3), instructions (FIDIC 3.5), and meeting minutes are routinely the determinative artefacts in disputes, claims, and arbitration. M05 RiskChangeControl deliberates on commercial consequence; M11 ActionRegister tracks open items; **M13 is where the paper trail lives.**

**Decision M13 enables:** *"Are all formal communications — letters, instructions, meeting minutes, action items — captured, tracked, responded to within contractual timelines, and available as an auditable record for claims, disputes, and governance?"*

### Sub-questions M13 answers

- Has every incoming letter been registered with received date + classification (information / instruction / notice / claim)?
- Is the response window for this notice tracking against contractual SLA (e.g., 14 days for RFI, 7 days for early-warning acknowledgement)?
- For every meeting (kick-off, weekly progress, technical review, contractual review), are minutes captured + circulated + acknowledged?
- Does this correspondence trigger an M05 commercial deliberation (VO claim, EOT claim, Early Warning Notice)?
- Is this action item from yesterday's meeting in M11 ActionRegister, with an owner + due date?
- For arbitration / dispute reconstruction: can we produce the full correspondence chain on Request X within minutes?

## 2. Scope (this round)

This Brief surfaces **8 OQ-1 architectural decisions** and **5 OQ-2 pattern defaults** that the M13 Spec (Round 34) will rest on. **All 13 are CLOSED** in this Brief — Spec can be authored without re-opening.

**In scope:**

- **CorrespondenceRegister** — incoming + outgoing formal communications (letters, emails, faxes, transmittals); classification by type (Information / Instruction / Notice / Claim / Approval) and contractual reference
- **NoticeTracker** — contractual notices with explicit response SLA (e.g., NEC4 8.4 Early Warning, FIDIC 20.1 Claim Notification); notice-to-response time tracking; auto-escalation on SLA breach
- **MeetingRegister** — meeting types (Kick-off / Progress / Technical / Contractual / DRB), agenda, attendees (from M01 Party + M34 User), minutes, distribution list
- **MinutesEntry** — line-item entries within a meeting's minutes (decision / action / discussion / risk-noted)
- **ActionItem** — meeting-derived actionable tasks; owner (M34 User) + due date + status; **fed to M11 ActionRegister Decision Queue**
- **RFI (Request For Information)** — formal RFI lifecycle (Open → Responded → Closed); SLA-bound; bidirectional with M12 (when built — M12 owns the document attachments)
- **Transmittal** — outgoing formal package transmissions (drawings, specifications, BOQ revisions); receipt-acknowledgement tracking
- **Document linkages** — every Correspondence / Notice / Minute / RFI / Transmittal entity carries `document_id` FK to M12 (when built; M12-stub pattern matching M04 photo stub during interim)

**Explicitly NOT in scope (decided OQ-1.1 = B):**

- **Document storage internals (file blobs, version control, watermarking, redlines)** → M12 DocumentControl owns. M13 stores `document_id` references; M12 owns the BLOB layer.
- **Commercial deliberation on correspondence (does this letter trigger a VO?)** → M05 RiskChangeControl. M13 captures faithfully; M05 decides commercial consequence.
- **Action item SLA enforcement / Decision Queue routing** → M11 ActionRegister. M13 emits action items; M11 owns the queue.
- **Site diary daily log** → M16 SiteDiary (Phase 1 separate module).
- **External-party portal access (client / lender / auditor view of correspondence)** → PF03 ExternalPartyPortal Phase 2.
- **Email integration / IMAP ingestion** → Phase 2 (manual entry only in v1.0; ingestion automation deferred until volume justifies).
- **Speech-to-text meeting minutes** → Phase 2.
- **Document review workflows (approval routing, redlining)** → M12 owns when built.

## 3. Prior Art

**Legacy reference:** No M13 spec in `ZEPCC_Legacy/`. M13 is a NEW module (no v2.x predecessor). Closest legacy concept = the "communications register" implicit in M05 v2.3 bundled scope; this Brief extracts it into a single-owner module per F-005.

### Drift from informal practice

| Informal practice | This Brief (v1.0) | Why |
|---|---|---|
| Project email folders + Excel correspondence log | First-class entities (CorrespondenceRegister, NoticeTracker, etc.) | Anti-drift; system-of-record discipline |
| Meeting minutes in DOCX files emailed around | MeetingRegister entity + MinutesEntry rows + distribution acknowledgement | Searchable; linkable to actions/notices/risks |
| Actions noted in minutes, tracked manually | ActionItem entity emitted to M11 ActionRegister Decision Queue | SLA enforcement; mechanical visibility |
| RFIs in a spreadsheet | RFI entity with SLA timer, integration to M12 (documents) + M03 (schedule impact via affected_milestones) | Contract-clause traceability |
| Transmittals on paper | Transmittal entity with receipt-acknowledgement tracking | Dispute-defensible |

---

## 4. OQ-1 — Design Decisions Required From User

> All 8 decisions are **CLOSED** in this Brief. M13 Spec (Round 34) references these by ID without re-opening.

### OQ-1.1 — Module scope decomposition

**Question:** What does M13 include, and what stays with adjacent modules?

**Options:**
- A. M13 owns correspondence + notices + meetings + actions + RFIs + transmittals + document workflows (broad scope)
- B. **M13 owns correspondence + notices + meetings + actions + RFIs + transmittals; document storage to M12; action SLA to M11; commercial deliberation to M05** (slim core; single-owner discipline)
- C. M13 + integrate site diary (M16 absorbed into M13)

**Resolution:** **B (LOCKED).** Single-owner discipline (F-005). M13 is the registry / paper-trail layer; M12 owns blobs; M11 owns action SLAs; M05 owns commercial deliberation; M16 owns daily site diary (different cadence — daily entries vs event-driven correspondence). Mirrors M04/M05 OQ-1.1 = B precedent (slim core).

**Cascade impact:**
- M12 DocumentControl Brief (future round) absorbs document storage; M13 stores `document_id` FK only
- M11 ActionRegister Brief (R58) consumes M13 ActionItem emit
- M16 SiteDiary remains independent (Phase 1)

**Status:** CLOSED

---

### OQ-1.2 — Notice SLA enforcement model

**Question:** How does M13 enforce contractual notice response SLAs?

**Options:**
- A. M13 calculates SLA-due-date; UI shows alongside list (passive — no auto-escalation)
- B. **M13 calculates SLA-due-date + emits Decision Queue triggers to M11 on threshold breaches** (50% / 80% / 100% of window) (active escalation)
- C. M13 calculates; SLA breach is a critical event triggering immediate PROJECT_DIRECTOR + PMO_DIRECTOR notification (binary)

**Resolution:** **B (LOCKED).** Tiered escalation balances signal-to-noise. 50% = informational; 80% = warning to owner; 100% = breach with PMO escalation. Aligns with M04 Decision Queue SLA defaults pattern + M05 OQ-2.3 cadence model.

**Cascade impact:**
- New X8 ENUM `NoticeSLAStatus` = `Within / Warning / Breach`
- Decision Queue triggers: `NOTICE_SLA_WARNING` (80%) + `NOTICE_SLA_BREACH` (100%)
- M11 consumes both as Medium / High severity
- Per-notice-type SLA configurable in `ProjectCorrespondenceConfig` (per OQ-2.4)

**Status:** CLOSED

---

### OQ-1.3 — Correspondence direction model

**Question:** How does M13 model incoming vs outgoing communications?

**Options:**
- A. Single `Correspondence` entity with `direction` ENUM (Incoming / Outgoing)
- B. **Separate `IncomingCorrespondence` and `OutgoingCorrespondence` entities** (different SLA logic, different attachment patterns, different audit trails)
- C. Single entity + sub-type discriminator

**Resolution:** **A (LOCKED).** Single entity is simpler; SLA logic differs by `correspondence_type` (Notice vs Information vs Instruction), not by direction. Direction is a single ENUM field. Simpler queries, simpler UI, simpler API surface. Option B would force duplicate logic across two near-identical entities.

**Cascade impact:**
- Single `Correspondence` entity with `direction` ENUM (Incoming / Outgoing)
- Filter views split by direction in UI (per role-default view mapping OQ-1.8)

**Status:** CLOSED

---

### OQ-1.4 — Meeting minutes structure

**Question:** Are meeting minutes free-text, structured (line-items), or both?

**Options:**
- A. Free-text only (single `minutes_text` blob per meeting)
- B. **Structured line-items** (`MinutesEntry` rows per meeting, each typed: Decision / Action / Discussion / Risk_Noted / Information)
- C. Both — free-text PLUS optional line-items

**Resolution:** **B (LOCKED).** Structured minutes are searchable, linkable, and reportable. Action items naturally extract from MinutesEntry rows where `entry_type = Action`. Risk-noted entries can flow to M05 for risk-register import. Free-text loses every linkability. The minor authoring friction (UI guides typing of each line) pays back in audit / reporting / claims defensibility.

**Cascade impact:**
- New X8 ENUM `MinutesEntryType` = `Decision / Action / Discussion / Risk_Noted / Information / Question`
- ActionItem entity is auto-created from MinutesEntry rows where `entry_type = Action`
- Risk_Noted entries can be promoted to M05.Risk via "Promote to Risk Register" UI action (audited)

**Status:** CLOSED

---

### OQ-1.5 — Action item ownership model

**Question:** Where does ActionItem owner come from?

**Options:**
- A. Free-text (any string)
- B. M34 User FK only (must be a registered user)
- C. **M34 User FK OR M01 Party FK** (user OR external party — e.g., contractor, consultant, regulator)
- D. Free-text with optional M34 User FK

**Resolution:** **C (LOCKED).** Real-world action items are often owned by external parties (contractor, design consultant, regulator). Forcing M34 User restricts to internal staff only. Forcing free-text loses linkability. Hybrid: `owner_user_id` (NULLABLE FK to M34 User) OR `owner_party_id` (NULLABLE FK to M01 Party); exactly one must be populated; UI guides selection.

**Cascade impact:**
- ActionItem entity: `owner_user_id UUID NULLABLE FK M34.User`, `owner_party_id UUID NULLABLE FK M01.Party`, CHECK constraint exactly-one-populated
- M11 ActionRegister consumes both; if owner is external party, SLA escalation goes to PROJECT_DIRECTOR (proxy for the party)
- Decision Queue trigger payloads carry both fields; M11 routes accordingly

**Status:** CLOSED

---

### OQ-1.6 — RFI scope + lifecycle

**Question:** Does M13 own RFIs, or do they live in M12 / a separate module?

**Options:**
- A. **M13 owns RFI entity + lifecycle; M12 owns RFI attachments** (drawings, sketches, specifications referenced)
- B. M12 owns RFI entirely (since RFIs typically reference drawings)
- C. Separate M-RFI module

**Resolution:** **A (LOCKED).** RFIs are formal communications with contractual SLA — that's M13's primary concern. The attachments (drawings, specs) are documents — that's M12's primary concern. Splitting RFI metadata (M13) from RFI attachments (M12) is the correct single-owner split. Option B over-loads M12 with communications-layer concerns. Option C creates artificial fragmentation for what is conceptually a correspondence type.

**Cascade impact:**
- RFI entity in M13 with state machine (Open → Responded → Closed); SLA-bound
- RFI.attachments[] = `document_id[]` FK array to M12
- M12-stub pattern (matching M04 photo stub) during interim until M12 v1.0 lands; migration script drafted in M13 Spec
- M03 integration: RFI may carry `affected_milestones[]` for schedule-impact assessment

**Status:** CLOSED

---

### OQ-1.7 — Distribution & acknowledgement model

**Question:** Does M13 track who received + acknowledged each communication?

**Options:**
- A. **Yes — explicit `DistributionList` rows with `received_at` + `acknowledged_at` per recipient**
- B. No — communications are sent; acknowledgement is on email layer
- C. Yes for Notices only; not for Information/Instruction

**Resolution:** **A (LOCKED).** Distribution + acknowledgement is the core legal evidence in disputes. "I sent this on date X" is contestable; "Person Y opened the system on date X+2 and clicked Acknowledge" is evidence. Tier 2 portal access (CLIENT_VIEWER, LENDER_VIEWER per PF03 Phase 2) needs this for external acknowledgement. Building it for all communications is one entity; restricting to notices only would force schema split later.

**Cascade impact:**
- DistributionList entity: `correspondence_id FK`, `recipient_user_id NULLABLE FK`, `recipient_party_id NULLABLE FK`, `recipient_email` (for non-system recipients), `received_at`, `acknowledged_at`, `acknowledgement_method` (system_click / email_reply / verbal_recorded)
- Append-only on acknowledgement (forward-only ledger pattern)
- UI shows acknowledgement status per recipient on correspondence detail view

**Status:** CLOSED

---

### OQ-1.8 — Role-default views per X9 v0.4 §13.3

**Question:** What is each role's primary + secondary chart view in M13?

**Resolution:** **Mapping (a) LOCKED:**

| Role | Primary view | Secondary view |
|---|---|---|
| `PROJECT_DIRECTOR` | **Notice tracker** — pending notices sorted by SLA-time-remaining (warning + breach highlighted) | Meeting calendar (this-week + next-week) |
| `PMO_DIRECTOR` | Notice SLA breach dashboard (across all projects) | Open RFI count by project + average response time |
| `PORTFOLIO_MANAGER` | Portfolio correspondence volume + breach rate (table) | — |
| `PLANNING_ENGINEER` | Open RFIs (own project; affected_milestones impact view) | Pending action items (own assigned) |
| `QS_MANAGER` | Pending action items (own assigned) + meeting prep queue | Notices linking to VOs (M05 cross-link) |
| `SITE_MANAGER` | **Daily inbound correspondence + RFI raise UI** (own project) | Today's meeting agenda |
| `FINANCE_LEAD` | Notices linking to commercial impact (M05 + M06 cross-link) | — |
| `PROCUREMENT_OFFICER` | Vendor correspondence + transmittals | Pending vendor RFIs |
| `COMPLIANCE_MANAGER` | Regulatory notices + responses | Notices linking to compliance items (M09 cross-link) |
| `ANALYST` | Correspondence trend (volume by type per month) | RFI response-time trend |
| `READ_ONLY` | Correspondence card (status badges + counts; no detail body) | — |
| `EXTERNAL_AUDITOR` | Full correspondence read + meeting minutes + RFI history | Distribution + acknowledgement audit trail |
| `SYSTEM_ADMIN` / `CLIENT_VIEWER` (Phase 2) / `LENDER_VIEWER` (Phase 2) / `NABH_ASSESSOR` (Phase 2) / `CONTRACTOR_LIMITED` (Phase 2) | (no primary M13 view; system / Phase 2 portal-gated) | — |

**Cascade impact:**
- X9 v0.5 cascade — add M13 row to §13.3 role-default views (alongside M05 row from same R34 batch)
- **Notice SLA breach funnel** (Within → Warning → Breach) — could be 6th flagship pipeline pattern instance (X9 §11); confirm in Spec round whether to formally name as flagship or treat as M13-internal variant
- 5×5 correspondence-volume heatmap (project × correspondence-type) for ANALYST view — verify X9 catalogue fit during Spec round

**Status:** CLOSED

---

## 5. OQ-2 — Pattern Defaults (Claude recommended; user confirmed)

### OQ-2.1 — Audit event naming discipline

**Default:** Lock proposed audit event names in this Brief (Appendix A) so the Spec carries them as locked from authoring.

**Reasoning:** M04/M05 OQ-2.1 + M03 v1.1 cascade pattern. Estimated 22-26 events.

**Status:** CLOSED — proceed with lock-in-Brief

### OQ-2.2 — Append-only ledgers

**Default:** Following entities are append-only (DB-level UPDATE/DELETE forbidden — same pattern as M02 BACIntegrityLedger, M04 NCRStatusLog, M06 CostLedgerEntry, M05 RiskStatusLog):

- `CorrespondenceStatusLog` — every Correspondence state transition + classification change
- `NoticeSLAEvent` — every SLA threshold crossed (50% / 80% / 100%) + breach event
- `DistributionList` — append-only on acknowledgement (forward-only ledger)
- `RFIStatusLog` — every RFI state transition (Open → Responded → Closed)
- `MeetingMinutesAuditLog` — every minutes edit / line-item add / line-item-classify

**Reasoning:** Communications are evidence. Audit trail integrity is the core value.

**Status:** CLOSED

### OQ-2.3 — Decision Queue SLA defaults

**Default:**

| Trigger | Severity | Owner | SLA |
|---|---|---|---|
| `NOTICE_SLA_WARNING` (80% of response window elapsed) | Medium | Recipient (owner_user_id or PROJECT_DIRECTOR if external) | per remaining window |
| `NOTICE_SLA_BREACH` (100% breached) | High | PROJECT_DIRECTOR | 24 hr to acknowledge breach |
| `RFI_RESPONSE_OVERDUE` (RFI Open > X days, X = `ProjectCorrespondenceConfig.rfi_sla_days`, default 14) | Medium | PROJECT_DIRECTOR + PLANNING_ENGINEER | 48 hr |
| `MEETING_MINUTES_NOT_CIRCULATED` (Meeting end + 48hr without circulated minutes) | Low | Meeting chair | 24 hr |
| `ACTION_ITEM_OVERDUE` (action item due_date past, status not Closed) | Medium → High (escalating) | ActionItem.owner_user_id or PROJECT_DIRECTOR | per overdue duration |
| `ACKNOWLEDGEMENT_OVERDUE` (Notice distributed + 7 days without recipient acknowledgement) | Medium | PROJECT_DIRECTOR | 24 hr |
| `CORRESPONDENCE_CLASSIFICATION_DISPUTED` (recipient flags re-classification request) | Medium | PROJECT_DIRECTOR | 48 hr |

**Reasoning:** Aligns with M03/M04/M05/M06 SLA conventions.

**Status:** CLOSED

### OQ-2.4 — Speed tier defaults

**Default:**

| Event class | Speed tier |
|---|---|
| Correspondence create / classify / send | 🔴 Real-time |
| Notice SLA threshold crossed (any) | 🔴 Real-time |
| RFI create / respond / close | 🔴 Real-time |
| Meeting minutes save / line-item add | 🔴 Real-time |
| ActionItem create (from MinutesEntry) | 🔴 Real-time |
| ActionItem owner notification | 🔴 Real-time |
| Daily NoticeTracker SLA sweep (background recompute) | 🟢 24 hr |
| Correspondence volume trend recompute (ANALYST view) | 🟢 24 hr |
| External party acknowledgement timeout sweep | 🟢 24 hr |

**Status:** CLOSED

### OQ-2.5 — ProjectCorrespondenceConfig entity (per-project tunables)

**Default:** M13-owned `ProjectCorrespondenceConfig` entity (1 row per project) carries:

| Field | Default | Notes |
|---|---|---|
| `notice_sla_warning_pct` | 0.80 | OQ-1.2 lock |
| `rfi_sla_days` | 14 | OQ-2.3 |
| `acknowledgement_timeout_days` | 7 | OQ-2.3 |
| `meeting_minutes_circulation_hours` | 48 | OQ-2.3 |
| `correspondence_retention_years` | 7 | aligns with Companies Act + DPDPA |

**Reasoning:** Mirrors M04 ProjectExecutionConfig + M05 ProjectRiskConfig pattern. Avoids M01 cascade for module-specific tunables. PROJECT_DIRECTOR + PMO_DIRECTOR may edit; audited.

**Status:** CLOSED

---

## 6. Users & Roles (all 17 canonical roles per M34 Spec Block 3)

| Role | M13 Access |
|---|---|
| `SYSTEM_ADMIN` | Full read; system-context only |
| `PMO_DIRECTOR` | **PRIMARY** — Notice SLA breach dashboard, acknowledgement audit, correspondence volume oversight |
| `PORTFOLIO_MANAGER` | **PRIMARY** — Portfolio correspondence rollup |
| `PROJECT_DIRECTOR` | **PRIMARY** — Notice tracker (own project), meeting calendar, action item oversight |
| `PLANNING_ENGINEER` | **PRIMARY** — Open RFIs (own project; affected_milestones impact), pending action items |
| `QS_MANAGER` | **PRIMARY** — Action item queue, meeting prep, notices linking to VOs |
| `FINANCE_LEAD` | **SECONDARY** — Notices linking to commercial impact (M05/M06 cross-link) |
| `PROCUREMENT_OFFICER` | **PRIMARY** — Vendor correspondence + transmittals + vendor RFIs |
| `SITE_MANAGER` | **PRIMARY** — Daily inbound correspondence (own project), RFI raise UI, today's meetings |
| `COMPLIANCE_MANAGER` | **PRIMARY** — Regulatory notices + responses, M09 cross-link |
| `ANALYST` | **PRIMARY** — Correspondence trends, RFI response-time analysis |
| `READ_ONLY` | **VIEW-ONLY** — Correspondence card (status badges only; no body) |
| `EXTERNAL_AUDITOR` | **VIEW-ONLY** — Full read + acknowledgement audit trail (MFA-required per M34) |
| `CLIENT_VIEWER` (Phase 2) | **NO ACCESS** Phase 1 — gated by PF03 |
| `LENDER_VIEWER` (Phase 2) | **NO ACCESS** Phase 1 — gated by PF03 |
| `NABH_ASSESSOR` (Phase 2) | **NO ACCESS** Phase 1 — gated by PF03 |
| `CONTRACTOR_LIMITED` (Phase 2) | **NO ACCESS** Phase 1 — gated by PF03 |

**MFA-required roles:** SYSTEM_ADMIN, PMO_DIRECTOR, PORTFOLIO_MANAGER, FINANCE_LEAD, EXTERNAL_AUDITOR (M34 inherit).

---

## 7. Key Entities (Spec Round 34 will detail; Brief locks the shape)

| Entity | Cardinality | Owner | Purpose |
|---|---|---|---|
| `Correspondence` | Many per project | M13 | Single source of truth for formal communications. Direction (Incoming/Outgoing), type classification, contractual reference, document_id FK to M12 |
| `CorrespondenceStatusLog` | Many per Correspondence | M13 (append-only) | Every classification change + state transition |
| `NoticeTracker` | Subset of Correspondence (where type=Notice) | M13 | SLA-bound view; tracks response window per contractual clause; auto-emits Decision Queue triggers |
| `NoticeSLAEvent` | Many per NoticeTracker | M13 (append-only) | Each SLA threshold crossed (50% / 80% / 100%) + breach |
| `MeetingRegister` | Many per project | M13 | Meeting types, attendees, agenda, distribution list |
| `MinutesEntry` | Many per Meeting | M13 | Structured line-items (Decision / Action / Discussion / Risk_Noted / Information / Question) |
| `MeetingMinutesAuditLog` | Many per Meeting | M13 (append-only) | Every minutes edit + line-item operation |
| `ActionItem` | Many per Meeting OR per Notice OR standalone | M13 | Action entity emitted to M11 ActionRegister; owner is User OR Party (CHECK constraint) |
| `RFI` | Many per project | M13 | RFI lifecycle (Open → Responded → Closed); SLA-bound; affects_milestones[] for M03 cross-link |
| `RFIStatusLog` | Many per RFI | M13 (append-only) | State transitions + response edits |
| `Transmittal` | Many per project | M13 | Outgoing formal package transmissions; receipt-acknowledgement tracking |
| `DistributionList` | Many per Correspondence/Notice/Minutes/Transmittal | M13 (append-only on acknowledgement) | Per-recipient receipt + acknowledgement record |
| `ProjectCorrespondenceConfig` | 1 per project | M13 | Per-project tunables (OQ-2.5) |

**Total entities:** 13 (5 primary + 3 sub-views/derivative + 5 append-only ledgers/sub-entities). Comparable to M04 (10), M05 (14), M06 (17).

---

## 8. Integration Points (sketch — full spec in Block 7 of Round 34 Spec)

### IN (M13 receives from)

| From | Data | Trigger | Speed |
|---|---|---|---|
| M01 | `Project.id`, `Contract.id`, `Party` (recipient identities), `Contract.notice_sla_default_days` (per-contract notice SLA tunables) | On Project state change + Contract edit | 🔴 |
| M03 | `Milestone` IDs (for RFI affected_milestones[] selection) | On RFI raise | 🔴 |
| M12 DocumentControl (when built) | `document_id` allocation for attachments | On attachment upload (during M12-stub interim, MinIO direct URL) | 🔴 |
| M34 | Auth, role, project scope, MFA gate | Every API call | 🔴 |
| M11 ActionRegister (when built) | Action item status updates back-events (when M11 marks closed) | On owner action | 🔴 |

### OUT (M13 sends to)

| To | Data | Trigger | Speed |
|---|---|---|---|
| **M11 ActionRegister** (when built) | `ActionItem` payload (owner, due_date, source_meeting_id OR source_notice_id, severity); plus all SLA-breach Decision Queue triggers | On MinutesEntry type=Action OR Notice SLA threshold crossed | 🔴 |
| **M05 RiskChangeControl** | Notice classification = Claim / Notice → trigger M05 EOT/VO claim assessment workflow (M05 reads via internal API, not push); Risk_Noted MinutesEntry promotion to M05.Risk (audited UI action) | On request OR explicit promote | 🔴 / on-demand |
| M03 PlanningMilestones | RFI.affected_milestones[] for schedule-impact view (M03 reads via internal API) | On request | 🟡 1hr cache |
| M09 ComplianceTracker (when built) | Regulatory Notices + responses cross-link | On Correspondence type=Regulatory_Notice | 🔴 |
| M12 DocumentControl (when built) | Document references for blob storage; M13 holds metadata, M12 holds blobs | On attachment | 🔴 |
| M19 ClaimsManagement (Phase 2) | Full correspondence chain export for claim documentation packets | On request (Phase 2) | 🟡 |

---

## 9. Key Business Rules (OQ-level — full BRs in Round 34 Spec Block 6)

The following are hard rules locked at Brief stage. Numbered `BR-13-xxx` in Spec round.

| # | Rule (one-line summary) | Authority |
|---|---|---|
| 1 | **Every Correspondence with type=Notice MUST have a contractual_reference** (clause text or contract section reference) — block save without it | OQ-1.2 |
| 2 | **NoticeTracker SLA calculations are immutable per-notice** — once SLA-due-date set on creation, only PMO_DIRECTOR can override (audited) | OQ-1.2 |
| 3 | **MinutesEntry where type=Action MUST have an owner** (user OR party); CHECK constraint exactly-one-populated | OQ-1.5 |
| 4 | **MinutesEntry where type=Risk_Noted MAY be promoted to M05.Risk** via UI action; promotion is one-way (cannot un-promote); audited | OQ-1.4 |
| 5 | **DistributionList rows are append-only on acknowledgement** — `acknowledged_at` set once, never updated | OQ-1.7 + OQ-2.2 |
| 6 | **RFI close requires response_text + responder_user_id** populated (≥ 50 chars); block close without | OQ-1.6 |
| 7 | **Transmittal close requires acknowledgement_count >= recipient_count** OR explicit PMO_DIRECTOR override | OQ-1.7 |
| 8 | **Notice SLA breach (100%) auto-creates a Decision Queue High-severity item** to PROJECT_DIRECTOR with 24hr SLA to acknowledge breach | OQ-1.2 + OQ-2.3 |
| 9 | **Meeting minutes circulation is mandatory within 48hr** of meeting end; LOW Decision Queue trigger after 48hr (configurable per OQ-2.5) | OQ-2.3 |
| 10 | **External recipient acknowledgement requires 7-day timeout** before flagging missing-acknowledgement (configurable) | OQ-2.3 |
| 11 | **Correspondence cannot be deleted** — only archived (status=Archived); audit log preserved | OQ-2.2 |
| 12 | **Document attachment via M12 (or stub) — M13 never stores BLOBs** (only document_id references) | OQ-1.1 + M12 single-owner |

---

## 10. Forward Constraints for Downstream Modules

When future module specs are authored, they must respect M13's locked contracts:

| Module | Constraint Imposed by M13 v1.0 |
|---|---|
| **M11 ActionRegister** (R58 Brief) | MUST consume M13 ActionItem emit + Notice/RFI/Meeting SLA Decision Queue triggers. M11 owns SLA escalation; M13 owns trigger emission |
| **M12 DocumentControl** (future round) | MUST accept M13 `document_id` allocation requests; provides blob storage; supports M13 attachment patterns (Correspondence + RFI + Transmittal + MinutesEntry) |
| **M05 RiskChangeControl** (R33 Spec) | M13 Notice with classification=Claim/Notice → triggers M05 EOT/VO claim assessment. M05 reads via M13 internal API (not push). Risk_Noted MinutesEntry → optional UI-promoted M05.Risk creation |
| **M09 ComplianceTracker** (future round) | MUST consume M13 regulatory notices + responses for compliance evidence |
| **M19 ClaimsManagement** (Phase 2) | Correspondence chain export for formal claim packets (M13 emits chain; M19 absorbs into claim documentation) |
| **PF03 ExternalPartyPortal** (Phase 2) | When built: external roles (CLIENT_VIEWER, LENDER_VIEWER, etc.) get scoped read access to Correspondence + DistributionList (acknowledgement UI) per their party_id scope |

---

## 11. Deliverables Upon Spec Lock

| Round | Artefact | Cadence |
|---|---|---|
| **31** | M05 RiskChangeControl Brief v1.0 | C1 (Brief) — ✅ LOCKED |
| **32 (this)** | M13 CorrespondenceMeetingRegister Brief v1.0 | C1 (Brief; C1b batch partner with M05) |
| 33 | M05 Spec v1.0 + X8 v0.7 cascade scaffold | C1 (Spec; one at a time per spec-protocol.md) |
| 34 | **M13 Spec v1.0 + X8/X9 audit pass for M05+M13 batch** | C1 (Spec) |
| 35 | **M05 + M13 Wireframes (C1b batch)** | C1b batch |
| 36 | **M05 + M13 Workflows (C1b batch)** | C1b batch |
| ↓ | Both M05 and M13 build-ready after R36 | — |

---

## 12. Open Items Tracker

| ID | Topic | Type | Status |
|---|---|---|---|
| OQ-1.1 | Module scope — slim core (B); document storage to M12; action SLA to M11 | User Decision | **CLOSED** |
| OQ-1.2 | Notice SLA enforcement — tiered escalation (B) — 50%/80%/100% | User Decision | **CLOSED** |
| OQ-1.3 | Correspondence direction model — single entity + ENUM (A) | User Decision | **CLOSED** |
| OQ-1.4 | Meeting minutes — structured line-items (B) | User Decision | **CLOSED** |
| OQ-1.5 | Action item ownership — User OR Party FK (C) | User Decision | **CLOSED** |
| OQ-1.6 | RFI scope — M13 metadata + M12 attachments (A) | User Decision | **CLOSED** |
| OQ-1.7 | Distribution & acknowledgement — explicit DistributionList (A) | User Decision | **CLOSED** |
| OQ-1.8 | Role-default views per X9 v0.4 §13.3 | User Decision | **CLOSED** |
| OQ-2.1 | Lock audit events in Brief | Pattern Default | **CLOSED** |
| OQ-2.2 | Append-only ledgers (5 entities) | Pattern Default | **CLOSED** |
| OQ-2.3 | Decision Queue SLA defaults (7 triggers) | Pattern Default | **CLOSED** |
| OQ-2.4 | Speed tier defaults | Pattern Default | **CLOSED** |
| OQ-2.5 | ProjectCorrespondenceConfig per-project tunables | Pattern Default | **CLOSED** |

**Lock criterion met:** All 13 items CLOSED. Brief LOCKED.

---

## 13. Cascade Notes (for Spec Round 34)

The M13 Spec Round 34 will produce / require:

| Cascade | Type | Target | Notes |
|---|---|---|---|
| **X8 v0.7 cascade (joint with M05)** | New ENUMs | `X8_GlossaryENUMs_v0_7.md` | Add: `CorrespondenceDirection`, `CorrespondenceType`, `NoticeSLAStatus`, `MinutesEntryType`, `RFIStatus`, `TransmittalStatus`, `ActionItemStatus`, `AcknowledgementMethod` (8 new ENUMs from M13; total v0.7 cascade is M05 + M13 combined) |
| **X9 v0.5 cascade (joint with M05)** | Role-default views update | `X9_VisualisationStandards_Spec_v0_5.md` | Add M13 row to §13.3 (alongside M05 row from same R34 batch). Notice SLA Breach Funnel — possibly 6th flagship pipeline pattern instance (verify in Spec round) |
| **M01 → M13 contract** | New (additive) | M01 cascade note (if `Contract.notice_sla_default_days` field needed) OR M13-owned ProjectCorrespondenceConfig | Decision: store in `ProjectCorrespondenceConfig` (per OQ-2.5) — avoids M01 cascade |
| **M03 → M13 contract** | Read-only | M13 reads `Milestone.id` for RFI affected_milestones[]; no M03 schema change | No cascade |
| **M11 ActionRegister contract (forward)** | Forward | M11 Brief (R58) must accept M13 ActionItem emit | Recorded as forward constraint |
| **M12 DocumentControl contract (forward)** | Forward | M12 Brief (future round) must accept M13 document_id allocation | Recorded as forward constraint |
| **M13 Spec Appendix A — Audit Events Catalogue** | New section | M13 Spec Round 34 | Per OQ-2.1 — lock from authoring. Estimated 22-26 events |
| **ProjectCorrespondenceConfig entity** | New | M13 Spec Round 34 Block 3 | Per OQ-2.5 — avoids M01 cascade |

### Modules unblocked by M13 lock

- **M05 RiskChangeControl** — M05 Spec (R33) can reference M13 Notice → claim trigger explicitly (was abstract in M05 Brief)
- **M11 ActionRegister** — Brief (R58) has full ActionItem contract from M13
- **M09 ComplianceTracker** — regulatory notice flow contract from M13
- **M19 ClaimsManagement** (Phase 2) — correspondence chain export contract from M13

---

## Appendix A — Proposed Audit Events Catalogue (locked from authoring)

Per OQ-2.1 — events locked at Brief stage so Spec is a re-statement, not a re-issue.

### A.1 Correspondence events
- `CORRESPONDENCE_CREATED`
- `CORRESPONDENCE_CLASSIFIED` — type assigned/changed
- `CORRESPONDENCE_SENT` — outgoing transmission timestamp
- `CORRESPONDENCE_ARCHIVED`

### A.2 Notice events
- `NOTICE_RAISED`
- `NOTICE_SLA_WARNING` — 80% threshold crossed
- `NOTICE_SLA_BREACH` — 100% threshold crossed
- `NOTICE_RESPONDED`
- `NOTICE_CLOSED`

### A.3 Meeting events
- `MEETING_SCHEDULED`
- `MEETING_HELD` — meeting end recorded
- `MINUTES_DRAFTED`
- `MINUTES_CIRCULATED`
- `MINUTES_ENTRY_ADDED` — line-item added
- `MINUTES_ENTRY_PROMOTED_TO_RISK` — Risk_Noted entry promoted to M05.Risk

### A.4 ActionItem events
- `ACTION_ITEM_CREATED` — emit to M11
- `ACTION_ITEM_OWNER_NOTIFIED`
- `ACTION_ITEM_OVERDUE` — emit to M11 Decision Queue

### A.5 RFI events
- `RFI_RAISED`
- `RFI_RESPONDED`
- `RFI_CLOSED`
- `RFI_RESPONSE_OVERDUE` — emit to M11 Decision Queue

### A.6 Distribution + Acknowledgement events
- `DISTRIBUTION_SENT`
- `ACKNOWLEDGEMENT_RECORDED`
- `ACKNOWLEDGEMENT_OVERDUE`

### A.7 Transmittal events
- `TRANSMITTAL_CREATED`
- `TRANSMITTAL_ACKNOWLEDGED`

**Estimated total:** 24 events. Round 34 Spec finalises exact count.

---

## What This Brief Does NOT Cover

- **Document storage** — M12 owns blobs; M13 stores `document_id` references
- **Email integration / IMAP ingestion** — Phase 2 (manual entry only in v1.0)
- **Speech-to-text meeting minutes** — Phase 2
- **Document review workflows** — M12 owns when built
- **External-party portal access** — PF03 Phase 2
- **Action SLA enforcement / queue routing** — M11 ActionRegister owns
- **Commercial deliberation on correspondence** — M05 RiskChangeControl owns
- **Site daily diary** — M16 SiteDiary (separate module)
- **Long-form claims documentation** — M19 ClaimsManagement Phase 2

---

*v1.0 — Brief LOCKED. All 13 OQ items CLOSED. Ready for Round 34 Spec authoring (after R33 M05 Spec lock — C1 cadence). M05+M13 form the foundation L2 commercial-control batch.*
