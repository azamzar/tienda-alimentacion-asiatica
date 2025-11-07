"""
HTTP Request Logging Middleware

Logs all incoming HTTP requests with structured data:
- Request method, path, query params
- Response status code
- Request duration
- User information (if authenticated)
- Client IP address
"""

import time
import uuid
from typing import Callable
import logging

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests with structured data

    Adds request_id to each request for tracing
    Logs request details and response time
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and log details

        Args:
            request: Incoming HTTP request
            call_next: Next middleware/handler

        Returns:
            HTTP response
        """

        # Generate unique request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Get client IP
        client_ip = request.client.host if request.client else "unknown"

        # Start timer
        start_time = time.time()

        # Log request start (only in DEBUG mode to avoid clutter)
        logger.debug(
            f"Request started: {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "ip_address": client_ip,
            }
        )

        # Process request
        try:
            response = await call_next(request)
        except Exception as e:
            # Log exception
            duration_ms = (time.time() - start_time) * 1000

            logger.error(
                f"Request failed: {request.method} {request.url.path} - {str(e)}",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "ip_address": client_ip,
                    "duration_ms": round(duration_ms, 2),
                },
                exc_info=True
            )
            raise

        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000

        # Get user info if authenticated
        user_id = None
        user_email = None
        if hasattr(request.state, "user"):
            user = request.state.user
            user_id = getattr(user, "id", None)
            user_email = getattr(user, "email", None)

        # Log request completion
        log_level = logging.INFO

        # Change level based on status code
        if response.status_code >= 500:
            log_level = logging.ERROR
        elif response.status_code >= 400:
            log_level = logging.WARNING

        logger.log(
            log_level,
            f"{request.method} {request.url.path} - {response.status_code} - {duration_ms:.2f}ms",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
                "ip_address": client_ip,
                "user_id": user_id,
                "user_email": user_email,
            }
        )

        # Add request ID to response headers for tracing
        response.headers["X-Request-ID"] = request_id

        return response


def get_request_id(request: Request) -> str:
    """
    Get request ID from request state

    Args:
        request: Current request

    Returns:
        Request ID string
    """
    return getattr(request.state, "request_id", "unknown")
