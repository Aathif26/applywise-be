"""Health-check endpoints."""

from fastapi import APIRouter, status
from sqlalchemy import text

from app.core.config import get_settings
from app.db.session import async_session_factory
from app.schemas.health import HealthDBResponse, HealthResponse

router = APIRouter(tags=["Health"])

settings = get_settings()


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Basic liveness check",
)
async def health() -> HealthResponse:
    """Return application status without touching external services."""
    return HealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
    )


@router.get(
    "/health/db",
    response_model=HealthDBResponse,
    status_code=status.HTTP_200_OK,
    summary="Database readiness check",
)
async def health_db() -> HealthDBResponse:
    """Verify the application can reach PostgreSQL."""
    try:
        async with async_session_factory() as session:
            await session.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "unavailable"

    return HealthDBResponse(
        status="healthy" if db_status == "connected" else "degraded",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        database=db_status,
    )

