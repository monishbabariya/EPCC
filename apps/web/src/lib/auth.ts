/**
 * Auth helpers (OIDC + local fallback).
 *
 * Round 25 scaffold: stub. Real Keycloak integration lands in Round 27
 * with the M34 thin slice.
 */

export const ROLES = [
  "SYSTEM_ADMIN",
  "PMO_DIRECTOR",
  "PORTFOLIO_MANAGER",
  "PROJECT_DIRECTOR",
  "PLANNING_ENGINEER",
  "QS_MANAGER",
  "FINANCE_LEAD",
  "PROCUREMENT_OFFICER",
  "SITE_MANAGER",
  "COMPLIANCE_MANAGER",
  "ANALYST",
  "READ_ONLY",
  "EXTERNAL_AUDITOR",
  "CLIENT_VIEWER",
  "LENDER_VIEWER",
  "NABH_ASSESSOR",
  "CONTRACTOR_LIMITED",
] as const;

export type Role = (typeof ROLES)[number];
