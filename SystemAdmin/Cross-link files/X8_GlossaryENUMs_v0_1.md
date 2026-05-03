# X8 — Glossary & ENUMs
## Cross-Cutting Document v0.1 (LIVING)
**Owner:** PMO Director / System Architect
**Created:** 2026-05-03
**Status:** Living — appended on every module spec lock
**Source modules locked into this version:** M34
**Folder:** /10_CrossCutting/

---

## 1. PURPOSE

Single canonical reference for:
- Every ENUM type used across EPCC modules
- Every system-wide vocabulary term (status patterns, severity, RAG, speed tiers)
- Every reserved keyword that a module spec must NOT redefine

**Rule:** When writing any module spec, look up here FIRST. If the ENUM exists, reference it. If new, add to this glossary and version-bump.

This prevents Audit Round 00 finding **F-004** from recurring (ENUM drift across modules).

---

## 2. NAMING CONVENTIONS — LOCKED

| Concept | Convention | Example |
|---|---|---|
| ENUM type name | PascalCase | `UserStatus`, `RoleFamily`, `EventCategory` |
| ENUM values | `UPPER_SNAKE_CASE` for system identifiers | `SYSTEM_ADMIN`, `LOGIN_SUCCESS` |
| ENUM values (display-friendly status) | `Pascal_Snake_Case` for human-readable states | `Draft`, `Under_Review`, `Stale_Pending_VO` |
| Severity / RAG | `Pascal` single word | `Critical`, `Green`, `Amber`, `Red` |
| Permission codes | `lower_snake_case` | `view_project`, `approve_variation_order` |
| Role codes | `UPPER_SNAKE_CASE` | `PMO_DIRECTOR` |
| Field names in entities | `lower_snake_case` | `user_id`, `created_at` |
| Database table names | `snake_case` plural | `users`, `system_audit_logs` |
| BR codes | `BR-{module_id}-{seq}` | `BR-34-010`, `BR-01-005` |
| Decision Queue trigger types | `UPPER_SNAKE_CASE` | `USER_LOCKED`, `HANDOVER_DATE_SLIPPAGE` |
| Audit event types | `UPPER_SNAKE_CASE` verb-noun | `LOGIN_SUCCESS`, `ROLE_REVOKED`, `TENANT_CONFIG_CHANGED` |

**Rule of thumb:** UPPER for system-machine identifiers, Pascal_Snake for human-readable states, lower for fields/permissions.

---

## 3. SYSTEM-WIDE ENUMS

These ENUMs are referenced by multiple modules. They MUST be the same everywhere.

### 3.1 `Severity`

Used for: NCR severity, DLP defect severity, punch list severity, audit log severity, decision queue priority, notification severity.

```
ENUM Severity {
  Critical
  High
  Medium
  Low
  Info        ← used for audit/notification only, not for issues
}
```

**Display order:** Critical → High → Medium → Low → Info
**RAG mapping:** Critical=Red · High=Red · Medium=Amber · Low=Green · Info=neutral

**LOCKED — modules must NOT introduce variants:**
- ❌ Do not use `CRITICAL` / `HIGH` (uppercase) — F-013 fix
- ❌ Do not use `Severe` / `Important` / `Minor` — non-canonical
- ❌ Do not introduce a `Trivial` or `Blocker` value — extend this enum at glossary level only

---

### 3.2 `RAGStatus`

Used for: project health, package health, KPI thresholds, gate readiness.

```
ENUM RAGStatus {
  Green
  Amber
  Red
}
```

**Notes:**
- Single word, Pascal case
- No "Yellow" — always "Amber"
- Project health may use bands (Excellent / Good / Watch / At_Risk / Critical) — those are a separate `HealthBand` enum (§3.3)

---

### 3.3 `HealthBand` (M10 EPCC Command)

Used for: project health composite score banding.

```
ENUM HealthBand {
  Excellent    // 85-100
  Good         // 70-84
  Watch        // 55-69
  At_Risk      // 40-54
  Critical     // 0-39
}
```

---

### 3.4 `SpeedTier`

