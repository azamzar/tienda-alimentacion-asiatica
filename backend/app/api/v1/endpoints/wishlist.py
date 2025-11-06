"""
Wishlist endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.services.wishlist_service import WishlistService
from app.schemas.wishlist import (
    WishlistItemCreate,
    WishlistItemResponse,
    WishlistBulkAdd
)

router = APIRouter()


@router.get("/me", response_model=List[WishlistItemResponse])
def get_my_wishlist(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    Get current user's wishlist

    Returns all products in the user's wishlist with full product details.
    """
    service = WishlistService(db)
    wishlist_items = service.get_user_wishlist(current_user.id, skip, limit)
    return wishlist_items


@router.get("/me/count", response_model=dict)
def get_my_wishlist_count(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    Get count of items in current user's wishlist

    Returns:
        {"count": number}
    """
    service = WishlistService(db)
    count = service.get_wishlist_count(current_user.id)
    return {"count": count}


@router.get("/me/check/{product_id}", response_model=dict)
def check_product_in_wishlist(
    product_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    Check if a product is in current user's wishlist

    Args:
        product_id: ID of the product to check

    Returns:
        {"in_wishlist": boolean}
    """
    service = WishlistService(db)
    in_wishlist = service.is_in_wishlist(current_user.id, product_id)
    return {"in_wishlist": in_wishlist}


@router.post("/me", response_model=WishlistItemResponse, status_code=status.HTTP_201_CREATED)
def add_to_wishlist(
    wishlist_item: WishlistItemCreate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    Add a product to current user's wishlist

    Args:
        wishlist_item: Product ID to add

    Returns:
        Created wishlist item with product details
    """
    service = WishlistService(db)
    item = service.add_to_wishlist(current_user.id, wishlist_item.product_id)

    # Reload to get product relationship
    db.refresh(item)
    return item


@router.post("/me/bulk", response_model=dict)
def bulk_add_to_wishlist(
    bulk_request: WishlistBulkAdd,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    Add multiple products to wishlist

    Args:
        bulk_request: List of product IDs

    Returns:
        Summary of operation with added, already_exists, and not_found lists
    """
    service = WishlistService(db)
    result = service.bulk_add_to_wishlist(current_user.id, bulk_request.product_ids)
    return result


@router.delete("/me/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_wishlist(
    product_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    Remove a product from current user's wishlist

    Args:
        product_id: ID of the product to remove
    """
    service = WishlistService(db)
    service.remove_from_wishlist(current_user.id, product_id)
    return None


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def clear_wishlist(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    Remove all items from current user's wishlist

    Returns count of items removed in response headers.
    """
    service = WishlistService(db)
    count = service.clear_wishlist(current_user.id)
    return None
