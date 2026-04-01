#!/bin/bash
# PostgreSQL restore script for wb-collector
set -e

BACKUP_DIR="/backups"

if [ -z "$1" ]; then
    echo "Usage: restore.sh <backup_file>"
    echo ""
    echo "Available backups:"
    ls -lh "${BACKUP_DIR}"/wb_collector_*.sql.gz 2>/dev/null || echo "  (none)"
    exit 1
fi

BACKUP_FILE="$1"
if [ ! -f "${BACKUP_FILE}" ]; then
    BACKUP_FILE="${BACKUP_DIR}/$1"
fi

if [ ! -f "${BACKUP_FILE}" ]; then
    echo "[restore] Error: File not found: $1"
    exit 1
fi

echo "[restore] Restoring from: ${BACKUP_FILE}"
echo "[restore] WARNING: This will overwrite the current database!"
echo "[restore] Press Ctrl+C to cancel, or wait 5 seconds..."
sleep 5

gunzip -c "${BACKUP_FILE}" | PGPASSWORD="${DB_PASS}" psql \
    -h "${DB_HOST:-postgres}" \
    -p "${DB_PORT:-5432}" \
    -U "${DB_USER:-wb_user}" \
    -d "${DB_NAME:-wb_collector}" \
    --single-transaction

echo "[restore] Done!"
