# M34 — System Administration & RBAC
## Spec v1.0
**Status:** Locked
**Locked:** Yes
**Author:** PMO Director / System Architect
**Created:** 2026-05-03 | **Last Updated:** 2026-05-03
**Last Audited:** v1.0 on 2026-05-03
**Reference Standards:** EPCC_StandardsMemory_v1_0.md (pending), EPCC_NamingConvention_v1_0.md
**Layer:** L1 Command
**Phase:** 1 — Foundational
**Build Priority:** 🔴 Critical (must precede every other module spec lock)
**Folder:** /02_L1_Command/

---

## CHANGE LOG

| Version | Date | Change Summary |
|---|---|---|
| v1.0 | 2026-05-03 | Initial spec. Locks canonical role taxonomy (13 internal + 4 external). Resolves all OQ-1.1 through OQ-1.10. Establishes hybrid AuditLog. Locks code-controlled role definition. |

---

## BLOCK 1 — IDENTITY

```
Module ID                : M34
Module Name              : System Administration & RBAC
Layer                    : L1 Command
Decision It Enables      : Is every user authenticated, scoped to the right tenant
                           and project, granted exactly the actions their role
                           permits — and is every privileged action permanently
                           logged with an immutable audit trail?

Primary User             : System_Admin
Secondary Users          : PMO_Director (role assignments + audit review),
                           All authenticated users (own profile + own audit)
Module Icon              : ShieldCheck (Lucide)
Navigation Section       : L1 Command (between M01 Project Registry and M23 BG Tracker)
```

---

## BLOCK 2 — SCOPE BOUNDARY

### INCLUDES

| Capability | Description |
|---|---|
| Tenant management | Multi-tenant isolation; one organisation = one tenant; schema-per-tenant per ES-DB-001 |
| User management | Internal user CRUD: identity, contact, employment, lifecycle |
| Role taxonomy | Code-controlled enum of 13 internal roles + 4 external (locked at release time) |
| Permission catalog | Action × Entity matrix; system-defined, code-controlled |
| Role-permission mapping | Static at release time; lives in code + seeded to DB on migration |
| User-Project-Role assignment | Per-project role assignment with scope (own/all) |
| Authentication | Local password (bcrypt) + OIDC SSO (configurable per tenant) |
| Multi-factor authentication | TOTP-based; mandatory for System_Admin and PMO_Director |
| Session management | Access token + refresh token; configurable timeouts |
| Password policy enforcement | Min 12 chars, mixed case + digit + symbol; 90-day rotation; last-3 history |
| Password reset workflow | Email link, 1-hour expiry, single-use, rate-limited |
| API key management | Service-to-service auth (Phase 2 ready) |
| System audit log (cross-cutting events) | Auth events, role changes, tenant config changes, code master changes |
| Feature flag registry | Per-tenant + per-project module/feature toggles |
| Code master registry | System-wide reference codes (units, document types, sectors) |
| User notification preferences | Channel (in-app/email/WhatsApp) per severity |
| User → Party affiliation | Optional FK to M01.Party (per OQ-1.10) |
| External user management | Separate `ExternalUser` entity for PF03 portal users |

### EXCLUDES

| Excluded | Where It Lives |
|---|---|
| Module-specific business rules | Each module M01–M33 owns its own |
| Project membership lists per module | Each module's role tables |
| Module-specific audit log content | Each module's Block 8 (M34 owns shell + cross-cutting events only) |
| Per-module feature configuration | Module-specific `*_Config` entities (e.g., `ActionRegisterConfig` in M11) |
| Notification dispatching/routing | M11 + M10 notification engine; M34 only stores user preferences |
| Mobile device binding | PF01 — extends M34 auth with device_id |
| Client/lender/contractor portal auth | PF03 — uses ExternalUser table M34 owns, but auth flow is PF03's |
| Party master | M01 — M34 references via optional FK |
| Project master | M01 — M34 references for role assignment scope |
| Decision Queue items | M11 Action Register + per-module decision generation |
| Permission of business actions on entities (e.g., approve_VO) | Defined per spec; enforced by M34 at API gate |

---

## BLOCK 3 — DATA ARCHITECTURE

### 3a. Entity Overview

| Entity | Description | Cardinality | Owner |
|---|---|---|---|
| `Tenant` | Top-level isolation unit (one organisation) | Many in system | M34 |
| `User` | Internal authenticated user with credentials | Many per tenant | M34 |
| `Role` | Canonical role definition (code-controlled enum) | 13 internal + 4 external | M34 (code + seed) |
| `Permission` | Atomic permission unit (action + entity) | ~200–400 (estimated) | M34 (code + seed) |
| `RolePermission` | Role × Permission mapping; defines what each role can do | Many | M34 (code + seed) |
| `UserRoleAssignment` | User × Project × Role assignment with scope | Many per user | M34 |
| `ExternalUser` | External party user (client, lender, contractor, assessor) | Many per tenant | M34 |
| `AuthSession` | Active authenticated session with token | One active per user-device | M34 |
| `AuthToken` | Refresh tokens for session continuation | Many per user | M34 |
| `MFAConfig` | TOTP secret per user | One per user (when enabled) | M34 |
| `PasswordResetRequest` | Self-service password reset workflow | Many per user (audit) | M34 |
| `LoginAttempt` | Login attempt audit (success + failure) | Many per user (rolling) | M34 |
| `SystemAuditLog` | Cross-cutting events: auth, role changes, tenant config | Many | M34 |
| `FeatureFlag` | Per-tenant + per-project feature toggles | Many | M34 |
| `CodeMaster` | System-wide reference codes (units, doc types, sectors) | Many | M34 |
| `APIKey` | Service-to-service authentication tokens | Few per tenant | M34 |
| `UserNotificationPreference` | Per-user channel preferences per severity | One per user | M34 |

