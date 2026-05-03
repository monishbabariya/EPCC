# M09 — Compliance Tracker
## Module Specification v2.1
## AMENDMENT — Changed Blocks Only
**Status:** Draft — Pending Review | **Locked:** No
**Spec Author:** PMO Director | **Date:** 2026-05-02
**Reference Standards:** EPCC_Standards_Memory_v5_1.md
**Base Version:** M09_Compliance_v2.0
**Amendment Scope:** GAP-07: DLPComplianceObservation entity for NABH re-inspection and
                     regulatory observations during DLP period. Post-SG-11 compliance
                     tracking mode. Revenue readiness impact of DLP non-compliance.

---

## CHANGE LOG

| Version | Date | Change Summary |
|---------|------|---------------|
| v2.0 | 2026-04-30 | Full spec: NABH multi-pathway, JCI ready, compliance checklist guidance, revenue readiness formula |
| v2.1 | 2026-05-02 | GAP-07: DLPComplianceObservation entity. Post-SG-11 NABH tracking mode. DLP non-compliance → M05 risk signal. DLP non-compliance → licensing_readiness_pct impact. BR-09-031 through BR-09-038 added. Block 7 integration updated. |

---

## BLOCK 2 — Scope Boundary (Updated)

**ADDITIONS to INCLUDES:**

| INCLUDES (New) | Rationale |
|----------------|-----------|
| `DLPComplianceObservation` — NABH and regulatory observations during DLP period | GAP-07: NABH re-inspections during DLP can expose non-compliances that affect licensing |
| Post-SG-11 NABH tracking mode — standard-level observations and resolution | GAP-07 |
| DLP Non_Compliance → M05 risk signal (regulatory non-compliance = licensing risk) | GAP-07: DLP regulatory issues are business risks requiring M05 risk register entries |
| DLP compliance status → licensing_readiness_pct adjustment | GAP-07: Unresolved DLP non-compliance reduces operational licensing score |

**ADDITION to EXCLUDES:**

| EXCLUDES (Clarification) |
|--------------------------|
| Physical defect management during DLP → M04 (DLPDefect). M09 tracks only compliance/regulatory observations. |
| DLP retention release decisions → M06 |
| DLP period dates and defect counts → M04 DLPRegister is the master |

---

## BLOCK 3 — Data Architecture (Amendment)

### 3a. New Entity

| Entity | Description | Cardinality |
|--------|-------------|-------------|
| `DLPComplianceObservation` | **(NEW v2.1)** Records NABH re-inspection findings, AERB post-commissioning observations, and other regulatory authority observations during the DLP period. Distinct from construction-phase compliance tracking. | Many per project |

---

