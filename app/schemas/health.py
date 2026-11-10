"""Health-check response schemas."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response for the basic health endpoint."""

    status: str
    app_name: str
    version: str


class HealthDBResponse(HealthResponse):
    """Response for the database health endpoint."""

    database: str

