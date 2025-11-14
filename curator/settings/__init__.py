"""
Settings package for CuratorAI project.

Import appropriate settings based on environment.
"""
import os

# Check DJANGO_SETTINGS_MODULE first to avoid conflicts
# If explicitly set to production, use production settings
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', '')
if 'production' in settings_module:
    from .production import *  # noqa
elif 'development' in settings_module:
    from .development import *  # noqa
else:
    # Fall back to DJANGO_ENVIRONMENT if DJANGO_SETTINGS_MODULE is not specific
    ENVIRONMENT = os.environ.get('DJANGO_ENVIRONMENT', 'development')
    
    if ENVIRONMENT == 'production':
        from .production import *  # noqa
    elif ENVIRONMENT == 'staging':
        from .production import *  # noqa
    else:
        from .development import *  # noqa

