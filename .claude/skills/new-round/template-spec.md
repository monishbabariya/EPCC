# {Module} {ShortName} — Spec v{Major}.{Minor}

> **Locked from:** Round {N-1} Brief v{Major}.{Minor}
> **All OQ-1 / OQ-2 questions:** CLOSED before this Spec started.

---

## Block 1 — Identity

| Field | Value |
|---|---|
| Module ID | {Module} |
| Module Name | {Full Name} |
| Layer | _[L0/L1/L2/L3 + sub-layer]_ |
| Owner | _[role responsible]_ |
| Spec Version | v{Major}.{Minor} |
| X8 Version Referenced | v0.X |
| X9 Version Referenced | v0.X |
| Dependencies | _[other modules this consumes]_ |
| Dependents | _[other modules that consume this]_ |

---

## Block 2 — Scope Boundary

### In Scope

- _[bullet list of what this module owns]_

### Out of Scope (Explicit)

- _[bullet list of what this module does NOT do — paired with the module that does]_

---

## Block 3 — Data Architecture

### Entities

#### Entity_1

| Field | Type | Constraints | Notes |
|---|---|---|---|
| `id` | UUID | PK | |
| `tenant_id` | UUID | FK → Tenant | Reserved field |
| _[other fields]_ | | | |
| `created_by` | UUID | FK → User | Reserved |
| `created_at` | timestamptz | NOT NULL | Reserved |
| `updated_by` | UUID | FK → User | Reserved |
| `updated_at` | timestamptz | NOT NULL | Reserved |
| `is_active` | boolean | DEFAULT TRUE | Reserved |

_[Repeat for each entity. Mark append-only entities clearly — no updated_*, no soft delete.]_

### Relationships

_[Mermaid ER diagram or table.]_

---

## Block 4 — Data Population Rules

### Rule DPR-{module}-001 — _[Rule name]_

**Trigger:** _[when this rule fires]_
**Action:** _[what data is written]_
**Constraints:** _[what must be true]_

_[Repeat for each rule.]_

---

## Block 5 — Filters & Views

### Role-Based Default Views (per X9 v0.X §13)

| Role | Primary View | Secondary Widgets | Hidden |
|---|---|---|---|
| SYSTEM_ADMIN | _[]_ | _[]_ | _[]_ |
| PMO_DIRECTOR | _[]_ | _[]_ | _[]_ |
| _[other roles]_ | | | |

### Filters

_[Filter definitions. Reference X8 ENUMs by name, never redefine.]_

---

## Block 6 — Business Rules

### BR-{module}-001 — _[Rule name]_

**Statement:** _[the rule]_
**Reason:** _[why this rule exists]_
**Implementation hook:** _[where in the entity / API this is enforced]_
**Failure mode:** _[what happens if violated]_

_[Repeat. Number sequentially: BR-{module}-001, BR-{module}-002, ...]_

---

## Block 7 — Integration Points

| Integrates With | Direction | Mechanism | Speed Tier | Notes |
|---|---|---|---|---|
| _[Module]_ | Read / Write | Internal API | T1 / T2 / T3 | _[]_ |

**Single-Owner Rule (F-005):** No direct DB reads from other modules. All access via API.

---

## Block 8 — Governance & Audit

### Audit Events Emitted

| Event Type (UPPER_SNAKE_CASE) | Trigger | Severity | Payload |
|---|---|---|---|
| _[EVENT_NAME]_ | _[when]_ | _[Critical/High/Medium/Low/Info]_ | _[fields]_ |

### Decision Queue Triggers

| Trigger (UPPER_SNAKE_CASE) | Condition | Decision Owner |
|---|---|---|
| _[TRIGGER_NAME]_ | _[condition]_ | _[role]_ |

### Stage Gate Coupling

_[Which SG-N gates this module participates in. What evidence it provides.]_

---

## Block 9 — Explicit Exclusions

_[What this Spec deliberately does NOT cover, with reason and pointer to where it IS covered.]_

| Excluded | Why | Where it lives instead |
|---|---|---|
| _[item]_ | _[reason]_ | _[Module / Round / file]_ |

---

## Block 10 — Open Questions

> **Lock criterion:** This list MUST be empty before Spec is marked LOCKED.

| ID | Question | Status |
|---|---|---|

_[If any rows exist here when ready to lock, the Spec is not ready. Continue iterating.]_

---

## Cascade Implications

_[What other modules / X8 / X9 / wireframes / workflows need updating after this Spec locks. Generate cascade notes for each.]_

---

*Spec locked → Wireframes round next.*
