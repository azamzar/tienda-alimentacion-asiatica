"""
Wishlist service with business logic
"""
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.wishlist import WishlistItem
from app.repositories.wishlist_repository import WishlistRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.wishlist import WishlistItemCreate


class WishlistService:
    """Service for wishlist business logic"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = WishlistRepository(db)
        self.product_repository = ProductRepository(db)

    def add_to_wishlist(
        self,
        user_id: int,
        product_id: int
    ) -> WishlistItem:
        """
        Add a product to user's wishlist

        Args:
            user_id: ID of the user
            product_id: ID of the product

        Returns:
            Created wishlist item

        Raises:
            HTTPException: If product doesn't exist or already in wishlist
        """
        # Check if product exists
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )

        # Check if already in wishlist
        existing = self.repository.get_user_wishlist_item(user_id, product_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product already in wishlist"
            )

        # Add to wishlist
        wishlist_item = self.repository.create({
            'user_id': user_id,
            'product_id': product_id
        })

        return wishlist_item

    def remove_from_wishlist(
        self,
        user_id: int,
        product_id: int
    ) -> bool:
        """
        Remove a product from user's wishlist

        Args:
            user_id: ID of the user
            product_id: ID of the product

        Returns:
            True if removed successfully

        Raises:
            HTTPException: If product not in wishlist
        """
        deleted = self.repository.delete_user_wishlist_item(user_id, product_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not in wishlist"
            )
        return True

    def get_user_wishlist(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[WishlistItem]:
        """
        Get all items in user's wishlist

        Args:
            user_id: ID of the user
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of wishlist items with product details
        """
        return self.repository.get_user_wishlist(user_id, skip, limit)

    def is_in_wishlist(
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
            True if product is in wishlist
        """
        return self.repository.is_product_in_wishlist(user_id, product_id)

    def clear_wishlist(self, user_id: int) -> int:
        """
        Remove all items from user's wishlist

        Args:
            user_id: ID of the user

        Returns:
            Number of items removed
        """
        return self.repository.clear_user_wishlist(user_id)

    def get_wishlist_count(self, user_id: int) -> int:
        """
        Get count of items in user's wishlist

        Args:
            user_id: ID of the user

        Returns:
            Number of wishlist items
        """
        return self.repository.count_user_wishlist(user_id)

    def bulk_add_to_wishlist(
        self,
        user_id: int,
        product_ids: List[int]
    ) -> dict:
        """
        Add multiple products to wishlist

        Args:
            user_id: ID of the user
            product_ids: List of product IDs

        Returns:
            Dictionary with added and failed product IDs
        """
        added = []
        already_exists = []
        not_found = []

        for product_id in product_ids:
            # Check if product exists
            product = self.product_repository.get_by_id(product_id)
            if not product:
                not_found.append(product_id)
                continue

            # Check if already in wishlist
            existing = self.repository.get_user_wishlist_item(user_id, product_id)
            if existing:
                already_exists.append(product_id)
                continue

            # Add to wishlist
            try:
                self.repository.create({
                    'user_id': user_id,
                    'product_id': product_id
                })
                added.append(product_id)
            except Exception:
                continue

        return {
            'added': added,
            'already_exists': already_exists,
            'not_found': not_found,
            'total_added': len(added)
        }
