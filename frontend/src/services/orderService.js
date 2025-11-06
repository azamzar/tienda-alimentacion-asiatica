import api from './api';

/**
 * Servicio para gestionar pedidos
 * NOTA: Todos los endpoints requieren autenticación JWT
 * El user_id se obtiene automáticamente del token
 */
export const orderService = {
  /**
   * Crear un pedido desde el carrito del usuario autenticado
   * @param {Object} orderData - Datos del pedido
   * @param {string} orderData.customer_name - Nombre del cliente
   * @param {string} orderData.customer_email - Email del cliente
   * @param {string} orderData.customer_phone - Teléfono del cliente
   * @param {string} orderData.shipping_address - Dirección de envío
   * @param {string} orderData.notes - Notas adicionales (opcional)
   * @returns {Promise<Object>} Pedido creado
   */
  createOrder: async (orderData) => {
    const { data } = await api.post('/orders/', orderData);
    return data;
  },

  /**
   * Obtener todos los pedidos del usuario autenticado con filtros
   * @param {Object} filters - Filtros de búsqueda
   * @param {string} filters.status - Filtrar por estado
   * @param {number} filters.skip - Registros a omitir
   * @param {number} filters.limit - Límite de registros
   * @returns {Promise<Array>} Lista de pedidos
   */
  getOrders: async (filters = {}) => {
    const { data } = await api.get('/orders/', { params: filters });
    return data;
  },

  /**
   * Obtener un pedido por ID
   * @param {number} orderId - ID del pedido
   * @returns {Promise<Object>} Datos del pedido
   */
  getOrderById: async (orderId) => {
    const { data } = await api.get(`/orders/${orderId}`);
    return data;
  },

  /**
   * Actualizar un pedido (estado, datos del cliente)
   * @param {number} orderId - ID del pedido
   * @param {Object} updates - Datos a actualizar
   * @param {string} updates.status - Nuevo estado (opcional)
   * @param {string} updates.customer_name - Nombre del cliente (opcional)
   * @param {string} updates.customer_phone - Teléfono (opcional)
   * @param {string} updates.shipping_address - Dirección (opcional)
   * @param {string} updates.notes - Notas (opcional)
   * @returns {Promise<Object>} Pedido actualizado
   */
  updateOrder: async (orderId, updates) => {
    const { data } = await api.patch(`/orders/${orderId}`, updates);
    return data;
  },

  /**
   * Cancelar un pedido y restaurar el stock
   * @param {number} orderId - ID del pedido
   * @returns {Promise<Object>} Pedido cancelado
   */
  cancelOrder: async (orderId) => {
    const { data } = await api.post(`/orders/${orderId}/cancel`);
    return data;
  },

  /**
   * Exportar pedidos a CSV (solo admin)
   * @param {Object} filters - Filtros de exportación
   * @param {string} filters.status - Filtrar por estado (opcional)
   * @returns {Promise<Blob>} Archivo CSV como blob
   */
  exportOrdersCSV: async (filters = {}) => {
    const response = await api.get('/orders/export/csv', {
      params: filters,
      responseType: 'blob'
    });
    return response.data;
  }
};
