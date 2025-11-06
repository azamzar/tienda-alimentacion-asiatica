import api from './api';

/**
 * Servicio para gestionar categorías
 */
export const categoryService = {
  /**
   * Obtener todas las categorías
   * @returns {Promise<Array>} Lista de categorías
   */
  getCategories: async () => {
    const { data } = await api.get('/categories/');
    return data;
  },

  /**
   * Obtener una categoría por ID
   * @param {number} id - ID de la categoría
   * @returns {Promise<Object>} Datos de la categoría
   */
  getCategoryById: async (id) => {
    const { data } = await api.get(`/categories/${id}`);
    return data;
  },

  /**
   * Crear una nueva categoría (solo admin)
   * @param {Object} categoryData - Datos de la categoría
   * @returns {Promise<Object>} Categoría creada
   */
  createCategory: async (categoryData) => {
    const { data } = await api.post('/categories/', categoryData);
    return data;
  },

  /**
   * Actualizar una categoría (solo admin)
   * @param {number} id - ID de la categoría
   * @param {Object} categoryData - Datos actualizados
   * @returns {Promise<Object>} Categoría actualizada
   */
  updateCategory: async (id, categoryData) => {
    const { data } = await api.put(`/categories/${id}`, categoryData);
    return data;
  },

  /**
   * Eliminar una categoría (solo admin)
   * @param {number} id - ID de la categoría
   * @returns {Promise<void>}
   */
  deleteCategory: async (id) => {
    await api.delete(`/categories/${id}`);
  },

  /**
   * Eliminar múltiples categorías (solo admin)
   * @param {Array<number>} categoryIds - Array de IDs de categorías
   * @returns {Promise<Object>} Resultado de la operación bulk
   */
  bulkDeleteCategories: async (categoryIds) => {
    const { data } = await api.post('/categories/bulk/delete', {
      category_ids: categoryIds
    });
    return data;
  }
};
