import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useCartStore } from '../store/useCartStore';
import CartItem from '../components/cart/CartItem';
import CartSummary from '../components/cart/CartSummary';
import Spinner from '../components/common/Spinner';
import Button from '../components/common/Button';
import './CartPage.css';

/**
 * Página del carrito de compras
 */
const CartPage = () => {
  const {
    items,
    totalItems,
    totalAmount,
    loading,
    error,
    fetchCart,
    updateItem,
    removeItem,
    clearCart,
    clearError
  } = useCartStore();

  useEffect(() => {
    fetchCart();
  }, [fetchCart]);

  // Limpiar error después de 5 segundos
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => {
        clearError();
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [error, clearError]);

  if (loading && items.length === 0) {
    return (
      <div className="cart-page">
        <div className="cart-page__loading">
          <Spinner size="large" />
          <p>Cargando carrito...</p>
        </div>
      </div>
    );
  }

  // Estado vacío
  if (items.length === 0 && !loading) {
    return (
      <div className="cart-page">
        <div className="cart-page__empty">
          <div className="cart-page__empty-icon">🛒</div>
          <h2>Tu carrito está vacío</h2>
          <p>Parece que aún no has agregado productos a tu carrito.</p>
          <Link to="/products">
            <Button variant="primary" size="large">
              Explorar Productos
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="cart-page">
      <div className="cart-page__container">
        {/* Header */}
        <div className="cart-page__header">
          <h1 className="cart-page__title">Carrito de Compras</h1>
          <p className="cart-page__subtitle">
            {totalItems} {totalItems === 1 ? 'producto' : 'productos'}
          </p>
        </div>

        {/* Mensaje de error */}
        {error && (
          <div className="cart-page__error">
            <span>⚠️ {error}</span>
            <button onClick={clearError}>✕</button>
          </div>
        )}

        {/* Layout principal */}
        <div className="cart-page__content">
          {/* Lista de productos */}
          <div className="cart-page__items">
            {items.map((item) => (
              <CartItem
                key={item.product.id}
                item={item}
                onUpdateQuantity={updateItem}
                onRemove={removeItem}
                loading={loading}
              />
            ))}
          </div>

          {/* Resumen del carrito */}
          <div className="cart-page__summary">
            <CartSummary
              totalItems={totalItems}
              totalAmount={totalAmount}
              loading={loading}
              onClearCart={clearCart}
            />
          </div>
        </div>

        {/* Link para continuar comprando */}
        <div className="cart-page__continue">
          <Link to="/products" className="cart-page__continue-link">
            ← Continuar Comprando
          </Link>
        </div>
      </div>
    </div>
  );
};

export default CartPage;
