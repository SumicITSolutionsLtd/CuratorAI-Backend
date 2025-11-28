"""
URL configuration for CuratorAI project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.shortcuts import render
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Admin customization
admin.site.site_header = "CuratorAI Admin"
admin.site.site_title = "CuratorAI Admin Portal"
admin.site.index_title = "Welcome to CuratorAI Admin Portal"

def api_root(request):
    """Root API endpoint - shows HTML landing page or JSON based on Accept header"""
    # Return JSON if client requests JSON (e.g., API clients)
    if request.META.get('HTTP_ACCEPT', '').startswith('application/json'):
        return JsonResponse({
            'message': 'Welcome to CuratorAI API',
            'version': '1.0.0',
            'status': 'operational',
            'documentation': {
                'swagger': request.build_absolute_uri('/api/schema/swagger-ui/'),
                'redoc': request.build_absolute_uri('/api/schema/redoc/'),
                'schema': request.build_absolute_uri('/api/schema/'),
            },
            'endpoints': {
                'authentication': request.build_absolute_uri('/api/v1/auth/'),
                'outfits': request.build_absolute_uri('/api/v1/outfits/'),
                'wardrobe': request.build_absolute_uri('/api/v1/wardrobe/'),
                'notifications': request.build_absolute_uri('/api/v1/notifications/'),
                'cart': request.build_absolute_uri('/api/v1/cart/'),
                'social': request.build_absolute_uri('/api/v1/social/'),
                'lookbooks': request.build_absolute_uri('/api/v1/lookbooks/'),
            }
        })
    
    # Return HTML landing page for browsers
    context = {
        'api_version': '1.0.0',
        'swagger_url': request.build_absolute_uri('/api/schema/swagger-ui/'),
        'redoc_url': request.build_absolute_uri('/api/schema/redoc/'),
        'admin_url': request.build_absolute_uri('/admin/'),
        'endpoints': {
            'authentication': request.build_absolute_uri('/api/v1/auth/'),
            'outfits': request.build_absolute_uri('/api/v1/outfits/'),
            'wardrobe': request.build_absolute_uri('/api/v1/wardrobe/'),
            'notifications': request.build_absolute_uri('/api/v1/notifications/'),
            'cart': request.build_absolute_uri('/api/v1/cart/'),
            'social': request.build_absolute_uri('/api/v1/social/'),
            'lookbooks': request.build_absolute_uri('/api/v1/lookbooks/'),
        }
    }
    return render(request, 'landing.html', context)


urlpatterns = [
    # Root API endpoint
    path('', api_root, name='api-root'),
    
    # Django Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API v1 Routes
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/outfits/', include('apps.outfits.urls')),
    path('api/v1/wardrobe/', include('apps.wardrobe.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/cart/', include('apps.cart.urls')),
    path('api/v1/social/', include('apps.social.urls')),
    path('api/v1/lookbooks/', include('apps.lookbooks.urls')),
    
    # Test Dashboard
    path('test-dashboard/', include('apps.test_dashboard.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]

