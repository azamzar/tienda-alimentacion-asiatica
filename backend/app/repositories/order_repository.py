from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc

from app.models.order import Order, OrderItem, OrderStatus
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """
    Repository para operaciones de base de datos relacionadas con Pedidos
    """

    def __init__(self, db: Session):
        super().__init__(Order, db)

    def get_with_items(self, order_id: int) -> Optional[Order]:
        """
        Obtiene un pedido con sus items y productos cargados

        Args:
            order_id: ID del pedido

        Returns:
            Order con items cargados si existe, None en caso contrario
        """
        return (
            self.db.query(Order)
            .options(
                joinedload(Order.items).joinedload(OrderItem.product)
            )
            .filter(Order.id == order_id)
            .first()
        )

    def get_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Order]:
        """
        Obtiene todos los pedidos de un usuario con paginación

        Args:
            user_id: ID del usuario
            skip: Número de registros a omitir
            limit: Número máximo de registros a devolver

        Returns:
            Lista de Orders
        """
        return (
            self.db.query(Order)
            .options(
                joinedload(Order.items).joinedload(OrderItem.product)
            )
            .filter(Order.user_id == user_id)
            .order_by(desc(Order.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(self, status: OrderStatus, skip: int = 0, limit: int = 100) -> List[Order]:
        """
        Obtiene pedidos por estado con paginación

        Args:
            status: Estado del pedido
            skip: Número de registros a omitir
            limit: Número máximo de registros a devolver

        Returns:
            Lista de Orders
        """
        return (
            self.db.query(Order)
            .options(
                joinedload(Order.items).joinedload(OrderItem.product)
            )
            .filter(Order.status == status)
            .order_by(desc(Order.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_by_user(self, user_id: str) -> int:
        """
        Cuenta el número de pedidos de un usuario

        Args:
            user_id: ID del usuario

        Returns:
            Número de pedidos
        """
        return self.db.query(Order).filter(Order.user_id == user_id).count()

    def count_by_status(self, status: OrderStatus) -> int:
        """
        Cuenta el número de pedidos por estado

        Args:
            status: Estado del pedido

        Returns:
            Número de pedidos
        """
        return self.db.query(Order).filter(Order.status == status).count()

    def update_status(self, order_id: int, new_status: OrderStatus) -> Optional[Order]:
        """
        Actualiza el estado de un pedido

        Args:
            order_id: ID del pedido
            new_status: Nuevo estado

        Returns:
            Order actualizado si existe, None en caso contrario
        """
        order = self.get_by_id(order_id)
        if order:
            order.status = new_status
            self.db.commit()
            self.db.refresh(order)
        return order


class OrderItemRepository(BaseRepository[OrderItem]):
    """
    Repository para operaciones de base de datos relacionadas con Items del Pedido
    """

    def __init__(self, db: Session):
        super().__init__(OrderItem, db)

    def get_by_order(self, order_id: int) -> List[OrderItem]:
        """
        Obtiene todos los items de un pedido con productos cargados

        Args:
            order_id: ID del pedido

        Returns:
            Lista de OrderItem
        """
        return (
            self.db.query(OrderItem)
            .options(joinedload(OrderItem.product))
            .filter(OrderItem.order_id == order_id)
            .all()
        )

    def bulk_create(self, order_items: List[dict]) -> List[OrderItem]:
        """
        Crea múltiples items de pedido en una transacción

        Args:
            order_items: Lista de diccionarios con datos de items

        Returns:
            Lista de OrderItem creados
        """
        items = [OrderItem(**item_data) for item_data in order_items]
        self.db.add_all(items)
        self.db.commit()
        for item in items:
            self.db.refresh(item)
        return items
