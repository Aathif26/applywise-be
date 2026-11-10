"""Aggregated API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import health

router = APIRouter()

# Mount endpoint routers here — add new ones as the app grows.
router.include_router(health.router)

