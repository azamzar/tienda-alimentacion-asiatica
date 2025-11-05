import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useCartStore } from '../store/useCartStore';
import { useOrderStore } from '../store/useOrderStore';
import CheckoutForm from '../components/checkout/CheckoutForm';
import OrderSummary from '../components/checkout/OrderSummary';
import Spinner from '../components/common/Spinner';
import Button from '../components/common/Button';
import './CheckoutPage.css';

/**
 * Página de checkout para completar la compra
 */
const CheckoutPage = () => {
  const navigate = useNavigate();
  const {
    items,
    totalItems,
    totalAmount,
    loading: cartLoading,
    fetchCart,
    clearCart
  } = useCartStore();

  const {
    createOrder,
    loading: orderLoading,
    error: orderError,
    clearError
  } = useOrderStore();

  const [isProcessingOrder, setIsProcessingOrder] = useState(false);

  useEffect(() => {
    fetchCart();
  }, [fetchCart]);

  // Si el carrito está vacío, redirigir (pero no si estamos procesando un pedido)
  useEffect(() => {
    if (!cartLoading && items.length === 0 && !isProcessingOrder) {
      navigate('/cart');
    }
  }, [items, cartLoading, isProcessingOrder, navigate]);

  const handleSubmit = async (formData) => {
    setIsProcessingOrder(true);

    // Show loading toast
    const toastId = toast.loading('Procesando tu pedido...');

    try {
      // Crear orden (el backend vacía el carrito automáticamente)
      const order = await createOrder(formData);

      // Dismiss loading and show success
      toast.success('¡Pedido creado exitosamente!', {
        id: toastId,
        icon: '🎉',
        duration: 3000,
      });

      // Navegar directamente a la página de detalle del pedido con estado de éxito
      navigate(`/orders/${order.id}`, {
        state: { fromCheckout: true, orderJustCreated: true }
      });
    } catch (error) {
      console.error('Error creating order:', error);

      // Dismiss loading and show error
      toast.error(error.response?.data?.detail || 'Error al crear el pedido. Intenta nuevamente.', {
        id: toastId,
        duration: 5000,
      });

      setIsProcessingOrder(false);
    }
  };

  if (cartLoading) {
    return (
      <div className="checkout-page">
        <div className="checkout-page__loading">
          <Spinner size="large" />
          <p>Cargando...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="checkout-page">
      <div className="checkout-page__container">
        {/* Header */}
        <div className="checkout-page__header">
          <h1 className="checkout-page__title">Finalizar Compra</h1>
          <p className="checkout-page__subtitle">
            Completa tus datos para confirmar el pedido
          </p>
        </div>

        {/* Mensaje de error global */}
        {orderError && (
          <div className="checkout-page__error">
            <span>⚠️ {orderError}</span>
            <button onClick={clearError}>✕</button>
          </div>
        )}

        {/* Layout principal */}
        <div className="checkout-page__content">
          {/* Formulario */}
          <div className="checkout-page__form">
            <CheckoutForm
              onSubmit={handleSubmit}
              loading={orderLoading}
            />
          </div>

          {/* Resumen del pedido */}
          <div className="checkout-page__summary">
            <OrderSummary
              items={items}
              totalItems={totalItems}
              totalAmount={totalAmount}
            />
          </div>
        </div>

        {/* Link para volver al carrito */}
        <div className="checkout-page__back">
          <Button
            variant="outline"
            onClick={() => navigate('/cart')}
            disabled={orderLoading}
          >
            ← Volver al Carrito
          </Button>
        </div>
      </div>
    </div>
  );
};

export default CheckoutPage;
