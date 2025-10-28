"""
Social media models for CuratorAI - Posts, Comments, Likes, Feed.
"""
from django.db import models
from django.conf import settings


class Post(models.Model):
    """
    Social post model - user's outfit/fashion posts.
    """
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends Only'),
        ('private', 'Private'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(max_length=2200)
    
    # Tags
    tags = models.JSONField(default=list, help_text='Hashtags')
    
    # Optional outfit reference
    outfit = models.ForeignKey('outfits.Outfit', on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    
    # Tagged items (from wardrobe or outfit items)
    tagged_items = models.JSONField(default=list, help_text='Items tagged in post with positions')
    
    # Location
    location_name = models.CharField(max_length=200, blank=True)
    location_lat = models.FloatField(null=True, blank=True)
    location_lng = models.FloatField(null=True, blank=True)
    
    # Social metrics
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    saves_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    
    # Privacy
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='public')
    
    # Soft delete
    is_deleted = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['privacy', '-created_at']),
            models.Index(fields=['-likes_count']),
            models.Index(fields=['is_deleted']),
        ]
    
    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"


class PostImage(models.Model):
    """
    Images for posts (1-10 per post).
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'post_images'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Image for post {self.post.id}"


class PostLike(models.Model):
    """
    Likes on posts.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'post_likes'
        unique_together = ('user', 'post')
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['post', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} likes post {self.post.id}"


class PostSave(models.Model):
    """
    Saved posts.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saves')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'post_saves'
        unique_together = ('user', 'post')
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['post', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} saved post {self.post.id}"


class Comment(models.Model):
    """
    Comments on posts.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)
    
    # Reply system
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    # Metrics
    likes_count = models.IntegerField(default=0)
    
    # Soft delete
    is_deleted = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', '-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['parent_comment']),
        ]
    
    def __str__(self):
        return f"Comment by {self.user.username} on post {self.post.id}"


class CommentLike(models.Model):
    """
    Likes on comments.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'comment_likes'
        unique_together = ('user', 'comment')
        indexes = [
            models.Index(fields=['comment', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} likes comment {self.comment.id}"

