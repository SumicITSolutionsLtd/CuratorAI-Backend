"""
Django admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, StylePreference, UserFollowing


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_verified', 'is_staff', 'created_at']
    list_filter = ['is_staff', 'is_superuser', 'is_verified', 'created_at']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('avatar', 'bio', 'oauth_provider', 'oauth_id', 'is_verified')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile model."""
    list_display = ['user', 'gender', 'country', 'city', 'body_type', 'created_at']
    list_filter = ['gender', 'body_type', 'country']
    search_fields = ['user__email', 'user__username']
    raw_id_fields = ['user']


@admin.register(StylePreference)
class StylePreferenceAdmin(admin.ModelAdmin):
    """Admin interface for StylePreference model."""
    list_display = ['user', 'budget_min', 'budget_max', 'currency', 'prefer_sustainable', 'created_at']
    list_filter = ['currency', 'prefer_sustainable', 'prefer_secondhand']
    search_fields = ['user__email', 'user__username']
    raw_id_fields = ['user']


@admin.register(UserFollowing)
class UserFollowingAdmin(admin.ModelAdmin):
    """Admin interface for UserFollowing model."""
    list_display = ['follower', 'following', 'created_at']
    search_fields = ['follower__username', 'following__username']
    raw_id_fields = ['follower', 'following']
    date_hierarchy = 'created_at'

