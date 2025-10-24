"""
Django admin configuration for outfits app.
"""
from django.contrib import admin
from .models import Outfit, OutfitItem, OutfitLike, OutfitSave


class OutfitItemInline(admin.TabularInline):
    """Inline admin for outfit items."""
    model = OutfitItem
    extra = 1
    fields = ['item_type', 'name', 'brand', 'price', 'purchase_url', 'is_available']


@admin.register(Outfit)
class OutfitAdmin(admin.ModelAdmin):
    """Admin interface for Outfit model."""
    list_display = ['title', 'user', 'occasion', 'season', 'is_public', 'likes_count', 'views_count', 'created_at']
    list_filter = ['occasion', 'season', 'is_public', 'ai_generated', 'created_at']
    search_fields = ['title', 'description', 'user__username', 'user__email']
    readonly_fields = ['likes_count', 'saves_count', 'views_count', 'created_at', 'updated_at']
    raw_id_fields = ['user']
    inlines = [OutfitItemInline]
    date_hierarchy = 'created_at'


@admin.register(OutfitItem)
class OutfitItemAdmin(admin.ModelAdmin):
    """Admin interface for OutfitItem model."""
    list_display = ['name', 'outfit', 'item_type', 'brand', 'price', 'is_available']
    list_filter = ['item_type', 'is_available']
    search_fields = ['name', 'brand', 'outfit__title']
    raw_id_fields = ['outfit']


@admin.register(OutfitLike)
class OutfitLikeAdmin(admin.ModelAdmin):
    """Admin interface for OutfitLike model."""
    list_display = ['user', 'outfit', 'created_at']
    search_fields = ['user__username', 'outfit__title']
    raw_id_fields = ['user', 'outfit']
    date_hierarchy = 'created_at'


@admin.register(OutfitSave)
class OutfitSaveAdmin(admin.ModelAdmin):
    """Admin interface for OutfitSave model."""
    list_display = ['user', 'outfit', 'collection_name', 'created_at']
    list_filter = ['collection_name']
    search_fields = ['user__username', 'outfit__title', 'collection_name']
    raw_id_fields = ['user', 'outfit']
    date_hierarchy = 'created_at'

