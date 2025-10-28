import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { useOrderStore } from '../store/useOrderStore';
import { formatPrice, formatDate } from '../utils/formatters';
import OrderStatusBadge from '../components/orders/OrderStatusBadge';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import Spinner from '../components/common/Spinner';
import './OrderDetailPage.css';

/**
 * Order detail page
 * Shows detailed information about a single order
 */
function OrderDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const { currentOrder, loading, error, fetchOrderById, cancelOrder } = useOrderStore();
  const [isCancelling, setIsCancelling] = useState(false);
  const [showSuccessBanner, setShowSuccessBanner] = useState(false);

  useEffect(() => {
    fetchOrderById(id);

    // Mostrar banner de éxito si viene del checkout
    if (location.state?.orderJustCreated) {
      setShowSuccessBanner(true);
      // Ocultar después de 5 segundos
      setTimeout(() => {
        setShowSuccessBanner(false);
      }, 5000);

      // Limpiar el estado de navegación para que no se muestre si recargan la página
      window.history.replaceState({}, document.title);
    }
  }, [id, location.state]);

  const handleCancelOrder = async () => {
    if (!window.confirm('¿Estás seguro de que quieres cancelar este pedido?')) {
      return;
    }

    setIsCancelling(true);
    try {
      await cancelOrder(id);
      alert('Pedido cancelado exitosamente');
    } catch (error) {
      alert('Error al cancelar el pedido. Por favor, inténtalo de nuevo.');
    } finally {
      setIsCancelling(false);
    }
  };

  // Loading state
  if (loading && !currentOrder) {
    return (
      <div className="order-detail-page">
        <div className="order-detail-loading">
          <Spinner size="large" centered text="Cargando pedido..." />
        </div>
      </div>
    );
  }

  // Error state
  if (error || !currentOrder) {
    return (
      <div className="order-detail-page">
        <div className="order-detail-error">
          <Card>
            <h2>Error</h2>
            <p>{error || 'Pedido no encontrado'}</p>
            <Button onClick={() => navigate('/orders')}>Volver a pedidos</Button>
          </Card>
        </div>
      </div>
    );
  }

  const order = currentOrder;
  const canCancel = order.status === 'pending';

  // Calculate subtotal from items
  const subtotal = order.items?.reduce((sum, item) => sum + item.subtotal, 0) || 0;

  // Calculate shipping cost (same logic as checkout)
  const shippingCost = subtotal >= 50 ? 0 : 5;

  return (
    <div className="order-detail-page">
      <div className="order-detail-container">
        {/* Success banner */}
        {showSuccessBanner && (
          <div className="order-detail-success-banner">
            <div className="order-detail-success-icon">✓</div>
            <div className="order-detail-success-content">
              <h3>¡Pedido creado exitosamente!</h3>
              <p>Tu pedido #{id} ha sido confirmado y está siendo procesado.</p>
            </div>
          </div>
        )}

        {/* Back button */}
        <button className="order-detail-back" onClick={() => navigate('/orders')}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          Volver a mis pedidos
        </button>

        {/* Header */}
        <div className="order-detail-header">
          <div className="order-detail-title">
            <h1>Pedido #{order.id}</h1>
            <OrderStatusBadge status={order.status} />
          </div>
          <p className="order-detail-date">Realizado el {formatDate(order.created_at)}</p>
        </div>

        <div className="order-detail-grid">
          {/* Customer information */}
          <Card className="order-detail-card">
            <h2 className="order-detail-card-title">Información del Cliente</h2>
            <div className="order-detail-info-grid">
              <div className="order-detail-info-item">
                <span className="order-detail-info-label">Nombre:</span>
                <span className="order-detail-info-value">{order.customer_name}</span>
              </div>
              <div className="order-detail-info-item">
                <span className="order-detail-info-label">Email:</span>
                <span className="order-detail-info-value">{order.customer_email}</span>
              </div>
              <div className="order-detail-info-item">
                <span className="order-detail-info-label">Teléfono:</span>
                <span className="order-detail-info-value">{order.customer_phone}</span>
              </div>
            </div>
          </Card>

          {/* Shipping information */}
          <Card className="order-detail-card">
            <h2 className="order-detail-card-title">Dirección de Envío</h2>
            <div className="order-detail-address">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                <circle cx="12" cy="10" r="3"></circle>
              </svg>
              <p>{order.shipping_address}</p>
            </div>
            {order.notes && (
              <div className="order-detail-notes">
                <h3>Notas adicionales:</h3>
                <p>{order.notes}</p>
              </div>
            )}
          </Card>
        </div>

        {/* Order items */}
        <Card className="order-detail-items-card">
          <h2 className="order-detail-card-title">Artículos del Pedido</h2>
          <div className="order-detail-items">
            {order.items && order.items.length > 0 ? (
              order.items.map((item) => (
                <div key={item.id} className="order-detail-item">
                  <div className="order-detail-item-image">
                    <img
                      src={
                        item.product?.image_url ||
                        'https://placehold.co/80x80/f0f0f0/666?text=Producto'
                      }
                      alt={item.product?.name || 'Producto'}
                      onError={(e) => {
                        if (!e.target.src.includes('placehold.co')) {
                          e.target.src = 'https://placehold.co/80x80/f0f0f0/666?text=Producto';
                        }
                      }}
                    />
                  </div>
                  <div className="order-detail-item-info">
                    <h3 className="order-detail-item-name">
                      {item.product?.name || 'Producto no disponible'}
                    </h3>
                    <p className="order-detail-item-price">
                      {formatPrice(item.unit_price)} × {item.quantity}
                    </p>
                  </div>
                  <div className="order-detail-item-total">
                    {formatPrice(item.subtotal)}
                  </div>
                </div>
              ))
            ) : (
              <p className="order-detail-no-items">No hay artículos en este pedido</p>
            )}
          </div>

          {/* Order summary */}
          <div className="order-detail-summary">
            <div className="order-detail-summary-row">
              <span>Subtotal:</span>
              <span>{formatPrice(subtotal)}</span>
            </div>
            <div className="order-detail-summary-row">
              <span>Envío:</span>
              <span>
                {shippingCost === 0 ? (
                  <span style={{ color: '#059669', fontWeight: '600' }}>GRATIS</span>
                ) : (
                  formatPrice(shippingCost)
                )}
              </span>
            </div>
            <div className="order-detail-summary-row order-detail-summary-total">
              <span>Total:</span>
              <span>{formatPrice(order.total_amount)}</span>
            </div>
          </div>
        </Card>

        {/* Actions */}
        {canCancel && (
          <div className="order-detail-actions">
            <Button
              variant="danger"
              onClick={handleCancelOrder}
              disabled={isCancelling}
              loading={isCancelling}
            >
              Cancelar Pedido
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}

export default OrderDetailPage;
