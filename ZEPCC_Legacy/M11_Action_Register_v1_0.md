# M11 — Action Register
## Module Specification v1.0
**Status:** Draft — Pending PMO Director Review | **Locked:** No
**Spec Author:** PMO Director | **Date:** 2026-05-02
**Reference Standards:** EPCC_Engineering_Standards_v1_2.md
**Layer:** Command (alongside M10)
**Build Priority:** Sprint 3 (after M01–M10 core build, before first go-live)

---

## CHANGE LOG

| Version | Date | Change Summary |
|---------|------|----------------|
| v1.0 | 2026-05-02 | Initial specification. Decision: Action Register (not general task manager). Closes Layer 2 operational follow-up gap identified in design review. |

---

## BLOCK 1 — Identity

| Field | Value |
|---|---|
| Module ID | M11 |
| Module Name | Action Register |
| System Layer | Command (read-write cross-cutting — unique position) |
| Navigation Section | Command (below M10 EPCC Command) |
| Module Code | `M11` |
| Module Icon | `ClipboardList` (Lucide) |

### Decision This Module Enables

> *"What follow-up actions have been assigned to whom, on which project, by when — and which ones are overdue?"*

This is distinct from the Decision Queue (M10), which answers: *"What governance decisions are pending that block the system?"*

The Action Register answers: *"What operational follow-up work has been assigned that the system cannot enforce but the team must track?"*

### Users

| Role | Access Level |
|---|---|
| PMO Director | Full — create, assign, view all projects, close any action |
| Portfolio Manager | Full — create, assign, view all projects, close any action |
| Project Director | Full — create, assign, view own projects only |
| Planning Engineer | Create + edit own actions, view all actions on own projects |
| QS Manager | Create + edit own actions, view all actions on own projects |
| Finance Lead | Create + edit own actions, view all actions on own projects |
| Procurement Officer | Create + edit own actions, view all actions on own projects |
| Site Manager | Create + edit own actions, view own package actions only |
| Read-Only | View only — no create, no edit, no close |
| System Admin | View only — no create (System Admin is not a project role) |

---

## BLOCK 2 — Scope Boundary

### INCLUDES

| Capability | Description |
|---|---|
| ActionItem creation | Any EPCC user with a project role can create an action on that project |
| Manual action creation | Free-form actions raised directly by a user |
| System-spawned action creation | Certain business rules in M05/M06/M07/M08/M09 can create ActionItems automatically (see Block 7) |
| Assignment to EPCC project role | Assignee must be a named EPCC user holding a role on that project |
| Optional entity linkage | Action can be linked to a specific DecisionQueueItem, Risk, Milestone, BOQItem, or Gate |
| Priority setting | High / Medium / Low — set by raiser at creation |
| Due date | Mandatory. Must be a future date at creation. |
| Status tracking | Open → In_Progress → Done / Cancelled |
| Overdue detection | Automatic — any action past due_date with status ≠ Done/Cancelled |
| M10 visibility | Overdue action count surfaced as a secondary badge on M10 project cards |
| M11 dashboard | Dedicated view: all actions across portfolio, filterable by project/assignee/status/overdue |
| Reminder notifications | WhatsApp + in-app reminder 24hr before due_date |
| Overdue notifications | WhatsApp + in-app alert when action becomes overdue |
| Completion audit | Who closed, when, with what note |
| Soft delete | Cancelled actions are soft-deleted (`is_active = false`) — never hard-deleted |

### EXCLUDES

| Excluded | Reason / Where It Lives |
|---|---|
| Subtasks / nested actions | Scope contamination — keep the entity flat and simple |
| Comment threads | WhatsApp handles discussion. Action Register handles assignment + tracking only. |
| File attachments on actions | Attachments belong on the linked entity (Risk, Gate, BOQItem). Not on the action itself. |
| Personal / non-project actions | `project_id` is mandatory. Personal reminders are out of scope. |
| Governance enforcement | Actions have no GovernanceBreachLog entries, no gate-blocking capability. That is the Decision Queue's role. |
| Automatic SLA escalation chain | Action Register has soft visibility (overdue badge). No forced escalation. No governance breach. This is deliberate — it is NOT the Decision Queue. |
| Task dependencies / sequencing | Build complexity not justified. Gantt-style task sequencing lives in M03 Planning. |
| Time tracking / hours logging | Out of scope. Not an EPCC concern. |
| Cross-tenant actions | Actions are strictly within a single tenant and single project. |
| Bulk import of actions | No HDI for actions. Manual or system-spawned only. |
| Mobile app (Phase 1) | Phase 2. In-browser responsive is sufficient for Phase 1. |

