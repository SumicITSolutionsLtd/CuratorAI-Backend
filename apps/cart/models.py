"""
Shopping cart models for CuratorAI.
"""
from django.db import models
from django.conf import settings
from decimal import Decimal


class ShoppingCart(models.Model):
    """
    User shopping cart.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shopping_cart')
    promo_code = models.CharField(max_length=50, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'shopping_carts'
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    @property
    def item_count(self):
        return sum(item.quantity for item in self.items.all())
    
    @property
    def subtotal(self):
        return sum(item.price * item.quantity for item in self.items.all())
    
    @property
    def shipping(self):
        # Simple shipping calculation
        if self.subtotal > 100:
            return Decimal('0.00')
        return Decimal('10.00')
    
    @property
    def tax(self):
        # Simple tax calculation (9%)
        return (self.subtotal + self.shipping) * Decimal('0.09')
    
    @property
    def total(self):
        return self.subtotal + self.shipping + self.tax - self.discount


class CartItem(models.Model):
    """
    Item in shopping cart.
    """
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='items')
    outfit_item_id = models.IntegerField(help_text='Reference to OutfitItem')
    
    # Product details (cached for performance)
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=20, blank=True)
    color = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    
    # URLs
    image_url = models.URLField(blank=True)
    product_url = models.URLField(blank=True)
    
    # Availability
    in_stock = models.BooleanField(default=True)
    
    # Timestamps
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cart_items'
        unique_together = ('cart', 'outfit_item_id', 'size')
        ordering = ['added_at']
    
    def __str__(self):
        return f"{self.name} x{self.quantity}"


class PromoCode(models.Model):
    """
    Promotional codes.
    """
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.IntegerField(default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Validity
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    # Usage limits
    max_uses = models.IntegerField(default=0, help_text='0 means unlimited')
    times_used = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'promo_codes'
    
    def __str__(self):
        return self.code
    
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        
        if not self.is_active:
            return False
        if now < self.valid_from or now > self.valid_until:
            return False
        if self.max_uses > 0 and self.times_used >= self.max_uses:
            return False
        
        return True
    
    def calculate_discount(self, subtotal):
        if self.discount_percentage > 0:
            return subtotal * Decimal(self.discount_percentage) / Decimal(100)
        return self.discount_amount

