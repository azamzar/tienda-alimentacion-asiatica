"""
Tests for cache utilities
"""
import pytest
import json
from unittest.mock import MagicMock, patch
from datetime import datetime

from app.utils.cache import (
    get_cache_key,
    get_from_cache,
    set_in_cache,
    delete_from_cache,
    delete_pattern_from_cache,
    cache_response,
    invalidate_cache,
    CacheManager
)


class TestGetCacheKey:
    """Tests for get_cache_key function"""

    @pytest.mark.unit
    @pytest.mark.cache
    def test_get_cache_key_single_part(self):
        """Test cache key with single part"""
        key = get_cache_key("products")
        assert key == "products"

    @pytest.mark.unit
    @pytest.mark.cache
    def test_get_cache_key_multiple_parts(self):
        """Test cache key with multiple parts"""
        key = get_cache_key("products", "list", "category", "1")
        assert key == "products:list:category:1"

    @pytest.mark.unit
    @pytest.mark.cache
    def test_get_cache_key_with_integers(self):
        """Test cache key with integer parts"""
        key = get_cache_key("product", 123, "details")
        assert key == "product:123:details"

    @pytest.mark.unit
    @pytest.mark.cache
    def test_get_cache_key_empty(self):
        """Test cache key with no parts"""
        key = get_cache_key()
        assert key == ""


class TestGetFromCache:
    """Tests for get_from_cache function"""

    @pytest.mark.unit
    @pytest.mark.cache
    def test_get_from_cache_success(self, mock_redis):
        """Test successful cache retrieval"""
        test_data = {"id": 1, "name": "Test Product"}
        mock_redis.get.return_value = json.dumps(test_data)

        with patch('app.config.settings.settings.CACHE_ENABLED', True):
            with patch('app.utils.cache.get_redis', return_value=mock_redis):
                result = get_from_cache("test:key")

        assert result == test_data
        mock_redis.get.assert_called_once_with("test:key")

    @pytest.mark.unit
    @pytest.mark.cache
    def test_get_from_cache_not_found(self, mock_redis):
        """Test cache retrieval when key doesn't exist"""
        mock_redis.get.return_value = None

        with patch('app.config.settings.settings.CACHE_ENABLED', True):
            with patch('app.utils.cache.get_redis', return_value=mock_redis):
                result = get_from_cache("nonexistent:key")

        assert result is None

    @pytest.mark.unit
    @pytest.mark.cache
    def test_get_from_cache_disabled(self, mock_redis):
        """Test cache retrieval when caching is disabled"""
        with patch('app.config.settings.settings.CACHE_ENABLED', False):
            result = get_from_cache("test:key")

        assert result is None
        mock_redis.get.assert_not_called()

    @pytest.mark.unit
    @pytest.mark.cache
    def test_get_from_cache_redis_unavailable(self):
        """Test cache retrieval when Redis is unavailable"""
        with patch('app.config.settings.settings.CACHE_ENABLED', True):
            with patch('app.utils.cache.get_redis', return_value=None):
                result = get_from_cache("test:key")

        assert result is None

    @pytest.mark.unit
    @pytest.mark.cache
    def test_get_from_cache_json_decode_error(self, mock_redis):
        """Test handling of invalid JSON in cache"""
        mock_redis.get.return_value = "invalid json"

        with patch('app.config.settings.settings.CACHE_ENABLED', True):
            with patch('app.utils.cache.get_redis', return_value=mock_redis):
                result = get_from_cache("test:key")

        # Should return None on JSON decode error
        assert result is None

    @pytest.mark.unit
    @pytest.mark.cache
    def test_get_from_cache_complex_data(self, mock_redis):
        """Test cache retrieval with complex nested data"""
        test_data = {
            "id": 1,
            "products": [
                {"id": 1, "name": "Product 1"},
                {"id": 2, "name": "Product 2"}
            ],
            "metadata": {"total": 2, "page": 1}
        }
        mock_redis.get.return_value = json.dumps(test_data)

        with patch('app.config.settings.settings.CACHE_ENABLED', True):
            with patch('app.utils.cache.get_redis', return_value=mock_redis):
                result = get_from_cache("test:key")

        assert result == test_data


