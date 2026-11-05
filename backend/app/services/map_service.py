"""Carga del conjunto de datos sintético y construcción de la respuesta /map."""

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

from algorithms.astar import CostModel, Grid, GridCell

DATA_FILE = Path(__file__).resolve().parents[3] / "data" / "processed" / "synthetic_grid.json"

DISCLAIMER = (
    "DATOS SIMULADOS: elevación, pendiente y riesgo son sintéticos y no provienen "
    "de NASA ni de ninguna misión real. Este laboratorio es educativo y no "
    "garantiza que una ruta sea segura en Marte."
)

COST_MODEL = CostModel(slope_weight=0.05, risk_weight=2.0)
COST_FORMULA = (
    "costo_paso = factor_longitud * (1 + slope_weight * slope_deg + risk_weight * risk); "
    "se usan los valores de la celda de destino del paso"
)


@lru_cache(maxsize=1)
def load_dataset() -> Dict[str, Any]:
    """Lee y valida data/processed/synthetic_grid.json (se carga una sola vez)."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"No se encontró {DATA_FILE}. Ejecuta: python3 data/generate_synthetic_grid.py"
        )
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    rows, cols = data["rows"], data["cols"]
    positions = {(c["row"], c["col"]) for c in data["cells"]}
    expected = {(r, c) for r in range(rows) for c in range(cols)}
    if len(data["cells"]) != rows * cols or positions != expected:
        raise ValueError("El conjunto de datos no cubre exactamente la cuadrícula declarada.")
    return data


@lru_cache(maxsize=1)
def get_grid() -> Grid:
    """Construye el objeto Grid que usa el algoritmo A*."""
    data = load_dataset()
    matrix = [[None] * data["cols"] for _ in range(data["rows"])]
    for c in data["cells"]:
        matrix[c["row"]][c["col"]] = GridCell(
            elevation_m=c["elevation_m"],
            slope_deg=c["slope_deg"],
            risk=c["risk"],
            blocked=c["blocked"],
        )
    return Grid(matrix, data["cell_size_m"])


def build_map_payload() -> Dict[str, Any]:
    """Diccionario compatible con el modelo MapResponse."""
    data = load_dataset()
    return {
        "name": data["name"],
        "data_source": "synthetic",
        "is_simulated": True,
        "disclaimer": DISCLAIMER,
        "grid": {
            "rows": data["rows"],
            "cols": data["cols"],
            "cell_size_m": data["cell_size_m"],
        },
        "coordinate_system": {
            "type": "grid_index",
            "index_base": 0,
            "row_axis": "down",
            "col_axis": "right",
            "description": (
                "Índices de cuadrícula (row, col) desde la esquina superior izquierda. "
                "No son latitud ni longitud."
            ),
        },
        "cost_model": {
            "formula": COST_FORMULA,
            "slope_weight": COST_MODEL.slope_weight,
            "risk_weight": COST_MODEL.risk_weight,
            "diagonal_length_factor": 1.4142,
            "cost_unit": "cost_units",
        },
        "cells": data["cells"],
    }
