import api from './api';

/**
 * Servicio para gestionar pedidos
 */
export const orderService = {
  /**
   * Crear un pedido desde el carrito del usuario
   * @param {string} userId - ID del usuario
   * @param {Object} orderData - Datos del pedido
   * @param {string} orderData.customer_name - Nombre del cliente
   * @param {string} orderData.customer_email - Email del cliente
   * @param {string} orderData.customer_phone - Teléfono del cliente
   * @param {string} orderData.shipping_address - Dirección de envío
   * @param {string} orderData.notes - Notas adicionales (opcional)
   * @returns {Promise<Object>} Pedido creado
   */
  createOrder: async (userId, orderData) => {
    const { data } = await api.post('/orders/', orderData, {
      params: { user_id: userId }
    });
    return data;
  },

  /**
   * Obtener todos los pedidos con filtros
   * @param {Object} filters - Filtros de búsqueda
   * @param {string} filters.user_id - Filtrar por usuario
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
   * @param {string} userId - ID del usuario (opcional, para validación)
   * @returns {Promise<Object>} Datos del pedido
   */
  getOrderById: async (orderId, userId = null) => {
    const params = userId ? { user_id: userId } : {};
    const { data } = await api.get(`/orders/${orderId}`, { params });
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
   * @param {string} userId - ID del usuario (opcional, para validación)
   * @returns {Promise<Object>} Pedido actualizado
   */
  updateOrder: async (orderId, updates, userId = null) => {
    const params = userId ? { user_id: userId } : {};
    const { data } = await api.patch(`/orders/${orderId}`, updates, { params });
    return data;
  },

  /**
   * Cancelar un pedido y restaurar el stock
   * @param {number} orderId - ID del pedido
   * @param {string} userId - ID del usuario (opcional, para validación)
   * @returns {Promise<Object>} Pedido cancelado
   */
  cancelOrder: async (orderId, userId = null) => {
    const params = userId ? { user_id: userId } : {};
    const { data } = await api.post(`/orders/${orderId}/cancel`, {}, { params });
    return data;
  }
};
