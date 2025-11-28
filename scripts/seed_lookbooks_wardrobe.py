"""
Standalone script to seed lookbooks and wardrobe data.
This script can be run directly without Django management command discovery.
"""
import os
import sys
import django
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set up Django - use base settings (will use DATABASE_URL if set)
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'curator.settings.base').strip()
if not settings_module or settings_module == '':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'curator.settings.base'
else:
    os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

django.setup()

import random
from decimal import Decimal
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.accounts.models import UserProfile
from apps.outfits.models import Outfit
from apps.lookbooks.models import Lookbook, LookbookOutfit, LookbookLike
from apps.wardrobe.models import Wardrobe, WardrobeItem

User = get_user_model()


def seed_lookbooks(users, outfits, count=15):
    """Create sample lookbooks with outfits."""
    lookbooks = []
    
    lookbook_templates = [
        {
            'title': 'Summer Essentials',
            'description': 'A curated collection of perfect summer outfits for every occasion.',
            'season': 'summer',
            'occasion': 'casual',
            'style': ['minimalist', 'fresh', 'light'],
            'tags': ['summer', 'casual', 'essentials']
        },
        {
            'title': 'Work Week Wardrobe',
            'description': 'Professional outfits to get you through the work week in style.',
            'season': 'all',
            'occasion': 'work',
            'style': ['professional', 'sophisticated', 'modern'],
            'tags': ['work', 'professional', 'office']
        },
        {
            'title': 'Weekend Vibes',
            'description': 'Relaxed and comfortable outfits for your weekend adventures.',
            'season': 'spring',
            'occasion': 'casual',
            'style': ['casual', 'comfortable', 'relaxed'],
            'tags': ['weekend', 'casual', 'comfort']
        },
        {
            'title': 'Evening Elegance',
            'description': 'Stunning evening looks for special occasions and formal events.',
            'season': 'winter',
            'occasion': 'formal',
            'style': ['elegant', 'sophisticated', 'glamorous'],
            'tags': ['evening', 'formal', 'elegant']
        },
        {
            'title': 'Festival Fashion',
            'description': 'Boho-chic and eclectic looks perfect for music festivals.',
            'season': 'summer',
            'occasion': 'party',
            'style': ['boho', 'eclectic', 'festival'],
            'tags': ['festival', 'boho', 'music']
        },
        {
            'title': 'Minimalist Capsule',
            'description': 'A carefully curated capsule wardrobe with versatile pieces.',
            'season': 'all',
            'occasion': 'casual',
            'style': ['minimalist', 'capsule', 'versatile'],
            'tags': ['capsule', 'minimalist', 'versatile']
        },
        {
            'title': 'Date Night Collection',
            'description': 'Romantic and flirty outfits perfect for date nights.',
            'season': 'spring',
            'occasion': 'party',
            'style': ['romantic', 'feminine', 'chic'],
            'tags': ['date', 'romantic', 'night']
        },
        {
            'title': 'Travel Style',
            'description': 'Comfortable yet stylish outfits for your next adventure.',
            'season': 'all',
            'occasion': 'travel',
            'style': ['comfortable', 'practical', 'stylish'],
            'tags': ['travel', 'comfort', 'adventure']
        },
    ]
    
    print(f"\n📚 Creating {count} lookbooks...")
    
    for i in range(count):
        template = random.choice(lookbook_templates)
        creator = random.choice(users)
        
        # Create lookbook
        lookbook = Lookbook.objects.create(
            creator=creator,
            title=template['title'],
            description=template['description'],
            season=template['season'],
            occasion=template['occasion'],
            style=template['style'],
            tags=template['tags'],
            is_public=random.choice([True, True, True, False]),  # 75% public
            is_featured=random.choice([True, False, False, False]),  # 25% featured
            likes_count=0,
            views_count=random.randint(100, 5000),
            comments_count=0,
            created_at=timezone.now() - timedelta(days=random.randint(0, 180))
        )
        
        # Add 3-8 outfits to the lookbook
        available_outfits = [o for o in outfits if o.season == template['season'] or template['season'] == 'all']
        if not available_outfits:
            available_outfits = outfits  # Fallback to all outfits
        
        num_outfits = min(random.randint(3, 8), len(available_outfits))
        selected_outfits = random.sample(available_outfits, k=num_outfits)
        
        for order, outfit in enumerate(selected_outfits):
            LookbookOutfit.objects.create(
                lookbook=lookbook,
                outfit=outfit,
                order=order,
                notes=f"Perfect for {template['occasion']} occasions"
            )
        
        # Add some likes
        num_likes = random.randint(0, len(users) // 3)
        likers = random.sample(users, k=min(num_likes, len(users)))
        for liker in likers:
            if liker != creator:
                LookbookLike.objects.get_or_create(
                    user=liker,
                    lookbook=lookbook
                )
        
        # Update likes count
        lookbook.likes_count = LookbookLike.objects.filter(lookbook=lookbook).count()
        lookbook.save()
        
        lookbooks.append(lookbook)
        if (i + 1) % 5 == 0:
            print(f"  Created {i + 1}/{count} lookbooks...")
    
    print(f"✅ Created {len(lookbooks)} lookbooks")
    return lookbooks


def seed_wardrobe_items(users, items_per_user=20):
    """Create wardrobe items for users."""
    categories = ['top', 'bottom', 'shoes', 'accessory', 'outerwear', 'dress', 'bag']
    colors = ['black', 'white', 'navy', 'beige', 'gray', 'brown', 'olive', 'burgundy', 'blue', 'red', 'green', 'pink']
    brands = ['Zara', 'H&M', 'Uniqlo', 'COS', 'Everlane', 'Reformation', 'Madewell', 'Arket', 'Massimo Dutti']
    sizes = ['XS', 'S', 'M', 'L', 'XL']
    seasons = ['spring', 'summer', 'fall', 'winter', 'all']
    
    item_templates = {
        'top': [
            {'name': 'White Cotton T-Shirt', 'brand': 'Everlane', 'price': 28},
            {'name': 'Silk Blouse', 'brand': 'Massimo Dutti', 'price': 79},
            {'name': 'Turtleneck Sweater', 'brand': 'COS', 'price': 89},
            {'name': 'Button-Down Shirt', 'brand': 'Uniqlo', 'price': 39},
            {'name': 'Satin Cami', 'brand': 'Zara', 'price': 39},
        ],
        'bottom': [
            {'name': 'High-Rise Jeans', 'brand': 'Madewell', 'price': 138},
            {'name': 'Wide Leg Trousers', 'brand': 'COS', 'price': 99},
            {'name': 'Tailored Pants', 'brand': 'Arket', 'price': 79},
            {'name': 'Midi Skirt', 'brand': 'H&M', 'price': 49},
            {'name': 'Joggers', 'brand': 'Everlane', 'price': 68},
        ],
        'shoes': [
            {'name': 'Leather Loafers', 'brand': 'Everlane', 'price': 168},
            {'name': 'White Sneakers', 'brand': 'Veja', 'price': 150},
            {'name': 'Pointed Pumps', 'brand': 'Mango', 'price': 69},
            {'name': 'Leather Sandals', 'brand': 'Ancient Greek Sandals', 'price': 245},
            {'name': 'Block Heel Sandals', 'brand': 'Sam Edelman', 'price': 120},
        ],
        'outerwear': [
            {'name': 'Denim Jacket', 'brand': "Levi's", 'price': 98},
            {'name': 'Tailored Blazer', 'brand': 'Zara', 'price': 129},
            {'name': 'Bomber Jacket', 'brand': 'Alpha Industries', 'price': 150},
            {'name': 'Trench Coat', 'brand': 'COS', 'price': 199},
            {'name': 'Cropped Hoodie', 'brand': 'Outdoor Voices', 'price': 75},
        ],
        'dress': [
            {'name': 'Linen Midi Dress', 'brand': 'Reformation', 'price': 178},
            {'name': 'Silk Evening Dress', 'brand': 'Reformation', 'price': 298},
            {'name': 'Embroidered Maxi Dress', 'brand': 'Free People', 'price': 168},
            {'name': 'Wrap Dress', 'brand': 'H&M', 'price': 39},
        ],
        'bag': [
            {'name': 'Structured Tote', 'brand': 'Cuyana', 'price': 175},
            {'name': 'Crossbody Bag', 'brand': 'Coach', 'price': 195},
            {'name': 'Straw Tote Bag', 'brand': 'COS', 'price': 49},
            {'name': 'Backpack', 'brand': 'Away', 'price': 175},
        ],
        'accessory': [
            {'name': 'Leather Belt', 'brand': 'Madewell', 'price': 45},
            {'name': 'Silk Scarf', 'brand': 'Zara', 'price': 29},
            {'name': 'Statement Earrings', 'brand': 'Mejuri', 'price': 98},
            {'name': 'Sunglasses', 'brand': 'Ray-Ban', 'price': 154},
        ],
    }
    
    print(f"\n👔 Creating wardrobe items ({items_per_user} per user)...")
    total_items = 0
    
    for user_idx, user in enumerate(users):
        # Get or create wardrobe for user
        wardrobe, _ = Wardrobe.objects.get_or_create(user=user)
        
        # Create items for this user
        for i in range(items_per_user):
            category = random.choice(categories)
            template = random.choice(item_templates.get(category, item_templates['top']))
            
            WardrobeItem.objects.create(
                wardrobe=wardrobe,
                category=category,
                name=template['name'],
                brand=template.get('brand', ''),
                color=random.choice(colors),
                size=random.choice(sizes) if category != 'accessory' else '',
                price=Decimal(str(template.get('price', random.randint(20, 300)))),
                currency='USD',
                season=random.choice(seasons),
                tags=random.sample(['casual', 'work', 'formal', 'party', 'comfortable', 'stylish'], k=random.randint(1, 3)),
                times_worn=random.randint(0, 50),
                last_worn_date=timezone.now().date() - timedelta(days=random.randint(0, 180)) if random.choice([True, False]) else None,
                purchase_date=timezone.now().date() - timedelta(days=random.randint(30, 1000)) if random.choice([True, False]) else None,
                purchase_link=f"https://example.com/product/{random.randint(1000, 9999)}" if random.choice([True, False]) else '',
            )
            total_items += 1
        
        if (user_idx + 1) % 5 == 0:
            print(f"  Created items for {user_idx + 1}/{len(users)} users...")
    
    print(f"✅ Created {total_items} wardrobe items for {len(users)} users")
    return total_items


def main():
    """Main function."""
    print("=" * 60)
    print("🌱 Seeding Lookbooks and Wardrobe Data")
    print("=" * 60)
    
    # Get users (need at least some users to create lookbooks/wardrobes)
    users = list(User.objects.filter(is_superuser=False)[:20])
    if not users:
        print("\n⚠️  No users found! Creating a test user first...")
        user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        UserProfile.objects.get_or_create(user=user)
        users = [user]
    
    print(f"\n👥 Found {len(users)} users")
    
    # Get outfits (need outfits to add to lookbooks)
    outfits = list(Outfit.objects.all()[:50])
    if not outfits:
        print("\n⚠️  No outfits found! Lookbooks will be created without outfits.")
        outfits = []
    else:
        print(f"👗 Found {len(outfits)} outfits")
    
    # Seed lookbooks
    lookbooks = seed_lookbooks(users, outfits, count=15)
    
    # Seed wardrobe items
    total_items = seed_wardrobe_items(users, items_per_user=20)
    
    print("\n" + "=" * 60)
    print("✅ Seeding completed successfully!")
    print(f"   - Created {len(lookbooks)} lookbooks")
    print(f"   - Created {total_items} wardrobe items")
    print("=" * 60)


if __name__ == '__main__':
    main()