Used for: integration response time classification, BR speed tier assignment, notification dispatch priority.

```
ENUM SpeedTier {
  Realtime         // 🔴 < 2 sec
  NearRealtime     // 🟡 2-4 hr
  Batch            // 🟢 24 hr (daily)
  Link             // — synchronous read on demand
}
```

**Visual indicators (for documentation only — not in DB):** 🔴 / 🟡 / 🟢
**LOCKED:** No free-text "fast" / "immediate" / "slow" — only these four values.

---

### 3.5 `RecordStatus` (generic state pattern)

Used for: most lifecycle entities. **Do not redefine — extend if needed.**

```
ENUM RecordStatus {
  Draft
  Active
  Suspended
  Archived
  Deleted          // soft-delete state
}
```

**Notes:**
- `Locked` is reserved for User-related contexts only (§3.7)
- Module-specific status enums extend this (e.g., `HandoverPlanStatus`, `VariationOrderStatus`)
- **Archived** ≠ **Deleted**: Archived = end of useful life, retained; Deleted = soft-delete flag (`is_active=false`)

---

### 3.6 `LockState` (audit & versioning)

Used for: spec lock states, baseline lock, contract lock, model lock.

```
ENUM LockState {
  Unlocked        // editable
  Pending_Review  // submitted for approval
  Locked          // approved, immutable; major version required to change
  Archived        // superseded by newer version
}
```

---

### 3.7 `UserStatus` (M34 — single source of truth)

```
ENUM UserStatus {
  Active
  Suspended       // admin-paused, can be reactivated
  Locked          // failed-attempt lockout, time-bound
  Archived        // terminated; permanent
}
```

**Locked vs Suspended:**
- `Locked` is automatic, time-bound (30 min default), set by failed login attempts
- `Suspended` is explicit, admin action, requires explicit reinstatement

---

### 3.8 `ProjectStatus` (M01 — single source of truth)

```
ENUM ProjectStatus {
  Draft
  Active
  On_Hold
  Closed          // normal completion
  Cancelled       // abnormal termination
}
```

---

### 3.9 `Phase` (M01 / M08 — project lifecycle phase)

Coarse-grained lifecycle phase. Different from Stage Gates (which are granular).

```
ENUM Phase {
  Pre_Investment       // SG-0 to SG-3
  Design               // SG-4
  Pre_Construction     // SG-5 to SG-6
  Construction         // SG-7
  Equipment            // SG-8
  Commissioning        // SG-9
  Empanelment          // SG-10
  Handover             // SG-11
  DLP                  // post-SG-11
  Closed               // post-DLP
}
```

---

### 3.10 `StageGate` (M08 — locked sequence)

```
ENUM StageGate {
  SG_0    // Idea screening
  SG_1    // Concept feasibility
  SG_2    // DPR / business case
  SG_3    // Capital sanction
  SG_4    // Detailed design
  SG_5    // Statutory clearances
  SG_6    // Procurement & award
  SG_7    // Construction execution
  SG_8    // Equipment installation
  SG_9    // Clinical commissioning
  SG_10   // Empanelment & go-live
  SG_11   // Operations handover
}
```

**LOCKED:** sequence is immutable. No SG-12, no SG-3.5.

---

### 3.11 `GatePassageOutcome`

Used for: M08 gate decisions, M11 decision queue resolutions.

```
ENUM GatePassageOutcome {
  Passed
  Conditional_Pass
  Stopped
  Reopened
  Skipped         // forbidden — see M08; logged but never permitted
}
```

---

### 3.12 `DataSource` (HDI cross-cutting)

Per HDI spec, every entity that can hold historical seed data gets this field.

```
ENUM DataSource {
  Live_EPCC          // captured during normal operation
  Historical_Seed    // imported via HDI one-time
  Mixed_Seed         // for calculated entities (e.g., EVMSnapshot) where some periods are seed
  Manual_Adjustment  // post-hoc PMO Director correction (logged)
}
```

---

### 3.13 `Currency` (Standard_Core CodeMaster — covered here for spec-time reference)

