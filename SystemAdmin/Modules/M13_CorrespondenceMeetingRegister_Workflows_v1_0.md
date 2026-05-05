---
artefact: M13_CorrespondenceMeetingRegister_Workflows_v1_0
round: 36
date: 2026-05-04
author: Monish (with Claude assist)
parent_spec: M13_CorrespondenceMeetingRegister_Spec_v1_0.md (Round 34)
parent_brief: M13_CorrespondenceMeetingRegister_Brief_v1_0 (Round 32)
x8_version: v0.8
x9_version: v0.5
status: LOCKED
type: Module Workflows (Mermaid flowcharts + BR traceability)
batch_partner: M05_RiskChangeControl_Workflows_v1_0.md (C1b batch per Build Execution Plan §3a)
br_coverage: 24 BRs (BR-13-001..024) across 4 WFs — 0 gaps (see BR Coverage Matrix)
---

# M13 — Correspondence & Meeting Register — Workflows v1.0

## CHANGE LOG

| Version | Date | Author | Change Summary |
|---|---|---|---|
| v1.0 | 2026-05-04 | Monish (with Claude assist) | Initial workflows lock (Round 36). 4 workflows covering all M13 Spec v1.0 (R34) BRs. WF-13-001 Correspondence Lifecycle + Site Instruction + Distribution (BR-13-001..008, 022..024); WF-13-002 M05 Trigger + Risk_Noted Promotion + RFI Impact (BR-13-009..012); WF-13-003 Meeting Management + Action Items (BR-13-013..017); WF-13-004 RFI Lifecycle (BR-13-018..021). All Mermaid flowcharts validate. C1b batch with M05 Workflows. |

---

## Purpose

Runtime workflows for M13 Correspondence & Meeting Register. Each Mermaid diagram describes the **runtime behaviour** of a decision-bearing process. Cross-references to BR codes link runtime to the locked specification (M13 Spec v1.0 Block 6).

4 workflows covered:

| # | Workflow | Decision Answered | Primary Role(s) | BR Coverage |
|---|---|---|---|---|
| **WF-13-001** | Correspondence Lifecycle + Site Instruction + Distribution | Has incoming correspondence been acknowledged, responded within contractual timelines, and appropriately escalated where overdue? Are Site Instructions complied with? Are distributions acknowledged? | PROJECT_DIRECTOR (manages) + COMPLIANCE_MANAGER (regulatory) + recipients (acknowledge) | BR-13-001..008, 022..024 |
| **WF-13-002** | M05 Correspondence Trigger + Risk_Noted Promotion + RFI Impact | Has correspondence been correctly flagged as triggering an M05 action (EWN, VO, EOT, Risk)? | PROJECT_DIRECTOR or PMO_DIRECTOR (only roles authorised per BR-13-009) | BR-13-009..012 |
| **WF-13-003** | Meeting Management + Minutes + Action Items | Have meeting minutes been recorded, circulated, and approved with all action items assigned and tracked? | Meeting chairperson + PMO_DIRECTOR/PROJECT_DIRECTOR (approve minutes) | BR-13-013..017 |
| **WF-13-004** | RFI Lifecycle | Has the contractor's RFI received a timely documented response, with cost/design/schedule impact escalated appropriately? | QS_MANAGER + PROJECT_DIRECTOR (respond) + PMO_DIRECTOR (close/reopen) | BR-13-018..021 |

---

## WF-13-001 — Correspondence Lifecycle + Site Instruction + Distribution

> **Decision:** Has incoming correspondence been acknowledged, responded to within contractual timelines, and appropriately escalated where overdue? Are Site Instructions complied with by the deadline? Are distribution recipients acknowledging receipt?
> **Primary Role:** PROJECT_DIRECTOR (manages register) + COMPLIANCE_MANAGER (regulatory subset) + recipients (acknowledge).
> **BR Coverage:** BR-13-001 (Project Activation auto-create config), BR-13-002 (Notice contractual_reference required), BR-13-003 (Site Instruction compliance_deadline required), BR-13-004 (response_required auto-set), BR-13-005 (response_due_date auto-compute), BR-13-006 (Notice SLA Warning sweep), BR-13-007 (Notice SLA Breach sweep), BR-13-008 (Correspondence respond), BR-13-022 (Site Instruction non-compliance sweep), BR-13-023 (Distribution sent event), BR-13-024 (Daily Acknowledgement sweep).

### Project Activation Sub-Flow (BR-13-001)

