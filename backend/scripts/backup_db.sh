#!/bin/bash

# ===================================
# PostgreSQL Database Backup Script
# ===================================
# This script creates a compressed backup of the PostgreSQL database
# Usage: ./backup_db.sh

set -e

# Load environment variables
if [ -f .env.prod ]; then
    export $(cat .env.prod | grep -v '^#' | xargs)
fi

# Configuration
BACKUP_DIR="${BACKUP_DIR:-/backup}"
BACKUP_RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-7}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/backup_${POSTGRES_DB}_${TIMESTAMP}.sql.gz"

echo "=========================================="
echo "PostgreSQL Database Backup"
echo "=========================================="
echo "Database: ${POSTGRES_DB}"
echo "Host: ${POSTGRES_HOST}"
echo "Backup file: ${BACKUP_FILE}"
echo "=========================================="

# Create backup directory if it doesn't exist
mkdir -p "${BACKUP_DIR}"

# Create backup
echo "Creating backup..."
PGPASSWORD="${POSTGRES_PASSWORD}" pg_dump \
    -h "${POSTGRES_HOST}" \
    -p "${POSTGRES_PORT}" \
    -U "${POSTGRES_USER}" \
    -d "${POSTGRES_DB}" \
    --no-owner \
    --no-acl \
    --clean \
    --if-exists \
    | gzip > "${BACKUP_FILE}"

# Check if backup was successful
if [ $? -eq 0 ]; then
    echo "✓ Backup created successfully: ${BACKUP_FILE}"

    # Get backup file size
    BACKUP_SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
    echo "✓ Backup size: ${BACKUP_SIZE}"
else
    echo "✗ Backup failed!"
    exit 1
fi

# Remove old backups
echo "=========================================="
echo "Cleaning up old backups (older than ${BACKUP_RETENTION_DAYS} days)..."
find "${BACKUP_DIR}" -name "backup_*.sql.gz" -type f -mtime +${BACKUP_RETENTION_DAYS} -delete

# Count remaining backups
BACKUP_COUNT=$(ls -1 "${BACKUP_DIR}"/backup_*.sql.gz 2>/dev/null | wc -l)
echo "✓ Total backups: ${BACKUP_COUNT}"
echo "=========================================="
echo "Backup completed successfully!"
echo "=========================================="
