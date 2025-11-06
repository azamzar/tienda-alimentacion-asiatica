"""
Wishlist repository for data access layer
"""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from app.models.wishlist import WishlistItem
from app.repositories.base import BaseRepository


class WishlistRepository(BaseRepository[WishlistItem]):
    """Repository for WishlistItem model with specialized queries"""

    def __init__(self, db: Session):
        super().__init__(WishlistItem, db)

    def get_user_wishlist(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[WishlistItem]:
        """
        Get all wishlist items for a user with product details

        Args:
            user_id: ID of the user
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of wishlist items with products loaded
        """
        return (
            self.db.query(WishlistItem)
            .options(joinedload(WishlistItem.product).joinedload('category'))
            .filter(WishlistItem.user_id == user_id)
            .order_by(WishlistItem.added_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_user_wishlist_item(
        self,
        user_id: int,
        product_id: int
    ) -> Optional[WishlistItem]:
        """
        Get a specific wishlist item for a user

        Args:
            user_id: ID of the user
            product_id: ID of the product

        Returns:
            WishlistItem if exists, None otherwise
        """
        return (
            self.db.query(WishlistItem)
            .filter(
                and_(
                    WishlistItem.user_id == user_id,
                    WishlistItem.product_id == product_id
                )
            )
            .first()
        )

    def delete_user_wishlist_item(
        self,
        user_id: int,
        product_id: int
    ) -> bool:
        """
        Delete a wishlist item for a user

        Args:
            user_id: ID of the user
            product_id: ID of the product

        Returns:
            True if item was deleted, False if not found
        """
        item = self.get_user_wishlist_item(user_id, product_id)
        if item:
            self.db.delete(item)
            self.db.commit()
            return True
        return False

    def count_user_wishlist(self, user_id: int) -> int:
        """
        Count wishlist items for a user

        Args:
            user_id: ID of the user

        Returns:
            Number of wishlist items
        """
        return (
            self.db.query(WishlistItem)
            .filter(WishlistItem.user_id == user_id)
            .count()
        )

    def is_product_in_wishlist(
        self,
        user_id: int,
        product_id: int
    ) -> bool:
        """
        Check if a product is in user's wishlist

        Args:
            user_id: ID of the user
            product_id: ID of the product

        Returns:
            True if product is in wishlist, False otherwise
        """
        return self.get_user_wishlist_item(user_id, product_id) is not None

    def clear_user_wishlist(self, user_id: int) -> int:
        """
        Remove all items from user's wishlist

        Args:
            user_id: ID of the user

        Returns:
            Number of items deleted
        """
        count = (
            self.db.query(WishlistItem)
            .filter(WishlistItem.user_id == user_id)
            .delete()
        )
        self.db.commit()
        return count