---

## BLOCK 3 — Data Architecture

### 3a. Primary Entity: `ActionItem`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `action_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | FK → TenantMaster | SYSTEM |
| `project_id` | UUID | Y | FK → M01 Project. Mandatory — no project-less actions. | INPUT / SYSTEM |
| `action_code` | VARCHAR(20) | Y | CALC: `ACT-{project_seq}-{padded_serial}` e.g. `ACT-001-0042`. Unique per project. | CALC |
| `title` | VARCHAR(200) | Y | Min 10 chars. Sentence case. Max 200 chars. Clear action verb required — validated client-side. | INPUT |
| `description` | TEXT | N | Additional context. Max 1,000 chars. | INPUT |
| `raised_by` | UUID | Y | FK → User. Auto-populated from session. | SYSTEM |
| `raised_by_role` | ENUM | Y | Snapshot of raiser's role at time of creation. Preserved if role changes later. | SYSTEM |
| `assigned_to` | UUID | Y | FK → User. Must hold an active role on this project (validated). | INPUT |
| `assigned_to_role` | ENUM | Y | Snapshot of assignee's role at time of assignment. | SYSTEM |
| `due_date` | DATE | Y | Must be ≥ today. Cannot be > 365 days from today (prevents indefinite deferrals). | INPUT |
| `priority` | ENUM | Y | `High / Medium / Low`. Default: Medium. | INPUT |
| `status` | ENUM | Y | `Open / In_Progress / Done / Cancelled`. Default: Open. | INPUT / SYSTEM |
| `module_source` | ENUM | N | `M05 / M06 / M07 / M08 / M09 / M10 / Manual`. Manual = user-created without a system trigger. | SYSTEM |
| `linked_entity_type` | ENUM | N | `DecisionQueueItem / Risk / Milestone / BOQItem / GateCriterion / VO / ComplianceItem / None`. | INPUT |
| `linked_entity_id` | UUID | N | UUID of the linked record. Required if `linked_entity_type ≠ None`. Validated against the correct entity table. | INPUT |
| `linked_entity_display` | VARCHAR(100) | N | CALC: human-readable reference label e.g. `RSK-042 · Drainage design risk` or `SG-7 · Criterion 3`. Computed on save. | CALC |
| `completion_note` | TEXT | N | Required when `status → Done`. Min 20 chars. What was done and what the outcome was. | INPUT |
| `reminder_sent_at` | TIMESTAMP | N | Populated when 24hr reminder notification is dispatched. | SYSTEM |
| `overdue_notified_at` | TIMESTAMP | N | Populated when overdue notification is dispatched. | SYSTEM |
| `is_overdue` | BOOLEAN | Y | CALC: `due_date < today AND status NOT IN (Done, Cancelled)`. Recalculated daily. | CALC |
| `overdue_days` | INTEGER | N | CALC: days since due_date if is_overdue = true. Null otherwise. | CALC |
| `is_active` | BOOLEAN | Y | Default true. Set false on Cancelled (soft delete). | SYSTEM |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `closed_at` | TIMESTAMP | N | Auto-populated when status → Done or Cancelled | SYSTEM |
| `closed_by` | UUID | N | FK → User. Auto-populated on close. | SYSTEM |

---

### 3b. Supporting Entity: `ActionItemAuditLog`

Immutable record of every status change on every ActionItem. Cannot be edited or deleted.