### 3b. Entity: `Tenant`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `tenant_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_code` | VARCHAR(10) | Y | Unique. Uppercase, 3–10 chars. e.g., `KDMC`, `EPCC01`. | INPUT |
| `tenant_name` | VARCHAR(200) | Y | Organisation legal name | INPUT |
| `db_schema_name` | VARCHAR(50) | Y | Auto = `t_{tenant_code_lower}`. Maps to PostgreSQL schema. | SYSTEM |
| `tenant_type` | ENUM | Y | `Production / Pilot / Sandbox / Demo` | INPUT |
| `subscription_tier` | ENUM | Y | `Tier_1_Standard / Tier_2_Premium` per Deployment Tier Spec | INPUT |
| `status` | ENUM | Y | `Active / Suspended / Archived` | SYSTEM |
| `auth_method_default` | ENUM | Y | `Local / OIDC / Both`. Default: `Local`. | INPUT |
| `oidc_issuer_url` | VARCHAR(500) | N | Required if auth_method = OIDC or Both | INPUT |
| `oidc_client_id` | VARCHAR(200) | N | Required if auth_method = OIDC or Both | INPUT |
| `oidc_client_secret_ref` | VARCHAR(200) | N | Vault reference (never stored in DB) | INPUT |
| `dpdp_data_fiduciary_name` | VARCHAR(200) | Y | Per DPDP Act 2023 ES-SEC-004 | INPUT |
| `dpdp_grievance_officer_email` | VARCHAR(150) | Y | Per DPDP Act | INPUT |
| `created_by` | UUID | Y | System_Admin user ID | LINK → User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_by` | UUID | Y | Auto | LINK → User |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true. Soft delete. | SYSTEM |

### 3c. Entity: `User`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `user_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | FK → Tenant | LINK → Tenant |
| `username` | VARCHAR(50) | Y | Unique within tenant. Lowercase, alphanumeric + underscore + dot. 3–50 chars. | INPUT |
| `email` | VARCHAR(150) | Y | Unique within tenant. Valid email format. | INPUT |
| `full_name` | VARCHAR(200) | Y | Min 3 chars | INPUT |
| `display_name` | VARCHAR(100) | N | Defaults to first 100 chars of full_name | INPUT |
| `phone` | VARCHAR(15) | N | Indian format `+91[0-9]{10}` | INPUT |
| `employee_code` | VARCHAR(30) | N | Per-organisation employee ID | INPUT |
| `designation` | VARCHAR(150) | N | Job title | INPUT |
| `department` | VARCHAR(100) | N | Department name | INPUT |
| `auth_method` | ENUM | Y | `Local / OIDC` | SYSTEM (from tenant default + override) |
| `password_hash` | VARCHAR(255) | N | bcrypt hash. Required if auth_method = Local. Never returned in API responses. | SYSTEM |
| `password_set_at` | TIMESTAMP | N | Set on password change | SYSTEM |
| `password_must_change` | BOOLEAN | Y | Default true on first creation; true on admin reset | SYSTEM |
| `password_history_hashes` | JSONB | N | Last 3 password hashes for OQ-2.4 last-3 check | SYSTEM |
| `mfa_enabled` | BOOLEAN | Y | Default false. Mandatory true for System_Admin, PMO_Director. | SYSTEM |
| `failed_login_count` | INTEGER | Y | Default 0. Increments on failed login. Resets on successful login. Lock at 5. | SYSTEM |
| `locked_until` | TIMESTAMP | N | Set when failed_login_count reaches 5. Auto-unlock after 30 min. | SYSTEM |
| `last_login_at` | TIMESTAMP | N | Updated on successful login | SYSTEM |
| `party_id` | UUID | N | Optional FK → M01.Party. Per OQ-1.10. | LINK → M01.Party |
| `party_role_label` | VARCHAR(100) | N | Free-text role at the Party (e.g., "Senior Site Engineer") | INPUT |
| `status` | ENUM | Y | `Active / Suspended / Locked / Archived`. Default `Active` | SYSTEM |
| `joined_at` | DATE | Y | Date user joined the organisation/project | INPUT |
| `terminated_at` | DATE | N | Set when user offboarded. Triggers role revocation cascade. | INPUT |
| `created_by` | UUID | Y | FK → User (creator) | LINK → User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_by` | UUID | Y | Auto | LINK → User |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true. Soft delete. | SYSTEM |

### 3d. Entity: `Role`

Role taxonomy is **code-controlled** (per OQ-1.7). Stored in DB as seed data, locked by Alembic migration.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `role_id` | UUID | Y | Auto-generated; seeded | SYSTEM |
| `role_code` | VARCHAR(40) | Y | Locked enum. Snake_case_uppercase. | CODE |
| `role_name` | VARCHAR(100) | Y | Display name | CODE |
| `role_family` | ENUM | Y | `Internal / External / System` | CODE |
| `description` | TEXT | Y | What this role does | CODE |
| `is_assignable` | BOOLEAN | Y | Can a user be assigned this role? `System` role is not assignable. | CODE |
| `requires_mfa` | BOOLEAN | Y | Per OQ-2.6 | CODE |
| `default_session_minutes` | INTEGER | Y | Default 480 (8 hours) per OQ-2.5 | CODE |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |

**Locked Role Taxonomy v1.0** (changes require new release):

| role_code | role_family | requires_mfa | Description |
|---|---|---|---|
| `SYSTEM_ADMIN` | System | Yes | Tenant config, code masters, emergency access |
| `PMO_DIRECTOR` | Internal | Yes | Top application authority — portfolio + governance |
| `PORTFOLIO_MANAGER` | Internal | Yes | Cross-program oversight |
| `PROJECT_DIRECTOR` | Internal | No | Per-project execution authority |
| `PLANNING_ENGINEER` | Internal | No | Schedule + planning ownership |
| `QS_MANAGER` | Internal | No | Quantity surveying + measurement |
| `FINANCE_LEAD` | Internal | Yes | Financial control |
| `PROCUREMENT_OFFICER` | Internal | No | Tendering + vendor + PO |
| `SITE_MANAGER` | Internal | No | Field operations (formerly "Supervisor" — alias retired) |
| `COMPLIANCE_MANAGER` | Internal | No | NABH + statutory ownership |
| `ANALYST` | Internal | No | Read-heavy support (PIOE etc.) |
| `READ_ONLY` | Internal | No | Audit/observer role |
| `EXTERNAL_AUDITOR` | Internal | No | NABH/lender external auditors with internal credentials |
| `CLIENT_VIEWER` | External | No | Phase 2 — PF03 |
| `LENDER_VIEWER` | External | No | Phase 2 — PF03 |
| `NABH_ASSESSOR` | External | No | Phase 2 — PF03 |
| `CONTRACTOR_LIMITED` | External | No | Phase 2 — PF03 |

**Note:** Per OQ-1.4 — `CIO` role eliminated. PIOE spec re-issue (Round 5+) replaces `CIO` references with `PMO_DIRECTOR`.

### 3e. Entity: `Permission`

Atomic permission unit. Code-controlled. Format: `{action}_{entity}` or `{action}_{entity}_{scope_qualifier}`.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `permission_id` | UUID | Y | Auto-generated; seeded | SYSTEM |
| `permission_code` | VARCHAR(80) | Y | Snake_case_lowercase. e.g., `create_project`, `edit_ncr`, `approve_vo` | CODE |
| `module_id` | VARCHAR(10) | Y | Owning module: `M01`, `M04`, `PIOE`, `M34`, etc. | CODE |
| `entity_name` | VARCHAR(80) | Y | Target entity. e.g., `Project`, `NCR`, `VariationOrder` | CODE |
| `action` | ENUM | Y | `view / create / edit / delete / approve / export / configure / impersonate` | CODE |
| `description` | TEXT | Y | Human-readable description | CODE |
| `is_field_level` | BOOLEAN | Y | True if permission controls a specific field (per OQ-1.3 D selective B) | CODE |
| `field_name` | VARCHAR(80) | N | Required if is_field_level | CODE |
| `is_active` | BOOLEAN | Y | Default true. Set false to retire a permission. | CODE |
| `created_at` | TIMESTAMP | Y | Auto on seed | SYSTEM |

**Permission count estimate:** 200–400 permissions across all modules. Each module spec defines its own permissions during spec writing.

### 3f. Entity: `RolePermission`

Maps roles to permissions. **Flat per OQ-1.1 — no inheritance.** Code-controlled.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `role_permission_id` | UUID | Y | Auto-generated; seeded | SYSTEM |
| `role_id` | UUID | Y | FK → Role | LINK → Role |
| `permission_id` | UUID | Y | FK → Permission | LINK → Permission |
| `default_scope` | ENUM | Y | `All / Own_Project / Own_Package / Own_Record / Own_Tenant`. Per OQ-1.3 D. | CODE |
| `created_at` | TIMESTAMP | Y | Auto on seed | SYSTEM |

**`default_scope` semantics:**
- `All` — applies to all records (e.g., PMO_Director.view_project)
- `Own_Project` — only records where user has UserRoleAssignment on that project
- `Own_Package` — only records belonging to package the user is assigned to
- `Own_Record` — only records where user is creator/owner
- `Own_Tenant` — within user's tenant only (default for all internal roles)

### 3g. Entity: `UserRoleAssignment`

Per OQ-1.2 — user has different roles on different projects.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `assignment_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | FK → Tenant | LINK → Tenant |
| `user_id` | UUID | Y | FK → User | LINK → User |
| `role_id` | UUID | Y | FK → Role. Must be `is_assignable = true` | LINK → Role |
| `project_id` | UUID | N | FK → M01.Project. NULL means tenant-wide assignment (e.g., PMO_Director). | LINK → M01.Project |
| `scope_override` | ENUM | N | Optional override of role's default_scope for this assignment | INPUT |
| `package_ids` | JSONB | N | Array of package_ids if role is package-scoped (Site_Manager) | INPUT |
| `assignment_status` | ENUM | Y | `Active / Suspended / Revoked / Expired` | SYSTEM |
| `valid_from` | DATE | Y | Default = today | INPUT |
| `valid_until` | DATE | N | NULL = indefinite. Set to terminate role at a specific date. | INPUT |
| `assigned_by` | UUID | Y | FK → User who made assignment | LINK → User |
| `assigned_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `revocation_reason` | TEXT | N | Required if assignment_status = Revoked. Min 30 chars. | INPUT |
| `revoked_by` | UUID | N | FK → User | LINK → User |
| `revoked_at` | TIMESTAMP | N | Auto on revocation | SYSTEM |
| `created_by` | UUID | Y | Auto | LINK → User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_by` | UUID | Y | Auto | LINK → User |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true. Soft delete. | SYSTEM |

