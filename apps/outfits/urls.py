"""
URL patterns for outfits app.
"""
from django.urls import path
from .views import (
    OutfitListCreateView,
    OutfitDetailView,
    OutfitLikeView,
    OutfitSaveView,
    UserOutfitsView,
)

app_name = 'outfits'

urlpatterns = [
    path('', OutfitListCreateView.as_view(), name='outfit-list-create'),
    path('<int:pk>/', OutfitDetailView.as_view(), name='outfit-detail'),
    path('<int:pk>/like/', OutfitLikeView.as_view(), name='outfit-like'),
    path('<int:pk>/save/', OutfitSaveView.as_view(), name='outfit-save'),
    path('user/<int:user_id>/', UserOutfitsView.as_view(), name='user-outfits'),
]

