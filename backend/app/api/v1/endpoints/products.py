from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status, UploadFile, File
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_admin
from app.schemas.product import Product, ProductCreate, ProductUpdate, BulkDeleteRequest, BulkUpdateRequest, BulkOperationResponse
from app.services.product_service import ProductService
from app.models.user import User

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
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Create a new product.

    **Requires admin role**
    """
    service = ProductService(db)
    return service.create_product(product)


@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Update a product.

    **Requires admin role**
    """
    service = ProductService(db)
    return service.update_product(product_id, product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Delete a product by ID.

    **Requires admin role**
    """
    service = ProductService(db)
    service.delete_product(product_id)
    return None


@router.post("/{product_id}/image", response_model=Product)
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Upload an image for a product.

    **Requires admin role**

    - **product_id**: ID of the product
    - **file**: Image file (JPG, PNG, GIF, WEBP, max 5MB)
    """
    service = ProductService(db)
    return await service.upload_product_image(product_id, file)


@router.delete("/{product_id}/image", response_model=Product)
def delete_product_image(
    product_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Delete the image of a product.

    **Requires admin role**
    """
    service = ProductService(db)
    return service.delete_product_image(product_id)


@router.post("/bulk/delete", response_model=BulkOperationResponse)
def bulk_delete_products(
    request: BulkDeleteRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Delete multiple products at once.

    **Requires admin role**

    - **product_ids**: List of product IDs to delete

    Returns:
    - success_count: Number of products successfully deleted
    - error_count: Number of errors encountered
    - total: Total products attempted
    - errors: List of error messages (if any)
    """
    service = ProductService(db)
    return service.bulk_delete_products(request.product_ids)


@router.patch("/bulk/update", response_model=BulkOperationResponse)
def bulk_update_products(
    request: BulkUpdateRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Update multiple products at once with the same values.

    **Requires admin role**

    - **product_ids**: List of product IDs to update
    - **update_data**: Data to update (can include: stock, price, category_id, etc.)

    Returns:
    - success_count: Number of products successfully updated
    - error_count: Number of errors encountered
    - total: Total products attempted
    - errors: List of error messages (if any)
    """
    service = ProductService(db)
    update_dict = request.update_data.model_dump(exclude_unset=True)
    return service.bulk_update_products(request.product_ids, update_dict)
