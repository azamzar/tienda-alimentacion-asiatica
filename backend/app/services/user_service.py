from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.schemas.user import UserUpdate, UserResponse
from app.repositories.user_repository import UserRepository
from app.core.security import get_password_hash


class UserService:
    """Service for user management operations"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def get_all_users(
        self,
        skip: int = 0,
        limit: int = 100,
        role: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[User]:
        """
        Get all users with optional filters

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            role: Filter by role (customer/admin)
            is_active: Filter by active status

        Returns:
            List of users
        """
        query = self.db.query(User)

        # Apply filters
        if role is not None:
            try:
                role_enum = UserRole(role)
                query = query.filter(User.role == role_enum)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid role: {role}. Must be 'customer' or 'admin'"
                )

        if is_active is not None:
            query = query.filter(User.is_active == is_active)

        # Order by created_at descending
        query = query.order_by(User.created_at.desc())

        return query.offset(skip).limit(limit).all()

    def get_user_by_id(self, user_id: int) -> User:
        """
        Get user by ID

        Args:
            user_id: User ID

        Returns:
            User

        Raises:
            HTTPException: If user not found
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return user

    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """
        Update user by ID

        Args:
            user_id: User ID
            user_data: Updated user data

        Returns:
            Updated user

        Raises:
            HTTPException: If user not found or email already exists
        """
        user = self.get_user_by_id(user_id)

        # Check if email is being changed and if it already exists
        if user_data.email and user_data.email != user.email:
            if self.repository.email_exists(user_data.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email '{user_data.email}' is already registered"
                )

        # Prepare update dictionary
        update_dict = user_data.model_dump(exclude_unset=True)

        # Hash password if it's being updated
        if 'password' in update_dict and update_dict['password']:
            update_dict['hashed_password'] = get_password_hash(update_dict['password'])
            del update_dict['password']

        return self.repository.update(user, update_dict)

    def delete_user(self, user_id: int) -> User:
        """
        Soft delete user by setting is_active to False

        Args:
            user_id: User ID

        Returns:
            Deactivated user

        Raises:
            HTTPException: If user not found or trying to delete admin
        """
        user = self.get_user_by_id(user_id)

        # Prevent deleting admin users (optional - remove if you want to allow it)
        if user.role == UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot delete admin users"
            )

        # Soft delete by setting is_active to False
        return self.repository.update(user, {"is_active": False})

    def get_users_count(self) -> dict:
        """
        Get statistics about users

        Returns:
            Dictionary with user counts
        """
        total_users = self.db.query(User).count()
        active_users = self.db.query(User).filter(User.is_active == True).count()
        inactive_users = total_users - active_users
        admin_users = self.db.query(User).filter(User.role == UserRole.ADMIN).count()
        customer_users = self.db.query(User).filter(User.role == UserRole.CUSTOMER).count()

        return {
            "total": total_users,
            "active": active_users,
            "inactive": inactive_users,
            "admins": admin_users,
            "customers": customer_users
        }