| Field | Type | Required | Description | Source |
|---|---|---|---|---|
| `audit_id` | UUID | Y | Auto-generated | SYSTEM |
| `action_id` | UUID | Y | FK → ActionItem | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `event_type` | ENUM | Y | `Created / Assigned / Status_Changed / Due_Date_Changed / Priority_Changed / Linked / Closed` | SYSTEM |
| `from_value` | TEXT | N | Previous value (serialised). Null for Created events. | SYSTEM |
| `to_value` | TEXT | N | New value (serialised). | SYSTEM |
| `changed_by` | UUID | Y | User who triggered the change. | SYSTEM |
| `changed_at` | TIMESTAMP | Y | Auto. | SYSTEM |
| `change_note` | TEXT | N | Populated for Status_Changed and Closed events. | INPUT / SYSTEM |

---

### 3c. Supporting Entity: `ActionRegisterConfig`

Per-tenant configuration. One record per tenant, created on provisioning.

| Field | Type | Required | Default | Description | Source |
|---|---|---|---|---|---|
| `config_id` | UUID | Y | Auto | — | SYSTEM |
| `tenant_id` | UUID | Y | — | — | SYSTEM |
| `reminder_hours_before` | INTEGER | Y | 24 | Hours before due_date to send reminder. Range: 4–72. | INPUT (System Admin) |
| `overdue_visibility_in_m10` | BOOLEAN | Y | true | Show overdue action count badge on M10 project cards. | INPUT (PMO Director) |
| `allow_system_spawned_actions` | BOOLEAN | Y | true | Allow M05/M06/M07/M08/M09 to auto-create ActionItems. | INPUT (PMO Director) |
| `updated_by` | UUID | Y | — | Last updated by (System Admin or PMO Director only). | SYSTEM |
| `updated_at` | TIMESTAMP | Y | — | Auto. | SYSTEM |

---

## BLOCK 4 — Data Population Rules

### 4a. Role Permission Matrix

| Action | PMO Dir | Portfolio Mgr | Project Dir | Planning Eng | QS Mgr | Finance Lead | Procurement | Site Mgr | Read-Only |
|---|---|---|---|---|---|---|---|---|---|
| Create action (any project) | ✅ | ✅ | ✅ (own) | ✅ (own) | ✅ (own) | ✅ (own) | ✅ (own) | ✅ (own pkg) | ❌ |
| Assign to any role | ✅ | ✅ | ✅ (own) | ✅ (own) | ✅ (own) | ✅ (own) | ✅ (own) | ❌ | ❌ |
| Reassign | ✅ | ✅ | ✅ (own) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Change due date | ✅ | ✅ | ✅ (own) | Own only | Own only | Own only | Own only | ❌ | ❌ |
| Change priority | ✅ | ✅ | ✅ (own) | Own only | Own only | Own only | Own only | ❌ | ❌ |
| Mark In_Progress | ✅ | ✅ | ✅ | Assignee | Assignee | Assignee | Assignee | Assignee | ❌ |
| Mark Done | ✅ | ✅ | ✅ (own) | Assignee | Assignee | Assignee | Assignee | Assignee | ❌ |
| Cancel action | ✅ | ✅ | ✅ (own) | Raiser | Raiser | Raiser | Raiser | ❌ | ❌ |
| View all project actions | ✅ | ✅ | ✅ (own) | ✅ (own) | ✅ (own) | ✅ (own) | ✅ (own) | Own pkg | ✅ (own) |
| View cross-project actions | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Configure ActionRegisterConfig | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### 4b. Mandatory Fields at Creation

The following fields are mandatory and must be provided or auto-populated at the point of creation. An action cannot be saved without all of these:

```
project_id        → Mandatory. Must be an active project.
title             → Min 10 chars. Clear action verb.
assigned_to       → Must be an active EPCC user on this project.
due_date          → Must be ≥ today.
priority          → Defaults to Medium if not explicitly set.
```

The following fields are optional at creation:
```
description       → Recommended but not enforced.
linked_entity     → Encouraged when action stems from a specific record.
```

### 4c. Entry Method Summary

| Field | How Populated |
|---|---|
| All core fields | UI form (M11 create action panel or M11 dashboard quick-create) |
| `module_source` | Auto-set to `Manual` on UI creation; set to module code on system-spawned |
| `linked_entity` | Optional link picker — user selects entity type then searches records |
| `action_code` | Never user-entered — always CALC |
| `raised_by` | Always from authenticated session — never editable |
| `is_overdue`, `overdue_days` | Recalculated by Celery Beat daily at 6am IST |

