#!/bin/bash
set -e

# Run migrations
python manage.py migrate --noinput

# Collect static files (skip if fails, but try to collect)
python manage.py collectstatic --noinput || echo "Warning: Static files collection failed, continuing..."

# Start server
# Railway provides PORT environment variable
exec python manage.py runserver 0.0.0.0:${PORT:-8000}

