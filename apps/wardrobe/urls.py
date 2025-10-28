"""
URL patterns for wardrobe app.
"""
from django.urls import path
from .views import (
    UserWardrobeView,
    WardrobeItemListView,
    WardrobeItemDetailView,
    WardrobeItemCreateView,
    WardrobeItemUpdateView,
    WardrobeItemDeleteView,
    WardrobeItemImageUploadView,
    MarkItemAsWornView,
    WardrobeStatisticsView,
)

app_name = 'wardrobe'

urlpatterns = [
    # Wardrobe
    path('users/<int:user_id>/wardrobe/', UserWardrobeView.as_view(), name='user-wardrobe'),
    path('users/<int:user_id>/wardrobe/stats/', WardrobeStatisticsView.as_view(), name='wardrobe-stats'),
    
    # Wardrobe Items
    path('items/', WardrobeItemListView.as_view(), name='item-list'),
    path('items/create/', WardrobeItemCreateView.as_view(), name='item-create'),
    path('items/<int:pk>/', WardrobeItemDetailView.as_view(), name='item-detail'),
    path('items/<int:pk>/update/', WardrobeItemUpdateView.as_view(), name='item-update'),
    path('items/<int:pk>/delete/', WardrobeItemDeleteView.as_view(), name='item-delete'),
    
    # Item Images
    path('items/<int:item_id>/images/', WardrobeItemImageUploadView.as_view(), name='item-image-upload'),
    
    # Wear Tracking
    path('items/<int:item_id>/worn/', MarkItemAsWornView.as_view(), name='mark-worn'),
]

