# API de Carrito y Pedidos - Documentación

Esta documentación describe los nuevos endpoints implementados para el manejo de carritos de compra y pedidos.

## Tabla de Contenidos

- [Modelos de Datos](#modelos-de-datos)
- [Endpoints de Carrito](#endpoints-de-carrito)
- [Endpoints de Pedidos](#endpoints-de-pedidos)
- [Flujo de Compra Típico](#flujo-de-compra-típico)
- [Ejemplos de Uso](#ejemplos-de-uso)

---

## Modelos de Datos

### Cart (Carrito)
```python
{
  "id": int,
  "user_id": str,           # ID del usuario (puede ser UUID temporal)
  "created_at": datetime,
  "updated_at": datetime,
  "items": [CartItem],      # Lista de items en el carrito
  "total_items": int,       # Cantidad total de items
  "total_amount": float     # Monto total del carrito
}
```

### CartItem (Item del Carrito)
```python
{
  "id": int,
  "cart_id": int,
  "product_id": int,
  "quantity": int,
  "added_at": datetime,
  "product": Product        # Información completa del producto
}
```

### Order (Pedido)
```python
{
  "id": int,
  "user_id": str,
  "status": OrderStatus,    # pending, confirmed, processing, shipped, delivered, cancelled
  "total_amount": float,
  "customer_name": str,
  "customer_email": str,
  "customer_phone": str,
  "shipping_address": str,
  "notes": str | null,
  "created_at": datetime,
  "updated_at": datetime,
  "items": [OrderItem]      # Lista de items del pedido
}
```

### OrderItem (Item del Pedido)
```python
{
  "id": int,
  "order_id": int,
  "product_id": int,
  "quantity": int,
  "unit_price": float,      # Precio en el momento de la compra
  "subtotal": float,
  "product": Product        # Información completa del producto
}
```

### OrderStatus (Estados del Pedido)
- `pending`: Pedido creado, pendiente de confirmación
- `confirmed`: Pedido confirmado
- `processing`: En proceso de preparación
- `shipped`: Enviado
- `delivered`: Entregado
- `cancelled`: Cancelado

---

## Endpoints de Carrito

Base URL: `/api/v1/carts`

### 1. Obtener Carrito del Usuario

```http
GET /api/v1/carts/{user_id}
```

**Descripción:** Obtiene el carrito de un usuario con todos sus items y totales calculados.

**Parámetros:**
- `user_id` (path): ID del usuario

**Respuesta Exitosa (200):**
```json
{
  "id": 1,
  "user_id": "test-user-1",
  "created_at": "2025-10-20T10:00:00",
  "updated_at": "2025-10-20T10:30:00",
  "items": [
    {
      "id": 1,
      "cart_id": 1,
      "product_id": 5,
      "quantity": 2,
      "added_at": "2025-10-20T10:00:00",
      "product": {
        "id": 5,
        "name": "Salsa de Soja Kikkoman",
        "price": 3.50,
        "stock": 60,
        ...
      }
    }
  ],
  "total_items": 2,
  "total_amount": 7.00
}
```

---

### 2. Agregar Producto al Carrito

```http
POST /api/v1/carts/{user_id}/items
```

**Descripción:** Agrega un producto al carrito. Si el producto ya existe, incrementa la cantidad.

**Parámetros:**
- `user_id` (path): ID del usuario

**Body:**
```json
{
  "product_id": 5,
  "quantity": 2
}
```

**Validaciones:**
- El producto debe existir
- Debe haber stock suficiente
- La cantidad debe ser mayor a 0

**Respuesta Exitosa (200):**
Retorna el carrito actualizado (mismo formato que GET)

**Errores:**
- `404`: Producto no encontrado
- `400`: Stock insuficiente

---

### 3. Actualizar Cantidad de un Item

```http
PUT /api/v1/carts/{user_id}/items/{product_id}
```

**Descripción:** Actualiza la cantidad de un producto específico en el carrito.

**Parámetros:**
- `user_id` (path): ID del usuario
- `product_id` (path): ID del producto

**Body:**
```json
{
  "quantity": 5
}
```

**Validaciones:**
- El producto debe estar en el carrito
- Debe haber stock suficiente para la nueva cantidad
- La cantidad debe ser mayor a 0

**Respuesta Exitosa (200):**
Retorna el carrito actualizado

**Errores:**
- `404`: Carrito o producto no encontrado
- `400`: Stock insuficiente

---

### 4. Eliminar Producto del Carrito

```http
DELETE /api/v1/carts/{user_id}/items/{product_id}
```

**Descripción:** Elimina un producto específico del carrito.

**Parámetros:**
- `user_id` (path): ID del usuario
- `product_id` (path): ID del producto a eliminar

**Respuesta Exitosa (200):**
Retorna el carrito actualizado

**Errores:**
- `404`: Carrito o producto no encontrado en el carrito

---

### 5. Vaciar Carrito

```http
DELETE /api/v1/carts/{user_id}
```

**Descripción:** Elimina todos los items del carrito del usuario.

**Parámetros:**
- `user_id` (path): ID del usuario

**Respuesta Exitosa (200):**
```json
{
  "message": "Carrito vaciado exitosamente",
  "items_removed": 5
}
```

---

## Endpoints de Pedidos

Base URL: `/api/v1/orders`

### 1. Crear Pedido desde Carrito

```http
POST /api/v1/orders/?user_id={user_id}
```

**Descripción:** Crea un pedido a partir del carrito actual del usuario. Reduce el stock, crea el pedido y vacía el carrito.

**Query Parameters:**
- `user_id` (required): ID del usuario

**Body:**
```json
{
  "customer_name": "Juan Pérez",
  "customer_email": "juan@example.com",
  "customer_phone": "+34 612 345 678",
  "shipping_address": "Calle Mayor 123, 28013 Madrid, España",
  "notes": "Por favor, llamar antes de entregar"
}
```

**Validaciones:**
- El carrito debe existir y tener items
- Debe haber stock suficiente para todos los productos
- Email debe ser válido

**Respuesta Exitosa (201):**
```json
{
  "id": 1,
  "user_id": "test-user-1",
  "status": "pending",
  "total_amount": 45.50,
  "customer_name": "Juan Pérez",
  "customer_email": "juan@example.com",
  "customer_phone": "+34 612 345 678",
  "shipping_address": "Calle Mayor 123, 28013 Madrid, España",
  "notes": "Por favor, llamar antes de entregar",
  "created_at": "2025-10-20T11:00:00",
  "updated_at": "2025-10-20T11:00:00",
  "items": [
    {
      "id": 1,
      "order_id": 1,
      "product_id": 1,
      "quantity": 5,
      "unit_price": 1.50,
      "subtotal": 7.50,
      "product": {...}
    }
  ]
}
```

**Errores:**
- `404`: Carrito no encontrado
- `400`: Carrito vacío o stock insuficiente

---

### 2. Obtener Pedido por ID

```http
GET /api/v1/orders/{order_id}?user_id={user_id}
```

**Descripción:** Obtiene los detalles completos de un pedido.

**Parámetros:**
- `order_id` (path): ID del pedido
- `user_id` (query, optional): ID del usuario (para validar propiedad)

**Respuesta Exitosa (200):**
Retorna el pedido completo (mismo formato que POST)

**Errores:**
- `404`: Pedido no encontrado
- `403`: El pedido no pertenece al usuario

---

### 3. Listar Pedidos con Filtros

```http
GET /api/v1/orders/?user_id={user_id}&status={status}&skip={skip}&limit={limit}
```

**Descripción:** Lista pedidos con filtros opcionales y paginación.

**Query Parameters:**
- `user_id` (optional): Filtrar por usuario
- `status` (optional): Filtrar por estado (pending, confirmed, processing, shipped, delivered, cancelled)
- `skip` (optional, default: 0): Número de registros a omitir
- `limit` (optional, default: 100, max: 100): Número de registros a devolver

**Ejemplos:**
```
GET /api/v1/orders/?user_id=test-user-1
GET /api/v1/orders/?status=pending
GET /api/v1/orders/?user_id=test-user-1&status=delivered
```

**Respuesta Exitosa (200):**
```json
[
  {
    "id": 1,
    "user_id": "test-user-1",
    "status": "confirmed",
    "total_amount": 45.50,
    ...
  },
  {
    "id": 2,
    "user_id": "test-user-1",
    "status": "delivered",
    "total_amount": 23.80,
    ...
  }
]
```

---

### 4. Actualizar Pedido

```http
PATCH /api/v1/orders/{order_id}?user_id={user_id}
```

**Descripción:** Actualiza información de un pedido (estado, datos del cliente).

**Parámetros:**
- `order_id` (path): ID del pedido
- `user_id` (query, optional): ID del usuario (para validación)

**Body (todos los campos opcionales):**
```json
{
  "status": "processing",
  "customer_name": "Juan Pérez García",
  "customer_phone": "+34 612 345 679",
  "shipping_address": "Nueva dirección",
  "notes": "Nuevas notas"
}
```

**Validaciones de Estado:**
- No se puede modificar un pedido cancelado
- No se puede cambiar el estado de un pedido ya entregado
- Solo admin puede cambiar ciertos campos si no es el propietario

**Respuesta Exitosa (200):**
Retorna el pedido actualizado

**Errores:**
- `404`: Pedido no encontrado
- `403`: Sin permisos para modificar
- `400`: Cambio de estado inválido

---

### 5. Cancelar Pedido

```http
POST /api/v1/orders/{order_id}/cancel?user_id={user_id}
```

**Descripción:** Cancela un pedido y restaura el stock de los productos.

**Parámetros:**
- `order_id` (path): ID del pedido
- `user_id` (query, optional): ID del usuario (para validación)

**Validaciones:**
- Solo se pueden cancelar pedidos en estado: pending, confirmed, processing
- No se pueden cancelar pedidos enviados o entregados
- El stock se restaura automáticamente

**Respuesta Exitosa (200):**
Retorna el pedido con estado "cancelled"

**Errores:**
- `404`: Pedido no encontrado
- `403`: Sin permisos para cancelar
- `400`: El pedido no se puede cancelar (ya cancelado, enviado o entregado)

---

## Flujo de Compra Típico

1. **Navegación y Selección**
   ```
   GET /api/v1/products/          # Ver productos
   GET /api/v1/products/{id}       # Ver detalle
   ```

2. **Agregar al Carrito**
   ```
   POST /api/v1/carts/{user_id}/items
   {
     "product_id": 5,
     "quantity": 2
   }
   ```

3. **Ver/Modificar Carrito**
   ```
   GET /api/v1/carts/{user_id}                      # Ver carrito
   PUT /api/v1/carts/{user_id}/items/{product_id}   # Actualizar cantidad
   DELETE /api/v1/carts/{user_id}/items/{product_id} # Eliminar item
   ```

4. **Crear Pedido**
   ```
   POST /api/v1/orders/?user_id={user_id}
   {
     "customer_name": "...",
     "customer_email": "...",
     "customer_phone": "...",
     "shipping_address": "...",
     "notes": "..."
   }
   ```

5. **Seguimiento del Pedido**
   ```
   GET /api/v1/orders/{order_id}?user_id={user_id}   # Ver estado
   GET /api/v1/orders/?user_id={user_id}             # Ver todos los pedidos
   ```

6. **Gestión del Pedido (Admin)**
   ```
   PATCH /api/v1/orders/{order_id}
   {
     "status": "confirmed"  # confirmed → processing → shipped → delivered
   }
   ```

7. **Cancelación (si necesario)**
   ```
   POST /api/v1/orders/{order_id}/cancel?user_id={user_id}
   ```

---

## Ejemplos de Uso

### Ejemplo 1: Agregar productos y crear pedido

```bash
# 1. Agregar producto al carrito
curl -X POST "http://localhost:8000/api/v1/carts/user-123/items" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 3
  }'

# 2. Agregar otro producto
curl -X POST "http://localhost:8000/api/v1/carts/user-123/items" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 5,
    "quantity": 1
  }'

# 3. Ver carrito
curl "http://localhost:8000/api/v1/carts/user-123"

# 4. Crear pedido
curl -X POST "http://localhost:8000/api/v1/orders/?user_id=user-123" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Ana López",
    "customer_email": "ana.lopez@example.com",
    "customer_phone": "+34 678 901 234",
    "shipping_address": "Plaza España 10, 08014 Barcelona",
    "notes": "Entrega por la tarde"
  }'
```

### Ejemplo 2: Modificar cantidad en carrito

```bash
# Cambiar cantidad de un producto
curl -X PUT "http://localhost:8000/api/v1/carts/user-123/items/1" \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 5
  }'
```

### Ejemplo 3: Ver pedidos de un usuario

```bash
# Todos los pedidos del usuario
curl "http://localhost:8000/api/v1/orders/?user_id=user-123"

# Solo pedidos pendientes
curl "http://localhost:8000/api/v1/orders/?user_id=user-123&status=pending"

# Con paginación
curl "http://localhost:8000/api/v1/orders/?user_id=user-123&skip=0&limit=10"
```

### Ejemplo 4: Actualizar estado de pedido (Admin)

```bash
curl -X PATCH "http://localhost:8000/api/v1/orders/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "confirmed"
  }'
```

### Ejemplo 5: Cancelar pedido

```bash
curl -X POST "http://localhost:8000/api/v1/orders/1/cancel?user_id=user-123"
```

---

## Notas Importantes

### Gestión de Stock
- Al agregar productos al carrito, se valida el stock pero NO se reserva
- El stock se reduce SOLO al crear el pedido
- Si se cancela un pedido, el stock se restaura automáticamente

### IDs de Usuario
- Se usa `user_id` (string) para identificar usuarios
- Puede ser un UUID temporal para usuarios no autenticados
- O un ID de usuario real cuando implementes autenticación

### Estados de Pedido
Los cambios de estado siguen un flujo:
```
pending → confirmed → processing → shipped → delivered
         ↓
      cancelled (solo desde pending/confirmed/processing)
```

### Validaciones de Negocio
- No se puede cancelar un pedido enviado o entregado
- No se puede modificar un pedido cancelado
- El stock debe ser suficiente al crear el pedido
- Los precios se capturan en el momento de la compra (unit_price)

---

## Próximos Pasos

Para producción, considera implementar:

1. **Autenticación y Autorización**
   - JWT tokens
   - Roles de usuario (customer, admin)
   - Endpoints protegidos

2. **Pagos**
   - Integración con Stripe/PayPal
   - Estados de pago
   - Webhooks de confirmación

3. **Notificaciones**
   - Emails de confirmación
   - Notificaciones de cambio de estado
   - SMS para actualizaciones

4. **Mejoras de Carrito**
   - Expiración de carritos abandonados
   - Recordatorios de carrito
   - Wishlist/favoritos

5. **Dashboard Admin**
   - Gestión de pedidos
   - Reportes de ventas
   - Gestión de inventario
