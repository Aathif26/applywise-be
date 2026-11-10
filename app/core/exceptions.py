"""Global exception handlers and standardised error response schema."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import get_logger

logger = get_logger(__name__)


# ── Error response schema ────────────────────────────────────────────────────


class ErrorDetail(BaseModel):
    """Individual error detail."""

    field: str | None = None
    message: str


class ErrorResponse(BaseModel):
    """Consistent envelope returned for all error responses."""

    error: str
    status_code: int
    details: list[ErrorDetail] = []


# ── Exception handlers ───────────────────────────────────────────────────────


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    """Handle Starlette / FastAPI HTTP exceptions."""
    logger.warning("HTTP %s on %s: %s", exc.status_code, request.url.path, exc.detail)
    body = ErrorResponse(
        error=str(exc.detail),
        status_code=exc.status_code,
    )
    return JSONResponse(status_code=exc.status_code, content=body.model_dump())


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Handle Pydantic request-validation errors."""
    logger.warning("Validation error on %s: %s", request.url.path, exc.errors())
    details = [
        ErrorDetail(
            field=" -> ".join(str(loc) for loc in err.get("loc", [])),
            message=err.get("msg", "Validation error"),
        )
        for err in exc.errors()
    ]
    body = ErrorResponse(
        error="Validation Error",
        status_code=422,
        details=details,
    )
    return JSONResponse(status_code=422, content=body.model_dump())


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Catch-all for unhandled exceptions — never leak stack traces."""
    logger.exception("Unhandled exception on %s", request.url.path)
    body = ErrorResponse(
        error="Internal Server Error",
        status_code=500,
    )
    return JSONResponse(status_code=500, content=body.model_dump())


def register_exception_handlers(app: FastAPI) -> None:
    """Wire all exception handlers onto *app*."""
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

