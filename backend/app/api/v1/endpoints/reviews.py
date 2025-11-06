"""
Review endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.services.review_service import ReviewService
from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse,
    ReviewStats
)

router = APIRouter()


@router.get("/products/{product_id}", response_model=List[ReviewResponse])
def get_product_reviews(
    product_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(deps.get_db)
):
    """
    Get all reviews for a specific product (public)

    Args:
        product_id: ID of the product
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return

    Returns:
        List of reviews for the product
    """
    service = ReviewService(db)
    reviews = service.get_product_reviews(product_id, skip, limit)
    return reviews


@router.get("/products/{product_id}/stats", response_model=ReviewStats)
def get_product_review_stats(
    product_id: int,
    db: Session = Depends(deps.get_db)
):
    """
    Get review statistics for a product (public)

    Args:
        product_id: ID of the product

    Returns:
        Review statistics (total, average, distribution)
    """
    service = ReviewService(db)
    stats = service.get_product_stats(product_id)
    return stats


@router.get("/products/{product_id}/me", response_model=ReviewResponse, response_model_exclude_none=True)
def get_my_review_for_product(
    product_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    Get current user's review for a specific product

    Args:
        product_id: ID of the product

    Returns:
        User's review if exists, 404 otherwise
    """
    service = ReviewService(db)
    review = service.get_user_review_for_product(current_user.id, product_id)

    if not review:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You haven't reviewed this product yet"
        )

    return review


@router.get("/me", response_model=List[ReviewResponse])
def get_my_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    Get all reviews by current user

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of user's reviews
    """
    service = ReviewService(db)
    reviews = service.get_user_reviews(current_user.id, skip, limit)
    return reviews


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    review_data: ReviewCreate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    Create a new review (authenticated users only)

    Args:
        review_data: Review data (product_id, rating, title, comment)

    Returns:
        Created review
    """
    service = ReviewService(db)
    review = service.create_review(review_data, current_user.id)

    # Reload to get user relationship
    db.refresh(review)
    return review


@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(
    review_id: int,
    review_data: ReviewUpdate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    Update an existing review

    Only the review author or admin can update

    Args:
        review_id: ID of the review to update
        review_data: Updated review data

    Returns:
        Updated review
    """
    service = ReviewService(db)
    is_admin = current_user.role.value == "admin"
    review = service.update_review(review_id, review_data, current_user.id, is_admin)

    # Reload to get relationships
    db.refresh(review)
    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    Delete a review

    Only the review author or admin can delete

    Args:
        review_id: ID of the review to delete
    """
    service = ReviewService(db)
    is_admin = current_user.role.value == "admin"
    service.delete_review(review_id, current_user.id, is_admin)
    return None
