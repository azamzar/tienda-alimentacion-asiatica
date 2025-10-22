import api from './api';

/**
 * Servicio para gestionar el carrito de compras
 */
export const cartService = {
  /**
   * Obtener el carrito del usuario
   * @param {string} userId - ID del usuario
   * @returns {Promise<Object>} Datos del carrito con items y totales
   */
  getCart: async (userId) => {
    const { data } = await api.get(`/carts/${userId}`);
    return data;
  },

  /**
   * Agregar un producto al carrito
   * Si el producto ya existe, incrementa la cantidad
   * @param {string} userId - ID del usuario
   * @param {Object} item - Datos del item
   * @param {number} item.product_id - ID del producto
   * @param {number} item.quantity - Cantidad a agregar
   * @returns {Promise<Object>} Carrito actualizado
   */
  addToCart: async (userId, item) => {
    const { data } = await api.post(`/carts/${userId}/items`, item);
    return data;
  },

  /**
   * Actualizar la cantidad de un producto en el carrito
   * @param {string} userId - ID del usuario
   * @param {number} productId - ID del producto
   * @param {number} quantity - Nueva cantidad
   * @returns {Promise<Object>} Carrito actualizado
   */
  updateCartItem: async (userId, productId, quantity) => {
    const { data } = await api.put(`/carts/${userId}/items/${productId}`, {
      quantity
    });
    return data;
  },

  /**
   * Eliminar un producto del carrito
   * @param {string} userId - ID del usuario
   * @param {number} productId - ID del producto a eliminar
   * @returns {Promise<Object>} Carrito actualizado
   */
  removeFromCart: async (userId, productId) => {
    const { data } = await api.delete(`/carts/${userId}/items/${productId}`);
    return data;
  },

  /**
   * Vaciar el carrito completamente
   * @param {string} userId - ID del usuario
   * @returns {Promise<Object>} Respuesta con mensaje de confirmación
   */
  clearCart: async (userId) => {
    const { data } = await api.delete(`/carts/${userId}`);
    return data;
  }
};
