# Project Briefing for AI Agents

This document provides all the necessary context for an AI agent to understand and contribute to the "tienda-alimentacion-asiatica" project.

## 🚨 IMPORTANT: Required Reading

**Before starting any work, you MUST read the following files to understand the current state of the project:**

1. **`backend/README.md`** - Complete backend documentation including:
   - Architecture and layer structure
   - All implemented models, services, repositories
   - Complete API endpoints documentation
   - Authentication and authorization system
   - How to run and test the backend

2. **`frontend/README.md`** - Complete frontend documentation including:
   - Current implementation status
   - All services, stores, and utilities
   - Component structure
   - Dependencies and their purpose
   - Next steps and pending work

3. **`agents.md`** (this file) - Project overview and AI agent guidelines

**Always start your work session by reading these three files to get the most up-to-date context.**

## 1. Project Overview

This is a web application for an Asian food store. The goal is to create a fully functional e-commerce platform where users can browse products, add them to a shopping cart, and eventually place orders.

The project is divided into two main parts:

- `frontend/`: A React-based single-page application (SPA) that provides the user interface.
- `backend/`: A Python FastAPI-based API server that handles business logic, data storage, and serves data to the frontend.

## 2. Technology Stack

### Frontend

- **Framework:** React.js (`.jsx`)
- **Build Tool:** Vite
- **Package Manager:** npm
- **Styling:** Plain CSS (`App.css`, `index.css`)
- **Containerization:** Docker, Docker Compose
- **State:** (To be implemented - Zustand or Redux Toolkit)
- **Routing:** (To be implemented - React Router)
- **HTTP Client:** (To be implemented - Axios or React Query)

### Backend

- **Language:** Python 3.9
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL 13
- **Migrations:** Alembic
- **Validation:** Pydantic & Pydantic Settings
- **Server:** Uvicorn
- **Package Manager:** pip (`requirements.txt`)
- **Containerization:** Docker, Docker Compose

## 3. Project Structure

### Root Structure

```
.
├── backend/                # Backend API (FastAPI)
├── frontend/               # Frontend SPA (React + Vite)
└── agents.md              # This file
```

