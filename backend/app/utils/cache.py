"""
Cache utilities for Redis-based caching.
Provides functions and decorators for caching data.
"""
import json
import functools
from typing import Optional, Any, Callable
from redis import Redis
from app.config.redis import get_redis
from app.config.settings import settings


def get_cache_key(*parts: str) -> str:
    """
    Generate a cache key from parts.

    Args:
        *parts: Parts to join with colons

    Returns:
        Cache key string (e.g., "products:list:category:1")
    """
    return ":".join(str(part) for part in parts)


def get_from_cache(key: str) -> Optional[Any]:
    """
    Get a value from cache.

    Args:
        key: Cache key

    Returns:
        Cached value (deserialized from JSON) or None if not found
    """
    if not settings.CACHE_ENABLED:
        return None

    redis_client = get_redis()
    if redis_client is None:
        return None

    try:
        value = redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        print(f"Cache get error for key '{key}': {e}")
        return None


def set_in_cache(key: str, value: Any, ttl: Optional[int] = None) -> bool:
    """
    Set a value in cache.

    Args:
        key: Cache key
        value: Value to cache (will be serialized to JSON)
        ttl: Time to live in seconds (default from settings)

    Returns:
        True if successful, False otherwise
    """
    if not settings.CACHE_ENABLED:
        return False

    redis_client = get_redis()
    if redis_client is None:
        return False

    try:
        ttl = ttl or settings.CACHE_TTL
        serialized = json.dumps(value, default=str)  # default=str handles datetime objects
        redis_client.setex(key, ttl, serialized)
        return True
    except Exception as e:
        print(f"Cache set error for key '{key}': {e}")
        return False


def delete_from_cache(key: str) -> bool:
    """
    Delete a key from cache.

    Args:
        key: Cache key

    Returns:
        True if deleted, False otherwise
    """
    if not settings.CACHE_ENABLED:
        return False

    redis_client = get_redis()
    if redis_client is None:
        return False

    try:
        redis_client.delete(key)
        return True
    except Exception as e:
        print(f"Cache delete error for key '{key}': {e}")
        return False


def delete_pattern_from_cache(pattern: str) -> int:
    """
    Delete all keys matching a pattern from cache.

    Args:
        pattern: Redis pattern (e.g., "products:*")

    Returns:
        Number of keys deleted
    """
    if not settings.CACHE_ENABLED:
        return 0

    redis_client = get_redis()
    if redis_client is None:
        return 0

    try:
        keys = redis_client.keys(pattern)
        if keys:
            return redis_client.delete(*keys)
        return 0
    except Exception as e:
        print(f"Cache delete pattern error for pattern '{pattern}': {e}")
        return 0


def cache_response(
    key_prefix: str,
    ttl: Optional[int] = None,
    key_builder: Optional[Callable] = None
):
    """
    Decorator to cache function responses.

    Usage:
        @cache_response(key_prefix="products", ttl=300)
        def get_all_products(skip: int = 0, limit: int = 100):
            return repository.get_all(skip, limit)

        # With custom key builder:
        @cache_response(
            key_prefix="product",
            ttl=600,
            key_builder=lambda product_id: f"product:{product_id}"
        )
        def get_product_by_id(product_id: int):
            return repository.get_by_id(product_id)

    Args:
        key_prefix: Prefix for cache key
        ttl: Time to live in seconds
        key_builder: Optional function to build custom cache key from args
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not settings.CACHE_ENABLED:
                return func(*args, **kwargs)

            # Build cache key
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                # Default key: prefix + function name + args + kwargs
                args_str = "_".join(str(arg) for arg in args)
                kwargs_str = "_".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
                parts = [key_prefix, func.__name__]
                if args_str:
                    parts.append(args_str)
                if kwargs_str:
                    parts.append(kwargs_str)
                cache_key = get_cache_key(*parts)

            # Try to get from cache
            cached_result = get_from_cache(cache_key)
            if cached_result is not None:
                return cached_result

            # Call function and cache result
            result = func(*args, **kwargs)

            # Cache the result
            if result is not None:
                # Convert SQLAlchemy models to dict if needed
                if hasattr(result, '__dict__') and not isinstance(result, (dict, list, str, int, float, bool)):
                    # Single model instance
                    cache_data = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}
                elif isinstance(result, list) and result and hasattr(result[0], '__dict__'):
                    # List of model instances
                    cache_data = [
                        {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                        for item in result
                    ]
                else:
                    cache_data = result

                set_in_cache(cache_key, cache_data, ttl)

            return result

        return wrapper
    return decorator


def invalidate_cache(pattern: str):
    """
    Decorator to invalidate cache after function execution.

    Usage:
        @invalidate_cache("products:*")
        def create_product(product_data):
            return repository.create(product_data)

    Args:
        pattern: Redis pattern to delete (e.g., "products:*")
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Invalidate cache after successful execution
            if settings.CACHE_ENABLED:
                deleted = delete_pattern_from_cache(pattern)
                if deleted > 0:
                    print(f"Cache invalidated: {deleted} keys matching '{pattern}'")

            return result

        return wrapper
    return decorator


class CacheManager:
    """Cache manager for organized cache operations"""

    @staticmethod
    def clear_all():
        """Clear all cache"""
        redis_client = get_redis()
        if redis_client:
            redis_client.flushdb()
            print("✓ All cache cleared")

    @staticmethod
    def clear_products():
        """Clear products cache"""
        count = delete_pattern_from_cache("products:*")
        print(f"✓ Cleared {count} product cache keys")

    @staticmethod
    def clear_categories():
        """Clear categories cache"""
        count = delete_pattern_from_cache("categories:*")
        print(f"✓ Cleared {count} category cache keys")

    @staticmethod
    def clear_orders():
        """Clear orders cache"""
        count = delete_pattern_from_cache("orders:*")
        print(f"✓ Cleared {count} order cache keys")

    @staticmethod
    def clear_dashboard():
        """Clear dashboard stats cache"""
        count = delete_pattern_from_cache("dashboard:*")
        print(f"✓ Cleared {count} dashboard cache keys")

    @staticmethod
    def get_stats() -> dict:
        """Get cache statistics"""
        redis_client = get_redis()
        if not redis_client:
            return {"status": "disabled"}

        try:
            info = redis_client.info()
            return {
                "status": "connected",
                "used_memory": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients"),
                "total_keys": redis_client.dbsize(),
                "uptime_seconds": info.get("uptime_in_seconds")
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