```mermaid
flowchart LR
    A[M01 emits PROJECT_ACTIVATED event] --> B[M13 receives]
    B --> C[Auto-create ProjectCorrespondenceConfig row<br/>OQ-2.5 defaults:<br/>notice_sla_warning_pct=0.80<br/>rfi_sla_days=14<br/>acknowledgement_timeout_days=7<br/>meeting_minutes_circulation_hours=48<br/>correspondence_retention_years=7]
    C --> D[PROJECT_CORRESPONDENCE_INITIALISED audit event]
```

### Correspondence Lifecycle State Machine

```mermaid
stateDiagram-v2
    [*] --> Created: RAISE_CORRESPONDENCE action
    Created --> Pending: response_required=true<br/>response_due_date computed<br/>(BR-13-004 + BR-13-005)
    Created --> Not_Required: response_required=false<br/>(Information / Outgoing without obligation)
    Pending --> Responded: BR-13-008 response action
    Pending --> Overdue: response_due_date < today<br/>BR-13-007 daily sweep
    Overdue --> Responded: late response captured
    Responded --> Closed: PROJECT_DIRECTOR closes
    Not_Required --> Closed: explicit close
    Closed --> Archived: soft-delete is_active=false<br/>per BR-13-018 hard-delete forbidden
```

### Runtime Flow

```mermaid
flowchart TD
    A[RAISE_CORRESPONDENCE action<br/>by authorised role per Block 4a] --> B{correspondence_type<br/>IN Notice / Site_Instruction?}
    B -->|YES| C{contractual_reference<br/>populated ≥ 50 chars?<br/>BR-13-002}
    C -->|NO| D[Block save:<br/>CONTRACTUAL_REFERENCE_REQUIRED]
    C -->|YES| E[Continue]
    B -->|NO| E
    E --> F{correspondence_type =<br/>Site_Instruction?}
    F -->|YES| G{compliance_deadline<br/>populated?<br/>compliance_status=Pending<br/>BR-13-003}
    G -->|NO| H[Block save:<br/>COMPLIANCE_DEADLINE_REQUIRED]
    G -->|YES| I[Continue]
    F -->|NO| I
    I --> J{correspondence_type IN<br/>Notice / RFI_Reference / Site_Instruction?<br/>BR-13-004}
    J -->|YES| K[Auto-set response_required=true]
    J -->|NO| L[response_required=false<br/>response_status=Not_Required]
    K --> M[Compute response_due_date:<br/>sent_date + applicable_sla_days<br/>per BR-13-005]
    M --> N[Persist Correspondence row<br/>response_status=Pending]
    L --> N
    N --> O[CORRESPONDENCE_CREATED audit event<br/>CorrespondenceStatusLog row append-only]

    O --> P[Distribution sent to recipients<br/>per DistributionList rows<br/>BR-13-023]
    P --> Q[DISTRIBUTION_SENT audit event<br/>per DistributionList row]

    style D fill:#fee2e2
    style H fill:#fee2e2
```

### Notice SLA Sweep (Daily 🟢 24hr — BR-13-006 + BR-13-007)

```mermaid
flowchart TD
    A[Daily Notice SLA sweep] --> B{For each Correspondence<br/>where response_required=true<br/>AND response_status=Pending<br/>AND correspondence_type=Notice<br/>AND contractual_weight IN<br/>Formal_Notice / Contractual}
    B --> C[Compute sla_remaining_pct:<br/>response_due_date - today /<br/>total_sla_days]
    C --> D{sla_remaining_pct ≤ 0.20?<br/>i.e. 80% elapsed<br/>BR-13-006}
    D -->|YES| E[Emit NOTICE_SLA_WARNING<br/>DQ trigger Medium<br/>to recipient or PROJECT_DIRECTOR<br/>Create NoticeSLAEvent row append-only]
    D -->|NO| F[Continue to next row]
    C --> G{response_due_date < today?<br/>i.e. 100% elapsed<br/>BR-13-007}
    G -->|YES| H[Set response_status = Overdue<br/>Emit NOTICE_SLA_BREACH<br/>DQ trigger High to PROJECT_DIRECTOR<br/>24hr SLA to acknowledge breach<br/>Create NoticeSLAEvent row]
    G -->|NO| F

    style E fill:#fef3c7
    style H fill:#fee2e2
```

### Correspondence Response (BR-13-008)

