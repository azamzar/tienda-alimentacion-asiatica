import { create } from 'zustand';
import { orderService } from '../services/orderService';

/**
 * Store de Zustand para gestionar pedidos
 * NOTA: Requiere que el usuario esté autenticado
 */
const useOrderStore = create((set, get) => ({
  // Estado
  orders: [],
  currentOrder: null,
  loading: false,
  error: null,

  // Crear un pedido desde el carrito (requiere autenticación)
  createOrder: async (orderData) => {
    set({ loading: true, error: null });
    try {
      const order = await orderService.createOrder(orderData);
      set({
        currentOrder: order,
        loading: false
      });
      return order;
    } catch (error) {
      set({
        loading: false,
        error: error.response?.data?.detail || 'Error al crear el pedido'
      });
      throw error;
    }
  },

  // Obtener todos los pedidos del usuario autenticado
  fetchOrders: async (filters = {}) => {
    set({ loading: true, error: null });
    try {
      const orders = await orderService.getOrders(filters);
      set({ orders, loading: false });
    } catch (error) {
      set({
        loading: false,
        error: error.response?.data?.detail || 'Error al cargar pedidos'
      });
    }
  },

  // Obtener un pedido específico
  fetchOrderById: async (orderId) => {
    set({ loading: true, error: null });
    try {
      const order = await orderService.getOrderById(orderId);
      set({ currentOrder: order, loading: false });
    } catch (error) {
      set({
        loading: false,
        error: error.response?.data?.detail || 'Error al cargar el pedido'
      });
    }
  },

  // Cancelar un pedido
  cancelOrder: async (orderId) => {
    set({ loading: true, error: null });
    try {
      const order = await orderService.cancelOrder(orderId);
      // Actualizar el pedido en la lista
      set((state) => ({
        orders: state.orders.map((o) =>
          o.id === orderId ? order : o
        ),
        currentOrder: state.currentOrder?.id === orderId ? order : state.currentOrder,
        loading: false
      }));
      return order;
    } catch (error) {
      set({
        loading: false,
        error: error.response?.data?.detail || 'Error al cancelar el pedido'
      });
      throw error;
    }
  },

  // Limpiar pedido actual
  clearCurrentOrder: () => set({ currentOrder: null }),

  // Limpiar error
  clearError: () => set({ error: null })
}));

export { useOrderStore };
export default useOrderStore;
