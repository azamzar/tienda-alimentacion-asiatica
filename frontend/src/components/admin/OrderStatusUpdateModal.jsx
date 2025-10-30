import React, { useState } from 'react';
import Modal from '../common/Modal';
import Button from '../common/Button';
import { ORDER_STATUS, ORDER_STATUS_LABELS, ORDER_STATUS_COLORS } from '../../utils/constants';
import './OrderStatusUpdateModal.css';

/**
 * Modal para actualizar el estado de un pedido (Admin)
 */
const OrderStatusUpdateModal = ({ isOpen, onClose, order, onUpdate }) => {
  const [selectedStatus, setSelectedStatus] = useState(order?.status || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  if (!order) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await onUpdate(order.id, { status: selectedStatus });
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al actualizar el estado del pedido');
    } finally {
      setLoading(false);
    }
  };

  const getStatusInfo = (status) => {
    const color = ORDER_STATUS_COLORS[status] || 'gray';
    const label = ORDER_STATUS_LABELS[status] || status;
    return { color, label };
  };

  // Estados permitidos según el estado actual
  const getAllowedTransitions = (currentStatus) => {
    const transitions = {
      [ORDER_STATUS.PENDING]: [ORDER_STATUS.CONFIRMED, ORDER_STATUS.CANCELLED],
      [ORDER_STATUS.CONFIRMED]: [ORDER_STATUS.PROCESSING, ORDER_STATUS.CANCELLED],
      [ORDER_STATUS.PROCESSING]: [ORDER_STATUS.SHIPPED, ORDER_STATUS.CANCELLED],
      [ORDER_STATUS.SHIPPED]: [ORDER_STATUS.DELIVERED],
      [ORDER_STATUS.DELIVERED]: [],
      [ORDER_STATUS.CANCELLED]: []
    };

    return transitions[currentStatus] || [];
  };

  const allowedStatuses = getAllowedTransitions(order.status);
  const canChangeStatus = allowedStatuses.length > 0;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Actualizar Estado del Pedido">
      <div className="order-status-update-modal">
        <div className="order-info">
          <h3>Pedido #{order.id}</h3>
          <p className="customer-name">{order.customer_name}</p>
          <p className="order-total">Total: {order.total_amount?.toFixed(2)} €</p>
        </div>

        <div className="current-status">
          <label>Estado actual:</label>
          <span
            className={`status-badge status-${getStatusInfo(order.status).color}`}
          >
            {getStatusInfo(order.status).label}
          </span>
        </div>

        {canChangeStatus ? (
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="status">Cambiar a:</label>
              <select
                id="status"
                value={selectedStatus}
                onChange={(e) => setSelectedStatus(e.target.value)}
                required
                className="status-select"
              >
                <option value="">Seleccionar nuevo estado</option>
                {allowedStatuses.map((status) => {
                  const { color, label } = getStatusInfo(status);
                  return (
                    <option key={status} value={status}>
                      {label}
                    </option>
                  );
                })}
              </select>
            </div>

            {error && <div className="error-message">{error}</div>}

            <div className="modal-actions">
              <Button type="button" variant="ghost" onClick={onClose} disabled={loading}>
                Cancelar
              </Button>
              <Button type="submit" variant="primary" disabled={loading || !selectedStatus}>
                {loading ? 'Actualizando...' : 'Actualizar Estado'}
              </Button>
            </div>
          </form>
        ) : (
          <div className="status-locked">
            <p>
              {order.status === ORDER_STATUS.DELIVERED
                ? 'Este pedido ya ha sido entregado y no se puede modificar.'
                : 'Este pedido está cancelado y no se puede modificar.'}
            </p>
            <div className="modal-actions">
              <Button variant="primary" onClick={onClose}>
                Cerrar
              </Button>
            </div>
          </div>
        )}
      </div>
    </Modal>
  );
};

export default OrderStatusUpdateModal;
