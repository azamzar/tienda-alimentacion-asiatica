"""
Password Reset Token Repository.
Handles data access for password reset tokens.
"""
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.password_reset_token import PasswordResetToken
from app.repositories.base import BaseRepository


class PasswordResetTokenRepository(BaseRepository[PasswordResetToken]):
    """Repository for password reset token operations"""

    def __init__(self, db: Session):
        super().__init__(PasswordResetToken, db)

    def get_by_token(self, token: str) -> Optional[PasswordResetToken]:
        """
        Get password reset token by token string.

        Args:
            token: Token string

        Returns:
            PasswordResetToken if found, None otherwise
        """
        return self.db.query(PasswordResetToken).filter(
            PasswordResetToken.token == token
        ).first()

    def get_valid_token(self, token: str) -> Optional[PasswordResetToken]:
        """
        Get valid (not used and not expired) password reset token.

        Args:
            token: Token string

        Returns:
            PasswordResetToken if valid, None otherwise
        """
        now = datetime.utcnow()
        return self.db.query(PasswordResetToken).filter(
            PasswordResetToken.token == token,
            PasswordResetToken.used == False,
            PasswordResetToken.expires_at > now
        ).first()

    def mark_as_used(self, token_id: int) -> bool:
        """
        Mark token as used.

        Args:
            token_id: Token ID

        Returns:
            True if updated successfully, False otherwise
        """
        token = self.get_by_id(token_id)
        if token:
            token.used = True
            self.db.commit()
            return True
        return False

    def delete_expired_tokens(self) -> int:
        """
        Delete all expired tokens.

        Returns:
            Number of deleted tokens
        """
        now = datetime.utcnow()
        result = self.db.query(PasswordResetToken).filter(
            PasswordResetToken.expires_at < now
        ).delete()
        self.db.commit()
        return result

    def delete_user_tokens(self, user_id: int) -> int:
        """
        Delete all tokens for a specific user.

        Args:
            user_id: User ID

        Returns:
            Number of deleted tokens
        """
        result = self.db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user_id
        ).delete()
        self.db.commit()
        return result
