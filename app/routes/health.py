from datetime import datetime, timezone

from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/health", response_model=HealthResponse, tags=["Monitoring"])
async def health_check():
    """Return service health status."""
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@router.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "WhatsApp AI Bot is running",
        "docs": "/docs",
        "health": "/health",
        "environment": settings.environment,
    }
