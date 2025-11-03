"""
Tests for CategoryService
"""
import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException

from app.services.category_service import CategoryService
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


@pytest.fixture
def mock_db_session():
    """Mock database session"""
    return Mock()


@pytest.fixture
def category_service(mock_db_session):
    """Create CategoryService instance with mocked database"""
    return CategoryService(mock_db_session)


@pytest.fixture
def sample_category():
    """Sample category model instance"""
    return Category(
        id=1,
        name="Bebidas",
        description="Bebidas asiáticas"
    )


@pytest.fixture
def sample_categories():
    """Sample list of category model instances"""
    return [
        Category(id=1, name="Bebidas", description="Bebidas asiáticas"),
        Category(id=2, name="Snacks", description="Snacks y aperitivos"),
        Category(id=3, name="Salsas", description="Salsas y condimentos")
    ]


class TestGetAllCategories:
    """Tests for get_all_categories method"""

    @pytest.mark.unit
    @pytest.mark.categories
    def test_get_all_categories_from_cache(self, category_service):
        """Test retrieving categories from cache"""
        cached_data = [
            {"id": 1, "name": "Cached Category 1", "description": "Description 1"},
            {"id": 2, "name": "Cached Category 2", "description": "Description 2"}
        ]

        with patch('app.services.category_service.get_from_cache', return_value=cached_data):
            categories = category_service.get_all_categories()

        assert len(categories) == 2
        assert categories[0].name == "Cached Category 1"
        assert categories[1].name == "Cached Category 2"

    @pytest.mark.unit
    @pytest.mark.categories
    def test_get_all_categories_from_database(self, category_service, sample_categories):
        """Test retrieving categories from database when cache miss"""
        category_service.repository.get_all = Mock(return_value=sample_categories)

        with patch('app.services.category_service.get_from_cache', return_value=None):
            with patch('app.services.category_service.set_in_cache') as mock_set_cache:
                categories = category_service.get_all_categories()

        assert len(categories) == 3
        assert categories[0].name == "Bebidas"
        assert categories[1].name == "Snacks"
        assert categories[2].name == "Salsas"
        mock_set_cache.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.categories
    def test_get_all_categories_empty_list(self, category_service):
        """Test retrieving empty list of categories"""
        category_service.repository.get_all = Mock(return_value=[])

        with patch('app.services.category_service.get_from_cache', return_value=None):
            with patch('app.services.category_service.set_in_cache') as mock_set_cache:
                categories = category_service.get_all_categories()

        assert len(categories) == 0
        # Should not cache empty results
        mock_set_cache.assert_not_called()

    @pytest.mark.unit
    @pytest.mark.categories
    def test_get_all_categories_cache_ttl(self, category_service, sample_categories):
        """Test that categories are cached with correct TTL"""
        category_service.repository.get_all = Mock(return_value=sample_categories)

        with patch('app.services.category_service.get_from_cache', return_value=None):
            with patch('app.services.category_service.set_in_cache') as mock_set_cache:
                category_service.get_all_categories()

        # Should cache with 10 minutes TTL
        call_args = mock_set_cache.call_args
        assert call_args[1]['ttl'] == 600


