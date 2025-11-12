#!/bin/bash

# ===================================
# PostgreSQL Database Restore Script
# ===================================
# This script restores a PostgreSQL database from a backup file
# Usage: ./restore_db.sh <backup_file>

set -e

# Check if backup file is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <backup_file>"
    echo "Example: $0 /backup/backup_tienda_asiatica_20250112_120000.sql.gz"
    exit 1
fi

BACKUP_FILE="$1"

# Check if backup file exists
if [ ! -f "${BACKUP_FILE}" ]; then
    echo "Error: Backup file not found: ${BACKUP_FILE}"
    exit 1
fi

# Load environment variables
if [ -f .env.prod ]; then
    export $(cat .env.prod | grep -v '^#' | xargs)
fi

echo "=========================================="
echo "PostgreSQL Database Restore"
echo "=========================================="
echo "Database: ${POSTGRES_DB}"
echo "Host: ${POSTGRES_HOST}"
echo "Backup file: ${BACKUP_FILE}"
echo "=========================================="
echo ""
echo "WARNING: This will replace all data in the database!"
read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Restore cancelled."
    exit 0
fi

echo ""
echo "Restoring database..."

# Restore backup
gunzip -c "${BACKUP_FILE}" | PGPASSWORD="${POSTGRES_PASSWORD}" psql \
    -h "${POSTGRES_HOST}" \
    -p "${POSTGRES_PORT}" \
    -U "${POSTGRES_USER}" \
    -d "${POSTGRES_DB}"

# Check if restore was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ Database restored successfully!"
    echo "=========================================="
else
    echo ""
    echo "=========================================="
    echo "✗ Restore failed!"
    echo "=========================================="
    exit 1
fi
