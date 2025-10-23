import axios from 'axios';

// Base URL del backend - se puede configurar con variable de entorno
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Crear instancia de axios con configuración base
const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 segundos timeout
});

// Interceptor para requests - agregar token de autenticación
api.interceptors.request.use(
  (config) => {
    // Obtener token del localStorage
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para responses - manejo centralizado de errores
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Manejo de errores común
    if (error.response) {
      // El servidor respondió con un código de error
      console.error('Error Response:', error.response.data);

      // Puedes manejar errores específicos aquí
      switch (error.response.status) {
        case 401:
          // No autorizado - redirigir a login
          console.error('No autorizado');
          break;
        case 404:
          console.error('Recurso no encontrado');
          break;
        case 500:
          console.error('Error del servidor');
          break;
        default:
          console.error('Error:', error.response.data.detail || error.message);
      }
    } else if (error.request) {
      // La petición se hizo pero no hubo respuesta
      console.error('No se recibió respuesta del servidor');
    } else {
      // Algo pasó al configurar la petición
      console.error('Error:', error.message);
    }

    return Promise.reject(error);
  }
);

export default api;