---

## BLOCK 5 — Filters and Views

### 5a. M11 Dashboard (Action Register Home)

**Primary view for PMO Director / Portfolio Manager — cross-project:**

```
Header row:
  Total Actions | Open | In Progress | Done (30d) | Overdue

Filter bar:
  Project (multi-select) | Assignee (multi-select) | Priority | Status | Overdue only (toggle)
  Module Source | Linked Entity Type | Due Date range

Main table:
  ACT code | Title | Project | Assigned To | Priority | Due Date | Status | Overdue Days | Module
  Sort: Overdue → High → Medium → Low → by Due Date (default)
  RAG row highlighting:
    Overdue → red left border + red-dim row
    High priority + due within 48hr → amber left border + amber-dim row
    Done → neutral, muted text
```

**Secondary view for Project roles — single project:**

```
Scoped to their project only.
Same filter bar minus Project selector.
Additional toggle: "My Actions Only" (default on for non-PMO roles)
```

### 5b. M10 Integration Surface

```
Project card badge (M10 portfolio grid):
  If overdue_action_count > 0:
    Badge: [N ACTIONS OVERDUE] — amber if ≤2, red if >2
    Clicking badge → navigates to M11 filtered to that project, overdue only

Project detail panel (M10 right panel):
  Action Register mini-panel:
    "3 Open · 1 Overdue" summary link
    Last 3 open actions (title, assignee, due date, priority)
    [View All Actions] → navigates to M11 scoped to project
```

### 5c. Context Panel on Any Module Page

When viewing a record that can be linked (Risk in M05, Gate in M08, etc.) a collapsible `Actions` panel is available at the bottom of the detail view:

```
[+ Create Action for this record]
List of actions linked to this specific entity:
  title | assignee | due date | status
  "No actions yet" empty state if none exist
```

This means a user on the M08 Gate Review page can see all open actions linked to that gate without navigating away.

---

