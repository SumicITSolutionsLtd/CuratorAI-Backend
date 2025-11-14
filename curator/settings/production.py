"""
Production settings for CuratorAI project.
"""
from .base import *
import dj_database_url

DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)

# Vercel/Production specific settings
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='curator-ai-backend.vercel.app,*.vercel.app,localhost,127.0.0.1', cast=Csv())

# Security settings (adjusted for Vercel)
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 0  # Disable for Vercel
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# CORS settings for production
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='', cast=Csv())

# Database - Use PostgreSQL in production if available, fallback to SQLite
# During build (collectstatic), we use in-memory SQLite to avoid file system issues
import os
IS_BUILD = os.environ.get('DJANGO_BUILD_MODE') == '1' or (
    os.environ.get('VERCEL', '') == '1' and os.environ.get('VERCEL_ENV') != 'production'
)

# Disable Celery apps during build as they require database access
# Also set STATIC_ROOT to match Vercel's expected output directory
if IS_BUILD:
    INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in [
        'django_celery_beat',
        'django_celery_results',
    ]]
    # Vercel expects static files in staticfiles_build directory
    STATIC_ROOT = BASE_DIR / 'staticfiles_build'

DATABASE_URL = config('DATABASE_URL', default=None)
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)
elif IS_BUILD:
    # During build, use PostgreSQL with dummy connection to avoid SQLite dependency
    # SQLite is not available in Vercel build environment
    # This will fail gracefully if Django tries to connect (which it shouldn't during collectstatic)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'build_db',
            'USER': 'build_user',
            'PASSWORD': 'build_pass',
            'HOST': 'localhost',
            'PORT': '5432',
            'OPTIONS': {
                'connect_timeout': 1,  # Fail fast if connection attempted
            },
        }
    }
    # Prevent database connection during build by setting connection max age to 0
    DATABASES['default']['CONN_MAX_AGE'] = 0
else:
    # Use SQLite for Vercel runtime (ephemeral, but works for testing)
    # Note: This requires SQLite to be available at runtime
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/db.sqlite3',  # Vercel temp directory
        }
    }

# Production email backend (configure with your SMTP settings)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# Production logging
# Use only console handler for Vercel/serverless environments
# Vercel automatically captures console output in their logging system
LOGGING['root']['handlers'] = ['console']
LOGGING['root']['level'] = 'INFO'

