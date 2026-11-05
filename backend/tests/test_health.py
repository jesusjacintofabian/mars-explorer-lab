"""Pruebas de GET /api/v1/health."""


def test_health_ok(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "mars-explorer-lab-api"
    assert body["api_version"] == "v1"
    assert body["data_source"] == "synthetic"


def test_health_has_exact_fields(client):
    body = client.get("/api/v1/health").json()
    assert set(body) == {"status", "service", "version", "api_version", "data_source"}


def test_unknown_path_uses_error_format(client):
    response = client.get("/api/v1/no-existe")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


def test_wrong_method_uses_error_format(client):
    response = client.post("/api/v1/health")
    assert response.status_code == 405
    assert response.json()["error"]["code"] == "METHOD_NOT_ALLOWED"
