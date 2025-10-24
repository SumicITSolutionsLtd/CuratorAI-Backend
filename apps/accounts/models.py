"""
User and Profile models for CuratorAI.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    """
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    is_verified = models.BooleanField(default=False)
    
    # OAuth fields
    oauth_provider = models.CharField(max_length=50, blank=True, null=True)
    oauth_id = models.CharField(max_length=255, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """
    Extended user profile information.
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    
    BODY_TYPE_CHOICES = [
        ('slim', 'Slim'),
        ('athletic', 'Athletic'),
        ('average', 'Average'),
        ('curvy', 'Curvy'),
        ('plus', 'Plus Size'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal Information
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    
    # Location
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Body Measurements
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES, blank=True)
    height = models.IntegerField(null=True, blank=True, help_text='Height in cm')
    weight = models.IntegerField(null=True, blank=True, help_text='Weight in kg')
    
    # Size preferences
    top_size = models.CharField(max_length=10, blank=True)
    bottom_size = models.CharField(max_length=10, blank=True)
    shoe_size = models.CharField(max_length=10, blank=True)
    dress_size = models.CharField(max_length=10, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"{self.user.email}'s Profile"


class StylePreference(models.Model):
    """
    User style preferences for personalized recommendations.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='style_preference')
    
    # Style preferences
    preferred_styles = models.JSONField(default=list, help_text='List of preferred fashion styles')
    preferred_colors = models.JSONField(default=list, help_text='List of preferred colors')
    preferred_brands = models.JSONField(default=list, help_text='List of preferred brands')
    preferred_patterns = models.JSONField(default=list, help_text='List of preferred patterns')
    
    # Budget
    budget_min = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    currency = models.CharField(max_length=3, default='USD')
    
    # Occasion preferences
    occasions = models.JSONField(default=list, help_text='Preferred occasions (work, casual, formal, party)')
    
    # Sustainability preferences
    prefer_sustainable = models.BooleanField(default=False)
    prefer_secondhand = models.BooleanField(default=False)
    
    # Fit preferences
    fit_preference = models.CharField(max_length=50, blank=True, help_text='Preferred fit (loose, regular, tight)')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'style_preferences'
    
    def __str__(self):
        return f"{self.user.email}'s Style Preferences"


class UserFollowing(models.Model):
    """
    Model to track user following relationships.
    """
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_following'
        unique_together = ('follower', 'following')
        indexes = [
            models.Index(fields=['follower', '-created_at']),
            models.Index(fields=['following', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

