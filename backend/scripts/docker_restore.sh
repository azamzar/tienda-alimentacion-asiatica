#!/bin/bash

# ===================================
# Docker Database Restore Helper
# ===================================
# This script runs the restore inside the Docker container
# Usage: ./docker_restore.sh <backup_file>

set -e

# Check if backup file is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <backup_file>"
    echo ""
    echo "Available backups:"
    ls -1 ./backup/backup_*.sql.gz 2>/dev/null || echo "  (no backups found)"
    echo ""
    echo "Example:"
    echo "  $0 ./backup/backup_tienda_asiatica_20250112_120000.sql.gz"
    exit 1
fi

BACKUP_FILE="$1"

# Check if backup file exists
if [ ! -f "${BACKUP_FILE}" ]; then
    echo "Error: Backup file not found: ${BACKUP_FILE}"
    exit 1
fi

echo "=========================================="
echo "Running Database Restore (Docker)"
echo "=========================================="

# Check if container is running
if ! docker ps | grep -q "tienda-backend"; then
    echo "Error: Backend container is not running"
    echo "Start the container with: docker-compose -f docker-compose.prod.yml up -d"
    exit 1
fi

# Get the container path (file should be in mounted volume)
CONTAINER_BACKUP_FILE="/app/${BACKUP_FILE#./}"

echo "Backup file: ${BACKUP_FILE}"
echo "Container path: ${CONTAINER_BACKUP_FILE}"
echo ""
echo "WARNING: This will replace all data in the database!"
read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Restore cancelled."
    exit 0
fi

# Run restore inside container
docker exec tienda-backend /app/scripts/restore_db.sh "${CONTAINER_BACKUP_FILE}"

echo ""
echo "=========================================="
echo "Restore completed!"
echo "=========================================="
