# EPCC — Deployment Tier Specification
## Version 1.0
**Owner:** PMO Director / Product
**Created:** 2026-05-02
**Scope:** Defines two deployment models for EPCC across different EPC client profiles.
           Governs commercial packaging, infrastructure provisioning, and contractual
           data isolation commitments.
**Status:** Draft — Pending PMO Director Review | Locked: No
**Relationship to Engineering Standards:** Does not modify ES-DB-001 (schema-per-tenant).
           Tier 2 uses the same codebase, same schema model, deployed on separate infrastructure.

---

## CHANGE LOG

| Version | Date | Change Summary |
|---------|------|----------------|
| v1.0 | 2026-05-02 | Initial specification. Closes multi-EPC deployment question. |

---

## 1. WHY TWO TIERS EXIST

EPCC serves two fundamentally different client profiles:

**Profile A — Growing EPC / PMC / Hospital Trust**
- 1–5 active projects
- Does not have dedicated IT infrastructure for project management software
- Primary concern: capability and cost
- Data residency: comfortable with managed hosted service
- Procurement: departmental or PMO Director decision

**Profile B — Large Enterprise EPC Firm**
- 10+ active projects, multi-portfolio
- Has existing IT governance, security policy, and compliance mandates (ISO 27001, SOC 2)
- Primary concern: data sovereignty and competitive confidentiality
- Data residency: contractually requires their data not to co-reside with competitor firms
- Procurement: IT + Legal + CTO sign-off required

A single deployment model cannot serve both profiles without over-engineering for Profile A
or under-delivering for Profile B. Two tiers solve this cleanly.

---

## 2. TIER DEFINITIONS

---

### TIER 1 — Multi-Tenant Shared Deployment

**Target client:** Growing EPC firms, PMCs, hospital trusts, government project offices

**Infrastructure model:**
```
One EPCC instance (Docker Compose stack)
  └── One PostgreSQL instance
        ├── public schema          → shared reference data
        ├── tenant_client_a        → Client A's full M01–M10 data
        ├── tenant_client_b        → Client B's full M01–M10 data
        └── tenant_client_n        → Client N's full M01–M10 data
```

**Isolation mechanism:** Schema-per-tenant (ES-DB-001). PostgreSQL `search_path` enforcement
+ `tenant_id` JWT injection. Cross-tenant queries prohibited at application layer.

**What EPCC commits to contractually in Tier 1:**
- Your data is stored in a dedicated, isolated schema
- No application query can read or write another tenant's schema
- Your data is never used to train models or improve features without explicit consent
- Per-tenant backups are available on request (ES-DR-002 v1.2)
- You can request a full export of your tenant schema at any time

**What EPCC does NOT commit to in Tier 1:**
- Physical server dedicated to you alone
- Guarantee that no other EPC firm's data exists on the same PostgreSQL instance
- Independent maintenance windows (all tenants share the same deployment cycle)

**Capacity:** Up to 50 active tenants per Tier 1 instance. Beyond 50: provision a second
Tier 1 instance or migrate large clients to Tier 2.

**Pricing model:** SaaS subscription — per active project per month (suggested)

---

### TIER 2 — Dedicated Single-Tenant Deployment

**Target client:** Large enterprise EPC firms with contractual data residency requirements
or internal IT governance mandates

**Infrastructure model:**
```
Dedicated infrastructure per client (two options):

OPTION A — Client's Own Infrastructure (On-Premises)
  Client provides: Server hardware, network, OS
  EPCC provides: Docker Compose stack, deployment runbook, support
  Data never leaves client's premises
  Client's IT team manages the server

OPTION B — Dedicated Cloud Tenancy (EPCC-Managed)
  EPCC provisions a dedicated cloud VPC (AWS/Azure/GCP) per client
  No shared infrastructure with any other client
  EPCC manages operations; client has read access to their environment
  Data residency in region of client's choice (Mumbai for Indian EPCs)
```

**Isolation mechanism:** Physical infrastructure separation. No schema routing needed —
the entire PostgreSQL instance belongs to this client. Codebase identical to Tier 1;
`tenant_id` enforcement still present (future-proofing for sub-tenants or JV structures).

**What EPCC commits to contractually in Tier 2:**
- Your data exists only on infrastructure dedicated to your organisation
- No other EPC firm's data is on the same server, the same PostgreSQL instance,
  or the same cloud VPC
- You have the right to audit the server at any time
- You control the backup schedule and retention policy for your instance
- You can terminate the contract and take your data (full pg_dump) with zero friction
- Independent maintenance windows — upgrades on your schedule (within 30-day window)

**Additional Tier 2 capabilities (enabled by dedicated infrastructure):**
- Custom domain: `epcc.clientname.com` vs `clientname.epcc.io`
- Client's own SSL certificate
- Integration with client's SSO/LDAP (SAML 2.0 — future Phase 2 feature)
- Client's own MinIO instance or S3 bucket for document storage
- Custom data retention policy beyond EPCC defaults
- Dedicated Grafana instance — client's own observability

**Pricing model:** Annual enterprise license + one-time deployment fee + annual support

---

## 3. FEATURE PARITY

