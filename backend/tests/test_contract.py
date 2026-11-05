"""Pruebas del contrato compartido con el frontend (campos que el frontend lee)."""

import json
from pathlib import Path

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
ORIGIN = "http://127.0.0.1:5500"


def test_frontend_required_map_fields(map_data):
    for key in ("name", "is_simulated", "disclaimer", "grid", "coordinate_system",
                "cost_model", "cells"):
        assert key in map_data
    assert {"rows", "cols", "cell_size_m"} <= set(map_data["grid"])


def test_frontend_required_route_fields(client):
    body = client.post("/api/v1/routes", json={
        "origin": {"row": 2, "col": 1}, "destination": {"row": 2, "col": 12}}).json()
    for key in ("path", "summary", "origin", "destination", "disclaimer", "is_simulated"):
        assert key in body
    for key in ("steps", "distance_m", "total_cost", "max_slope_deg",
                "mean_risk", "max_risk", "nodes_expanded"):
        assert isinstance(body["summary"][key], (int, float))


def test_error_format_is_uniform(client):
    bodies = [
        client.post("/api/v1/routes", json={"origin": {"row": 3, "col": 6},
                                            "destination": {"row": 1, "col": 1}}).json(),
        client.post("/api/v1/routes", json={}).json(),
        client.get("/api/v1/nada").json(),
    ]
    for body in bodies:
        assert set(body) == {"error"}
        assert set(body["error"]) == {"code", "message", "details"}
        assert isinstance(body["error"]["details"], dict)


def test_cors_allows_frontend_origin(client):
    response = client.get("/api/v1/health", headers={"Origin": ORIGIN})
    assert response.headers.get("access-control-allow-origin") == ORIGIN


def test_cors_preflight_for_post(client):
    response = client.options("/api/v1/routes", headers={
        "Origin": ORIGIN,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type",
    })
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == ORIGIN


def test_cors_rejects_unknown_origin(client):
    response = client.get("/api/v1/health", headers={"Origin": "http://evil.example"})
    assert "access-control-allow-origin" not in response.headers


def test_dataset_file_matches_api(map_data):
    data_file = Path(__file__).resolve().parents[2] / "data" / "processed" / "synthetic_grid.json"
    raw = json.loads(data_file.read_text(encoding="utf-8"))
    assert raw["cells"] == map_data["cells"]


def test_frontend_files_exist_and_config_matches_contract():
    for name in ("index.html", "css/styles.css", "js/config.js", "js/api.js",
                 "js/map.js", "js/app.js"):
        assert (FRONTEND_DIR / name).exists(), name
    config = (FRONTEND_DIR / "js" / "config.js").read_text(encoding="utf-8")
    assert "http://127.0.0.1:8000" in config
    assert "/api/v1" in config
