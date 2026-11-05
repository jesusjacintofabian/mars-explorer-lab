"""Fixtures compartidas por todas las pruebas."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def map_data(client: TestClient) -> dict:
    return client.get("/api/v1/map").json()


@pytest.fixture(scope="session")
def cells_by_pos(map_data: dict) -> dict:
    return {(c["row"], c["col"]): c for c in map_data["cells"]}
