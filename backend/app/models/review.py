"""
Review model - Product reviews and ratings
"""
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, CheckConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base


class Review(Base):
    """
    Review model for product reviews and ratings

    Attributes:
        id: Primary key
        product_id: Foreign key to products table
        user_id: Foreign key to users table
        rating: Rating from 1 to 5 stars
        title: Optional review title
        comment: Optional review text
        created_at: Timestamp when review was created
        updated_at: Timestamp when review was last updated

    Relationships:
        product: Product being reviewed
        user: User who wrote the review
    """
    __tablename__ = "reviews"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Review data
    rating = Column(Integer, nullable=False)  # 1-5 stars
    title = Column(String(200), nullable=True)
    comment = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    product = relationship("Product", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    # Constraints
    __table_args__ = (
        # Rating must be between 1 and 5
        CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range_check'),
        # One review per user per product
        Index('idx_user_product_unique', 'user_id', 'product_id', unique=True),
        # Index for queries
        Index('idx_product_rating', 'product_id', 'rating'),
    )

    def __repr__(self):
        return f"<Review(id={self.id}, product_id={self.product_id}, user_id={self.user_id}, rating={self.rating})>"
