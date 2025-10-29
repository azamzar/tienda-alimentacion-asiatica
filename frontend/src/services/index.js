// Exportar todos los servicios desde un solo archivo
// Esto permite importar múltiples servicios más fácilmente:
// import { productService, cartService, authService } from './services';

export { default as authService } from './authService';
export { productService } from './productService';
export { categoryService } from './categoryService';
export { cartService } from './cartService';
export { orderService } from './orderService';
export { dashboardService } from './dashboardService';
export { default as api } from './api';