Both tiers run identical EPCC software (same Docker image, same codebase, same module versions).
There is no "premium features only in Tier 2." The difference is exclusively infrastructure and contractual.

| Feature | Tier 1 | Tier 2 |
|---|---|---|
| All M01–M10 modules | ✅ | ✅ |
| PIOE | ✅ | ✅ |
| All business rules, EVM, Gate Control | ✅ | ✅ |
| WhatsApp notifications | ✅ | ✅ |
| Power BI reporting layer | ✅ | ✅ |
| Physical infrastructure isolation | ❌ | ✅ |
| Independent maintenance window | ❌ | ✅ |
| Custom SSO/LDAP (Phase 2) | ❌ | ✅ |
| Dedicated observability stack | ❌ | ✅ |
| Client-owned backup control | ❌ | ✅ |
| Custom domain + SSL | ❌ | ✅ |
| On-premises deployment option | ❌ | ✅ |

---

## 4. ENGINEERING IMPACT

**Tier 2 requires zero engineering changes to the EPCC codebase.**

The same Docker Compose stack is deployed to a dedicated server or VPC with one configuration
difference: `TENANT_COUNT=1` environment variable. The middleware still enforces `tenant_id`
and `search_path` — this is correct behaviour even for a single-tenant instance and allows
future sub-tenant support without rework.

**Provisioning difference:**

| Step | Tier 1 | Tier 2 |
|---|---|---|
| Infrastructure | Shared — already running | Provision new server/VPC |
| Docker Compose | Add tenant schema to existing instance | Fresh deployment on new instance |
| DNS | Add subdomain to shared pool | Configure client's custom domain |
| SSL | Wildcard cert covers new subdomain | Client's own cert or Let's Encrypt |
| Time to provision | < 1 hour (automated schema creation) | 1–3 days (infrastructure provisioning) |
| Ongoing ops overhead | Negligible — part of shared ops | +1 deployment to monitor per client |

**Alembic migration deployment for Tier 2:**

Tier 2 clients get migrations on their own schedule (within the 30-day window after release).
The CI/CD pipeline (ES-CICD-001) supports a `--target-instance` parameter that routes the
migration to a specific deployment. Tier 2 migration is a separate GitHub Actions job
triggered manually by the System Admin after Tier 1 migration is confirmed stable.

---

## 5. DECISION FRAMEWORK — WHICH TIER FOR A NEW CLIENT

```
New client onboarding:

QUESTION 1: Does the client have a contractual requirement stating their data
            cannot co-reside with competitors or other organisations?
  YES → Tier 2 automatically. No further questions.
  NO  → Continue to Question 2.

QUESTION 2: Does the client have an internal IT governance policy (ISO 27001,
            SOC 2, internal security standards) that mandates dedicated infrastructure
            for third-party SaaS tools?
  YES → Tier 2 recommended. PMO Director + client IT to confirm.
  NO  → Continue to Question 3.

QUESTION 3: Does the client have 10+ active projects or an annual contract
            value above ₹50 Cr?
  YES → Offer Tier 2 as an option (enterprise positioning). Default to Tier 1
        unless client requests Tier 2.
  NO  → Tier 1.
```

---

## 6. MIGRATION PATH: TIER 1 → TIER 2

A client starting on Tier 1 who grows into Tier 2 requirements can migrate without data loss:

```
Step 1: Provision Tier 2 infrastructure for the client
Step 2: pg_dump --schema=tenant_{slug} from Tier 1 instance (ES-DR-002 per-schema backup)
Step 3: pg_restore to new dedicated Tier 2 PostgreSQL instance
Step 4: Run Alembic migrate to confirm schema is at current HEAD
Step 5: DNS cutover (update client's subdomain to new instance)
Step 6: 48hr parallel run — both instances active, writes to Tier 2 only
Step 7: Confirm Tier 2 stable → decommission client's schema from Tier 1 instance
        (soft-delete tenant record in Tier 1 TenantMaster)
Step 8: Provide client with confirmation of full data migration + deletion from Tier 1
```

**Migration is non-destructive and reversible until Step 7.** The per-schema backup capability
(ES-DR-002 v1.2) is what makes this migration path clean — it exists precisely for this scenario.

**Estimated migration window:** 4–6 hours. Can be scheduled Saturday midnight with zero
business-hours impact.

---

## 7. WHAT THIS SPEC CLOSES

| Concern | Resolution |
|---|---|
| "Multiple EPC firms on same DB is a data risk" | ES-DB-001 schema isolation is technically complete. Tier 2 provides contractual and physical isolation for clients who require it. |
| "Competitor data on same server" | Tier 2 dedicated deployment. Physical separation guaranteed. |
| "Cannot restore one EPC firm without affecting others" | ES-DR-002 v1.2 per-schema backup. Surgical per-tenant restore. |
| "Large EPC firm won't sign with shared infrastructure" | Tier 2 option closes the enterprise sales objection. |
| "Schema-per-tenant was the wrong decision" | Confirmed correct. Schema-per-tenant serves Tier 1. Tier 2 gets dedicated infrastructure — codebase unchanged. |

---

*Spec complete. Zero open questions.*
*ES-DB-001 (schema-per-tenant) remains locked and unchanged.*
*This document is a product and commercial specification, not an engineering change.*
