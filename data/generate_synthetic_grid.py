"""Generador del conjunto de datos SINTÉTICO de Mars Explorer Lab.

Todos los valores de este archivo se calculan con fórmulas matemáticas
deterministas. NO provienen de NASA, de HiRISE, de MOLA ni de ninguna misión
real. Sirven únicamente para aprender y probar el mapa y el algoritmo A*.

Uso (desde la raíz del repositorio):
    python3 data/generate_synthetic_grid.py

Resultado:
    data/processed/synthetic_grid.json
"""

import json
import math
from pathlib import Path

ROWS = 10
COLS = 14
CELL_SIZE_M = 100.0          # Cada celda representa 100 m x 100 m (simulado).
BLOCKED_SLOPE_DEG = 20.0     # Pendiente a partir de la cual la celda se bloquea.

# Celdas bloqueadas adicionales (rocas, paredes de cráter, etc. simulados).
# Formato: (fila, columna). Las filas crecen hacia abajo.
EXTRA_BLOCKED = {
    # Muro rocoso vertical con un único paso en las filas 8 y 9.
    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
    # Anillo cerrado alrededor de la celda (8, 11): meseta inalcanzable.
    (7, 10), (7, 11), (7, 12),
    (8, 10), (8, 12),
    (9, 10), (9, 11), (9, 12),
}

# Zonas de riesgo simuladas: (fila_centro, col_centro, intensidad, dispersión)
RISK_ZONES = [
    (3.0, 9.0, 0.95, 3.0),
    (7.0, 3.0, 0.70, 2.5),
    (1.0, 2.0, 0.40, 2.0),
]


def elevation(row: int, col: int) -> float:
    """Elevación simulada en metros (relieve suave + colinas + un cráter)."""
    base = 1000.0 + 6.0 * col + 4.0 * row
    hills = 55.0 * math.sin(col / 2.2) * math.cos(row / 2.8)
    crater = -70.0 * math.exp(-(((row - 6.0) ** 2) + ((col - 9.5) ** 2)) / 5.0)
    return base + hills + crater


def slope_deg(elev: list, row: int, col: int) -> float:
    """Pendiente en grados usando diferencias centrales sobre la elevación."""
    r0, r1 = max(row - 1, 0), min(row + 1, ROWS - 1)
    c0, c1 = max(col - 1, 0), min(col + 1, COLS - 1)
    d_row = (elev[r1][col] - elev[r0][col]) / ((r1 - r0) * CELL_SIZE_M)
    d_col = (elev[row][c1] - elev[row][c0]) / ((c1 - c0) * CELL_SIZE_M)
    return math.degrees(math.atan(math.hypot(d_row, d_col)))


def risk(row: int, col: int) -> float:
    """Riesgo simulado entre 0.0 y 1.0 (suma de zonas gaussianas)."""
    total = 0.0
    for r0, c0, strength, spread in RISK_ZONES:
        dist2 = (row - r0) ** 2 + (col - c0) ** 2
        total += strength * math.exp(-dist2 / (2.0 * spread))
    return min(total, 1.0)


def build() -> dict:
    elev = [[elevation(r, c) for c in range(COLS)] for r in range(ROWS)]
    cells = []
    for r in range(ROWS):
        for c in range(COLS):
            slope = slope_deg(elev, r, c)
            blocked = (r, c) in EXTRA_BLOCKED or slope >= BLOCKED_SLOPE_DEG
            cells.append({
                "row": r,
                "col": c,
                "elevation_m": round(elev[r][c], 1),
                "slope_deg": round(slope, 1),
                "risk": round(risk(r, c), 2),
                "blocked": blocked,
            })
    return {
        "name": "Zona sintética Mars Explorer Lab",
        "data_source": "synthetic",
        "is_simulated": True,
        "generator": "data/generate_synthetic_grid.py",
        "rows": ROWS,
        "cols": COLS,
        "cell_size_m": CELL_SIZE_M,
        "blocked_slope_deg": BLOCKED_SLOPE_DEG,
        "cells": cells,
    }


def write(path: Path) -> None:
    """Escribe el JSON con una celda por línea (fácil de leer y comparar)."""
    data = build()
    header = {k: v for k, v in data.items() if k != "cells"}
    lines = ["{"]
    for key, value in header.items():
        lines.append(f'  {json.dumps(key)}: {json.dumps(value, ensure_ascii=False)},')
    lines.append('  "cells": [')
    rendered = [
        "    " + json.dumps(cell, ensure_ascii=False) for cell in data["cells"]
    ]
    lines.append(",\n".join(rendered))
    lines.append("  ]")
    lines.append("}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    output = Path(__file__).resolve().parent / "processed" / "synthetic_grid.json"
    write(output)
    print(f"Archivo generado: {output}")