### Backend Structure (Clean Architecture)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI application entry point
│   │
│   ├── config/
│   │   ├── settings.py              # Pydantic Settings configuration
│   │   └── database.py              # SQLAlchemy setup
│   │
│   ├── core/
│   │   └── exceptions.py            # Custom exceptions
│   │
│   ├── api/
│   │   ├── deps.py                  # Shared dependencies (get_db)
│   │   └── v1/
│   │       ├── router.py            # Main API v1 router
│   │       └── endpoints/
│   │           ├── categories.py    # Category endpoints
│   │           └── products.py      # Product endpoints
│   │
│   ├── models/
│   │   ├── base.py                  # SQLAlchemy Base
│   │   ├── category.py              # Category model
│   │   └── product.py               # Product model
│   │
│   ├── schemas/
│   │   ├── category.py              # Category Pydantic schemas
│   │   └── product.py               # Product Pydantic schemas
│   │
│   ├── services/
│   │   ├── category_service.py      # Category business logic
│   │   └── product_service.py       # Product business logic
│   │
│   └── repositories/
│       ├── base.py                  # Base repository with CRUD
│       ├── category_repository.py   # Category data access
│       └── product_repository.py    # Product data access
│
├── scripts/
│   └── init_db.py                   # Database initialization script
│
├── alembic/
│   ├── versions/                    # Database migrations
│   ├── env.py                       # Alembic configuration
│   └── script.py.mako               # Migration template
│
├── tests/
│   ├── unit/                        # Unit tests
│   └── integration/                 # Integration tests
│
├── main.py                          # Entry point (imports app.main)
├── requirements.txt                 # Python dependencies
├── alembic.ini                      # Alembic configuration
├── Dockerfile                       # Docker image definition
├── docker-compose.dev.yml           # Development Docker Compose
├── .env                             # Environment variables (not in git)
└── README.md                        # Backend documentation
```

### Frontend Structure (To be refactored)

```
frontend/
├── src/
│   ├── App.jsx                      # Main application component
│   ├── main.jsx                     # React DOM render
│   └── index.css                    # Global styles
├── index.html                       # HTML entry point
├── package.json                     # Node.js dependencies
├── Dockerfile                       # Docker image definition
└── docker-compose.dev.yml           # Development Docker Compose
```

## 4. Backend Architecture

The backend implements a **layered architecture (Clean Architecture)** with clear separation of concerns:

### Architecture Layers

```
┌─────────────────────────────────────────┐
│         API Layer (Endpoints)           │  ← FastAPI routes (app/api/v1/endpoints/)
├─────────────────────────────────────────┤
│       Service Layer (Business Logic)    │  ← Business logic (app/services/)
├─────────────────────────────────────────┤
│    Repository Layer (Data Access)       │  ← Data access (app/repositories/)
├─────────────────────────────────────────┤
│         Models (Database)               │  ← SQLAlchemy models (app/models/)
└─────────────────────────────────────────┘
```

### Key Patterns

1. **Repository Pattern**: Abstraction of data access operations
   - `BaseRepository` provides generic CRUD operations
   - Specific repositories add custom queries

2. **Service Layer**: Encapsulates business logic
   - Validates business rules
   - Coordinates between repositories
   - Handles exceptions

3. **Dependency Injection**: Uses FastAPI's Depends
   - Database sessions injected via `get_db()`
   - Services instantiated per request

4. **Pydantic Settings**: Type-safe configuration
   - Environment variables validated
   - Default values defined

## 5. Database Schema

### Current Models

**Category**
- `id` (Integer, PK)
- `name` (String, unique, indexed)
- `description` (Text, optional)
- `created_at` (DateTime)
- `products` (Relationship → Product)

**Product**
- `id` (Integer, PK)
- `name` (String, indexed)
- `description` (Text, optional)
- `price` (Float)
- `image_url` (String, optional)
- `stock` (Integer, default=0)
- `category_id` (Integer, FK → categories.id)
- `created_at` (DateTime)
- `updated_at` (DateTime)
- `category` (Relationship → Category)

## 6. How to Run the Project

The project is fully containerized using Docker with **independent services** (backend and frontend) that communicate through a **shared Docker network**. This architecture simulates production where services are deployed separately.

### Initial Setup (First Time Only)

**Create the shared Docker network:**
```bash
docker network create tienda-net
```

This network allows backend and frontend containers to communicate using service names.

### Running the Backend

```bash
cd backend
docker-compose -f docker-compose.dev.yml up --build
```

This will start:
- PostgreSQL database on port 5432
- FastAPI server with hot-reload on port 8000

Both services are connected to the `tienda-net` network.

**Initialize database with sample data:**
```bash
docker-compose -f docker-compose.dev.yml exec backend-tienda-alimentacion python scripts/init_db.py
```

**Access the API:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Running the Frontend

In a separate terminal:

```bash
cd frontend
docker-compose -f docker-compose.dev.yml up --build
```

This will start the Vite development server on http://localhost:5173

The frontend is also connected to the `tienda-net` network.

### Service Communication

**Internal Docker network (container-to-container):**
- Backend: `http://backend-tienda-alimentacion:8000`
- Frontend: `http://frontend-tienda-alimentacion:5173`
- Database: `postgresql://db:5432`

**External access (from your browser):**
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

**Note:** When making API calls from the browser, use `http://localhost:8000/api/v1`. The internal service names are for server-to-server communication within Docker.

## 7. API Endpoints

### Current Endpoints (API v1)

**Root**
- `GET /` - API information
- `GET /health` - Health check

**Categories**
- `GET /api/v1/categories/` - List all categories
- `GET /api/v1/categories/{id}` - Get category by ID
- `POST /api/v1/categories/` - Create new category
- `DELETE /api/v1/categories/{id}` - Delete category