class TestSetInCache:
    """Tests for set_in_cache function"""

    @pytest.mark.unit
    @pytest.mark.cache
    def test_set_in_cache_success(self, mock_redis):
        """Test successful cache set"""
        test_data = {"id": 1, "name": "Test"}

        with patch('app.config.settings.settings.CACHE_ENABLED', True):
            with patch('app.config.settings.settings.CACHE_TTL', 300):
                with patch('app.utils.cache.get_redis', return_value=mock_redis):
                    result = set_in_cache("test:key", test_data)

        assert result is True
        mock_redis.setex.assert_called_once_with("test:key", 300, json.dumps(test_data))

    @pytest.mark.unit
    @pytest.mark.cache
    def test_set_in_cache_custom_ttl(self, mock_redis):
        """Test cache set with custom TTL"""
        test_data = {"id": 1}
        custom_ttl = 600

        with patch('app.config.settings.settings.CACHE_ENABLED', True):
            with patch('app.utils.cache.get_redis', return_value=mock_redis):
                result = set_in_cache("test:key", test_data, ttl=custom_ttl)

        assert result is True
        mock_redis.setex.assert_called_once_with("test:key", custom_ttl, json.dumps(test_data))

    @pytest.mark.unit
    @pytest.mark.cache
    def test_set_in_cache_disabled(self, mock_redis):
        """Test cache set when caching is disabled"""
        with patch('app.config.settings.settings.CACHE_ENABLED', False):
            result = set_in_cache("test:key", {"data": "test"})

        assert result is False
        mock_redis.setex.assert_not_called()

    @pytest.mark.unit
    @pytest.mark.cache
    def test_set_in_cache_redis_unavailable(self):
        """Test cache set when Redis is unavailable"""
        with patch('app.config.settings.settings.CACHE_ENABLED', True):
            with patch('app.utils.cache.get_redis', return_value=None):
                result = set_in_cache("test:key", {"data": "test"})

        assert result is False

    @pytest.mark.unit
    @pytest.mark.cache
    def test_set_in_cache_datetime_handling(self, mock_redis):
        """Test cache set with datetime objects"""
        test_data = {"id": 1, "created_at": datetime(2024, 1, 1, 12, 0, 0)}

        with patch('app.config.settings.settings.CACHE_ENABLED', True):
            with patch('app.config.settings.settings.CACHE_TTL', 300):
                with patch('app.utils.cache.get_redis', return_value=mock_redis):
                    result = set_in_cache("test:key", test_data)

        assert result is True
        # Datetime should be serialized using default=str
        mock_redis.setex.assert_called_once()


class TestDeleteFromCache:
    """Tests for delete_from_cache function"""

    @pytest.mark.unit
    @pytest.mark.cache
    def test_delete_from_cache_success(self, mock_redis):
        """Test successful cache deletion"""
        with patch('app.config.settings.settings.CACHE_ENABLED', True):
            with patch('app.utils.cache.get_redis', return_value=mock_redis):
                result = delete_from_cache("test:key")

        assert result is True
        mock_redis.delete.assert_called_once_with("test:key")

    @pytest.mark.unit
    @pytest.mark.cache
    def test_delete_from_cache_disabled(self, mock_redis):
        """Test cache deletion when caching is disabled"""
        with patch('app.config.settings.settings.CACHE_ENABLED', False):
            result = delete_from_cache("test:key")

        assert result is False
        mock_redis.delete.assert_not_called()

    @pytest.mark.unit
    @pytest.mark.cache
    def test_delete_from_cache_redis_unavailable(self):
        """Test cache deletion when Redis is unavailable"""
        with patch('app.config.settings.settings.CACHE_ENABLED', True):
            with patch('app.utils.cache.get_redis', return_value=None):
                result = delete_from_cache("test:key")

        assert result is False


class TestDeletePatternFromCache:
    """Tests for delete_pattern_from_cache function"""

    @pytest.mark.unit
    @pytest.mark.cache
    def test_delete_pattern_success(self, mock_redis):
        """Test successful pattern deletion"""
        mock_redis.keys.return_value = ["products:1", "products:2", "products:3"]
        mock_redis.delete.return_value = 3

        with patch('app.config.settings.settings.CACHE_ENABLED', True):
            with patch('app.utils.cache.get_redis', return_value=mock_redis):
                result = delete_pattern_from_cache("products:*")

        assert result == 3
        mock_redis.keys.assert_called_once_with("products:*")
        mock_redis.delete.assert_called_once_with("products:1", "products:2", "products:3")

    @pytest.mark.unit
    @pytest.mark.cache
    def test_delete_pattern_no_matches(self, mock_redis):
        """Test pattern deletion with no matches"""
        mock_redis.keys.return_value = []

        with patch('app.config.settings.settings.CACHE_ENABLED', True):
            with patch('app.utils.cache.get_redis', return_value=mock_redis):
                result = delete_pattern_from_cache("nonexistent:*")

        assert result == 0
        mock_redis.keys.assert_called_once_with("nonexistent:*")
        mock_redis.delete.assert_not_called()

    @pytest.mark.unit
    @pytest.mark.cache
    def test_delete_pattern_disabled(self, mock_redis):
        """Test pattern deletion when caching is disabled"""
        with patch('app.config.settings.settings.CACHE_ENABLED', False):
            result = delete_pattern_from_cache("products:*")

        assert result == 0
        mock_redis.keys.assert_not_called()


