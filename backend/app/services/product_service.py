from typing import List, Optional
from pathlib import Path
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository
from app.config.settings import settings
from app.utils.file_utils import save_upload_file, delete_file
from app.utils.image_optimizer import generate_thumbnails, delete_product_images
from app.utils.cache import (
    get_from_cache,
    set_in_cache,
    delete_pattern_from_cache,
    get_cache_key
)


class ProductService:
    """Service layer for Product business logic"""

    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    def get_all_products(
        self,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None
    ) -> List[Product]:
        """Get all products with optional category filter (cached)"""
        # Build cache key
        cache_key = get_cache_key(
            "products", "list",
            f"skip={skip}", f"limit={limit}",
            f"category={category_id}" if category_id else "all"
        )

        # Try to get from cache
        cached_data = get_from_cache(cache_key)
        if cached_data is not None:
            # Reconstruct Product objects from cached data
            return [Product(**item) for item in cached_data]

        # Get from database
        if category_id:
            products = self.repository.get_by_category(category_id, skip, limit)
        else:
            products = self.repository.get_all(skip, limit)

        # Cache the result (convert to dict for JSON serialization)
        if products:
            cache_data = [
                {k: v for k, v in p.__dict__.items() if not k.startswith('_')}
                for p in products
            ]
            set_in_cache(cache_key, cache_data, ttl=300)  # 5 minutes

        return products

    def get_product_by_id(self, product_id: int) -> Product:
        """Get a product by ID, raise 404 if not found (cached)"""
        # Build cache key
        cache_key = get_cache_key("products", "detail", str(product_id))

        # Try to get from cache
        cached_data = get_from_cache(cache_key)
        if cached_data is not None:
            return Product(**cached_data)

        # Get from database
        product = self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )

        # Cache the result
        cache_data = {k: v for k, v in product.__dict__.items() if not k.startswith('_')}
        set_in_cache(cache_key, cache_data, ttl=600)  # 10 minutes

        return product

    def create_product(self, product_data: ProductCreate) -> Product:
        """Create a new product with validation and cache invalidation"""
        # Validate category exists if provided
        if product_data.category_id:
            category = self.category_repository.get_by_id(product_data.category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Category with id {product_data.category_id} not found"
                )

        product_dict = product_data.model_dump()
        product = self.repository.create(product_dict)

        # Invalidate products list cache
        delete_pattern_from_cache("products:list:*")

        return product

    def update_product(self, product_id: int, product_data: ProductUpdate) -> Product:
        """Update a product with validation and cache invalidation"""
        # Get existing product
        db_product = self.get_product_by_id(product_id)

        # Validate category if being updated
        if product_data.category_id is not None:
            category = self.category_repository.get_by_id(product_data.category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Category with id {product_data.category_id} not found"
                )

        # Update only provided fields
        update_data = product_data.model_dump(exclude_unset=True)
        product = self.repository.update(db_product, update_data)

        # Invalidate cache for this product and list
        delete_pattern_from_cache(f"products:detail:{product_id}")
        delete_pattern_from_cache("products:list:*")

        return product

    def delete_product(self, product_id: int) -> None:
        """Delete a product by ID with cache invalidation"""
        # Verify product exists
        self.get_product_by_id(product_id)

        # Delete product
        self.repository.delete(product_id)

        # Invalidate cache for this product and list
        delete_pattern_from_cache(f"products:detail:{product_id}")
        delete_pattern_from_cache("products:list:*")

    def search_products(self, name: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Search products by name"""
        return self.repository.search_by_name(name, skip, limit)

    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """Get products with low stock"""
        return self.repository.get_low_stock_products(threshold)

    async def upload_product_image(self, product_id: int, file: UploadFile) -> Product:
        """
        Upload an image for a product and generate optimized thumbnails

        Args:
            product_id: ID of the product
            file: Uploaded image file

        Returns:
            Updated product with image_url

        Raises:
            HTTPException: If product not found or upload fails
        """
        # Get existing product
        product = self.get_product_by_id(product_id)

        # Delete old images if exist (all thumbnails)
        if product.image_url:
            delete_product_images(product_id, Path(settings.PRODUCTS_UPLOAD_DIR))

        # Save temporary uploaded file
        temp_filename = await save_upload_file(
            file,
            settings.PRODUCTS_UPLOAD_DIR,
            settings.MAX_UPLOAD_SIZE
        )
        temp_path = Path(settings.PRODUCTS_UPLOAD_DIR) / temp_filename

        try:
            # Generate all optimized thumbnails (thumbnail, medium, large) + original
            # This creates a directory structure: uploads/products/{id}/original.jpg, thumbnail.webp, etc.
            image_urls = generate_thumbnails(
                source_image_path=temp_path,
                product_id=product_id,
                upload_dir=Path(settings.PRODUCTS_UPLOAD_DIR)
            )

            # Delete temporary file (we now have organized images in product directory)
            delete_file(temp_path)

            # Update product with the 'large' image URL (best quality for detail view)
            # Frontend can choose which size to use: thumbnail, medium, or large
            image_url = image_urls.get("large", image_urls.get("original"))
            update_data = {"image_url": image_url}
            updated_product = self.repository.update(product, update_data)

            # Invalidate cache for this product
            delete_pattern_from_cache(f"products:detail:{product_id}")
            delete_pattern_from_cache("products:list:*")

            return updated_product

        except Exception as e:
            # Clean up temporary file if something goes wrong
            if temp_path.exists():
                delete_file(temp_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process image: {str(e)}"
            )

    def delete_product_image(self, product_id: int) -> Product:
        """
        Delete all images (original + thumbnails) of a product

        Args:
            product_id: ID of the product

        Returns:
            Updated product without image

        Raises:
            HTTPException: If product not found
        """
        # Get existing product
        product = self.get_product_by_id(product_id)

        if not product.image_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product has no image to delete"
            )

        # Delete all product images (original + thumbnails)
        success = delete_product_images(product_id, Path(settings.PRODUCTS_UPLOAD_DIR))

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete product images"
            )

        # Update product (remove image_url)
        update_data = {"image_url": None}
        updated_product = self.repository.update(product, update_data)

        # Invalidate cache for this product
        delete_pattern_from_cache(f"products:detail:{product_id}")
        delete_pattern_from_cache("products:list:*")

        return updated_product
