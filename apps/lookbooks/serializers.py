"""
Serializers for lookbooks app.
"""
from rest_framework import serializers
from apps.accounts.models import User
from apps.outfits.serializers import OutfitSerializer
from .models import Lookbook, LookbookOutfit, LookbookLike


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user serializer."""
    avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', 'is_verified']
    
    def get_avatar(self, obj):
        """Return avatar URL from avatar_url field or ImageField as fallback."""
        # Prioritize avatar_url field (external URL) over ImageField
        if obj.avatar_url:
            return obj.avatar_url
        # Fallback to ImageField if avatar_url is not set
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None


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
    cover_image = serializers.SerializerMethodField()
    
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
    
    def get_cover_image(self, obj):
        """Return image URL from cover_image_url field or ImageField as fallback."""
        # Prioritize cover_image_url field (external URL) over ImageField - ALWAYS
        if obj.cover_image_url and obj.cover_image_url.strip():
            return obj.cover_image_url
        # Fallback to ImageField if cover_image_url is not set or empty
        if obj.cover_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None
    
    def get_outfits_count(self, obj):
        return obj.outfits.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return LookbookLike.objects.filter(user=request.user, lookbook=obj).exists()
        return False
    
    def get_price_range(self, obj):
        # Calculate price range from outfits
        try:
            outfits = obj.outfits.all()
            if not outfits:
                return None
            
            prices = []
            for outfit_rel in outfits:
                if hasattr(outfit_rel, 'outfit') and outfit_rel.outfit:
                    outfit = outfit_rel.outfit
                    if hasattr(outfit, 'total_price') and outfit.total_price:
                        prices.append(outfit.total_price)
            
            if not prices:
                return None
            
            return {
                'min': float(min(prices)),
                'max': float(max(prices)),
                'currency': 'USD'
            }
        except Exception:
            return None
    
    def get_total_value(self, obj):
        try:
            outfits = obj.outfits.all()
            total = 0
            for outfit_rel in outfits:
                if hasattr(outfit_rel, 'outfit') and outfit_rel.outfit:
                    outfit = outfit_rel.outfit
                    if hasattr(outfit, 'total_price') and outfit.total_price:
                        total += outfit.total_price
            return float(total) if total else 0
        except Exception:
            return 0


class LookbookCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating lookbooks."""
    outfit_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False, default=list)
    cover_image_url = serializers.URLField(required=False, allow_blank=True)
    
    class Meta:
        model = Lookbook
        fields = ['title', 'description', 'cover_image', 'cover_image_url', 'season', 'occasion', 'style', 'tags', 'is_public', 'outfit_ids']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'cover_image': {'required': False},
            'season': {'required': False},
            'occasion': {'required': False},
            'style': {'required': False},
            'tags': {'required': False},
            'is_public': {'required': False},
        }
    
    def validate(self, data):
        """Set defaults for optional fields."""
        if 'season' not in data or not data.get('season'):
            data['season'] = 'all'
        if 'occasion' not in data or not data.get('occasion'):
            data['occasion'] = 'casual'
        if 'style' not in data or not data.get('style'):
            data['style'] = []
        if 'tags' not in data or not data.get('tags'):
            data['tags'] = []
        if 'is_public' not in data:
            data['is_public'] = True
        return data
    
    def create(self, validated_data):
        outfit_ids = validated_data.pop('outfit_ids', [])
        lookbook = Lookbook.objects.create(**validated_data)
        
        # Add outfits to lookbook
        for idx, outfit_id in enumerate(outfit_ids):
            LookbookOutfit.objects.create(lookbook=lookbook, outfit_id=outfit_id, order=idx)
        
        return lookbook

