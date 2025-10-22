/**
 * Funciones de validación para formularios
 */

/**
 * Validar email
 * @param {string} email - Email a validar
 * @returns {boolean} True si es válido
 */
export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validar teléfono español
 * @param {string} phone - Teléfono a validar
 * @returns {boolean} True si es válido
 */
export const isValidPhone = (phone) => {
  // Acepta formatos: +34 612 345 678, 612345678, 612 34 56 78
  const phoneRegex = /^(\+34|0034)?[\s\-]?[6-9]\d{2}[\s\-]?\d{2}[\s\-]?\d{2}[\s\-]?\d{2}$/;
  return phoneRegex.test(phone);
};

/**
 * Validar que un campo no esté vacío
 * @param {string} value - Valor a validar
 * @returns {boolean} True si no está vacío
 */
export const isNotEmpty = (value) => {
  return value && value.trim().length > 0;
};

/**
 * Validar longitud mínima
 * @param {string} value - Valor a validar
 * @param {number} minLength - Longitud mínima
 * @returns {boolean} True si cumple la longitud mínima
 */
export const hasMinLength = (value, minLength) => {
  return value && value.length >= minLength;
};

/**
 * Validar que sea un número positivo
 * @param {number} value - Valor a validar
 * @returns {boolean} True si es positivo
 */
export const isPositiveNumber = (value) => {
  return typeof value === 'number' && value > 0;
};

/**
 * Validar formulario de checkout
 * @param {Object} formData - Datos del formulario
 * @returns {Object} Objeto con errores { field: 'mensaje de error' }
 */
export const validateCheckoutForm = (formData) => {
  const errors = {};

  if (!isNotEmpty(formData.customer_name)) {
    errors.customer_name = 'El nombre es requerido';
  }

  if (!isValidEmail(formData.customer_email)) {
    errors.customer_email = 'El email no es válido';
  }

  if (!isValidPhone(formData.customer_phone)) {
    errors.customer_phone = 'El teléfono no es válido';
  }

  if (!isNotEmpty(formData.shipping_address)) {
    errors.shipping_address = 'La dirección de envío es requerida';
  } else if (!hasMinLength(formData.shipping_address, 10)) {
    errors.shipping_address = 'La dirección debe tener al menos 10 caracteres';
  }

  return errors;
};
