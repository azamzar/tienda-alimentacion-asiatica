import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../common/Button';
import OrderStatusBadge from '../orders/OrderStatusBadge';
import { formatDate, formatPrice } from '../../utils/formatters';
import './AdminOrderTable.css';

/**
 * Tabla de pedidos para administradores
 */
const AdminOrderTable = ({ orders, onUpdateStatus, loading }) => {
  const navigate = useNavigate();

  if (loading) {
    return (
      <div className="admin-order-table-loading">
        <div className="spinner"></div>
        <p>Cargando pedidos...</p>
      </div>
    );
  }

  if (!orders || orders.length === 0) {
    return (
      <div className="admin-order-table-empty">
        <p>No hay pedidos que mostrar</p>
      </div>
    );
  }

  return (
    <div className="admin-order-table-container">
      <div className="admin-order-table-wrapper">
        <table className="admin-order-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Cliente</th>
              <th>Email</th>
              <th>Teléfono</th>
              <th>Total</th>
              <th>Estado</th>
              <th>Fecha</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id}>
                <td className="order-id">#{order.id}</td>
                <td className="customer-name">{order.customer_name}</td>
                <td className="customer-email">{order.customer_email}</td>
                <td className="customer-phone">{order.customer_phone}</td>
                <td className="order-total">{formatPrice(order.total_amount)}</td>
                <td>
                  <OrderStatusBadge status={order.status} />
                </td>
                <td className="order-date">{formatDate(order.created_at)}</td>
                <td className="order-actions">
                  <div className="action-buttons">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => navigate(`/orders/${order.id}`)}
                    >
                      Ver
                    </Button>
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={() => onUpdateStatus(order)}
                      disabled={order.status === 'delivered' || order.status === 'cancelled'}
                    >
                      Actualizar
                    </Button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Vista móvil */}
      <div className="admin-order-cards">
        {orders.map((order) => (
          <div key={order.id} className="admin-order-card">
            <div className="order-card-header">
              <span className="order-card-id">Pedido #{order.id}</span>
              <OrderStatusBadge status={order.status} />
            </div>

            <div className="order-card-body">
              <div className="order-card-row">
                <span className="label">Cliente:</span>
                <span className="value">{order.customer_name}</span>
              </div>
              <div className="order-card-row">
                <span className="label">Email:</span>
                <span className="value">{order.customer_email}</span>
              </div>
              <div className="order-card-row">
                <span className="label">Teléfono:</span>
                <span className="value">{order.customer_phone}</span>
              </div>
              <div className="order-card-row">
                <span className="label">Total:</span>
                <span className="value total">{formatPrice(order.total_amount)}</span>
              </div>
              <div className="order-card-row">
                <span className="label">Fecha:</span>
                <span className="value">{formatDate(order.created_at)}</span>
              </div>
            </div>

            <div className="order-card-actions">
              <Button
                variant="ghost"
                onClick={() => navigate(`/orders/${order.id}`)}
              >
                Ver Detalles
              </Button>
              <Button
                variant="primary"
                onClick={() => onUpdateStatus(order)}
                disabled={order.status === 'delivered' || order.status === 'cancelled'}
              >
                Actualizar Estado
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AdminOrderTable;
