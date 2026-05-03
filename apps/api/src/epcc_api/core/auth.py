"""OIDC + local-password auth.

Round 25 scaffold: types only. JWKS fetch, token validation, and the
local-password fallback land in Round 27 with M34.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class AuthenticatedUser:
    user_id: UUID
    tenant_id: UUID
    roles: frozenset[str]
    email: str
    mfa_verified: bool

    def has_role(self, role: str) -> bool:
        return role in self.roles
