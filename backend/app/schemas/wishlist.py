"""
Wishlist schemas for request/response validation
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schemas.product import Product


# Base schema
class WishlistItemBase(BaseModel):
    """Base wishlist item schema"""
    product_id: int


# Schema for creating wishlist item
class WishlistItemCreate(WishlistItemBase):
    """Schema for adding product to wishlist"""
    pass


# Schema for wishlist item in database
class WishlistItemInDB(WishlistItemBase):
    """Schema for wishlist item in database"""
    id: int
    user_id: int
    added_at: datetime

    class Config:
        from_attributes = True


# Schema for wishlist item response (with product info)
class WishlistItemResponse(WishlistItemInDB):
    """Schema for wishlist item response with product details"""
    product: Product

    class Config:
        from_attributes = True


# Schema for batch operations
class WishlistBulkAdd(BaseModel):
    """Schema for adding multiple products to wishlist"""
    product_ids: list[int]

    class Config:
        schema_extra = {
            "example": {
                "product_ids": [1, 2, 3, 4, 5]
            }
        }
