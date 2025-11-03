# Tienda Alimentación Asiática - Frontend

Frontend de la aplicación de tienda de alimentación asiática, desarrollado con React + Vite.

## Estado del Proyecto

✅ **Fase 1: Arquitectura Base (Completado)**
- [x] Estructura de carpetas modular
- [x] Capa de servicios API con Axios
- [x] Stores de Zustand para estado global
- [x] Funciones utilitarias
- [x] Dependencias instaladas

✅ **Fase 2: Componentes y Páginas (Completado)**
- [x] React Router configurado
- [x] Componentes UI reutilizables
- [x] Páginas principales implementadas
- [x] Sistema de autenticación completo
- [x] Carrito de compras y checkout
- [x] Gestión de pedidos para clientes
- [x] Panel de administración de productos

✅ **Fase 3: Funcionalidades Avanzadas (Completado)**
- [x] Estilos y diseño responsive
- [x] Dashboard de administración con estadísticas
- [x] Optimizaciones de rendimiento
- [x] Tests

## Tabla de Contenidos

- [Estado del Proyecto](#estado-del-proyecto)
- [Tecnologías](#tecnologías)
- [Arquitectura](#arquitectura)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación y Ejecución](#instalación-y-ejecución)
- [Dependencias Principales](#dependencias-principales)
- [Implementación Actual](#implementación-actual)
- [Páginas y Rutas](#páginas-y-rutas)
- [Gestión de Estado](#gestión-de-estado)
- [Servicios API](#servicios-api)
- [Utilidades](#utilidades)
- [Componentes](#componentes)
- [Desarrollo](#desarrollo)

---

## Tecnologías

- **React 18** - Librería UI
- **Vite** - Build tool y dev server
- **React Router DOM v6** - Enrutamiento y navegación
- **Zustand** - Gestión de estado global
- **Axios** - Cliente HTTP para API
- **CSS Modules** - Estilos modulares

## Arquitectura

El frontend sigue una arquitectura modular y escalable:

```
┌──────────────────────────────────────┐
│         Pages (Vistas)               │  ← Páginas principales
├──────────────────────────────────────┤
│      Components (UI Components)      │  ← Componentes reutilizables
├──────────────────────────────────────┤
│       Store (State Management)       │  ← Zustand stores
├──────────────────────────────────────┤
│       Services (API Layer)           │  ← Llamadas HTTP con Axios
├──────────────────────────────────────┤
│       Backend API (FastAPI)          │  ← http://localhost:8000
└──────────────────────────────────────┘
```

### Principios de Arquitectura

1. **Separación de Responsabilidades**: Cada carpeta tiene un propósito específico
2. **Componentes Reutilizables**: UI components desacoplados de la lógica de negocio
3. **Estado Global Centralizado**: Zustand para cart, products, user
4. **Capa de Servicios**: Toda comunicación con API centralizada
5. **Enrutamiento Declarativo**: React Router para navegación

## Estructura del Proyecto

```
frontend/
├── src/
│   ├── components/           # Componentes reutilizables
│   │   ├── common/          # Componentes genéricos (Button, Input, Card, Modal, Spinner)
│   │   ├── layout/          # Layout components (Header, Footer)
│   │   ├── auth/            # Componentes de autenticación (ProtectedRoute)
│   │   ├── products/        # Componentes relacionados con productos (ProductCard, ProductGrid)
│   │   ├── cart/            # Componentes del carrito (CartItem, CartSummary)
│   │   ├── orders/          # Componentes de pedidos (OrderStatusBadge)
│   │   └── admin/           # Componentes de administración (ProductTable, ProductFormModal)
│   │
│   ├── pages/               # Páginas/Vistas principales
│   │   ├── HomePage.jsx     # Página principal con hero y productos destacados
│   │   ├── ProductsPage.jsx # Listado de productos con filtros
│   │   ├── ProductDetailPage.jsx # Detalle de producto
│   │   ├── CartPage.jsx     # Carrito de compras
│   │   ├── CheckoutPage.jsx # Proceso de checkout
│   │   ├── OrdersPage.jsx   # Historial de pedidos
│   │   ├── OrderDetailPage.jsx # Detalle de un pedido
│   │   ├── LoginPage.jsx    # Página de inicio de sesión
│   │   ├── RegisterPage.jsx # Página de registro
│   │   ├── admin/
│   │   │   ├── AdminDashboardPage.jsx # Dashboard de admin
│   │   │   └── AdminProductsPage.jsx  # Gestión de productos (CRUD)
│   │   └── NotFoundPage.jsx # Página 404
│   │
│   ├── services/            # Capa de servicios API
│   │   ├── api.js           # Configuración base de Axios
│   │   ├── productService.js # Endpoints de productos
│   │   ├── cartService.js   # Endpoints de carrito
│   │   ├── orderService.js  # Endpoints de pedidos
│   │   └── categoryService.js # Endpoints de categorías
│   │
│   ├── store/               # Estado global con Zustand
│   │   ├── useCartStore.js  # Store del carrito
│   │   ├── useProductStore.js # Store de productos
│   │   └── useUserStore.js  # Store del usuario
│   │
│   ├── hooks/               # Custom React Hooks
│   │   ├── useProducts.js   # Hook para gestionar productos
│   │   ├── useCart.js       # Hook para gestionar carrito
│   │   └── useOrders.js     # Hook para gestionar pedidos
│   │
│   ├── utils/               # Funciones utilitarias
│   │   ├── formatters.js    # Formateo de precios, fechas, etc.
│   │   ├── validators.js    # Validaciones de formularios
│   │   └── constants.js     # Constantes de la aplicación
│   │
│   ├── routes/              # Configuración de rutas
│   │   └── AppRouter.jsx    # Definición de rutas
│   │
│   ├── App.jsx              # Componente raíz
│   ├── main.jsx             # Entry point
│   └── index.css            # Estilos globales
│
├── public/                  # Archivos estáticos
├── index.html               # HTML template
├── package.json             # Dependencias y scripts
├── vite.config.js           # Configuración de Vite
└── README.md                # Este archivo
```

## Instalación y Ejecución

### Prerrequisitos

- Node.js >= 16.x
- npm >= 8.x
- Backend corriendo en http://localhost:8000

### Instalación

1. **Navegar al directorio del frontend**
   ```bash
   cd frontend
   ```

2. **Instalar dependencias**
   ```bash
   npm install
   ```

3. **Configurar variables de entorno (opcional)**
   Crear archivo `.env` en la raíz del frontend:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```

### Ejecución

#### Modo Desarrollo

```bash
npm run dev
```

La aplicación estará disponible en: http://localhost:5173

#### Build para Producción

```bash
npm run build
```

Los archivos generados estarán en `dist/`

#### Preview de Producción

```bash
npm run preview
```

### Docker (Recomendado)

```bash
# Desde el directorio frontend
docker-compose -f docker-compose.dev.yml up --build
```

## Dependencias Principales

### react-router-dom (v6.x)

**Propósito**: Enrutamiento y navegación en la SPA

**Uso**:
```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';

<BrowserRouter>
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/products" element={<Products />} />
    <Route path="/cart" element={<Cart />} />
  </Routes>
</BrowserRouter>
```

**Por qué lo usamos**:
- Navegación sin recargar la página
- URLs amigables y bookmarkables
- Manejo de parámetros de ruta (`/products/:id`)
- Historia del navegador (back/forward)

### zustand (v4.x)

**Propósito**: Gestión de estado global (state management)

**Uso**:
```jsx
import create from 'zustand';

const useCartStore = create((set) => ({
  items: [],
  addItem: (item) => set((state) => ({
    items: [...state.items, item]
  })),
}));

// En componente
const { items, addItem } = useCartStore();
```

**Por qué lo usamos**:
- Más simple que Redux (sin boilerplate)
- API minimalista e intuitiva
- Excelente rendimiento
- No requiere Context providers
- TypeScript-friendly

**Stores implementados**:
- ✅ `useCartStore`: Gestión del carrito (items, totales, add/remove)
- ✅ `useProductStore`: Productos y categorías
- ✅ `useOrderStore`: Pedidos y órdenes

### axios (v1.x)

**Propósito**: Cliente HTTP para comunicación con backend

**Uso**:
```jsx
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1'
});

// GET request
const products = await api.get('/products');

// POST request
const cart = await api.post(`/carts/${userId}/items`, {
  product_id: 5,
  quantity: 2
});
```

**Por qué lo usamos**:
- Más potente que `fetch` nativo
- Interceptores para requests/responses
- Manejo automático de JSON
- Mejor manejo de errores
- Cancelación de requests
- Configuración global (baseURL, headers)

**Ventajas sobre fetch**:
```jsx
// Con fetch
fetch('http://localhost:8000/api/v1/products')
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));

// Con axios (más limpio)
axios.get('/products')
  .then(({ data }) => console.log(data))
  .catch(err => console.error(err));
```

## Implementación Actual

### ✅ Servicios API Implementados

Todos los servicios están en `src/services/` y usan axios para comunicarse con el backend:

#### **api.js**
Configuración base de axios con:
- Base URL: `http://localhost:8000/api/v1`
- Timeout: 10 segundos
- Interceptores para requests y responses
- Manejo centralizado de errores

#### **productService.js**
```javascript
✅ getProducts(params)           // Obtener productos con filtros
✅ getProductById(id)            // Obtener producto por ID
✅ searchProducts(name)          // Buscar por nombre
✅ getLowStockProducts(threshold)// Productos con bajo stock
✅ createProduct(data)           // Crear producto (admin)
✅ updateProduct(id, data)       // Actualizar producto (admin)
✅ deleteProduct(id)             // Eliminar producto (admin)
✅ uploadProductImage(id, file)  // Subir imagen de producto (admin)
✅ deleteProductImage(id)        // Eliminar imagen de producto (admin)
```

#### **categoryService.js**
```javascript
✅ getCategories()               // Obtener todas las categorías
✅ getCategoryById(id)           // Obtener categoría por ID
✅ createCategory(data)          // Crear categoría (admin)
✅ deleteCategory(id)            // Eliminar categoría (admin)
```

#### **cartService.js**
```javascript
✅ getCart(userId)               // Obtener carrito del usuario
✅ addToCart(userId, item)       // Agregar producto al carrito
✅ updateCartItem(userId, productId, quantity) // Actualizar cantidad
✅ removeFromCart(userId, productId) // Eliminar producto
✅ clearCart(userId)             // Vaciar carrito
```

#### **orderService.js**
```javascript
✅ createOrder(userId, orderData)    // Crear pedido desde carrito
✅ getOrders(filters)                // Obtener pedidos con filtros
✅ getOrderById(orderId, userId)     // Obtener pedido específico
✅ updateOrder(orderId, updates)     // Actualizar pedido
✅ cancelOrder(orderId, userId)      // Cancelar pedido
```

#### **userService.js**
```javascript
✅ getUsers(params)                  // Obtener usuarios con filtros (admin)
✅ getUserStats()                    // Obtener estadísticas de usuarios (admin)
✅ getUserById(id)                   // Obtener usuario por ID (admin)
✅ updateUser(id, data)              // Actualizar usuario (admin)
✅ deleteUser(id)                    // Desactivar usuario (admin)
```

### ✅ Stores de Zustand Implementados

Todos los stores están en `src/store/`:

#### **useCartStore.js**
Estado y acciones del carrito:
```javascript
// Estado
{
  userId: string,           // ID del usuario (generado o desde localStorage)
  items: CartItem[],        // Items en el carrito
  totalItems: number,       // Cantidad total
  totalAmount: number,      // Monto total
  loading: boolean,
  error: string | null
}

// Acciones
✅ initializeUserId()         // Generar/cargar userId
✅ fetchCart()                // Cargar carrito del servidor
✅ addItem(productId, qty)    // Agregar producto
✅ updateItem(productId, qty) // Actualizar cantidad
✅ removeItem(productId)      // Eliminar producto
✅ clearCart()                // Vaciar carrito
✅ clearError()               // Limpiar error
```

#### **useProductStore.js**
Estado y acciones de productos:
```javascript
// Estado
{
  products: Product[],
  categories: Category[],
  selectedCategory: number | null,
  searchQuery: string,
  loading: boolean,
  error: string | null
}

// Acciones
✅ fetchProducts(params)           // Cargar todos los productos
✅ fetchProductsByCategory(id)     // Filtrar por categoría
✅ searchProducts(query)           // Buscar productos
✅ fetchCategories()               // Cargar categorías
✅ setSelectedCategory(id)         // Setear categoría activa
✅ setSearchQuery(query)           // Setear búsqueda
✅ clearFilters()                  // Limpiar filtros
✅ clearError()                    // Limpiar error
```

#### **useOrderStore.js**
Estado y acciones de pedidos:
```javascript
// Estado
{
  orders: Order[],
  currentOrder: Order | null,
  loading: boolean,
  error: string | null
}

// Acciones
✅ createOrder(userId, data)       // Crear pedido
✅ fetchOrders(userId)             // Cargar pedidos del usuario
✅ fetchOrderById(orderId, userId) // Cargar pedido específico
✅ cancelOrder(orderId, userId)    // Cancelar pedido
✅ clearCurrentOrder()             // Limpiar pedido actual
✅ clearError()                    // Limpiar error
```

### ✅ Utilidades Implementadas

Todas las utilidades están en `src/utils/`:

#### **formatters.js**
```javascript
✅ formatPrice(price)          // Formatear precio: "12,50 €"
✅ formatDate(date)            // Formatear fecha: "20/10/2025, 14:30"
✅ formatDateShort(date)       // Formatear fecha corta: "20/10/2025"
✅ truncateText(text, length)  // Truncar texto con "..."
✅ getInitials(name)           // Obtener iniciales: "JP"
```

#### **constants.js**
```javascript
✅ ORDER_STATUS               // Estados de pedido
✅ ORDER_STATUS_LABELS        // Traducciones de estados
✅ ORDER_STATUS_COLORS        // Colores para estados
✅ PAGINATION                 // Configuración de paginación
✅ ERROR_MESSAGES             // Mensajes de error comunes
✅ ROUTES                     // Rutas de la aplicación
✅ API_CONFIG                 // Configuración de la API
```

#### **validators.js**
```javascript
✅ isValidEmail(email)         // Validar email
✅ isValidPhone(phone)         // Validar teléfono español
✅ isNotEmpty(value)           // Validar no vacío
✅ hasMinLength(value, min)    // Validar longitud mínima
✅ isPositiveNumber(value)     // Validar número positivo
✅ validateCheckoutForm(data)  // Validar formulario de checkout
```

### 📁 Estructura de Carpetas Actual

```
frontend/src/
├── services/              ✅ COMPLETADO
│   ├── api.js
│   ├── productService.js
│   ├── categoryService.js
│   ├── cartService.js
│   ├── orderService.js
│   └── index.js
│
├── store/                 ✅ COMPLETADO
│   ├── useCartStore.js
│   ├── useProductStore.js
│   ├── useOrderStore.js
│   └── index.js
│
├── utils/                 ✅ COMPLETADO
│   ├── formatters.js
│   ├── constants.js
│   └── validators.js
│
├── components/            🔄 EN PROGRESO
│   ├── common/           (vacío - por implementar)
│   ├── layout/           (vacío - por implementar)
│   ├── products/         (vacío - por implementar)
│   ├── cart/             (vacío - por implementar)
│   └── orders/           (vacío - por implementar)
│
├── pages/                 🔄 EN PROGRESO
│   └── (por implementar)
│
├── routes/                📋 PENDIENTE
│   └── (por implementar)
│
├── hooks/                 📋 PENDIENTE
│   └── (por implementar)
│
├── App.jsx               📋 PENDIENTE (por refactorizar)
├── main.jsx              ✅ COMPLETADO
└── index.css             ✅ COMPLETADO
```

## Páginas y Rutas

| Ruta | Componente | Descripción | Acceso |
|------|-----------|-------------|--------|
| `/` | HomePage | Página principal con hero y productos destacados | Público |
| `/login` | LoginPage | Inicio de sesión | Público |
| `/register` | RegisterPage | Registro de nuevos usuarios | Público |
| `/products` | ProductsPage | Listado de productos con filtros | Público |
| `/products/:id` | ProductDetailPage | Detalle de un producto | Público |
| `/cart` | CartPage | Carrito de compras | 🔒 Autenticado |
| `/checkout` | CheckoutPage | Formulario de checkout | 🔒 Autenticado |
| `/orders` | OrdersPage | Historial de pedidos del usuario | 🔒 Autenticado |
| `/orders/:id` | OrderDetailPage | Detalle de un pedido específico | 🔒 Autenticado |
| `/admin` | AdminDashboardPage | Dashboard de administración | 🔐 Admin |
| `/admin/products` | AdminProductsPage | Gestión de productos (CRUD) | 🔐 Admin |
| `/admin/categories` | AdminCategoriesPage | Gestión de categorías (CRUD) | 🔐 Admin |
| `/admin/orders` | AdminOrdersPage | Gestión de pedidos (view, update status) | 🔐 Admin |
| `/admin/users` | AdminUsersPage | Gestión de usuarios (view, edit, deactivate) | 🔐 Admin |

## Gestión de Estado

### useCartStore

**Estado**:
```javascript
{
  userId: string,           // ID del usuario actual
  items: CartItem[],        // Items en el carrito
  totalItems: number,       // Cantidad total de productos
  totalAmount: number,      // Monto total
  loading: boolean,         // Estado de carga
  error: string | null      // Mensajes de error
}
```

**Acciones**:
- `fetchCart(userId)` - Obtener carrito del servidor
- `addItem(productId, quantity)` - Agregar producto
- `updateItem(productId, quantity)` - Actualizar cantidad
- `removeItem(productId)` - Eliminar producto
- `clearCart()` - Vaciar carrito

### useProductStore

**Estado**:
```javascript
{
  products: Product[],      // Lista de productos
  categories: Category[],   // Lista de categorías
  selectedCategory: number | null,
  searchQuery: string,
  loading: boolean,
  error: string | null
}
```

**Acciones**:
- `fetchProducts()` - Cargar productos
- `fetchCategories()` - Cargar categorías
- `setSelectedCategory(id)` - Filtrar por categoría
- `setSearchQuery(query)` - Filtrar por búsqueda

### useUserStore

**Estado**:
```javascript
{
  userId: string,           // ID temporal o autenticado
  orders: Order[],          // Pedidos del usuario
}
```

**Acciones**:
- `generateUserId()` - Generar ID temporal (UUID)
- `fetchOrders()` - Cargar pedidos

## Servicios API

### productService.js

```javascript
getProducts(params)           // GET /api/v1/products
getProductById(id)            // GET /api/v1/products/{id}
searchProducts(name)          // GET /api/v1/products/search?name=
getCategories()               // GET /api/v1/categories
```

### cartService.js

```javascript
getCart(userId)               // GET /api/v1/carts/{user_id}
addToCart(userId, item)       // POST /api/v1/carts/{user_id}/items
updateCartItem(userId, productId, quantity)  // PUT /api/v1/carts/{user_id}/items/{product_id}
removeFromCart(userId, productId)            // DELETE /api/v1/carts/{user_id}/items/{product_id}
clearCart(userId)             // DELETE /api/v1/carts/{user_id}
```

### orderService.js

```javascript
createOrder(userId, orderData)    // POST /api/v1/orders?user_id={user_id}
getOrders(userId, filters)        // GET /api/v1/orders?user_id={user_id}
getOrderById(orderId, userId)     // GET /api/v1/orders/{order_id}
updateOrder(orderId, updates)     // PATCH /api/v1/orders/{order_id}
cancelOrder(orderId, userId)      // POST /api/v1/orders/{order_id}/cancel
```

## Componentes

### Layout Components

- **Header**: Navegación principal con logo, enlaces, carrito badge y menú de usuario
- **Footer**: Información de contacto y links útiles

### Auth Components

- **ProtectedRoute**: Wrapper para rutas que requieren autenticación
- **AdminRoute**: Wrapper para rutas que requieren rol de admin

### Product Components

- **ProductCard**: Tarjeta de producto con imagen, precio, stock y botón de agregar al carrito
- **ProductGrid**: Grid responsive de productos con filtros y búsqueda

### Cart Components

- **CartItem**: Item individual en el carrito con control de cantidad
- **CartSummary**: Resumen de totales y subtotales del carrito

### Order Components

- **OrderStatusBadge**: Badge visual con código de colores según estado del pedido
- **CheckoutForm**: Formulario completo de checkout con validación

### Admin Components

- **StatCard**: Tarjeta de estadística con icono y valor (usado en dashboard)
- **ProductTable**: Tabla de productos con acciones de editar y eliminar
- **ProductFormModal**: Modal para crear y editar productos con validación
- **AdminCategoryTable**: Tabla responsive de categorías con CRUD
- **CategoryFormModal**: Modal para crear y editar categorías
- **AdminOrderTable**: Tabla responsive de pedidos con filtros y búsqueda
- **OrderStatusUpdateModal**: Modal para actualizar estado de pedidos
- **AdminUserTable**: Tabla responsive de usuarios con filtros por rol y estado
- **UserFormModal**: Modal para editar información de usuarios

### Common Components

- **Button**: Botón reutilizable con variantes (primary, secondary, ghost, danger)
- **Input**: Input de formulario con validación y estados de error
- **Card**: Contenedor genérico con estilos consistentes
- **Modal**: Modal genérico con overlay y animaciones
- **Spinner**: Indicador de carga centrado
- **ImageUpload**: Componente de upload de imágenes con drag & drop, preview y validación
- **OptimizedImage**: Componente de imagen con lazy loading, carga progresiva y WebP
- **Skeleton**: Componente genérico de placeholder animado
- **ProductCardSkeleton**: Placeholder para ProductCard durante carga
- **ProductGridSkeleton**: Grid de placeholders para ProductGrid

## Optimizaciones de Rendimiento

El frontend incluye múltiples optimizaciones para mejorar el rendimiento y la experiencia de usuario.

### OptimizedImage Component

Componente avanzado de imagen con múltiples optimizaciones:

**Características:**
- ✅ **Lazy loading** con Intersection Observer
- ✅ **Carga progresiva** (thumbnail → full size)
- ✅ **Soporte WebP** con fallback automático
- ✅ **Responsive images** (srcset + sizes)
- ✅ **Blur-up effect** durante carga
- ✅ **Error handling** con imagen fallback
- ✅ Compatible con imágenes optimizadas del backend

**Uso:**
```jsx
import OptimizedImage from './components/common/OptimizedImage';

<OptimizedImage
  src={product.image_url}
  productId={product.id}
  alt="Product name"
  size="medium"          // thumbnail | medium | large
  lazy={true}
  fallback="/placeholder.png"
/>
```

**Funcionamiento:**
1. Si `lazy=true`, espera a que la imagen entre en viewport (50px antes)
2. Carga primero el thumbnail (progresivo)
3. Luego carga la versión full size
4. Aplica fade-in smooth
5. Si falla, muestra fallback

**Integración con Backend:**
- Usa automáticamente thumbnails WebP del backend
- Genera srcset para responsive images
- Soporte para URLs externas

### Skeleton Loaders

Placeholders animados que mejoran la percepción de velocidad:

**Componentes:**
- `Skeleton` - Componente base reutilizable
- `ProductCardSkeleton` - Para tarjetas de producto
- `ProductGridSkeleton` - Para grid completo

**Variantes:**
```jsx
<Skeleton variant="text" width="80%" height="20px" />
<Skeleton variant="circular" width="40px" height="40px" />
<Skeleton variant="rectangular" width="100%" height="200px" />
```

**Beneficios:**
- Mejor UX durante cargas
- Reduce frustración del usuario
- Indica estructura del contenido

### React Performance Optimizations

**ProductCard Optimizado:**

Usa `React.memo` y `useCallback` para prevenir re-renders innecesarios:

```jsx
import React, { memo, useCallback } from 'react';

const ProductCard = memo(({ product }) => {
  const handleAddToCart = useCallback(async (e) => {
    // Lógica estable
  }, [product.id]);

  return (
    <Card>
      <OptimizedImage
        src={product.image_url}
        productId={product.id}
        size="medium"
        lazy={true}
      />
      {/* ... */}
    </Card>
  );
});

ProductCard.displayName = 'ProductCard';
```

**Optimizaciones:**
- `React.memo` - Solo re-renderiza si props cambian
- `useCallback` - Referencias estables de funciones
- `OptimizedImage` - Lazy loading automático

**ProductGrid Optimizado:**

Usa `useMemo` para operaciones costosas:

```jsx
const ProductGrid = () => {
  // Memoiza filtrado (solo recalcula cuando cambian deps)
  const filteredProducts = useMemo(() => {
    return products.filter(/* ... */);
  }, [products, selectedCategory, searchQuery]);

  // Memoiza conteos de categorías
  const categoryCounts = useMemo(() => {
    const counts = new Map();
    products.forEach(/* ... */);
    return counts;
  }, [products]);

  // Handlers estables con useCallback
  const handleCategoryChange = useCallback((categoryId) => {
    setSelectedCategory(categoryId);
  }, [setSelectedCategory]);

  return (
    <>
      {loading && <ProductGridSkeleton count={8} />}
      {!loading && (
        <div className="product-grid">
          {filteredProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}
    </>
  );
};
```

**Optimizaciones:**
- `useMemo` - Evita recalcular filtros en cada render
- `useCallback` - Handlers estables para ProductCard
- Debounce search (300ms) - Reduce re-renders
- Skeleton loaders - Mejor UX de carga

### Resultados Esperados

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| Time to Interactive | ~3s | ~1.2s | **-60%** |
| Largest Contentful Paint | ~2s | ~0.8s | **-60%** |
| Total Blocking Time | ~400ms | ~150ms | **-62%** |
| Re-renders innecesarios | Muchos | Mínimos | **~80%** |
| Imágenes cargadas inicial | Todas | Solo visibles | **Lazy** |
| Tamaño imágenes | 500KB | 100KB (WebP) | **-80%** |

### Mejores Prácticas

**1. Usar OptimizedImage en lugar de `<img>`:**
```jsx
// ❌ Antes
<img src={product.image_url} alt={product.name} />

// ✅ Después
<OptimizedImage
  src={product.image_url}
  productId={product.id}
  alt={product.name}
  size="medium"
  lazy={true}
/>
```

**2. Usar Skeleton durante cargas:**
```jsx
// ❌ Antes
{loading && <Spinner />}

// ✅ Después
{loading && <ProductGridSkeleton count={8} />}
```

**3. Memoizar componentes pesados:**
```jsx
// ✅ Componente memoizado
const HeavyComponent = memo(({ data }) => {
  return <div>{/* ... */}</div>;
});
```

**4. Memoizar computaciones costosas:**
```jsx
// ✅ Filtrado memoizado
const filteredData = useMemo(() => {
  return data.filter(/* ... */);
}, [data, filters]);
```

## Desarrollo

### Flujo de Datos Típico

```
Usuario interactúa con UI
        ↓
Componente llama a función del Store (Zustand)
        ↓
Store llama a Service (Axios)
        ↓
Service hace request HTTP al Backend
        ↓
Backend responde
        ↓
Service procesa respuesta
        ↓
Store actualiza estado
        ↓
React re-renderiza componentes afectados
```

### Ejemplo Completo: Agregar al Carrito

**1. Usuario hace clic en "Agregar al carrito"**

```jsx
// ProductCard.jsx
import { useCartStore } from '../store/useCartStore';

function ProductCard({ product }) {
  const addItem = useCartStore((state) => state.addItem);

  const handleAddToCart = async () => {
    await addItem(product.id, 1);
  };

  return (
    <button onClick={handleAddToCart}>
      Agregar al carrito
    </button>
  );
}
```

**2. Store llama al servicio**

```javascript
// store/useCartStore.js
import { cartService } from '../services/cartService';

const useCartStore = create((set, get) => ({
  items: [],

  addItem: async (productId, quantity) => {
    const userId = get().userId;
    const cart = await cartService.addToCart(userId, {
      product_id: productId,
      quantity
    });
    set({
      items: cart.items,
      totalAmount: cart.total_amount
    });
  }
}));
```

**3. Servicio hace la petición HTTP**

```javascript
// services/cartService.js
import api from './api';

export const cartService = {
  addToCart: async (userId, item) => {
    const { data } = await api.post(`/carts/${userId}/items`, item);
    return data;
  }
};
```

### Convenciones de Código

- **Nombres de archivos**: PascalCase para componentes (`ProductCard.jsx`), camelCase para otros (`productService.js`)
- **Componentes**: Functional components con hooks
- **Estado**: Usar Zustand para estado global, useState para estado local
- **Estilos**: CSS Modules o clases CSS estándar
- **Imports**: Organizar en orden: React, librerías, componentes, servicios, estilos

### Testing

El frontend cuenta con una suite completa de tests utilizando **Vitest** y **React Testing Library**.

#### Framework y Dependencias

- **vitest** ^1.0.4 - Framework de testing rápido y nativo de Vite
- **@testing-library/react** ^14.1.2 - Testing de componentes React
- **@testing-library/jest-dom** ^6.1.5 - Matchers personalizados para DOM
- **@vitest/ui** ^1.0.4 - Interfaz gráfica para tests
- **@vitest/coverage-v8** ^1.0.4 - Reporte de cobertura de código
- **jsdom** ^23.0.1 - Simulación de entorno de navegador

#### Estructura de Tests

```
frontend/src/tests/
├── setup.js                           # Configuración global de tests
├── components/
│   ├── common/
│   │   ├── OptimizedImage.test.jsx   # 25 tests - Componente de imagen optimizada
│   │   └── Skeleton.test.jsx          # 15 tests - Skeleton loaders
│   └── products/
│       ├── ProductCard.test.jsx       # 34 tests - Tarjeta de producto
│       └── ProductGrid.test.jsx       # 25 tests - Grid de productos
```

#### Comandos de Testing

```bash
# Ejecutar todos los tests
npm test

# Ejecutar tests en modo watch
npm run test:watch

# Interfaz gráfica de tests
npm run test:ui

# Generar reporte de cobertura
npm run test:coverage

# Ejecutar tests específicos
npm test OptimizedImage
```

#### Configuración Global (setup.js)

Mocks globales configurados para todos los tests:

- **IntersectionObserver** - Para lazy loading de imágenes
- **matchMedia** - Para queries responsive
- **Image** - Para simular carga de imágenes
- **@testing-library/jest-dom** - Matchers personalizados

#### Tests Implementados

**OptimizedImage Component (25 tests)**
- ✅ Basic rendering (props, className, fallback alt)
- ✅ Lazy loading (placeholder, IntersectionObserver)
- ✅ Image source handling (HTTP/HTTPS, optimized URLs, /uploads/)
- ✅ Image sizes (thumbnail, medium, large)
- ✅ Error handling (fallback images)
- ✅ Responsive images (srcset, sizes attribute)
- ✅ Loading states (loading/loaded classes, loader)
- ✅ Progressive loading (thumbnail → full size)
- ✅ Loading attribute (lazy/eager)

**Skeleton Component (15 tests)**
- ✅ Rendering (default props, variants)
- ✅ Variants (text, circular, rectangular)
- ✅ Dimensions (width, height)
- ✅ Animation (animated/static)
- ✅ Combined props

**ProductCard Component (34 tests)**
- ✅ Rendering (product info, image, category, description)
- ✅ Stock status (badges for out of stock, low stock)
- ✅ Add to cart button (states, loading, disabled)
- ✅ Error handling (401 auth, server errors)
- ✅ Navigation (product detail routing)
- ✅ Price formatting (decimals, whole numbers)
- ✅ Accessibility (alt text, button labels, aria attributes)

**ProductGrid Component (25 tests)**
- ✅ Rendering (products, categories, search input, product count)
- ✅ Data fetching (products and categories on mount)
- ✅ Loading state (skeleton loader)
- ✅ Error state (error messages)
- ✅ Empty state (no products message, clear filters)
- ✅ Category filtering (filter by category, active state)
- ✅ Search functionality (debounce, filtered results)
- ✅ Clear filters (button visibility, reset)
- ✅ Product grid display (ProductCard rendering)
- ✅ Category title (dynamic title based on selection)
- ✅ Performance optimizations (memoized filtering)

#### Estadísticas de Tests

| Categoría | Tests | Estado |
|-----------|-------|--------|
| **Common Components** | 40 | ✅ 100% |
| - OptimizedImage | 25 | ✅ Passing |
| - Skeleton | 15 | ✅ Passing |
| **Product Components** | 59 | ✅ 100% |
| - ProductCard | 34 | ✅ Passing |
| - ProductGrid | 25 | ✅ Passing |
| **TOTAL** | **99** | **✅ 100%** |

#### Configuración de Cobertura

Configurado en `vitest.config.js` con umbrales del 80%:

```javascript
coverage: {
  provider: 'v8',
  lines: 80,
  functions: 80,
  branches: 80,
  statements: 80
}
```

#### Convenciones de Testing

**1. Estructura de Tests**
```jsx
describe('ComponentName', () => {
  describe('Feature Group', () => {
    it('should do something specific', () => {
      // Arrange
      const { container } = render(<Component />);

      // Act
      const element = screen.getByText('Text');

      // Assert
      expect(element).toBeInTheDocument();
    });
  });
});
```

**2. Mocking de Stores**
```jsx
vi.mock('../../../store/useCartStore');

beforeEach(() => {
  useCartStore.mockReturnValue({
    addItem: mockAddItem,
    items: []
  });
});
```

**3. Mocking de Router**
```jsx
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});
```

**4. Mocking de Componentes**
```jsx
vi.mock('../../../components/common/OptimizedImage', () => ({
  default: ({ alt, src }) => <img alt={alt} src={src} />,
}));
```

**5. Testing Asíncrono**
```jsx
await waitFor(() => {
  expect(screen.getByText('Expected Text')).toBeInTheDocument();
}, { timeout: 500 });
```

#### Ejemplo de Test Completo

```jsx
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import ProductCard from '../../../components/products/ProductCard';
import { useCartStore } from '../../../store/useCartStore';

vi.mock('../../../store/useCartStore');

const renderWithRouter = (component) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

describe('ProductCard', () => {
  const mockAddItem = vi.fn();
  const mockProduct = {
    id: 1,
    name: 'Test Product',
    price: 9.99,
    stock: 10
  };

  beforeEach(() => {
    vi.clearAllMocks();
    useCartStore.mockReturnValue({
      addItem: mockAddItem,
    });
  });

  it('calls addItem when add to cart button is clicked', async () => {
    mockAddItem.mockResolvedValue({});
    renderWithRouter(<ProductCard product={mockProduct} />);

    const addButton = screen.getByRole('button', { name: /Añadir/i });
    fireEvent.click(addButton);

    await waitFor(() => {
      expect(mockAddItem).toHaveBeenCalledWith(1, 1);
    });
  });
});
```

## Variables de Entorno

Crear archivo `.env` en la raíz del frontend:

```env
# API Backend
VITE_API_BASE_URL=http://localhost:8000

# Configuración de la app
VITE_APP_NAME=Tienda Alimentación Asiática
```

Acceder en el código:
```javascript
const API_URL = import.meta.env.VITE_API_BASE_URL;
```

## Próximos Pasos

### ✅ Fase 1: Completada
- [x] Estructura de carpetas modular
- [x] Capa de servicios API con Axios
- [x] Stores de Zustand para estado global (auth, cart, products, orders)
- [x] Funciones utilitarias (formatters, validators, constants)
- [x] Sistema de autenticación JWT (login, register, logout)
- [x] Rutas protegidas (ProtectedRoute, AdminRoute)
- [x] Interceptores de Axios para incluir JWT automáticamente
- [x] Dependencias instaladas

### ✅ Fase 2: Completada (UI Implementation)
- [x] Configurar React Router con todas las rutas
- [x] Crear componentes de layout (Header, Footer)
- [x] Crear componentes comunes (Button, Card, Input, Modal, Spinner)
- [x] Crear componentes de productos (ProductCard, ProductGrid con filtros)
- [x] Implementar página Home con hero y productos destacados
- [x] Implementar página Products con filtros y búsqueda
- [x] Implementar página ProductDetail completa
- [x] Agregar estilos CSS responsive y globales mejorados
- [x] Fix: Agregado import React a todos los componentes JSX
- [x] Fix: Configurado CORS en backend para múltiples puertos (5173-5176)
- [x] Fix: Corregidas rutas de imports (ProtectedRoute, useAuthStore)

### ✅ Fase 3: Completada (Carrito y Checkout)
- [x] Implementar página Cart con UI completa
- [x] Crear componentes de carrito (CartItem, CartSummary)
- [x] Implementar página Checkout con formulario de pedido
- [x] Validación completa de formulario checkout
- [x] Integración carrito → checkout → orden
- [x] Página de confirmación con animación
- [x] Actualización de servicios para JWT (cartService, orderService)

### ✅ Fase 4: Completada (Gestión de Órdenes)
- [x] Implementar página Orders (historial de pedidos con filtros por estado)
- [x] Implementar página OrderDetail con información completa
- [x] Componente OrderStatusBadge con estados visuales
- [x] Banner de éxito animado tras crear pedido
- [x] Flujo optimizado de checkout sin pantallas intermedias
- [x] Fix: Backend vacía carrito automáticamente al crear pedido
- [x] Fix: Campo subtotal agregado en CartItemResponse

### ✅ Fase 5: Completada (Panel de Administración - Productos) - 2025-10-29
- [x] AdminProductsPage con búsqueda y filtros por categoría
- [x] Componente ProductTable con acciones de editar/eliminar
- [x] Componente ProductFormModal para crear/editar productos
- [x] Badges de estado de stock (disponible/bajo/agotado)
- [x] Modal de confirmación para eliminar productos
- [x] Validación completa de formulario de productos
- [x] Rutas protegidas para admin (AdminRoute)
- [x] Navegación actualizada en Header con enlaces de admin
- [x] Fix: Redirección automática tras login según rol de usuario
- [x] Diseño responsive para todas las páginas de admin

### ✅ Fase 6: Completada (Admin Dashboard & HomePage Improvements) - 2025-10-29
- [x] AdminDashboardPage con estadísticas completas
- [x] Componente StatCard con iconos y variantes de color
- [x] Servicio dashboardService para obtener estadísticas
- [x] Endpoint backend optimizado `/api/v1/admin/dashboard/stats`
- [x] Dashboard muestra: total productos, pedidos, ventas, pendientes, stock bajo
- [x] Desglose de pedidos por los 6 estados
- [x] Tabla de pedidos recientes (últimos 5)
- [x] Lista de productos con stock bajo (top 10)
- [x] Botón de actualización en tiempo real
- [x] Diseño responsive completo
- [x] HomePage: Botón "Añadir al carrito" en productos destacados
- [x] HomePage: Añadir producto sin entrar en detalle
- [x] HomePage: Redirección automática a login si no está autenticado

### ✅ Fase 7: Completada (Gestión de Pedidos Admin) - 2025-10-30
- [x] Backend: Método `get_all()` en OrderRepository para admin
- [x] Backend: Método `get_all_orders()` en OrderService
- [x] Backend: Endpoint de pedidos actualizado para admin
- [x] OrderStatusUpdateModal con validación de transiciones de estado
- [x] AdminOrderTable con diseño responsive (tabla + tarjetas)
- [x] AdminOrdersPage con interfaz completa de gestión
- [x] Estadísticas de pedidos (total, pendientes, confirmados, procesando, enviados, entregados, cancelados)
- [x] Filtrado de pedidos por estado
- [x] Búsqueda de pedidos por ID, nombre o email
- [x] Actualización de estado de pedidos con validación
- [x] Reglas de transición de estados (pending → confirmed → processing → shipped → delivered)
- [x] Header actualizado con enlace "Gestión de Pedidos"
- [x] Ruta `/admin/orders` añadida y protegida con AdminRoute
- [x] Diseño responsive para todas las páginas de gestión de pedidos
- [x] Botón de actualización en tiempo real de la lista de pedidos

### ✅ Fase 8: Completada (Gestión de Categorías Admin) - 2025-10-30
- [x] Backend: Schema CategoryUpdate para actualizaciones parciales
- [x] Backend: Método update_category() en CategoryService
- [x] Backend: Endpoint PUT /api/v1/categories/{id}
- [x] Backend: Validación de nombres únicos en create y update
- [x] CategoryFormModal con validación para crear/editar
- [x] AdminCategoryTable con diseño responsive (tabla + tarjetas)
- [x] AdminCategoriesPage con interfaz completa de CRUD
- [x] Estadísticas de categorías (total, con/sin descripción)
- [x] Modal de confirmación de eliminación con advertencia
- [x] Header actualizado con enlace "Gestión de Categorías"
- [x] Ruta `/admin/categories` añadida y protegida con AdminRoute
- [x] Diseño responsive para todas las páginas de gestión
- [x] Operaciones CRUD completas probadas (GET, POST, PUT, DELETE)

### ✅ Fase 9: Completada (Gestión de Usuarios Admin) - 2025-10-30
- [x] Backend: UserService creado con métodos CRUD (get_all_users, update_user, delete_user)
- [x] Backend: Endpoints /api/v1/users creados (GET, PUT, DELETE)
- [x] Backend: Filtrado de usuarios por rol (customer/admin) y estado (activo/inactivo)
- [x] Backend: Endpoint de estadísticas de usuarios (total, activos, inactivos, admins, customers)
- [x] Backend: Soft delete de usuarios (is_active = False)
- [x] Backend: Protección contra eliminación de usuarios admin
- [x] userService.js creado con métodos completos (getUsers, getUserStats, updateUser, deleteUser)
- [x] AdminUserTable con badges de rol y estado, diseño responsive (tabla + tarjetas)
- [x] UserFormModal para editar información de usuarios (email, nombre, estado activo)
- [x] AdminUsersPage con interfaz completa de gestión
- [x] Estadísticas de usuarios (total, activos, inactivos, admins, customers)
- [x] Filtros por rol (customer/admin) y estado (activo/inactivo)
- [x] Modal de confirmación para desactivar usuarios
- [x] Protección UI: los admin no pueden ser desactivados
- [x] Header actualizado con enlace "Gestión de Usuarios"
- [x] Ruta `/admin/users` añadida y protegida con AdminRoute
- [x] Diseño responsive para todas las páginas de gestión
- [x] Operaciones CRUD completas probadas (GET, PUT, DELETE)

### ✅ Fase 10: Completada (Sistema de Imágenes de Productos) - 2025-10-31
- [x] Componente ImageUpload con drag & drop y preview
- [x] Validación de archivos (tipo, tamaño máximo 5MB)
- [x] Integración en ProductFormModal con toggle file/URL
- [x] Servicio productService actualizado (uploadProductImage, deleteProductImage)
- [x] Upload automático al crear/editar productos
- [x] Preview de imagen actual en modo edición
- [x] Botones para cambiar y eliminar imágenes
- [x] Diseño responsive del componente ImageUpload
- [x] Manejo de errores de validación
- [x] Soporte para múltiples formatos (JPG, PNG, GIF, WEBP)

### ✅ Fase 11: Optimizaciones de Rendimiento (Completado - 2025-11-03)
- [x] Implementar lazy loading de imágenes (OptimizedImage con Intersection Observer)
- [x] Optimización de rendimiento (React.memo, useMemo, useCallback)
- [x] Sistema de optimización de imágenes con WebP
- [x] Skeleton loaders para mejor UX
- [x] Carga progresiva de imágenes (thumbnail → full)
- [x] Responsive images con srcset
- [x] Reducción de re-renders innecesarios
- [x] Debounce en búsqueda

### ✅ Fase 12: Tests (Completado - 2025-11-03)
- [x] Configuración de Vitest con React Testing Library
- [x] Tests de OptimizedImage component (25 tests)
- [x] Tests de Skeleton component (15 tests)
- [x] Tests de ProductCard component (34 tests)
- [x] Tests de ProductGrid component (25 tests)
- [x] Configuración de cobertura de código (80% umbral)
- [x] Mocking de stores, router y componentes
- [x] Setup global con IntersectionObserver y matchMedia mocks

### 📋 Fase 13: Futuras Mejoras
- [ ] Agregar paginación infinita en productos (react-window/virtualization)
- [ ] Sistema de wishlist/favoritos
- [ ] Modo oscuro
- [ ] Internacionalización (i18n)
- [ ] PWA (Progressive Web App)
- [ ] Agregar animaciones con Framer Motion
- [ ] Notificaciones toast para acciones del usuario
- [ ] Service Worker para caché offline

## Cómo Continuar el Desarrollo

### Paso 1: Configurar React Router
```bash
# Crear el archivo de rutas
touch src/routes/AppRouter.jsx
```

### Paso 2: Crear componentes de layout
```bash
# Header con navegación y carrito badge
touch src/components/layout/Header.jsx

# Footer con información
touch src/components/layout/Footer.jsx
```

### Paso 3: Crear componentes comunes
```bash
touch src/components/common/Button.jsx
touch src/components/common/Card.jsx
touch src/components/common/Input.jsx
touch src/components/common/Modal.jsx
touch src/components/common/Spinner.jsx
```

### Paso 4: Implementar páginas
```bash
touch src/pages/Home.jsx
touch src/pages/Products.jsx
touch src/pages/ProductDetail.jsx
touch src/pages/Cart.jsx
touch src/pages/Checkout.jsx
touch src/pages/Orders.jsx
touch src/pages/OrderDetail.jsx
```

### Paso 5: Refactorizar App.jsx
- Envolver la aplicación con BrowserRouter
- Importar y usar AppRouter
- Inicializar userId del carrito al montar

## Recursos

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [React Router Documentation](https://reactrouter.com/)
- [Zustand Documentation](https://github.com/pmndrs/zustand)
- [Axios Documentation](https://axios-http.com/)

## Resumen de lo Implementado

✅ **Arquitectura Base Completa**
- Estructura de carpetas modular y escalable
- Separación clara de responsabilidades

✅ **Capa de Servicios**
- 6 servicios completos (auth, products, categories, cart, orders, users)
- Configuración de axios con interceptores para JWT
- Manejo centralizado de errores

✅ **Gestión de Estado**
- 4 stores de Zustand (auth, cart, products, orders)
- Estado global reactivo con persistencia
- Acciones asíncronas para API

✅ **Autenticación y Autorización**
- Sistema completo de login/register con JWT
- Rutas protegidas (ProtectedRoute, AdminRoute)
- Redirección automática según rol de usuario
- Persistencia de sesión con localStorage

✅ **UI Completa para Clientes**
- Catálogo de productos con filtros y búsqueda
- Páginas de detalle de producto
- Carrito de compras interactivo
- Flujo completo de checkout
- Historial de pedidos con filtros por estado
- Detalle de pedidos con toda la información

✅ **UI Completa para Administradores**
- Dashboard con estadísticas completas
- Panel de gestión de productos (CRUD completo)
- Búsqueda y filtros de productos
- Creación y edición de productos con validación
- Eliminación de productos con confirmación
- Badges visuales de stock (disponible/bajo/agotado)
- Panel de gestión de pedidos (ver todos, filtrar, buscar)
- Actualización de estado de pedidos con validación
- Estadísticas de pedidos en tiempo real
- Panel de gestión de categorías (CRUD completo)
- Creación, edición y eliminación de categorías
- Estadísticas de categorías en tiempo real
- Panel de gestión de usuarios (view, edit, deactivate)
- Filtros por rol y estado de usuarios
- Estadísticas de usuarios en tiempo real
- Protección contra desactivar usuarios admin

✅ **Componentes Reutilizables**
- Layout: Header con navegación responsive, Footer
- Common: Button, Input, Card, Modal, Spinner
- Auth: ProtectedRoute, AdminRoute
- Products: ProductCard, ProductGrid
- Cart: CartItem, CartSummary
- Orders: OrderStatusBadge, CheckoutForm
- Admin: StatCard, ProductTable, ProductFormModal, AdminOrderTable, OrderStatusUpdateModal, AdminCategoryTable, CategoryFormModal, AdminUserTable, UserFormModal

✅ **Utilidades**
- Formateadores (precios, fechas, texto)
- Constantes (estados, rutas, configuración)
- Validadores (email, teléfono, formularios)

✅ **Estilos y UX**
- Diseño responsive para todos los dispositivos
- Estilos CSS modulares y consistentes
- Animaciones suaves y transiciones
- Estados de loading y error bien manejados
- Feedback visual en todas las acciones

🔄 **Pendiente**
- Bulk operations para productos y categorías
- Sistema de subida de imágenes
- Tests unitarios y de integración
- Mejoras de rendimiento y optimización

## Notas Importantes para Desarrollo

### React Imports
**IMPORTANTE**: Todos los archivos `.jsx` deben incluir `import React from 'react'` al inicio, incluso si no se usa explícitamente. Esto es necesario para que JSX funcione correctamente.

```jsx
import React from 'react';
import { useState } from 'react';
// ... resto de imports
```

### Named Exports en Stores
Los stores de Zustand tienen tanto default export como named export:
```javascript
export { useAuthStore };
export default useAuthStore;
```

Esto permite importarlos de ambas formas:
```javascript
import { useAuthStore } from './store/useAuthStore';  // Named import
import useAuthStore from './store/useAuthStore';      // Default import
```

### Estructura de Rutas
- Archivos de autenticación en: `src/pages/LoginPage.jsx` y `src/pages/RegisterPage.jsx`
- Componente ProtectedRoute en: `src/components/auth/ProtectedRoute.jsx`
- Todos los imports de stores deben ser relativos desde su ubicación

### Servidor de Desarrollo
El servidor Vite puede correr en diferentes puertos (5173-5176) si otros están ocupados. El backend tiene CORS configurado para todos estos puertos.

## Licencia

Este proyecto es privado y de uso interno.
