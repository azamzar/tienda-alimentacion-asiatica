from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate
from app.repositories.category_repository import CategoryRepository


class CategoryService:
    """Service layer for Category business logic"""

    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def get_all_categories(self) -> List[Category]:
        """Get all categories"""
        return self.repository.get_all()

    def get_category_by_id(self, category_id: int) -> Category:
        """Get a category by ID, raise 404 if not found"""
        category = self.repository.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found"
            )
        return category

    def create_category(self, category_data: CategoryCreate) -> Category:
        """Create a new category with validation"""
        # Check if category with same name already exists
        if self.repository.exists_by_name(category_data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with name '{category_data.name}' already exists"
            )

        category_dict = category_data.model_dump()
        return self.repository.create(category_dict)

    def delete_category(self, category_id: int) -> None:
        """Delete a category by ID"""
        # Verify category exists
        self.get_category_by_id(category_id)

        # Delete category
        self.repository.delete(category_id)
