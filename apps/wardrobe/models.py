"""
Wardrobe models for CuratorAI.
"""
from django.db import models
from django.conf import settings


class Wardrobe(models.Model):
    """
    Main wardrobe model - one per user.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wardrobe')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'wardrobes'
    
    def __str__(self):
        return f"{self.user.username}'s Wardrobe"
    
    @property
    def total_items(self):
        return self.items.count()


class WardrobeItem(models.Model):
    """
    Individual clothing item in a user's wardrobe.
    """
    CATEGORY_CHOICES = [
        ('top', 'Top'),
        ('bottom', 'Bottom'),
        ('shoes', 'Shoes'),
        ('accessory', 'Accessory'),
        ('outerwear', 'Outerwear'),
        ('dress', 'Dress'),
        ('bag', 'Bag'),
    ]
    
    SEASON_CHOICES = [
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('fall', 'Fall'),
        ('winter', 'Winter'),
        ('all', 'All Season'),
    ]
    
    wardrobe = models.ForeignKey(Wardrobe, on_delete=models.CASCADE, related_name='items')
    
    # Basic Information
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=20, blank=True)
    
    # Price Information
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    
    # Images
    primary_image = models.ImageField(upload_to='wardrobe/items/', null=True, blank=True)
    primary_image_url = models.URLField(blank=True, help_text='External image URL (used when primary_image is not available)')
    
    # Additional Details
    season = models.CharField(max_length=20, choices=SEASON_CHOICES, default='all')
    tags = models.JSONField(default=list, help_text='List of tags for categorization')
    notes = models.TextField(blank=True)
    
    # Purchase Information
    purchase_link = models.URLField(blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    
    # Usage Tracking
    times_worn = models.IntegerField(default=0)
    last_worn_date = models.DateField(null=True, blank=True)
    
    # Soft Delete
    is_deleted = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'wardrobe_items'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['wardrobe', 'category']),
            models.Index(fields=['wardrobe', '-created_at']),
            models.Index(fields=['is_deleted']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.category})"


class WardrobeItemImage(models.Model):
    """
    Additional images for wardrobe items.
    """
    item = models.ForeignKey(WardrobeItem, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='wardrobe/items/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'wardrobe_item_images'
        ordering = ['-is_primary', '-created_at']
    
    def __str__(self):
        return f"Image for {self.item.name}"


class WardrobeItemAttribute(models.Model):
    """
    Custom attributes for wardrobe items (e.g., Material: Cotton).
    """
    item = models.ForeignKey(WardrobeItem, on_delete=models.CASCADE, related_name='attributes')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'wardrobe_item_attributes'
        unique_together = ('item', 'key')
    
    def __str__(self):
        return f"{self.key}: {self.value}"


class WardrobeItemWearLog(models.Model):
    """
    Track when items are worn.
    """
    item = models.ForeignKey(WardrobeItem, on_delete=models.CASCADE, related_name='wear_logs')
    worn_date = models.DateField()
    outfit_id = models.IntegerField(null=True, blank=True, help_text='Optional reference to outfit')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'wardrobe_item_wear_logs'
        ordering = ['-worn_date']
        indexes = [
            models.Index(fields=['item', '-worn_date']),
        ]
    
    def __str__(self):
        return f"{self.item.name} worn on {self.worn_date}"

