from pydantic import BaseModel, Field
from typing import Optional
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
