import api from './api';

/**
 * Dashboard service - Obtiene estadísticas y métricas para el panel de administración
 */
export const dashboardService = {
  /**
   * Obtener estadísticas generales del dashboard
   * @returns {Promise<Object>} Estadísticas del dashboard
   */
  async getDashboardStats() {
    try {
      // Llamar al endpoint optimizado del backend que retorna todas las estadísticas
      const { data } = await api.get('/admin/dashboard/stats');
      return data;
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
      throw error;
    }
  },

  /**
   * Obtener pedidos recientes
   * @param {number} limit - Número de pedidos a obtener
   * @returns {Promise<Array>} Lista de pedidos recientes
   */
  async getRecentOrders(limit = 10) {
    try {
      const { data } = await api.get('/orders/', {
        params: { limit }
      });
      return data;
    } catch (error) {
      console.error('Error fetching recent orders:', error);
      throw error;
    }
  },

  /**
   * Obtener productos con bajo stock
   * @param {number} threshold - Umbral de stock bajo
   * @returns {Promise<Array>} Lista de productos con bajo stock
   */
  async getLowStockProducts(threshold = 10) {
    try {
      const { data } = await api.get('/products/low-stock/', {
        params: { threshold }
      });
      return data;
    } catch (error) {
      console.error('Error fetching low stock products:', error);
      throw error;
    }
  }
};

export default dashboardService;
