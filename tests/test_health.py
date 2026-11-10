"""Smoke tests for health endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    """GET /api/v1/health returns 200 with app info."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "app_name" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_health_db(client: AsyncClient) -> None:
    """GET /api/v1/health/db returns 200 and reports database status."""
    response = await client.get("/api/v1/health/db")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] in ("healthy", "degraded")
    assert "database" in data
    assert data["database"] in ("connected", "unavailable")

