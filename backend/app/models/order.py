from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.models.base import Base


class OrderStatus(str, enum.Enum):
    """
    Estados posibles de un pedido
    """
    PENDING = "pending"           # Pedido creado, pendiente de confirmación
    CONFIRMED = "confirmed"       # Pedido confirmado
    PROCESSING = "processing"     # En proceso de preparación
    SHIPPED = "shipped"           # Enviado
    DELIVERED = "delivered"       # Entregado
    CANCELLED = "cancelled"       # Cancelado


class Order(Base):
    """
    Modelo de Pedido

    Representa un pedido realizado por un usuario
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), nullable=False, index=True)
    status = Column(SQLEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING, index=True)
    total_amount = Column(Float, nullable=False)

    # Información del cliente
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=False)
    customer_phone = Column(String(50), nullable=False)
    shipping_address = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, status={self.status}, total={self.total_amount})>"


class OrderItem(Base):
    """
    Modelo de Item del Pedido

    Representa un producto en un pedido con su cantidad y precio en el momento de la compra
    """
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)  # Precio en el momento de la compra
    subtotal = Column(Float, nullable=False)    # quantity * unit_price

    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product")

    def __repr__(self):
        return f"<OrderItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity}, subtotal={self.subtotal})>"
