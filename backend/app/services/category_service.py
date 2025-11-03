from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.repositories.category_repository import CategoryRepository
from app.utils.cache import (
    get_from_cache,
    set_in_cache,
    delete_pattern_from_cache,
    get_cache_key
)


class CategoryService:
    """Service layer for Category business logic"""

    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def get_all_categories(self) -> List[Category]:
        """Get all categories (cached)"""
        # Build cache key
        cache_key = get_cache_key("categories", "list")

        # Try to get from cache
        cached_data = get_from_cache(cache_key)
        if cached_data is not None:
            return [Category(**item) for item in cached_data]

        # Get from database
        categories = self.repository.get_all()

        # Cache the result
        if categories:
            cache_data = [
                {k: v for k, v in c.__dict__.items() if not k.startswith('_')}
                for c in categories
            ]
            set_in_cache(cache_key, cache_data, ttl=600)  # 10 minutes

        return categories

    def get_category_by_id(self, category_id: int) -> Category:
        """Get a category by ID, raise 404 if not found (cached)"""
        # Build cache key
        cache_key = get_cache_key("categories", "detail", str(category_id))

        # Try to get from cache
        cached_data = get_from_cache(cache_key)
        if cached_data is not None:
            return Category(**cached_data)

        # Get from database
        category = self.repository.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found"
            )

        # Cache the result
        cache_data = {k: v for k, v in category.__dict__.items() if not k.startswith('_')}
        set_in_cache(cache_key, cache_data, ttl=600)  # 10 minutes

        return category

    def create_category(self, category_data: CategoryCreate) -> Category:
        """Create a new category with validation and cache invalidation"""
        # Check if category with same name already exists
        if self.repository.exists_by_name(category_data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with name '{category_data.name}' already exists"
            )

        category_dict = category_data.model_dump()
        category = self.repository.create(category_dict)

        # Invalidate categories cache
        delete_pattern_from_cache("categories:*")
        # Also invalidate product lists since categories affect product queries
        delete_pattern_from_cache("products:list:*")

        return category

    def update_category(self, category_id: int, category_data: CategoryUpdate) -> Category:
        """Update a category by ID with cache invalidation"""
        # Verify category exists
        category = self.get_category_by_id(category_id)

        # If name is being changed, check if new name already exists
        if category_data.name and category_data.name != category.name:
            if self.repository.exists_by_name(category_data.name):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Category with name '{category_data.name}' already exists"
                )

        # Update category
        update_dict = category_data.model_dump(exclude_unset=True)
        updated_category = self.repository.update(category, update_dict)

        # Invalidate cache
        delete_pattern_from_cache("categories:*")
        delete_pattern_from_cache("products:list:*")

        return updated_category

    def delete_category(self, category_id: int) -> None:
        """Delete a category by ID with cache invalidation"""
        # Verify category exists
        self.get_category_by_id(category_id)

        # Delete category
        self.repository.delete(category_id)

        # Invalidate cache
        delete_pattern_from_cache("categories:*")
        delete_pattern_from_cache("products:list:*")