## BLOCK 6 — Business Rules

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---|---|---|---|---|
| BR-11-001 | ActionItem creation attempted | Validate: (1) `assigned_to` is an active EPCC user with a role on `project_id`. (2) `due_date` ≥ today. (3) `due_date` ≤ today + 365 days. (4) `title` ≥ 10 chars. (5) If `linked_entity_type ≠ None`, `linked_entity_id` resolves to an existing record of the correct entity type. | PASS → create record. FAIL → HTTP 422 with specific field error. | 🔴 Real-time |
| BR-11-002 | ActionItem created successfully | Dispatch notification to `assigned_to`: "Action assigned: {title}. Due: {due_date}. Raised by: {raised_by_name}. Project: {project_code}." Channels: in-app + WhatsApp (if user has WhatsApp notifications enabled for M11). | Notification dispatched. `ActionItemAuditLog` entry: `event_type = Created`. | 🔴 Real-time |
| BR-11-003 | ActionItem.status set to In_Progress | Validate: only `assigned_to`, PMO Director, Portfolio Manager, or Project Director (own project) can set In_Progress. | Status updated. AuditLog entry. No notification required. | 🔴 Real-time |
| BR-11-004 | ActionItem.status set to Done | Validate: `completion_note` ≥ 20 chars required. Only `assigned_to` or roles with close permission can mark Done. | Status updated. `closed_at` = NOW(). `closed_by` populated. AuditLog entry (`event_type = Closed`, `to_value = Done`, `change_note = completion_note`). Notification to `raised_by` if raiser ≠ assignee: "Action completed: {title}." | 🔴 Real-time |
| BR-11-005 | ActionItem.status set to Cancelled | Validate: only `raised_by`, PMO Director, or Portfolio Manager can cancel. `is_active` → false (soft delete). `closed_at` populated. | AuditLog entry. Optional notification to assignee if cancelled by someone else. | 🔴 Real-time |
| BR-11-006 | ActionItem.due_date changed | Validate: new due_date ≥ today. Only raiser, PMO Director, Portfolio Manager, or Project Director can change due date. | AuditLog entry (`event_type = Due_Date_Changed`, `from_value = old_date`, `to_value = new_date`). Notification to `assigned_to`: "Action due date updated: {title}. New due: {new_due_date}." | 🔴 Real-time |
| BR-11-007 | ActionItem.assigned_to changed (reassignment) | Validate: only PMO Director, Portfolio Manager, or Project Director can reassign. New assignee must hold an active role on the project. | AuditLog entry (`event_type = Assigned`). Notification to new assignee: "Action reassigned to you: {title}. Due: {due_date}." Notification to former assignee: "Action reassigned: {title}." | 🔴 Real-time |
| BR-11-008 | Celery Beat — daily run at 6am IST | For all ActionItems where `status NOT IN (Done, Cancelled)`: recalculate `is_overdue` and `overdue_days`. Update M10 `overdue_action_count` per project. | Batch update. M10 badge counts refreshed. No individual notification from this rule — overdue notification handled by BR-11-009. | 🟢 24hr |
| BR-11-009 | ActionItem becomes overdue (first occurrence — `is_overdue` flips from false to true) | `overdue_notified_at` is null (notification not yet sent). | Dispatch overdue notification to `assigned_to`: "OVERDUE: {title}. Was due: {due_date}. Project: {project_code}." Channels: in-app + WhatsApp. `overdue_notified_at` = NOW(). Notification to `raised_by` (if different): "Action overdue: {title}. Assigned to: {assignee_name}." | 🟢 24hr |
| BR-11-010 | ActionItem due_date is tomorrow (24hr before due) | `reminder_sent_at` is null. `status NOT IN (Done, Cancelled)`. Check `ActionRegisterConfig.reminder_hours_before` for this tenant. | Dispatch reminder to `assigned_to`: "Reminder: {title} is due tomorrow. Project: {project_code}." Channels: in-app only (reminder is lower severity — WhatsApp only if user has M11 WhatsApp reminders enabled). `reminder_sent_at` = NOW(). | 🟢 24hr |
| BR-11-011 | ActionItem overdue ≥ 7 days with no status change | `is_overdue = true` AND `overdue_days ≥ 7` AND `status = Open` (not even In_Progress) | Secondary escalation notification to `raised_by` and Project Director (if not already the raiser): "Action stalled 7+ days: {title}. Assigned to: {assignee_name}. Consider reassignment." No governance breach. No Decision Queue item. Soft visibility only. | 🟢 24hr |
| BR-11-012 | M10 project card rendered | CALC: count of `is_overdue = true AND is_active = true` ActionItems for this project. | `overdue_action_count` exposed via M10 ProjectSummary API response. Rendered as amber/red badge on project card per DashboardCacheConfig TTL. | 🔴 Real-time (cached per ES-M10-v2.2) |

### System-Spawned Action Rules (Cross-Module)

These rules allow other modules to create ActionItems automatically when specific conditions arise. All subject to `ActionRegisterConfig.allow_system_spawned_actions = true`.

| Rule ID | Module Source | Trigger | Action Created | Assigned To |
|---|---|---|---|---|
| BR-11-013 | M05 Risk | Risk score crosses from Medium to High (rag_status escalation) | "Review and update mitigation plan for {risk_code}: {risk_title}" | Risk Owner |
| BR-11-014 | M05 VO | VO raised with cost_impact > ₹50L | "Review VO {vo_code} scope and cost with contractor — confirm or dispute" | QS Manager |
| BR-11-015 | M06 Financial | Payment certificate issued but `payment_status = Overdue` after payment_terms days elapsed | "Follow up on overdue payment: Certificate {cert_code} — ₹{amount}. Contract: {party_name}" | Finance Lead |
| BR-11-016 | M07 EVM | ETC flagged as stale (same trigger as Decision Queue) — in ADDITION to the Decision Queue item | "Update ETC for period {period}: {project_code} — {package_name}" | Planning Engineer |
| BR-11-017 | M08 Gate | GateCriterion fails verification during gate readiness check | "Resolve gate criterion: {criterion_description} — {gate_code}" | Role responsible for that criterion |
| BR-11-018 | M09 Compliance | Compliance item document due within 14 days and not yet uploaded | "Upload compliance document: {item_name} — Due: {due_date}" | Procurement Officer (or PMO Director if no Procurement Officer assigned) |

