import React from 'react';
import { formatPrice } from '../../utils/formatters';
import './OrderSummary.css';

/**
 * Resumen de la orden para la página de checkout
 * @param {Array} items - Items del carrito
 * @param {number} totalItems - Cantidad total de items
 * @param {number} totalAmount - Monto total
 */
const OrderSummary = ({ items, totalItems, totalAmount }) => {
  // Calcular costos
  const shippingCost = totalAmount >= 50 ? 0 : 5;
  const finalTotal = totalAmount + shippingCost;

  return (
    <div className="order-summary">
      <h2 className="order-summary__title">Resumen del Pedido</h2>

      {/* Lista de productos */}
      <div className="order-summary__items">
        {items && items.length > 0 ? (
          items.map((item) => (
            <div key={item.product.id} className="order-summary__item">
              <div className="order-summary__item-image">
                {item.product.image_url ? (
                  <img src={item.product.image_url} alt={item.product.name} />
                ) : (
                  <div className="order-summary__item-placeholder">📦</div>
                )}
              </div>
              <div className="order-summary__item-details">
                <p className="order-summary__item-name">{item.product.name}</p>
                <p className="order-summary__item-quantity">
                  Cantidad: {item.quantity}
                </p>
              </div>
              <div className="order-summary__item-price">
                {formatPrice(item.subtotal)}
              </div>
            </div>
          ))
        ) : (
          <p className="order-summary__empty">No hay productos en el carrito</p>
        )}
      </div>

      {/* Totales */}
      <div className="order-summary__totals">
        <div className="order-summary__row">
          <span className="order-summary__label">
            Subtotal ({totalItems} {totalItems === 1 ? 'producto' : 'productos'})
          </span>
          <span className="order-summary__value">{formatPrice(totalAmount)}</span>
        </div>

        <div className="order-summary__row">
          <span className="order-summary__label">Envío</span>
          <span className="order-summary__value">
            {shippingCost === 0 ? (
              <span className="order-summary__free">GRATIS</span>
            ) : (
              formatPrice(shippingCost)
            )}
          </span>
        </div>

        {totalAmount < 50 && totalAmount > 0 && (
          <div className="order-summary__shipping-note">
            <small>
              🎉 Envío gratis a partir de {formatPrice(50)}
              <br />
              Te faltan {formatPrice(50 - totalAmount)}
            </small>
          </div>
        )}

        <div className="order-summary__divider"></div>

        <div className="order-summary__row order-summary__row--total">
          <span className="order-summary__label">Total a Pagar</span>
          <span className="order-summary__value order-summary__value--total">
            {formatPrice(finalTotal)}
          </span>
        </div>
      </div>

      {/* Información adicional */}
      <div className="order-summary__info">
        <div className="order-summary__info-item">
          <span className="order-summary__info-icon">✓</span>
          <span>Pago seguro</span>
        </div>
        <div className="order-summary__info-item">
          <span className="order-summary__info-icon">✓</span>
          <span>Envío en 24-48h</span>
        </div>
        <div className="order-summary__info-item">
          <span className="order-summary__info-icon">✓</span>
          <span>Devoluciones gratis</span>
        </div>
      </div>
    </div>
  );
};

export default OrderSummary;
