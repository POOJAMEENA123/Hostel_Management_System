#!/bin/bash

MYSQL_DATA=/home/runner/mysql-data
MYSQL_RUN=/home/runner/mysql-run
MYSQL_SOCK=$MYSQL_RUN/mysql.sock
APP_DIR=/home/runner/workspace

mkdir -p "$MYSQL_DATA" "$MYSQL_RUN"

# Initialize MySQL data directory if needed
if [ ! -f "$MYSQL_DATA/mysql.ibd" ]; then
  echo "[start.sh] Initializing MySQL data directory..."
  mysqld --initialize-insecure --user=runner --datadir="$MYSQL_DATA" 2>&1
  echo "[start.sh] Initialization done."
fi

# Start MySQL in the background
echo "[start.sh] Starting MySQL..."
mysqld --user=runner \
  --datadir="$MYSQL_DATA" \
  --socket="$MYSQL_SOCK" \
  --pid-file="$MYSQL_RUN/mysql.pid" \
  --port=3306 \
  --mysqlx=OFF \
  --log-error="$MYSQL_DATA/mysql.err" &

MYSQLD_PID=$!

# Wait for MySQL to be ready (up to 30s)
for i in $(seq 1 30); do
  if mysqladmin --socket="$MYSQL_SOCK" status >/dev/null 2>&1; then
    echo "[start.sh] MySQL is ready."
    break
  fi
  echo "[start.sh] Waiting for MySQL... ($i/30)"
  sleep 1
done

# Create database and load schema if needed
DB_EXISTS=$(mysql -u root --socket="$MYSQL_SOCK" -e "SHOW DATABASES LIKE 'hostel_management_system';" 2>/dev/null | grep -c hostel || true)
if [ "$DB_EXISTS" -eq 0 ]; then
  echo "[start.sh] Creating database and loading schema..."
  mysql -u root --socket="$MYSQL_SOCK" -e "CREATE DATABASE hostel_management_system;"

  for SQL_FILE in "$APP_DIR"/database/*.sql; do
    echo "[start.sh] Loading $(basename $SQL_FILE)..."
    mysql -u root --socket="$MYSQL_SOCK" hostel_management_system < "$SQL_FILE"
  done

  mysql -u root --socket="$MYSQL_SOCK" -e \
    "ALTER USER 'root'@'localhost' IDENTIFIED BY 'root'; FLUSH PRIVILEGES;"
  echo "[start.sh] Database setup complete."
fi

echo "[start.sh] Starting PHP server on port 5000..."
cd "$APP_DIR"
php -S 0.0.0.0:5000
