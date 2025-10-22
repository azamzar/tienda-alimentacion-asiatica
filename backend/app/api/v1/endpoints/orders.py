from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.order_service import OrderService
from app.schemas.order import (
    OrderResponse,
    CreateOrderFromCartRequest,
    OrderUpdate,
    OrderStatusEnum
)


router = APIRouter()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order_from_cart(
    user_id: Annotated[str, Query(..., description="ID del usuario")],
    request: CreateOrderFromCartRequest,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Crea un pedido a partir del carrito del usuario

    - **user_id**: ID del usuario (query parameter)
    - **customer_name**: Nombre del cliente
    - **customer_email**: Email del cliente
    - **customer_phone**: Teléfono del cliente
    - **shipping_address**: Dirección de envío
    - **notes**: Notas adicionales (opcional)

    El pedido se crea tomando todos los productos del carrito actual,
    se valida el stock, se reduce el inventario y se vacía el carrito.
    """
    service = OrderService(db)
    return service.create_order_from_cart(user_id, request)


@router.get("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def get_order(
    order_id: int,
    user_id: Annotated[Optional[str], Query(None, description="ID del usuario (para validación)")] = None,
    db: Annotated[Session, Depends(get_db)] = Depends(get_db)
):
    """
    Obtiene un pedido por ID

    - **order_id**: ID del pedido
    - **user_id**: ID del usuario (opcional, para validar propiedad)
    """
    service = OrderService(db)
    return service.get_order(order_id, user_id)


@router.get("/", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
def get_orders(
    user_id: Annotated[Optional[str], Query(None, description="Filtrar por usuario")] = None,
    status_filter: Annotated[Optional[OrderStatusEnum], Query(None, alias="status", description="Filtrar por estado")] = None,
    skip: Annotated[int, Query(0, ge=0)] = 0,
    limit: Annotated[int, Query(100, ge=1, le=100)] = 100,
    db: Annotated[Session, Depends(get_db)] = Depends(get_db)
):
    """
    Lista pedidos con filtros opcionales

    - **user_id**: Filtrar pedidos de un usuario específico
    - **status**: Filtrar por estado (pending, confirmed, processing, shipped, delivered, cancelled)
    - **skip**: Número de registros a omitir (paginación)
    - **limit**: Número máximo de registros a devolver (máx: 100)
    """
    service = OrderService(db)

    if user_id:
        return service.get_user_orders(user_id, skip, limit)
    elif status_filter:
        return service.get_orders_by_status(status_filter, skip, limit)
    else:
        # Si no hay filtros, devolver lista vacía o implementar get_all
        return []


@router.patch("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def update_order(
    order_id: int,
    request: OrderUpdate,
    user_id: Annotated[Optional[str], Query(None, description="ID del usuario (para validación)")] = None,
    db: Annotated[Session, Depends(get_db)] = Depends(get_db)
):
    """
    Actualiza un pedido

    - **order_id**: ID del pedido
    - **user_id**: ID del usuario (para validar propiedad en cambios no-admin)
    - **status**: Nuevo estado del pedido
    - Otros campos del pedido (información del cliente)

    Los cambios de estado tienen validaciones de negocio.
    """
    service = OrderService(db)
    return service.update_order(order_id, request, user_id)


@router.post("/{order_id}/cancel", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def cancel_order(
    order_id: int,
    user_id: Annotated[Optional[str], Query(None, description="ID del usuario (para validación)")] = None,
    db: Annotated[Session, Depends(get_db)] = Depends(get_db)
):
    """
    Cancela un pedido y restaura el stock

    - **order_id**: ID del pedido a cancelar
    - **user_id**: ID del usuario (para validar propiedad)

    Solo se pueden cancelar pedidos en estados: pending, confirmed, processing.
    El stock se restaura automáticamente.
    """
    service = OrderService(db)
    return service.cancel_order(order_id, user_id)
