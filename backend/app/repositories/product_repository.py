from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """Repository for Product model with specific queries"""

    def __init__(self, db: Session):
        super().__init__(Product, db)

    def get_by_category(self, category_id: int, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get all products by category"""
        return (
            self.db.query(Product)
            .filter(Product.category_id == category_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Search products by name (case-insensitive)"""
        return (
            self.db.query(Product)
            .filter(Product.name.ilike(f"%{name}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """Get products with stock below threshold"""
        return self.db.query(Product).filter(Product.stock < threshold).all()

    def get_in_stock_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get products that are in stock"""
        return (
            self.db.query(Product)
            .filter(Product.stock > 0)
            .offset(skip)
            .limit(limit)
            .all()
        )
