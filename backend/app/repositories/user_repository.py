from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model with custom queries"""

    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address

        Args:
            email: User email address

        Returns:
            User if found, None otherwise
        """
        return self.db.query(User).filter(User.email == email).first()

    def email_exists(self, email: str) -> bool:
        """
        Check if email already exists

        Args:
            email: Email to check

        Returns:
            True if email exists, False otherwise
        """
        return self.db.query(User).filter(User.email == email).first() is not None

    def get_active_users(self, skip: int = 0, limit: int = 100):
        """
        Get all active users

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of active users
        """
        return (
            self.db.query(User)
            .filter(User.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
