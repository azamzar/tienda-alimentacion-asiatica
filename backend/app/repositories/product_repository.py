from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from app.models.product import Product
from app.models.review import Review
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

    def search_products_advanced(
        self,
        search_query: Optional[str] = None,
        category_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[float] = None,
        in_stock_only: Optional[bool] = None,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "desc",
        skip: int = 0,
        limit: int = 100
    ) -> List[Product]:
        """
        Advanced product search with multiple filters and sorting

        Args:
            search_query: Search text (matches name and description)
            category_id: Filter by category
            min_price: Minimum price filter
            max_price: Maximum price filter
            min_rating: Minimum average rating filter
            in_stock_only: Show only products with stock > 0
            sort_by: Field to sort by (name, price, created_at, rating)
            sort_order: Sort order (asc or desc)
            skip: Pagination offset
            limit: Pagination limit

        Returns:
            List of products matching filters
        """
        # Start with base query
        query = self.db.query(Product)

        # Apply search filter (name or description)
        if search_query:
            search_filter = or_(
                Product.name.ilike(f"%{search_query}%"),
                Product.description.ilike(f"%{search_query}%")
            )
            query = query.filter(search_filter)

        # Apply category filter
        if category_id:
            query = query.filter(Product.category_id == category_id)

        # Apply price range filters
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        # Apply stock filter
        if in_stock_only:
            query = query.filter(Product.stock > 0)

        # Apply rating filter (requires subquery with reviews)
        if min_rating is not None:
            # Subquery to calculate average rating per product
            rating_subquery = (
                self.db.query(
                    Review.product_id,
                    func.avg(Review.rating).label('avg_rating')
                )
                .group_by(Review.product_id)
                .having(func.avg(Review.rating) >= min_rating)
                .subquery()
            )
            query = query.join(
                rating_subquery,
                Product.id == rating_subquery.c.product_id
            )

        # Apply sorting
        if sort_by == "name":
            sort_column = Product.name
        elif sort_by == "price":
            sort_column = Product.price
        elif sort_by == "created_at":
            sort_column = Product.created_at
        elif sort_by == "rating":
            # Sort by average rating (requires subquery)
            rating_subquery = (
                self.db.query(
                    Review.product_id,
                    func.avg(Review.rating).label('avg_rating')
                )
                .group_by(Review.product_id)
                .subquery()
            )
            query = query.outerjoin(
                rating_subquery,
                Product.id == rating_subquery.c.product_id
            )
            sort_column = rating_subquery.c.avg_rating
        else:
            sort_column = Product.created_at

        # Apply sort order
        if sort_order == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        # Apply pagination
        query = query.offset(skip).limit(limit)

        return query.all()

    def autocomplete_search(self, query: str, limit: int = 5) -> List[Product]:
        """
        Quick autocomplete search for product names
        Returns limited results for autocomplete suggestions

        Args:
            query: Search query string
            limit: Maximum number of results (default 5)

        Returns:
            List of products matching the query
        """
        return (
            self.db.query(Product)
            .filter(Product.name.ilike(f"%{query}%"))
            .order_by(Product.name.asc())
            .limit(limit)
            .all()
        )

    def get_price_range(self) -> dict:
        """
        Get the minimum and maximum prices from all products

        Returns:
            Dict with min_price and max_price
        """
        result = self.db.query(
            func.min(Product.price).label('min_price'),
            func.max(Product.price).label('max_price')
        ).first()

        return {
            'min_price': float(result.min_price) if result.min_price else 0.0,
            'max_price': float(result.max_price) if result.max_price else 100.0
        }
