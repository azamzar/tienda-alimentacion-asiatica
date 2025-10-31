/**
 * Funciones utilitarias para formateo de datos
 */

/**
 * Formatear precio en euros
 * @param {number} price - Precio a formatear
 * @returns {string} Precio formateado (ej: "12,50 €")
 */
export const formatPrice = (price) => {
  if (typeof price !== 'number') return '0,00 €';
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: 'EUR'
  }).format(price);
};

/**
 * Formatear fecha
 * @param {string|Date} date - Fecha a formatear
 * @returns {string} Fecha formateada (ej: "20/10/2025, 14:30")
 */
export const formatDate = (date) => {
  if (!date) return '';
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return new Intl.DateTimeFormat('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(dateObj);
};

/**
 * Formatear fecha simple (solo día)
 * @param {string|Date} date - Fecha a formatear
 * @returns {string} Fecha formateada (ej: "20/10/2025")
 */
export const formatDateShort = (date) => {
  if (!date) return '';
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return new Intl.DateTimeFormat('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  }).format(dateObj);
};

/**
 * Truncar texto con puntos suspensivos
 * @param {string} text - Texto a truncar
 * @param {number} maxLength - Longitud máxima
 * @returns {string} Texto truncado
 */
export const truncateText = (text, maxLength = 100) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

/**
 * Obtener initiales de un nombre
 * @param {string} name - Nombre completo
 * @returns {string} Iniciales (ej: "Juan Pérez" -> "JP")
 */
export const getInitials = (name) => {
  if (!name) return '';
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .substring(0, 2);
};

/**
 * Obtener URL completa de imagen
 * Convierte rutas relativas del backend en URLs absolutas
 * @param {string} imageUrl - URL de la imagen (puede ser relativa o absoluta)
 * @returns {string} URL completa de la imagen
 */
export const getImageUrl = (imageUrl) => {
  if (!imageUrl) return 'https://placehold.co/400x300/f0f0f0/666?text=Sin+Imagen';

  // Si ya es una URL completa (http:// o https://), devolverla tal cual
  if (imageUrl.startsWith('http://') || imageUrl.startsWith('https://')) {
    return imageUrl;
  }

  // Si es una ruta relativa del backend, agregar la base URL
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
  return `${API_BASE_URL}${imageUrl}`;
};
