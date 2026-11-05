"""Algoritmo A* sobre una cuadrícula, independiente de FastAPI.

Este módulo NO importa FastAPI ni Pydantic: solo usa la biblioteca estándar.
Así se puede probar, entender y reutilizar por separado.

Modelo de costos (todos los datos de la primera versión son SINTÉTICOS)
------------------------------------------------------------------------
Entrar en una celda cuesta:

    costo = factor_longitud * (1 + peso_pendiente * pendiente_deg
                                 + peso_riesgo * riesgo)

* factor_longitud vale 1.0 en movimientos ortogonales y raíz(2) en diagonales.
* pendiente_deg y riesgo son los de la celda de DESTINO del paso.
* peso_pendiente y peso_riesgo son >= 0, por lo que el multiplicador entre
  paréntesis siempre es >= 1.

Admisibilidad de la heurística
------------------------------
La heurística es la distancia octil (en factores de longitud):

    h(n) = (dx + dy) + (raíz(2) - 2) * min(dx, dy)

donde dx y dy son las diferencias de fila y columna hasta el destino.
h(n) es la longitud del camino más corto posible en una cuadrícula de
8 vecinos sin obstáculos. Como cada paso real cuesta al menos su
factor_longitud (el multiplicador es >= 1), el costo real de cualquier camino
es >= su longitud >= h(n). Por tanto h NUNCA sobreestima: es admisible.
Además es consistente (h(n) <= costo(n, m) + h(m)), así que A* no necesita
reabrir nodos y la ruta devuelta es óptima respecto a ESTE modelo de costos.

Si se desactivan las diagonales, la heurística pasa a ser la distancia
Manhattan (dx + dy), que también es admisible y consistente en ese caso.

Aviso: "óptima" significa óptima según los costos sintéticos definidos aquí.
No implica que la ruta sea físicamente segura en Marte.
"""

from __future__ import annotations

import heapq
import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

Cell = Tuple[int, int]  # (fila, columna)
SQRT2 = math.sqrt(2.0)

# Movimientos: (delta_fila, delta_columna, factor_longitud)
ORTHOGONAL_MOVES: Tuple[Tuple[int, int, float], ...] = (
    (-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),
)
DIAGONAL_MOVES: Tuple[Tuple[int, int, float], ...] = (
    (-1, -1, SQRT2), (-1, 1, SQRT2), (1, -1, SQRT2), (1, 1, SQRT2),
)


# --------------------------------------------------------------------------
# Errores
# --------------------------------------------------------------------------
class AStarError(Exception):
    """Clase base de los errores del algoritmo."""


class InvalidCellError(AStarError):
    """La coordenada no es un par de enteros dentro de la cuadrícula."""

    def __init__(self, cell: object, message: str) -> None:
        super().__init__(message)
        self.cell = cell


class BlockedCellError(AStarError):
    """El origen o el destino es una celda bloqueada."""

    def __init__(self, cell: Cell) -> None:
        super().__init__(f"La celda {cell} está bloqueada.")
        self.cell = cell


class NoRouteError(AStarError):
    """No existe ningún camino transitable entre origen y destino."""

    def __init__(self, start: Cell, goal: Cell, nodes_expanded: int) -> None:
        super().__init__(f"No existe ruta de {start} a {goal}.")
        self.start = start
        self.goal = goal
        self.nodes_expanded = nodes_expanded


# --------------------------------------------------------------------------
# Datos
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class GridCell:
    """Una celda de la cuadrícula."""

    elevation_m: float
    slope_deg: float
    risk: float          # 0.0 (sin riesgo) a 1.0 (riesgo máximo), simulado
    blocked: bool


@dataclass(frozen=True)
class CostModel:
    """Pesos del modelo de costos. Deben ser >= 0 para que A* sea correcto."""

    slope_weight: float = 0.05
    risk_weight: float = 2.0

    def __post_init__(self) -> None:
        if self.slope_weight < 0 or self.risk_weight < 0:
            raise ValueError("Los pesos del modelo de costos deben ser >= 0.")

    def cell_multiplier(self, cell: GridCell) -> float:
        """Multiplicador (>= 1) por pendiente y riesgo de la celda."""
        return 1.0 + self.slope_weight * cell.slope_deg + self.risk_weight * cell.risk


class Grid:
    """Cuadrícula rectangular de celdas indexadas por (fila, columna)."""

    def __init__(self, cells: Sequence[Sequence[GridCell]], cell_size_m: float) -> None:
        if not cells or not cells[0]:
            raise ValueError("La cuadrícula no puede estar vacía.")
        width = len(cells[0])
        if any(len(row) != width for row in cells):
            raise ValueError("Todas las filas deben tener el mismo número de columnas.")
        if cell_size_m <= 0:
            raise ValueError("cell_size_m debe ser positivo.")
        self._cells = [list(row) for row in cells]
        self.rows = len(cells)
        self.cols = width
        self.cell_size_m = float(cell_size_m)

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def cell(self, row: int, col: int) -> GridCell:
        return self._cells[row][col]


@dataclass(frozen=True)
class RouteResult:
    """Resultado de una búsqueda exitosa."""

    path: List[Cell]
    total_cost: float        # unidades de costo (adimensionales)
    distance_m: float        # metros sintéticos
    max_slope_deg: float
    mean_risk: float
    max_risk: float
    nodes_expanded: int


