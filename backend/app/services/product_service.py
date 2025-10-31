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
        """Get all products with optional category filter"""
        if category_id:
            return self.repository.get_by_category(category_id, skip, limit)
        return self.repository.get_all(skip, limit)

    def get_product_by_id(self, product_id: int) -> Product:
        """Get a product by ID, raise 404 if not found"""
        product = self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
        return product

    def create_product(self, product_data: ProductCreate) -> Product:
        """Create a new product with validation"""
        # Validate category exists if provided
        if product_data.category_id:
            category = self.category_repository.get_by_id(product_data.category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Category with id {product_data.category_id} not found"
                )

        product_dict = product_data.model_dump()
        return self.repository.create(product_dict)

    def update_product(self, product_id: int, product_data: ProductUpdate) -> Product:
        """Update a product with validation"""
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
        return self.repository.update(db_product, update_data)

    def delete_product(self, product_id: int) -> None:
        """Delete a product by ID"""
        # Verify product exists
        self.get_product_by_id(product_id)

        # Delete product
        self.repository.delete(product_id)

    def search_products(self, name: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Search products by name"""
        return self.repository.search_by_name(name, skip, limit)

    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """Get products with low stock"""
        return self.repository.get_low_stock_products(threshold)

    async def upload_product_image(self, product_id: int, file: UploadFile) -> Product:
        """
        Upload an image for a product

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

        # Delete old image if exists
        if product.image_url:
            old_image_path = Path(settings.PRODUCTS_UPLOAD_DIR) / Path(product.image_url).name
            delete_file(old_image_path)

        # Save new image
        filename = await save_upload_file(
            file,
            settings.PRODUCTS_UPLOAD_DIR,
            settings.MAX_UPLOAD_SIZE
        )

        # Update product with new image URL
        image_url = f"/uploads/products/{filename}"
        update_data = {"image_url": image_url}
        updated_product = self.repository.update(product, update_data)

        return updated_product

    def delete_product_image(self, product_id: int) -> Product:
        """
        Delete the image of a product

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

        # Delete image file
        image_path = Path(settings.PRODUCTS_UPLOAD_DIR) / Path(product.image_url).name
        delete_file(image_path)

        # Update product (remove image_url)
        update_data = {"image_url": None}
        updated_product = self.repository.update(product, update_data)

        return updated_product