class TestCacheResponseDecorator:
    """Tests for cache_response decorator"""

    @pytest.mark.unit
    @pytest.mark.cache
    def test_cache_response_decorator_caches_result(self, mock_redis):
        """Test that decorator caches function result"""
        mock_redis.get.return_value = None

        @cache_response(key_prefix="test", ttl=300)
        def get_data():
            return {"id": 1, "value": "test"}

        with patch('app.config.settings.settings.CACHE_ENABLED', True):
            with patch('app.utils.cache.get_redis', return_value=mock_redis):
                result = get_data()

        assert result == {"id": 1, "value": "test"}
        mock_redis.setex.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.cache
    def test_cache_response_decorator_returns_cached(self, mock_redis):
        """Test that decorator returns cached result"""
        cached_data = {"id": 1, "value": "cached"}
        mock_redis.get.return_value = json.dumps(cached_data)

        call_count = 0

        @cache_response(key_prefix="test")
        def get_data():
            nonlocal call_count
            call_count += 1
            return {"id": 1, "value": "new"}

        with patch('app.config.settings.settings.CACHE_ENABLED', True):
            with patch('app.utils.cache.get_redis', return_value=mock_redis):
                result = get_data()

        assert result == cached_data
        assert call_count == 0  # Function should not be called

    @pytest.mark.unit
    @pytest.mark.cache
    def test_cache_response_decorator_disabled(self):
        """Test decorator when caching is disabled"""
        call_count = 0

        @cache_response(key_prefix="test")
        def get_data():
            nonlocal call_count
            call_count += 1
            return {"id": 1}

        with patch('app.config.settings.settings.CACHE_ENABLED', False):
            result = get_data()

        assert result == {"id": 1}
        assert call_count == 1  # Function should be called


class TestInvalidateCacheDecorator:
    """Tests for invalidate_cache decorator"""

    @pytest.mark.unit
    @pytest.mark.cache
    def test_invalidate_cache_decorator(self, mock_redis):
        """Test that decorator invalidates cache after execution"""
        mock_redis.keys.return_value = ["products:1", "products:2"]
        mock_redis.delete.return_value = 2

        @invalidate_cache("products:*")
        def create_product(name):
            return {"id": 1, "name": name}

        with patch('app.config.settings.settings.CACHE_ENABLED', True):
            with patch('app.utils.cache.get_redis', return_value=mock_redis):
                result = create_product("Test Product")

        assert result == {"id": 1, "name": "Test Product"}
        mock_redis.keys.assert_called_once_with("products:*")
        mock_redis.delete.assert_called_once()


class TestCacheManager:
    """Tests for CacheManager class"""

    @pytest.mark.unit
    @pytest.mark.cache
    def test_cache_manager_clear_all(self, mock_redis):
        """Test clearing all cache"""
        with patch('app.utils.cache.get_redis', return_value=mock_redis):
            CacheManager.clear_all()

        mock_redis.flushdb.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.cache
    def test_cache_manager_clear_products(self, mock_redis):
        """Test clearing products cache"""
        mock_redis.keys.return_value = ["products:1", "products:2"]
        mock_redis.delete.return_value = 2

        with patch('app.config.settings.settings.CACHE_ENABLED', True):
            with patch('app.utils.cache.get_redis', return_value=mock_redis):
                CacheManager.clear_products()

        mock_redis.keys.assert_called_once_with("products:*")

    @pytest.mark.unit
    @pytest.mark.cache
    def test_cache_manager_get_stats_connected(self, mock_redis):
        """Test getting cache stats when connected"""
        mock_redis.info.return_value = {
            "used_memory_human": "1.5M",
            "connected_clients": 5,
            "uptime_in_seconds": 3600
        }
        mock_redis.dbsize.return_value = 100

        with patch('app.utils.cache.get_redis', return_value=mock_redis):
            stats = CacheManager.get_stats()

        assert stats["status"] == "connected"
        assert stats["used_memory"] == "1.5M"
        assert stats["total_keys"] == 100

    @pytest.mark.unit
    @pytest.mark.cache
    def test_cache_manager_get_stats_disabled(self):
        """Test getting cache stats when Redis is disabled"""
        with patch('app.utils.cache.get_redis', return_value=None):
            stats = CacheManager.get_stats()

        assert stats["status"] == "disabled"
