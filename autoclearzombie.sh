#!/bin/bash
# autoclearzombie.sh - Auto clear zombie sessions di radacct
# Zombie = session yang acctstoptime NULL dan tidak dapat Interim-Update
# selama lebih dari N menit (router mati / koneksi putus mendadak).
#
# Cron example (setiap 5 menit):
#   */5 * * * * /path/to/autoclearzombie.sh >> /var/log/autoclearzombie.log 2>&1

# --- Konfigurasi ---
DB_HOST="localhost"
DB_PORT="3306"
DB_USER="radius"
DB_PASS="radius_password"
DB_NAME="radius"

# Session dianggap zombie jika tidak dapat update lebih dari N menit.
# Harus > 2x Interim-Update router (toleransi 1 miss).
# Contoh: Interim-Update 5 menit → threshold 10-15 menit.
ZOMBIE_THRESHOLD_MINUTES=10

# --- Eksekusi ---
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

RESULT=$(mariadb -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" --skip-ssl -N -e "
    UPDATE radacct
    SET
        acctstoptime       = NOW(),
        acctterminatecause = 'Admin-Reset',
        acctsessiontime    = TIMESTAMPDIFF(SECOND, acctstarttime, NOW())
    WHERE acctstoptime IS NULL
      AND COALESCE(acctupdatetime, acctstarttime) < DATE_SUB(NOW(), INTERVAL $ZOMBIE_THRESHOLD_MINUTES MINUTE);
    SELECT ROW_COUNT();
" 2>&1)

AFFECTED=$(echo "$RESULT" | tail -1)

echo "[$TIMESTAMP] Cleared $AFFECTED zombie session(s) (threshold: ${ZOMBIE_THRESHOLD_MINUTES}m)"
