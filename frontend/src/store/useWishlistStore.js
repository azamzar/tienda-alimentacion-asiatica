import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import wishlistService from '../services/wishlistService';

/**
 * Store de Zustand para gestionar la wishlist
 * Requiere autenticación del usuario
 */
const useWishlistStore = create(
  persist(
    (set, get) => ({
      // Estado
      wishlistItems: [],
      wishlistCount: 0,
      loading: false,
      error: null,

      // Cargar wishlist desde el servidor
      fetchWishlist: async () => {
        set({ loading: true, error: null });
        try {
          const items = await wishlistService.getWishlist();
          const count = items.length;
          set({ wishlistItems: items, wishlistCount: count, loading: false });
        } catch (error) {
          set({
            loading: false,
            error: error.response?.data?.detail || 'Error al cargar la wishlist'
          });
        }
      },

      // Cargar solo el contador (más ligero)
      fetchWishlistCount: async () => {
        try {
          const count = await wishlistService.getWishlistCount();
          set({ wishlistCount: count });
        } catch (error) {
          console.error('Error fetching wishlist count:', error);
        }
      },

      // Verificar si un producto está en la wishlist
      isInWishlist: (productId) => {
        const { wishlistItems } = get();
        return wishlistItems.some(item => item.product_id === productId);
      },

      // Agregar producto a la wishlist
      addToWishlist: async (productId) => {
        set({ loading: true, error: null });
        try {
          const item = await wishlistService.addToWishlist(productId);
          set((state) => ({
            wishlistItems: [...state.wishlistItems, item],
            wishlistCount: state.wishlistCount + 1,
            loading: false
          }));
          return item;
        } catch (error) {
          set({
            loading: false,
            error: error.response?.data?.detail || 'Error al agregar a favoritos'
          });
          throw error;
        }
      },

      // Remover producto de la wishlist
      removeFromWishlist: async (productId) => {
        set({ loading: true, error: null });
        try {
          await wishlistService.removeFromWishlist(productId);
          set((state) => ({
            wishlistItems: state.wishlistItems.filter(item => item.product_id !== productId),
            wishlistCount: Math.max(0, state.wishlistCount - 1),
            loading: false
          }));
        } catch (error) {
          set({
            loading: false,
            error: error.response?.data?.detail || 'Error al quitar de favoritos'
          });
          throw error;
        }
      },

      // Toggle: agregar o quitar de wishlist
      toggleWishlist: async (productId) => {
        const { isInWishlist, addToWishlist, removeFromWishlist } = get();

        if (isInWishlist(productId)) {
          await removeFromWishlist(productId);
          return false; // removed
        } else {
          await addToWishlist(productId);
          return true; // added
        }
      },

      // Limpiar wishlist
      clearWishlist: async () => {
        set({ loading: true, error: null });
        try {
          await wishlistService.clearWishlist();
          set({ wishlistItems: [], wishlistCount: 0, loading: false });
        } catch (error) {
          set({
            loading: false,
            error: error.response?.data?.detail || 'Error al limpiar la wishlist'
          });
          throw error;
        }
      },

      // Limpiar error
      clearError: () => set({ error: null }),

      // Reset store (útil para logout)
      reset: () => set({
        wishlistItems: [],
        wishlistCount: 0,
        loading: false,
        error: null
      })
    }),
    {
      name: 'wishlist-storage', // nombre en localStorage
      partialize: (state) => ({
        // Solo persistir estos campos
        wishlistCount: state.wishlistCount
      })
    }
  )
);

export { useWishlistStore };
export default useWishlistStore;
