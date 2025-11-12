# Deployment Guide - Tienda Alimentación Asiática

Guía completa para desplegar la aplicación en producción.

## Tabla de Contenidos

- [Arquitectura de Deployment](#arquitectura-de-deployment)
- [Requisitos Previos](#requisitos-previos)
- [Configuración Inicial](#configuración-inicial)
- [Deployment Backend](#deployment-backend)
- [Deployment Frontend](#deployment-frontend)
- [CI/CD con GitHub Actions](#cicd-con-github-actions)
- [Backup y Restauración](#backup-y-restauración)
- [Monitoring y Logs](#monitoring-y-logs)
- [Troubleshooting](#troubleshooting)

---

## Arquitectura de Deployment

```
┌──────────────────────────────────────────────────────────────┐
│                         Internet                             │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Load Balancer  │ (Optional)
                    │   / Cloudflare   │
                    └──────────────────┘
                       │            │
           ┌───────────┘            └───────────┐
           ▼                                    ▼
┌─────────────────────┐              ┌─────────────────────┐
│  Frontend Server    │              │  Backend Server     │
│  (nginx + React)    │─────────────▶│  (FastAPI)          │
│  Port 80/443        │              │  Port 8000          │
└─────────────────────┘              └─────────────────────┘
                                              │
                                ┌─────────────┴─────────────┐
                                ▼                           ▼
                      ┌──────────────┐           ┌──────────────┐
                      │  PostgreSQL  │           │    Redis     │
                      │  Port 5432   │           │  Port 6379   │
                      └──────────────┘           └──────────────┘
```

**Arquitectura recomendada:**
- **Frontend**: Servidor separado o CDN (Vercel, Netlify, AWS S3 + CloudFront)
- **Backend**: Servidor con Docker (AWS EC2, Digital Ocean, Linode, Railway)
- **Base de datos**: PostgreSQL gestionada (AWS RDS, Digital Ocean Managed DB)
- **Cache**: Redis gestionado (AWS ElastiCache, Redis Cloud)

---

## Requisitos Previos

### Software
- Docker y Docker Compose
- Git
- Dominio configurado (para SSL/TLS)

### Servicios externos
- Cuenta Docker Hub (para imágenes)
- Servidor cloud (AWS, Digital Ocean, etc.)
- PostgreSQL (local o gestionada)
- Redis (local o gestionada)
- Servicio SMTP (Gmail, SendGrid, Mailgun)

### Conocimientos
- Bash/Linux básico
- Docker y contenedores
- Configuración de DNS
- SSL/TLS certificates

---

## Configuración Inicial

### 1. Preparar el servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo apt install docker-compose -y

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker

# Verificar instalación
docker --version
docker-compose --version
```

### 2. Clonar el repositorio

```bash
# En el servidor
cd /opt
sudo git clone https://github.com/tu-usuario/tienda-alimentacion-asiatica.git
cd tienda-alimentacion-asiatica
sudo chown -R $USER:$USER .
```

### 3. Configurar firewall

```bash
# Permitir puertos necesarios
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 8000/tcp  # API (opcional - puede estar detrás de nginx)
sudo ufw enable
```

---

## Deployment Backend

### 1. Configurar variables de entorno

```bash
cd backend
cp .env.prod.example .env.prod
nano .env.prod
```

**Configuración mínima requerida:**

```bash
# Database
POSTGRES_USER=tienda_user
POSTGRES_PASSWORD=<SECURE_PASSWORD>
POSTGRES_DB=tienda_asiatica
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Security - IMPORTANTE: Generar con: openssl rand -hex 32
SECRET_KEY=<YOUR_SECURE_SECRET_KEY>

# CORS - Dominio del frontend
CORS_ORIGINS=https://tudominio.com

# Email
EMAIL_ENABLED=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=<YOUR_APP_PASSWORD>
EMAIL_FROM=noreply@tudominio.com
FRONTEND_URL=https://tudominio.com
```

### 2. Construir y ejecutar

```bash
# Construir imágenes
docker-compose -f docker-compose.prod.yml build

# Iniciar servicios
docker-compose -f docker-compose.prod.yml up -d

# Verificar que los servicios estén corriendo
docker-compose -f docker-compose.prod.yml ps

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f backend
```

### 3. Inicializar base de datos

```bash
# Ejecutar migraciones
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# (Opcional) Cargar datos iniciales
docker-compose -f docker-compose.prod.yml exec backend python scripts/init_db.py

# Crear usuario administrador
docker-compose -f docker-compose.prod.yml exec backend python scripts/create_admin.py
```

### 4. Verificar health checks

```bash
# Health check básico
curl http://localhost:8000/health

# Health check detallado
curl http://localhost:8000/health/detailed
```

---

## Deployment Frontend

### Opción A: Deployment con Docker (Servidor propio)

#### 1. Configurar variables de entorno

```bash
cd frontend
cp .env.prod.example .env.prod
nano .env.prod
```

```bash
# URL del backend API
VITE_API_BASE_URL=https://api.tudominio.com
```

#### 2. Construir y ejecutar

```bash
# Construir imagen (pasando build args)
docker-compose -f docker-compose.prod.yml build --build-arg VITE_API_BASE_URL=https://api.tudominio.com

# Iniciar servicio
docker-compose -f docker-compose.prod.yml up -d

# Verificar
curl http://localhost/
```

#### 3. Configurar SSL con Let's Encrypt

```bash
# Instalar certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtener certificado
sudo certbot --nginx -d tudominio.com -d www.tudominio.com

# Copiar certificados para Docker
sudo cp /etc/letsencrypt/live/tudominio.com/fullchain.pem frontend/ssl/
sudo cp /etc/letsencrypt/live/tudominio.com/privkey.pem frontend/ssl/
```

**Actualizar nginx.conf** para usar HTTPS (descomentar sección SSL).

### Opción B: Deployment en Vercel/Netlify (Recomendado)

#### Vercel

```bash
# Instalar Vercel CLI
npm install -g vercel

# En el directorio frontend
cd frontend
vercel

# Configurar variables de entorno en Vercel dashboard
# VITE_API_BASE_URL=https://api.tudominio.com
```

#### Netlify

```bash
# Instalar Netlify CLI
npm install -g netlify-cli

# En el directorio frontend
cd frontend
netlify deploy --prod

# Build command: npm run build
# Publish directory: dist
```

**netlify.toml:**
```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

---

## CI/CD con GitHub Actions

### 1. Configurar secrets en GitHub

Ve a: **Repository Settings > Secrets and variables > Actions**

Agregar los siguientes secrets:

```
# Docker Hub
DOCKER_USERNAME=tu-usuario
DOCKER_PASSWORD=tu-password

# Backend API URL (para frontend build)
VITE_API_BASE_URL=https://api.tudominio.com

# Deployment (opcional)
SERVER_HOST=tu-servidor.com
SERVER_USER=deploy
SERVER_SSH_KEY=<tu-private-key>
```

### 2. Workflows configurados

Los workflows se ejecutan automáticamente en:

- **Backend Tests** (`backend-tests.yml`): Cada push/PR a backend
- **Frontend Tests** (`frontend-tests.yml`): Cada push/PR a frontend
- **Backend Deploy** (`backend-deploy.yml`): Push a main/master
- **Frontend Deploy** (`frontend-deploy.yml`): Push a main/master

### 3. Habilitar deployment automático

Para habilitar el deployment automático a tu servidor, descomenta la sección `deploy` en los workflows y configura los secrets necesarios.

---

## Backup y Restauración

### Backup automático

```bash
# Configurar backups automáticos (ejecutar una vez)
cd backend
chmod +x scripts/*.sh
./scripts/setup_cron_backup.sh
```

Esto configura un cron job que ejecuta backups diarios a las 2:00 AM.

### Backup manual

```bash
# Desde el servidor
cd backend
./scripts/docker_backup.sh

# Los backups se guardan en: backend/backup/
```

### Restaurar backup

```bash
# Listar backups disponibles
ls -lh backend/backup/

# Restaurar un backup específico
cd backend
./scripts/docker_restore.sh backup/backup_tienda_asiatica_20250112_120000.sql.gz
```

### Descargar backups del servidor

```bash
# Desde tu máquina local
scp usuario@servidor:/opt/tienda-alimentacion-asiatica/backend/backup/*.gz ./backups/
```

---

## Monitoring y Logs

### Ver logs en tiempo real

```bash
# Backend
docker-compose -f backend/docker-compose.prod.yml logs -f backend

# Base de datos
docker-compose -f backend/docker-compose.prod.yml logs -f db

# Redis
docker-compose -f backend/docker-compose.prod.yml logs -f redis

# Frontend (si está en Docker)
docker-compose -f frontend/docker-compose.prod.yml logs -f frontend
```

### Logs estructurados

Los logs del backend están en formato JSON para facilitar el análisis:

```bash
# Ver logs de aplicación
tail -f backend/logs/app.log | jq

# Ver solo errores
tail -f backend/logs/error.log | jq

# Filtrar por request_id
grep "request_id_123" backend/logs/app.log | jq
```

### Health checks

```bash
# Health check básico
curl https://api.tudominio.com/health

# Health check detallado (métricas de sistema, DB, Redis)
curl https://api.tudominio.com/health/detailed | jq

# Readiness check (para Kubernetes)
curl https://api.tudominio.com/health/readiness

# Liveness check
curl https://api.tudominio.com/health/liveness
```

### Monitoring recomendado

**Servicios externos:**
- **Uptime Robot**: Monitoreo de uptime (gratuito)
- **Sentry**: Error tracking
- **DataDog / New Relic**: APM y métricas
- **Grafana + Prometheus**: Monitoring self-hosted

---

## Troubleshooting

### Backend no inicia

```bash
# Ver logs detallados
docker-compose -f docker-compose.prod.yml logs backend

# Verificar conectividad a base de datos
docker-compose -f docker-compose.prod.yml exec backend psql -h db -U tienda_user -d tienda_asiatica

# Verificar conectividad a Redis
docker-compose -f docker-compose.prod.yml exec backend redis-cli -h redis ping
```

### Error "Database connection failed"

```bash
# Verificar que PostgreSQL está corriendo
docker-compose -f docker-compose.prod.yml ps db

# Verificar logs de PostgreSQL
docker-compose -f docker-compose.prod.yml logs db

# Verificar credenciales en .env.prod
cat backend/.env.prod | grep POSTGRES

# Reiniciar servicios
docker-compose -f docker-compose.prod.yml restart db backend
```

### Frontend muestra error de API

1. Verificar que `VITE_API_BASE_URL` apunta al backend correcto
2. Verificar CORS en backend (`.env.prod` → `CORS_ORIGINS`)
3. Verificar que el backend está accesible desde el navegador

```bash
# Desde el navegador (consola)
fetch('https://api.tudominio.com/health')
  .then(r => r.json())
  .then(console.log)
```

### Alto uso de recursos

```bash
# Ver uso de recursos por contenedor
docker stats

# Verificar logs de sistema
docker-compose -f docker-compose.prod.yml exec backend curl http://localhost:8000/health/detailed

# Limpiar recursos no utilizados
docker system prune -a --volumes
```

### Certificados SSL expirados

```bash
# Renovar certificados Let's Encrypt
sudo certbot renew

# Copiar nuevos certificados
sudo cp /etc/letsencrypt/live/tudominio.com/*.pem frontend/ssl/

# Reiniciar nginx
docker-compose -f frontend/docker-compose.prod.yml restart
```

---

## Comandos útiles

### Docker

```bash
# Detener servicios
docker-compose -f docker-compose.prod.yml down

# Reconstruir imagen
docker-compose -f docker-compose.prod.yml build --no-cache backend

# Ver uso de espacio
docker system df

# Limpiar recursos
docker system prune -a
```

### Base de datos

```bash
# Acceder a psql
docker-compose -f docker-compose.prod.yml exec db psql -U tienda_user -d tienda_asiatica

# Ver tablas
\dt

# Salir
\q
```

### Actualizar la aplicación

```bash
# Pull últimos cambios
git pull origin main

# Backend
cd backend
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Frontend
cd frontend
docker-compose -f docker-compose.prod.yml build --build-arg VITE_API_BASE_URL=https://api.tudominio.com
docker-compose -f docker-compose.prod.yml up -d
```

---

## Checklist de Producción

### Seguridad
- [ ] SECRET_KEY generado con `openssl rand -hex 32`
- [ ] Contraseñas de base de datos seguras
- [ ] CORS configurado solo para dominios permitidos
- [ ] SSL/TLS configurado (HTTPS)
- [ ] Firewall configurado (solo puertos necesarios)
- [ ] Rate limiting habilitado
- [ ] Emails configurados con App Passwords

### Backups
- [ ] Backups automáticos configurados
- [ ] Backups testeados (restore exitoso)
- [ ] Backups guardados fuera del servidor

### Monitoring
- [ ] Health checks funcionando
- [ ] Logs estructurados configurados
- [ ] Monitoring externo configurado (Uptime Robot, Sentry)
- [ ] Alertas configuradas para errores críticos

### Performance
- [ ] Redis cache habilitado
- [ ] Imágenes optimizadas (WebP, thumbnails)
- [ ] Nginx gzip habilitado
- [ ] CDN configurado (Cloudflare, CloudFront)

### CI/CD
- [ ] GitHub Actions workflows funcionando
- [ ] Tests pasando en CI
- [ ] Deployment automático configurado

---

## Recursos adicionales

- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [GitHub Actions](https://docs.github.com/en/actions)

---

## Soporte

Para problemas o preguntas:
- Crear un issue en GitHub
- Revisar logs con `docker-compose logs`
- Verificar health checks en `/health/detailed`

---

**Última actualización**: Enero 2025
