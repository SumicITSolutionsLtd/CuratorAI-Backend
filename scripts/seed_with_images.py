"""
Script to re-seed database with real image URLs from Unsplash.
This script updates existing data with real fashion images.
For ImageField models, we'll store URLs as strings (models should support URLField or we use a workaround).
"""
import os
import sys
import django
import random
from pathlib import Path
from decimal import Decimal
from datetime import datetime, timedelta

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set up Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'curator.settings.base'
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.accounts.models import UserProfile
from apps.outfits.models import Outfit, OutfitItem
from apps.wardrobe.models import Wardrobe, WardrobeItem
from apps.lookbooks.models import Lookbook
from apps.social.models import Post, PostImage

User = get_user_model()

# Image URLs (using Unsplash Source - no API key needed, direct image URLs)
FASHION_IMAGE_URLS = [
    # Fashion/Outfit images
    'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1521223890158-f9f7f3b5dcce?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1506629905607-0c3c0b0c0c0c?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1521223890158-f9f7f3b5dcce?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1506629905607-0c3c0b0c0c0c?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800&h=800&fit=crop',
    'https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=800&h=800&fit=crop',
]

USER_AVATAR_URLS = [
    'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=400&fit=crop',
]

WARDROBE_ITEM_IMAGES = {
    'top': [
        'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=600&h=600&fit=crop',
        'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=600&h=600&fit=crop',
        'https://images.unsplash.com/photo-1594633313593-bab3825d0caf?w=600&h=600&fit=crop',
    ],
    'bottom': [
        'https://images.unsplash.com/photo-1542272604-787c3835535d?w=600&h=600&fit=crop',
        'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=600&h=600&fit=crop',
    ],
    'shoes': [
        'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=600&h=600&fit=crop',
        'https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=600&h=600&fit=crop',
    ],
    'dress': [
        'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=600&h=600&fit=crop',
        'https://images.unsplash.com/photo-1594633313593-bab3825d0caf?w=600&h=600&fit=crop',
    ],
    'outerwear': [
        'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600&h=600&fit=crop',
        'https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?w=600&h=600&fit=crop',
    ],
    'accessory': [
        'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&h=600&fit=crop',
        'https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=600&h=600&fit=crop',
    ],
    'bag': [
        'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&h=600&fit=crop',
        'https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=600&h=600&fit=crop',
    ],
}


def get_random_image_url(category='fashion'):
    """Get a random image URL."""
    if category == 'user':
        return random.choice(USER_AVATAR_URLS)
    elif category in WARDROBE_ITEM_IMAGES:
        return random.choice(WARDROBE_ITEM_IMAGES[category])
    else:
        return random.choice(FASHION_IMAGE_URLS)


def update_user_avatars():
    """Update all users with avatar images - prioritize image_url over ImageField."""
    print("\n👤 Updating user avatars...")
    users = User.objects.all()
    updated = 0
    for user in users:
        # Always update image_url if it's empty (even if ImageField exists)
        # This ensures image_url takes priority in serializers
        if not user.avatar_url:
            img_url = get_random_image_url('user')
            user.avatar_url = img_url
            user.save(update_fields=['avatar_url'])
            updated += 1
    print(f"✅ Updated {updated} user avatars with image URLs")


def update_outfit_images():
    """Update all outfits with main images - prioritize image_url over ImageField."""
    print("\n👗 Updating outfit images...")
    outfits = Outfit.objects.all()
    updated = 0
    for outfit in outfits:
        # Always update main_image_url if it's empty (even if ImageField exists)
        if not outfit.main_image_url:
            img_url = get_random_image_url('fashion')
            outfit.main_image_url = img_url
            outfit.save(update_fields=['main_image_url'])
            updated += 1
    print(f"✅ Updated {updated} outfit images with URLs")


def update_wardrobe_item_images():
    """Update all wardrobe items with images."""
    print("\n👜 Updating wardrobe item images...")
    items = WardrobeItem.objects.all()
    updated = 0
    for item in items:
        if not item.primary_image_url:
            # Map wardrobe category to image category
            category_map = {
                'top': 'top',
                'bottom': 'bottom',
                'shoes': 'shoes',
                'dress': 'dress',
                'outerwear': 'outerwear',
                'accessory': 'accessory',
                'bag': 'bag',
            }
            img_category = category_map.get(item.category, 'fashion')
            img_url = get_random_image_url(img_category)
            item.primary_image_url = img_url
            item.save(update_fields=['primary_image_url'])
            updated += 1
    print(f"✅ Updated {updated} wardrobe item images")


