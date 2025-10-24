"""
Serializers for outfits app.
"""
from rest_framework import serializers
from .models import Outfit, OutfitItem, OutfitLike, OutfitSave


class OutfitItemSerializer(serializers.ModelSerializer):
    """Serializer for OutfitItem model."""
    
    class Meta:
        model = OutfitItem
        fields = [
            'id', 'item_type', 'name', 'brand', 'image', 'price', 'currency',
            'size', 'color', 'material', 'purchase_url', 'affiliate_link',
            'retailer', 'is_available', 'product_id'
        ]


class OutfitSerializer(serializers.ModelSerializer):
    """Serializer for Outfit model."""
    items = OutfitItemSerializer(many=True, read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    
    class Meta:
        model = Outfit
        fields = [
            'id', 'user', 'user_username', 'title', 'description',
            'main_image', 'thumbnail', 'occasion', 'season', 'style_tags',
            'color_palette', 'ai_generated', 'confidence_score', 'is_public',
            'likes_count', 'saves_count', 'views_count', 'items',
            'is_liked', 'is_saved', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'user', 'likes_count', 'saves_count', 'views_count',
            'ai_generated', 'confidence_score', 'created_at', 'updated_at'
        ]
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return OutfitLike.objects.filter(user=request.user, outfit=obj).exists()
        return False
    
    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return OutfitSave.objects.filter(user=request.user, outfit=obj).exists()
        return False


class OutfitCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating outfits with items."""
    items = OutfitItemSerializer(many=True, required=False)
    
    class Meta:
        model = Outfit
        fields = [
            'title', 'description', 'main_image', 'occasion', 'season',
            'style_tags', 'color_palette', 'is_public', 'items'
        ]
    
    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        outfit = Outfit.objects.create(**validated_data)
        
        # Create outfit items
        for item_data in items_data:
            OutfitItem.objects.create(outfit=outfit, **item_data)
        
        return outfit


class OutfitLikeSerializer(serializers.ModelSerializer):
    """Serializer for outfit likes."""
    
    class Meta:
        model = OutfitLike
        fields = ['id', 'user', 'outfit', 'created_at']
        read_only_fields = ['user', 'created_at']

