from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_admin
from app.schemas.category import Category, CategoryCreate, CategoryUpdate
from app.services.category_service import CategoryService
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[Category])
def get_categories(db: Session = Depends(get_db)):
    """
    Retrieve all categories.

    **Public endpoint** - No authentication required
    """
    service = CategoryService(db)
    return service.get_all_categories()


@router.get("/{category_id}", response_model=Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """
    Get a specific category by ID.

    **Public endpoint** - No authentication required
    """
    service = CategoryService(db)
    return service.get_category_by_id(category_id)


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Create a new category.

    **Requires admin role**
    """
    service = CategoryService(db)
    return service.create_category(category)


@router.put("/{category_id}", response_model=Category)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Update a category by ID.

    **Requires admin role**
    """
    service = CategoryService(db)
    return service.update_category(category_id, category)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Delete a category by ID.

    **Requires admin role**
    """
    service = CategoryService(db)
    service.delete_category(category_id)
    return None
