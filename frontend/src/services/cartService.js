import api from './api';

/**
 * Servicio para gestionar el carrito de compras
 * NOTA: Todos los endpoints requieren autenticación JWT
 * El user_id se obtiene automáticamente del token
 */
export const cartService = {
  /**
   * Obtener el carrito del usuario autenticado
   * @returns {Promise<Object>} Datos del carrito con items y totales
   */
  getCart: async () => {
    const { data } = await api.get('/carts/me');
    return data;
  },

  /**
   * Agregar un producto al carrito del usuario autenticado
   * Si el producto ya existe, incrementa la cantidad
   * @param {Object} item - Datos del item
   * @param {number} item.product_id - ID del producto
   * @param {number} item.quantity - Cantidad a agregar
   * @returns {Promise<Object>} Carrito actualizado
   */
  addToCart: async (item) => {
    const { data } = await api.post('/carts/me/items', item);
    return data;
  },

  /**
   * Actualizar la cantidad de un producto en el carrito
   * @param {number} productId - ID del producto
   * @param {number} quantity - Nueva cantidad
   * @returns {Promise<Object>} Carrito actualizado
   */
  updateCartItem: async (productId, quantity) => {
    const { data } = await api.put(`/carts/me/items/${productId}`, {
      quantity
    });
    return data;
  },

  /**
   * Eliminar un producto del carrito
   * @param {number} productId - ID del producto a eliminar
   * @returns {Promise<Object>} Carrito actualizado
   */
  removeFromCart: async (productId) => {
    const { data } = await api.delete(`/carts/me/items/${productId}`);
    return data;
  },

  /**
   * Vaciar el carrito completamente
   * @returns {Promise<Object>} Respuesta con mensaje de confirmación
   */
  clearCart: async () => {
    const { data } = await api.delete('/carts/me');
    return data;
  }
};