```mermaid
flowchart LR
    A[Recipient or PROJECT_DIRECTOR<br/>RESPOND_TO_CORRESPONDENCE action] --> B[Create new Correspondence row<br/>direction = opposite of original<br/>parent_correspondence_id = original.id]
    B --> C{Same parent_correspondence_id<br/>OR original is parent?}
    C -->|NO| D[Block: INVALID_THREAD_LINK]
    C -->|YES| E[Update original Correspondence:<br/>response_status = Responded<br/>responded_at = now<br/>responded_by_user_id = caller<br/>responded_via_correspondence_id = new]
    E --> F[CORRESPONDENCE_RESPONDED audit event]
    F --> G{Was original Overdue?}
    G -->|YES| H[Emit NOTICE_SLA_OVERDUE_RESOLVED<br/>(informational; closes prior breach)]
    G -->|NO| I[Done]
```

### Site Instruction Compliance Sweep (Daily — BR-13-022)

```mermaid
flowchart TD
    A[Daily Site Instruction sweep] --> B{For each Correspondence<br/>where correspondence_type=Site_Instruction<br/>AND compliance_status IN Pending / In_Progress<br/>AND compliance_deadline < today}
    B --> C[Set compliance_status = Non_Complied]
    C --> D[Emit SITE_INSTRUCTION_NON_COMPLIED<br/>audit event]
    D --> E[Emit SITE_INSTRUCTION_NON_COMPLIED<br/>DQ trigger High<br/>to PROJECT_DIRECTOR + PMO_DIRECTOR<br/>24hr SLA]
    E --> F[Emit cross-module event to M05<br/>internal API for potential<br/>NCR-basis assessment]

    style C fill:#fee2e2
    style E fill:#fee2e2
```

### Daily Acknowledgement Sweep (BR-13-024)

```mermaid
flowchart TD
    A[Daily Acknowledgement sweep] --> B{For each DistributionList row<br/>where received_at IS NOT NULL<br/>AND acknowledged_at IS NULL<br/>AND received_at + acknowledgement_timeout_days < today<br/>default 7 days}
    B --> C[Emit ACKNOWLEDGEMENT_OVERDUE<br/>DQ trigger Medium<br/>to PROJECT_DIRECTOR<br/>24hr SLA to chase recipient]
    C --> D[Continue to next row]
```

### Audit Events Emitted

| Event | Trigger BR | Severity |
|---|---|---|
| `PROJECT_CORRESPONDENCE_INITIALISED` | BR-13-001 | Info |
| `CORRESPONDENCE_CREATED` | BR-13-002..005 | Info |
| `CORRESPONDENCE_CLASSIFIED` | (type/contractual_weight change) | Info |
| `CORRESPONDENCE_SENT` | (outgoing transmission) | Info |
| `CORRESPONDENCE_RESPONDED` | BR-13-008 | Info |
| `CORRESPONDENCE_ARCHIVED` | (soft-delete) | Info |
| `NOTICE_SLA_WARNING` | BR-13-006 | Medium |
| `NOTICE_SLA_BREACH` | BR-13-007 | High |
| `NOTICE_SLA_OVERDUE_RESOLVED` | (responded after breach) | Info |
| `SITE_INSTRUCTION_NON_COMPLIED` | BR-13-022 | High |
| `DISTRIBUTION_SENT` | BR-13-023 | Info |
| `ACKNOWLEDGEMENT_RECORDED` | (recipient acknowledges) | Info |
| `ACKNOWLEDGEMENT_OVERDUE` | BR-13-024 | Medium |

### Decision Queue Triggers Emitted

| Trigger | Severity | Owner | SLA | Source BR |
|---|---|---|---|---|
| `NOTICE_SLA_WARNING` | Medium | Recipient or PROJECT_DIRECTOR | per remaining window | BR-13-006 |
| `NOTICE_SLA_BREACH` | High | PROJECT_DIRECTOR | 24 hr | BR-13-007 |
| `SITE_INSTRUCTION_NON_COMPLIED` | High | PROJECT_DIRECTOR + PMO_DIRECTOR | 24 hr | BR-13-022 |
| `ACKNOWLEDGEMENT_OVERDUE` | Medium | PROJECT_DIRECTOR | 24 hr | BR-13-024 |

---

## WF-13-002 — M05 Correspondence Trigger + Risk_Noted Promotion + RFI Impact

