from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.order_repository import OrderRepository, OrderItemRepository
from app.repositories.cart_repository import CartRepository, CartItemRepository
from app.repositories.product_repository import ProductRepository
from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderUpdate,
    OrderSummary,
    CreateOrderFromCartRequest,
    OrderStatusEnum
)


class OrderService:
    """
    Servicio de lógica de negocio para Pedidos
    """

    def __init__(self, db: Session):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.order_item_repo = OrderItemRepository(db)
        self.cart_repo = CartRepository(db)
        self.cart_item_repo = CartItemRepository(db)
        self.product_repo = ProductRepository(db)

    def create_order_from_cart(self, user_id: str, request: CreateOrderFromCartRequest) -> OrderResponse:
        """
        Crea un pedido a partir del carrito del usuario

        Args:
            user_id: ID del usuario
            request: Datos del pedido (información del cliente)

        Returns:
            OrderResponse con el pedido creado

        Raises:
            HTTPException: Si el carrito no existe, está vacío o hay problemas de stock
        """
        # Obtener carrito del usuario
        cart = self.cart_repo.get_by_user_id(user_id)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Carrito no encontrado para el usuario {user_id}"
            )

        if not cart.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El carrito está vacío. No se puede crear un pedido."
            )

        # Validar stock y calcular total
        order_items_data = []
        total_amount = 0.0

        for cart_item in cart.items:
            product = cart_item.product

            # Verificar stock disponible
            if product.stock < cart_item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuficiente para '{product.name}'. Disponible: {product.stock}, solicitado: {cart_item.quantity}"
                )

            # Calcular subtotal
            subtotal = cart_item.quantity * product.price
            total_amount += subtotal

            # Preparar datos del item del pedido
            order_items_data.append({
                "product_id": product.id,
                "quantity": cart_item.quantity,
                "unit_price": product.price,
                "subtotal": subtotal
            })

        # Crear el pedido
        order = Order(
            user_id=user_id,
            status=OrderStatus.PENDING,
            total_amount=round(total_amount, 2),
            customer_name=request.customer_name,
            customer_email=request.customer_email,
            customer_phone=request.customer_phone,
            shipping_address=request.shipping_address,
            notes=request.notes
        )

        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)

        # Crear los items del pedido
        for item_data in order_items_data:
            item_data["order_id"] = order.id

        self.order_item_repo.bulk_create(order_items_data)

        # Reducir el stock de los productos
        for cart_item in cart.items:
            product = cart_item.product
            product.stock -= cart_item.quantity

        # Limpiar el carrito
        self.cart_item_repo.clear_cart(cart.id)

        self.db.commit()

        # Obtener el pedido completo con items
        order = self.order_repo.get_with_items(order.id)
        return self._build_order_response(order)

    def get_order(self, order_id: int, user_id: Optional[str] = None) -> OrderResponse:
        """
        Obtiene un pedido por ID

        Args:
            order_id: ID del pedido
            user_id: ID del usuario (para validar propiedad)

        Returns:
            OrderResponse con información completa del pedido

        Raises:
            HTTPException: Si el pedido no existe o no pertenece al usuario
        """
        order = self.order_repo.get_with_items(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido con ID {order_id} no encontrado"
            )

        # Validar que el pedido pertenece al usuario (si se proporciona user_id)
        if user_id and order.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver este pedido"
            )

        return self._build_order_response(order)

    def get_user_orders(self, user_id: str, skip: int = 0, limit: int = 100) -> List[OrderResponse]:
        """
        Obtiene todos los pedidos de un usuario

        Args:
            user_id: ID del usuario
            skip: Número de registros a omitir
            limit: Número máximo de registros

        Returns:
            Lista de OrderResponse
        """
        orders = self.order_repo.get_by_user_id(user_id, skip, limit)
        return [self._build_order_response(order) for order in orders]

    def get_orders_by_status(self, status: OrderStatusEnum, skip: int = 0, limit: int = 100) -> List[OrderResponse]:
        """
        Obtiene pedidos filtrados por estado

        Args:
            status: Estado del pedido
            skip: Número de registros a omitir
            limit: Número máximo de registros

        Returns:
            Lista de OrderResponse
        """
        # Convertir de OrderStatusEnum a OrderStatus
        order_status = OrderStatus(status.value)
        orders = self.order_repo.get_by_status(order_status, skip, limit)
        return [self._build_order_response(order) for order in orders]

    def update_order(self, order_id: int, request: OrderUpdate, user_id: Optional[str] = None) -> OrderResponse:
        """
        Actualiza un pedido

        Args:
            order_id: ID del pedido
            request: Datos a actualizar
            user_id: ID del usuario (para validar propiedad en cambios no-admin)

        Returns:
            OrderResponse actualizado

        Raises:
            HTTPException: Si el pedido no existe o hay conflictos de validación
        """
        order = self.order_repo.get_with_items(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido con ID {order_id} no encontrado"
            )

        # Validar propiedad para cambios de información del cliente
        if user_id and order.user_id != user_id:
            # Solo permitir cambio de estado si es admin (sin user_id)
            if request.customer_name or request.customer_email or request.customer_phone or request.shipping_address:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permiso para modificar este pedido"
                )

        # Validar cambios de estado
        if request.status:
            # Convertir de OrderStatusEnum a OrderStatus
            new_status = OrderStatus(request.status.value)

            # Validaciones de negocio para cambios de estado
            if order.status == OrderStatus.CANCELLED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se puede modificar un pedido cancelado"
                )

            if order.status == OrderStatus.DELIVERED and new_status != OrderStatus.DELIVERED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se puede cambiar el estado de un pedido ya entregado"
                )

            order.status = new_status

        # Actualizar otros campos
        update_data = request.model_dump(exclude_unset=True, exclude={"status"})
        for field, value in update_data.items():
            setattr(order, field, value)

        self.db.commit()
        self.db.refresh(order)

        order = self.order_repo.get_with_items(order_id)
        return self._build_order_response(order)

    def cancel_order(self, order_id: int, user_id: Optional[str] = None) -> OrderResponse:
        """
        Cancela un pedido y restaura el stock

        Args:
            order_id: ID del pedido
            user_id: ID del usuario (para validar propiedad)

        Returns:
            OrderResponse del pedido cancelado

        Raises:
            HTTPException: Si el pedido no existe, no puede cancelarse, etc.
        """
        order = self.order_repo.get_with_items(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido con ID {order_id} no encontrado"
            )

        # Validar propiedad
        if user_id and order.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para cancelar este pedido"
            )

        # Validar que se puede cancelar
        if order.status == OrderStatus.CANCELLED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El pedido ya está cancelado"
            )

        if order.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede cancelar un pedido en estado '{order.status.value}'"
            )

        # Restaurar stock
        for order_item in order.items:
            product = order_item.product
            product.stock += order_item.quantity

        # Cambiar estado a cancelado
        order.status = OrderStatus.CANCELLED
        self.db.commit()
        self.db.refresh(order)

        order = self.order_repo.get_with_items(order_id)
        return self._build_order_response(order)

    def _build_order_response(self, order: Order) -> OrderResponse:
        """
        Construye la respuesta del pedido

        Args:
            order: Objeto Order con items cargados

        Returns:
            OrderResponse
        """
        return OrderResponse.model_validate(order)
