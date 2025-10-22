# Project Briefing for AI Agents

This document provides all the necessary context for an AI agent to understand and contribute to the "tienda-alimentacion-asiatica" project.

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

The project is fully containerized using Docker.

### Running the Backend

```bash
cd backend
docker-compose -f docker-compose.dev.yml up --build
```

This will start:
- PostgreSQL database on port 5432
- FastAPI server with hot-reload on port 8000

**Initialize database with sample data:**
```bash
docker-compose -f docker-compose.dev.yml exec backend-tienda-alimentacion python scripts/init_db.py
```

**Access the API:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Running the Frontend

```bash
cd frontend
docker-compose -f docker-compose.dev.yml up --build
```

This will start the Vite development server on http://localhost:5173

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
POSTGRES_PASSWORD=tienda_password
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

## 10. Project Status & Roadmap

### ✅ Completed (Fase 1 - Backend Refactoring)

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

### 🔄 In Progress

- [ ] Frontend refactoring to scalable architecture
- [ ] Testing implementation (pytest)
- [ ] Logging system

### 📋 Planned Features

**Phase 2 - Backend Improvements:**
- [ ] Unit and integration testing (pytest)
- [ ] Structured logging
- [ ] Centralized exception handling
- [ ] API rate limiting

**Phase 3 - Frontend Refactoring:**
- [ ] Folder structure by features
- [ ] State management (Zustand/Redux)
- [ ] React Router implementation
- [ ] API layer with Axios/React Query
- [ ] Component library structure

**Phase 4 - New Features:**
- [ ] User authentication (JWT)
- [ ] Shopping cart functionality
- [ ] Order management system
- [ ] Admin panel
- [ ] Image upload system
- [ ] Payment integration
- [ ] Email notifications

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

- The backend has been fully refactored with a scalable architecture
- All backend code follows Clean Architecture principles
- When adding new features, maintain the layered architecture
- Always use the service layer for business logic
- Use repositories for all database operations
- Follow existing patterns for consistency
- Test endpoints using Swagger UI at http://localhost:8000/docs
- The frontend still needs refactoring to match backend architecture quality
