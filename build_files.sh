#!/bin/bash

# Install dependencies
pip install -r requirements/production.txt

# Collect static files
python manage.py collectstatic --noinput --clear

# Make migrations (optional, but recommended)
python manage.py makemigrations --noinput
python manage.py migrate --noinput

