"""
Review schemas for request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict
from datetime import datetime


# Base schema with common fields
class ReviewBase(BaseModel):
    """Base review schema with common fields"""
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")
    title: Optional[str] = Field(None, max_length=200, description="Optional review title")
    comment: Optional[str] = Field(None, max_length=2000, description="Optional review text")

    @validator('rating')
    def validate_rating(cls, v):
        if not 1 <= v <= 5:
            raise ValueError('Rating must be between 1 and 5')
        return v


# Schema for creating a review
class ReviewCreate(ReviewBase):
    """Schema for creating a new review"""
    product_id: int = Field(..., gt=0, description="ID of the product being reviewed")


# Schema for updating a review
class ReviewUpdate(BaseModel):
    """Schema for updating an existing review"""
    rating: Optional[int] = Field(None, ge=1, le=5, description="Updated rating")
    title: Optional[str] = Field(None, max_length=200, description="Updated title")
    comment: Optional[str] = Field(None, max_length=2000, description="Updated comment")

    @validator('rating')
    def validate_rating(cls, v):
        if v is not None and not 1 <= v <= 5:
            raise ValueError('Rating must be between 1 and 5')
        return v


# Schema for review in database (internal use)
class ReviewInDB(ReviewBase):
    """Schema for review in database"""
    id: int
    product_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Schema for user info in review response
class ReviewUserInfo(BaseModel):
    """User information for review response"""
    id: int
    full_name: Optional[str]
    email: str

    class Config:
        from_attributes = True


# Schema for review response (includes user info)
class ReviewResponse(ReviewInDB):
    """Schema for review response with user information"""
    user: ReviewUserInfo

    class Config:
        from_attributes = True


# Schema for review statistics
class ReviewStats(BaseModel):
    """Statistics for product reviews"""
    total_reviews: int = Field(..., description="Total number of reviews")
    average_rating: float = Field(..., description="Average rating (0-5)")
    rating_distribution: Dict[int, int] = Field(
        ...,
        description="Distribution of ratings (1-5 stars: count)"
    )

    class Config:
        schema_extra = {
            "example": {
                "total_reviews": 42,
                "average_rating": 4.5,
                "rating_distribution": {
                    1: 2,
                    2: 3,
                    3: 5,
                    4: 12,
                    5: 20
                }
            }
        }