**Products**
- `GET /api/v1/products/` - List products (pagination + filters)
- `GET /api/v1/products/{id}` - Get product by ID
- `GET /api/v1/products/search/?name=xxx` - Search products by name
- `GET /api/v1/products/low-stock/?threshold=10` - Get low stock products
- `POST /api/v1/products/` - Create new product
- `PUT /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Delete product

## 8. Development Conventions

### Code Style
- **Python:** Follow PEP 8, use type hints
- **JavaScript/React:** Follow standard React conventions
- **Git:** Clear and descriptive commit messages

### Backend Conventions
- All endpoints use async/await
- Pydantic schemas for validation
- Service layer handles business logic
- Repository layer handles data access
- Exceptions handled in service layer
- HTTP exceptions from FastAPI

### API Conventions
- RESTful design
- JSON responses
- API versioning with `/api/v1/`
- Proper HTTP status codes (200, 201, 204, 400, 404, 500)
- Query parameters for filtering/pagination

### Dependencies
- **Python:** Add to `requirements.txt`
- **Node.js:** Use `npm install <package>`

## 9. Environment Variables

Backend environment variables (defined in `.env`):

```bash
# Database
POSTGRES_USER=tienda_user
POSTGRES_PASSWORD=tienda2025.
POSTGRES_DB=tienda_asiatica
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

# Application
APP_NAME=Tienda Alimentación Asiática API
APP_VERSION=1.0.0
DEBUG=False
API_V1_PREFIX=/api/v1
```

**Note:** If you change the PostgreSQL password, you must recreate the Docker volumes. See backend README for instructions.

## 10. Project Status & Roadmap

### ✅ Completed

**Fase 1 - Backend Refactoring:**
- [x] Backend architecture refactored to Clean Architecture
- [x] Repository pattern implemented
- [x] Service layer with business logic
- [x] API versioning (v1)
- [x] Pydantic Settings for configuration
- [x] Alembic configured for migrations
- [x] PostgreSQL database integrated
- [x] Category and Product CRUD operations
- [x] Search and filtering capabilities
- [x] Docker containerization
- [x] API documentation (Swagger/ReDoc)

**Fase 2 - Cart and Orders:**
- [x] Shopping cart functionality (Cart & CartItem models)
- [x] Order management system (Order & OrderItem models)
- [x] Cart endpoints (add, update, remove, clear)
- [x] Order endpoints (create, list, get, update, cancel)
- [x] Stock management integration

**Fase 3 - Authentication & Authorization:**
- [x] User authentication with JWT tokens
- [x] Password hashing with bcrypt
- [x] User model with role-based access control (RBAC)
- [x] Two roles: customer (default) and admin
- [x] Auth endpoints (register, login, logout, me)
- [x] Protected endpoints with authentication
- [x] Role-based permissions on all endpoints:
  - Products: POST/PUT/DELETE require admin
  - Categories: POST/DELETE require admin
  - Carts: All endpoints require authentication, use `/me`
  - Orders: All require auth, customers see only theirs, admins see all
- [x] Database migration for User model

### ✅ Recently Completed (2025-10-27)

**Fase 4 - Frontend Authentication:**
- [x] Frontend authentication system with JWT
- [x] Auth service (register, login, logout, getCurrentUser)
- [x] Auth store with Zustand (state management)
- [x] Login and Register pages with validation
- [x] Protected routes component (ProtectedRoute, AdminRoute)
- [x] API interceptors to include JWT tokens automatically
- [x] Session persistence with localStorage
- [x] Role-based UI rendering (customer/admin)

**Fase 5 - Admin User & Bug Fixes:**
- [x] Script to create admin users (interactive & non-interactive modes)
- [x] Fixed ProductResponse import issue
- [x] Fixed FastAPI Query parameter issues
- [x] Fixed bcrypt password truncation bug
- [x] Updated bcrypt dependency to compatible version (4.x)
- [x] Local Python virtual environment setup for backend
- [x] VS Code configuration for Python development
- [x] Database password change handling documented

**Fase 6 - Frontend UI Complete Implementation:**
- [x] React Router configured with all routes (public, protected, admin)
- [x] Common components: Button, Card, Input, Spinner, Modal
- [x] Layout components: Header (with nav and cart badge), Footer
- [x] Product components: ProductCard, ProductGrid (with filters and search)
- [x] Pages: HomePage (with hero and featured products), ProductsPage, ProductDetailPage
- [x] Global CSS reset and responsive styles
- [x] Fixed React import requirement in all JSX files
- [x] Fixed CORS configuration for multiple dev ports (5173-5176)
- [x] Fixed import paths (ProtectedRoute, stores)
- [x] Added named exports to all Zustand stores

**Fase 7 - Shopping Cart & Checkout (Completed 2025-10-27):**
- [x] Shopping cart UI implementation (CartItem, CartSummary)
- [x] CartPage with empty state, loading, and error handling
- [x] Checkout page with complete order form
- [x] CheckoutForm with real-time validation
- [x] OrderSummary component for checkout
- [x] Order creation from cart
- [x] Automatic cart clearing after order
- [x] Success page with animation
- [x] Updated cartService to use JWT authentication (/carts/me endpoints)
- [x] Updated orderService to use JWT authentication
- [x] Updated useCartStore and useOrderStore
- [x] Cart route protected (requires authentication)
- [x] Fully responsive design for cart and checkout
- [x] Shipping cost calculation (free over €50)

**Fase 8 - Orders Management Pages (Completed 2025-10-28):**
- [x] OrderStatusBadge component with 5 states (pending, processing, shipped, delivered, cancelled)
- [x] OrdersPage with order list and status filters
- [x] OrderDetailPage with complete order information
- [x] Customer information display (name, email, phone)
- [x] Shipping address and notes display
- [x] Order items list with product images and prices
- [x] Order summary with subtotal, shipping, and total
- [x] Cancel order functionality (for pending orders only)
- [x] Success banner animation when order is created
- [x] Optimized checkout flow (direct navigation without flash)
- [x] Backend: Added subtotal field to CartItemResponse schema
- [x] Backend: Cart service now calculates subtotal for each item
- [x] Frontend: Fixed order and cart item price display
- [x] Routes properly protected (requires authentication)
- [x] Fully responsive design for all order pages

**Current Admin Credentials:**
- Email: `admin@tienda.com`
- Password: `AdminPass123`
- Role: admin

### 🔄 In Progress

- [ ] Admin dashboard
- [ ] Product management UI (admin CRUD)

### 📋 Planned Features

**Phase 6 - Frontend UI Implementation:**
- [ ] React Router configuration with all routes
- [ ] Layout components (Header, Footer, Navigation)
- [ ] Common UI components (Button, Card, Input, Modal, Spinner)
- [ ] Product catalog with filters and search
- [ ] Product detail page
- [ ] Shopping cart UI
- [ ] Checkout flow
- [ ] Order history for customers
- [ ] Admin dashboard
- [ ] Product management UI (admin only)
- [ ] Order management UI (admin)

**Phase 7 - Backend Improvements:**
- [ ] Unit and integration testing (pytest)
- [ ] Structured logging
- [ ] API rate limiting
- [ ] Refresh tokens
- [ ] Password reset/recovery
- [ ] Email notifications
- [ ] Image upload system for products

**Phase 8 - Additional Features:**
- [ ] Payment integration (Stripe/PayPal)
- [ ] Advanced search and filtering
- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Real-time notifications (WebSockets)
- [ ] Analytics dashboard for admin
- [ ] Export orders to CSV/PDF

## 11. Common Development Tasks

### Adding a New Endpoint

1. Create/update model in `app/models/`
2. Create schemas in `app/schemas/`
3. Create repository in `app/repositories/`
4. Create service in `app/services/`
5. Create endpoints in `app/api/v1/endpoints/`
6. Register router in `app/api/v1/router.py`

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Debugging

```bash
# View logs
docker-compose -f docker-compose.dev.yml logs -f backend-tienda-alimentacion

