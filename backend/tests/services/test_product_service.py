"""
Tests for ProductService
"""
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from fastapi import HTTPException, UploadFile

from app.services.product_service import ProductService
from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate


@pytest.fixture
def mock_db_session():
    """Mock database session"""
    return Mock()


@pytest.fixture
def product_service(mock_db_session):
    """Create ProductService instance with mocked database"""
    return ProductService(mock_db_session)


@pytest.fixture
def sample_product():
    """Sample product model instance"""
    return Product(
        id=1,
        name="Test Product",
        description="Test description",
        price=19.99,
        stock=100,
        category_id=1,
        image_url=None
    )


@pytest.fixture
def sample_category():
    """Sample category model instance"""
    return Category(
        id=1,
        name="Test Category",
        description="Test category description"
    )


class TestGetAllProducts:
    """Tests for get_all_products method"""

    @pytest.mark.unit
    @pytest.mark.products
    def test_get_all_products_from_cache(self, product_service, sample_product):
        """Test retrieving products from cache"""
        cached_data = [{
            "id": 1,
            "name": "Cached Product",
            "price": 9.99,
            "stock": 50,
            "category_id": 1
        }]

        with patch('app.services.product_service.get_from_cache', return_value=cached_data):
            products = product_service.get_all_products()

        assert len(products) == 1
        assert products[0].name == "Cached Product"
        assert products[0].price == 9.99

    @pytest.mark.unit
    @pytest.mark.products
    def test_get_all_products_from_database(self, product_service, sample_product):
        """Test retrieving products from database when cache miss"""
        product_service.repository.get_all = Mock(return_value=[sample_product])

        with patch('app.services.product_service.get_from_cache', return_value=None):
            with patch('app.services.product_service.set_in_cache') as mock_set_cache:
                products = product_service.get_all_products()

        assert len(products) == 1
        assert products[0].name == "Test Product"
        mock_set_cache.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.products
    def test_get_all_products_with_category_filter(self, product_service, sample_product):
        """Test retrieving products filtered by category"""
        product_service.repository.get_by_category = Mock(return_value=[sample_product])

        with patch('app.services.product_service.get_from_cache', return_value=None):
            with patch('app.services.product_service.set_in_cache'):
                products = product_service.get_all_products(category_id=1)

        assert len(products) == 1
        product_service.repository.get_by_category.assert_called_once_with(1, 0, 100)

    @pytest.mark.unit
    @pytest.mark.products
    def test_get_all_products_with_pagination(self, product_service):
        """Test retrieving products with pagination parameters"""
        product_service.repository.get_all = Mock(return_value=[])

        with patch('app.services.product_service.get_from_cache', return_value=None):
            product_service.get_all_products(skip=10, limit=20)

        product_service.repository.get_all.assert_called_once_with(10, 20)


class TestGetProductById:
    """Tests for get_product_by_id method"""

    @pytest.mark.unit
    @pytest.mark.products
    def test_get_product_by_id_from_cache(self, product_service):
        """Test retrieving product from cache"""
        cached_data = {
            "id": 1,
            "name": "Cached Product",
            "price": 9.99
        }

        with patch('app.services.product_service.get_from_cache', return_value=cached_data):
            product = product_service.get_product_by_id(1)

        assert product.id == 1
        assert product.name == "Cached Product"

    @pytest.mark.unit
    @pytest.mark.products
    def test_get_product_by_id_from_database(self, product_service, sample_product):
        """Test retrieving product from database when cache miss"""
        product_service.repository.get_by_id = Mock(return_value=sample_product)

        with patch('app.services.product_service.get_from_cache', return_value=None):
            with patch('app.services.product_service.set_in_cache') as mock_set_cache:
                product = product_service.get_product_by_id(1)

        assert product.id == 1
        assert product.name == "Test Product"
        mock_set_cache.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.products
    def test_get_product_by_id_not_found(self, product_service):
        """Test 404 error when product not found"""
        product_service.repository.get_by_id = Mock(return_value=None)

        with patch('app.services.product_service.get_from_cache', return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                product_service.get_product_by_id(999)

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value.detail)


