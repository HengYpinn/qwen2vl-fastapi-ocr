"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Document OCR API"}


@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint."""
    # Add any necessary readiness checks here
    # e.g., database connectivity, external service availability
    return {"status": "ready", "service": "Document OCR API"}