### 3b. New Entity Fields — `DLPComplianceObservation`

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `observation_id` | UUID | Y | Auto-generated | SYSTEM |
| `tenant_id` | UUID | Y | — | SYSTEM |
| `project_id` | UUID | Y | — | LINK → M01 Project |
| `dlp_id` | UUID | Y | FK → M04 DLPRegister. Cannot create observation if DLPRegister.status ≠ Active. | LINK → M04 DLPRegister |
| `compliance_item_id` | UUID | Y | FK → M09 ComplianceItem (which framework raised this observation). e.g., NABH, AERB. | LINK → ComplianceItem |
| `nabh_standard_id` | UUID | N | FK → M09 ComplianceStandard. Required if compliance_item_id references NABH. | LINK → ComplianceStandard |
| `observation_code` | VARCHAR(20) | Y | System-generated. Format: DLP-OBS-{seq_pad3}. e.g., DLP-OBS-001. | SYSTEM |
| `observation_type` | ENUM | Y | `NABH_Inspection / AERB_Post_Commissioning / PCB_Renewal / Fire_Renewal / Regulatory_Condition / Voluntary_Audit` | INPUT (dropdown) |
| `observation_date` | DATE | Y | Date observation was made. Must be ≥ DLPRegister.dlp_start_date. | INPUT |
| `observed_by_type` | ENUM | Y | `External_Auditor / Regulatory_Authority / Internal_Audit` | INPUT (dropdown) |
| `observed_by_name` | VARCHAR(200) | Y | Name of auditor, authority, or audit team. | INPUT |
| `observation_text` | TEXT | Y | Min 50 chars. Specific description of what was observed / the non-compliance. | INPUT |
| `severity` | ENUM | Y | `Non_Compliance / Observation / Recommendation` | INPUT (dropdown) |
| `nabh_chapter` | VARCHAR(100) | N | NABH chapter reference. e.g., "AAC — Access, Assessment and Continuity of Care" | INPUT |
| `nabh_standard_ref` | VARCHAR(50) | N | Specific NABH standard number. e.g., "AAC.1.2" | INPUT |
| `documentary_evidence_url` | VARCHAR(500) | N | Data Lake URL — audit report, inspection note | INPUT |
| `compliance_response` | TEXT | N | How the team will address this observation. Required before status → Response_Submitted. Min 50 chars. | INPUT |
| `response_due` | DATE | Y | CALC: Non_Compliance = observation_date + 14 days. Observation = observation_date + 30 days. Recommendation = observation_date + 60 days. | CALC |
| `response_date` | DATE | N | Date response was submitted to authority | INPUT |
| `linked_defect_id` | UUID | N | FK → M04 DLPDefect if this observation is directly tied to a physical defect. | LINK → M04 DLPDefect |
| `m05_risk_id` | UUID | N | FK → M05 Risk record auto-created for Non_Compliance severity. | LINK → M05 Risk |
| `resolution_status` | ENUM | Y | `Open / Response_Submitted / Verification_Pending / Closed` | SYSTEM |
| `verification_date` | DATE | N | Date authority confirmed resolution | INPUT |
| `verified_by` | VARCHAR(200) | N | Authority or auditor who confirmed resolution | INPUT |
| `closed_at` | TIMESTAMP | N | Auto on status → Closed | SYSTEM |
| `licensing_impact` | BOOLEAN | Y | CALC: true if severity = Non_Compliance AND resolution_status ≠ Closed | CALC |

---

### 3b. Updated Fields — `ComplianceReadinessSnapshot` (v2.1)

New fields added to existing entity:

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `dlp_phase_active` | BOOLEAN | Y | **(NEW)** True when M04 DLPRegister.status = Active for this project | LINK → M04 DLPRegister |
| `open_dlp_non_compliance_count` | INTEGER | N | **(NEW)** Count of DLPComplianceObservations with severity = Non_Compliance AND resolution_status ≠ Closed | CALC |
| `dlp_licensing_impact_count` | INTEGER | N | **(NEW)** Count of DLPComplianceObservations with licensing_impact = true | CALC |
| `licensing_readiness_pct_dlp_adjusted` | DECIMAL(5,4) | N | **(NEW)** Adjusted licensing_readiness_pct after DLP non-compliance deduction. Feeds M10 RR formula when dlp_phase_active = true. | CALC |

**DLP adjustment formula:**
```
If dlp_phase_active = true AND open_dlp_non_compliance_count > 0:
  licensing_readiness_pct_dlp_adjusted =
    licensing_readiness_pct × (1 − 0.10 × open_dlp_non_compliance_count)
  Cap: minimum 0.50 (50%) — DLP non-compliance cannot reduce below 50% regardless of count
  (prevents punitive over-reduction while still flagging the issue)

If dlp_phase_active = false OR open_dlp_non_compliance_count = 0:
  licensing_readiness_pct_dlp_adjusted = licensing_readiness_pct (no adjustment)

M10 uses licensing_readiness_pct_dlp_adjusted in the Revenue Readiness formula (§7.82)
when dlp_phase_active = true.
```

---

### 3b. Updated Fields — `NABHPathwayConfig` (v2.1 — DLP mode flag)