class TestCreateProduct:
    """Tests for create_product method"""

    @pytest.mark.unit
    @pytest.mark.products
    def test_create_product_success(self, product_service, sample_product, sample_category):
        """Test successful product creation"""
        product_data = ProductCreate(
            name="New Product",
            description="New description",
            price=29.99,
            stock=50,
            category_id=1
        )

        product_service.category_repository.get_by_id = Mock(return_value=sample_category)
        product_service.repository.create = Mock(return_value=sample_product)

        with patch('app.services.product_service.delete_pattern_from_cache'):
            product = product_service.create_product(product_data)

        assert product is not None
        assert product.name == "Test Product"
        product_service.repository.create.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.products
    def test_create_product_invalid_category(self, product_service):
        """Test product creation with invalid category"""
        product_data = ProductCreate(
            name="New Product",
            price=29.99,
            stock=50,
            category_id=999
        )

        product_service.category_repository.get_by_id = Mock(return_value=None)

        with pytest.raises(HTTPException) as exc_info:
            product_service.create_product(product_data)

        assert exc_info.value.status_code == 400
        assert "Category" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.products
    def test_create_product_invalidates_cache(self, product_service, sample_product):
        """Test that cache is invalidated after creation"""
        product_data = ProductCreate(
            name="New Product",
            price=29.99,
            stock=50
        )

        product_service.repository.create = Mock(return_value=sample_product)

        with patch('app.services.product_service.delete_pattern_from_cache') as mock_delete:
            product_service.create_product(product_data)

        mock_delete.assert_called_once_with("products:list:*")


class TestUpdateProduct:
    """Tests for update_product method"""

    @pytest.mark.unit
    @pytest.mark.products
    def test_update_product_success(self, product_service, sample_product):
        """Test successful product update"""
        update_data = ProductUpdate(name="Updated Product", price=39.99)

        product_service.get_product_by_id = Mock(return_value=sample_product)
        product_service.repository.update = Mock(return_value=sample_product)

        with patch('app.services.product_service.delete_pattern_from_cache'):
            updated = product_service.update_product(1, update_data)

        assert updated is not None
        product_service.repository.update.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.products
    def test_update_product_with_category(self, product_service, sample_product, sample_category):
        """Test updating product with new category"""
        update_data = ProductUpdate(category_id=1)

        product_service.get_product_by_id = Mock(return_value=sample_product)
        product_service.category_repository.get_by_id = Mock(return_value=sample_category)
        product_service.repository.update = Mock(return_value=sample_product)

        with patch('app.services.product_service.delete_pattern_from_cache'):
            updated = product_service.update_product(1, update_data)

        assert updated is not None
        product_service.category_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.unit
    @pytest.mark.products
    def test_update_product_invalid_category(self, product_service, sample_product):
        """Test update with invalid category"""
        update_data = ProductUpdate(category_id=999)

        product_service.get_product_by_id = Mock(return_value=sample_product)
        product_service.category_repository.get_by_id = Mock(return_value=None)

        with pytest.raises(HTTPException) as exc_info:
            product_service.update_product(1, update_data)

        assert exc_info.value.status_code == 400

    @pytest.mark.unit
    @pytest.mark.products
    def test_update_product_invalidates_cache(self, product_service, sample_product):
        """Test that cache is invalidated after update"""
        update_data = ProductUpdate(name="Updated")

        product_service.get_product_by_id = Mock(return_value=sample_product)
        product_service.repository.update = Mock(return_value=sample_product)

        with patch('app.services.product_service.delete_pattern_from_cache') as mock_delete:
            product_service.update_product(1, update_data)

        assert mock_delete.call_count == 2  # detail and list


class TestDeleteProduct:
    """Tests for delete_product method"""

    @pytest.mark.unit
    @pytest.mark.products
    def test_delete_product_success(self, product_service, sample_product):
        """Test successful product deletion"""
        product_service.get_product_by_id = Mock(return_value=sample_product)
        product_service.repository.delete = Mock()

        with patch('app.services.product_service.delete_pattern_from_cache'):
            product_service.delete_product(1)

        product_service.repository.delete.assert_called_once_with(1)

    @pytest.mark.unit
    @pytest.mark.products
    def test_delete_product_not_found(self, product_service):
        """Test deletion of non-existent product"""
        product_service.get_product_by_id = Mock(
            side_effect=HTTPException(status_code=404, detail="Not found")
        )

        with pytest.raises(HTTPException):
            product_service.delete_product(999)

    @pytest.mark.unit
    @pytest.mark.products
    def test_delete_product_invalidates_cache(self, product_service, sample_product):
        """Test that cache is invalidated after deletion"""
        product_service.get_product_by_id = Mock(return_value=sample_product)
        product_service.repository.delete = Mock()

        with patch('app.services.product_service.delete_pattern_from_cache') as mock_delete:
            product_service.delete_product(1)

        assert mock_delete.call_count == 2


class TestSearchProducts:
    """Tests for search_products method"""

    @pytest.mark.unit
    @pytest.mark.products
    def test_search_products(self, product_service, sample_product):
        """Test product search functionality"""
        product_service.repository.search_by_name = Mock(return_value=[sample_product])

        products = product_service.search_products("test")

        assert len(products) == 1
        product_service.repository.search_by_name.assert_called_once_with("test", 0, 100)

    @pytest.mark.unit
    @pytest.mark.products
    def test_search_products_with_pagination(self, product_service):
        """Test product search with pagination"""
        product_service.repository.search_by_name = Mock(return_value=[])

        product_service.search_products("test", skip=10, limit=20)

        product_service.repository.search_by_name.assert_called_once_with("test", 10, 20)


