import React, { useState } from 'react';
import { formatPrice } from '../../utils/formatters';
import './CartItem.css';

/**
 * Componente para mostrar un item individual del carrito
 * @param {Object} item - Item del carrito con {product, quantity, subtotal}
 * @param {Function} onUpdateQuantity - Callback para actualizar cantidad
 * @param {Function} onRemove - Callback para eliminar item
 */
const CartItem = ({ item, onUpdateQuantity, onRemove, loading }) => {
  const [localQuantity, setLocalQuantity] = useState(item.quantity);
  const [isUpdating, setIsUpdating] = useState(false);

  const handleQuantityChange = async (newQuantity) => {
    if (newQuantity < 1) return;
    if (newQuantity > item.product.stock) {
      alert(`Solo hay ${item.product.stock} unidades disponibles`);
      return;
    }

    setLocalQuantity(newQuantity);
    setIsUpdating(true);

    try {
      await onUpdateQuantity(item.product.id, newQuantity);
    } catch (error) {
      // Revertir en caso de error
      setLocalQuantity(item.quantity);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleRemove = async () => {
    setIsUpdating(true);
    try {
      await onRemove(item.product.id);
    } catch (error) {
      setIsUpdating(false);
    }
  };

  const isDisabled = loading || isUpdating;

  return (
    <div className={`cart-item ${isDisabled ? 'cart-item--disabled' : ''}`}>
      {/* Imagen del producto */}
      <div className="cart-item__image">
        {item.product.image_url ? (
          <img src={item.product.image_url} alt={item.product.name} />
        ) : (
          <div className="cart-item__image-placeholder">
            📦
          </div>
        )}
      </div>

      {/* Información del producto */}
      <div className="cart-item__info">
        <h3 className="cart-item__name">{item.product.name}</h3>
        <p className="cart-item__price">{formatPrice(item.product.price)} / unidad</p>
        {item.product.stock < 10 && (
          <p className="cart-item__stock-warning">
            ⚠️ Solo quedan {item.product.stock} unidades
          </p>
        )}
      </div>

      {/* Controles de cantidad */}
      <div className="cart-item__quantity">
        <button
          className="cart-item__qty-btn"
          onClick={() => handleQuantityChange(localQuantity - 1)}
          disabled={isDisabled || localQuantity <= 1}
          aria-label="Disminuir cantidad"
        >
          -
        </button>
        <span className="cart-item__qty-value">{localQuantity}</span>
        <button
          className="cart-item__qty-btn"
          onClick={() => handleQuantityChange(localQuantity + 1)}
          disabled={isDisabled || localQuantity >= item.product.stock}
          aria-label="Aumentar cantidad"
        >
          +
        </button>
      </div>

      {/* Subtotal */}
      <div className="cart-item__subtotal">
        <p className="cart-item__subtotal-label">Subtotal</p>
        <p className="cart-item__subtotal-price">{formatPrice(item.subtotal)}</p>
      </div>

      {/* Botón eliminar */}
      <button
        className="cart-item__remove"
        onClick={handleRemove}
        disabled={isDisabled}
        aria-label="Eliminar producto"
        title="Eliminar producto"
      >
        🗑️
      </button>
    </div>
  );
};

export default CartItem;
