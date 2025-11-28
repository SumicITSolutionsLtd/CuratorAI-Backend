"""
Serializers for wardrobe app.
"""
from rest_framework import serializers
from .models import Wardrobe, WardrobeItem, WardrobeItemImage, WardrobeItemAttribute, WardrobeItemWearLog


class WardrobeItemAttributeSerializer(serializers.ModelSerializer):
    """Serializer for wardrobe item attributes."""
    
    class Meta:
        model = WardrobeItemAttribute
        fields = ['key', 'value']


class WardrobeItemImageSerializer(serializers.ModelSerializer):
    """Serializer for wardrobe item images."""
    
    class Meta:
        model = WardrobeItemImage
        fields = ['id', 'image', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']


class WardrobeItemSerializer(serializers.ModelSerializer):
    """Serializer for wardrobe items."""
    images = WardrobeItemImageSerializer(many=True, read_only=True)
    attributes = WardrobeItemAttributeSerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = WardrobeItem
        fields = [
            'id', 'category', 'name', 'brand', 'color', 'size', 
            'price', 'currency', 'primary_image', 'season', 'tags', 
            'notes', 'purchase_link', 'purchase_date', 'times_worn', 
            'last_worn_date', 'images', 'attributes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'times_worn', 'last_worn_date', 'created_at', 'updated_at']
    
    def get_primary_image(self, obj):
        """Return image URL from primary_image_url field or ImageField as fallback."""
        # Prioritize primary_image_url field (external URL) over ImageField - ALWAYS
        if obj.primary_image_url and obj.primary_image_url.strip():
            return obj.primary_image_url
        # Fallback to ImageField if primary_image_url is not set
        if obj.primary_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.primary_image.url)
            return obj.primary_image.url
        return None


class WardrobeItemCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating wardrobe items."""
    attributes = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True,
        default=list
    )
    primary_image_url = serializers.URLField(required=False, allow_blank=True)
    
    class Meta:
        model = WardrobeItem
        fields = [
            'category', 'name', 'brand', 'color', 'size', 
            'price', 'currency', 'primary_image', 'primary_image_url', 'season', 'tags', 
            'notes', 'purchase_link', 'purchase_date', 'attributes'
        ]
        extra_kwargs = {
            'category': {'required': True},
            'name': {'required': True},
            'brand': {'required': False, 'allow_blank': True},
            'color': {'required': True},
            'size': {'required': False, 'allow_blank': True},
            'price': {'required': False},
            'currency': {'required': False},
            'primary_image': {'required': False},
            'season': {'required': False},
            'tags': {'required': False},
            'notes': {'required': False, 'allow_blank': True},
            'purchase_link': {'required': False, 'allow_blank': True},
            'purchase_date': {'required': False},
        }
    
    def validate(self, data):
        """Set defaults for optional fields."""
        if 'season' not in data or not data.get('season'):
            data['season'] = 'all'
        if 'tags' not in data or not data.get('tags'):
            data['tags'] = []
        if 'currency' not in data or not data.get('currency'):
            data['currency'] = 'USD'
        return data
    
    def create(self, validated_data):
        attributes_data = validated_data.pop('attributes', [])
        item = WardrobeItem.objects.create(**validated_data)
        
        # Create attributes
        for attr_data in attributes_data:
            WardrobeItemAttribute.objects.create(
                item=item,
                key=attr_data.get('key'),
                value=attr_data.get('value')
            )
        
        return item


class WardrobeSerializer(serializers.ModelSerializer):
    """Serializer for wardrobe."""
    total_items = serializers.IntegerField(read_only=True)
    categories = serializers.SerializerMethodField()
    
    class Meta:
        model = Wardrobe
        fields = ['id', 'user_id', 'total_items', 'categories', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user_id', 'created_at', 'updated_at']
    
    def get_categories(self, obj):
        """Get count of items by category."""
        items = obj.items.filter(is_deleted=False)
        categories = {}
        
        for category_code, category_name in WardrobeItem.CATEGORY_CHOICES:
            count = items.filter(category=category_code).count()
            if count > 0:
                categories[category_code] = count
        
        return categories


class WardrobeItemWearLogSerializer(serializers.ModelSerializer):
    """Serializer for wear logs."""
    
    class Meta:
        model = WardrobeItemWearLog
        fields = ['id', 'worn_date', 'outfit_id', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']

