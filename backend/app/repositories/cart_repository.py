from typing import Optional, List
from sqlalchemy.orm import Session, joinedload

from app.models.cart import Cart, CartItem
from app.repositories.base import BaseRepository


class CartRepository(BaseRepository[Cart]):
    """
    Repository para operaciones de base de datos relacionadas con Carritos
    """

    def __init__(self, db: Session):
        super().__init__(Cart, db)

    def get_by_user_id(self, user_id: str) -> Optional[Cart]:
        """
        Obtiene el carrito de un usuario específico con sus items y productos

        Args:
            user_id: ID del usuario

        Returns:
            Cart si existe, None en caso contrario
        """
        return (
            self.db.query(Cart)
            .options(
                joinedload(Cart.items).joinedload(CartItem.product)
            )
            .filter(Cart.user_id == user_id)
            .first()
        )

    def get_with_items(self, cart_id: int) -> Optional[Cart]:
        """
        Obtiene un carrito con sus items y productos cargados

        Args:
            cart_id: ID del carrito

        Returns:
            Cart con items cargados si existe, None en caso contrario
        """
        return (
            self.db.query(Cart)
            .options(
                joinedload(Cart.items).joinedload(CartItem.product)
            )
            .filter(Cart.id == cart_id)
            .first()
        )

    def create_for_user(self, user_id: str) -> Cart:
        """
        Crea un nuevo carrito para un usuario

        Args:
            user_id: ID del usuario

        Returns:
            El carrito creado
        """
        cart = Cart(user_id=user_id)
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return cart


class CartItemRepository(BaseRepository[CartItem]):
    """
    Repository para operaciones de base de datos relacionadas con Items del Carrito
    """

    def __init__(self, db: Session):
        super().__init__(CartItem, db)

    def get_by_cart_and_product(self, cart_id: int, product_id: int) -> Optional[CartItem]:
        """
        Obtiene un item específico del carrito por carrito y producto

        Args:
            cart_id: ID del carrito
            product_id: ID del producto

        Returns:
            CartItem si existe, None en caso contrario
        """
        return (
            self.db.query(CartItem)
            .filter(CartItem.cart_id == cart_id, CartItem.product_id == product_id)
            .first()
        )

    def get_by_cart(self, cart_id: int) -> List[CartItem]:
        """
        Obtiene todos los items de un carrito con productos cargados

        Args:
            cart_id: ID del carrito

        Returns:
            Lista de CartItem
        """
        return (
            self.db.query(CartItem)
            .options(joinedload(CartItem.product))
            .filter(CartItem.cart_id == cart_id)
            .all()
        )

    def delete_by_cart_and_product(self, cart_id: int, product_id: int) -> bool:
        """
        Elimina un item específico del carrito

        Args:
            cart_id: ID del carrito
            product_id: ID del producto

        Returns:
            True si se eliminó, False en caso contrario
        """
        item = self.get_by_cart_and_product(cart_id, product_id)
        if item:
            self.db.delete(item)
            self.db.commit()
            return True
        return False

    def clear_cart(self, cart_id: int) -> int:
        """
        Elimina todos los items de un carrito

        Args:
            cart_id: ID del carrito

        Returns:
            Número de items eliminados
        """
        deleted_count = (
            self.db.query(CartItem)
            .filter(CartItem.cart_id == cart_id)
            .delete()
        )
        self.db.commit()
        return deleted_count
