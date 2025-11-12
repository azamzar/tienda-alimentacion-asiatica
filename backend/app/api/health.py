"""
Health Check Endpoints

Provides comprehensive health checks for monitoring and orchestration.
"""
import logging
from typing import Dict, Any
from datetime import datetime
import psutil
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.api.deps import get_db
from app.config.settings import settings
from app.utils.cache import redis_client

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Basic health check endpoint.
    Returns 200 OK if the service is running.

    This is used by Docker healthcheck and load balancers.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@router.get("/health/detailed", status_code=status.HTTP_200_OK)
async def detailed_health_check(db: Session = Depends(get_db)):
    """
    Detailed health check endpoint.

    Checks the health of all critical services:
    - Application status
    - Database connectivity
    - Redis cache connectivity
    - System resources (CPU, Memory, Disk)

    Returns 200 OK if all services are healthy.
    Returns 503 Service Unavailable if any critical service is down.
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "checks": {}
    }

    # Check Database
    try:
        db.execute(text("SELECT 1"))
        health_status["checks"]["database"] = {
            "status": "healthy",
            "message": "Database connection successful"
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}"
        }

    # Check Redis Cache
    try:
        if settings.CACHE_ENABLED and redis_client:
            redis_client.ping()
            health_status["checks"]["redis"] = {
                "status": "healthy",
                "message": "Redis connection successful"
            }
        else:
            health_status["checks"]["redis"] = {
                "status": "disabled",
                "message": "Redis cache is disabled"
            }
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        health_status["status"] = "unhealthy"
        health_status["checks"]["redis"] = {
            "status": "unhealthy",
            "message": f"Redis connection failed: {str(e)}"
        }

    # Check System Resources
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        health_status["checks"]["system"] = {
            "status": "healthy",
            "cpu_percent": round(cpu_percent, 2),
            "memory_percent": round(memory.percent, 2),
            "memory_available_mb": round(memory.available / (1024 * 1024), 2),
            "disk_percent": round(disk.percent, 2),
            "disk_free_gb": round(disk.free / (1024 * 1024 * 1024), 2)
        }

        # Set warnings if resources are high
        if cpu_percent > 80 or memory.percent > 80 or disk.percent > 80:
            health_status["checks"]["system"]["warning"] = "High resource usage detected"

    except Exception as e:
        logger.error(f"System health check failed: {e}")
        health_status["checks"]["system"] = {
            "status": "error",
            "message": f"Could not retrieve system metrics: {str(e)}"
        }

    # Set HTTP status code based on overall health
    if health_status["status"] == "unhealthy":
        return health_status, status.HTTP_503_SERVICE_UNAVAILABLE

    return health_status


@router.get("/health/readiness", status_code=status.HTTP_200_OK)
async def readiness_check(db: Session = Depends(get_db)):
    """
    Readiness check endpoint.

    Indicates whether the service is ready to accept traffic.
    Used by Kubernetes readiness probes.

    Returns 200 OK if the service is ready.
    Returns 503 Service Unavailable if not ready.
    """
    try:
        # Check database connection
        db.execute(text("SELECT 1"))

        # Check Redis if enabled
        if settings.CACHE_ENABLED and redis_client:
            redis_client.ping()

        return {
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return {
            "status": "not_ready",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }, status.HTTP_503_SERVICE_UNAVAILABLE


@router.get("/health/liveness", status_code=status.HTTP_200_OK)
async def liveness_check():
    """
    Liveness check endpoint.

    Indicates whether the service is alive and should not be restarted.
    Used by Kubernetes liveness probes.

    Returns 200 OK if the service is alive.
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }
