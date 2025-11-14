#!/bin/bash
set -e  # Exit on any error

# Set production environment
export DJANGO_ENVIRONMENT=production
export DJANGO_SETTINGS_MODULE=curator.settings.production
export DJANGO_BUILD_MODE=1  # Indicate we're in build mode

# Install dependencies
pip install -r requirements/production.txt

# Collect static files only (no database operations needed for build)
# Migrations should be run separately or at runtime
python manage.py collectstatic --noinput --clear

# Note: Migrations are skipped during build as they require database access
# Run migrations separately or configure them to run at runtime

