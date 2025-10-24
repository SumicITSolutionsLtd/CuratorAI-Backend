"""
Development settings for CuratorAI project.
"""
from .base import *

DEBUG = True

# Use SQLite for easy development setup (no PostgreSQL required)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Add debug toolbar for development
INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Show toolbar for localhost
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# Console email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True

# Disable password validators in development for easier testing
AUTH_PASSWORD_VALIDATORS = []

# Use console logging in development
LOGGING['root']['level'] = 'DEBUG'
LOGGING['loggers']['django']['level'] = 'DEBUG'

