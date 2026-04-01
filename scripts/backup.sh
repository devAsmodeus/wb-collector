#!/bin/bash
# PostgreSQL backup script for wb-collector
set -e

BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/wb_collector_${TIMESTAMP}.sql.gz"

# Create backup directory if not exists
mkdir -p "${BACKUP_DIR}"

# Run pg_dump and compress
echo "[backup] Starting backup at ${TIMESTAMP}..."
PGPASSWORD="${DB_PASS}" pg_dump \
    -h "${DB_HOST:-postgres}" \
    -p "${DB_PORT:-5432}" \
    -U "${DB_USER:-wb_user}" \
    -d "${DB_NAME:-wb_collector}" \
    --no-owner \
    --no-privileges \
    | gzip > "${BACKUP_FILE}"

echo "[backup] Backup saved: ${BACKUP_FILE} ($(du -h ${BACKUP_FILE} | cut -f1))"

# Remove backups older than 7 days
find "${BACKUP_DIR}" -name "wb_collector_*.sql.gz" -mtime +7 -delete
echo "[backup] Cleaned up backups older than 7 days"

# List current backups
echo "[backup] Current backups:"
ls -lh "${BACKUP_DIR}"/wb_collector_*.sql.gz 2>/dev/null || echo "  (none)"
