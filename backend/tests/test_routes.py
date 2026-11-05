"""Pruebas de POST /api/v1/routes."""

import math

URL = "/api/v1/routes"


def payload(o, d, **extra):
    body = {"origin": {"row": o[0], "col": o[1]}, "destination": {"row": d[0], "col": d[1]}}
    body.update(extra)
    return body


def recompute_cost(path, cells_by_pos, map_data):
    """Recalcula el costo desde los datos públicos del mapa (independiente de A*)."""
    model = map_data["cost_model"]
    total = 0.0
    length = 0.0
    for a, b in zip(path, path[1:]):
        diagonal = a["row"] != b["row"] and a["col"] != b["col"]
        factor = math.sqrt(2.0) if diagonal else 1.0
        cell = cells_by_pos[(b["row"], b["col"])]
        total += factor * (1 + model["slope_weight"] * cell["slope_deg"]
                           + model["risk_weight"] * cell["risk"])
        length += factor
    return total, length * map_data["grid"]["cell_size_m"]


def test_valid_route(client):
    response = client.post(URL, json=payload((2, 1), (2, 12)))
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["is_simulated"] is True
    assert body["origin"] == {"row": 2, "col": 1}
    assert body["destination"] == {"row": 2, "col": 12}
    assert body["path"][0] == body["origin"]
    assert body["path"][-1] == body["destination"]
    assert body["summary"]["steps"] == len(body["path"]) - 1


def test_response_format(client):
    body = client.post(URL, json=payload((2, 1), (2, 12))).json()
    assert set(body) == {"status", "data_source", "is_simulated", "disclaimer",
                         "origin", "destination", "allow_diagonal", "path", "summary"}
    assert set(body["summary"]) == {"steps", "distance_m", "total_cost", "max_slope_deg",
                                    "mean_risk", "max_risk", "nodes_expanded"}
    for cell in body["path"]:
        assert set(cell) == {"row", "col"}


def test_path_is_continuous_and_avoids_blocked(client, cells_by_pos):
    body = client.post(URL, json=payload((2, 1), (2, 12))).json()
    path = body["path"]
    for a, b in zip(path, path[1:]):
        assert max(abs(a["row"] - b["row"]), abs(a["col"] - b["col"])) == 1
    for cell in path:
        assert cells_by_pos[(cell["row"], cell["col"])]["blocked"] is False


def test_cost_and_distance_match_independent_calculation(client, cells_by_pos, map_data):
    body = client.post(URL, json=payload((2, 1), (2, 12))).json()
    cost, distance = recompute_cost(body["path"], cells_by_pos, map_data)
    assert math.isclose(body["summary"]["total_cost"], cost, abs_tol=1e-3)
    assert math.isclose(body["summary"]["distance_m"], distance, abs_tol=0.01)


def test_summary_risk_and_slope_match_path(client, cells_by_pos):
    body = client.post(URL, json=payload((2, 1), (2, 12))).json()
    cells = [cells_by_pos[(c["row"], c["col"])] for c in body["path"]]
    assert body["summary"]["max_slope_deg"] == max(c["slope_deg"] for c in cells)
    assert body["summary"]["max_risk"] == max(c["risk"] for c in cells)


def test_same_origin_and_destination(client):
    response = client.post(URL, json=payload((0, 0), (0, 0)))
    assert response.status_code == 200
    body = response.json()
    assert body["path"] == [{"row": 0, "col": 0}]
    assert body["summary"]["steps"] == 0
    assert body["summary"]["distance_m"] == 0
    assert body["summary"]["total_cost"] == 0


def test_without_diagonals_uses_only_orthogonal_steps(client):
    body = client.post(URL, json=payload((2, 1), (2, 12), allow_diagonal=False)).json()
    assert body["allow_diagonal"] is False
    for a, b in zip(body["path"], body["path"][1:]):
        assert abs(a["row"] - b["row"]) + abs(a["col"] - b["col"]) == 1


def test_diagonals_never_cost_more_than_orthogonal_only(client):
    with_diag = client.post(URL, json=payload((0, 0), (5, 5))).json()
    without = client.post(URL, json=payload((0, 0), (5, 5), allow_diagonal=False)).json()
    assert with_diag["summary"]["total_cost"] <= without["summary"]["total_cost"] + 1e-9


def test_out_of_bounds_origin(client):
    response = client.post(URL, json=payload((-1, 0), (2, 2)))
    assert response.status_code == 400
    error = response.json()["error"]
    assert error["code"] == "OUT_OF_BOUNDS"
    assert error["details"]["field"] == "origin"


def test_out_of_bounds_destination(client):
    response = client.post(URL, json=payload((2, 2), (10, 14)))
    assert response.status_code == 400
    error = response.json()["error"]
    assert error["code"] == "OUT_OF_BOUNDS"
    assert error["details"]["field"] == "destination"


def test_blocked_origin(client):
    response = client.post(URL, json=payload((3, 6), (2, 2)))
    assert response.status_code == 400
    error = response.json()["error"]
    assert error["code"] == "CELL_BLOCKED"
    assert error["details"] == {"field": "origin", "row": 3, "col": 6}


def test_blocked_destination(client):
    response = client.post(URL, json=payload((2, 2), (3, 6)))
    assert response.status_code == 400
    error = response.json()["error"]
    assert error["code"] == "CELL_BLOCKED"
    assert error["details"]["field"] == "destination"


def test_unreachable_destination(client, cells_by_pos):
    # La celda (8, 11) está libre pero rodeada de celdas bloqueadas.
    assert cells_by_pos[(8, 11)]["blocked"] is False
    response = client.post(URL, json=payload((2, 1), (8, 11)))
    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "NO_ROUTE"
    assert error["details"]["destination"] == {"row": 8, "col": 11}


def test_validation_error_missing_field(client):
    response = client.post(URL, json={"origin": {"row": 1, "col": 1}})
    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert error["details"]["problems"][0]["field"] == "destination"


def test_validation_error_wrong_types(client):
    body = {"origin": {"row": "1", "col": 1.5}, "destination": {"row": 2, "col": 2}}
    response = client.post(URL, json=body)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_validation_error_extra_field(client):
    response = client.post(URL, json=payload((1, 1), (2, 2), unknown=True))
    assert response.status_code == 422


def test_validation_error_invalid_json(client):
    response = client.post(URL, content="esto no es json",
                           headers={"Content-Type": "application/json"})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_route_is_deterministic(client):
    first = client.post(URL, json=payload((2, 1), (2, 12))).json()
    second = client.post(URL, json=payload((2, 1), (2, 12))).json()
    assert first == second
