from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.services.cart_service import CartService
from app.schemas.cart import CartResponse, AddToCartRequest, UpdateCartItemRequest
from app.models.user import User


router = APIRouter()


@router.get("/me", response_model=CartResponse, status_code=status.HTTP_200_OK)
def get_cart(
    db: Annotated[Session, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene el carrito del usuario autenticado

    **Requires authentication** - El user_id se obtiene del token JWT
    """
    service = CartService(db)
    # Usar el ID del usuario autenticado como string
    return service.get_cart(str(current_user.id))


@router.post("/me/items", response_model=CartResponse, status_code=status.HTTP_200_OK)
def add_to_cart(
    request: AddToCartRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    """
    Agrega un producto al carrito del usuario autenticado

    **Requires authentication**

    - **product_id**: ID del producto a agregar
    - **quantity**: Cantidad a agregar (default: 1)
    """
    service = CartService(db)
    return service.add_to_cart(str(current_user.id), request)


@router.put("/me/items/{product_id}", response_model=CartResponse, status_code=status.HTTP_200_OK)
def update_cart_item(
    product_id: int,
    request: UpdateCartItemRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    """
    Actualiza la cantidad de un producto en el carrito del usuario autenticado

    **Requires authentication**

    - **product_id**: ID del producto a actualizar
    - **quantity**: Nueva cantidad
    """
    service = CartService(db)
    return service.update_cart_item(str(current_user.id), product_id, request)


@router.delete("/me/items/{product_id}", response_model=CartResponse, status_code=status.HTTP_200_OK)
def remove_from_cart(
    product_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    """
    Elimina un producto del carrito del usuario autenticado

    **Requires authentication**

    - **product_id**: ID del producto a eliminar
    """
    service = CartService(db)
    return service.remove_from_cart(str(current_user.id), product_id)


@router.delete("/me", status_code=status.HTTP_200_OK)
def clear_cart(
    db: Annotated[Session, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    """
    Vacía el carrito del usuario autenticado

    **Requires authentication**
    """
    service = CartService(db)
    return service.clear_cart(str(current_user.id))