```
ENUM Currency {
  INR    // default
  USD
  EUR
  GBP
  AED
  SGD
  JPY
  CHF
}
```

**Locked:** All financial fields use INR by default. Multi-currency requires PMO_Director enable.

---

### 3.14 `Unit` — see CodeMaster (M34 §3o)

Units (kg, m³, kWh, hr, etc.) are stored as CodeMaster records, not ENUMs. M34 owns the canonical list. Module specs reference CodeMaster.

---

### 3.15 `BillableState`

Used for: M03 BaselineExtension (delays), M05 VariationOrder (changes), M19 Claims.

```
ENUM BillableState {
  Billable                // recoverable from client
  Non_Billable            // contractor-borne
  Disputed                // under negotiation
  Not_Yet_Determined      // pending classification
}
```

---

### 3.16 `Discipline` — see CodeMaster

Civil, Structural, MEP, HVAC, Electrical, Plumbing, Medical_Equipment, IT, Landscape, etc. CodeMaster-driven, not enum.

---

### 3.17 `Sector` — see CodeMaster

Hospital_DBOT, Hospital_PPP, Hospital_EPC, Highway, Metro, Railway, etc. CodeMaster-driven.

---

### 3.18 `DeliveryModel`

```
ENUM DeliveryModel {
  EPC
  EPCM
  DBOT          // Design-Build-Operate-Transfer (KDMC pilot)
  PPP
  Turnkey
  Construction_Management
}
```

---

## 4. M34-OWNED ENUMS (locked v1.0)

### 4.1 `RoleCode` (locked taxonomy)

The canonical 17-role list. Stored as Role table seed.

```
INTERNAL ROLES (assignable to internal Users):
  SYSTEM_ADMIN
  PMO_DIRECTOR
  PORTFOLIO_MANAGER
  PROJECT_DIRECTOR
  PLANNING_ENGINEER
  QS_MANAGER
  FINANCE_LEAD
  PROCUREMENT_OFFICER
  SITE_MANAGER
  COMPLIANCE_MANAGER
  ANALYST
  READ_ONLY
  EXTERNAL_AUDITOR

EXTERNAL ROLES (assigned to ExternalUser):
  CLIENT_VIEWER
  LENDER_VIEWER
  NABH_ASSESSOR
  CONTRACTOR_LIMITED
```

**Retired aliases (do NOT use):**
- ~~`CIO`~~ → use `PMO_DIRECTOR`
- ~~`Supervisor`~~ → use `SITE_MANAGER`
- ~~`Procurement`~~ → use `PROCUREMENT_OFFICER`

### 4.2 `RoleFamily`

```
ENUM RoleFamily {
  Internal
  External
  System         // System_Admin only — not assignable to external parties
}
```

### 4.3 `PermissionAction`

Atomic actions that combine with entities to form permission codes.

```
ENUM PermissionAction {
  view
  create
  edit
  delete
  approve
  export
  configure
  impersonate         // SYSTEM_ADMIN only
}
```

### 4.4 `PermissionScope`

```
ENUM PermissionScope {
  All                 // global
  Own_Tenant          // within user's tenant
  Own_Project         // user has UserRoleAssignment on this project
  Own_Package         // user has package_id in their assignment
  Own_Record          // user is the record's created_by
}
```

### 4.5 `AuthMethod`

```
ENUM AuthMethod {
  Local                  // bcrypt password
  OIDC                   // SSO via OAuth2/OIDC
  Both                   // tenant-level: users choose
  Local_External         // ExternalUser bcrypt
  Email_Magic_Link       // ExternalUser passwordless
}
```

### 4.6 `TenantStatus`

```
ENUM TenantStatus {
  Active
  Suspended    // admin-paused; preserves data, blocks all logins
  Archived     // permanent; tenant terminated
}
```

### 4.7 `TenantType`

```
ENUM TenantType {
  Production
  Pilot
  Sandbox
  Demo
}
```

### 4.8 `SubscriptionTier`

```
ENUM SubscriptionTier {
  Tier_1_Standard
  Tier_2_Premium
}
```

