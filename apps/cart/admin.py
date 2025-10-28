from django.contrib import admin
from .models import ShoppingCart, CartItem, PromoCode

admin.site.register(ShoppingCart)
admin.site.register(CartItem)
admin.site.register(PromoCode)

