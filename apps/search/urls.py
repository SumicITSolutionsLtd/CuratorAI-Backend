"""
URL patterns for search app.
"""
from django.urls import path
from .views import VisualSearchUploadView, VisualSearchURLView

app_name = 'search'

urlpatterns = [
    # Visual search endpoints
    path('visual/', VisualSearchUploadView.as_view(), name='visual-search'),
    path('visual/url/', VisualSearchURLView.as_view(), name='visual-search-url'),
]

