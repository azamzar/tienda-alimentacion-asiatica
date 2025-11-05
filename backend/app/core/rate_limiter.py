from typing import Callable
from fastapi import Request, HTTPException, status
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio

from app.config.settings import settings


class RateLimiter:
    """
    Rate limiter basado en memoria para control de solicitudes por IP

    En producción, considere usar Redis para rate limiting distribuido
    """

    def __init__(self):
        # Estructura: {ip_address: {endpoint: [(timestamp, count)]}}
        self.requests = defaultdict(lambda: defaultdict(list))
        self.cleanup_task = None

    def _cleanup_old_requests(self):
        """Limpia requests antiguos cada 60 segundos"""
        now = datetime.utcnow()
        cutoff = now - timedelta(hours=1)

        # Limpiar requests más antiguos de 1 hora
        for ip_requests in self.requests.values():
            for endpoint_requests in ip_requests.values():
                endpoint_requests[:] = [
                    (ts, count) for ts, count in endpoint_requests
                    if ts > cutoff
                ]

    async def start_cleanup_task(self):
        """Inicia tarea de limpieza periódica"""
        while True:
            await asyncio.sleep(60)  # Cada minuto
            self._cleanup_old_requests()

    def is_rate_limited(
        self,
        ip: str,
        endpoint: str,
        max_requests: int,
        window_seconds: int
    ) -> bool:
        """
        Verifica si una IP ha excedido el límite de requests

        Args:
            ip: Dirección IP del cliente
            endpoint: Nombre del endpoint
            max_requests: Máximo de requests permitidos
            window_seconds: Ventana de tiempo en segundos

        Returns:
            True si está limitado, False si puede proceder
        """
        if not settings.RATE_LIMIT_ENABLED:
            return False

        now = datetime.utcnow()
        cutoff = now - timedelta(seconds=window_seconds)

        # Obtener requests del endpoint para esta IP
        endpoint_requests = self.requests[ip][endpoint]

        # Filtrar solo requests dentro de la ventana de tiempo
        recent_requests = [ts for ts, _ in endpoint_requests if ts > cutoff]

        # Limpiar requests antiguos
        self.requests[ip][endpoint] = [(ts, 1) for ts in recent_requests]

        # Verificar si excede el límite
        if len(recent_requests) >= max_requests:
            return True

        # Agregar este request
        self.requests[ip][endpoint].append((now, 1))
        return False

    def get_client_ip(self, request: Request) -> str:
        """
        Obtiene la IP del cliente, considerando proxies

        Args:
            request: FastAPI Request object

        Returns:
            IP del cliente
        """
        # Verificar headers de proxy
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fallback a IP directa
        return request.client.host if request.client else "unknown"


# Instancia global del rate limiter
rate_limiter = RateLimiter()


def rate_limit(max_requests: int, window_seconds: int = 60):
    """
    Decorator para aplicar rate limiting a endpoints

    Args:
        max_requests: Máximo de requests permitidos
        window_seconds: Ventana de tiempo en segundos (default: 60)

    Example:
        @router.post("/login")
        @rate_limit(max_requests=5, window_seconds=60)
        async def login(request: Request, ...):
            ...
    """
    def decorator(func: Callable):
        async def wrapper(*args, **kwargs):
            # Buscar el objeto Request en los argumentos
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break

            if not request:
                # Buscar en kwargs
                request = kwargs.get("request")

            if not request:
                # Si no hay request, proceder sin rate limiting
                return await func(*args, **kwargs)

            # Obtener IP del cliente
            client_ip = rate_limiter.get_client_ip(request)
            endpoint = f"{request.method}:{request.url.path}"

            # Verificar rate limit
            if rate_limiter.is_rate_limited(
                client_ip, endpoint, max_requests, window_seconds
            ):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Demasiadas solicitudes. Límite: {max_requests} por {window_seconds} segundos.",
                    headers={
                        "Retry-After": str(window_seconds),
                        "X-RateLimit-Limit": str(max_requests),
                        "X-RateLimit-Window": str(window_seconds)
                    }
                )

            return await func(*args, **kwargs)

        return wrapper
    return decorator
