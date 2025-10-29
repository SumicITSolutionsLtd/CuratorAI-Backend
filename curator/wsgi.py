"""
WSGI config for curator project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'curator.settings.production')

application = get_wsgi_application()

# Vercel serverless function handler
app = application

