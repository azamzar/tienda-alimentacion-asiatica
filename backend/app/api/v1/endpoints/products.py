from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter()


@router.get("/", response_model=List[Product])
def get_products(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max number of records to return"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all products with optional filtering by category.

    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return (max 100)
    - **category_id**: Optional filter by category ID
    """
    service = ProductService(db)
    return service.get_all_products(skip=skip, limit=limit, category_id=category_id)


@router.get("/search/", response_model=List[Product])
def search_products(
    name: str = Query(..., min_length=1, description="Product name to search"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Search products by name (case-insensitive).
    """
    service = ProductService(db)
    return service.search_products(name=name, skip=skip, limit=limit)


@router.get("/low-stock/", response_model=List[Product])
def get_low_stock_products(
    threshold: int = Query(10, ge=0, description="Stock threshold"),
    db: Session = Depends(get_db)
):
    """
    Get products with stock below the specified threshold.
    """
    service = ProductService(db)
    return service.get_low_stock_products(threshold=threshold)


@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get a specific product by ID.
    """
    service = ProductService(db)
    return service.get_product_by_id(product_id)


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product.
    """
    service = ProductService(db)
    return service.create_product(product)


@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a product.
    """
    service = ProductService(db)
    return service.update_product(product_id, product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product by ID.
    """
    service = ProductService(db)
    service.delete_product(product_id)
    return None
