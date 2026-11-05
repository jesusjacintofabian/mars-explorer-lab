"""Pruebas de GET /api/v1/map."""


def test_map_status_and_flags(client):
    response = client.get("/api/v1/map")
    assert response.status_code == 200
    body = response.json()
    assert body["data_source"] == "synthetic"
    assert body["is_simulated"] is True
    assert "SIMULADOS" in body["disclaimer"]


def test_map_grid_dimensions(map_data):
    assert map_data["grid"] == {"rows": 10, "cols": 14, "cell_size_m": 100.0}


def test_map_has_one_cell_per_position(map_data):
    positions = {(c["row"], c["col"]) for c in map_data["cells"]}
    expected = {(r, c) for r in range(10) for c in range(14)}
    assert len(map_data["cells"]) == 140
    assert positions == expected


def test_map_cell_format(map_data):
    expected_keys = {"row", "col", "elevation_m", "slope_deg", "risk", "blocked"}
    for cell in map_data["cells"]:
        assert set(cell) == expected_keys
        assert isinstance(cell["row"], int) and isinstance(cell["col"], int)
        assert isinstance(cell["blocked"], bool)
        assert 0.0 <= cell["risk"] <= 1.0
        assert cell["slope_deg"] >= 0.0


def test_map_has_blocked_and_free_cells(map_data):
    blocked = [c for c in map_data["cells"] if c["blocked"]]
    assert 0 < len(blocked) < len(map_data["cells"])


def test_map_coordinate_system(map_data):
    system = map_data["coordinate_system"]
    assert system["type"] == "grid_index"
    assert system["index_base"] == 0
    assert system["row_axis"] == "down"
    assert system["col_axis"] == "right"


def test_map_cost_model(map_data):
    model = map_data["cost_model"]
    assert model["slope_weight"] == 0.05
    assert model["risk_weight"] == 2.0
    assert model["cost_unit"] == "cost_units"
