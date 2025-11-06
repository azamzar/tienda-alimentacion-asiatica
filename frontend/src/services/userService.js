import api from './api';

/**
 * Servicio para gestionar usuarios (solo admin)
 */
export const userService = {
  /**
   * Obtener todos los usuarios
   * @param {Object} params - Parámetros de filtrado
   * @param {number} params.skip - Número de registros a saltar
   * @param {number} params.limit - Límite de registros
   * @param {string} params.role - Filtrar por rol (customer/admin)
   * @param {boolean} params.is_active - Filtrar por estado activo
   * @returns {Promise<Array>} Lista de usuarios
   */
  getUsers: async (params = {}) => {
    const { data } = await api.get('/users/', { params });
    return data;
  },

  /**
   * Obtener estadísticas de usuarios
   * @returns {Promise<Object>} Estadísticas de usuarios
   */
  getUserStats: async () => {
    const { data } = await api.get('/users/stats');
    return data;
  },

  /**
   * Obtener un usuario por ID
   * @param {number} id - ID del usuario
   * @returns {Promise<Object>} Datos del usuario
   */
  getUserById: async (id) => {
    const { data } = await api.get(`/users/${id}`);
    return data;
  },

  /**
   * Actualizar un usuario (solo admin)
   * @param {number} id - ID del usuario
   * @param {Object} userData - Datos actualizados
   * @returns {Promise<Object>} Usuario actualizado
   */
  updateUser: async (id, userData) => {
    const { data } = await api.put(`/users/${id}`, userData);
    return data;
  },

  /**
   * Desactivar un usuario (soft delete, solo admin)
   * @param {number} id - ID del usuario
   * @returns {Promise<Object>} Usuario desactivado
   */
  deleteUser: async (id) => {
    const { data } = await api.delete(`/users/${id}`);
    return data;
  },

  /**
   * Cambiar rol de un usuario (solo admin)
   * @param {number} id - ID del usuario
   * @param {string} role - Nuevo rol ('customer' o 'admin')
   * @returns {Promise<Object>} Usuario actualizado
   */
  changeUserRole: async (id, role) => {
    const { data } = await api.patch(`/users/${id}/role`, { role });
    return data;
  },

  /**
   * Resetear contraseña de un usuario (solo admin)
   * @param {number} id - ID del usuario
   * @param {string} newPassword - Nueva contraseña
   * @returns {Promise<Object>} Usuario actualizado
   */
  resetUserPassword: async (id, newPassword) => {
    const { data } = await api.post(`/users/${id}/reset-password`, {
      new_password: newPassword
    });
    return data;
  }
};
