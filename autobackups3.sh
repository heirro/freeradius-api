#!/bin/bash

# Configuration
REMOTE="s3"
BUCKET="backup-db"
BACKUP_PATH="radiusdb/"
BACKUP_DATE=$(date +%Y%m%d)
FILENAME="${BACKUP_DATE}.sql.gz"
TEMP_DIR="/tmp/mariadb-backup"
LOCAL_FILE="${TEMP_DIR}/${FILENAME}"

# Database credentials
DB_HOST="localhost"
DB_PORT="3306"
DB_USER="raduser"
DB_PASS="radpass"
DB_NAME="radiusdb"

# Create temp directory
mkdir -p ${TEMP_DIR}

# Streaming dump & upload ke R2 (tanpa simpan lokal)
echo "Starting backup at $(date)"
mariadb-dump --skip-ssl \
  -h ${DB_HOST} \
  --port ${DB_PORT} \
  -u ${DB_USER} \
  -p"${DB_PASS}" \
  ${DB_NAME} \
  --single-transaction \
  --quick \
  --lock-tables=false | gzip > ${LOCAL_FILE}

# Check if dump successful
if [ $? -ne 0 ] || [ ! -f ${LOCAL_FILE} ]; then
    echo "ERROR: Database dump failed!" >&2
    exit 1
fi

echo "Dump completed: ${LOCAL_FILE} ($(du -h ${LOCAL_FILE} | cut -f1))"

# Step 2: Upload to R2
echo "Uploading to R2..."
rclone copy ${LOCAL_FILE} ${REMOTE}:${BUCKET}/${BACKUP_PATH}/ \
  --progress \
  --checksum

# Check if upload successful
if [ $? -eq 0 ]; then
    echo "Upload successful to R2: ${BUCKET}/${BACKUP_PATH}/${FILENAME}"
    
    # Step 3: Remove local file after successful upload
    rm -f ${LOCAL_FILE}
    echo "Local temporary file removed: ${LOCAL_FILE}"
    
    # Optional: cleanup empty temp dir
    rmdir ${TEMP_DIR} 2>/dev/null
    
    echo "Backup completed successfully at $(date)"
else
    echo "ERROR: Upload to R2 failed! Local file preserved at: ${LOCAL_FILE}" >&2
    exit 1
fi