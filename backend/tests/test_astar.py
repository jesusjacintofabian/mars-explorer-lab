"""Pruebas del algoritmo A* (sin FastAPI)."""

import heapq
import math
import random

import pytest

from algorithms.astar import (
    SQRT2,
    BlockedCellError,
    CostModel,
    Grid,
    GridCell,
    InvalidCellError,
    NoRouteError,
    find_path,
    heuristic,
)


def make_grid(rows, cols, blocked=(), slope=0.0, risk=0.0, cell_size_m=100.0):
    blocked = set(blocked)
    cells = [
        [GridCell(1000.0, slope, risk, (r, c) in blocked) for c in range(cols)]
        for r in range(rows)
    ]
    return Grid(cells, cell_size_m)


# ------------------------------------------------------------ rutas posibles
def test_straight_line_cost_without_slope_or_risk():
    grid = make_grid(1, 5)
    result = find_path(grid, (0, 0), (0, 4))
    assert result.path == [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
    assert result.total_cost == pytest.approx(4.0)
    assert result.distance_m == pytest.approx(400.0)


def test_diagonal_move_costs_sqrt2():
    grid = make_grid(3, 3)
    result = find_path(grid, (0, 0), (2, 2))
    assert result.path == [(0, 0), (1, 1), (2, 2)]
    assert result.total_cost == pytest.approx(2 * SQRT2)


def test_slope_and_risk_increase_cost():
    grid = make_grid(1, 3, slope=10.0, risk=0.5)
    model = CostModel(slope_weight=0.1, risk_weight=2.0)
    result = find_path(grid, (0, 0), (0, 2), model)
    per_step = 1 + 0.1 * 10.0 + 2.0 * 0.5
    assert result.total_cost == pytest.approx(2 * per_step)


def test_prefers_detour_around_wall():
    grid = make_grid(3, 5, blocked={(1, 2), (0, 2)})
    result = find_path(grid, (0, 0), (0, 4))
    assert all(not grid.cell(*c).blocked for c in result.path)
    assert (2, 2) in result.path


def test_avoids_high_risk_when_cheaper():
    cells = [[GridCell(0, 0, 0.0, False) for _ in range(5)] for _ in range(3)]
    for c in range(1, 4):
        cells[1][c] = GridCell(0, 0, 1.0, False)   # franja de riesgo en la fila central
    grid = Grid(cells, 100.0)
    result = find_path(grid, (1, 0), (1, 4), CostModel(0.0, 5.0))
    assert all(grid.cell(*c).risk == 0.0 for c in result.path[1:-1])


def test_same_start_and_goal():
    grid = make_grid(2, 2)
    result = find_path(grid, (1, 1), (1, 1))
    assert result.path == [(1, 1)]
    assert result.total_cost == 0.0
    assert result.distance_m == 0.0


def test_no_corner_cutting():
    # Los dos bloqueos impiden el paso diagonal (0,0)->(1,1).
    grid = make_grid(2, 2, blocked={(0, 1), (1, 0)})
    with pytest.raises(NoRouteError):
        find_path(grid, (0, 0), (1, 1))


def test_orthogonal_only_mode():
    grid = make_grid(3, 3)
    result = find_path(grid, (0, 0), (2, 2), allow_diagonal=False)
    assert result.total_cost == pytest.approx(4.0)
    assert len(result.path) == 5


# ----------------------------------------------------------- rutas imposibles
def test_unreachable_goal_raises():
    grid = make_grid(3, 3, blocked={(0, 1), (1, 0), (1, 1)})
    with pytest.raises(NoRouteError) as info:
        find_path(grid, (0, 0), (2, 2))
    assert info.value.nodes_expanded >= 1


def test_blocked_start_and_goal():
    grid = make_grid(2, 2, blocked={(0, 0), (1, 1)})
    with pytest.raises(BlockedCellError) as info:
        find_path(grid, (0, 0), (0, 1))
    assert info.value.cell == (0, 0)
    with pytest.raises(BlockedCellError) as info:
        find_path(grid, (0, 1), (1, 1))
    assert info.value.cell == (1, 1)


# ---------------------------------------------------------------- validación
@pytest.mark.parametrize("bad", [(-1, 0), (0, -1), (2, 0), (0, 2), (99, 99)])
def test_out_of_bounds_cells(bad):
    grid = make_grid(2, 2)
    with pytest.raises(InvalidCellError):
        find_path(grid, bad, (0, 0))
    with pytest.raises(InvalidCellError):
        find_path(grid, (0, 0), bad)


@pytest.mark.parametrize("bad", [None, (1,), (1, 2, 3), (1.0, 0), ("a", 0), (True, 0), "ab"])
def test_malformed_cells(bad):
    grid = make_grid(2, 2)
    with pytest.raises(InvalidCellError):
        find_path(grid, bad, (0, 0))


def test_negative_weights_rejected():
    with pytest.raises(ValueError):
        CostModel(slope_weight=-0.1)
    with pytest.raises(ValueError):
        CostModel(risk_weight=-1.0)


def test_invalid_grid_construction():
    with pytest.raises(ValueError):
        Grid([], 100.0)
    with pytest.raises(ValueError):
        Grid([[GridCell(0, 0, 0, False)], []], 100.0)
    with pytest.raises(ValueError):
        Grid([[GridCell(0, 0, 0, False)]], 0)


# ----------------------------------------------------------------- heurística
def test_heuristic_values():
    assert heuristic((0, 0), (0, 0)) == 0
    assert heuristic((0, 0), (0, 3)) == pytest.approx(3.0)
    assert heuristic((0, 0), (3, 3)) == pytest.approx(3 * SQRT2)
    assert heuristic((0, 0), (2, 5)) == pytest.approx(3 + 2 * SQRT2)
    assert heuristic((0, 0), (2, 5), allow_diagonal=False) == 7.0


# --------------------------------------- admisibilidad y optimalidad (Dijkstra)
def dijkstra_cost(grid, start, goal, model, allow_diagonal):
    """Referencia independiente: Dijkstra completo (equivale a A* con h = 0)."""
    moves = [(-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0)]
    if allow_diagonal:
        moves += [(-1, -1, SQRT2), (-1, 1, SQRT2), (1, -1, SQRT2), (1, 1, SQRT2)]
    dist = {start: 0.0}
    heap = [(0.0, start)]
    while heap:
        d, cur = heapq.heappop(heap)
        if cur == goal:
            return d
        if d > dist.get(cur, math.inf):
            continue
        for dr, dc, f in moves:
            r, c = cur[0] + dr, cur[1] + dc
            if not grid.in_bounds(r, c) or grid.cell(r, c).blocked:
                continue
            if dr and dc and (grid.cell(cur[0] + dr, cur[1]).blocked
                              or grid.cell(cur[0], cur[1] + dc).blocked):
                continue
            nd = d + f * model.cell_multiplier(grid.cell(r, c))
            if nd < dist.get((r, c), math.inf):
                dist[(r, c)] = nd
                heapq.heappush(heap, (nd, (r, c)))
    return None


@pytest.mark.parametrize("seed", range(25))
@pytest.mark.parametrize("allow_diagonal", [True, False])
def test_astar_matches_dijkstra_on_random_grids(seed, allow_diagonal):
    rng = random.Random(seed)
    rows, cols = 8, 9
    cells = [[GridCell(0.0, rng.uniform(0, 20), rng.random(), rng.random() < 0.22)
              for _ in range(cols)] for _ in range(rows)]
    cells[0][0] = GridCell(0.0, 3.0, 0.1, False)
    cells[rows - 1][cols - 1] = GridCell(0.0, 3.0, 0.1, False)
    grid = Grid(cells, 100.0)
    model = CostModel(0.05, 2.0)
    expected = dijkstra_cost(grid, (0, 0), (rows - 1, cols - 1), model, allow_diagonal)
    if expected is None:
        with pytest.raises(NoRouteError):
            find_path(grid, (0, 0), (rows - 1, cols - 1), model, allow_diagonal)
    else:
        result = find_path(grid, (0, 0), (rows - 1, cols - 1), model, allow_diagonal)
        assert result.total_cost == pytest.approx(expected)


@pytest.mark.parametrize("allow_diagonal", [True, False])
def test_heuristic_never_exceeds_true_cost(allow_diagonal):
    grid = make_grid(6, 6, slope=5.0, risk=0.2)
    model = CostModel(0.05, 2.0)
    goal = (5, 5)
    for r in range(6):
        for c in range(6):
            true_cost = find_path(grid, (r, c), goal, model, allow_diagonal).total_cost
            assert heuristic((r, c), goal, allow_diagonal) <= true_cost + 1e-9
