import { create } from 'zustand';
import { productService } from '../services/productService';
import { categoryService } from '../services/categoryService';

/**
 * Store de Zustand para gestionar productos y categorías
 */
const useProductStore = create((set, get) => ({
  // Estado
  products: [],
  categories: [],
  selectedCategory: null,
  searchQuery: '',
  loading: false,
  error: null,

  // Obtener todos los productos
  fetchProducts: async (params = {}) => {
    set({ loading: true, error: null });
    try {
      const products = await productService.getProducts(params);
      set({ products, loading: false });
    } catch (error) {
      set({
        loading: false,
        error: error.response?.data?.detail || 'Error al cargar productos'
      });
    }
  },

  // Obtener productos filtrados por categoría
  fetchProductsByCategory: async (categoryId) => {
    set({ loading: true, error: null, selectedCategory: categoryId });
    try {
      const products = await productService.getProducts({
        category_id: categoryId
      });
      set({ products, loading: false });
    } catch (error) {
      set({
        loading: false,
        error: error.response?.data?.detail || 'Error al cargar productos'
      });
    }
  },

  // Buscar productos por nombre
  searchProducts: async (searchQuery) => {
    if (!searchQuery.trim()) {
      // Si no hay búsqueda, cargar todos los productos
      get().fetchProducts();
      return;
    }

    set({ loading: true, error: null, searchQuery });
    try {
      const products = await productService.searchProducts(searchQuery);
      set({ products, loading: false });
    } catch (error) {
      set({
        loading: false,
        error: error.response?.data?.detail || 'Error al buscar productos'
      });
    }
  },

  // Obtener todas las categorías
  fetchCategories: async () => {
    try {
      const categories = await categoryService.getCategories();
      set({ categories });
    } catch (error) {
      console.error('Error al cargar categorías:', error);
    }
  },

  // Setear categoría seleccionada y filtrar
  setSelectedCategory: (categoryId) => {
    set({ selectedCategory: categoryId });
    if (categoryId) {
      get().fetchProductsByCategory(categoryId);
    } else {
      get().fetchProducts();
    }
  },

  // Setear query de búsqueda
  setSearchQuery: (query) => {
    set({ searchQuery: query });
  },

  // Limpiar filtros
  clearFilters: () => {
    set({ selectedCategory: null, searchQuery: '' });
    get().fetchProducts();
  },

  // Limpiar error
  clearError: () => set({ error: null })
}));

export default useProductStore;
