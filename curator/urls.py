"""
URL configuration for CuratorAI project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Admin customization
admin.site.site_header = "CuratorAI Admin"
admin.site.site_title = "CuratorAI Admin Portal"
admin.site.index_title = "Welcome to CuratorAI Admin Portal"

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API v1 Routes
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/outfits/', include('apps.outfits.urls')),
    # TODO: Uncomment these when apps are created
    # path('api/v1/wardrobe/', include('apps.wardrobe.urls')),
    # path('api/v1/posts/', include('apps.posts.urls')),
    # path('api/v1/recommendations/', include('apps.recommendations.urls')),
    # path('api/v1/search/', include('apps.search.urls')),
    # path('api/v1/lookbooks/', include('apps.lookbooks.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]

