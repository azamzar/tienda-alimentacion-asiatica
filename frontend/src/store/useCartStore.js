import { create } from 'zustand';
import { cartService } from '../services/cartService';

/**
 * Store de Zustand para gestionar el carrito de compras
 * NOTA: Requiere que el usuario esté autenticado
 */
const useCartStore = create((set, get) => ({
  // Estado
  items: [],
  totalItems: 0,
  totalAmount: 0,
  loading: false,
  error: null,

  // Obtener carrito del servidor (requiere autenticación)
  fetchCart: async () => {
    set({ loading: true, error: null });
    try {
      const cart = await cartService.getCart();
      set({
        items: cart.items || [],
        totalItems: cart.total_items || 0,
        totalAmount: cart.total_amount || 0,
        loading: false
      });
    } catch (error) {
      // Si el carrito no existe (404), inicializarlo vacío
      if (error.response?.status === 404) {
        set({
          items: [],
          totalItems: 0,
          totalAmount: 0,
          loading: false,
          error: null
        });
      } else if (error.response?.status === 401) {
        // No autenticado - no mostrar error, simplemente limpiar el carrito
        set({
          items: [],
          totalItems: 0,
          totalAmount: 0,
          loading: false,
          error: null
        });
      } else {
        set({
          loading: false,
          error: error.response?.data?.detail || 'Error al cargar el carrito'
        });
      }
    }
  },

  // Agregar producto al carrito (requiere autenticación)
  addItem: async (productId, quantity = 1) => {
    set({ loading: true, error: null });
    try {
      const cart = await cartService.addToCart({
        product_id: productId,
        quantity
      });
      set({
        items: cart.items || [],
        totalItems: cart.total_items || 0,
        totalAmount: cart.total_amount || 0,
        loading: false
      });
    } catch (error) {
      set({
        loading: false,
        error: error.response?.data?.detail || 'Error al agregar producto'
      });
      throw error;
    }
  },

  // Actualizar cantidad de un producto
  updateItem: async (productId, quantity) => {
    set({ loading: true, error: null });
    try {
      const cart = await cartService.updateCartItem(productId, quantity);
      set({
        items: cart.items || [],
        totalItems: cart.total_items || 0,
        totalAmount: cart.total_amount || 0,
        loading: false
      });
    } catch (error) {
      set({
        loading: false,
        error: error.response?.data?.detail || 'Error al actualizar producto'
      });
      throw error;
    }
  },

  // Eliminar producto del carrito
  removeItem: async (productId) => {
    set({ loading: true, error: null });
    try {
      const cart = await cartService.removeFromCart(productId);
      set({
        items: cart.items || [],
        totalItems: cart.total_items || 0,
        totalAmount: cart.total_amount || 0,
        loading: false
      });
    } catch (error) {
      set({
        loading: false,
        error: error.response?.data?.detail || 'Error al eliminar producto'
      });
      throw error;
    }
  },

  // Vaciar carrito
  clearCart: async () => {
    set({ loading: true, error: null });
    try {
      await cartService.clearCart();
      set({
        items: [],
        totalItems: 0,
        totalAmount: 0,
        loading: false
      });
    } catch (error) {
      set({
        loading: false,
        error: error.response?.data?.detail || 'Error al vaciar carrito'
      });
      throw error;
    }
  },

  // Limpiar error
  clearError: () => set({ error: null })
}));

export { useCartStore };
export default useCartStore;
