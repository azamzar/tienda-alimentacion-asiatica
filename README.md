# Tienda Alimentación Asiática

E-commerce completo para tienda de alimentación asiática con sistema de gestión de productos, pedidos, usuarios y más.

## 🌟 Características

### Para Clientes
- 🛒 Carrito de compras completo
- 🔍 Búsqueda avanzada con autocomplete
- ⭐ Sistema de reviews y ratings
- ❤️ Lista de favoritos/wishlist
- 🔄 Reordenar pedidos anteriores
- 📧 Notificaciones por email
- 🔐 Autenticación JWT segura
- 🌙 Modo oscuro

### Para Administradores
- 📊 Dashboard con estadísticas en tiempo real
- 📦 Gestión completa de productos (CRUD + imágenes)
- 📂 Gestión de categorías
- 📋 Gestión de pedidos con estados
- 👥 Gestión de usuarios
- 💾 Operaciones bulk (actualizar/eliminar múltiples)
- 📤 Exportación a CSV
- 🔒 Permisos basados en roles

### Características Técnicas
- ⚡ API REST con FastAPI
- 🎨 Frontend React + Vite
- 🐘 PostgreSQL para persistencia
- 🚀 Redis para caché
- 🖼️ Optimización automática de imágenes (WebP)
- 📝 Logging estructurado (JSON)
- 🧪 Tests automatizados (203 tests)
- 🔄 CI/CD con GitHub Actions
- 🐳 Docker y Docker Compose
- 🔐 SSL/TLS ready

## 📁 Estructura del Proyecto

```
tienda-alimentacion-asiatica/
├── backend/                # API FastAPI
│   ├── app/               # Código fuente
│   ├── tests/             # Tests (104 tests)
│   ├── scripts/           # Scripts de utilidad
│   ├── alembic/           # Migraciones de BD
│   ├── Dockerfile.prod    # Docker producción
│   └── docker-compose.prod.yml
│
├── frontend/              # React SPA
│   ├── src/              # Código fuente
│   ├── tests/            # Tests (99 tests)
│   ├── Dockerfile.prod   # Docker producción
│   ├── nginx.conf        # Configuración nginx
│   └── docker-compose.prod.yml
│
├── .github/
│   └── workflows/        # GitHub Actions CI/CD
│
├── agents.md             # Documentación para IA
├── DEPLOYMENT.md         # Guía de deployment
└── README.md            # Este archivo
```

## 🚀 Quick Start

### Desarrollo

```bash
# 1. Crear red Docker
docker network create tienda-net

# 2. Backend
cd backend
docker-compose -f docker-compose.dev.yml up --build
docker-compose -f docker-compose.dev.yml exec backend-tienda-alimentacion python scripts/init_db.py
docker-compose -f docker-compose.dev.yml exec backend-tienda-alimentacion python scripts/create_admin.py

# 3. Frontend (en otra terminal)
cd frontend
docker-compose -f docker-compose.dev.yml up --build
```

**URLs:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Producción

Ver [DEPLOYMENT.md](./DEPLOYMENT.md) para guía completa de deployment.

## 📚 Documentación

- **[agents.md](./agents.md)** - Documentación completa del proyecto para IA
- **[backend/README.md](./backend/README.md)** - Documentación del backend
- **[frontend/README.md](./frontend/README.md)** - Documentación del frontend
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Guía de deployment en producción

## 🧪 Tests

```bash
# Backend (104 tests)
cd backend
pytest tests/ -v --cov=app

# Frontend (99 tests)
cd frontend
npm test

# Total: 203 tests
```

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **PostgreSQL** - Base de datos relacional
- **Redis** - Caché en memoria
- **Alembic** - Migraciones de BD
- **Pydantic** - Validación de datos
- **JWT** - Autenticación segura
- **Pillow** - Procesamiento de imágenes
- **pytest** - Testing framework

### Frontend
- **React 18** - Librería UI
- **Vite** - Build tool
- **React Router** - Enrutamiento
- **Zustand** - State management
- **Axios** - Cliente HTTP
- **Vitest** - Testing framework

### DevOps
- **Docker** - Containerización
- **Docker Compose** - Orquestación
- **GitHub Actions** - CI/CD
- **Nginx** - Reverse proxy y servidor web

## 🔐 Seguridad

- ✅ Autenticación JWT con refresh tokens
- ✅ Hash de contraseñas con bcrypt
- ✅ Rate limiting en endpoints críticos
- ✅ CORS configurado
- ✅ Validación de entrada con Pydantic
- ✅ SQL injection prevention (SQLAlchemy)
- ✅ XSS protection headers
- ✅ HTTPS ready (SSL/TLS)
- ✅ SECRET_KEY en variables de entorno

## 📈 Performance

- ⚡ Caché con Redis (90% reducción en tiempo de respuesta)
- 🖼️ Imágenes optimizadas WebP (80% reducción en tamaño)
- 📦 Lazy loading de imágenes
- 🗜️ Gzip compression
- 📊 Database indexes optimizados
- 🔄 Connection pooling

## 📦 Releases

### Phase 21 - Production Ready (Enero 2025) ✅
- ✅ Dockerfiles optimizados multi-stage
- ✅ Docker Compose para producción
- ✅ Nginx con SSL/TLS
- ✅ Scripts de backup automático
- ✅ Health checks mejorados
- ✅ CI/CD con GitHub Actions
- ✅ Logging estructurado (JSON)
- ✅ Email system completo
- ✅ Password reset via email
- ✅ Database optimization (indexes)

### Phase 20 - Enhanced Discovery (Noviembre 2024)
- ✅ Búsqueda avanzada con autocomplete
- ✅ Filtros por precio, rating, stock
- ✅ Sistema de ordenamiento

### Phase 19 - Customer Features (Noviembre 2024)
- ✅ Reviews y ratings de productos
- ✅ Wishlist/favoritos
- ✅ Reorder button

### Phases 1-18
Ver [agents.md](./agents.md) para historial completo.

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'feat: Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir un Pull Request

## 📝 Convenciones de Commits

```
feat: Nueva funcionalidad
fix: Corrección de bug
docs: Cambios en documentación
style: Cambios de formato
refactor: Refactorización de código
test: Agregar o modificar tests
chore: Tareas de mantenimiento
```

## 📄 Licencia

Este proyecto es privado y de uso interno.

## 👥 Autores

- Alberto - Desarrollo inicial

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- React team por la librería UI
- Comunidad open source

---

**Versión actual**: 1.0.0
**Última actualización**: Enero 2025

Para deployment, ver [DEPLOYMENT.md](./DEPLOYMENT.md)