> **Decision:** Has correspondence been correctly flagged as triggering a formal M05 action (EWN, VO, EOT, or new Risk)? Has a meeting Risk_Noted entry been promoted to M05.Risk?
> **Primary Role:** PROJECT_DIRECTOR or PMO_DIRECTOR (only roles authorised to set `triggers_m05 = true` per BR-13-009).
> **BR Coverage:** BR-13-009 (triggers_m05 RBAC restricted), BR-13-010 (triggers_m05 → emit CORRESPONDENCE_M05_FLAGGED), BR-13-011 (Risk_Noted MinutesEntry → M05.Risk promotion), BR-13-012 (RFI cost/schedule impact → emit RFI_IMPACT_FLAGGED).

### M05 Trigger Flow

```mermaid
flowchart TD
    A[Caller attempts FLAG_M05_TRIGGER action<br/>Set Correspondence.triggers_m05 = true] --> B{Caller role}
    B -->|PROJECT_DIRECTOR<br/>OR PMO_DIRECTOR| C[Permission check passes<br/>per BR-13-009]
    B -->|Any other role| D[API rejects 403<br/>FLAG_M05_RBAC_VIOLATION<br/>per BR-13-009]
    C --> E{m05_trigger_reason<br/>populated ≥ 50 chars?}
    E -->|NO| F[Block save:<br/>M05_TRIGGER_REASON_REQUIRED]
    E -->|YES| G[Set Correspondence.triggers_m05 = true]
    G --> H[CorrespondenceStatusLog row append-only<br/>event_type = TriggersM05_Flipped]
    H --> I[Emit CORRESPONDENCE_M05_FLAGGED event<br/>to M05 internal API per BR-13-010<br/>Payload: correspondence_id, project_id,<br/>correspondence_type, contractual_weight,<br/>subject, m05_trigger_reason, sent_date]
    I --> J[M05 receives signal:<br/>evaluates whether to open EWN / VO / EOT<br/>M05 owns the decision per OQ-1.1<br/>M13 does not prescribe action]
    J --> K[Fire-and-forget signal<br/>M13 records timestamp + actor<br/>No callback expected from M05]

    style D fill:#fee2e2
    style F fill:#fee2e2
    style I fill:#fef3c7
```

### Risk_Noted Promotion to M05.Risk (BR-13-011)

```mermaid
flowchart TD
    A[MinutesEntry exists<br/>entry_type = Risk_Noted] --> B{Caller role}
    B -->|PROJECT_DIRECTOR<br/>OR PMO_DIRECTOR| C[Permission check passes<br/>per Block 4a PROMOTE_RISK_NOTED_TO_M05]
    B -->|Any other role| D[API rejects 403]
    C --> E[PROMOTE_RISK_NOTED_TO_M05 action]
    E --> F[Create new M05.Risk row<br/>via M05 internal API:<br/>category derived from entry text<br/>title = first 200 chars of entry_text<br/>description = full entry_text<br/>status = Draft per OQ-2.6 broad-raise]
    F --> G[Update MinutesEntry:<br/>promoted_to_m05_risk_id = new Risk.id<br/>One-way; not reversible<br/>per BR-13-011]
    G --> H[Emit RISK_PROMOTED_FROM_MINUTES audit event<br/>Severity: Medium]
    H --> I[M05.Risk continues normal lifecycle<br/>per WF-05-001<br/>Subsequent state machine independent of M13]

    style D fill:#fee2e2
    style G fill:#fef3c7
```

### RFI Impact Cross-Module Flag (BR-13-012)

```mermaid
flowchart LR
    A[RFI updated:<br/>cost_impact = true<br/>OR schedule_impact = true] --> B[Emit RFI_IMPACT_FLAGGED event<br/>to M05 internal API per BR-13-012]
    B --> C[M05 receives:<br/>reviews RFI for potential<br/>EWN / VO opening]
    A --> D[Emit RFI_IMPACT_REQUIRES_M05_REVIEW<br/>DQ trigger to M11 stub]
    D --> E[M11 stub queues<br/>for M11 ActionRegister consumption<br/>when M11 built]
```

### Audit Events Emitted

| Event | Trigger BR | Severity |
|---|---|---|
| `CORRESPONDENCE_M05_FLAGGED` | BR-13-009 + BR-13-010 | High |
| `RISK_PROMOTED_FROM_MINUTES` | BR-13-011 | Medium |
| `RFI_IMPACT_FLAGGED` | BR-13-012 | High |

### Decision Queue Triggers Emitted

| Trigger | Severity | Owner | SLA | Source BR |
|---|---|---|---|---|
| `RFI_IMPACT_REQUIRES_M05_REVIEW` (informational; routed via M11 stub) | Medium (M05-defined when M05 acts) | M11 → M05 routing | per M11 SLA | BR-13-012 |

### Cross-Module Events