class TestGetLowStockProducts:
    """Tests for get_low_stock_products method"""

    @pytest.mark.unit
    @pytest.mark.products
    def test_get_low_stock_products(self, product_service, sample_product):
        """Test retrieving low stock products"""
        sample_product.stock = 5
        product_service.repository.get_low_stock_products = Mock(return_value=[sample_product])

        products = product_service.get_low_stock_products(threshold=10)

        assert len(products) == 1
        assert products[0].stock <= 10
        product_service.repository.get_low_stock_products.assert_called_once_with(10)


class TestUploadProductImage:
    """Tests for upload_product_image method"""

    @pytest.mark.unit
    @pytest.mark.products
    @pytest.mark.images
    @pytest.mark.asyncio
    async def test_upload_product_image_success(self, product_service, sample_product):
        """Test successful image upload"""
        # Create mock upload file
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test.jpg"

        product_service.get_product_by_id = Mock(return_value=sample_product)
        product_service.repository.update = Mock(return_value=sample_product)

        with patch('app.services.product_service.save_upload_file', new_callable=AsyncMock) as mock_save:
            with patch('app.services.product_service.generate_thumbnails') as mock_gen:
                with patch('app.services.product_service.delete_file'):
                    with patch('app.services.product_service.delete_pattern_from_cache'):
                        mock_save.return_value = "temp_test.jpg"
                        mock_gen.return_value = {
                            "original": "/uploads/products/1/original.jpg",
                            "thumbnail": "/uploads/products/1/thumbnail.webp",
                            "medium": "/uploads/products/1/medium.webp",
                            "large": "/uploads/products/1/large.webp"
                        }

                        updated = await product_service.upload_product_image(1, mock_file)

        assert updated is not None
        product_service.repository.update.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.products
    @pytest.mark.images
    @pytest.mark.asyncio
    async def test_upload_product_image_replaces_old(self, product_service, sample_product):
        """Test that old images are deleted when uploading new"""
        sample_product.image_url = "/uploads/products/1/old.jpg"
        mock_file = Mock(spec=UploadFile)

        product_service.get_product_by_id = Mock(return_value=sample_product)
        product_service.repository.update = Mock(return_value=sample_product)

        with patch('app.services.product_service.delete_product_images') as mock_delete:
            with patch('app.services.product_service.save_upload_file', new_callable=AsyncMock):
                with patch('app.services.product_service.generate_thumbnails') as mock_gen:
                    with patch('app.services.product_service.delete_file'):
                        with patch('app.services.product_service.delete_pattern_from_cache'):
                            mock_gen.return_value = {"large": "/uploads/products/1/large.webp"}

                            await product_service.upload_product_image(1, mock_file)

        mock_delete.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.products
    @pytest.mark.images
    @pytest.mark.asyncio
    async def test_upload_product_image_not_found(self, product_service):
        """Test upload to non-existent product"""
        mock_file = Mock(spec=UploadFile)

        product_service.get_product_by_id = Mock(
            side_effect=HTTPException(status_code=404, detail="Not found")
        )

        with pytest.raises(HTTPException):
            await product_service.upload_product_image(999, mock_file)


class TestDeleteProductImage:
    """Tests for delete_product_image method"""

    @pytest.mark.unit
    @pytest.mark.products
    @pytest.mark.images
    def test_delete_product_image_success(self, product_service, sample_product):
        """Test successful image deletion"""
        sample_product.image_url = "/uploads/products/1/image.jpg"

        product_service.get_product_by_id = Mock(return_value=sample_product)
        product_service.repository.update = Mock(return_value=sample_product)

        with patch('app.services.product_service.delete_product_images', return_value=True):
            with patch('app.services.product_service.delete_pattern_from_cache'):
                updated = product_service.delete_product_image(1)

        assert updated is not None
        product_service.repository.update.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.products
    @pytest.mark.images
    def test_delete_product_image_no_image(self, product_service, sample_product):
        """Test deletion when product has no image"""
        sample_product.image_url = None

        product_service.get_product_by_id = Mock(return_value=sample_product)

        with pytest.raises(HTTPException) as exc_info:
            product_service.delete_product_image(1)

        assert exc_info.value.status_code == 400
        assert "no image" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.products
    @pytest.mark.images
    def test_delete_product_image_deletion_fails(self, product_service, sample_product):
        """Test error handling when deletion fails"""
        sample_product.image_url = "/uploads/products/1/image.jpg"

        product_service.get_product_by_id = Mock(return_value=sample_product)

        with patch('app.services.product_service.delete_product_images', return_value=False):
            with pytest.raises(HTTPException) as exc_info:
                product_service.delete_product_image(1)

        assert exc_info.value.status_code == 500
