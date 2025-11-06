"""
Wishlist model - User's favorite products
"""
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base


class WishlistItem(Base):
    """
    Wishlist item model for user's favorite products

    Attributes:
        id: Primary key
        user_id: Foreign key to users table
        product_id: Foreign key to products table
        added_at: Timestamp when product was added to wishlist

    Relationships:
        user: User who added the product
        product: Product in wishlist
    """
    __tablename__ = "wishlist_items"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)

    # Timestamp
    added_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="wishlist_items")
    product = relationship("Product", back_populates="wishlist_items")

    # Constraints
    __table_args__ = (
        # One product per user in wishlist (unique constraint)
        Index('idx_user_product_wishlist_unique', 'user_id', 'product_id', unique=True),
        # Index for queries
        Index('idx_user_wishlist', 'user_id'),
    )

    def __repr__(self):
        return f"<WishlistItem(id={self.id}, user_id={self.user_id}, product_id={self.product_id})>"