| Direction | Event | Target | Trigger | Speed |
|---|---|---|---|---|
| OUT | `CORRESPONDENCE_M05_FLAGGED` | M05 internal API | Correspondence.triggers_m05 → true | 🔴 Real-time |
| OUT | M05.Risk creation request | M05 internal API | PROMOTE_RISK_NOTED_TO_M05 action | 🔴 Real-time |
| OUT | `RFI_IMPACT_FLAGGED` | M05 internal API | RFI cost_impact OR schedule_impact = true | 🔴 Real-time |

---

## WF-13-003 — Meeting Management + Minutes Approval + Action Items

> **Decision:** Have meeting minutes been recorded, circulated, and approved with all action items assigned and tracked?
> **Primary Role:** Meeting chairperson (drafts minutes) + attendees (review + dispute) + PMO_DIRECTOR / PROJECT_DIRECTOR (approve).
> **BR Coverage:** BR-13-013 (Minutes Approved requires action_item_id populated for all Action entries), BR-13-014 (Auto-create ActionItem from MinutesEntry type=Action), BR-13-015 (Minutes Disputed requires note ≥100 chars), BR-13-016 (Daily ActionItem SLA sweep), BR-13-017 (Meeting minutes circulation timer 48hr).

### Meeting + Minutes State Machine

```mermaid
stateDiagram-v2
    [*] --> Scheduled: SCHEDULE_MEETING action
    Scheduled --> Held: meeting_end_time recorded
    Held --> Draft: minutes_status = Draft<br/>(DRAFT_MINUTES action)
    Draft --> Circulated: CIRCULATE_MINUTES action<br/>by PMO_DIRECTOR/PROJECT_DIRECTOR
    Circulated --> Approved: APPROVE_MINUTES action<br/>by PMO_DIRECTOR/PROJECT_DIRECTOR<br/>(BR-13-013 requires all Action<br/>entries have action_item_id)
    Circulated --> Disputed: DISPUTE_MINUTES action<br/>(BR-13-015 requires note ≥100 chars)
    Disputed --> Approved: PMO_DIRECTOR resolves<br/>(BR-13-015)
    Approved --> [*]
```

### MinutesEntry Auto-Action Creation (BR-13-014)

```mermaid
flowchart LR
    A[ADD_MINUTES_ENTRY action<br/>during Draft phase] --> B{entry_type = Action?}
    B -->|YES| C[Auto-create ActionItem row:<br/>source = Meeting<br/>source_meeting_id = parent meeting<br/>source_minutes_entry_id = this entry<br/>title = first 200 chars of entry_text<br/>description = full entry_text<br/>status = Open<br/>due_date = required at creation<br/>owner = required CHECK exactly-one of<br/>owner_user_id / owner_party_id]
    C --> D[Update MinutesEntry:<br/>action_item_id = ActionItem.id]
    D --> E[ACTION_ITEM_CREATED audit event<br/>MINUTES_ENTRY_ADDED audit event]
    B -->|NO| F[Persist MinutesEntry only<br/>MINUTES_ENTRY_ADDED audit]
    B -->|Risk_Noted| G[Persist MinutesEntry<br/>Eligible for promotion to M05.Risk<br/>per BR-13-011 — see WF-13-002]
```

### Minutes Approval Flow

```mermaid
flowchart TD
    A[Meeting held] --> B[Minutes drafted by chairperson<br/>or PROJECT_DIRECTOR<br/>minutes_status = Draft<br/>MINUTES_DRAFTED audit]
    B --> C[CIRCULATE_MINUTES action<br/>by PROJECT_DIRECTOR/PMO_DIRECTOR<br/>per Block 4a CIRCULATE_MINUTES]
    C --> D[minutes_status: Draft → Circulated<br/>minutes_circulated_at = now<br/>MINUTES_CIRCULATED audit]
    D --> E{Attendee disputes?<br/>BR-13-015}
    E -->|YES| F[DISPUTE_MINUTES action<br/>minutes_dispute_note ≥ 100 chars required]
    F --> G[minutes_status: Circulated → Disputed<br/>MEETING_MINUTES_DISPUTED audit<br/>Emit DQ trigger MEETING_MINUTES_DISPUTED<br/>Medium to PMO_DIRECTOR 48hr SLA]
    G --> H[PMO_DIRECTOR RESOLVE_DISPUTED_MINUTES action<br/>per Block 4a]
    H --> I[minutes_status: Disputed → Approved<br/>MEETING_MINUTES_APPROVED audit]
    E -->|NO| J[APPROVE_MINUTES action<br/>by PROJECT_DIRECTOR or PMO_DIRECTOR]
    J --> K{All MinutesEntry rows<br/>where entry_type=Action<br/>have action_item_id populated?<br/>BR-13-013}
    K -->|NO| L[Block transition:<br/>ACTION_ENTRIES_MUST_HAVE_ACTION_ITEMS]
    K -->|YES| M[minutes_status: Circulated → Approved<br/>minutes_approved_at = now<br/>minutes_approved_by_user_id = caller<br/>MEETING_MINUTES_APPROVED audit<br/>MeetingMinutesAuditLog row append-only]

    style F fill:#fef3c7
    style G fill:#fef3c7
    style L fill:#fee2e2
    style M fill:#dcfce7
```

