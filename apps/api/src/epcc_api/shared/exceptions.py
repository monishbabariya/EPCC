"""Cross-module exception hierarchy.

Mapped to RFC 9457 problem-details responses by `main.py` exception handlers
once those land in Round 27.
"""

from __future__ import annotations


class EpccError(Exception):
    """Base for all EPCC domain errors."""

    status_code: int = 500
    code: str = "epcc.internal_error"


class NotFoundError(EpccError):
    status_code = 404
    code = "epcc.not_found"


class PermissionDeniedError(EpccError):
    status_code = 403
    code = "epcc.permission_denied"


class ValidationError(EpccError):
    status_code = 422
    code = "epcc.validation_failed"


class BusinessRuleViolation(EpccError):
    status_code = 409
    code = "epcc.business_rule_violation"

    def __init__(self, br_code: str, message: str) -> None:
        super().__init__(f"{br_code}: {message}")
        self.br_code = br_code
