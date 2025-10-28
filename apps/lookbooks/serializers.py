"""
Serializers for lookbooks app.
"""
from rest_framework import serializers
from apps.accounts.models import User
from apps.outfits.serializers import OutfitSerializer
from .models import Lookbook, LookbookOutfit, LookbookLike


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user serializer."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', 'is_verified']


class LookbookOutfitSerializer(serializers.ModelSerializer):
    """Serializer for lookbook outfits."""
    outfit = OutfitSerializer(read_only=True)
    
    class Meta:
        model = LookbookOutfit
        fields = ['id', 'outfit', 'order', 'notes', 'created_at']


class LookbookSerializer(serializers.ModelSerializer):
    """Serializer for lookbooks."""
    creator = UserBasicSerializer(read_only=True)
    outfits = LookbookOutfitSerializer(many=True, read_only=True)
    outfits_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    price_range = serializers.SerializerMethodField()
    total_value = serializers.SerializerMethodField()
    
    class Meta:
        model = Lookbook
        fields = [
            'id', 'creator', 'title', 'description', 'cover_image',
            'season', 'occasion', 'style', 'tags', 'outfits', 'outfits_count',
            'price_range', 'total_value', 'likes_count', 'views_count',
            'comments_count', 'is_public', 'is_featured', 'is_liked',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'likes_count', 'views_count', 'comments_count', 'created_at', 'updated_at']
    
    def get_outfits_count(self, obj):
        return obj.outfits.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return LookbookLike.objects.filter(user=request.user, lookbook=obj).exists()
        return False
    
    def get_price_range(self, obj):
        # Calculate price range from outfits
        outfits = obj.outfits.all()
        if not outfits:
            return None
        
        prices = [outfit.outfit.total_price for outfit in outfits if outfit.outfit.total_price]
        if not prices:
            return None
        
        return {
            'min': float(min(prices)),
            'max': float(max(prices)),
            'currency': 'USD'
        }
    
    def get_total_value(self, obj):
        outfits = obj.outfits.all()
        total = sum(outfit.outfit.total_price for outfit in outfits if outfit.outfit.total_price)
        return float(total) if total else 0


class LookbookCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating lookbooks."""
    outfit_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    
    class Meta:
        model = Lookbook
        fields = ['title', 'description', 'cover_image', 'season', 'occasion', 'style', 'tags', 'is_public', 'outfit_ids']
    
    def create(self, validated_data):
        outfit_ids = validated_data.pop('outfit_ids', [])
        lookbook = Lookbook.objects.create(**validated_data)
        
        # Add outfits to lookbook
        for idx, outfit_id in enumerate(outfit_ids):
            LookbookOutfit.objects.create(lookbook=lookbook, outfit_id=outfit_id, order=idx)
        
        return lookbook

