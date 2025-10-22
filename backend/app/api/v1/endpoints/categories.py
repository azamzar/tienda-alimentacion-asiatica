from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.category import Category, CategoryCreate
from app.services.category_service import CategoryService

router = APIRouter()


@router.get("/", response_model=List[Category])
def get_categories(db: Session = Depends(get_db)):
    """
    Retrieve all categories.
    """
    service = CategoryService(db)
    return service.get_all_categories()


@router.get("/{category_id}", response_model=Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """
    Get a specific category by ID.
    """
    service = CategoryService(db)
    return service.get_category_by_id(category_id)


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new category.
    """
    service = CategoryService(db)
    return service.create_category(category)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    Delete a category by ID.
    """
    service = CategoryService(db)
    service.delete_category(category_id)
    return None
