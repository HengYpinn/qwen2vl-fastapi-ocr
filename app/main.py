"""Main FastAPI application."""

import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.api.endpoints import documents, health

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting Document OCR API")
    yield
    # Shutdown
    logger.info("Shutting down Document OCR API")


# Create FastAPI application
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    debug=settings.debug,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        f"Request: {request.method} {request.url} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.4f}s"
    )
    return response


# Include routers
app.include_router(documents.router)
app.include_router(health.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Document OCR API",
        "version": settings.api_version,
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
