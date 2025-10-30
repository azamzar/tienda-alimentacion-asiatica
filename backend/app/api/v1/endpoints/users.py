from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_admin
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService


router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    role: Optional[str] = Query(None, description="Filter by role (customer/admin)"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Get all users with optional filters.

    **Requires admin role**

    Query Parameters:
    - skip: Number of records to skip (default: 0)
    - limit: Maximum number of records to return (default: 100, max: 100)
    - role: Filter by role (customer/admin)
    - is_active: Filter by active status (true/false)
    """
    service = UserService(db)
    return service.get_all_users(skip=skip, limit=limit, role=role, is_active=is_active)


@router.get("/stats")
def get_user_stats(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Get user statistics.

    **Requires admin role**

    Returns:
    - total: Total number of users
    - active: Number of active users
    - inactive: Number of inactive users
    - admins: Number of admin users
    - customers: Number of customer users
    """
    service = UserService(db)
    return service.get_users_count()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Get user by ID.

    **Requires admin role**
    """
    service = UserService(db)
    return service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Update user by ID.

    **Requires admin role**

    Allows updating:
    - email (must be unique)
    - full_name
    - password (will be hashed)
    - is_active (activate/deactivate user)
    """
    service = UserService(db)
    return service.update_user(user_id, user_data)


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Soft delete user by setting is_active to False.

    **Requires admin role**

    Note: Admin users cannot be deleted for security reasons.
    """
    service = UserService(db)
    return service.delete_user(user_id)