**Composite uniqueness:** (`tenant_id`, `user_id`, `role_id`, `project_id`) — user cannot have the same role on the same project twice.

### 3h. Entity: `ExternalUser`

Per OQ-1.5 — separate table for external party users. Phase 2 active; Phase 1 schema-ready.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `external_user_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | FK → Tenant | LINK → Tenant |
| `external_user_code` | VARCHAR(50) | Y | Unique within tenant. Format: `EXT-{tenant_code}-{seq}` | SYSTEM |
| `email` | VARCHAR(150) | Y | Unique within tenant | INPUT |
| `full_name` | VARCHAR(200) | Y | — | INPUT |
| `phone` | VARCHAR(15) | N | Indian format | INPUT |
| `external_role` | ENUM | Y | `CLIENT_VIEWER / LENDER_VIEWER / NABH_ASSESSOR / CONTRACTOR_LIMITED` | INPUT |
| `affiliated_party_id` | UUID | N | FK → M01.Party (their employer/organisation) | LINK → M01.Party |
| `auth_method` | ENUM | Y | `Local_External / Email_Magic_Link`. SSO not supported for externals. | SYSTEM |
| `password_hash` | VARCHAR(255) | N | If auth_method = Local_External | SYSTEM |
| `mfa_enabled` | BOOLEAN | Y | Default false. Optional. | INPUT |
| `project_access_ids` | JSONB | Y | Array of project_ids the external user can see. Strict whitelist. | INPUT |
| `valid_from` | DATE | Y | Project access starts | INPUT |
| `valid_until` | DATE | Y | Mandatory end date. Default: today + 365 days. Renewable. | INPUT |
| `status` | ENUM | Y | `Active / Suspended / Expired / Revoked` | SYSTEM |
| `nda_signed` | BOOLEAN | Y | Default false. Required true for status = Active. | INPUT |
| `nda_signed_at` | TIMESTAMP | N | Auto on signing | SYSTEM |
| `created_by` | UUID | Y | FK → User (PMO_Director or PROJECT_DIRECTOR who provisioned) | LINK → User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |

### 3i. Entity: `AuthSession`

Active authenticated session.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `session_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `user_id` | UUID | N | FK → User. Mutex with external_user_id. | LINK → User |
| `external_user_id` | UUID | N | FK → ExternalUser. Mutex with user_id. | LINK → ExternalUser |
| `access_token_hash` | VARCHAR(255) | Y | Hashed, not plaintext | SYSTEM |
| `refresh_token_hash` | VARCHAR(255) | Y | Hashed | SYSTEM |
| `device_info` | JSONB | Y | `{user_agent, ip, device_type}` | SYSTEM |
| `mfa_verified` | BOOLEAN | Y | Default false; true after TOTP success in this session | SYSTEM |
| `started_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `last_activity_at` | TIMESTAMP | Y | Updated on each authenticated request | SYSTEM |
| `expires_at` | TIMESTAMP | Y | Default = started_at + 480min (per role default_session_minutes) | SYSTEM |
| `revoked_at` | TIMESTAMP | N | Set on logout or admin revoke | SYSTEM |
| `revocation_reason` | ENUM | N | `Logout / Admin_Revoke / Password_Change / Role_Change / Idle_Timeout / Expired` | SYSTEM |

**Note:** Constraint enforces exactly one of `user_id` or `external_user_id` is non-null.

### 3j. Entity: `MFAConfig`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `mfa_id` | UUID | Y | Auto-generated | SYSTEM |
| `user_id` | UUID | Y | FK → User. Unique. | LINK → User |
| `totp_secret_encrypted` | VARCHAR(500) | Y | AES-encrypted. Decryption key in Vault. | SYSTEM |
| `backup_codes_hash` | JSONB | Y | Array of 10 hashed single-use backup codes | SYSTEM |
| `enrolled_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `last_verified_at` | TIMESTAMP | N | Auto on each successful TOTP verification | SYSTEM |

### 3k. Entity: `PasswordResetRequest`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `request_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `user_id` | UUID | Y | FK → User | LINK → User |
| `request_type` | ENUM | Y | `Self_Service / Admin_Forced` | INPUT |
| `requested_by` | UUID | Y | FK → User. Self if self-service. | LINK → User |
| `token_hash` | VARCHAR(255) | Y | Hashed reset token (sent in email link) | SYSTEM |
| `requested_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `expires_at` | TIMESTAMP | Y | Auto = requested_at + 60min per OQ-2.10 | SYSTEM |
| `consumed_at` | TIMESTAMP | N | Set when token used | SYSTEM |
| `status` | ENUM | Y | `Pending / Consumed / Expired / Cancelled` | SYSTEM |
| `request_ip` | VARCHAR(45) | Y | Source IP | SYSTEM |

### 3l. Entity: `LoginAttempt`

Rolling audit of login attempts. Retention: 90 days.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `attempt_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `username_attempted` | VARCHAR(150) | Y | Username or email entered | SYSTEM |
| `user_id` | UUID | N | FK → User if username resolves | LINK → User |
| `attempt_type` | ENUM | Y | `Internal / External` | SYSTEM |
| `result` | ENUM | Y | `Success / Failed_Bad_Password / Failed_User_Not_Found / Failed_Locked / Failed_MFA / Failed_Suspended` | SYSTEM |
| `ip_address` | VARCHAR(45) | Y | Source IP | SYSTEM |
| `user_agent` | TEXT | Y | Browser UA | SYSTEM |
| `attempted_at` | TIMESTAMP | Y | Auto | SYSTEM |

### 3m. Entity: `SystemAuditLog`

Per OQ-1.8 — Hybrid model. M34 owns CROSS-CUTTING events. Modules own module-specific events.