# Access container
docker-compose -f docker-compose.dev.yml exec backend-tienda-alimentacion bash

# Access database
docker-compose -f docker-compose.dev.yml exec db psql -U tienda_user -d tienda_asiatica
```

## 12. Additional Resources

- Backend README: `backend/README.md` - Comprehensive backend documentation
- FastAPI Documentation: https://fastapi.tiangolo.com/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- Alembic Documentation: https://alembic.sqlalchemy.org/
- React Documentation: https://react.dev/
- Vite Documentation: https://vitejs.dev/

## 13. Notes for AI Agents

### Backend Architecture
- The backend has been fully refactored with a scalable architecture
- All backend code follows Clean Architecture principles
- When adding new features, maintain the layered architecture
- Always use the service layer for business logic
- Use repositories for all database operations
- Follow existing patterns for consistency
- Test endpoints using Swagger UI at http://localhost:8000/docs

### Authentication & Authorization
- JWT-based authentication is implemented and working
- All users register with role `customer` by default
- Use `get_current_user` dependency for authenticated endpoints
- Use `get_current_admin` dependency for admin-only endpoints
- Passwords are hashed with bcrypt (never store plain text)
- Tokens expire after 24 hours (configurable in `app/core/security.py`)
- Protected endpoints must include header: `Authorization: Bearer <token>`

### Security Best Practices
- The SECRET_KEY in `app/core/security.py` is currently hardcoded - **MUST** be moved to environment variables in production
- Never commit `.env` files with real secrets
- Always validate user permissions in the service layer, not just in endpoints
- Use `user_id` from JWT token, never trust user_id from request parameters

### Cart and Orders
- Cart endpoints use `/me` instead of `/{user_id}` to get user_id from token
- Orders endpoints filter by user_id from token for customers
- Admins can see all orders by checking `current_user.role == UserRole.ADMIN`
- Stock is only reduced when order is created, not when added to cart

### Frontend Development
- Frontend architecture base is ready (services, stores, utilities)
- ✅ **Authentication implemented**: auth store, login/register pages, protected routes
- ✅ API interceptors include JWT token automatically in all requests
- Use Zustand for state management (already set up for auth, cart, products, orders)
- **Frontend structure**:
  - `/pages`: LoginPage, RegisterPage, HomePage
  - `/components`: ProtectedRoute, AdminRoute
  - `/services`: authService, productService, cartService, orderService, categoryService
  - `/store`: useAuthStore, useCartStore, useProductStore, useOrderStore
  - `/utils`: formatters, validators, constants

### Development Environment Setup
- **Backend**: Python virtual environment created in `backend/venv/`
- **VS Code**: Configured to use local Python interpreter
- **Docker**: Both backend and frontend run in separate containers
- **Network**: Services communicate via `tienda-net` Docker network

### Common Issues & Solutions
1. **PostgreSQL password change**: Run `docker-compose down -v` then rebuild
2. **Import errors in IDE**: Ensure Python interpreter is set to `backend/venv/Scripts/python.exe`
3. **Bcrypt warnings**: These are informational only, functionality works correctly
4. **CORS issues**: Backend is configured to accept requests from localhost:5173

### Next Steps
1. ~~Create frontend auth service and store~~ ✅ DONE
2. ~~Implement login/register UI~~ ✅ DONE
3. ~~Add protected routes~~ ✅ DONE
4. ~~Update API interceptors to include JWT~~ ✅ DONE
5. ~~Fix backend import errors~~ ✅ DONE
6. ~~Create admin user script~~ ✅ DONE
7. ~~Implement product catalog with filters~~ ✅ DONE
8. ~~Create layout components (Header, Footer)~~ ✅ DONE
9. ~~Build common UI components~~ ✅ DONE
10. ~~Implement shopping cart UI (frontend)~~ ✅ DONE
11. ~~Create checkout flow UI (frontend)~~ ✅ DONE
12. ~~Implement orders pages (list and detail)~~ ✅ DONE
13. Build admin dashboard (frontend)
14. Implement product management (admin CRUD)

### Important Notes for AI Assistants

**React JSX Requirements:**
- ALL `.jsx` files MUST include `import React from 'react'` at the top
- This is required even if React is not explicitly used in the file
- Failure to include this will cause "React is not defined" errors

**Store Exports:**
- All Zustand stores have both default and named exports
- Example: `export { useAuthStore }; export default useAuthStore;`
- Import either way: `import { useAuthStore }` or `import useAuthStore`

**File Locations:**
- Auth pages: `src/pages/LoginPage.jsx`, `src/pages/RegisterPage.jsx`
- ProtectedRoute: `src/components/auth/ProtectedRoute.jsx`
- All stores: `src/store/` directory

**CORS Configuration:**
- Backend accepts requests from ports 5173-5176
- This covers all Vite dev server port variations
- Located in `backend/app/config/settings.py`

**Current Status:**
- ✅ Frontend: Product catalog fully functional
- ✅ Frontend: Shopping cart fully functional
- ✅ Frontend: Checkout flow complete with optimized UX
- ✅ Frontend: Order management pages complete (list and detail)
- ✅ Backend: All endpoints working with auth
- ✅ Backend: Cart items include subtotal field
- ⏳ Pending: Admin panel, Product management
