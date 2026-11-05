"""Modelos Pydantic: definen y validan el contrato JSON de la API."""

from typing import Any, Dict, List, Literal

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt


# ---------------------------------------------------------------- Comunes
class CellCoordinate(BaseModel):
    """Celda de la cuadrícula. Índices que empiezan en 0.

    `row` crece hacia abajo (fila 0 = borde superior).
    `col` crece hacia la derecha (columna 0 = borde izquierdo).
    NO son latitud ni longitud.
    """

    model_config = ConfigDict(extra="forbid")

    row: StrictInt = Field(description="Fila (0 = borde superior).", examples=[2])
    col: StrictInt = Field(description="Columna (0 = borde izquierdo).", examples=[3])


# ----------------------------------------------------------------- Health
class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    service: str
    version: str
    api_version: str
    data_source: Literal["synthetic"] = "synthetic"


# -------------------------------------------------------------------- Map
class GridInfo(BaseModel):
    rows: int = Field(description="Número de filas.")
    cols: int = Field(description="Número de columnas.")
    cell_size_m: float = Field(description="Lado de cada celda, en metros simulados.")


class CoordinateSystem(BaseModel):
    type: Literal["grid_index"] = "grid_index"
    index_base: int = 0
    row_axis: Literal["down"] = "down"
    col_axis: Literal["right"] = "right"
    description: str


class CostModelInfo(BaseModel):
    formula: str
    slope_weight: float
    risk_weight: float
    diagonal_length_factor: float
    cost_unit: Literal["cost_units"] = "cost_units"


class MapCell(BaseModel):
    row: int
    col: int
    elevation_m: float = Field(description="Elevación simulada en metros.")
    slope_deg: float = Field(description="Pendiente simulada en grados.")
    risk: float = Field(ge=0.0, le=1.0, description="Riesgo simulado de 0.0 a 1.0.")
    blocked: bool = Field(description="true = celda no transitable.")


class MapResponse(BaseModel):
    name: str
    data_source: Literal["synthetic"] = "synthetic"
    is_simulated: bool = True
    disclaimer: str
    grid: GridInfo
    coordinate_system: CoordinateSystem
    cost_model: CostModelInfo
    cells: List[MapCell]


# ----------------------------------------------------------------- Routes
class RouteRequest(BaseModel):
    """Solicitud de ruta. `allow_diagonal` es opcional (por defecto true)."""

    model_config = ConfigDict(extra="forbid")

    origin: CellCoordinate
    destination: CellCoordinate
    allow_diagonal: StrictBool = Field(
        default=True, description="Permite movimientos diagonales."
    )


class RouteSummary(BaseModel):
    steps: int = Field(description="Número de movimientos (len(path) - 1).")
    distance_m: float = Field(description="Distancia sintética en metros.")
    total_cost: float = Field(description="Costo total en cost_units (adimensional).")
    max_slope_deg: float
    mean_risk: float
    max_risk: float
    nodes_expanded: int = Field(description="Nodos expandidos por A* (informativo).")


class RouteResponse(BaseModel):
    status: Literal["ok"] = "ok"
    data_source: Literal["synthetic"] = "synthetic"
    is_simulated: bool = True
    disclaimer: str
    origin: CellCoordinate
    destination: CellCoordinate
    allow_diagonal: bool
    path: List[CellCoordinate] = Field(
        description="Celdas de la ruta en orden, incluyendo origen y destino."
    )
    summary: RouteSummary


# ----------------------------------------------------------------- Errores
class ErrorBody(BaseModel):
    code: str
    message: str
    details: Dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    error: ErrorBody
