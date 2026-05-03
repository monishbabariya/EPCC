"""Pytest fixtures shared by unit + integration tests.

Round 25 scaffold: only `client` for the empty FastAPI app. Per-module
fixtures (seeded users, tenants, projects) land in Round 27+.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from epcc_api.main import app


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client