| Field | Type | Required | Validation Rule | Source |
|-------|------|----------|-----------------|--------|
| `dlp_audit_mode` | BOOLEAN | Y | **(NEW)** Default false. Set true on M04 DLPRegister activation (SG-11 signal). When true: standard-level NABH tracking activated for post-handover compliance monitoring. | SYSTEM |
| `dlp_audit_activated_at` | TIMESTAMP | N | **(NEW)** Populated when dlp_audit_mode → true | SYSTEM |
| `post_handover_nabh_target` | DATE | N | **(NEW)** Target date for NABH final accreditation inspection (post-operations commencement). | INPUT (Compliance Manager) |

---

## BLOCK 6 — Business Rules (Amendment — new rules v2.1)

*All existing rules BR-09-001 through BR-09-030 from v2.0 remain in force.*

| Rule ID | Trigger | Logic | Output | Speed Tier |
|---------|---------|-------|--------|------------|
| BR-09-031 | M04 sends DLP activation signal (SG-11 passed) | M04 DLPRegister.status → Active signal received | Set `NABHPathwayConfig.dlp_audit_mode = true`. Set `dlp_audit_activated_at = NOW()`. Update `ComplianceReadinessSnapshot.dlp_phase_active = true`. Notify Compliance Manager: "DLP phase activated. Post-handover NABH compliance tracking is now active." | 🔴 Real-time |
| BR-09-032 | DLPComplianceObservation created | New observation record saved | Validate: dlp_id references an Active DLPRegister. Validate: observation_date ≥ DLPRegister.dlp_start_date. Auto-generate observation_code. Update `ComplianceReadinessSnapshot`: recalculate open_dlp_non_compliance_count and dlp_licensing_impact_count. | 🔴 Real-time |
| BR-09-033 | DLPComplianceObservation with severity = Non_Compliance | Detected on save | Auto-create M05 Risk record: category = REGULATORY, sub_category = REGULATORY-NABH, description = "DLP NABH Non_Compliance: {observation_code} — {nabh_standard_ref}. Response due {response_due}.", severity = High, probability = Medium (already materialised partially). Set `m05_risk_id` on observation record. Notify PMO Director + Compliance Manager. | 🔴 Real-time |
| BR-09-034 | DLPComplianceObservation response_due breached | response_due < today AND resolution_status = Open | Decision Queue item: DLP_COMPLIANCE_RESPONSE_OVERDUE. Severity: Critical (Non_Compliance), High (Observation). Owner = Compliance Manager. SLA = 24hr. Governance breach for Non_Compliance items unresponsed > 48hr total. | 🟡 2-4hr |
| BR-09-035 | DLPComplianceObservation status → Closed | verification_date populated AND verified_by populated | Recalculate open_dlp_non_compliance_count. Recalculate licensing_readiness_pct_dlp_adjusted. Send updated counts to M06 (m09_open_non_compliance updated). If M05 risk record linked: signal M05 to transition Risk status to Mitigated. If linked_defect_id: signal M04 that observation is closed. | 🔴 Real-time |
| BR-09-036 | licensing_readiness_pct_dlp_adjusted recalculates | open_dlp_non_compliance_count changes | Apply DLP adjustment formula. Update ComplianceReadinessSnapshot. Send updated licensing_readiness_pct to M10 (via ComplianceReadinessSnapshot daily snapshot or real-time signal if change > 5%). | 🟡 2-4hr |
| BR-09-037 | DLPComplianceObservation: Non_Compliance on AERB post-commissioning | observation_type = AERB_Post_Commissioning AND severity = Non_Compliance | Additional escalation: PMO Director + Safety Officer notified immediately. AERB non-compliance during DLP is regulatory risk to continued LINAC operation. Decision Queue: CRITICAL, 12hr SLA, PMO Director. | 🔴 Real-time |
| BR-09-038 | DLP phase ends (M04 DLPRegister.status → Closed signal received) | DLP period over AND all defects resolved | Set NABHPathwayConfig.dlp_audit_mode = false. Final ComplianceReadinessSnapshot.dlp_phase_active = false. If any DLPComplianceObservation still open: alert Compliance Manager: "DLP period closed but {N} compliance observations still open. These require resolution for ongoing licensing." | 🔴 Real-time |