def update_lookbook_images():
    """Update all lookbooks with cover images - prioritize image_url over ImageField."""
    print("\n📚 Updating lookbook images...")
    lookbooks = Lookbook.objects.all()
    updated = 0
    for lookbook in lookbooks:
        # Always update cover_image_url if it's empty (even if ImageField exists)
        if not lookbook.cover_image_url:
            img_url = get_random_image_url('fashion')
            lookbook.cover_image_url = img_url
            lookbook.save(update_fields=['cover_image_url'])
            updated += 1
    print(f"✅ Updated {updated} lookbook images with URLs")


def update_post_images():
    """Update all social posts with images."""
    print("\n📸 Updating post images...")
    posts = Post.objects.all()
    updated_posts = 0
    updated_images = 0
    
    for post in posts:
        # Check if post has images
        post_images = post.images.all()
        
        if not post_images.exists():
            # Add 1-3 images per post
            num_images = random.randint(1, 3)
            for i in range(num_images):
                img_url = get_random_image_url('fashion')
                PostImage.objects.create(
                    post=post,
                    image_url=img_url,
                    order=i
                )
            updated_posts += 1
        else:
            # Update existing images that don't have image_url
            for post_image in post_images:
                if not post_image.image_url:
                    img_url = get_random_image_url('fashion')
                    post_image.image_url = img_url
                    post_image.save(update_fields=['image_url'])
                    updated_images += 1
    
    print(f"✅ Updated {updated_posts} posts with new images")
    print(f"✅ Updated {updated_images} existing post images with URLs")


def check_and_seed_data():
    """Check if data exists, if not, seed basic data first."""
    print("\n🔍 Checking existing data...")
    
    user_count = User.objects.count()
    outfit_count = Outfit.objects.count()
    wardrobe_count = WardrobeItem.objects.count()
    lookbook_count = Lookbook.objects.count()
    post_count = Post.objects.count()
    
    print(f"  Users: {user_count}")
    print(f"  Outfits: {outfit_count}")
    print(f"  Wardrobe Items: {wardrobe_count}")
    print(f"  Lookbooks: {lookbook_count}")
    print(f"  Posts: {post_count}")
    
    # If no data exists, seed basic data first
    if user_count == 0 or outfit_count == 0:
        print("\n⚠️  No data found. Seeding basic data first...")
        from django.core.management import execute_from_command_line
        try:
            # Seed users and outfits
            if user_count == 0:
                execute_from_command_line(['manage.py', 'seed_data', '--users', '20', '--outfits', '50'])
            else:
                execute_from_command_line(['manage.py', 'seed_data', '--outfits', '50'])
            
            # Seed wardrobe if needed
            if wardrobe_count == 0:
                execute_from_command_line(['manage.py', 'seed_data', '--wardrobe-items', '100'])
            
            # Seed lookbooks if needed
            if lookbook_count == 0:
                execute_from_command_line(['manage.py', 'seed_data', '--lookbooks', '20'])
            
            # Seed posts if needed
            if post_count == 0:
                execute_from_command_line(['manage.py', 'seed_data', '--posts', '50'])
            
            print("✅ Basic data seeded successfully!")
        except Exception as e:
            print(f"⚠️  Warning: Could not seed data automatically: {e}")
            print("   Please run 'python manage.py seed_data' manually first.")


def main():
    """Main function to update all data with images."""
    print("=" * 60)
    print("🖼️  Seeding Database with Real Image URLs")
    print("=" * 60)
    
    try:
        # Check and seed data if needed
        check_and_seed_data()
        
        # Update all images
        update_user_avatars()
        update_outfit_images()
        update_wardrobe_item_images()
        update_lookbook_images()
        update_post_images()
        
        print("\n" + "=" * 60)
        print("✅ All images updated successfully!")
        print("=" * 60)
        return True
    except Exception as e:
        print(f"\n❌ Error updating images: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

