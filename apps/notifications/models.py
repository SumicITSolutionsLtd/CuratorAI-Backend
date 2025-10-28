"""
Notification models for CuratorAI.
"""
from django.db import models
from django.conf import settings


class Notification(models.Model):
    """
    User notification model.
    """
    TYPE_CHOICES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('recommendation', 'Recommendation'),
        ('sale', 'Sale'),
        ('system', 'System'),
        ('promo', 'Promo'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Optional fields
    image_url = models.URLField(blank=True)
    action_url = models.CharField(max_length=500, blank=True)
    
    # Actor (who triggered the notification)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='triggered_notifications'
    )
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['type']),
        ]
    
    def __str__(self):
        return f"{self.type} notification for {self.user.username}"


class NotificationPreference(models.Model):
    """
    User notification preferences.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Email Notifications
    email_likes = models.BooleanField(default=True)
    email_comments = models.BooleanField(default=True)
    email_follows = models.BooleanField(default=True)
    email_recommendations = models.BooleanField(default=False)
    email_marketing = models.BooleanField(default=False)
    email_digest = models.CharField(
        max_length=20,
        choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('never', 'Never')],
        default='weekly'
    )
    
    # Push Notifications
    push_likes = models.BooleanField(default=True)
    push_comments = models.BooleanField(default=True)
    push_follows = models.BooleanField(default=True)
    push_recommendations = models.BooleanField(default=True)
    push_marketing = models.BooleanField(default=False)
    
    # In-App Notifications
    inapp_likes = models.BooleanField(default=True)
    inapp_comments = models.BooleanField(default=True)
    inapp_follows = models.BooleanField(default=True)
    inapp_recommendations = models.BooleanField(default=True)
    inapp_system = models.BooleanField(default=True)
    
    # Do Not Disturb
    dnd_enabled = models.BooleanField(default=False)
    dnd_start_time = models.TimeField(null=True, blank=True)
    dnd_end_time = models.TimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_preferences'
    
    def __str__(self):
        return f"Notification preferences for {self.user.username}"

