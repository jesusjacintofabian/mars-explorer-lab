"""Formato único de errores de la API.

Todas las respuestas de error (400, 404, 405, 422) tienen esta forma:

    {"error": {"code": "...", "message": "...", "details": {...}}}
"""

from typing import Any, Dict, Optional

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class ApiError(Exception):
    """Error de negocio con código HTTP y código de error estable."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details or {}


def _error_response(
    status_code: int, code: str, message: str, details: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    body = {"error": {"code": code, "message": message, "details": details or {}}}
    return JSONResponse(status_code=status_code, content=body)


def register_error_handlers(app: FastAPI) -> None:
    """Registra los manejadores de errores en la aplicación."""

    @app.exception_handler(ApiError)
    async def handle_api_error(_: Request, exc: ApiError) -> JSONResponse:
        return _error_response(exc.status_code, exc.code, exc.message, exc.details)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        problems = []
        for item in exc.errors():
            location = [str(part) for part in item.get("loc", ()) if part != "body"]
            problems.append({"field": ".".join(location), "message": str(item.get("msg", ""))})
        return _error_response(
            422,
            "VALIDATION_ERROR",
            "La solicitud no tiene el formato esperado.",
            {"problems": problems},
        )

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_error(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        codes = {404: "NOT_FOUND", 405: "METHOD_NOT_ALLOWED"}
        messages = {
            404: "El recurso solicitado no existe.",
            405: "El método HTTP no está permitido para este recurso.",
        }
        code = codes.get(exc.status_code, "HTTP_ERROR")
        message = messages.get(exc.status_code, str(exc.detail))
        return _error_response(exc.status_code, code, message)
