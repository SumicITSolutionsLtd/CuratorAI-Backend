#!/bin/bash
set -e  # Exit on any error

# Set production environment
export DJANGO_ENVIRONMENT=production
export DJANGO_SETTINGS_MODULE=curator.settings.production
export DJANGO_BUILD_MODE=1  # Indicate we're in build mode

# Set a dummy DATABASE_URL if not already set to avoid SQLite (not available in Vercel build)
# This prevents Django from trying to use SQLite during build
if [ -z "$DATABASE_URL" ]; then
    export DATABASE_URL="postgresql://build_user:build_pass@localhost:5432/build_db"
fi

# Install dependencies
pip install -r requirements/production.txt

# Collect static files only (no database operations needed for build)
# Migrations should be run separately or at runtime
python manage.py collectstatic --noinput --clear

# Note: Migrations are skipped during build as they require database access
# Run migrations separately or configure them to run at runtime

