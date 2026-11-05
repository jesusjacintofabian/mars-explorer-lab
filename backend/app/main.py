"""Punto de entrada de la API de Mars Explorer Lab.

Ejecutar desde el directorio backend/:
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.errors import register_error_handlers

DEFAULT_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]


def get_allowed_origins() -> list:
    """Orígenes del frontend permitidos por CORS.

    Se pueden cambiar con la variable de entorno MARS_ALLOWED_ORIGINS
    (valores separados por comas).
    """
    raw = os.getenv("MARS_ALLOWED_ORIGINS", "")
    custom = [item.strip() for item in raw.split(",") if item.strip()]
    return custom or DEFAULT_ORIGINS


app = FastAPI(
    title="Mars Explorer Lab API",
    description=(
        "API educativa con datos SINTÉTICOS para calcular rutas con A*. "
        "No es la solución oficial del desafío NASA Space Apps."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

register_error_handlers(app)
app.include_router(router, prefix="/api/v1")