### Minutes Circulation Timer (BR-13-017)

```mermaid
flowchart TD
    A[Daily Minutes Circulation sweep<br/>🟢 24hr batch] --> B{For each MeetingRegister<br/>where meeting_end_time < now<br/>AND minutes_status IN Draft<br/>AND meeting_end_time + 48hr < now<br/>per ProjectCorrespondenceConfig.<br/>meeting_minutes_circulation_hours}
    B --> C[Emit MEETING_MINUTES_NOT_CIRCULATED<br/>DQ trigger Low<br/>to chairperson<br/>24hr SLA]

    style C fill:#fef3c7
```

### ActionItem State Machine + Daily SLA Sweep (BR-13-016)

```mermaid
stateDiagram-v2
    [*] --> Open: Auto-created from MinutesEntry<br/>OR manual create<br/>(BR-13-014)
    Open --> In_Progress: Owner acknowledges
    In_Progress --> Completed: Owner marks complete<br/>closed_at set
    Open --> Cancelled: Cancelled (closure_note ≥50 chars)
    In_Progress --> Cancelled: Cancelled (closure_note required)
    Open --> Deferred: Deferred (closure_note required;<br/>new due_date may be set)
    In_Progress --> Deferred: Deferred
    Open --> Overdue: due_date < today<br/>BR-13-016 daily sweep
    In_Progress --> Overdue: due_date < today<br/>BR-13-016 daily sweep
    Overdue --> Completed: late completion
    Overdue --> Cancelled: Cancelled
    Completed --> [*]
    Cancelled --> [*]
    Deferred --> [*]: Deferred terminal until reactivated
```

```mermaid
flowchart TD
    A[Daily ActionItem SLA sweep<br/>🟢 24hr batch] --> B{For each ActionItem<br/>where status IN Open / In_Progress<br/>AND due_date < today}
    B --> C[Set status = Overdue if not already<br/>Set escalated_to_m11 = true<br/>per BR-13-016]
    C --> D[Emit ACTION_ITEM_OVERDUE audit event]
    D --> E[Emit ACTION_ITEM_OVERDUE DQ trigger<br/>Medium → escalating to High after 7 days<br/>to ActionItem.owner_user_id<br/>or PROJECT_DIRECTOR if external party owner]

    style C fill:#fef3c7
    style E fill:#fef3c7
```

### Audit Events Emitted

| Event | Trigger BR | Severity |
|---|---|---|
| `MEETING_SCHEDULED` | (MeetingRegister.create) | Info |
| `MEETING_HELD` | (meeting_end_time recorded) | Info |
| `MINUTES_DRAFTED` | (status → Draft) | Info |
| `MINUTES_CIRCULATED` | (status → Circulated) | Info |
| `MEETING_MINUTES_APPROVED` | BR-13-013 | Info |
| `MEETING_MINUTES_DISPUTED` | BR-13-015 | Medium |
| `MINUTES_ENTRY_ADDED` | (MinutesEntry.create) | Info |
| `ACTION_ITEM_CREATED` | BR-13-014 | Info |
| `ACTION_ITEM_OWNER_NOTIFIED` | (post-create) | Info |
| `ACTION_ITEM_OVERDUE` | BR-13-016 | Medium → escalating |

### Decision Queue Triggers Emitted

| Trigger | Severity | Owner | SLA | Source BR |
|---|---|---|---|---|
| `MEETING_MINUTES_DISPUTED` | Medium | PMO_DIRECTOR | 48 hr | BR-13-015 |
| `MEETING_MINUTES_NOT_CIRCULATED` | Low | Meeting chairperson | 24 hr | BR-13-017 |
| `ACTION_ITEM_OVERDUE` | Medium → High escalating | ActionItem.owner_user_id or PROJECT_DIRECTOR | per overdue duration | BR-13-016 |

