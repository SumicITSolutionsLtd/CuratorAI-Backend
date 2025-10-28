"""
Views for cart app.
"""
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from .models import ShoppingCart, CartItem, PromoCode
from .serializers import ShoppingCartSerializer, CartItemSerializer, AddToCartSerializer


class GetCartView(generics.RetrieveAPIView):
    """
    Get user's shopping cart.
    """
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get cart",
        description="Retrieve user's shopping cart with all items",
        tags=["Shopping Cart"]
    )
    def get_object(self):
        user_id = self.kwargs.get('user_id')
        
        # Ensure user can only access their own cart
        if self.request.user.id != user_id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('You can only access your own cart')
        
        cart, _ = ShoppingCart.objects.get_or_create(user=self.request.user)
        return cart


class AddToCartView(views.APIView):
    """
    Add item to cart.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Add to cart",
        description="Add an item to the shopping cart",
        tags=["Shopping Cart"],
        request=AddToCartSerializer
    )
    def post(self, request, user_id):
        # Ensure user can only add to their own cart
        if request.user.id != user_id:
            return Response({
                'success': False,
                'message': 'Unauthorized'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        cart, _ = ShoppingCart.objects.get_or_create(user=request.user)
        
        # Check if item already exists in cart
        outfit_item_id = serializer.validated_data['outfit_item_id']
        size = serializer.validated_data.get('size', '')
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            outfit_item_id=outfit_item_id,
            size=size,
            defaults=serializer.validated_data
        )
        
        if not created:
            # Update quantity if item exists
            cart_item.quantity += serializer.validated_data.get('quantity', 1)
            cart_item.save()
        
        cart.save()  # Update timestamp
        
        response_serializer = ShoppingCartSerializer(cart)
        return Response({
            'success': True,
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)


class UpdateCartItemView(views.APIView):
    """
    Update cart item quantity.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Update cart item",
        description="Update quantity of a cart item",
        tags=["Shopping Cart"]
    )
    def patch(self, request, user_id, item_id):
        # Ensure user can only update their own cart
        if request.user.id != user_id:
            return Response({
                'success': False,
                'message': 'Unauthorized'
            }, status=status.HTTP_403_FORBIDDEN)
        
        cart = get_object_or_404(ShoppingCart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        quantity = request.data.get('quantity')
        if quantity is None or quantity < 1:
            return Response({
                'success': False,
                'message': 'Invalid quantity'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item.quantity = quantity
        cart_item.save()
        cart.save()  # Update timestamp
        
        response_serializer = ShoppingCartSerializer(cart)
        return Response({
            'success': True,
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)


class RemoveFromCartView(views.APIView):
    """
    Remove item from cart.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Remove from cart",
        description="Remove an item from the shopping cart",
        tags=["Shopping Cart"]
    )
    def delete(self, request, user_id, item_id):
        # Ensure user can only remove from their own cart
        if request.user.id != user_id:
            return Response({
                'success': False,
                'message': 'Unauthorized'
            }, status=status.HTTP_403_FORBIDDEN)
        
        cart = get_object_or_404(ShoppingCart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        cart_item.delete()
        cart.save()  # Update timestamp
        
        response_serializer = ShoppingCartSerializer(cart)
        return Response({
            'success': True,
            'message': 'Item removed from cart',
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)


class ApplyPromoCodeView(views.APIView):
    """
    Apply promo code to cart.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Apply promo code",
        description="Apply a promotional code to the cart",
        tags=["Shopping Cart"]
    )
    def post(self, request, user_id):
        # Ensure user can only apply to their own cart
        if request.user.id != user_id:
            return Response({
                'success': False,
                'message': 'Unauthorized'
            }, status=status.HTTP_403_FORBIDDEN)
        
        code = request.data.get('code')
        if not code:
            return Response({
                'success': False,
                'message': 'Promo code is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        cart = get_object_or_404(ShoppingCart, user=request.user)
        
        try:
            promo = PromoCode.objects.get(code=code.upper())
        except PromoCode.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Invalid promo code'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not promo.is_valid():
            return Response({
                'success': False,
                'message': 'Promo code is expired or invalid'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if cart.subtotal < promo.min_purchase_amount:
            return Response({
                'success': False,
                'message': f'Minimum purchase amount is {promo.min_purchase_amount}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Apply discount
        discount = promo.calculate_discount(cart.subtotal)
        cart.promo_code = code.upper()
        cart.discount = discount
        cart.save()
        
        response_serializer = ShoppingCartSerializer(cart)
        return Response({
            'success': True,
            'message': 'Promo code applied successfully',
            'promo_code': cart.promo_code,
            'discount': float(cart.discount),
            'discount_percentage': promo.discount_percentage,
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)


class RemovePromoCodeView(views.APIView):
    """
    Remove promo code from cart.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Remove promo code",
        description="Remove promotional code from cart",
        tags=["Shopping Cart"]
    )
    def delete(self, request, user_id):
        # Ensure user can only remove from their own cart
        if request.user.id != user_id:
            return Response({
                'success': False,
                'message': 'Unauthorized'
            }, status=status.HTTP_403_FORBIDDEN)
        
        cart = get_object_or_404(ShoppingCart, user=request.user)
        cart.promo_code = ''
        cart.discount = 0
        cart.save()
        
        response_serializer = ShoppingCartSerializer(cart)
        return Response({
            'success': True,
            'message': 'Promo code removed',
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)


class ClearCartView(views.APIView):
    """
    Clear all items from cart.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Clear cart",
        description="Remove all items from the shopping cart",
        tags=["Shopping Cart"]
    )
    def delete(self, request, user_id):
        # Ensure user can only clear their own cart
        if request.user.id != user_id:
            return Response({
                'success': False,
                'message': 'Unauthorized'
            }, status=status.HTTP_403_FORBIDDEN)
        
        cart = get_object_or_404(ShoppingCart, user=request.user)
        cart.items.all().delete()
        cart.promo_code = ''
        cart.discount = 0
        cart.save()
        
        return Response({
            'success': True,
            'message': 'Cart cleared successfully'
        }, status=status.HTTP_204_NO_CONTENT)


class CalculateShippingView(views.APIView):
    """
    Calculate shipping cost.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Calculate shipping",
        description="Calculate shipping costs for cart items",
        tags=["Shopping Cart"]
    )
    def post(self, request):
        # For now, return simple shipping methods
        # In production, integrate with shipping API
        
        shipping_methods = [
            {
                'id': 'standard',
                'name': 'Standard Shipping',
                'price': 10.00,
                'currency': 'USD',
                'estimated_days': '5-7'
            },
            {
                'id': 'express',
                'name': 'Express Shipping',
                'price': 25.00,
                'currency': 'USD',
                'estimated_days': '2-3'
            },
            {
                'id': 'overnight',
                'name': 'Overnight Shipping',
                'price': 40.00,
                'currency': 'USD',
                'estimated_days': '1'
            }
        ]
        
        return Response({
            'shipping_methods': shipping_methods,
            'recommended': 'standard'
        }, status=status.HTTP_200_OK)

