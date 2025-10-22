from typing import Optional
from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """Repository for Category model with specific queries"""

    def __init__(self, db: Session):
        super().__init__(Category, db)

    def get_by_name(self, name: str) -> Optional[Category]:
        """Get a category by name"""
        return self.db.query(Category).filter(Category.name == name).first()

    def exists_by_name(self, name: str) -> bool:
        """Check if a category exists by name"""
        return self.db.query(Category).filter(Category.name == name).first() is not None
