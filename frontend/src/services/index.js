// Exportar todos los servicios desde un solo archivo
// Esto permite importar múltiples servicios más fácilmente:
// import { productService, cartService } from './services';

export { productService } from './productService';
export { categoryService } from './categoryService';
export { cartService } from './cartService';
export { orderService } from './orderService';
export { default as api } from './api';