class TestGetCategoryById:
    """Tests for get_category_by_id method"""

    @pytest.mark.unit
    @pytest.mark.categories
    def test_get_category_by_id_from_cache(self, category_service):
        """Test retrieving category from cache"""
        cached_data = {
            "id": 1,
            "name": "Cached Category",
            "description": "Cached description"
        }

        with patch('app.services.category_service.get_from_cache', return_value=cached_data):
            category = category_service.get_category_by_id(1)

        assert category.id == 1
        assert category.name == "Cached Category"

    @pytest.mark.unit
    @pytest.mark.categories
    def test_get_category_by_id_from_database(self, category_service, sample_category):
        """Test retrieving category from database when cache miss"""
        category_service.repository.get_by_id = Mock(return_value=sample_category)

        with patch('app.services.category_service.get_from_cache', return_value=None):
            with patch('app.services.category_service.set_in_cache') as mock_set_cache:
                category = category_service.get_category_by_id(1)

        assert category.id == 1
        assert category.name == "Bebidas"
        mock_set_cache.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.categories
    def test_get_category_by_id_not_found(self, category_service):
        """Test 404 error when category not found"""
        category_service.repository.get_by_id = Mock(return_value=None)

        with patch('app.services.category_service.get_from_cache', return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                category_service.get_category_by_id(999)

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.categories
    def test_get_category_by_id_cache_key(self, category_service, sample_category):
        """Test that correct cache key is generated"""
        category_service.repository.get_by_id = Mock(return_value=sample_category)

        with patch('app.services.category_service.get_from_cache', return_value=None) as mock_get_cache:
            with patch('app.services.category_service.set_in_cache'):
                category_service.get_category_by_id(1)

        # Should use cache key with category ID
        mock_get_cache.assert_called_once_with("categories:detail:1")


class TestCreateCategory:
    """Tests for create_category method"""

    @pytest.mark.unit
    @pytest.mark.categories
    def test_create_category_success(self, category_service, sample_category):
        """Test successful category creation"""
        category_data = CategoryCreate(
            name="Nueva Categoría",
            description="Nueva descripción"
        )

        category_service.repository.exists_by_name = Mock(return_value=False)
        category_service.repository.create = Mock(return_value=sample_category)

        with patch('app.services.category_service.delete_pattern_from_cache'):
            category = category_service.create_category(category_data)

        assert category is not None
        assert category.name == "Bebidas"
        category_service.repository.create.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.categories
    def test_create_category_duplicate_name(self, category_service):
        """Test category creation with duplicate name"""
        category_data = CategoryCreate(
            name="Bebidas",
            description="Descripción"
        )

        category_service.repository.exists_by_name = Mock(return_value=True)

        with pytest.raises(HTTPException) as exc_info:
            category_service.create_category(category_data)

        assert exc_info.value.status_code == 400
        assert "already exists" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.categories
    def test_create_category_invalidates_cache(self, category_service, sample_category):
        """Test that cache is invalidated after creation"""
        category_data = CategoryCreate(
            name="Nueva Categoría",
            description="Descripción"
        )

        category_service.repository.exists_by_name = Mock(return_value=False)
        category_service.repository.create = Mock(return_value=sample_category)

        with patch('app.services.category_service.delete_pattern_from_cache') as mock_delete:
            category_service.create_category(category_data)

        # Should invalidate both categories and products cache
        assert mock_delete.call_count == 2
        calls = [call[0][0] for call in mock_delete.call_args_list]
        assert "categories:*" in calls
        assert "products:list:*" in calls

    @pytest.mark.unit
    @pytest.mark.categories
    def test_create_category_without_description(self, category_service, sample_category):
        """Test creating category without description"""
        category_data = CategoryCreate(name="Nueva Categoría")

        category_service.repository.exists_by_name = Mock(return_value=False)
        category_service.repository.create = Mock(return_value=sample_category)

        with patch('app.services.category_service.delete_pattern_from_cache'):
            category = category_service.create_category(category_data)

        assert category is not None


class TestUpdateCategory:
    """Tests for update_category method"""

    @pytest.mark.unit
    @pytest.mark.categories
    def test_update_category_success(self, category_service, sample_category):
        """Test successful category update"""
        update_data = CategoryUpdate(name="Bebidas Actualizadas", description="Nueva descripción")

        category_service.get_category_by_id = Mock(return_value=sample_category)
        category_service.repository.exists_by_name = Mock(return_value=False)
        category_service.repository.update = Mock(return_value=sample_category)

        with patch('app.services.category_service.delete_pattern_from_cache'):
            updated = category_service.update_category(1, update_data)

        assert updated is not None
        category_service.repository.update.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.categories
    def test_update_category_same_name(self, category_service, sample_category):
        """Test updating category with same name (no duplicate check needed)"""
        update_data = CategoryUpdate(name="Bebidas", description="Nueva descripción")

        category_service.get_category_by_id = Mock(return_value=sample_category)
        category_service.repository.exists_by_name = Mock(return_value=False)
        category_service.repository.update = Mock(return_value=sample_category)

        with patch('app.services.category_service.delete_pattern_from_cache'):
            updated = category_service.update_category(1, update_data)

        assert updated is not None

    @pytest.mark.unit
    @pytest.mark.categories
    def test_update_category_duplicate_name(self, category_service, sample_category):
        """Test update with duplicate name"""
        update_data = CategoryUpdate(name="Snacks")

        category_service.get_category_by_id = Mock(return_value=sample_category)
        category_service.repository.exists_by_name = Mock(return_value=True)

        with pytest.raises(HTTPException) as exc_info:
            category_service.update_category(1, update_data)

        assert exc_info.value.status_code == 400
        assert "already exists" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.categories
    def test_update_category_not_found(self, category_service):
        """Test updating non-existent category"""
        update_data = CategoryUpdate(name="Nueva")

        category_service.get_category_by_id = Mock(
            side_effect=HTTPException(status_code=404, detail="Not found")
        )

        with pytest.raises(HTTPException):
            category_service.update_category(999, update_data)

    @pytest.mark.unit
    @pytest.mark.categories
    def test_update_category_invalidates_cache(self, category_service, sample_category):
        """Test that cache is invalidated after update"""
        update_data = CategoryUpdate(description="Nueva descripción")

        category_service.get_category_by_id = Mock(return_value=sample_category)
        category_service.repository.update = Mock(return_value=sample_category)

        with patch('app.services.category_service.delete_pattern_from_cache') as mock_delete:
            category_service.update_category(1, update_data)

        # Should invalidate both categories and products cache
        assert mock_delete.call_count == 2

    @pytest.mark.unit
    @pytest.mark.categories
    def test_update_category_partial_update(self, category_service, sample_category):
        """Test partial update (only description)"""
        update_data = CategoryUpdate(description="Solo descripción")

        category_service.get_category_by_id = Mock(return_value=sample_category)
        category_service.repository.update = Mock(return_value=sample_category)

        with patch('app.services.category_service.delete_pattern_from_cache'):
            updated = category_service.update_category(1, update_data)

        assert updated is not None


class TestDeleteCategory:
    """Tests for delete_category method"""

    @pytest.mark.unit
    @pytest.mark.categories
    def test_delete_category_success(self, category_service, sample_category):
        """Test successful category deletion"""
        category_service.get_category_by_id = Mock(return_value=sample_category)
        category_service.repository.delete = Mock()

        with patch('app.services.category_service.delete_pattern_from_cache'):
            category_service.delete_category(1)

        category_service.repository.delete.assert_called_once_with(1)

    @pytest.mark.unit
    @pytest.mark.categories
    def test_delete_category_not_found(self, category_service):
        """Test deletion of non-existent category"""
        category_service.get_category_by_id = Mock(
            side_effect=HTTPException(status_code=404, detail="Not found")
        )

        with pytest.raises(HTTPException):
            category_service.delete_category(999)

    @pytest.mark.unit
    @pytest.mark.categories
    def test_delete_category_invalidates_cache(self, category_service, sample_category):
        """Test that cache is invalidated after deletion"""
        category_service.get_category_by_id = Mock(return_value=sample_category)
        category_service.repository.delete = Mock()

        with patch('app.services.category_service.delete_pattern_from_cache') as mock_delete:
            category_service.delete_category(1)

        # Should invalidate both categories and products cache
        assert mock_delete.call_count == 2
        calls = [call[0][0] for call in mock_delete.call_args_list]
        assert "categories:*" in calls
        assert "products:list:*" in calls


class TestCategoryValidation:
    """Tests for category validation logic"""

    @pytest.mark.unit
    @pytest.mark.categories
    def test_name_uniqueness_on_create(self, category_service):
        """Test that name uniqueness is checked on create"""
        category_data = CategoryCreate(name="Bebidas")

        category_service.repository.exists_by_name = Mock(return_value=True)

        with pytest.raises(HTTPException) as exc_info:
            category_service.create_category(category_data)

        category_service.repository.exists_by_name.assert_called_once_with("Bebidas")
        assert exc_info.value.status_code == 400

    @pytest.mark.unit
    @pytest.mark.categories
    def test_name_uniqueness_on_update(self, category_service, sample_category):
        """Test that name uniqueness is checked on update when name changes"""
        update_data = CategoryUpdate(name="Nuevo Nombre")

        category_service.get_category_by_id = Mock(return_value=sample_category)
        category_service.repository.exists_by_name = Mock(return_value=True)

        with pytest.raises(HTTPException) as exc_info:
            category_service.update_category(1, update_data)

        category_service.repository.exists_by_name.assert_called_once_with("Nuevo Nombre")
        assert exc_info.value.status_code == 400