---

## WF-13-004 — RFI Lifecycle

> **Decision:** Has the contractor's Request for Information received a timely, documented response — and has any design / cost / schedule impact been escalated appropriately?
> **Primary Role:** SITE_MANAGER / PROJECT_DIRECTOR / PLANNING_ENGINEER / QS_MANAGER / PROCUREMENT_OFFICER (raise) → QS_MANAGER / PROJECT_DIRECTOR / PMO_DIRECTOR (respond) → PROJECT_DIRECTOR / PMO_DIRECTOR (close); PMO_DIRECTOR only for reopen.
> **BR Coverage:** BR-13-018 (RFI response_due_date auto-compute), BR-13-019 (RFI Responded requires response_text), BR-13-020 (Daily RFI SLA sweep), BR-13-021 (RFI close reopen requires PMO_DIRECTOR).

### RFI State Machine

```mermaid
stateDiagram-v2
    [*] --> Open: RAISE_RFI action<br/>response_due_date auto-set<br/>(BR-13-018)
    Open --> Responded: RESPOND_TO_RFI action<br/>response_text ≥ 50 chars<br/>(BR-13-019)
    Open --> Overdue: response_due_date < today<br/>(BR-13-020 daily sweep)
    Overdue --> Responded: late response captured
    Responded --> Closed: CLOSE_RFI action<br/>by PROJECT_DIRECTOR/PMO_DIRECTOR
    Closed --> Open: REOPEN_RFI action<br/>PMO_DIRECTOR only<br/>(BR-13-021)
    Closed --> [*]
```

### Runtime Flow

```mermaid
flowchart TD
    A[Authorised role per Block 4a<br/>RAISE_RFI action] --> B[RFI created:<br/>question_text ≥ 100 chars<br/>raised_by_user_id<br/>or raised_by_party_id<br/>addressed_to free-text<br/>status = Open]
    B --> C[Compute response_due_date:<br/>raised_at_date + ProjectCorrespondenceConfig.rfi_sla_days<br/>default 14 days<br/>per BR-13-018]
    C --> D[Persist RFI row<br/>RFI_RAISED audit event]

    D --> E[Daily RFI SLA sweep<br/>🟢 24hr batch<br/>per BR-13-020]
    E --> F{response_due_date < today<br/>AND status = Open?}
    F -->|YES| G[Set status = Overdue<br/>Emit RFI_RESPONSE_OVERDUE<br/>DQ trigger Medium<br/>to PROJECT_DIRECTOR + PLANNING_ENGINEER<br/>48hr SLA]
    F -->|NO| H[Continue]

    D --> I[QS_MANAGER / PROJECT_DIRECTOR /<br/>PMO_DIRECTOR<br/>RESPOND_TO_RFI action<br/>per Block 4a]
    I --> J{response_text<br/>populated ≥ 50 chars?<br/>BR-13-019}
    J -->|NO| K[Block transition:<br/>RESPONSE_TEXT_REQUIRED]
    J -->|YES| L[status: Open → Responded<br/>responded_at = now<br/>responded_by_user_id = caller<br/>RFI_RESPONDED audit event]
    L --> M{cost_impact = true<br/>OR schedule_impact = true?<br/>BR-13-012 / WF-13-002]
    M -->|YES| N[Emit RFI_IMPACT_FLAGGED to M05<br/>see WF-13-002 cross-module]
    M -->|NO| O[No M05 trigger]
    N --> P[CLOSE_RFI action<br/>PROJECT_DIRECTOR or PMO_DIRECTOR]
    O --> P
    P --> Q[status: Responded → Closed<br/>closed_at = now<br/>RFI_CLOSED audit event<br/>RFIStatusLog row append-only]

    Q --> R{Reopen needed later?}
    R -->|YES| S{Caller is PMO_DIRECTOR?<br/>BR-13-021}
    S -->|YES| T[REOPEN_RFI action<br/>status: Closed → Open<br/>Audit log preserved]
    S -->|NO| U[API rejects 403<br/>REOPEN_REQUIRES_PMO_DIRECTOR]

    style K fill:#fee2e2
    style G fill:#fef3c7
    style U fill:#fee2e2
    style L fill:#dcfce7
    style Q fill:#dcfce7
```

### Audit Events Emitted

