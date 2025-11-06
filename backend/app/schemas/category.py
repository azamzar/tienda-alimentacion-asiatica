from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CategoryBase(BaseModel):
    """Base schema for Category"""
    name: str = Field(..., min_length=1, max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")


class CategoryCreate(CategoryBase):
    """Schema for creating a new category"""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating a category"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")


class Category(CategoryBase):
    """Schema for Category response"""
    id: int
    created_at: datetime
    product_count: Optional[int] = Field(None, description="Number of products in this category")

    class Config:
        from_attributes = True


class BulkDeleteRequest(BaseModel):
    """Schema for bulk delete request"""
    category_ids: List[int]

    class Config:
        json_schema_extra = {
            "example": {
                "category_ids": [1, 2, 3, 4, 5]
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
