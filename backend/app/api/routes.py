"""Endpoints REST de la versión 1 de la API."""

from fastapi import APIRouter

from app.models.schemas import (
    ErrorResponse,
    HealthResponse,
    MapResponse,
    RouteRequest,
    RouteResponse,
)
from app.services import map_service, route_service

router = APIRouter()

API_VERSION = "v1"
APP_VERSION = "1.0.0"


@router.get("/health", response_model=HealthResponse, summary="Estado del servicio")
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="mars-explorer-lab-api",
        version=APP_VERSION,
        api_version=API_VERSION,
        data_source="synthetic",
    )


@router.get("/map", response_model=MapResponse, summary="Datos de la zona de estudio")
def get_map() -> MapResponse:
    return MapResponse(**map_service.build_map_payload())


@router.post(
    "/routes",
    response_model=RouteResponse,
    summary="Calcula una ruta con A*",
    responses={
        400: {"model": ErrorResponse, "description": "Celda fuera de la cuadrícula o bloqueada."},
        404: {"model": ErrorResponse, "description": "No existe ruta."},
        422: {"model": ErrorResponse, "description": "Solicitud con formato inválido."},
    },
)
def post_route(request: RouteRequest) -> RouteResponse:
    return RouteResponse(**route_service.compute_route(request))
