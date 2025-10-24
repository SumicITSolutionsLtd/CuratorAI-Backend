"""
ASGI config for curator project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'curator.settings.development')

application = get_asgi_application()

