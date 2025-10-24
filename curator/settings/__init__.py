"""
Settings package for CuratorAI project.

Import appropriate settings based on environment.
"""
import os

# Determine which settings to use
ENVIRONMENT = os.environ.get('DJANGO_ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    from .production import *  # noqa
elif ENVIRONMENT == 'staging':
    from .production import *  # noqa
else:
    from .development import *  # noqa

