#!/bin/bash

# ===================================
# Docker Database Backup Helper
# ===================================
# This script runs the backup inside the Docker container
# Usage: ./docker_backup.sh

set -e

echo "=========================================="
echo "Running Database Backup (Docker)"
echo "=========================================="

# Check if container is running
if ! docker ps | grep -q "tienda-backend"; then
    echo "Error: Backend container is not running"
    echo "Start the container with: docker-compose -f docker-compose.prod.yml up -d"
    exit 1
fi

# Run backup inside container
docker exec tienda-backend /app/scripts/backup_db.sh

echo ""
echo "=========================================="
echo "Backup completed!"
echo "=========================================="
echo ""
echo "Backup files are stored in: ./backend/backup/"
echo ""
echo "To list backups:"
echo "  ls -lh ./backend/backup/"
echo ""
echo "To restore a backup:"
echo "  ./docker_restore.sh <backup_file>"
echo "=========================================="
