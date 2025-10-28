import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useOrderStore } from '../store/useOrderStore';
import { formatPrice, formatDate } from '../utils/formatters';
import OrderStatusBadge from '../components/orders/OrderStatusBadge';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import Spinner from '../components/common/Spinner';
import './OrdersPage.css';

/**
 * Orders page
 * Displays list of user's orders
 */
function OrdersPage() {
  const navigate = useNavigate();
  const { orders, loading, error, fetchOrders } = useOrderStore();
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    fetchOrders();
  }, []);

  const handleOrderClick = (orderId) => {
    navigate(`/orders/${orderId}`);
  };

  const handleFilterChange = (status) => {
    setStatusFilter(status);
    if (status === 'all') {
      fetchOrders();
    } else {
      fetchOrders({ status });
    }
  };

  // Loading state
  if (loading && orders.length === 0) {
    return (
      <div className="orders-page">
        <div className="orders-loading">
          <Spinner size="large" centered text="Cargando pedidos..." />
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="orders-page">
        <div className="orders-error">
          <Card>
            <h2>Error</h2>
            <p>{error}</p>
            <Button onClick={() => fetchOrders()}>Reintentar</Button>
          </Card>
        </div>
      </div>
    );
  }

  // Empty state
  if (orders.length === 0) {
    return (
      <div className="orders-page">
        <div className="orders-empty">
          <Card>
            <div className="orders-empty-icon">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="64"
                height="64"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
              </svg>
            </div>
            <h2>No tienes pedidos aún</h2>
            <p>Cuando realices un pedido, aparecerá aquí</p>
            <Button variant="primary" onClick={() => navigate('/products')}>
              Explorar productos
            </Button>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="orders-page">
      <div className="orders-container">
        {/* Header */}
        <div className="orders-header">
          <h1>Mis Pedidos</h1>
          <p className="orders-count">
            {orders.length} {orders.length === 1 ? 'pedido' : 'pedidos'}
          </p>
        </div>

        {/* Status filter */}
        <div className="orders-filters">
          <button
            className={`orders-filter-btn ${statusFilter === 'all' ? 'active' : ''}`}
            onClick={() => handleFilterChange('all')}
          >
            Todos
          </button>
          <button
            className={`orders-filter-btn ${statusFilter === 'pending' ? 'active' : ''}`}
            onClick={() => handleFilterChange('pending')}
          >
            Pendientes
          </button>
          <button
            className={`orders-filter-btn ${statusFilter === 'processing' ? 'active' : ''}`}
            onClick={() => handleFilterChange('processing')}
          >
            Procesando
          </button>
          <button
            className={`orders-filter-btn ${statusFilter === 'shipped' ? 'active' : ''}`}
            onClick={() => handleFilterChange('shipped')}
          >
            Enviados
          </button>
          <button
            className={`orders-filter-btn ${statusFilter === 'delivered' ? 'active' : ''}`}
            onClick={() => handleFilterChange('delivered')}
          >
            Entregados
          </button>
        </div>

        {/* Orders list */}
        <div className="orders-list">
          {orders.map((order) => (
            <Card
              key={order.id}
              hoverable
              onClick={() => handleOrderClick(order.id)}
              className="order-card"
            >
              <div className="order-card-header">
                <div className="order-card-info">
                  <h3 className="order-card-id">Pedido #{order.id}</h3>
                  <p className="order-card-date">{formatDate(order.created_at)}</p>
                </div>
                <OrderStatusBadge status={order.status} />
              </div>

              <div className="order-card-body">
                <div className="order-card-items">
                  <span className="order-card-label">Artículos:</span>
                  <span className="order-card-value">{order.items?.length || 0}</span>
                </div>
                <div className="order-card-total">
                  <span className="order-card-label">Total:</span>
                  <span className="order-card-value order-card-price">
                    {formatPrice(order.total_amount)}
                  </span>
                </div>
              </div>

              <div className="order-card-footer">
                <span className="order-card-address">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
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
                  {order.shipping_address}
                </span>
              </div>

              <div className="order-card-arrow">
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
                  <polyline points="9 18 15 12 9 6"></polyline>
                </svg>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}

export default OrdersPage;
