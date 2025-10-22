from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime
from typing import List, Optional
from enum import Enum

from app.schemas.product import ProductResponse


# ============ Enums ============

class OrderStatusEnum(str, Enum):
    """Estados posibles de un pedido"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# ============ OrderItem Schemas ============

class OrderItemBase(BaseModel):
    """Schema base para items del pedido"""
    product_id: int = Field(..., gt=0, description="ID del producto")
    quantity: int = Field(..., gt=0, description="Cantidad del producto")
    unit_price: float = Field(..., gt=0, description="Precio unitario en el momento de la compra")
    subtotal: float = Field(..., gt=0, description="Subtotal del item")


class OrderItemCreate(BaseModel):
    """Schema interno para crear items de pedido"""
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float


class OrderItemResponse(OrderItemBase):
    """Schema de respuesta para items del pedido"""
    id: int
    order_id: int
    product: ProductResponse  # Información completa del producto

    model_config = ConfigDict(from_attributes=True)


# ============ Order Schemas ============

class OrderBase(BaseModel):
    """Schema base para pedidos"""
    customer_name: str = Field(..., min_length=1, max_length=255, description="Nombre del cliente")
    customer_email: EmailStr = Field(..., description="Email del cliente")
    customer_phone: str = Field(..., min_length=1, max_length=50, description="Teléfono del cliente")
    shipping_address: str = Field(..., min_length=1, description="Dirección de envío")
    notes: Optional[str] = Field(None, description="Notas adicionales del pedido")


class OrderCreate(OrderBase):
    """Schema para crear un pedido"""
    user_id: str = Field(..., min_length=1, max_length=255, description="ID del usuario")
    # Los items se tomarán del carrito del usuario


class OrderUpdate(BaseModel):
    """Schema para actualizar un pedido"""
    status: Optional[OrderStatusEnum] = Field(None, description="Nuevo estado del pedido")
    customer_name: Optional[str] = Field(None, min_length=1, max_length=255)
    customer_email: Optional[EmailStr] = None
    customer_phone: Optional[str] = Field(None, min_length=1, max_length=50)
    shipping_address: Optional[str] = Field(None, min_length=1)
    notes: Optional[str] = None


class OrderResponse(OrderBase):
    """Schema de respuesta para pedidos"""
    id: int
    user_id: str
    status: OrderStatusEnum
    total_amount: float
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes=True)


class OrderSummary(BaseModel):
    """Schema resumido del pedido (sin items detallados)"""
    id: int
    user_id: str
    status: OrderStatusEnum
    total_amount: float
    customer_name: str
    created_at: datetime
    updated_at: datetime
    total_items: int = Field(default=0, description="Cantidad total de items")

    model_config = ConfigDict(from_attributes=True)


# ============ Request Schemas ============

class CreateOrderFromCartRequest(OrderBase):
    """Request para crear un pedido desde el carrito"""
    pass  # Hereda todos los campos de OrderBase
