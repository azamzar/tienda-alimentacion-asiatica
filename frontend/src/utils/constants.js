/**
 * Constantes de la aplicación
 */

// Estados de pedido
export const ORDER_STATUS = {
  PENDING: 'pending',
  CONFIRMED: 'confirmed',
  PROCESSING: 'processing',
  SHIPPED: 'shipped',
  DELIVERED: 'delivered',
  CANCELLED: 'cancelled'
};

// Traducciones de estados de pedido
export const ORDER_STATUS_LABELS = {
  [ORDER_STATUS.PENDING]: 'Pendiente',
  [ORDER_STATUS.CONFIRMED]: 'Confirmado',
  [ORDER_STATUS.PROCESSING]: 'En proceso',
  [ORDER_STATUS.SHIPPED]: 'Enviado',
  [ORDER_STATUS.DELIVERED]: 'Entregado',
  [ORDER_STATUS.CANCELLED]: 'Cancelado'
};

// Colores para estados de pedido
export const ORDER_STATUS_COLORS = {
  [ORDER_STATUS.PENDING]: '#FFA500',
  [ORDER_STATUS.CONFIRMED]: '#4CAF50',
  [ORDER_STATUS.PROCESSING]: '#2196F3',
  [ORDER_STATUS.SHIPPED]: '#9C27B0',
  [ORDER_STATUS.DELIVERED]: '#4CAF50',
  [ORDER_STATUS.CANCELLED]: '#F44336'
};

// Configuración de paginación
export const PAGINATION = {
  DEFAULT_LIMIT: 20,
  MAX_LIMIT: 100
};

// Mensajes de error comunes
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Error de conexión. Por favor, verifica tu conexión a internet.',
  SERVER_ERROR: 'Error del servidor. Por favor, intenta más tarde.',
  NOT_FOUND: 'Recurso no encontrado.',
  UNAUTHORIZED: 'No autorizado. Por favor, inicia sesión.',
  VALIDATION_ERROR: 'Error de validación. Verifica los datos ingresados.'
};

// Rutas de la aplicación
export const ROUTES = {
  HOME: '/',
  PRODUCTS: '/products',
  PRODUCT_DETAIL: '/products/:id',
  CART: '/cart',
  CHECKOUT: '/checkout',
  ORDERS: '/orders',
  ORDER_DETAIL: '/orders/:id'
};

// Configuración de la API
export const API_CONFIG = {
  TIMEOUT: 10000, // 10 segundos
  RETRY_ATTEMPTS: 3
};