**Events logged here:**
- Login/logout (success + failure)
- Role assignment / revocation
- Permission grant / revoke
- Tenant config changes
- Code master changes
- Feature flag changes
- API key creation/revocation
- MFA enrollment/disable
- Password reset (self + admin-forced)
- User creation/suspension/archival

**Retention:** Permanent for privileged actions; 7 years for routine. Per OQ-2.7.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `audit_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `event_category` | ENUM | Y | `Auth / RBAC / Tenant_Config / Code_Master / Feature_Flag / API_Key / User_Lifecycle` | SYSTEM |
| `event_type` | VARCHAR(80) | Y | UPPERCASE_SNAKE_CASE per F-013 fix. e.g., `LOGIN_SUCCESS`, `ROLE_ASSIGNED` | SYSTEM |
| `actor_user_id` | UUID | N | Who performed the action. Null for system events. | LINK → User |
| `target_user_id` | UUID | N | Who was acted upon (if applicable) | LINK → User |
| `target_entity_type` | VARCHAR(80) | N | Entity type if action targeted an entity | SYSTEM |
| `target_entity_id` | UUID | N | Entity record ID if applicable | SYSTEM |
| `from_value` | JSONB | N | State before change | SYSTEM |
| `to_value` | JSONB | N | State after change | SYSTEM |
| `reason` | TEXT | N | Reason or comment if user provided | INPUT |
| `ip_address` | VARCHAR(45) | N | Source IP if web action | SYSTEM |
| `user_agent` | TEXT | N | Browser UA if web action | SYSTEM |
| `severity` | ENUM | Y | `Info / Warning / Critical` | SYSTEM |
| `is_privileged_action` | BOOLEAN | Y | Determines retention. True = permanent; False = 7y. | CALC |
| `event_at` | TIMESTAMP | Y | Auto | SYSTEM |

**Immutability:** Append-only. No updates. No soft delete. Retention enforced by archive process, not deletion.

### 3n. Entity: `FeatureFlag`

Per OQ-1.9 — per-tenant + per-project granularity.

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `flag_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | FK → Tenant | LINK → Tenant |
| `project_id` | UUID | N | FK → M01.Project. NULL = tenant-wide | LINK → M01.Project |
| `flag_code` | VARCHAR(80) | Y | Code-defined flag identifier. e.g., `M26_AI_INTELLIGENCE_ENABLED` | CODE |
| `is_enabled` | BOOLEAN | Y | True/false toggle | INPUT |
| `enabled_reason` | TEXT | N | Why this flag was enabled (audit context) | INPUT |
| `created_by` | UUID | Y | FK → User (System_Admin only) | LINK → User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_by` | UUID | Y | Auto | LINK → User |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |

**Composite uniqueness:** (`tenant_id`, `project_id`, `flag_code`).

### 3o. Entity: `CodeMaster`

System-wide reference codes. e.g., units (kg, m³), document types (RFI, Submittal, Drawing), sectors (Hospital, Highway).

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `code_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | N | NULL = system-wide. Set for tenant-specific overrides. | LINK → Tenant |
| `code_category` | VARCHAR(50) | Y | e.g., `Unit`, `DocumentType`, `Sector`, `Discipline`, `Currency` | INPUT |
| `code_value` | VARCHAR(50) | Y | The code itself. e.g., `kg`, `RFI`, `Hospital_DBOT` | INPUT |
| `display_label` | VARCHAR(150) | Y | Human-readable label | INPUT |
| `description` | TEXT | N | Long description | INPUT |
| `tier` | ENUM | Y | `Standard_Core / Domain_Specific / Custom` per existing M02 3-tier pattern | INPUT |
| `parent_code_id` | UUID | N | FK to parent CodeMaster for hierarchical codes | LINK → CodeMaster |
| `sort_order` | INTEGER | Y | Default 100. Lower = first in dropdown. | INPUT |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |
| `created_by` | UUID | Y | Standard_Core: SEED; others: User | LINK → User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

**Composite uniqueness:** (`tenant_id`, `code_category`, `code_value`) — but tenant_id NULL is treated as a single global value.

### 3p. Entity: `APIKey`

Phase 2 ready. Service-to-service authentication for future integrations (Tally export, BIM, etc.).

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `api_key_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | FK → Tenant | LINK → Tenant |
| `key_name` | VARCHAR(100) | Y | Human-readable identifier. e.g., `Tally_Export_KDMC_Prod` | INPUT |
| `key_hash` | VARCHAR(255) | Y | Hashed key (raw key shown ONCE on creation) | SYSTEM |
| `key_prefix` | VARCHAR(8) | Y | First 8 chars of raw key (for identification in logs) | SYSTEM |
| `permissions_scoped` | JSONB | Y | Array of permission_codes this key can use | INPUT |
| `created_by` | UUID | Y | FK → User (System_Admin only) | LINK → User |
| `created_at` | TIMESTAMP | Y | Auto | SYSTEM |
| `last_used_at` | TIMESTAMP | N | Updated on each authenticated call | SYSTEM |
| `expires_at` | TIMESTAMP | Y | Mandatory. Default created_at + 365d. | INPUT |
| `revoked_at` | TIMESTAMP | N | Set on revocation | SYSTEM |
| `is_active` | BOOLEAN | Y | Default true | SYSTEM |

### 3q. Entity: `UserNotificationPreference`

| Field | Type | Required | Validation Rule | Source |
|---|---|---|---|---|
| `pref_id` | UUID | Y | Auto-generated | SYSTEM |
| `user_id` | UUID | Y | FK → User. Unique. | LINK → User |
| `severity` | ENUM | Y | `Critical / High / Medium / Low / Info` | SYSTEM |
| `channel_in_app` | BOOLEAN | Y | Default true (always on for Critical) | INPUT |
| `channel_email` | BOOLEAN | Y | Default true | INPUT |
| `channel_whatsapp` | BOOLEAN | Y | Default false (opt-in) | INPUT |
| `whatsapp_number` | VARCHAR(15) | N | Required if channel_whatsapp = true | INPUT |
| `quiet_hours_start` | TIME | N | e.g., 22:00 IST | INPUT |
| `quiet_hours_end` | TIME | N | e.g., 07:00 IST | INPUT |
| `quiet_hours_respect_critical` | BOOLEAN | Y | Default false — Critical bypasses quiet hours | INPUT |
| `updated_by` | UUID | Y | Self-service | LINK → User |
| `updated_at` | TIMESTAMP | Y | Auto | SYSTEM |

**Note:** One row per user per severity (5 rows per user).

---

## BLOCK 4 — DATA POPULATION RULES

### 4a. Role × Action Permission Matrix (M34's own actions)

| Action | SYSTEM_ADMIN | PMO_DIRECTOR | PORTFOLIO_MGR | PROJECT_DIR | OTHERS | READ_ONLY |
|---|---|---|---|---|---|---|
| Create Tenant | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Edit Tenant config | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Create User | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Edit User identity | ✅ | ✅ | ❌ | Self only | Self only | Self only |
| Suspend User | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Archive User | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Assign Role to User | ✅ | ✅ | ✅ (own program) | ✅ (own project, restricted) | ❌ | ❌ |
| Revoke Role | ✅ | ✅ | ✅ (own program) | ✅ (own project, restricted) | ❌ | ❌ |
| Reset another user's password | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Reset own password | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Enroll MFA | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Disable own MFA (where not mandatory) | ✅ | ❌ (mandatory) | ✅ | ✅ | ✅ | ✅ |
| View System Audit Log | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| View own audit trail | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Create ExternalUser | ✅ | ✅ | ❌ | ✅ (own project) | ❌ | ❌ |
| Edit Feature Flag | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Edit Code Master (Standard_Core) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Edit Code Master (Domain_Specific) | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Edit Code Master (Custom) | ✅ | ✅ | ✅ | ✅ (own project) | ❌ | ❌ |
| Create API Key | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Revoke API Key | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

**`PROJECT_DIR (own project, restricted)` for role assignment:** can only assign roles below own level (PLANNING_ENGINEER, QS_MANAGER, PROCUREMENT_OFFICER, SITE_MANAGER, COMPLIANCE_MANAGER, ANALYST, READ_ONLY). Cannot assign PROJECT_DIRECTOR, PORTFOLIO_MANAGER, PMO_DIRECTOR, or SYSTEM_ADMIN.

### 4b. Mandatory Fields at Creation

**User creation:**
```
username, email, full_name, auth_method, joined_at, party_id (optional), role assignment (at least one)
```

**ExternalUser creation:**
```
email, full_name, external_role, project_access_ids (≥ 1), valid_until, nda_signed = true
```

**Tenant creation (System_Admin only):**
```
tenant_code, tenant_name, tenant_type, subscription_tier, dpdp_data_fiduciary_name, dpdp_grievance_officer_email
```

### 4c. Entry Methods

| Field group | Entry method |
|---|---|
| User identity | Form — email + name + designation |
| Role assignment | Multi-step: pick role → pick project (or tenant-wide) → confirm scope |
| Feature flags | Toggle UI per tenant/project |
| Code Masters | Tabular editor with category filter |
| Password change | Form with current + new + confirm + complexity meter |
| MFA enrollment | Wizard: QR scan → verify code → save backup codes |
| Notification preferences | Settings page — toggle per severity per channel |

### 4d. Default KPI Thresholds

| KPI | Threshold | Trigger |
|---|---|---|
| Failed login attempts | 5 in 30 min | Lock user 30 min |
| Idle session | 30 min | Auto-logout |
| Active session | 8 hours | Force re-auth |
| Refresh token | 30 days | Force re-login |
| Password age | 90 days | Force change |
| API key age | 365 days | Force rotation |
| Inactive user | 90 days no login | Auto-suspend (configurable per tenant) |

---

## BLOCK 5 — FILTERS AND VIEWS

### 5a. User Management Dashboard (System_Admin / PMO_Director)

```
Header KPIs:
  [Active Users] [Suspended] [Locked] [Pending First Login]

