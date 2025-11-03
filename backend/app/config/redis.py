"""
Redis connection configuration and client management.
"""
import redis
from typing import Optional
from app.config.settings import settings


class RedisClient:
    """Redis client singleton for connection management"""

    _instance: Optional[redis.Redis] = None

    @classmethod
    def get_client(cls) -> Optional[redis.Redis]:
        """
        Get or create Redis client instance.

        Returns:
            Redis client instance if caching is enabled, None otherwise
        """
        if not settings.CACHE_ENABLED:
            return None

        if cls._instance is None:
            try:
                cls._instance = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB,
                    password=settings.REDIS_PASSWORD,
                    decode_responses=True,  # Automatically decode bytes to strings
                    socket_connect_timeout=5,
                    socket_timeout=5,
                    retry_on_timeout=True
                )
                # Test connection
                cls._instance.ping()
                print(f"✓ Redis connected successfully at {settings.REDIS_HOST}:{settings.REDIS_PORT}")
            except redis.ConnectionError as e:
                print(f"✗ Redis connection failed: {e}")
                cls._instance = None
            except Exception as e:
                print(f"✗ Unexpected error connecting to Redis: {e}")
                cls._instance = None

        return cls._instance

    @classmethod
    def close(cls) -> None:
        """Close Redis connection"""
        if cls._instance is not None:
            cls._instance.close()
            cls._instance = None
            print("✓ Redis connection closed")


def get_redis() -> Optional[redis.Redis]:
    """
    Dependency function to get Redis client.
    Use this in FastAPI dependencies.

    Returns:
        Redis client or None if caching is disabled
    """
    return RedisClient.get_client()