**Important boundary:** Rules BR-11-013 through BR-11-018 create ActionItems IN ADDITION to any Decision Queue items those same events create. They are not alternatives. The Decision Queue governs. The Action Register assists follow-through.

---

## BLOCK 7 — Integration Points

| Direction | Module | Data Exchanged | Trigger | Speed Tier |
|---|---|---|---|---|
| RECEIVES FROM | M05 Risk & Change | Risk score escalation event (risk_id, risk_code, risk_title, risk_owner_id, project_id) | Risk rag_status → High (BR-11-013) | 🔴 Real-time |
| RECEIVES FROM | M05 Risk & Change | VO raised event (vo_id, vo_code, cost_impact, qs_manager_id, project_id) | VO creation with cost_impact > ₹50L (BR-11-014) | 🔴 Real-time |
| RECEIVES FROM | M06 Financial | Payment overdue event (cert_id, cert_code, amount, finance_lead_id, project_id) | Payment_status = Overdue after terms elapsed (BR-11-015) | 🟡 2-4hr |
| RECEIVES FROM | M07 EVM | ETC stale event (project_id, package_id, period, planning_engineer_id) | Same trigger as DecisionQueueItem ETC_STALE (BR-11-016) | 🔴 Real-time |
| RECEIVES FROM | M08 Gate Control | Gate criterion fail event (criterion_id, criterion_description, gate_id, gate_code, responsible_role, project_id) | GateCriterion verification fails during readiness check (BR-11-017) | 🔴 Real-time |
| RECEIVES FROM | M09 Compliance | Compliance document due-soon event (item_id, item_name, due_date, project_id) | Document due within 14 days, not yet uploaded (BR-11-018) | 🟡 2-4hr |
| SENDS TO | M10 EPCC Command | `overdue_action_count` per project | Daily recalc (BR-11-008) + on each ActionItem status change | 🔴 Real-time + 🟢 24hr |
| SENDS TO | Notification Service | Assignment, reminder, overdue, completion, stale notifications | Per business rules BR-11-002, BR-11-004, BR-11-007, BR-11-009, BR-11-010, BR-11-011 | 🔴 Real-time / 🟢 24hr |

**M11 does NOT send data to:** RecalcQueue, GovernanceBreachLog, AuditLog (core governance systems). M11 has its own `ActionItemAuditLog` — it does not write to the system-wide AuditLog. This is a deliberate boundary. ActionItems are operational, not governance records.

---

## BLOCK 8 — Governance and Audit

### What IS governed in M11

| Governance Mechanism | Implementation |
|---|---|
| Immutable audit trail | `ActionItemAuditLog` — every status change, reassignment, date change, close |
| Soft delete | Cancelled actions: `is_active = false`. Record preserved. Never hard-deleted. |
| Assignee validation | Assignee must hold an active role on the project — prevents assignment to arbitrary users |
| Completion note | Required on Done — creates a searchable record of what was done |
| Role snapshot | `raised_by_role` and `assigned_to_role` snapshotted at creation — preserved if roles change |

### What is deliberately NOT governed in M11

| Not Governed | Rationale |
|---|---|
| Missed ActionItems do NOT trigger GovernanceBreachLog entries | This would conflate operational follow-up with governance decisions. The Decision Queue governs. M11 assists. |
| Overdue ActionItems do NOT block gate passage | Gates are governed by GateCriteria. An overdue ActionItem is not a gate criterion unless explicitly added by the PMO Director as one. |
| No mandatory escalation chain | The soft notification at 7 days overdue (BR-11-011) is the ceiling. No further system escalation. Human judgement governs from there. |

### RBAC Enforcement

All M11 API endpoints enforce `project_id` + `tenant_id` scope checks before any data is returned or written. A user can never read or write ActionItems outside their own tenant and project scope. System Admin has view-only access and cannot create or close actions.

---

