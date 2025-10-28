"""
Lookbook models for CuratorAI.
"""
from django.db import models
from django.conf import settings


class Lookbook(models.Model):
    """
    Lookbook - collection of outfits curated around a theme.
    """
    SEASON_CHOICES = [
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('fall', 'Fall'),
        ('winter', 'Winter'),
        ('all', 'All Season'),
    ]
    
    OCCASION_CHOICES = [
        ('casual', 'Casual'),
        ('work', 'Work'),
        ('formal', 'Formal'),
        ('party', 'Party'),
        ('travel', 'Travel'),
        ('vacation', 'Vacation'),
    ]
    
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lookbooks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='lookbooks/', blank=True)
    
    # Categorization
    season = models.CharField(max_length=20, choices=SEASON_CHOICES)
    occasion = models.CharField(max_length=20, choices=OCCASION_CHOICES)
    style = models.JSONField(default=list, help_text='Style tags')
    tags = models.JSONField(default=list, help_text='General tags')
    
    # Social metrics
    likes_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    
    # Visibility
    is_public = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lookbooks'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['creator', '-created_at']),
            models.Index(fields=['is_public', 'is_featured', '-likes_count']),
            models.Index(fields=['season', 'occasion']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.creator.username}"


class LookbookOutfit(models.Model):
    """
    Outfit in a lookbook.
    """
    lookbook = models.ForeignKey(Lookbook, on_delete=models.CASCADE, related_name='outfits')
    outfit = models.ForeignKey('outfits.Outfit', on_delete=models.CASCADE, related_name='in_lookbooks')
    order = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'lookbook_outfits'
        ordering = ['order', 'created_at']
        unique_together = ('lookbook', 'outfit')
    
    def __str__(self):
        return f"{self.outfit.title} in {self.lookbook.title}"


class LookbookLike(models.Model):
    """
    Likes on lookbooks.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lookbook_likes')
    lookbook = models.ForeignKey(Lookbook, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'lookbook_likes'
        unique_together = ('user', 'lookbook')
        indexes = [
            models.Index(fields=['lookbook', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} likes {self.lookbook.title}"

