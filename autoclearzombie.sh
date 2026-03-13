#!/bin/bash
# autoclearzombie.sh - Auto clear zombie sessions di radacct
# Zombie = session yang acctstoptime NULL dan sudah lebih dari X jam
#
# Cron example (setiap 30 menit):
#   */30 * * * * /path/to/autoclearzombie.sh >> /var/log/autoclearzombie.log 2>&1

# --- Konfigurasi ---
DB_HOST="localhost"
DB_PORT="3306"
DB_USER="radius"
DB_PASS="radius_password"
DB_NAME="radius"

# Session dianggap zombie jika sudah idle lebih dari N jam
ZOMBIE_THRESHOLD_HOURS=24

# --- Eksekusi ---
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

RESULT=$(mariadb -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" --skip-ssl -N -e "
    UPDATE radacct
    SET
        acctstoptime       = NOW(),
        acctterminatecause = 'Admin-Reset',
        acctsessiontime    = TIMESTAMPDIFF(SECOND, acctstarttime, NOW())
    WHERE acctstoptime IS NULL
      AND acctstarttime < DATE_SUB(NOW(), INTERVAL $ZOMBIE_THRESHOLD_HOURS HOUR);
    SELECT ROW_COUNT();
" 2>&1)

AFFECTED=$(echo "$RESULT" | tail -1)

echo "[$TIMESTAMP] Cleared $AFFECTED zombie session(s) (threshold: ${ZOMBIE_THRESHOLD_HOURS}h)"
