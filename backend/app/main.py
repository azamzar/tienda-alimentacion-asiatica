from pathlib import Path
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config.settings import settings
from app.config.database import engine
from app.models.base import Base
from app.api.v1.router import api_router
from app.api.health import router as health_router
from app.core.logging_config import setup_logging
from app.middleware import RequestLoggingMiddleware

# Setup structured logging
setup_logging()
logger = logging.getLogger(__name__)

# Create database tables (for development - use Alembic in production)
Base.metadata.create_all(bind=engine)

# Create upload directories if they don't exist
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.PRODUCTS_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Log application startup
logger.info(
    f"Starting {settings.APP_NAME} v{settings.APP_VERSION}",
    extra={"debug_mode": settings.DEBUG}
)

# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para tienda de alimentación asiática",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add request logging middleware (before CORS)
app.add_middleware(RequestLoggingMiddleware)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include health check router (no prefix - at root level)
app.include_router(health_router, tags=["Health"])

# Include API v1 router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory=str(settings.UPLOAD_DIR)), name="uploads")


@app.get("/")
def read_root():
    """Root endpoint - API information"""
    return {
        "message": f"Bienvenido a {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
        "health_detailed": "/health/detailed"
    }
