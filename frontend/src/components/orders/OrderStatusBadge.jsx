import React from 'react';
import './OrderStatusBadge.css';

/**
 * Order status badge component
 * Displays order status with appropriate styling
 *
 * @param {Object} props
 * @param {string} props.status - Order status (pending, processing, shipped, delivered, cancelled)
 */
function OrderStatusBadge({ status }) {
  const statusConfig = {
    pending: {
      label: 'Pendiente',
      className: 'order-status-badge-pending'
    },
    processing: {
      label: 'Procesando',
      className: 'order-status-badge-processing'
    },
    shipped: {
      label: 'Enviado',
      className: 'order-status-badge-shipped'
    },
    delivered: {
      label: 'Entregado',
      className: 'order-status-badge-delivered'
    },
    cancelled: {
      label: 'Cancelado',
      className: 'order-status-badge-cancelled'
    }
  };

  const config = statusConfig[status] || statusConfig.pending;

  return (
    <span className={`order-status-badge ${config.className}`}>
      {config.label}
    </span>
  );
}

export default OrderStatusBadge;
