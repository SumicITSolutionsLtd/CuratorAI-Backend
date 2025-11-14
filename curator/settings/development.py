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

# Add debug toolbar for development (if available)
try:
    import debug_toolbar
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
except ImportError:
    pass  # debug_toolbar not installed, skip it

# Add django-extensions (if available)
try:
    import django_extensions
    INSTALLED_APPS += [
        'django_extensions',
    ]
except ImportError:
    pass  # django_extensions not installed, skip it

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

