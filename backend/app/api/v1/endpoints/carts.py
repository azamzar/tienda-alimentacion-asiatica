from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.cart_service import CartService
from app.schemas.cart import CartResponse, AddToCartRequest, UpdateCartItemRequest


router = APIRouter()


@router.get("/{user_id}", response_model=CartResponse, status_code=status.HTTP_200_OK)
def get_cart(
    user_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Obtiene el carrito de un usuario

    - **user_id**: ID del usuario (puede ser un UUID temporal o ID de usuario autenticado)
    """
    service = CartService(db)
    return service.get_cart(user_id)


@router.post("/{user_id}/items", response_model=CartResponse, status_code=status.HTTP_200_OK)
def add_to_cart(
    user_id: str,
    request: AddToCartRequest,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Agrega un producto al carrito

    - **user_id**: ID del usuario
    - **product_id**: ID del producto a agregar
    - **quantity**: Cantidad a agregar (default: 1)
    """
    service = CartService(db)
    return service.add_to_cart(user_id, request)


@router.put("/{user_id}/items/{product_id}", response_model=CartResponse, status_code=status.HTTP_200_OK)
def update_cart_item(
    user_id: str,
    product_id: int,
    request: UpdateCartItemRequest,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Actualiza la cantidad de un producto en el carrito

    - **user_id**: ID del usuario
    - **product_id**: ID del producto a actualizar
    - **quantity**: Nueva cantidad
    """
    service = CartService(db)
    return service.update_cart_item(user_id, product_id, request)


@router.delete("/{user_id}/items/{product_id}", response_model=CartResponse, status_code=status.HTTP_200_OK)
def remove_from_cart(
    user_id: str,
    product_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Elimina un producto del carrito

    - **user_id**: ID del usuario
    - **product_id**: ID del producto a eliminar
    """
    service = CartService(db)
    return service.remove_from_cart(user_id, product_id)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def clear_cart(
    user_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Vacía el carrito del usuario

    - **user_id**: ID del usuario
    """
    service = CartService(db)
    return service.clear_cart(user_id)
