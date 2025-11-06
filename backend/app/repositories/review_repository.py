"""
Review repository for data access layer
"""
from typing import List, Optional, Dict
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_
from app.models.review import Review
from app.models.user import User
from app.repositories.base import BaseRepository


class ReviewRepository(BaseRepository[Review]):
    """Repository for Review model with specialized queries"""

    def __init__(self, db: Session):
        super().__init__(Review, db)

    def get_by_product_id(
        self,
        product_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Review]:
        """
        Get all reviews for a specific product with pagination

        Args:
            product_id: ID of the product
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of reviews for the product
        """
        return (
            self.db.query(Review)
            .options(joinedload(Review.user))
            .filter(Review.product_id == product_id)
            .order_by(Review.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_user_id(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Review]:
        """
        Get all reviews written by a specific user

        Args:
            user_id: ID of the user
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of reviews by the user
        """
        return (
            self.db.query(Review)
            .options(joinedload(Review.product))
            .filter(Review.user_id == user_id)
            .order_by(Review.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

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
        return (
            self.db.query(Review)
            .filter(
                and_(
                    Review.user_id == user_id,
                    Review.product_id == product_id
                )
            )
            .first()
        )

    def get_product_stats(self, product_id: int) -> Dict:
        """
        Get review statistics for a product

        Args:
            product_id: ID of the product

        Returns:
            Dictionary with total_reviews, average_rating, and rating_distribution
        """
        # Get total count and average rating
        stats = (
            self.db.query(
                func.count(Review.id).label('total_reviews'),
                func.avg(Review.rating).label('average_rating')
            )
            .filter(Review.product_id == product_id)
            .first()
        )

        total_reviews = stats.total_reviews or 0
        average_rating = float(stats.average_rating or 0)

        # Get rating distribution
        distribution_query = (
            self.db.query(
                Review.rating,
                func.count(Review.id).label('count')
            )
            .filter(Review.product_id == product_id)
            .group_by(Review.rating)
            .all()
        )

        # Initialize distribution with 0 for all ratings
        rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for rating, count in distribution_query:
            rating_distribution[rating] = count

        return {
            'total_reviews': total_reviews,
            'average_rating': round(average_rating, 2),
            'rating_distribution': rating_distribution
        }

    def delete_user_review(self, user_id: int, product_id: int) -> bool:
        """
        Delete a user's review for a specific product

        Args:
            user_id: ID of the user
            product_id: ID of the product

        Returns:
            True if review was deleted, False if not found
        """
        review = self.get_user_review_for_product(user_id, product_id)
        if review:
            self.db.delete(review)
            self.db.commit()
            return True
        return False

    def count_by_product(self, product_id: int) -> int:
        """
        Count reviews for a specific product

        Args:
            product_id: ID of the product

        Returns:
            Number of reviews
        """
        return self.db.query(func.count(Review.id)).filter(
            Review.product_id == product_id
        ).scalar()

    def count_by_user(self, user_id: int) -> int:
        """
        Count reviews by a specific user

        Args:
            user_id: ID of the user

        Returns:
            Number of reviews
        """
        return self.db.query(func.count(Review.id)).filter(
            Review.user_id == user_id
        ).scalar()
