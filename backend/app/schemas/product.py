from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.schemas.category import Category


class ProductBase(BaseModel):
    """Base schema for Product"""
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., gt=0, description="Product price (must be greater than 0)")
    image_url: Optional[str] = Field(None, max_length=500, description="Product image URL")
    stock: int = Field(default=0, ge=0, description="Product stock quantity")
    category_id: Optional[int] = Field(None, description="Category ID")


class ProductCreate(ProductBase):
    """Schema for creating a new product"""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    image_url: Optional[str] = Field(None, max_length=500)
    stock: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None


class Product(ProductBase):
    """Schema for Product response"""
    id: int
    created_at: datetime
    updated_at: datetime
    category: Optional[Category] = None

    class Config:
        from_attributes = True


# Alias for compatibility
ProductResponse = Product


class ProductWithReviews(Product):
    """Schema for Product with review statistics"""
    average_rating: Optional[float] = Field(None, description="Average rating (0-5)")
    total_reviews: Optional[int] = Field(None, description="Total number of reviews")

    class Config:
        from_attributes = True


class BulkDeleteRequest(BaseModel):
    """Schema for bulk delete request"""
    product_ids: List[int]

    class Config:
        json_schema_extra = {
            "example": {
                "product_ids": [1, 2, 3, 4, 5]
            }
        }


class BulkUpdateRequest(BaseModel):
    """Schema for bulk update request"""
    product_ids: List[int]
    update_data: ProductUpdate

    class Config:
        json_schema_extra = {
            "example": {
                "product_ids": [1, 2, 3],
                "update_data": {
                    "stock": 100,
                    "category_id": 2
                }
            }
        }


class BulkOperationResponse(BaseModel):
    """Schema for bulk operation response"""
    success_count: int
    error_count: int
    total: int
    errors: Optional[List[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success_count": 3,
                "error_count": 0,
                "total": 3,
                "errors": None
            }
        }
