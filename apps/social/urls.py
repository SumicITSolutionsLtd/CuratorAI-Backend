"""
URL patterns for social app.
"""
from django.urls import path
from .views import (
    SocialFeedView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    LikePostView,
    SavePostView,
    SharePostView,
    PostCommentsView,
    AddCommentView,
    UpdateCommentView,
    DeleteCommentView,
    LikeCommentView,
)

app_name = 'social'

urlpatterns = [
    # Feed
    path('feed/', SocialFeedView.as_view(), name='feed'),
    
    # Posts
    path('posts/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    # Post Actions
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='post-like'),
    path('posts/<int:post_id>/save/', SavePostView.as_view(), name='post-save'),
    path('posts/<int:post_id>/share/', SharePostView.as_view(), name='post-share'),
    
    # Comments
    path('posts/<int:post_id>/comments/', PostCommentsView.as_view(), name='post-comments'),
    path('posts/<int:post_id>/comments/add/', AddCommentView.as_view(), name='comment-add'),
    path('comments/<int:pk>/update/', UpdateCommentView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', DeleteCommentView.as_view(), name='comment-delete'),
    path('comments/<int:comment_id>/like/', LikeCommentView.as_view(), name='comment-like'),
]