| Event | Trigger BR | Severity |
|---|---|---|
| `RFI_RAISED` | BR-13-018 | Info |
| `RFI_RESPONDED` | BR-13-019 | Info |
| `RFI_CLOSED` | (state → Closed) | Info |
| `RFI_RESPONSE_OVERDUE` | BR-13-020 | Medium |
| `RFI_IMPACT_FLAGGED` | BR-13-012 (in WF-13-002) | High |

### Decision Queue Triggers Emitted

| Trigger | Severity | Owner | SLA | Source BR |
|---|---|---|---|---|
| `RFI_RESPONSE_OVERDUE` | Medium | PROJECT_DIRECTOR + PLANNING_ENGINEER | 48 hr | BR-13-020 |

### Failure Modes

| Failure | Behaviour |
|---|---|
| Caller attempts CLOSE_RFI without response | Block transition; RFI cannot move to Closed without prior Responded transition |
| Non-PMO_DIRECTOR attempts to reopen Closed RFI | API rejects 403 per BR-13-021 |
| Response text < 50 chars | Block transition with reason RESPONSE_TEXT_TOO_SHORT per BR-13-019 |

---

## BR Coverage Matrix — M13

Every BR in M13 Spec v1.0 (R34) Block 6 mapped to at least one workflow. **0 coverage gaps.**

| BR Code | BR Summary | WF-13-001 Correspondence | WF-13-002 M05 Trigger | WF-13-003 Meetings | WF-13-004 RFI |
|---|---|---|---|---|---|
| BR-13-001 | Project Activation auto-create config | ✓ | | | |
| BR-13-002 | Notice contractual_reference required | ✓ | | | |
| BR-13-003 | Site Instruction compliance_deadline required | ✓ | | | |
| BR-13-004 | response_required auto-set | ✓ | | | |
| BR-13-005 | response_due_date auto-compute | ✓ | | | |
| BR-13-006 | Notice SLA Warning sweep (80%) | ✓ | | | |
| BR-13-007 | Notice SLA Breach sweep (100%) | ✓ | | | |
| BR-13-008 | Correspondence respond action | ✓ | | | |
| BR-13-009 | triggers_m05 RBAC restricted | | ✓ | | |
| BR-13-010 | triggers_m05 → emit CORRESPONDENCE_M05_FLAGGED | | ✓ | | |
| BR-13-011 | Risk_Noted promotion to M05.Risk | | ✓ | | |
| BR-13-012 | RFI cost/schedule impact emit | | ✓ | | ✓ |
| BR-13-013 | Minutes Approved requires action_item_id | | | ✓ | |
| BR-13-014 | Auto-create ActionItem from MinutesEntry | | | ✓ | |
| BR-13-015 | Minutes Disputed requires note ≥100 chars | | | ✓ | |
| BR-13-016 | Daily ActionItem SLA sweep | | | ✓ | |
| BR-13-017 | Meeting minutes circulation timer 48hr | | | ✓ | |
| BR-13-018 | RFI response_due_date auto-compute | | | | ✓ |
| BR-13-019 | RFI Responded requires response_text | | | | ✓ |
| BR-13-020 | Daily RFI SLA sweep | | | | ✓ |
| BR-13-021 | RFI close reopen requires PMO_DIRECTOR | | | | ✓ |
| BR-13-022 | Site Instruction non-compliance sweep | ✓ | | | |
| BR-13-023 | Distribution sent event | ✓ | | | |
| BR-13-024 | Daily Acknowledgement sweep | ✓ | | | |

**Coverage:** 24 / 24 BRs covered. **0 gaps.**

---

*v1.0 — Workflows LOCKED 2026-05-04 (Round 36). C1b batch with M05 Workflows. M13 build-ready after this round.*

---

## M05+M13 Batch Status (post-R36)

```
✅ R31  M05 Brief v1.0a (7-state VO patch R33)
✅ R32  M13 Brief v1.0
✅ R33  M05 Spec v1.0 + X8 v0.7
✅ R34  M13 Spec v1.0 + X8 v0.8 + X9 v0.5
✅ R35  M05 + M13 Wireframes v1.0 (C1b batch)
✅ R36  M05 + M13 Workflows v1.0 (C1b batch)  ← THIS ROUND
       ↓
       M05 + M13 BUILD-READY
```

### Next Rounds (per Build Execution Plan §3a)

**Build-track:**
- R37 — Monorepo scaffold + 10 ADRs + CI workflow + Docker Compose + Keycloak realm seed (first code in repo)

**Spec-track (parallel):**
- R37 — M07 EVMEngine Brief (M05 contract `RISK_ADJUSTED_EAC_DELTA` event now locked in M05 Block 7b — M07 unblocked)