### 4.9 `SessionRevocationReason`

```
ENUM SessionRevocationReason {
  Logout                 // user-initiated
  Admin_Revoke           // admin killed session
  Password_Change        // BR-34-006 cascade
  Role_Change            // BR-34-011 cascade
  Idle_Timeout           // 30 min inactive
  Expired                // 8 hr active
  Concurrent_Limit       // BR-34-034 — oldest revoked
}
```

### 4.10 `LoginAttemptResult`

```
ENUM LoginAttemptResult {
  Success
  Failed_Bad_Password
  Failed_User_Not_Found
  Failed_Locked
  Failed_MFA
  Failed_Suspended
  Failed_Tenant_Suspended
}
```

### 4.11 `AuditEventCategory`

Top-level grouping for SystemAuditLog.

```
ENUM AuditEventCategory {
  Auth                   // login, logout, MFA
  RBAC                   // role assignments
  Tenant_Config          // tenant settings
  Code_Master            // reference data changes
  Feature_Flag           // flag toggles
  API_Key                // API key lifecycle
  User_Lifecycle         // user create/suspend/terminate
}
```

### 4.12 `AuditEventType` (cross-cutting — extended per module)

Each module may register its own event types in this enum (extension at glossary level).

**M34-owned event types:**
```
LOGIN_SUCCESS
LOGIN_FAILED
USER_LOCKED
USER_CREATED
USER_TERMINATED
USER_SUSPENDED
USER_AUTOSUSPENDED
PASSWORD_CHANGED
PASSWORD_EXPIRY_FORCED
PASSWORD_RESET_REQUESTED
PASSWORD_RESET_RATE_LIMITED
MFA_ENROLLED
MFA_DISABLED
MFA_BACKUP_CODE_USED
ROLE_ASSIGNED
ROLE_REVOKED
ROLE_EXPIRED
TENANT_CONFIG_CHANGED
TENANT_SUSPENDED
FEATURE_FLAG_CHANGED
CODE_MASTER_CHANGED
API_KEY_CREATED
API_KEY_REVOKED
EXTERNAL_USER_CREATED
EXTERNAL_USER_EXPIRED
SSO_AUTO_PROVISIONED
```

**Reserved namespaces for future modules:**
- `M01_*` for M01 Project Registry events (project create, contract sign, etc.)
- `M02_*` for M02 BOQ/WBS events
- ... etc.

---

## 5. CODEMASTER CATEGORIES (M34-OWNED)

These live as `CodeMaster` records, NOT as ENUMs. Modules query them at runtime.

| Category | Tier | Owned By | Notes |
|---|---|---|---|
| Unit | Standard_Core | SYSTEM_ADMIN | kg, m, m², m³, hr, etc. |
| DocumentType | Domain_Specific | PMO_DIRECTOR | RFI, Submittal, Drawing, Transmittal, MOM |
| Sector | Domain_Specific | PMO_DIRECTOR | Hospital, Highway, Metro, etc. + sub-types |
| Discipline | Custom | PROJECT_DIRECTOR (own project) | CIV, STR, MEP, HVAC, ELE, etc. |
| Currency | Standard_Core | SYSTEM_ADMIN | INR, USD, etc. (mirrors §3.13) |

---

## 6. RESERVED FIELDS (every entity gets these)

Per Standards Memory + I2 (audit stamp). Modules MUST NOT redefine these:

| Field | Type | Required | Purpose |
|---|---|---|---|
| `tenant_id` | UUID | Y | Multi-tenant isolation |
| `created_by` | UUID | Y | Who created the record |
| `created_at` | TIMESTAMP | Y | When created |
| `updated_by` | UUID | Y | Last modifier |
| `updated_at` | TIMESTAMP | Y | Last modification time |
| `is_active` | BOOLEAN | Y | Soft-delete flag (default true) |

**Some entities exempt:**
- Append-only logs (`SystemAuditLog`, `LoginAttempt`, `BACIntegrityLedger`) → no `is_active`, no `updated_*`
- Junction tables (`RolePermission`, `BOQWBSMap`) → may omit `created_by`/`updated_by`