## BLOCK 9 — Explicit Exclusions

```
[ ] Subtasks / child actions                    → Flat entity only. No hierarchy.
[ ] Comment threads on actions                  → WhatsApp. Not M11.
[ ] File attachments on ActionItems             → Attach to the linked entity, not the action.
[ ] Personal (non-project) actions              → project_id is mandatory. No exceptions.
[ ] Governance breach logging for missed actions → Decision Queue governs breaches. M11 does not.
[ ] Gate-blocking capability                    → Gates are blocked by GateCriteria. Not by ActionItems.
[ ] Time tracking / effort logging              → Not an EPCC concern.
[ ] Task dependencies / sequencing              → M03 Planning handles project schedule.
[ ] Cross-tenant actions                        → tenant_id is mandatory and scoped.
[ ] Bulk import of actions                      → Manual or system-spawned only.
[ ] Action templates                            → Phase 2 consideration if volume justifies.
[ ] Recurring actions                           → Phase 2 consideration.
[ ] Mobile-native push notifications            → Phase 2. WhatsApp covers Phase 1 mobile.
```

---

## BLOCK 10 — Open Questions

**All v1.0 questions resolved. Zero open questions.**

| # | Question | Resolution |
|---|---|---|
| 1 | Should M11 be a sub-module of M10 or its own module? | Own module (M11). Rationale: it is a cross-cutting write-capable module — any role can create actions from any module context. Sub-moduling it under M10 (read-only) would create a confusing ownership. Standalone M11 with its own navigation entry under the Command section is cleaner. |
| 2 | Should overdue ActionItems create Decision Queue items? | No. Creating a Decision Queue item for an overdue ActionItem would be circular — the ActionItem may itself be a follow-up on a Decision Queue item. The separation must be clean: Decision Queue = governance, M11 = operational follow-up. Overdue visibility in M10 + soft notifications is the correct consequence model. |
| 3 | Should the BR-11-013 through BR-11-018 system-spawned actions duplicate the Decision Queue items those same events already create? | Yes, deliberately. The Decision Queue item demands a decision from a specific role within an SLA, with escalation and governance breach consequences. The ActionItem is the operational follow-up — "do the work." These are complementary, not redundant. A Planning Engineer has a Decision Queue item demanding they update ETC (governance enforcement) AND an ActionItem reminding them of that same obligation (operational visibility). Both serve different purposes for different moments in the workflow. |
| 4 | What happens to an ActionItem if the project is closed? | All open ActionItems are automatically Cancelled (soft delete) when a project reaches SG-11 (project closure gate). The `completion_note` is auto-set to "Auto-cancelled on project closure at SG-11." `closed_by` = system. This ensures no orphan open actions persist after closure. |
| 5 | Should the `due_date` cap of 365 days be configurable? | No. Actions with a due date more than a year away are not operational follow-up — they are project planning items that belong in M03. The 365-day hard cap enforces this boundary. |

---

## IMPLEMENTATION NOTES (for Sprint 3)

**Database:** Single schema migration adds two tables: `action_item` and `action_item_audit_log`. One config table addition: `action_register_config`. No changes to any existing module table.

**API:** 6 endpoints required:
- `POST /projects/{project_id}/actions` — create
- `GET /projects/{project_id}/actions` — list with filters
- `GET /actions/{action_id}` — detail
- `PATCH /actions/{action_id}` — update (status, due_date, priority, assignment, note)
- `GET /portfolio/actions` — cross-project view (PMO Director / Portfolio Manager only)
- `GET /projects/{project_id}/action-count` — overdue count for M10 badge

**Celery Beat jobs added:**
- `recalculate_action_overdue_status` — daily 6am IST (BR-11-008, BR-11-009)
- `send_action_reminders` — daily 8am IST (BR-11-010, BR-11-011)

**Estimated build:** 1 sprint (2 weeks). Frontend: M11 dashboard view, quick-create panel, M10 badge integration, context panel component (reusable across M05/M08/M09 entity detail views).

---

*Spec complete. Zero open questions. Ready for PMO Director review and lock.*
*Memory file update required: §7.139 — M11 Action Register v1.0 decisions.*
