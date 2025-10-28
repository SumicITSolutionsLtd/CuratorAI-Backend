"""
URL patterns for lookbooks app.
"""
from django.urls import path
from .views import (
    LookbookListView,
    FeaturedLookbooksView,
    LookbookDetailView,
    LookbookCreateView,
    LookbookUpdateView,
    LookbookDeleteView,
    LikeLookbookView,
    LookbookCommentsView,
)

app_name = 'lookbooks'

urlpatterns = [
    # Lookbooks
    path('', LookbookListView.as_view(), name='lookbook-list'),
    path('featured/', FeaturedLookbooksView.as_view(), name='featured-lookbooks'),
    path('create/', LookbookCreateView.as_view(), name='lookbook-create'),
    path('<int:pk>/', LookbookDetailView.as_view(), name='lookbook-detail'),
    path('<int:pk>/update/', LookbookUpdateView.as_view(), name='lookbook-update'),
    path('<int:pk>/delete/', LookbookDeleteView.as_view(), name='lookbook-delete'),
    
    # Actions
    path('<int:lookbook_id>/like/', LikeLookbookView.as_view(), name='lookbook-like'),
    path('<int:lookbook_id>/comments/', LookbookCommentsView.as_view(), name='lookbook-comments'),
]

