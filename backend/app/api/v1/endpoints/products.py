from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import csv
import io
from datetime import datetime

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


@router.get("/advanced-search/", response_model=List[Product])
def advanced_search_products(
    search_query: Optional[str] = Query(None, description="Search in name and description"),
    category_id: Optional[int] = Query(None, description="Filter by category"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    min_rating: Optional[float] = Query(None, ge=1, le=5, description="Minimum average rating (1-5)"),
    in_stock_only: Optional[bool] = Query(None, description="Show only in-stock products"),
    sort_by: Optional[str] = Query("created_at", description="Sort by: name, price, created_at, rating"),
    sort_order: Optional[str] = Query("desc", description="Sort order: asc or desc"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Advanced product search with multiple filters and sorting.

    **Filters:**
    - **search_query**: Search text in product name and description
    - **category_id**: Filter by category
    - **min_price** / **max_price**: Price range filter
    - **min_rating**: Minimum average rating (1-5 stars)
    - **in_stock_only**: Show only products with stock > 0

    **Sorting:**
    - **sort_by**: Field to sort (name, price, created_at, rating)
    - **sort_order**: asc (ascending) or desc (descending)
    """
    service = ProductService(db)
    return service.search_products_advanced(
        search_query=search_query,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        in_stock_only=in_stock_only,
        sort_by=sort_by,
        sort_order=sort_order,
        skip=skip,
        limit=limit
    )


@router.get("/autocomplete/", response_model=List[Product])
def autocomplete_products(
    q: str = Query(..., min_length=2, description="Search query (min 2 characters)"),
    limit: int = Query(5, ge=1, le=10, description="Max suggestions to return"),
    db: Session = Depends(get_db)
):
    """
    Quick autocomplete search for product suggestions.

    Returns a limited number of products matching the query.
    Ideal for real-time search suggestions.

    - **q**: Search query string (minimum 2 characters)
    - **limit**: Maximum number of suggestions (default 5, max 10)
    """
    service = ProductService(db)
    return service.autocomplete_search(query=q, limit=limit)


@router.get("/price-range/")
def get_price_range(db: Session = Depends(get_db)):
    """
    Get the minimum and maximum prices from all products.

    Useful for setting up price range sliders in the frontend.

    **Returns:**
    ```json
    {
        "min_price": 0.99,
        "max_price": 99.99
    }
    ```
    """
    service = ProductService(db)
    return service.get_price_range()


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


@router.get("/export/csv", status_code=status.HTTP_200_OK)
def export_products_csv(
    category_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Exporta todos los productos a un archivo CSV

    **Requires admin role**

    - **category_id**: Filtrar por categoría (opcional)

    Genera un archivo CSV con todos los productos del sistema con la siguiente estructura:
    - Product ID, Name, Description, Price, Stock, Category, Image URL, Created At, Updated At
    """
    service = ProductService(db)

    # Obtener todos los productos (sin límite de paginación para exportación)
    if category_id:
        products = service.get_products_by_category(category_id)
    else:
        products = service.get_products(skip=0, limit=100000)

    # Crear CSV en memoria
    output = io.StringIO()
    writer = csv.writer(output)

    # Escribir encabezados
    writer.writerow([
        'Product ID',
        'Name',
        'Description',
        'Price',
        'Stock',
        'Category',
        'Image URL',
        'Created At',
        'Updated At'
    ])

    # Escribir datos de productos
    for product in products:
        writer.writerow([
            product.id,
            product.name,
            product.description or '',
            f"{product.price:.2f}",
            product.stock,
            product.category.name if product.category else 'Sin categoría',
            product.image_url or '',
            product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            product.updated_at.strftime('%Y-%m-%d %H:%M:%S') if product.updated_at else ''
        ])

    # Preparar la respuesta
    output.seek(0)

    # Generar nombre de archivo con timestamp
    filename = f"products_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
