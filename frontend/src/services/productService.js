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
  }
};
