// Exportar todos los stores desde un solo archivo
// Esto permite importar múltiples stores más fácilmente:
// import { useCartStore, useProductStore, useAuthStore } from './store';

export { default as useAuthStore } from './useAuthStore';
export { default as useCartStore } from './useCartStore';
export { default as useProductStore } from './useProductStore';
export { default as useOrderStore } from './useOrderStore';
