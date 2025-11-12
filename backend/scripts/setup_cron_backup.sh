#!/bin/bash

# ===================================
# Setup Automated Database Backups
# ===================================
# This script sets up a cron job to run daily database backups
# Usage: ./setup_cron_backup.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_SCRIPT="${SCRIPT_DIR}/backup_db.sh"

echo "=========================================="
echo "Setup Automated Database Backups"
echo "=========================================="

# Make backup script executable
chmod +x "${BACKUP_SCRIPT}"
echo "✓ Made backup script executable"

# Create cron job entry
# Runs daily at 2:00 AM
CRON_SCHEDULE="0 2 * * *"
CRON_JOB="${CRON_SCHEDULE} cd ${SCRIPT_DIR}/.. && ${BACKUP_SCRIPT} >> /var/log/backup.log 2>&1"

# Check if cron job already exists
crontab -l 2>/dev/null | grep -q "${BACKUP_SCRIPT}" && CRON_EXISTS=1 || CRON_EXISTS=0

if [ $CRON_EXISTS -eq 1 ]; then
    echo "⚠ Cron job already exists. Skipping..."
else
    # Add cron job
    (crontab -l 2>/dev/null; echo "${CRON_JOB}") | crontab -
    echo "✓ Cron job added successfully"
fi

echo ""
echo "Backup schedule: Daily at 2:00 AM"
echo "Log file: /var/log/backup.log"
echo ""
echo "Current cron jobs:"
crontab -l | grep "${BACKUP_SCRIPT}" || echo "  (none)"
echo ""
echo "=========================================="
echo "Setup completed!"
echo "=========================================="
echo ""
echo "To manually run a backup:"
echo "  ${BACKUP_SCRIPT}"
echo ""
echo "To view cron logs:"
echo "  tail -f /var/log/backup.log"
echo ""
echo "To list all cron jobs:"
echo "  crontab -l"
echo ""
echo "To remove the cron job:"
echo "  crontab -e"
echo "=========================================="
