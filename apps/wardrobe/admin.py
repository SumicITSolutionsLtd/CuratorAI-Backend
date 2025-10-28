from django.contrib import admin
from .models import Wardrobe, WardrobeItem, WardrobeItemImage, WardrobeItemAttribute, WardrobeItemWearLog

admin.site.register(Wardrobe)
admin.site.register(WardrobeItem)
admin.site.register(WardrobeItemImage)
admin.site.register(WardrobeItemAttribute)
admin.site.register(WardrobeItemWearLog)

