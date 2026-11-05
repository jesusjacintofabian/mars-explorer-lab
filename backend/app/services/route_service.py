"""Servicio de rutas: conecta la API con el algoritmo A*."""

from typing import Any, Dict

from algorithms.astar import (
    BlockedCellError,
    InvalidCellError,
    NoRouteError,
    find_path,
)

from app.errors import ApiError
from app.models.schemas import RouteRequest
from app.services.map_service import COST_MODEL, DISCLAIMER, get_grid


def compute_route(request: RouteRequest) -> Dict[str, Any]:
    """Valida la solicitud, ejecuta A* y devuelve un dict compatible con RouteResponse."""
    grid = get_grid()
    origin = (request.origin.row, request.origin.col)
    destination = (request.destination.row, request.destination.col)

    try:
        result = find_path(
            grid,
            origin,
            destination,
            cost_model=COST_MODEL,
            allow_diagonal=request.allow_diagonal,
        )
    except InvalidCellError as exc:
        which = "origin" if exc.cell == origin else "destination"
        raise ApiError(
            400,
            "OUT_OF_BOUNDS",
            f"La celda de {'origen' if which == 'origin' else 'destino'} está fuera "
            f"de la cuadrícula ({grid.rows} filas x {grid.cols} columnas).",
            {"field": which, "row": exc.cell[0], "col": exc.cell[1],
             "rows": grid.rows, "cols": grid.cols},
        ) from exc
    except BlockedCellError as exc:
        which = "origin" if exc.cell == origin else "destination"
        raise ApiError(
            400,
            "CELL_BLOCKED",
            f"La celda de {'origen' if which == 'origin' else 'destino'} "
            f"({exc.cell[0]}, {exc.cell[1]}) está bloqueada.",
            {"field": which, "row": exc.cell[0], "col": exc.cell[1]},
        ) from exc
    except NoRouteError as exc:
        raise ApiError(
            404,
            "NO_ROUTE",
            "No existe una ruta transitable entre el origen y el destino.",
            {"origin": {"row": origin[0], "col": origin[1]},
             "destination": {"row": destination[0], "col": destination[1]},
             "nodes_expanded": exc.nodes_expanded},
        ) from exc

    return {
        "status": "ok",
        "data_source": "synthetic",
        "is_simulated": True,
        "disclaimer": DISCLAIMER,
        "origin": {"row": origin[0], "col": origin[1]},
        "destination": {"row": destination[0], "col": destination[1]},
        "allow_diagonal": request.allow_diagonal,
        "path": [{"row": r, "col": c} for r, c in result.path],
        "summary": {
            "steps": len(result.path) - 1,
            "distance_m": round(result.distance_m, 2),
            "total_cost": round(result.total_cost, 4),
            "max_slope_deg": result.max_slope_deg,
            "mean_risk": round(result.mean_risk, 4),
            "max_risk": result.max_risk,
            "nodes_expanded": result.nodes_expanded,
        },
    }