Table columns:
  Username | Full Name | Designation | Roles (chips) | Last Login | Status | Actions
Filters:
  Status | Role | Project | Last Login (range) | MFA Status
Sort default:
  Status (Active first) → Last Login (desc)
Bulk actions:
  Suspend | Force password reset | Re-enable
```

### 5b. Role Assignment View (per User)

```
Header:
  User: {full_name} | {email} | Status: {status}
Sections:
  Active Assignments (table: Role | Project | Scope | Valid From | Valid Until | Assigned By | Actions)
  Revoked Assignments (collapsed by default)
Actions per assignment:
  Edit valid_until | Revoke | View Audit
```

### 5c. System Audit Log View (System_Admin / PMO_Director)

```
Filter bar:
  event_category | event_type | actor_user | target_user | severity | date range | tenant
Table columns:
  Timestamp | Category | Event Type | Actor | Target | From | To | IP | Severity
Sort default: Timestamp DESC
RAG row colour: Critical = red border, Warning = amber, Info = neutral
Export: CSV (filtered)
```

### 5d. Feature Flag View

```
Group by: Module
Per flag row:
  flag_code | Tenant default | Per-project overrides (count) | Last updated
Actions: Toggle tenant default | Manage per-project overrides
```

### 5e. Code Master Editor

```
Filter: code_category dropdown
Editable table:
  code_value | display_label | tier (badge) | parent | sort_order | is_active
Standard_Core rows: read-only badge (system-locked)
Domain_Specific: editable by PMO_Director
Custom: editable by Project_Director (for own project)
```

### 5f. Self-Service User Profile

```
Sections:
  Profile (name, designation, phone, photo)
  Security (Change password, MFA, Active sessions)
  Notifications (per-severity matrix toggles)
  My Roles (read-only list across projects)
