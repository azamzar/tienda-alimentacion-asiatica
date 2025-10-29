import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import StatCard from '../../components/admin/StatCard';
import OrderStatusBadge from '../../components/orders/OrderStatusBadge';
import Spinner from '../../components/common/Spinner';
import { dashboardService } from '../../services/dashboardService';
import { formatPrice, formatDate } from '../../utils/formatters';
import './AdminDashboardPage.css';

/**
 * Admin dashboard page - Panel principal de administración
 * Muestra estadísticas, pedidos recientes y productos con bajo stock
 */
function AdminDashboardPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await dashboardService.getDashboardStats();
      setStats(data);
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      setError('Error al cargar las estadísticas del dashboard');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="admin-dashboard">
        <Spinner />
      </div>
    );
  }

  if (error) {
    return (
      <div className="admin-dashboard">
        <div className="dashboard-error">
          <p>{error}</p>
          <button onClick={fetchDashboardData} className="retry-button">
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <div>
          <h1 className="dashboard-title">Panel de Administración</h1>
          <p className="dashboard-subtitle">
            Resumen de tu tienda y actividad reciente
          </p>
        </div>
        <button onClick={fetchDashboardData} className="refresh-button">
          🔄 Actualizar
        </button>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid">
        <StatCard
          title="Total Productos"
          value={stats.totalProducts}
          icon="📦"
          color="blue"
          subtitle={`${stats.outOfStockProducts} sin stock`}
        />
        <StatCard
          title="Total Pedidos"
          value={stats.totalOrders}
          icon="🛒"
          color="green"
          subtitle={`${stats.pendingOrders} pendientes`}
        />
        <StatCard
          title="Ventas Totales"
          value={formatPrice(stats.totalRevenue)}
          icon="💰"
          color="purple"
          subtitle="Ingresos acumulados"
        />
        <StatCard
          title="Stock Bajo"
          value={stats.lowStockProducts}
          icon="⚠️"
          color="yellow"
          subtitle="Requieren reposición"
        />
      </div>

      {/* Pedidos por Estado */}
      <div className="dashboard-section">
        <h2 className="section-title">Pedidos por Estado</h2>
        <div className="orders-status-grid">
          <div className="status-card">
            <div className="status-card-header">
              <span className="status-card-label">Pendientes</span>
              <OrderStatusBadge status="pending" />
            </div>
            <p className="status-card-value">{stats.ordersByStatus.pending}</p>
          </div>
          <div className="status-card">
            <div className="status-card-header">
              <span className="status-card-label">Confirmados</span>
              <OrderStatusBadge status="confirmed" />
            </div>
            <p className="status-card-value">{stats.ordersByStatus.confirmed}</p>
          </div>
          <div className="status-card">
            <div className="status-card-header">
              <span className="status-card-label">En Proceso</span>
              <OrderStatusBadge status="processing" />
            </div>
            <p className="status-card-value">{stats.ordersByStatus.processing}</p>
          </div>
          <div className="status-card">
            <div className="status-card-header">
              <span className="status-card-label">Enviados</span>
              <OrderStatusBadge status="shipped" />
            </div>
            <p className="status-card-value">{stats.ordersByStatus.shipped}</p>
          </div>
          <div className="status-card">
            <div className="status-card-header">
              <span className="status-card-label">Entregados</span>
              <OrderStatusBadge status="delivered" />
            </div>
            <p className="status-card-value">{stats.ordersByStatus.delivered}</p>
          </div>
          <div className="status-card">
            <div className="status-card-header">
              <span className="status-card-label">Cancelados</span>
              <OrderStatusBadge status="cancelled" />
            </div>
            <p className="status-card-value">{stats.ordersByStatus.cancelled}</p>
          </div>
        </div>
      </div>

      <div className="dashboard-grid">
        {/* Pedidos Recientes */}
        <div className="dashboard-section">
          <div className="section-header">
            <h2 className="section-title">Pedidos Recientes</h2>
            <Link to="/admin/orders" className="section-link">
              Ver todos →
            </Link>
          </div>

          {stats.recentOrders.length === 0 ? (
            <div className="empty-state">
              <p>No hay pedidos recientes</p>
            </div>
          ) : (
            <div className="table-container">
              <table className="dashboard-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Cliente</th>
                    <th>Total</th>
                    <th>Estado</th>
                    <th>Fecha</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.recentOrders.map((order) => (
                    <tr key={order.id}>
                      <td>#{order.id}</td>
                      <td>{order.customer_name}</td>
                      <td className="table-amount">{formatPrice(order.total_amount)}</td>
                      <td>
                        <OrderStatusBadge status={order.status} />
                      </td>
                      <td className="table-date">{formatDate(order.created_at)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Productos con Bajo Stock */}
        <div className="dashboard-section">
          <div className="section-header">
            <h2 className="section-title">Productos con Bajo Stock</h2>
            <Link to="/admin/products" className="section-link">
              Gestionar →
            </Link>
          </div>

          {stats.lowStockProductsList.length === 0 ? (
            <div className="empty-state">
              <p>✓ Todos los productos tienen stock suficiente</p>
            </div>
          ) : (
            <div className="low-stock-list">
              {stats.lowStockProductsList.map((product) => (
                <div key={product.id} className="low-stock-item">
                  <div className="low-stock-info">
                    <p className="low-stock-name">{product.name}</p>
                    <p className="low-stock-category">{product.category?.name}</p>
                  </div>
                  <div className="low-stock-stock">
                    <span className={`stock-badge ${product.stock === 0 ? 'stock-out' : 'stock-low'}`}>
                      {product.stock === 0 ? 'Sin stock' : `${product.stock} unidades`}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default AdminDashboardPage;
