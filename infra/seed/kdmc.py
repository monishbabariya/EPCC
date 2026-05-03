"""KDMC-001-DBOT pilot seed.

Round 25 scaffold: prints a structured plan of what will be seeded once the
M34 + M01 thin slices ship. Real seed runs in Round 27/28.

Per `EPCC_BuildArchitecture_Spec_v1_0.md` §Appendix B and OQ-1.6 (locked
Round 23), `make seed` is the single command that takes a clean Postgres
to a demo-ready KDMC tenant.
"""

from __future__ import annotations

KDMC_TENANT = {
    "code": "kdmc",
    "name": "Kalyan-Dombivli Municipal Corporation",
}

KDMC_PROJECT = {
    "code": "KDMC-001-DBOT",
    "name": "150-bed Maternity, Cancer & Cardiology Hospital",
    "delivery_model": "DBOT",
    "sector_top_level": "Healthcare",
    "sector_sub_type": "Hospital_DBOT",
    "value_inr_cr": 68.4,
    "client": "Kalyan-Dombivli Municipal Corporation",
    "contractor": "L&T Construction",
    "phase": "Construction",
    "pincode": "421203",
    "region": "West",
}

ROLES_TO_SEED = [
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
]


def main() -> None:
    print("=" * 72)
    print("KDMC-001-DBOT pilot seed (Round 25 scaffold — plan only)")
    print("=" * 72)
    print(f"Tenant:  {KDMC_TENANT['code']} — {KDMC_TENANT['name']}")
    print(f"Project: {KDMC_PROJECT['code']} — {KDMC_PROJECT['name']}")
    print(f"         {KDMC_PROJECT['delivery_model']} · {KDMC_PROJECT['phase']} · "
          f"₹{KDMC_PROJECT['value_inr_cr']} Cr")
    print()
    print("Will create one user per internal role on first M34 run:")
    for role in ROLES_TO_SEED:
        print(f"  - {role.lower()}@kdmc.local  ({role})")
    print()
    print("Currently a no-op — real seeding lands in Round 27 (M34) + Round 28 (M01).")


if __name__ == "__main__":
    main()
