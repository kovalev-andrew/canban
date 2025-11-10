#!/bin/bash

# Don't exit on error - we want to see what's happening
set +e

echo "=== Starting Django application ==="
echo "PORT: ${PORT:-8000}"
echo "DATABASE_URL: ${DATABASE_URL:+SET}"
echo "PGHOST: ${PGHOST:-not set}"
echo "DB_HOST: ${DB_HOST:-not set}"

# Check if DATABASE_URL is set (Railway provides this automatically)
if [ -z "$DATABASE_URL" ] && [ -z "$PGHOST" ] && [ -z "$DB_HOST" ]; then
    echo "WARNING: DATABASE_URL or database connection variables are not set."
    echo "If you're on Railway, please ensure PostgreSQL service is connected."
    echo "Attempting to continue, but database operations will fail..."
fi

# Run migrations
echo "=== Running migrations ==="
python manage.py migrate --noinput
MIGRATE_EXIT_CODE=$?

if [ $MIGRATE_EXIT_CODE -ne 0 ]; then
    echo "ERROR: Database migration failed with exit code $MIGRATE_EXIT_CODE"
    echo "If on Railway, ensure PostgreSQL service is connected and DATABASE_URL is set."
    echo "Continuing anyway to see if server can start..."
else
    echo "=== Migrations completed successfully ==="
fi

# Collect static files
echo "=== Collecting static files ==="
python manage.py collectstatic --noinput
COLLECTSTATIC_EXIT_CODE=$?

if [ $COLLECTSTATIC_EXIT_CODE -ne 0 ]; then
    echo "WARNING: Static files collection failed, continuing..."
else
    echo "=== Static files collected successfully ==="
fi

# Start server
echo "=== Starting Django development server ==="
echo "Listening on 0.0.0.0:${PORT:-8000}"

# Use exec to replace shell process with Django server
exec python manage.py runserver 0.0.0.0:${PORT:-8000}