```

---

## BLOCK 6 — BUSINESS RULES

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---|---|---|---|---|
| BR-34-001 | User creation attempted | Validate: username unique within tenant; email unique within tenant; full_name ≥ 3 chars; phone format if provided | PASS → create User. Set password_must_change=true. Generate temp password emailed to user. | 🔴 Real-time |
| BR-34-002 | User created successfully | Auto-create UserNotificationPreference rows (5 rows, one per severity, defaults applied) | Notification prefs initialised. SystemAuditLog: USER_CREATED, severity=Info, is_privileged=true. | 🔴 Real-time |
| BR-34-003 | Login attempt | Resolve username → User. Check status=Active. Verify password (bcrypt). Check locked_until=null or past. | If pass: increment last_login_at; reset failed_login_count; create AuthSession; require MFA if mfa_enabled. If fail: increment failed_login_count; LoginAttempt record. | 🔴 Real-time |
| BR-34-004 | Failed login count = 5 | User has 5 failed attempts in last 30 min | Set User.locked_until = NOW() + 30min. Set status = Locked. SystemAuditLog: USER_LOCKED severity=Warning. Notify PMO_Director. | 🔴 Real-time |
| BR-34-005 | MFA mandatory role login (PMO_Director, System_Admin) | After password validation | Require TOTP before issuing access token. AuthSession.mfa_verified = true on success. | 🔴 Real-time |
| BR-34-006 | Password change | Validate: min 12 chars, mixed case + digit + symbol; not in last 3 password_history_hashes | PASS → bcrypt hash; update password_hash; push old hash to password_history (keep last 3); set password_set_at; revoke all existing AuthSessions for user. | 🔴 Real-time |
| BR-34-007 | Password age > 90 days | Daily Celery Beat | Set User.password_must_change = true. Force password change on next login. SystemAuditLog: PASSWORD_EXPIRY_FORCED. | 🟢 24hr |
| BR-34-008 | Password reset request (self-service) | Email submitted at /reset-password | Verify email exists. Rate-limit: max 3 requests per hour per email. Generate token, hash it, store in PasswordResetRequest with 60-min expiry. Email link to user. | 🔴 Real-time |
| BR-34-009 | Password reset token consumed | User clicks link with valid token | Validate token hash, not expired, not already consumed. Show password change form. On submit: BR-34-006 logic. Set PasswordResetRequest.consumed_at, status=Consumed. | 🔴 Real-time |
| BR-34-010 | UserRoleAssignment created | New assignment | Validate: user exists + active; role exists + is_assignable; project_id resolves (if not null) and is active; assigner has permission to grant this role per 4a; no duplicate (tenant, user, role, project). Validate scope_override is valid for role's permissions. | PASS → create record. SystemAuditLog: ROLE_ASSIGNED severity=Info, is_privileged=true. Notify user. Invalidate user's permission cache. | 🔴 Real-time |
| BR-34-011 | UserRoleAssignment revoked | Revocation initiated | Validate: revoker has permission. Require revocation_reason ≥ 30 chars. Set assignment_status=Revoked, revoked_by, revoked_at. Revoke all AuthSessions for user (force re-login). | SystemAuditLog: ROLE_REVOKED severity=Info. Notify user. Invalidate permission cache. | 🔴 Real-time |
| BR-34-012 | UserRoleAssignment.valid_until reached | Daily Celery Beat | For all assignments with valid_until = today: set assignment_status=Expired. Revoke user AuthSessions if no other active assignment provides project access. | SystemAuditLog: ROLE_EXPIRED severity=Info. Notify user 7 days before. | 🟢 24hr |
| BR-34-013 | User.terminated_at set | User offboarded | Cascade: revoke all UserRoleAssignments (assignment_status=Revoked, reason="User terminated {date}"); revoke all AuthSessions; set User.status=Archived; rotate API keys created by this user. | SystemAuditLog: USER_TERMINATED severity=Critical, is_privileged=true. | 🔴 Real-time |
| BR-34-014 | API request | Every authenticated API call | Resolve token → AuthSession → user_id + tenant_id. Reject if session expired or revoked. Update AuthSession.last_activity_at. | Pass user/tenant context to downstream. Idle-timeout check: if last_activity_at < NOW() − 30min, revoke session, return 401. | 🔴 Real-time |
| BR-34-015 | Permission check | Module calls `can(user_id, action, entity, scope, context)` | Resolve user roles → permissions via RolePermission. Check if (action, entity) in granted permissions. Apply scope filter (Own_Project: check user has UserRoleAssignment on context.project_id). | Return boolean. Cache for 60 sec keyed (user_id, permission_code, project_id). Invalidate cache on role change. | 🔴 Real-time |
| BR-34-016 | MFA enrollment | User initiates MFA setup | Generate TOTP secret. Encrypt with AES (key in Vault). Generate 10 backup codes. Display QR code + backup codes ONCE. Require user verify by entering current TOTP code before activation. | Set User.mfa_enabled=true. Create MFAConfig. SystemAuditLog: MFA_ENROLLED severity=Info, is_privileged=true. | 🔴 Real-time |
| BR-34-017 | MFA disable attempt | User tries to disable MFA | Block if user role has requires_mfa=true (PMO_Director, System_Admin). Otherwise: require current TOTP code. | If allowed: set mfa_enabled=false, soft-delete MFAConfig. SystemAuditLog: MFA_DISABLED severity=Warning. | 🔴 Real-time |
| BR-34-018 | Tenant config change | System_Admin edits Tenant | Validate: tenant_code immutable; subscription_tier change requires lifecycle hook. | Persist change. SystemAuditLog: TENANT_CONFIG_CHANGED severity=Critical, is_privileged=true. | 🔴 Real-time |
| BR-34-019 | FeatureFlag toggle | System_Admin or PMO_Director toggles | Validate: flag_code is registered (defined in code). Update is_enabled. Invalidate flag cache for affected scope. | SystemAuditLog: FEATURE_FLAG_CHANGED severity=Info, is_privileged=true. Notify module owners if flag is module-scoped. | 🔴 Real-time |
| BR-34-020 | CodeMaster edit | User edits a code | Validate: tier permission (Standard_Core: System_Admin only; Domain_Specific: PMO_Director; Custom: Project_Director on own project). | Persist. SystemAuditLog: CODE_MASTER_CHANGED severity=Info. Notify dependent modules to refresh cache. | 🔴 Real-time |
| BR-34-021 | API Key creation | System_Admin creates key | Generate raw key (URL-safe random 32 bytes). Show ONCE. Hash and store. Set expires_at default = today + 365d. | SystemAuditLog: API_KEY_CREATED severity=Critical, is_privileged=true. | 🔴 Real-time |
| BR-34-022 | API Key authenticated request | Service-to-service call | Verify hash matches stored. Verify not expired or revoked. Verify request scope is in permissions_scoped. Update last_used_at. | Pass key context. Reject with 401 if any check fails. | 🔴 Real-time |
| BR-34-023 | ExternalUser creation | PMO_Director or PROJECT_DIRECTOR creates external user | Validate: external_role is valid; project_access_ids ⊆ user's permission scope; valid_until ≤ today + 365d; nda_signed must be true | Generate temp password emailed; require password change on first login. SystemAuditLog: EXTERNAL_USER_CREATED severity=Info. | 🔴 Real-time |
| BR-34-024 | ExternalUser valid_until reached | Daily Celery Beat | Set ExternalUser.status=Expired. Revoke all AuthSessions. | SystemAuditLog: EXTERNAL_USER_EXPIRED. Notify creator. | 🟢 24hr |
| BR-34-025 | Idle session | User has no API activity for 30 min | Revoke AuthSession with revocation_reason=Idle_Timeout. | Next request returns 401 → user re-logs in. | 🟡 2-4hr |
| BR-34-026 | NotificationPreference quiet_hours | Notification dispatch (M11/M10) calls M34 to check | If now is in quiet_hours and severity ≠ Critical (or quiet_hours_respect_critical=true): defer to next active hour. If Critical and respect_critical=false: send immediately. | Return go/defer decision. | 🔴 Real-time |
| BR-34-027 | Inactive user | User.last_login_at < NOW() − 90 days | Daily Celery Beat | Set User.status=Suspended. Notify PMO_Director. SystemAuditLog: USER_AUTOSUSPENDED severity=Warning. | 🟢 24hr |
| BR-34-028 | Permission cache invalidation | Role assignment created/revoked, RolePermission seed updated | Invalidate Redis cache for affected user_ids | Cache cleared. | 🔴 Real-time |
| BR-34-029 | Login audit retention | Daily Celery Beat | Delete LoginAttempt records > 90 days old. Archive SystemAuditLog records > 7 years where is_privileged_action=false. Privileged: never deleted, archive to cold storage after 7y. | Records archived/deleted per OQ-2.7. | 🟢 24hr |
| BR-34-030 | Backup codes consumed | User uses TOTP backup code | Mark code consumed. If < 3 codes remaining, notify user to regenerate. If 0 remaining and TOTP unavailable, lock user — admin reset required. | SystemAuditLog: MFA_BACKUP_CODE_USED severity=Info. | 🔴 Real-time |
| BR-34-031 | Self password reset rate limit | Same email submits > 3 reset requests in 60 min | Block additional requests. SystemAuditLog: PASSWORD_RESET_RATE_LIMITED severity=Warning. | Return generic "If account exists, email sent" (do not leak existence). | 🔴 Real-time |
| BR-34-032 | First login after creation | password_must_change=true | Force password change before any other action. | Block all non-password-change endpoints. | 🔴 Real-time |
| BR-34-033 | Tenant suspension | Tenant.status → Suspended | Cascade: revoke all AuthSessions for tenant; block all logins for tenant; preserve data | SystemAuditLog: TENANT_SUSPENDED severity=Critical, is_privileged=true. | 🔴 Real-time |
| BR-34-034 | Concurrent session limit | User attempts new login while N active sessions exist | Default N=3 per user. On Nth+1: revoke oldest session. | Notify user via email: "New login from {ip}. Old session revoked." | 🔴 Real-time |
| BR-34-035 | OIDC SSO login | User logs in via OIDC provider | Validate ID token signature, issuer, audience, expiry. Resolve email → User. If user not found and tenant has SSO_AUTO_PROVISION flag: create User with default READ_ONLY role + notify PMO_Director. | Issue AuthSession with mfa_verified=true (assume IdP enforces MFA). | 🔴 Real-time |

---

## BLOCK 7 — INTEGRATION POINTS

| Direction | Module | Data Exchanged | Trigger | Speed Tier |
|---|---|---|---|---|
| SENDS TO | ALL modules | `user_id`, `tenant_id`, `roles`, `project_scope` context | Every authenticated API request | 🔴 Real-time |
| SENDS TO | ALL modules | Permission check API: `can(user, action, entity, scope, context) → boolean` | On each state-changing or privileged read | 🔴 Real-time |
| SENDS TO | ALL modules | `Role` enum reference data (seed) | Migration time + runtime cache | LINK |
| SENDS TO | ALL modules | `CodeMaster` reference data (units, doc types, sectors) | Module form rendering + cache | 🔴 Real-time |
| RECEIVES FROM | M01 Project Registry | `project_id`, `project_status` for scope resolution | On project create/status change | 🔴 Real-time |
| RECEIVES FROM | M01 Party Master | `party_id` for User.party_id linkage | On party created/updated | 🟡 2-4hr |
| SENDS TO | M01 | `User` records that are also Party representatives (back-link via party_id) | On user create with party_id | 🔴 Real-time |
| SENDS TO | M11 Action Register | UserNotificationPreference for routing decisions | On notification dispatch | 🔴 Real-time |
| RECEIVES FROM | M11 | Notification dispatch requests (forwarded for delivery) | On action assignment | 🔴 Real-time |
| SENDS TO | M10 EPCC Command | User dashboard scope (projects user can see) | On dashboard load | 🔴 Real-time |
| SENDS TO | M10 EPCC Command | Decision Queue: USER_LOCKED, ROLE_ASSIGNMENT_PENDING_REVIEW, EXTERNAL_USER_EXPIRY_PENDING | Per BR-34-004, BR-34-024 | 🔴 Real-time |
| SENDS TO | All modules | Feature flag values for module-scoped flags | On module load + on flag change | 🔴 Real-time |
| SENDS TO | All modules | Audit log shell — modules append their own events to SystemAuditLog OR maintain own logs (per OQ-1.8 hybrid) | Continuous | 🔴 Real-time |
| RECEIVES FROM | All modules | `is_privileged_action` flag for cross-cutting events (login, role change) | On qualifying events | 🔴 Real-time |
| SENDS TO | PF03 External Party Portal | ExternalUser auth context | Future (Phase 2) | 🔴 Real-time |
| SENDS TO | PF01 Mobile Field Platform | Auth tokens with extended scope (device_id) | On mobile login | 🔴 Real-time |

---

## BLOCK 8 — GOVERNANCE AND AUDIT

### 8a. Logged Events (SystemAuditLog within M34)

| Action | Logged | Detail | Visible To | Retention |
|---|---|---|---|---|
| Tenant created | Yes | All fields | System_Admin | Permanent |
| Tenant config changed | Yes | from/to per field | System_Admin | Permanent |
| User created | Yes | All initial fields | System_Admin, PMO_Director | Permanent |
| User identity edited | Yes | from/to per field | System_Admin, PMO_Director | Project lifetime |
| User suspended/unsuspended | Yes | Reason, actor | System_Admin, PMO_Director | Permanent |
| User terminated | Yes | Date, actor, cascade summary | System_Admin, PMO_Director | Permanent |
| Login success | Yes | IP, UA, MFA status | Self + System_Admin | 7 years (privileged) |
| Login failure | Yes | Reason, IP, UA | System_Admin | 90 days |
| User locked (5 failed attempts) | Yes | IP source of failures | System_Admin, PMO_Director | Permanent |
| Password changed (self) | Yes | Timestamp only (no values) | Self + System_Admin | 7 years |
| Password reset (admin-forced) | Yes | Forcer, target, reason | System_Admin, PMO_Director | Permanent |
| MFA enrolled | Yes | Method | Self + System_Admin | Permanent |
| MFA disabled | Yes | Reason | Self + System_Admin | Permanent |
| Role assigned | Yes | Target, role, project, scope, assigner | System_Admin, PMO_Director, target user | Permanent |
| Role revoked | Yes | Reason, revoker | System_Admin, PMO_Director, target user | Permanent |
| Permission cache invalidated | No | (operational, not security) | — | — |
| Feature flag changed | Yes | Flag, scope, from/to | System_Admin, PMO_Director | Permanent |
| Code Master changed | Yes | Category, code, from/to | System_Admin, PMO_Director | Permanent |
| API Key created | Yes | Name, scope, expires_at, prefix | System_Admin | Permanent |
| API Key revoked | Yes | Reason | System_Admin | Permanent |
| External User created | Yes | All fields | PMO_Director, Project_Director (own project) | Permanent |
| External User revoked/expired | Yes | Reason | PMO_Director | Permanent |

### 8b. Immutability Rules

- `SystemAuditLog` is APPEND-ONLY. No updates. No soft delete. Records archived to cold storage; never deleted.
- `LoginAttempt` is rotational (90-day retention).
- `User.password_hash` history: last 3 retained in `password_history_hashes`. Older not retained (privacy + bcrypt cost).
- `MFAConfig.totp_secret_encrypted` cleared on user termination (not just soft-deleted) — reduces breach surface.

### 8c. Privacy Rules (DPDP Act 2023 alignment)

- Per-tenant `dpdp_data_fiduciary_name` and `dpdp_grievance_officer_email` — surfaced on user-facing privacy notice.
- User's right to data export: API endpoint to download all user-related records (activity, audit logs concerning self).
- User's right to deletion: PMO_Director-initiated GDPR-style erasure. Records redacted (PII removed, IDs preserved) for historical audit integrity.

---

## BLOCK 9 — EXPLICIT EXCLUSIONS

```
This module does NOT:
─────────────────────────────────────────────────────────────────────
[ ] Define module-specific business rules                         → Each module spec
[ ] Store module-specific entity data                             → Each module
[ ] Own per-module audit log content (post-hybrid split)          → Each module Block 8
[ ] Manage notification dispatch logic                            → M10/M11 notification engine
[ ] Authenticate external party portal flows                      → PF03 (uses M34 ExternalUser)
[ ] Bind mobile devices to users                                  → PF01 (extends M34 auth)
[ ] Manage Party master records                                   → M01
[ ] Manage Project master records                                 → M01
[ ] Generate Decision Queue items beyond auth/RBAC events         → Each module
[ ] Store user uploads or evidence files                          → MinIO + per-module references
[ ] Track contractor / vendor employee performance                → M04 + M30
[ ] Make business approval decisions (e.g., approve VO)           → Each module owns its own approvals
[ ] Calculate any business KPI                                    → M07 EVM, M10 Command
[ ] Provide user training                                         → M21 Training & Competency
[ ] Decide who reports to whom (org chart)                        → Outside EPCC scope (HR system)
```

---

## BLOCK 10 — OPEN QUESTIONS

**All v1.0 questions resolved. Zero open questions.**

| # | Question | Resolution |
|---|---|---|
| 1 | Role hierarchy — flat or hierarchical? | **Flat (OQ-1.1=A).** Every permission explicitly granted via RolePermission. Audit clarity wins. |
| 2 | Multi-project users — same role or per-project? | **Per-project (OQ-1.2=B).** UserRoleAssignment is per-project; tenant-wide assignment via project_id=NULL. |
| 3 | Permission granularity? | **Entity + scope, with selective field-level (OQ-1.3=D).** Permission has is_field_level + field_name optional. RolePermission has default_scope. Field-level enforced at API serialisation. |
| 4 | CIO vs PMO_Director? | **Eliminated CIO (OQ-1.4=A).** PIOE re-issue replaces references. Only PMO_DIRECTOR exists. |
| 5 | External users — same table or separate? | **Separate (OQ-1.5=B).** ExternalUser entity with own auth_method, project_access_ids whitelist, mandatory NDA, mandatory valid_until ≤ 365d. |
| 6 | Authentication — local / SSO / both? | **Both (OQ-1.6=C).** Local default; OIDC configurable per tenant. ExternalUser only supports Local_External or Email_Magic_Link (no SSO). |
| 7 | Custom roles — code-locked or runtime? | **Code-locked (OQ-1.7=A).** New role = new release. Adding role = Alembic migration + RolePermission seed update. |
| 8 | AuditLog — central or per-module? | **Hybrid (OQ-1.8=C).** M34 owns SystemAuditLog for cross-cutting events (auth, RBAC, tenant config, code masters, feature flags, API keys, user lifecycle). Modules own their own state-change logs in their Block 8. |
| 9 | Feature flags — granularity? | **Tenant + project (OQ-1.9=C).** project_id NULL = tenant-wide; specified = project-specific override. |
| 10 | User → Party linkage? | **Optional FK on User (OQ-1.10=A).** User.party_id nullable. Party-employed users (e.g., contractor's site engineer) can be linked. ExternalUser uses affiliated_party_id separately. |
| 11 | OQ-2 password policy | **Min 12, mixed case + digit + symbol; 90d rotation; last-3 history.** Per OQ-2.4. |
| 12 | OQ-2 session timeouts | **8h active / 30m idle / 30d refresh.** Per OQ-2.5. |
| 13 | OQ-2 MFA mandatory | **System_Admin and PMO_Director mandatory; Portfolio_Manager and Finance_Lead recommended.** Per OQ-2.6 and Role.requires_mfa flag. |
| 14 | OQ-2 audit retention | **Permanent (privileged); 7 years (routine); 90 days (login attempts).** Per OQ-2.7. |
| 15 | OQ-2 rate limiting | **60 req/min per user; 600 req/min per API key.** Per OQ-2.9. Enforced at API gateway. |
| 16 | OQ-2 password reset | **1-hour expiry, single-use, rate-limited 3/hour.** Per OQ-2.10. |
| 17 | Concurrent sessions per user | **Max 3 active simultaneous sessions; oldest revoked on Nth+1 login.** Per BR-34-034. |
| 18 | Inactive user auto-suspension | **90 days no login → suspended.** Per BR-34-027. Configurable per tenant in v2.0. |
| 19 | OIDC auto-provisioning | **Optional flag SSO_AUTO_PROVISION per tenant.** If true, unknown SSO email → create User with READ_ONLY role + notify PMO_Director. If false, login fails. |
| 20 | Backup codes for MFA | **10 codes generated at enrollment, single-use each, regenerable, < 3 remaining triggers warning.** Per BR-34-030. |

---

## APPENDIX A — Permission Code Convention

Every permission follows: `{action}_{entity}` or `{action}_{entity}_{qualifier}`.

Examples:
```
view_project
create_project
edit_project
delete_project
approve_variation_order
view_boq_actual_rate           ← field-level (is_field_level=true, field_name=actual_rate)
configure_kpi_threshold
export_evm_snapshot
impersonate_user               ← System_Admin only
```

Module specs MUST register their permissions during spec writing. M34 spec lock triggers a permission seed update task before any module's API can be tested.

---

## APPENDIX B — Permission Cache Strategy

```
Cache key: rbac:perm:{user_id}:{permission_code}:{project_id}
Cache value: boolean
Cache TTL: 60 seconds
Invalidation triggers:
  - UserRoleAssignment created/revoked → invalidate all keys for user_id
  - RolePermission seed change → invalidate full namespace (rare; on release)
  - Tenant suspended → invalidate all keys for tenant
