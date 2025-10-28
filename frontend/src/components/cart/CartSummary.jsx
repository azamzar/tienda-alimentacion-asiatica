import React from 'react';
import { useNavigate } from 'react-router-dom';
import { formatPrice } from '../../utils/formatters';
import Button from '../common/Button';
import './CartSummary.css';

/**
 * Componente para mostrar el resumen del carrito con totales y botón de checkout
 * @param {number} totalItems - Cantidad total de items
 * @param {number} totalAmount - Monto total
 * @param {boolean} loading - Estado de carga
 * @param {Function} onClearCart - Callback para vaciar carrito
 */
const CartSummary = ({ totalItems, totalAmount, loading, onClearCart }) => {
  const navigate = useNavigate();

  const handleCheckout = () => {
    navigate('/checkout');
  };

  const handleClear = async () => {
    if (window.confirm('¿Estás seguro de que quieres vaciar el carrito?')) {
      try {
        await onClearCart();
      } catch (error) {
        console.error('Error al vaciar carrito:', error);
      }
    }
  };

  // Calcular estimación de envío (ejemplo: gratis si > 50€, sino 5€)
  const shippingCost = totalAmount >= 50 ? 0 : 5;
  const total = totalAmount + shippingCost;

  return (
    <div className="cart-summary">
      <h2 className="cart-summary__title">Resumen del Pedido</h2>

      <div className="cart-summary__items">
        <div className="cart-summary__row">
          <span className="cart-summary__label">Productos ({totalItems})</span>
          <span className="cart-summary__value">{formatPrice(totalAmount)}</span>
        </div>

        <div className="cart-summary__row">
          <span className="cart-summary__label">Envío</span>
          <span className="cart-summary__value">
            {shippingCost === 0 ? (
              <span className="cart-summary__free">GRATIS</span>
            ) : (
              formatPrice(shippingCost)
            )}
          </span>
        </div>

        {totalAmount < 50 && totalAmount > 0 && (
          <div className="cart-summary__shipping-info">
            <p>🎉 Envío gratis a partir de {formatPrice(50)}</p>
            <p>Te faltan {formatPrice(50 - totalAmount)} para envío gratis</p>
          </div>
        )}

        <div className="cart-summary__divider"></div>

        <div className="cart-summary__row cart-summary__row--total">
          <span className="cart-summary__label">Total</span>
          <span className="cart-summary__value cart-summary__value--total">
            {formatPrice(total)}
          </span>
        </div>
      </div>

      <div className="cart-summary__actions">
        <Button
          onClick={handleCheckout}
          variant="primary"
          fullWidth
          disabled={loading || totalItems === 0}
        >
          Proceder al Checkout
        </Button>

        <Button
          onClick={handleClear}
          variant="outline"
          fullWidth
          disabled={loading || totalItems === 0}
        >
          Vaciar Carrito
        </Button>
      </div>

      <div className="cart-summary__info">
        <p>✓ Pago seguro</p>
        <p>✓ Envío en 24-48h</p>
        <p>✓ Devoluciones gratis</p>
      </div>
    </div>
  );
};

export default CartSummary;
