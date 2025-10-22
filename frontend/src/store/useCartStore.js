import { create } from 'zustand';
import { cartService } from '../services/cartService';

/**
 * Store de Zustand para gestionar el carrito de compras
 */
const useCartStore = create((set, get) => ({
  // Estado
  userId: null,
  items: [],
  totalItems: 0,
  totalAmount: 0,
  loading: false,
  error: null,

  // Inicializar userId (generar UUID temporal o cargar desde localStorage)
  initializeUserId: () => {
    let userId = localStorage.getItem('userId');
    if (!userId) {
      // Generar UUID simple
      userId = 'user-' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('userId', userId);
    }
    set({ userId });
    return userId;
  },

  // Obtener carrito del servidor
  fetchCart: async () => {
    const { userId } = get();
    if (!userId) {
      console.error('No userId available');
      return;
    }

    set({ loading: true, error: null });
    try {
      const cart = await cartService.getCart(userId);
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
      } else {
        set({
          loading: false,
          error: error.response?.data?.detail || 'Error al cargar el carrito'
        });
      }
    }
  },

  // Agregar producto al carrito
  addItem: async (productId, quantity = 1) => {
    const { userId } = get();
    if (!userId) {
      console.error('No userId available');
      return;
    }

    set({ loading: true, error: null });
    try {
      const cart = await cartService.addToCart(userId, {
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
    const { userId } = get();
    if (!userId) {
      console.error('No userId available');
      return;
    }

    set({ loading: true, error: null });
    try {
      const cart = await cartService.updateCartItem(userId, productId, quantity);
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
    const { userId } = get();
    if (!userId) {
      console.error('No userId available');
      return;
    }

    set({ loading: true, error: null });
    try {
      const cart = await cartService.removeFromCart(userId, productId);
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
    const { userId } = get();
    if (!userId) {
      console.error('No userId available');
      return;
    }

    set({ loading: true, error: null });
    try {
      await cartService.clearCart(userId);
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

export default useCartStore;