Backing store: Redis (per Engineering Standards)
```

---

## APPENDIX C — Migration Notes

```
Migration: 20260503_0001_m34_initial_schema.py
  - Creates Tenant, User, Role, Permission, RolePermission, UserRoleAssignment,
    ExternalUser, AuthSession, AuthToken, MFAConfig, PasswordResetRequest,
    LoginAttempt, SystemAuditLog, FeatureFlag, CodeMaster, APIKey,
    UserNotificationPreference

Migration: 20260503_0002_m34_seed_roles_permissions.py
  - Seeds 17 roles per locked taxonomy
  - Seeds Standard_Core CodeMaster entries (units, currencies, severities)
  - No permissions seeded yet (modules register their own during spec lock)

Migration: 20260503_0003_m34_seed_permissions_m34_self.py
  - Seeds M34's own 30+ permissions (manage users, view audit, etc.)
  - Seeds RolePermission rows for M34 actions per Block 4a matrix
```

---

## APPENDIX D — API Surface (sketch — full OpenAPI in implementation phase)

**Auth endpoints:**
```
POST   /api/v1/auth/login              { username, password }
POST   /api/v1/auth/logout             (no body, session-bound)
POST   /api/v1/auth/refresh            { refresh_token }
POST   /api/v1/auth/mfa/verify         { code }
POST   /api/v1/auth/password/reset     { email }                    (init)
POST   /api/v1/auth/password/reset/confirm { token, new_password }   (consume)
POST   /api/v1/auth/password/change    { current, new }
POST   /api/v1/auth/sso/oidc/start     { tenant_code }
GET    /api/v1/auth/sso/oidc/callback  ?code&state
```

**MFA:**
```
POST   /api/v1/auth/mfa/enroll/start
POST   /api/v1/auth/mfa/enroll/verify  { code }
POST   /api/v1/auth/mfa/disable        { code }
POST   /api/v1/auth/mfa/backup/regenerate
```

**Admin user management:**
```
GET    /api/v1/admin/users
POST   /api/v1/admin/users
GET    /api/v1/admin/users/{user_id}
PATCH  /api/v1/admin/users/{user_id}
POST   /api/v1/admin/users/{user_id}/suspend
POST   /api/v1/admin/users/{user_id}/terminate
POST   /api/v1/admin/users/{user_id}/force-password-reset
```

**Role assignment:**
```
GET    /api/v1/admin/users/{user_id}/roles
POST   /api/v1/admin/users/{user_id}/roles      { role_code, project_id, scope_override, valid_until }
DELETE /api/v1/admin/users/{user_id}/roles/{assignment_id}    { revocation_reason }
```

**Audit:**
```
GET    /api/v1/admin/audit                ?event_category&event_type&from&to&actor
GET    /api/v1/users/me/audit             (self-only audit trail)
```

**Tenant + config:**
```
GET    /api/v1/admin/tenants
PATCH  /api/v1/admin/tenants/{tenant_id}
GET    /api/v1/admin/feature-flags
PATCH  /api/v1/admin/feature-flags/{flag_id}
GET    /api/v1/admin/code-masters
POST   /api/v1/admin/code-masters
PATCH  /api/v1/admin/code-masters/{code_id}
```

**Permission check (internal — used by other modules):**
```
POST   /internal/v1/rbac/can             { user_id, permission_code, project_id?, record_id? }
```

---

*v1.0 — Spec locked. Zero open questions. Ready for Round 3 (Wireframes).*
