"""Per-spec module packages.

Each subpackage mirrors a `SystemAdmin/Modules/M0X_*_Spec_*.md` (or, for M34,
`SystemAdmin/M34_*_Spec_*.md`). Internal layout (locked in
`EPCC_BuildArchitecture_Spec_v1_0.md` §3.3):

    m0X_<name>/
        models.py        Block 3 entities
        schemas.py       Block 3 + Block 5 request/response shapes
        routes.py        Block 7 integration points (FastAPI router)
        service.py       Block 6 business rules
        permissions.py   M34 + module-specific RBAC checks
        tests/           BR-tagged tests
"""