---

## 7. NAMING DICTIONARY (vocabulary)

When the same concept appears in 2+ modules, use the canonical term:

| Canonical Term | Used For | Avoid |
|---|---|---|
| `Project` | A construction project | "Job", "Site", "Engagement" |
| `Package` | Contractual work package within a project | "Lot", "Section" |
| `BOQ Item` | Line item in Bill of Quantities | "Item", "Line" |
| `WBS Node` | Hierarchical breakdown node | "Activity", "Task" (those mean schedule entries) |
| `Activity` | Schedule entry in M03 | "Task" |
| `Milestone` | Key date in schedule | — |
| `Variation Order` | Approved scope change | "Change Order", "VO" — VO is OK as abbreviation |
| `EOT` | Extension of Time | "Time Extension" |
| `LD` | Liquidated Damages | "Penalty" — not interchangeable |
| `RA Bill` | Running Account Bill | "Invoice" — RA Bill is the formal term |
| `BAC` | Budget at Completion | — |
| `EAC` | Estimate at Completion | — |
| `EVM` | Earned Value Management | "Earned Value" alone is OK in narrative |
| `Stage Gate` (or `Gate`) | M08 governance gate | — |
| `Decision Queue` | Cross-module pending decision register | "Action Queue", "Workflow Queue" |
| `Action Item` | M11 follow-up | "Task" — ambiguous with schedule task |
| `NCR` | Non-Conformance Report | — |
| `DLP` | Defects Liability Period | "Maintenance Period" — not the same |
| `Punch List` | Pre-handover defects | "Snag List" — synonyms in industry but use Punch List in spec |
| `Handover Certificate` | Practical completion document | "Taking Over Certificate" — synonyms; Handover Certificate is canonical |
| `Compliance Item` | Regulatory tracking unit | — |
| `Standard` | NABH/IS/AERB standard within compliance | "Code", "Spec" — ambiguous |
| `Party` | External organisation (client, contractor, etc.) | "Vendor", "Stakeholder" — broader concepts |
| `User` | Authenticated person in system | — |
| `Role` | RBAC role | — |
| `Permission` | RBAC atomic permission | "Right", "Capability" |
| `Tenant` | Isolation unit (one organisation) | "Company", "Org" |

---

## 8. EXTENSION PROTOCOL

When writing a new module spec and you encounter:

| Scenario | Action |
|---|---|
| ENUM already exists in §3 or §4 | **Reference it.** Do not redefine. |
| ENUM exists but you need a new value | **Append to existing ENUM here.** Bump glossary version. Modify spec to reference. |
| Entirely new ENUM concept | **Add new section here.** Confirm with PMO Director. Bump glossary version. |
| Naming conflict (you want `Status` but `RecordStatus` exists) | **Reference existing or use module-prefixed name.** e.g., `HandoverPlanStatus`. |
| Reserved field (e.g. `created_at`) | **Inherit from §6.** Do not redefine. |

---

## 9. CHANGE LOG

| Version | Date | Change |
|---|---|---|
| v0.1 | 2026-05-03 | Initial draft. M34 ENUMs locked. System-wide ENUMs (Severity, RAG, SpeedTier, RecordStatus, LockState, StageGate, DataSource, etc.) locked. Naming dictionary established. |

**Future bumps:**
- v0.2 — after M01 spec lock
- v0.3 — after M02/M03 spec lock
- ... etc.
- v1.0 — after all Phase 1 specs locked

---

## 10. ENFORCEMENT

| Layer | Mechanism |
|---|---|
| Brief writing | First step: query this glossary for any ENUM the brief mentions |
| Spec writing | Block 3 (Data Architecture) ENUM fields reference glossary section number |
| Spec audit (per round) | Verify no ENUM redefined; any new ENUM is added here |
| Code review (future) | Lint rule: ENUM definitions in code import from `enums/` package; package must match glossary |

---

*v0.1 — Living document. Updated on every module spec lock. Source of truth for all cross-module vocabulary.*
