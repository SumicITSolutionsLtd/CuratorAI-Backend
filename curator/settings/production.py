"""
Production settings for CuratorAI project.
"""
from .base import *
import dj_database_url

DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)

# Vercel/Production specific settings
# ALLOWED_HOSTS handling for Vercel's dynamic domains
import os

# Get ALLOWED_HOSTS from environment variable
allowed_hosts_str = config('ALLOWED_HOSTS', default='', cast=str)
if allowed_hosts_str:
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
else:
    # Default to localhost if not specified
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Vercel provides VERCEL_URL environment variable with the current deployment URL
# Format: backend-zeta-henna-62.vercel.app (no protocol)
vercel_url = os.environ.get('VERCEL_URL', '')
if vercel_url:
    # Remove protocol if present
    vercel_host = vercel_url.replace('https://', '').replace('http://', '')
    if vercel_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(vercel_host)

# Also check HTTP_HOST header at runtime (handled by custom middleware if needed)
# For now, we'll rely on VERCEL_URL being set correctly
# If VERCEL_URL is not set, user must configure ALLOWED_HOSTS environment variable

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
# Allow all origins if explicitly set, otherwise use specific origins
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)

# Get CORS allowed origins from environment
cors_origins_str = config('CORS_ALLOWED_ORIGINS', default='', cast=str)
if cors_origins_str:
    # Parse from environment variable
    CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv())
    # Always ensure frontend domain is included
    frontend_url = 'https://curator-ai-phi.vercel.app'
    if frontend_url not in CORS_ALLOWED_ORIGINS:
        CORS_ALLOWED_ORIGINS.append(frontend_url)
else:
    # Default to frontend domain
    CORS_ALLOWED_ORIGINS = [
        'https://curator-ai-phi.vercel.app',
        'http://localhost:3000',
        'http://localhost:5173',
    ]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

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
else:
    # At runtime on Vercel, use WhiteNoise to serve static files
    # Static files are in staticfiles directory (copied from staticfiles_build during build)
    # This ensures they're accessible to the Python function
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    
    # Add WhiteNoise middleware for serving static files
    # It should be right after SecurityMiddleware
    if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
        MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    
    # WhiteNoise configuration
    WHITENOISE_USE_FINDERS = False
    WHITENOISE_AUTOREFRESH = False
    WHITENOISE_ROOT = STATIC_ROOT

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

