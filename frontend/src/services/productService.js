import api from './api';

/**
 * Servicio para gestionar productos
 */
export const productService = {
  /**
   * Obtener todos los productos con filtros y paginación
   * @param {Object} params - Parámetros de búsqueda
   * @param {number} params.skip - Registros a omitir
   * @param {number} params.limit - Límite de registros
   * @param {number} params.category_id - Filtrar por categoría
   * @returns {Promise<Array>} Lista de productos
   */
  getProducts: async (params = {}) => {
    const { data } = await api.get('/products/', { params });
    return data;
  },

  /**
   * Obtener un producto por ID
   * @param {number} id - ID del producto
   * @returns {Promise<Object>} Datos del producto
   */
  getProductById: async (id) => {
    const { data } = await api.get(`/products/${id}`);
    return data;
  },

  /**
   * Buscar productos por nombre
   * @param {string} name - Nombre a buscar
   * @returns {Promise<Array>} Lista de productos encontrados
   */
  searchProducts: async (name) => {
    const { data } = await api.get('/products/search/', {
      params: { name }
    });
    return data;
  },

  /**
   * Obtener productos con bajo stock
   * @param {number} threshold - Umbral de stock
   * @returns {Promise<Array>} Productos con bajo stock
   */
  getLowStockProducts: async (threshold = 10) => {
    const { data } = await api.get('/products/low-stock/', {
      params: { threshold }
    });
    return data;
  },

  /**
   * Crear un nuevo producto (solo admin)
   * @param {Object} productData - Datos del producto
   * @returns {Promise<Object>} Producto creado
   */
  createProduct: async (productData) => {
    const { data } = await api.post('/products/', productData);
    return data;
  },

  /**
   * Actualizar un producto (solo admin)
   * @param {number} id - ID del producto
   * @param {Object} productData - Datos a actualizar
   * @returns {Promise<Object>} Producto actualizado
   */
  updateProduct: async (id, productData) => {
    const { data } = await api.put(`/products/${id}`, productData);
    return data;
  },

  /**
   * Eliminar un producto (solo admin)
   * @param {number} id - ID del producto
   * @returns {Promise<void>}
   */
  deleteProduct: async (id) => {
    await api.delete(`/products/${id}`);
  },

  /**
   * Subir imagen para un producto (solo admin)
   * @param {number} id - ID del producto
   * @param {File} file - Archivo de imagen
   * @returns {Promise<Object>} Producto actualizado
   */
  uploadProductImage: async (id, file) => {
    const formData = new FormData();
    formData.append('file', file);

    const { data } = await api.post(`/products/${id}/image`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return data;
  },

  /**
   * Eliminar imagen de un producto (solo admin)
   * @param {number} id - ID del producto
   * @returns {Promise<Object>} Producto actualizado
   */
  deleteProductImage: async (id) => {
    const { data } = await api.delete(`/products/${id}/image`);
    return data;
  },

  /**
   * Eliminar múltiples productos (solo admin)
   * @param {number[]} productIds - Array de IDs de productos a eliminar
   * @returns {Promise<Object>} Resultado de la operación
   */
  bulkDeleteProducts: async (productIds) => {
    const { data } = await api.post('/products/bulk/delete', {
      product_ids: productIds
    });
    return data;
  },

  /**
   * Actualizar múltiples productos (solo admin)
   * @param {number[]} productIds - Array de IDs de productos a actualizar
   * @param {Object} updateData - Datos a actualizar
   * @returns {Promise<Object>} Resultado de la operación
   */
  bulkUpdateProducts: async (productIds, updateData) => {
    const { data } = await api.patch('/products/bulk/update', {
      product_ids: productIds,
      update_data: updateData
    });
    return data;
  },

  /**
   * Exportar productos a CSV (solo admin)
   * @param {Object} filters - Filtros de exportación
   * @param {number} filters.category_id - Filtrar por categoría (opcional)
   * @returns {Promise<Blob>} Archivo CSV como blob
   */
  exportProductsCSV: async (filters = {}) => {
    const response = await api.get('/products/export/csv', {
      params: filters,
      responseType: 'blob'
    });
    return response.data;
  }
};