---

## BLOCK 7 — Integration Points (Amendment)

| Direction | Module | Data Exchanged | Trigger | Speed Tier |
|-----------|--------|---------------|---------|------------|
| RECEIVES FROM | M04 Execution Capture | **(NEW v2.1)** DLP activation signal (dlp_start_date, dlp_end_date) | On SG-11 activation in M04 (forwarded from M08) | 🔴 Real-time |
| RECEIVES FROM | M04 Execution Capture | **(NEW v2.1)** DLPRegister.status → Closed signal | On DLP retention release completion (BR-04-038 → M06 → M04 closure) | 🔴 Real-time |
| RECEIVES FROM | M04 Execution Capture | **(NEW v2.1)** DLPDefect.nabh_observation_link — defect closure signal | On DLPDefect status → Closed where nabh_observation_link set | 🔴 Real-time |
| SENDS TO | M05 Risk & Change | **(NEW v2.1)** Auto-created Risk record for Non_Compliance DLP observations | On BR-09-033 | 🔴 Real-time |
| SENDS TO | M06 Financial Control | **(NEW v2.1)** m09_open_non_compliance count update | On DLPComplianceObservation create/close | 🟡 2-4hr |
| SENDS TO | M10 EPCC Command | Updated licensing_readiness_pct_dlp_adjusted + open_dlp_non_compliance_count | On ComplianceReadinessSnapshot (🟢 24hr) or significant change (🟡 2-4hr) | 🟡/🟢 |
| SENDS TO | M08 Gate Control | Compliance status per regulatory item for gate criteria (unchanged) | On compliance status change | 🔴 Real-time |

---

## BLOCK 9 — Explicit Exclusions (Amendment — additions)

```
[ ] Physical defect tracking during DLP                      → M04 DLPDefect
[ ] DLP retention release blocking                           → M06 owns. M09 provides count signal only.
[ ] DLP period dates or defect counts                        → M04 DLPRegister is master
[ ] Approve DLP retention release override                   → M06 (Finance Lead + PMO Director)
[ ] Post-DLP warranty management                             → Outside EPCC scope
```

---

## BLOCK 10 — Open Questions

**All questions resolved. Zero open questions.**

| # | Question | Resolution |
|---|----------|-----------|
| 1 | Can a DLPComplianceObservation exist without a physical defect link? | Yes. A NABH observation may be procedural (missing record, untrained staff, protocol gap) with no physical defect. linked_defect_id is optional. The two entities are independent but cross-referenceable. |
| 2 | Does AERB have DLP-equivalent post-commissioning requirements for LINAC? | Yes — AERB issues a commissioning clearance but also requires periodic safety audits and may issue post-commissioning observations. These are tracked as DLPComplianceObservation with observation_type = AERB_Post_Commissioning. Separate from AERB initial clearance (tracked in ComplianceItem during construction). |
| 3 | What happens to the NABH accreditation pathway during DLP? | NABHPathwayConfig.dlp_audit_mode = true shifts tracking from construction-phase chapter monitoring to standard-level operational compliance. The pathway (Entry/Pre/Full) does not change — DLP is the period when the hospital proves it can maintain the standard operationally. |
| 4 | Does DLP non-compliance affect M10 project health index? | Yes — through licensing_readiness_pct_dlp_adjusted flowing into the Revenue Readiness formula (§7.82), which in turn affects the Compliance dimension of the Project Health Index in M10. The impact is bounded (minimum 50% licensing score) to prevent catastrophic health index collapse for minor observations. |
