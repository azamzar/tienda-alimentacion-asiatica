import api from './api';

/**
 * Servicio de autenticación
 * Maneja todas las operaciones relacionadas con autenticación de usuarios
 */

const TOKEN_KEY = 'access_token';
const USER_KEY = 'user';

const authService = {
  /**
   * Registrar un nuevo usuario
   * @param {Object} userData - { email, password, full_name }
   * @returns {Promise<Object>} Usuario creado
   */
  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  /**
   * Iniciar sesión
   * @param {Object} credentials - { email, password }
   * @returns {Promise<Object>} { access_token, token_type }
   */
  login: async (credentials) => {
    const response = await api.post('/auth/login', credentials);
    const { access_token, token_type } = response.data;

    // Guardar token en localStorage
    if (access_token) {
      localStorage.setItem(TOKEN_KEY, access_token);
    }

    return response.data;
  },

  /**
   * Cerrar sesión
   * Limpia el token y datos del usuario del almacenamiento local
   */
  logout: () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  },

  /**
   * Obtener información del usuario actual
   * @returns {Promise<Object>} Usuario actual
   */
  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    const user = response.data;

    // Guardar usuario en localStorage
    if (user) {
      localStorage.setItem(USER_KEY, JSON.stringify(user));
    }

    return user;
  },

  /**
   * Obtener el token de acceso del almacenamiento local
   * @returns {string|null} Token de acceso
   */
  getToken: () => {
    return localStorage.getItem(TOKEN_KEY);
  },

  /**
   * Verificar si el usuario está autenticado
   * @returns {boolean} True si hay un token guardado
   */
  isAuthenticated: () => {
    return !!localStorage.getItem(TOKEN_KEY);
  },

  /**
   * Obtener el usuario guardado en localStorage
   * @returns {Object|null} Usuario o null
   */
  getStoredUser: () => {
    const userStr = localStorage.getItem(USER_KEY);
    return userStr ? JSON.parse(userStr) : null;
  },

  /**
   * Verificar si el usuario es administrador
   * @returns {boolean} True si el usuario es admin
   */
  isAdmin: () => {
    const user = authService.getStoredUser();
    return user?.role === 'admin';
  },
};

export default authService;
