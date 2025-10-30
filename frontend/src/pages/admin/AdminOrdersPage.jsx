import React, { useState, useEffect } from 'react';
import { orderService } from '../../services/orderService';
import AdminOrderTable from '../../components/admin/AdminOrderTable';
import OrderStatusUpdateModal from '../../components/admin/OrderStatusUpdateModal';
import Button from '../../components/common/Button';
import { ORDER_STATUS, ORDER_STATUS_LABELS } from '../../utils/constants';
import './AdminOrdersPage.css';

/**
 * Página de gestión de pedidos para administradores
 */
const AdminOrdersPage = () => {
  const [orders, setOrders] = useState([]);
  const [filteredOrders, setFilteredOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [statusFilter, setStatusFilter] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  // Cargar pedidos
  const fetchOrders = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await orderService.getOrders();
      setOrders(data);
      setFilteredOrders(data);
    } catch (err) {
      console.error('Error al cargar pedidos:', err);
      setError(err.response?.data?.detail || 'Error al cargar los pedidos');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  // Filtrar pedidos por estado y búsqueda
  useEffect(() => {
    let filtered = [...orders];

    // Filtrar por estado
    if (statusFilter) {
      filtered = filtered.filter((order) => order.status === statusFilter);
    }

    // Filtrar por búsqueda (nombre, email, ID)
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(
        (order) =>
          order.id.toString().includes(term) ||
          order.customer_name.toLowerCase().includes(term) ||
          order.customer_email.toLowerCase().includes(term)
      );
    }

    setFilteredOrders(filtered);
  }, [statusFilter, searchTerm, orders]);

  // Abrir modal para actualizar estado
  const handleUpdateStatus = (order) => {
    setSelectedOrder(order);
    setIsModalOpen(true);
  };

  // Actualizar estado del pedido
  const handleStatusUpdate = async (orderId, updates) => {
    try {
      await orderService.updateOrder(orderId, updates);
      // Recargar pedidos
      await fetchOrders();
      setIsModalOpen(false);
      setSelectedOrder(null);
    } catch (err) {
      console.error('Error al actualizar pedido:', err);
      throw err;
    }
  };

  // Limpiar filtros
  const handleClearFilters = () => {
    setStatusFilter('');
    setSearchTerm('');
  };

  // Estadísticas rápidas
  const stats = {
    total: orders.length,
    pending: orders.filter((o) => o.status === ORDER_STATUS.PENDING).length,
    confirmed: orders.filter((o) => o.status === ORDER_STATUS.CONFIRMED).length,
    processing: orders.filter((o) => o.status === ORDER_STATUS.PROCESSING).length,
    shipped: orders.filter((o) => o.status === ORDER_STATUS.SHIPPED).length,
    delivered: orders.filter((o) => o.status === ORDER_STATUS.DELIVERED).length,
    cancelled: orders.filter((o) => o.status === ORDER_STATUS.CANCELLED).length,
  };

  return (
    <div className="admin-orders-page">
      <div className="page-header">
        <div className="header-content">
          <h1>Gestión de Pedidos</h1>
          <p className="subtitle">Administra todos los pedidos de la tienda</p>
        </div>
        <Button onClick={fetchOrders} disabled={loading}>
          {loading ? 'Actualizando...' : 'Actualizar'}
        </Button>
      </div>

      {/* Estadísticas */}
      <div className="orders-stats">
        <div className="stat-card">
          <div className="stat-value">{stats.total}</div>
          <div className="stat-label">Total Pedidos</div>
        </div>
        <div className="stat-card stat-yellow">
          <div className="stat-value">{stats.pending}</div>
          <div className="stat-label">Pendientes</div>
        </div>
        <div className="stat-card stat-blue">
          <div className="stat-value">{stats.confirmed}</div>
          <div className="stat-label">Confirmados</div>
        </div>
        <div className="stat-card stat-purple">
          <div className="stat-value">{stats.processing}</div>
          <div className="stat-label">En Proceso</div>
        </div>
        <div className="stat-card stat-indigo">
          <div className="stat-value">{stats.shipped}</div>
          <div className="stat-label">Enviados</div>
        </div>
        <div className="stat-card stat-green">
          <div className="stat-value">{stats.delivered}</div>
          <div className="stat-label">Entregados</div>
        </div>
      </div>

      {/* Filtros */}
      <div className="orders-filters">
        <div className="search-box">
          <input
            type="text"
            placeholder="Buscar por ID, nombre o email..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="filter-controls">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="status-filter"
          >
            <option value="">Todos los estados</option>
            {Object.values(ORDER_STATUS).map((status) => (
              <option key={status} value={status}>
                {ORDER_STATUS_LABELS[status]}
              </option>
            ))}
          </select>

          {(statusFilter || searchTerm) && (
            <Button variant="ghost" onClick={handleClearFilters}>
              Limpiar filtros
            </Button>
          )}
        </div>
      </div>

      {/* Resultados */}
      <div className="orders-results">
        {filteredOrders.length > 0 && (
          <p className="results-count">
            Mostrando {filteredOrders.length} de {orders.length} pedidos
          </p>
        )}
      </div>

      {/* Error */}
      {error && (
        <div className="error-message">
          <p>{error}</p>
          <Button onClick={fetchOrders}>Reintentar</Button>
        </div>
      )}

      {/* Tabla de pedidos */}
      {!error && (
        <AdminOrderTable
          orders={filteredOrders}
          onUpdateStatus={handleUpdateStatus}
          loading={loading}
        />
      )}

      {/* Modal de actualización de estado */}
      <OrderStatusUpdateModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setSelectedOrder(null);
        }}
        order={selectedOrder}
        onUpdate={handleStatusUpdate}
      />
    </div>
  );
};

export default AdminOrdersPage;
