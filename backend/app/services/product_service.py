from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository


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
