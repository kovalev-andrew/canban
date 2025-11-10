#!/bin/bash
set -e

# Check if DATABASE_URL is set (Railway provides this automatically)
if [ -z "$DATABASE_URL" ] && [ -z "$PGHOST" ] && [ -z "$DB_HOST" ]; then
    echo "WARNING: DATABASE_URL or database connection variables are not set."
    echo "If you're on Railway, please ensure PostgreSQL service is connected."
    echo "Attempting to continue, but database operations will fail..."
fi

# Run migrations (will fail if database is not configured, but that's OK for now)
python manage.py migrate --noinput || {
    echo "ERROR: Database migration failed. Please check your database configuration."
    echo "If on Railway, ensure PostgreSQL service is connected and DATABASE_URL is set."
    exit 1
}

# Collect static files (skip if fails, but try to collect)
python manage.py collectstatic --noinput || echo "Warning: Static files collection failed, continuing..."

# Start server
# Railway provides PORT environment variable
exec python manage.py runserver 0.0.0.0:${PORT:-8000}

