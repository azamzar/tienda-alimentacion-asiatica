// Exportar todos los stores desde un solo archivo
// Esto permite importar múltiples stores más fácilmente:
// import { useCartStore, useProductStore } from './store';

export { default as useCartStore } from './useCartStore';
export { default as useProductStore } from './useProductStore';
export { default as useOrderStore } from './useOrderStore';
