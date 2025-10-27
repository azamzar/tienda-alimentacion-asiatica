import { create } from 'zustand';
import authService from '../services/authService';

/**
 * Store de autenticación con Zustand
 * Maneja el estado global de autenticación del usuario
 */
const useAuthStore = create((set, get) => ({
  // Estado
  user: authService.getStoredUser(),
  isAuthenticated: authService.isAuthenticated(),
  isLoading: false,
  error: null,

  // Acciones

  /**
   * Registrar un nuevo usuario
   */
  register: async (userData) => {
    set({ isLoading: true, error: null });
    try {
      const user = await authService.register(userData);

      // Después del registro, hacer login automáticamente
      await get().login({
        email: userData.email,
        password: userData.password
      });

      return user;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Error al registrar usuario';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  /**
   * Iniciar sesión
   */
  login: async (credentials) => {
    set({ isLoading: true, error: null });
    try {
      await authService.login(credentials);

      // Obtener información del usuario
      const user = await authService.getCurrentUser();

      set({
        user,
        isAuthenticated: true,
        isLoading: false,
        error: null
      });

      return user;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Error al iniciar sesión';
      set({
        error: errorMessage,
        isLoading: false,
        isAuthenticated: false,
        user: null
      });
      throw error;
    }
  },

  /**
   * Cerrar sesión
   */
  logout: () => {
    authService.logout();
    set({
      user: null,
      isAuthenticated: false,
      error: null
    });
  },

  /**
   * Verificar y cargar el usuario actual (al iniciar la app)
   */
  checkAuth: async () => {
    if (!authService.isAuthenticated()) {
      set({ isAuthenticated: false, user: null });
      return;
    }

    set({ isLoading: true });
    try {
      const user = await authService.getCurrentUser();
      set({
        user,
        isAuthenticated: true,
        isLoading: false
      });
    } catch (error) {
      // Si el token es inválido, cerrar sesión
      authService.logout();
      set({
        user: null,
        isAuthenticated: false,
        isLoading: false
      });
    }
  },

  /**
   * Limpiar errores
   */
  clearError: () => {
    set({ error: null });
  },

  /**
   * Verificar si el usuario es admin
   */
  isAdmin: () => {
    const { user } = get();
    return user?.role === 'admin';
  },
}));

export { useAuthStore };
export default useAuthStore;