# --------------------------------------------------------------------------
# Funciones auxiliares
# --------------------------------------------------------------------------
def heuristic(a: Cell, b: Cell, allow_diagonal: bool = True) -> float:
    """Heurística admisible y consistente (ver docstring del módulo)."""
    d_row = abs(a[0] - b[0])
    d_col = abs(a[1] - b[1])
    if not allow_diagonal:
        return float(d_row + d_col)
    return (d_row + d_col) + (SQRT2 - 2.0) * min(d_row, d_col)


def validate_cell(grid: Grid, cell: object, name: str = "celda") -> Cell:
    """Comprueba que `cell` sea un par de enteros dentro de la cuadrícula."""
    if (
        not isinstance(cell, (tuple, list))
        or len(cell) != 2
        or any(isinstance(v, bool) or not isinstance(v, int) for v in cell)
    ):
        raise InvalidCellError(cell, f"{name}: se esperaba un par (fila, columna) de enteros.")
    row, col = cell
    if not grid.in_bounds(row, col):
        raise InvalidCellError(
            cell,
            f"{name}: ({row}, {col}) está fuera de la cuadrícula "
            f"({grid.rows} filas x {grid.cols} columnas).",
        )
    return (row, col)


def step_cost(grid: Grid, model: CostModel, target: Cell, length_factor: float) -> float:
    """Costo de entrar en la celda `target` con el factor de longitud dado."""
    return length_factor * model.cell_multiplier(grid.cell(*target))


def _neighbors(grid: Grid, current: Cell, allow_diagonal: bool):
    """Genera (vecino, factor_longitud) transitables desde `current`."""
    row, col = current
    for d_row, d_col, factor in ORTHOGONAL_MOVES:
        r, c = row + d_row, col + d_col
        if grid.in_bounds(r, c) and not grid.cell(r, c).blocked:
            yield (r, c), factor
    if not allow_diagonal:
        return
    for d_row, d_col, factor in DIAGONAL_MOVES:
        r, c = row + d_row, col + d_col
        if not grid.in_bounds(r, c) or grid.cell(r, c).blocked:
            continue
        # Sin "cortar esquinas": las dos celdas laterales deben ser transitables.
        if grid.cell(row + d_row, col).blocked or grid.cell(row, col + d_col).blocked:
            continue
        yield (r, c), factor


def _reconstruct(came_from: Dict[Cell, Cell], goal: Cell) -> List[Cell]:
    path = [goal]
    while path[-1] in came_from:
        path.append(came_from[path[-1]])
    path.reverse()
    return path


# --------------------------------------------------------------------------
# Algoritmo principal
# --------------------------------------------------------------------------
def find_path(
    grid: Grid,
    start: object,
    goal: object,
    cost_model: Optional[CostModel] = None,
    allow_diagonal: bool = True,
) -> RouteResult:
    """Calcula la ruta de menor costo entre `start` y `goal` con A*.

    Lanza:
        InvalidCellError: coordenadas mal formadas o fuera de la cuadrícula.
        BlockedCellError: origen o destino bloqueado.
        NoRouteError: el destino no es alcanzable.
    """
    model = cost_model or CostModel()
    start_cell = validate_cell(grid, start, "origen")
    goal_cell = validate_cell(grid, goal, "destino")
    if grid.cell(*start_cell).blocked:
        raise BlockedCellError(start_cell)
    if grid.cell(*goal_cell).blocked:
        raise BlockedCellError(goal_cell)

    g_cost: Dict[Cell, float] = {start_cell: 0.0}
    came_from: Dict[Cell, Cell] = {}
    length_so_far: Dict[Cell, float] = {start_cell: 0.0}
    closed: set = set()
    counter = 0  # desempate determinista en el montículo
    open_heap: List[Tuple[float, float, int, Cell]] = []
    h_start = heuristic(start_cell, goal_cell, allow_diagonal)
    heapq.heappush(open_heap, (h_start, h_start, counter, start_cell))
    expanded = 0

    while open_heap:
        _, _, _, current = heapq.heappop(open_heap)
        if current in closed:
            continue  # entrada obsoleta del montículo
        closed.add(current)
        expanded += 1

        if current == goal_cell:
            path = _reconstruct(came_from, goal_cell)
            cells = [grid.cell(*c) for c in path]
            return RouteResult(
                path=path,
                total_cost=g_cost[goal_cell],
                distance_m=length_so_far[goal_cell] * grid.cell_size_m,
                max_slope_deg=max(c.slope_deg for c in cells),
                mean_risk=sum(c.risk for c in cells) / len(cells),
                max_risk=max(c.risk for c in cells),
                nodes_expanded=expanded,
            )

        for neighbor, factor in _neighbors(grid, current, allow_diagonal):
            if neighbor in closed:
                continue
            tentative = g_cost[current] + step_cost(grid, model, neighbor, factor)
            if tentative < g_cost.get(neighbor, math.inf):
                g_cost[neighbor] = tentative
                came_from[neighbor] = current
                length_so_far[neighbor] = length_so_far[current] + factor
                h = heuristic(neighbor, goal_cell, allow_diagonal)
                counter += 1
                heapq.heappush(open_heap, (tentative + h, h, counter, neighbor))

    raise NoRouteError(start_cell, goal_cell, expanded)
