from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.cart_repository import CartRepository, CartItemRepository
from app.repositories.product_repository import ProductRepository
from app.models.cart import Cart, CartItem
from app.schemas.cart import CartResponse, AddToCartRequest, UpdateCartItemRequest


class CartService:
    """
    Servicio de lógica de negocio para Carritos de Compra
    """

    def __init__(self, db: Session):
        self.db = db
        self.cart_repo = CartRepository(db)
        self.cart_item_repo = CartItemRepository(db)
        self.product_repo = ProductRepository(db)

    def get_or_create_cart(self, user_id: str) -> Cart:
        """
        Obtiene el carrito de un usuario o lo crea si no existe

        Args:
            user_id: ID del usuario

        Returns:
            Cart del usuario
        """
        cart = self.cart_repo.get_by_user_id(user_id)
        if not cart:
            cart = self.cart_repo.create_for_user(user_id)
        return cart

    def get_cart(self, user_id: str) -> CartResponse:
        """
        Obtiene el carrito de un usuario con cálculos de totales

        Args:
            user_id: ID del usuario

        Returns:
            CartResponse con información completa del carrito

        Raises:
            HTTPException: Si el carrito no existe
        """
        cart = self.cart_repo.get_by_user_id(user_id)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Carrito no encontrado para el usuario {user_id}"
            )

        return self._build_cart_response(cart)

    def add_to_cart(self, user_id: str, request: AddToCartRequest) -> CartResponse:
        """
        Agrega un producto al carrito del usuario

        Args:
            user_id: ID del usuario
            request: Datos del producto a agregar

        Returns:
            CartResponse actualizado

        Raises:
            HTTPException: Si el producto no existe o no hay stock suficiente
        """
        # Verificar que el producto existe
        product = self.product_repo.get_by_id(request.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {request.product_id} no encontrado"
            )

        # Verificar stock disponible
        if product.stock < request.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente. Disponible: {product.stock}, solicitado: {request.quantity}"
            )

        # Obtener o crear carrito
        cart = self.get_or_create_cart(user_id)

        # Verificar si el producto ya está en el carrito
        existing_item = self.cart_item_repo.get_by_cart_and_product(cart.id, request.product_id)

        if existing_item:
            # Actualizar cantidad
            new_quantity = existing_item.quantity + request.quantity

            # Verificar stock para la nueva cantidad
            if product.stock < new_quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuficiente. Disponible: {product.stock}, en carrito: {existing_item.quantity}, solicitado: {request.quantity}"
                )

            existing_item.quantity = new_quantity
            self.db.commit()
            self.db.refresh(existing_item)
        else:
            # Crear nuevo item
            new_item = CartItem(
                cart_id=cart.id,
                product_id=request.product_id,
                quantity=request.quantity
            )
            self.db.add(new_item)
            self.db.commit()
            self.db.refresh(new_item)

        # Refrescar y retornar carrito actualizado
        cart = self.cart_repo.get_with_items(cart.id)
        return self._build_cart_response(cart)

    def update_cart_item(self, user_id: str, product_id: int, request: UpdateCartItemRequest) -> CartResponse:
        """
        Actualiza la cantidad de un producto en el carrito

        Args:
            user_id: ID del usuario
            product_id: ID del producto
            request: Nueva cantidad

        Returns:
            CartResponse actualizado

        Raises:
            HTTPException: Si el carrito, producto o item no existen, o no hay stock suficiente
        """
        # Obtener carrito
        cart = self.cart_repo.get_by_user_id(user_id)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Carrito no encontrado para el usuario {user_id}"
            )

        # Obtener producto
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {product_id} no encontrado"
            )

        # Verificar stock
        if product.stock < request.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente. Disponible: {product.stock}, solicitado: {request.quantity}"
            )

        # Obtener item del carrito
        cart_item = self.cart_item_repo.get_by_cart_and_product(cart.id, product_id)
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto {product_id} no encontrado en el carrito"
            )

        # Actualizar cantidad
        cart_item.quantity = request.quantity
        self.db.commit()
        self.db.refresh(cart_item)

        # Refrescar y retornar carrito actualizado
        cart = self.cart_repo.get_with_items(cart.id)
        return self._build_cart_response(cart)

    def remove_from_cart(self, user_id: str, product_id: int) -> CartResponse:
        """
        Elimina un producto del carrito

        Args:
            user_id: ID del usuario
            product_id: ID del producto a eliminar

        Returns:
            CartResponse actualizado

        Raises:
            HTTPException: Si el carrito o item no existen
        """
        # Obtener carrito
        cart = self.cart_repo.get_by_user_id(user_id)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Carrito no encontrado para el usuario {user_id}"
            )

        # Eliminar item
        deleted = self.cart_item_repo.delete_by_cart_and_product(cart.id, product_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto {product_id} no encontrado en el carrito"
            )

        # Refrescar y retornar carrito actualizado
        cart = self.cart_repo.get_with_items(cart.id)
        return self._build_cart_response(cart)

    def clear_cart(self, user_id: str) -> dict:
        """
        Vacía el carrito del usuario

        Args:
            user_id: ID del usuario

        Returns:
            Mensaje de confirmación

        Raises:
            HTTPException: Si el carrito no existe
        """
        # Obtener carrito
        cart = self.cart_repo.get_by_user_id(user_id)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Carrito no encontrado para el usuario {user_id}"
            )

        # Limpiar items
        deleted_count = self.cart_item_repo.clear_cart(cart.id)

        return {
            "message": "Carrito vaciado exitosamente",
            "items_removed": deleted_count
        }

    def _build_cart_response(self, cart: Cart) -> CartResponse:
        """
        Construye la respuesta del carrito con cálculos de totales

        Args:
            cart: Objeto Cart con items cargados

        Returns:
            CartResponse con totales calculados
        """
        total_items = sum(item.quantity for item in cart.items)
        total_amount = sum(item.quantity * item.product.price for item in cart.items)

        cart_dict = {
            "id": cart.id,
            "user_id": cart.user_id,
            "created_at": cart.created_at,
            "updated_at": cart.updated_at,
            "items": cart.items,
            "total_items": total_items,
            "total_amount": round(total_amount, 2)
        }

        return CartResponse(**cart_dict)
