from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional

from app.schemas.product import ProductResponse


# ============ CartItem Schemas ============

class CartItemBase(BaseModel):
    """Schema base para items del carrito"""
    product_id: int = Field(..., gt=0, description="ID del producto")
    quantity: int = Field(..., gt=0, description="Cantidad del producto")


class CartItemCreate(CartItemBase):
    """Schema para crear/actualizar un item en el carrito"""
    pass


class CartItemUpdate(BaseModel):
    """Schema para actualizar la cantidad de un item"""
    quantity: int = Field(..., gt=0, description="Nueva cantidad del producto")


class CartItemResponse(CartItemBase):
    """Schema de respuesta para items del carrito"""
    id: int
    cart_id: int
    added_at: datetime
    product: ProductResponse  # Información completa del producto
    subtotal: float = Field(default=0.0, description="Subtotal del item (quantity * product.price)")

    model_config = ConfigDict(from_attributes=True)


# ============ Cart Schemas ============

class CartBase(BaseModel):
    """Schema base para carritos"""
    user_id: str = Field(..., min_length=1, max_length=255, description="ID del usuario")


class CartCreate(CartBase):
    """Schema para crear un carrito"""
    pass


class CartResponse(CartBase):
    """Schema de respuesta para carritos"""
    id: int
    created_at: datetime
    updated_at: datetime
    items: List[CartItemResponse] = []
    total_items: int = Field(default=0, description="Cantidad total de items en el carrito")
    total_amount: float = Field(default=0.0, description="Monto total del carrito")

    model_config = ConfigDict(from_attributes=True)


class CartSummary(BaseModel):
    """Schema resumido del carrito (sin detalles de productos)"""
    id: int
    user_id: str
    total_items: int
    total_amount: float
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============ Request Schemas ============

class AddToCartRequest(BaseModel):
    """Request para agregar un producto al carrito"""
    product_id: int = Field(..., gt=0, description="ID del producto a agregar")
    quantity: int = Field(default=1, gt=0, description="Cantidad a agregar")


class UpdateCartItemRequest(BaseModel):
    """Request para actualizar la cantidad de un item"""
    quantity: int = Field(..., gt=0, description="Nueva cantidad")
