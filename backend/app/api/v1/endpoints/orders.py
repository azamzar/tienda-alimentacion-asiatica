from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import csv
import io
from datetime import datetime

from app.api.deps import get_db, get_current_user, get_current_admin
from app.services.order_service import OrderService
from app.schemas.order import (
    OrderResponse,
    CreateOrderFromCartRequest,
    OrderUpdate,
    OrderStatusEnum
)
from app.models.user import User, UserRole


router = APIRouter()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order_from_cart(
    request: CreateOrderFromCartRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    """
    Crea un pedido a partir del carrito del usuario autenticado

    **Requires authentication**

    - **customer_name**: Nombre del cliente
    - **customer_email**: Email del cliente
    - **customer_phone**: Teléfono del cliente
    - **shipping_address**: Dirección de envío
    - **notes**: Notas adicionales (opcional)

    El pedido se crea tomando todos los productos del carrito actual,
    se valida el stock, se reduce el inventario y se vacía el carrito.
    """
    service = OrderService(db)
    return service.create_order_from_cart(str(current_user.id), request)


@router.get("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def get_order(
    order_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene un pedido por ID

    **Requires authentication**

    - **order_id**: ID del pedido

    Los clientes solo pueden ver sus propios pedidos.
    Los admins pueden ver cualquier pedido.
    """
    service = OrderService(db)
    # Si es admin, puede ver cualquier pedido (user_id=None)
    # Si es cliente, solo puede ver sus propios pedidos
    user_id_filter = None if current_user.role == UserRole.ADMIN else str(current_user.id)
    return service.get_order(order_id, user_id_filter)


@router.get("/", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
def get_orders(
    status_filter: Optional[OrderStatusEnum] = Query(None, alias="status", description="Filtrar por estado"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista pedidos del usuario autenticado con filtros opcionales

    **Requires authentication**

    - **status**: Filtrar por estado (pending, confirmed, processing, shipped, delivered, cancelled)
    - **skip**: Número de registros a omitir (paginación)
    - **limit**: Número máximo de registros a devolver (máx: 100)

    Los clientes solo ven sus propios pedidos.
    Los admins ven todos los pedidos de todos los usuarios.
    """
    service = OrderService(db)

    # Si es admin, puede ver todos los pedidos
    if current_user.role == UserRole.ADMIN:
        if status_filter:
            return service.get_orders_by_status(status_filter, skip, limit)
        else:
            return service.get_all_orders(skip, limit)
    else:
        # Si es cliente, solo ve sus propios pedidos
        return service.get_user_orders(str(current_user.id), skip, limit)


@router.patch("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def update_order(
    order_id: int,
    request: OrderUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    """
    Actualiza un pedido

    **Requires authentication**

    - **order_id**: ID del pedido
    - **status**: Nuevo estado del pedido (solo admins)
    - Otros campos del pedido (información del cliente)

    Los clientes solo pueden actualizar sus propios pedidos y solo campos básicos.
    Los admins pueden cambiar el estado y actualizar cualquier pedido.
    Los cambios de estado tienen validaciones de negocio.
    """
    service = OrderService(db)
    # Si es admin, puede actualizar cualquier pedido
    # Si es cliente, solo puede actualizar sus propios pedidos
    user_id_filter = None if current_user.role == UserRole.ADMIN else str(current_user.id)
    return service.update_order(order_id, request, user_id_filter)


@router.post("/{order_id}/cancel", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def cancel_order(
    order_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    """
    Cancela un pedido y restaura el stock

    **Requires authentication**

    - **order_id**: ID del pedido a cancelar

    Solo se pueden cancelar pedidos en estados: pending, confirmed, processing.
    El stock se restaura automáticamente.

    Los clientes solo pueden cancelar sus propios pedidos.
    Los admins pueden cancelar cualquier pedido.
    """
    service = OrderService(db)
    # Si es admin, puede cancelar cualquier pedido
    # Si es cliente, solo puede cancelar sus propios pedidos
    user_id_filter = None if current_user.role == UserRole.ADMIN else str(current_user.id)
    return service.cancel_order(order_id, user_id_filter)


@router.get("/export/csv", status_code=status.HTTP_200_OK)
def export_orders_csv(
    status_filter: Optional[OrderStatusEnum] = Query(None, alias="status", description="Filtrar por estado"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Exporta todos los pedidos a un archivo CSV

    **Requires admin role**

    - **status**: Filtrar por estado (pending, confirmed, processing, shipped, delivered, cancelled)

    Genera un archivo CSV con todos los pedidos del sistema con la siguiente estructura:
    - Order ID, Date, Customer Name, Customer Email, Customer Phone, Status, Total Amount, Items
    """
    service = OrderService(db)

    # Obtener todos los pedidos (sin límite de paginación para exportación)
    if status_filter:
        orders = service.get_orders_by_status(status_filter, skip=0, limit=100000)
    else:
        orders = service.get_all_orders(skip=0, limit=100000)

    # Crear CSV en memoria
    output = io.StringIO()
    writer = csv.writer(output)

    # Escribir encabezados
    writer.writerow([
        'Order ID',
        'Date',
        'Customer Name',
        'Customer Email',
        'Customer Phone',
        'Shipping Address',
        'Status',
        'Total Amount',
        'Items Count',
        'Notes'
    ])

    # Escribir datos de pedidos
    for order in orders:
        writer.writerow([
            order.id,
            order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            order.customer_name,
            order.customer_email,
            order.customer_phone,
            order.shipping_address,
            order.status.value,
            f"{order.total_amount:.2f}",
            len(order.items),
            order.notes or ''
        ])

    # Preparar la respuesta
    output.seek(0)

    # Generar nombre de archivo con timestamp
    filename = f"orders_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
