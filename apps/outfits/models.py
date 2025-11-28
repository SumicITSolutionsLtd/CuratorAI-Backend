"""
Outfit models for CuratorAI.
"""
from django.db import models
from django.conf import settings


class Outfit(models.Model):
    """
    Main outfit model representing a complete outfit recommendation or user-created outfit.
    """
    OCCASION_CHOICES = [
        ('casual', 'Casual'),
        ('work', 'Work/Professional'),
        ('formal', 'Formal'),
        ('party', 'Party/Event'),
        ('sport', 'Sport/Active'),
        ('date', 'Date'),
        ('travel', 'Travel'),
    ]
    
    SEASON_CHOICES = [
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('fall', 'Fall'),
        ('winter', 'Winter'),
        ('all', 'All Season'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='outfits')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Images
    main_image = models.ImageField(upload_to='outfits/', null=True, blank=True)
    main_image_url = models.URLField(blank=True, help_text='External image URL (used when main_image is not available)')
    thumbnail = models.ImageField(upload_to='outfits/thumbnails/', null=True, blank=True)
    
    # Categorization
    occasion = models.CharField(max_length=20, choices=OCCASION_CHOICES)
    season = models.CharField(max_length=20, choices=SEASON_CHOICES)
    style_tags = models.JSONField(default=list, help_text='List of style tags (e.g., minimalist, boho, streetwear)')
    color_palette = models.JSONField(default=list, help_text='Primary colors in the outfit')
    
    # AI Features
    ai_generated = models.BooleanField(default=False)
    confidence_score = models.FloatField(null=True, blank=True, help_text='AI confidence score (0-1)')
    embedding_vector = models.JSONField(null=True, blank=True, help_text='Image embedding for similarity search')
    
    # Social
    is_public = models.BooleanField(default=True)
    likes_count = models.IntegerField(default=0)
    saves_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'outfits'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['occasion', 'season']),
            models.Index(fields=['-likes_count']),
            models.Index(fields=['is_public', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.user.username}"


class OutfitItem(models.Model):
    """
    Individual clothing item within an outfit.
    """
    ITEM_TYPE_CHOICES = [
        ('top', 'Top'),
        ('bottom', 'Bottom'),
        ('dress', 'Dress'),
        ('outerwear', 'Outerwear'),
        ('shoes', 'Shoes'),
        ('accessory', 'Accessory'),
        ('bag', 'Bag'),
        ('jewelry', 'Jewelry'),
    ]
    
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE, related_name='items')
    
    # Item Details
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='outfit_items/', null=True, blank=True)
    image_url = models.URLField(blank=True, help_text='External image URL (used when image is not available)')
    
    # Product Information
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    size = models.CharField(max_length=20, blank=True)
    color = models.CharField(max_length=50, blank=True)
    material = models.CharField(max_length=100, blank=True)
    
    # Purchase Links
    purchase_url = models.URLField(blank=True)
    affiliate_link = models.URLField(blank=True)
    retailer = models.CharField(max_length=100, blank=True)
    is_available = models.BooleanField(default=True)
    
    # Product Reference
    product_id = models.CharField(max_length=255, blank=True, help_text='External product ID')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'outfit_items'
        ordering = ['item_type', 'created_at']
        indexes = [
            models.Index(fields=['outfit', 'item_type']),
        ]
    
    def __str__(self):
        return f"{self.item_type}: {self.name}"


class OutfitLike(models.Model):
    """
    Track users who liked an outfit.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='outfit_likes')
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'outfit_likes'
        unique_together = ('user', 'outfit')
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['outfit', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} likes {self.outfit.title}"


class OutfitSave(models.Model):
    """
    Track users who saved an outfit.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='outfit_saves')
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE, related_name='saves')
    collection_name = models.CharField(max_length=100, blank=True, help_text='Optional collection name')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'outfit_saves'
        unique_together = ('user', 'outfit')
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['outfit', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} saved {self.outfit.title}"

