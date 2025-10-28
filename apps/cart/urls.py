"""
URL patterns for cart app.
"""
from django.urls import path
from .views import (
    GetCartView,
    AddToCartView,
    UpdateCartItemView,
    RemoveFromCartView,
    ApplyPromoCodeView,
    RemovePromoCodeView,
    ClearCartView,
    CalculateShippingView,
)

app_name = 'cart'

urlpatterns = [
    # Cart
    path('<int:user_id>/', GetCartView.as_view(), name='get-cart'),
    path('<int:user_id>/items/', AddToCartView.as_view(), name='add-to-cart'),
    path('<int:user_id>/items/<int:item_id>/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('<int:user_id>/items/<int:item_id>/remove/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('<int:user_id>/clear/', ClearCartView.as_view(), name='clear-cart'),
    
    # Promo Codes
    path('<int:user_id>/promo/', ApplyPromoCodeView.as_view(), name='apply-promo'),
    path('<int:user_id>/promo/remove/', RemovePromoCodeView.as_view(), name='remove-promo'),
    
    # Shipping
    path('shipping/calculate/', CalculateShippingView.as_view(), name='calculate-shipping'),
]

