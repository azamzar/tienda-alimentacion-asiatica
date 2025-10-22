# Tienda Alimentación Asiática - Backend API

API REST desarrollada con FastAPI para una tienda de alimentación asiática. Implementa una arquitectura en capas escalable y mantenible.

## Tabla de Contenidos

- [Tecnologías](#tecnologías)
- [Arquitectura](#arquitectura)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Configuración](#configuración)
- [Instalación y Ejecución](#instalación-y-ejecución)
- [Endpoints de la API](#endpoints-de-la-api)
- [Migraciones de Base de Datos](#migraciones-de-base-de-datos)
- [Desarrollo](#desarrollo)

---

## Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **PostgreSQL** - Base de datos relacional
- **Pydantic** - Validación de datos y settings
- **Alembic** - Migraciones de base de datos
- **Docker & Docker Compose** - Containerización
- **Uvicorn** - Servidor ASGI

## Arquitectura

El backend implementa una **arquitectura en capas (Clean Architecture)** que separa las responsabilidades:

```
┌─────────────────────────────────────────┐
│         API Layer (Endpoints)           │  ← FastAPI routes
├─────────────────────────────────────────┤
│       Service Layer (Business Logic)    │  ← Lógica de negocio
├─────────────────────────────────────────┤
│    Repository Layer (Data Access)       │  ← Acceso a datos
├─────────────────────────────────────────┤
│         Models (Database)               │  ← SQLAlchemy models
└─────────────────────────────────────────┘
```

### Capas de la Arquitectura

1. **API Layer** (`app/api/v1/endpoints/`)
   - Define los endpoints HTTP
   - Validación de requests/responses con Pydantic
   - Manejo de dependencias (inyección de DB session)
   - Documentación automática (Swagger/OpenAPI)

2. **Service Layer** (`app/services/`)
   - Contiene la lógica de negocio
   - Validaciones de negocio
   - Coordinación entre repositorios
   - Manejo de excepciones

3. **Repository Layer** (`app/repositories/`)
   - Abstracción del acceso a datos
   - Operaciones CRUD reutilizables
   - Queries especializadas
   - Patrón Repository

4. **Models** (`app/models/`)
   - Definición de tablas con SQLAlchemy
   - Relaciones entre entidades
   - Constraints de base de datos

5. **Schemas** (`app/schemas/`)
   - Modelos Pydantic para validación
   - Serialización/deserialización
   - Documentación de API

## Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                      # Entry point de FastAPI
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py              # Configuración con Pydantic Settings
│   │   └── database.py              # Setup de SQLAlchemy
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── exceptions.py            # Excepciones personalizadas
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                  # Dependencias compartidas (get_db)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py            # Router principal API v1
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── categories.py    # Endpoints de categorías
│   │           └── products.py      # Endpoints de productos
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py                  # Base declarativa de SQLAlchemy
│   │   ├── category.py              # Modelo Category
│   │   └── product.py               # Modelo Product
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── category.py              # Schemas Pydantic para Category
│   │   └── product.py               # Schemas Pydantic para Product
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── category_service.py      # Lógica de negocio de categorías
│   │   └── product_service.py       # Lógica de negocio de productos
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py                  # Repository base con CRUD genérico
│   │   ├── category_repository.py   # Repository de categorías
│   │   └── product_repository.py    # Repository de productos
│   │
│   └── utils/
│       └── __init__.py
│
├── scripts/
│   └── init_db.py                   # Script para inicializar la DB con datos
│
├── alembic/
│   ├── versions/                    # Migraciones de base de datos
│   ├── env.py                       # Configuración de Alembic
│   └── script.py.mako               # Template para nuevas migraciones
│
├── tests/
│   ├── unit/                        # Tests unitarios
│   └── integration/                 # Tests de integración
│
├── main.py                          # Entry point que importa app.main
├── requirements.txt                 # Dependencias de producción
├── alembic.ini                      # Configuración de Alembic
├── pytest.ini                       # Configuración de pytest
├── Dockerfile                       # Imagen Docker
├── docker-compose.dev.yml           # Docker Compose para desarrollo
├── .env                             # Variables de entorno (no versionado)
└── README.md                        # Este archivo
```

## Configuración

### Variables de Entorno

El proyecto usa **Pydantic Settings** para gestionar la configuración. Las variables se definen en `.env`:

```bash
# Database Configuration
POSTGRES_USER=tienda_user
POSTGRES_PASSWORD=tienda_password
POSTGRES_DB=tienda_asiatica
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Application Configuration
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

# Application Settings
APP_NAME=Tienda Alimentación Asiática API
APP_VERSION=1.0.0
DEBUG=False

# API Configuration
API_V1_PREFIX=/api/v1
```

### Configuración en `app/config/settings.py`

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Tienda Alimentación Asiática API"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    class Config:
        env_file = ".env"
```

## Instalación y Ejecución

### Opción 1: Docker Compose (Recomendado)

1. **Clonar el repositorio**
   ```bash
   cd backend
   ```

2. **Configurar variables de entorno**
   ```bash
   # El archivo .env ya existe con la configuración
   ```

3. **Construir y ejecutar los contenedores**
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```

4. **Inicializar la base de datos con datos de ejemplo**
   ```bash
   docker-compose -f docker-compose.dev.yml exec backend-tienda-alimentacion python scripts/init_db.py
   ```

5. **Acceder a la API**
   - API: http://localhost:8000
   - Documentación Swagger: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Opción 2: Instalación Local

1. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar PostgreSQL**
   - Instalar PostgreSQL
   - Crear base de datos `tienda_asiatica`
   - Actualizar `.env` con credenciales locales

4. **Ejecutar la aplicación**
   ```bash
   uvicorn main:app --reload
   ```

## Endpoints de la API

### Endpoints Principales

#### Root
```
GET /                    # Información de la API
GET /health              # Health check
```

#### Categorías
```
GET    /api/v1/categories/           # Listar todas las categorías
GET    /api/v1/categories/{id}       # Obtener categoría por ID
POST   /api/v1/categories/           # Crear nueva categoría
DELETE /api/v1/categories/{id}       # Eliminar categoría
```

#### Productos
```
GET    /api/v1/products/             # Listar productos (con paginación y filtros)
GET    /api/v1/products/{id}         # Obtener producto por ID
GET    /api/v1/products/search/      # Buscar productos por nombre
GET    /api/v1/products/low-stock/   # Productos con stock bajo
POST   /api/v1/products/             # Crear nuevo producto
PUT    /api/v1/products/{id}         # Actualizar producto
DELETE /api/v1/products/{id}         # Eliminar producto
```

### Ejemplos de Uso

#### Listar productos con filtros
```bash
# Todos los productos con paginación
curl "http://localhost:8000/api/v1/products/?skip=0&limit=10"

# Filtrar por categoría
curl "http://localhost:8000/api/v1/products/?category_id=1"

# Buscar por nombre
curl "http://localhost:8000/api/v1/products/search/?name=ramen"

# Productos con bajo stock
curl "http://localhost:8000/api/v1/products/low-stock/?threshold=10"
```

#### Crear un producto
```bash
curl -X POST "http://localhost:8000/api/v1/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Miso Paste",
    "description": "Pasta de miso tradicional japonesa",
    "price": 4.50,
    "stock": 30,
    "category_id": 2
  }'
```

#### Actualizar un producto
```bash
curl -X PUT "http://localhost:8000/api/v1/products/1" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 1.75,
    "stock": 150
  }'
```

## Migraciones de Base de Datos

El proyecto usa **Alembic** para gestionar migraciones de base de datos.

### Crear una nueva migración

```bash
# Dentro del contenedor
docker-compose -f docker-compose.dev.yml exec backend-tienda-alimentacion alembic revision --autogenerate -m "Descripción del cambio"

# Local
alembic revision --autogenerate -m "Descripción del cambio"
```

### Aplicar migraciones

```bash
# Dentro del contenedor
docker-compose -f docker-compose.dev.yml exec backend-tienda-alimentacion alembic upgrade head

# Local
alembic upgrade head
```

### Ver historial de migraciones

```bash
alembic history
```

### Revertir última migración

```bash
alembic downgrade -1
```

## Desarrollo

### Modelos de Datos

#### Category Model
```python
class Category(Base):
    __tablename__ = "categories"

    id: int (PK)
    name: str (unique, indexed)
    description: str (optional)
    created_at: datetime
    products: List[Product] (relationship)
```

#### Product Model
```python
class Product(Base):
    __tablename__ = "products"

    id: int (PK)
    name: str (indexed)
    description: str (optional)
    price: float
    image_url: str (optional)
    stock: int (default=0)
    category_id: int (FK → categories.id)
    created_at: datetime
    updated_at: datetime
    category: Category (relationship)
```

### Agregar un Nuevo Endpoint

1. **Crear el modelo** en `app/models/`
2. **Crear los schemas** en `app/schemas/`
3. **Crear el repository** en `app/repositories/`
4. **Crear el service** en `app/services/`
5. **Crear los endpoints** en `app/api/v1/endpoints/`
6. **Registrar el router** en `app/api/v1/router.py`

### Flujo de una Request

```
1. Request HTTP → 2. Endpoint (API Layer)
                      ↓
                  3. Service (Business Logic)
                      ↓
                  4. Repository (Data Access)
                      ↓
                  5. Database (PostgreSQL)
                      ↓
6. Response JSON ← 7. Schema (Pydantic serialization)
```

### Patrón Repository

El `BaseRepository` proporciona operaciones CRUD genéricas:

```python
class BaseRepository(Generic[ModelType]):
    def get_by_id(self, id: int) -> Optional[ModelType]
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]
    def create(self, obj_in: dict) -> ModelType
    def update(self, db_obj: ModelType, obj_in: dict) -> ModelType
    def delete(self, id: int) -> bool
    def count(self) -> int
```

Los repositorios específicos heredan y añaden queries personalizadas:

```python
class ProductRepository(BaseRepository[Product]):
    def get_by_category(self, category_id: int) -> List[Product]
    def search_by_name(self, name: str) -> List[Product]
    def get_low_stock_products(self, threshold: int) -> List[Product]
```

### Validaciones

Las validaciones se realizan en múltiples niveles:

1. **Pydantic Schemas**: Validación de tipos y formatos
   ```python
   price: float = Field(..., gt=0, description="Precio mayor a 0")
   ```

2. **Service Layer**: Validaciones de negocio
   ```python
   if self.repository.exists_by_name(name):
       raise HTTPException(status_code=400, detail="Ya existe")
   ```

3. **Database Constraints**: Constraints en DB
   ```python
   name = Column(String(100), unique=True, nullable=False)
   ```

## Logs y Debugging

### Ver logs en tiempo real

```bash
docker-compose -f docker-compose.dev.yml logs -f backend-tienda-alimentacion
```

### Acceder al contenedor

```bash
docker-compose -f docker-compose.dev.yml exec backend-tienda-alimentacion bash
```

### Conectar a la base de datos

```bash
docker-compose -f docker-compose.dev.yml exec db psql -U tienda_user -d tienda_asiatica
```

## Próximos Pasos

- [ ] Implementar sistema de autenticación (JWT)
- [ ] Agregar tests (pytest)
- [ ] Implementar logging estructurado
- [ ] Agregar carrito de compras
- [ ] Sistema de órdenes/pedidos
- [ ] Panel de administración
- [ ] Subida de imágenes
- [ ] Paginación mejorada con cursores
- [ ] Cache con Redis
- [ ] Rate limiting

## Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir un Pull Request

## Licencia

Este proyecto es privado y de uso interno.
