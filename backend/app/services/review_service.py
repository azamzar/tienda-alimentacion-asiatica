"""
Review service with business logic
"""
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.review import Review
from app.models.user import User, UserRole
from app.repositories.review_repository import ReviewRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse, ReviewStats


class ReviewService:
    """Service for review business logic"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = ReviewRepository(db)
        self.product_repository = ProductRepository(db)

    def create_review(
        self,
        review_data: ReviewCreate,
        user_id: int
    ) -> Review:
        """
        Create a new review

        Args:
            review_data: Review data
            user_id: ID of the user creating the review

        Returns:
            Created review

        Raises:
            HTTPException: If product doesn't exist or user already reviewed it
        """
        # Check if product exists
        product = self.product_repository.get_by_id(review_data.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {review_data.product_id} not found"
            )

        # Check if user already reviewed this product
        existing_review = self.repository.get_user_review_for_product(
            user_id=user_id,
            product_id=review_data.product_id
        )
        if existing_review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already reviewed this product. Use update instead."
            )

        # Create review
        review_dict = review_data.dict()
        review_dict['user_id'] = user_id

        review = self.repository.create(review_dict)
        return review

    def update_review(
        self,
        review_id: int,
        review_data: ReviewUpdate,
        user_id: int,
        is_admin: bool = False
    ) -> Review:
        """
        Update an existing review

        Args:
            review_id: ID of the review to update
            review_data: Updated review data
            user_id: ID of the user updating the review
            is_admin: Whether the user is an admin

        Returns:
            Updated review

        Raises:
            HTTPException: If review doesn't exist or user is not authorized
        """
        review = self.repository.get_by_id(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Review with id {review_id} not found"
            )

        # Only the review author or admin can update
        if review.user_id != user_id and not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to update this review"
            )

        # Update only provided fields
        update_data = review_data.dict(exclude_unset=True)
        updated_review = self.repository.update(review, update_data)

        return updated_review

    def delete_review(
        self,
        review_id: int,
        user_id: int,
        is_admin: bool = False
    ) -> bool:
        """
        Delete a review

        Args:
            review_id: ID of the review to delete
            user_id: ID of the user deleting the review
            is_admin: Whether the user is an admin

        Returns:
            True if deleted successfully

        Raises:
            HTTPException: If review doesn't exist or user is not authorized
        """
        review = self.repository.get_by_id(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Review with id {review_id} not found"
            )

        # Only the review author or admin can delete
        if review.user_id != user_id and not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to delete this review"
            )

        return self.repository.delete(review_id)

    def get_product_reviews(
        self,
        product_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Review]:
        """
        Get all reviews for a product

        Args:
            product_id: ID of the product
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of reviews

        Raises:
            HTTPException: If product doesn't exist
        """
        # Check if product exists
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )

        return self.repository.get_by_product_id(product_id, skip, limit)

    def get_user_reviews(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Review]:
        """
        Get all reviews by a user

        Args:
            user_id: ID of the user
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of reviews
        """
        return self.repository.get_by_user_id(user_id, skip, limit)

    def get_product_stats(self, product_id: int) -> Dict:
        """
        Get review statistics for a product

        Args:
            product_id: ID of the product

        Returns:
            Dictionary with review statistics

        Raises:
            HTTPException: If product doesn't exist
        """
        # Check if product exists
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )

        return self.repository.get_product_stats(product_id)

    def get_user_review_for_product(
        self,
        user_id: int,
        product_id: int
    ) -> Optional[Review]:
        """
        Get a user's review for a specific product

        Args:
            user_id: ID of the user
            product_id: ID of the product

        Returns:
            Review if exists, None otherwise
        """
        return self.repository.get_user_review_for_product(user_id, product_id)

    def get_review_by_id(self, review_id: int) -> Review:
        """
        Get a review by ID

        Args:
            review_id: ID of the review

        Returns:
            Review object

        Raises:
            HTTPException: If review doesn't exist
        """
        review = self.repository.get_by_id(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Review with id {review_id} not found"
            )
        return review
