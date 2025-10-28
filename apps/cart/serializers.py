"""
Serializers for cart app.
"""
from rest_framework import serializers
from .models import ShoppingCart, CartItem, PromoCode


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for cart items."""
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'outfit_item_id', 'name', 'brand', 'price', 
            'size', 'color', 'quantity', 'image_url', 'product_url', 
            'in_stock', 'added_at'
        ]
        read_only_fields = ['id', 'added_at']


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Serializer for shopping cart."""
    items = CartItemSerializer(many=True, read_only=True)
    item_count = serializers.IntegerField(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    shipping = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    tax = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = ShoppingCart
        fields = [
            'id', 'user_id', 'items', 'item_count', 'subtotal', 
            'shipping', 'tax', 'discount', 'total', 'promo_code', 'updated_at'
        ]
        read_only_fields = ['id', 'user_id', 'updated_at']


class AddToCartSerializer(serializers.Serializer):
    """Serializer for adding items to cart."""
    outfit_item_id = serializers.IntegerField(required=True)
    name = serializers.CharField(max_length=200, required=True)
    brand = serializers.CharField(max_length=100, required=False, allow_blank=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    size = serializers.CharField(max_length=20, required=False, allow_blank=True)
    color = serializers.CharField(max_length=50, required=True)
    quantity = serializers.IntegerField(default=1, min_value=1, max_value=10)
    image_url = serializers.URLField(required=False, allow_blank=True)
    product_url = serializers.URLField(required=False, allow_blank=True)
    in_stock = serializers.BooleanField(default=True)

