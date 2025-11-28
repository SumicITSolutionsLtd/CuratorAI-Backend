"""
Management command to seed the database with sample data.
"""
import random
from decimal import Decimal
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.accounts.models import UserProfile, StylePreference, UserFollowing
from apps.outfits.models import Outfit, OutfitItem, OutfitLike, OutfitSave
from apps.lookbooks.models import Lookbook, LookbookOutfit, LookbookLike
from apps.wardrobe.models import Wardrobe, WardrobeItem
try:
    from apps.social.models import Post, PostImage, PostLike, PostSave, Comment, CommentLike
    SOCIAL_APP_AVAILABLE = True
except ImportError:
    SOCIAL_APP_AVAILABLE = False

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with sample data for development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=20,
            help='Number of users to create'
        )
        parser.add_argument(
            '--outfits',
            type=int,
            default=50,
            help='Number of outfits to create'
        )
        parser.add_argument(
            '--lookbooks',
            type=int,
            default=20,
            help='Number of lookbooks to create'
        )
        parser.add_argument(
            '--wardrobe-items',
            type=int,
            default=100,
            help='Number of wardrobe items to create per user'
        )
        parser.add_argument(
            '--posts',
            type=int,
            default=50,
            help='Number of social posts to create'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        # Check if migrations have been run
        from django.db import connection
        tables = connection.introspection.table_names()
        
        if 'users' not in tables or 'outfits' not in tables:
            self.stdout.write(self.style.ERROR(
                '\n❌ ERROR: Database tables do not exist!\n'
                'Please run migrations first:\n'
                '  python manage.py migrate\n'
                'Then run this command again.\n'
            ))
            return
        
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            try:
                # Delete in order to respect foreign key constraints
                from django.db import connection
                tables = connection.introspection.table_names()
                
                if 'outfit_saves' in tables:
                    OutfitSave.objects.all().delete()
                if 'outfit_likes' in tables:
                    OutfitLike.objects.all().delete()
                if 'outfit_items' in tables:
                    OutfitItem.objects.all().delete()
                if 'outfits' in tables:
                    Outfit.objects.all().delete()
                if 'user_following' in tables:
                    UserFollowing.objects.all().delete()
                if 'style_preferences' in tables:
                    StylePreference.objects.all().delete()
                if 'user_profiles' in tables:
                    UserProfile.objects.all().delete()
                if 'users' in tables:
                    # Delete users one by one to avoid cascade issues with missing tables
                    non_superusers = User.objects.filter(is_superuser=False)
                    count = non_superusers.count()
                    for user in non_superusers:
                        try:
                            user.delete()
                        except Exception:
                            # If cascade delete fails due to missing tables, continue
                            pass
                    self.stdout.write(self.style.SUCCESS(f'Deleted {count} users'))
                self.stdout.write(self.style.SUCCESS('Cleared existing data'))
            except Exception as e:
                # Don't fail completely if some tables are missing
                self.stdout.write(self.style.WARNING(f'Warning during clear: {e}'))
                self.stdout.write(self.style.SUCCESS('Continuing with seeding...'))

        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # Seed users
        users = self.seed_users(options.get('users', 20))
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users'))

        # Seed outfits
        outfits = self.seed_outfits(users, options.get('outfits', 50))
        self.stdout.write(self.style.SUCCESS(f'Created {len(outfits)} outfits'))

        # Seed social interactions
        self.seed_social_interactions(users, outfits)
        self.stdout.write(self.style.SUCCESS('Created social interactions'))

        # Seed lookbooks
        lookbooks = self.seed_lookbooks(users, outfits, options.get('lookbooks', 20))
        self.stdout.write(self.style.SUCCESS(f'Created {len(lookbooks)} lookbooks'))

        # Seed wardrobe items
        self.seed_wardrobe_items(users, options.get('wardrobe-items', 100))
        self.stdout.write(self.style.SUCCESS(f'Created wardrobe items for {len(users)} users'))

        # Seed social posts
        if SOCIAL_APP_AVAILABLE:
            posts = self.seed_social_posts(users, outfits, options.get('posts', 50))
            self.stdout.write(self.style.SUCCESS(f'Created {len(posts)} social posts'))
        else:
            self.stdout.write(self.style.WARNING('Social app not available, skipping posts'))

        self.stdout.write(self.style.SUCCESS('✅ Database seeding completed successfully!'))

    def seed_users(self, count):
        """Create sample users with profiles and style preferences."""
        users = []

        # Predefined user data for realistic names
        user_data = [
            {'username': 'sarah_j', 'first_name': 'Sarah', 'last_name': 'Johnson', 'email': 'sarah.johnson@example.com'},
            {'username': 'mike_chen', 'first_name': 'Mike', 'last_name': 'Chen', 'email': 'mike.chen@example.com'},
            {'username': 'emma_w', 'first_name': 'Emma', 'last_name': 'Wilson', 'email': 'emma.wilson@example.com'},
            {'username': 'james_fashion', 'first_name': 'James', 'last_name': 'Lee', 'email': 'james.lee@example.com'},
            {'username': 'liv_style', 'first_name': 'Olivia', 'last_name': 'Brown', 'email': 'olivia.brown@example.com'},
            {'username': 'alex_minimal', 'first_name': 'Alex', 'last_name': 'Martinez', 'email': 'alex.martinez@example.com'},
            {'username': 'sophia_chic', 'first_name': 'Sophia', 'last_name': 'Garcia', 'email': 'sophia.garcia@example.com'},
            {'username': 'noah_street', 'first_name': 'Noah', 'last_name': 'Rodriguez', 'email': 'noah.rodriguez@example.com'},
            {'username': 'ava_elegant', 'first_name': 'Ava', 'last_name': 'Taylor', 'email': 'ava.taylor@example.com'},
            {'username': 'liam_casual', 'first_name': 'Liam', 'last_name': 'Anderson', 'email': 'liam.anderson@example.com'},
            {'username': 'mia_boho', 'first_name': 'Mia', 'last_name': 'Thomas', 'email': 'mia.thomas@example.com'},
            {'username': 'ethan_sport', 'first_name': 'Ethan', 'last_name': 'Jackson', 'email': 'ethan.jackson@example.com'},
            {'username': 'isabella_glam', 'first_name': 'Isabella', 'last_name': 'White', 'email': 'isabella.white@example.com'},
            {'username': 'mason_urban', 'first_name': 'Mason', 'last_name': 'Harris', 'email': 'mason.harris@example.com'},
            {'username': 'charlotte_vintage', 'first_name': 'Charlotte', 'last_name': 'Martin', 'email': 'charlotte.martin@example.com'},
            {'username': 'lucas_modern', 'first_name': 'Lucas', 'last_name': 'Thompson', 'email': 'lucas.thompson@example.com'},
            {'username': 'amelia_preppy', 'first_name': 'Amelia', 'last_name': 'Garcia', 'email': 'amelia.garcia@example.com'},
            {'username': 'oliver_edgy', 'first_name': 'Oliver', 'last_name': 'Martinez', 'email': 'oliver.martinez@example.com'},
            {'username': 'harper_soft', 'first_name': 'Harper', 'last_name': 'Robinson', 'email': 'harper.robinson@example.com'},
            {'username': 'benjamin_classic', 'first_name': 'Benjamin', 'last_name': 'Clark', 'email': 'benjamin.clark@example.com'},
        ]

        cities = [
            ('New York', 'US'), ('Los Angeles', 'US'), ('London', 'UK'),
            ('Paris', 'FR'), ('Tokyo', 'JP'), ('Milan', 'IT'),
            ('Berlin', 'DE'), ('Sydney', 'AU'), ('Toronto', 'CA'),
            ('Seoul', 'KR'), ('Barcelona', 'ES'), ('Amsterdam', 'NL')
        ]

        style_options = [
            'minimalist', 'boho', 'streetwear', 'preppy', 'vintage',
            'modern', 'classic', 'edgy', 'romantic', 'athleisure',
            'chic', 'casual', 'elegant', 'urban', 'sophisticated'
        ]

        color_options = [
            'black', 'white', 'navy', 'beige', 'gray', 'brown',
            'olive', 'burgundy', 'camel', 'cream', 'charcoal',
            'blush', 'sage', 'rust', 'emerald', 'denim'
        ]

        brand_options = [
            'Zara', 'H&M', 'Uniqlo', 'COS', 'Everlane',
            'Reformation', 'Madewell', 'Arket', '& Other Stories',
            'Massimo Dutti', 'Sezane', 'Ganni', 'Acne Studios',
            'A.P.C.', 'Norse Projects', 'Our Legacy'
        ]

        for i in range(min(count, len(user_data))):
            data = user_data[i]

            # Check if user already exists
            user, created = User.objects.get_or_create(
                email=data['email'],
                defaults={
                    'username': data['username'],
                    'password': 'pbkdf2_sha256$720000$dummy$dummy',  # Will be set below
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'is_verified': random.choice([True, True, True, False]),  # 75% verified
                    'bio': self.generate_bio(data['first_name'])
                }
            )
            
            # If user was just created, set the password properly
            if created:
                user.set_password('testpass123')
                user.save()
                
                # Create profile
                city, country = random.choice(cities)
                gender = random.choice(['M', 'F', 'O'])

                UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'gender': gender,
                        'date_of_birth': datetime.now().date() - timedelta(days=random.randint(7300, 14600)),  # 20-40 years old
                        'country': country,
                        'city': city,
                        'body_type': random.choice(['slim', 'athletic', 'average', 'curvy', 'plus']),
                        'height': random.randint(155, 190),
                        'weight': random.randint(50, 100),
                        'top_size': random.choice(['XS', 'S', 'M', 'L', 'XL']),
                        'bottom_size': random.choice(['26', '28', '30', '32', '34', '36']),
                        'shoe_size': random.choice(['7', '8', '9', '10', '11']),
                        'dress_size': random.choice(['0', '2', '4', '6', '8', '10', '12'])
                    }
                )

                # Create style preferences
                StylePreference.objects.get_or_create(
                    user=user,
                    defaults={
                        'preferred_styles': random.sample(style_options, k=random.randint(2, 5)),
                        'preferred_colors': random.sample(color_options, k=random.randint(3, 7)),
                        'preferred_brands': random.sample(brand_options, k=random.randint(2, 6)),
                        'preferred_patterns': ['solid', 'stripes', 'floral', 'geometric', 'abstract'][:random.randint(1, 3)],
                        'budget_min': Decimal(random.choice([0, 50, 100, 200])),
                        'budget_max': Decimal(random.choice([500, 1000, 2000, 5000])),
                        'currency': 'USD',
                        'occasions': random.sample(['work', 'casual', 'formal', 'party', 'sport', 'date'], k=random.randint(2, 4)),
                        'prefer_sustainable': random.choice([True, False]),
                        'prefer_secondhand': random.choice([True, False]),
                        'fit_preference': random.choice(['loose', 'regular', 'tight', 'oversized', 'fitted'])
                    }
                )
            else:
                # User already exists, skip
                self.stdout.write(self.style.WARNING(f'User {data["email"]} already exists, skipping...'))

            users.append(user)

        # Create following relationships
        for user in users:
            # Each user follows 3-8 random other users
            potential_follows = [u for u in users if u != user]
            follows = random.sample(potential_follows, k=min(random.randint(3, 8), len(potential_follows)))
            for follow in follows:
                UserFollowing.objects.get_or_create(
                    follower=user,
                    following=follow
                )

        return users

    def seed_outfits(self, users, count):
        """Create sample outfits with items."""
        outfits = []

        outfit_templates = [
            {
                'title': 'Summer Brunch Look',
                'description': 'Perfect for a relaxed weekend brunch with friends. Light, airy, and effortlessly chic.',
                'occasion': 'casual',
                'season': 'summer',
                'style_tags': ['casual', 'minimalist', 'fresh'],
                'color_palette': ['white', 'beige', 'tan'],
                'items': [
                    {'type': 'dress', 'name': 'Linen Midi Dress', 'brand': 'Reformation', 'price': 178},
                    {'type': 'shoes', 'name': 'Leather Sandals', 'brand': 'Ancient Greek Sandals', 'price': 245},
                    {'type': 'accessory', 'name': 'Straw Tote Bag', 'brand': 'COS', 'price': 49},
                ]
            },
            {
                'title': 'Office Power Suit',
                'description': 'Make a statement in the boardroom. Professional yet stylish ensemble.',
                'occasion': 'work',
                'season': 'all',
                'style_tags': ['professional', 'modern', 'sophisticated'],
                'color_palette': ['navy', 'white', 'black'],
                'items': [
                    {'type': 'outerwear', 'name': 'Tailored Blazer', 'brand': 'Zara', 'price': 129},
                    {'type': 'bottom', 'name': 'Wide Leg Trousers', 'brand': 'COS', 'price': 99},
                    {'type': 'top', 'name': 'Silk Blouse', 'brand': 'Massimo Dutti', 'price': 79},
                    {'type': 'shoes', 'name': 'Pointed Pumps', 'brand': 'Mango', 'price': 69},
                ]
            },
            {
                'title': 'Weekend Casual Vibes',
                'description': 'Comfortable and cool for running errands or meeting friends for coffee.',
                'occasion': 'casual',
                'season': 'spring',
                'style_tags': ['casual', 'streetwear', 'relaxed'],
                'color_palette': ['denim', 'white', 'olive'],
                'items': [
                    {'type': 'outerwear', 'name': 'Denim Jacket', 'brand': "Levi's", 'price': 98},
                    {'type': 'top', 'name': 'White Cotton Tee', 'brand': 'Everlane', 'price': 28},
                    {'type': 'bottom', 'name': 'High-Rise Jeans', 'brand': 'Madewell', 'price': 138},
                    {'type': 'shoes', 'name': 'White Sneakers', 'brand': 'Veja', 'price': 150},
                ]
            },
            {
                'title': 'Evening Elegance',
                'description': 'Stunning outfit for a special evening out or formal event.',
                'occasion': 'formal',
                'season': 'winter',
                'style_tags': ['elegant', 'sophisticated', 'glamorous'],
                'color_palette': ['black', 'gold', 'burgundy'],
                'items': [
                    {'type': 'dress', 'name': 'Silk Evening Dress', 'brand': 'Reformation', 'price': 298},
                    {'type': 'shoes', 'name': 'Strappy Heels', 'brand': 'Stuart Weitzman', 'price': 425},
                    {'type': 'accessory', 'name': 'Clutch Bag', 'brand': 'Mango', 'price': 59},
                    {'type': 'jewelry', 'name': 'Statement Earrings', 'brand': 'Mejuri', 'price': 98},
                ]
            },
            {
                'title': 'Athleisure Chic',
                'description': 'Gym to street style that keeps you comfortable and stylish all day.',
                'occasion': 'sport',
                'season': 'all',
                'style_tags': ['athleisure', 'sporty', 'comfortable'],
                'color_palette': ['black', 'gray', 'white'],
                'items': [
                    {'type': 'top', 'name': 'Sports Bra', 'brand': 'Lululemon', 'price': 52},
                    {'type': 'bottom', 'name': 'High-Waist Leggings', 'brand': 'Alo Yoga', 'price': 118},
                    {'type': 'outerwear', 'name': 'Cropped Hoodie', 'brand': 'Outdoor Voices', 'price': 75},
                    {'type': 'shoes', 'name': 'Running Shoes', 'brand': 'Nike', 'price': 140},
                ]
            },
            {
                'title': 'Date Night Ready',
                'description': 'Flirty and fun outfit perfect for a romantic evening.',
                'occasion': 'date',
                'season': 'spring',
                'style_tags': ['romantic', 'feminine', 'chic'],
                'color_palette': ['blush', 'nude', 'gold'],
                'items': [
                    {'type': 'top', 'name': 'Satin Cami', 'brand': 'Zara', 'price': 39},
                    {'type': 'bottom', 'name': 'Midi Skirt', 'brand': 'H&M', 'price': 49},
                    {'type': 'shoes', 'name': 'Block Heel Sandals', 'brand': 'Sam Edelman', 'price': 120},
                    {'type': 'bag', 'name': 'Crossbody Bag', 'brand': 'Coach', 'price': 195},
                ]
            },
            {
                'title': 'Travel Comfort',
                'description': 'Stylish yet comfortable outfit for long flights and airport days.',
                'occasion': 'travel',
                'season': 'all',
                'style_tags': ['comfortable', 'casual', 'practical'],
                'color_palette': ['navy', 'gray', 'black'],
                'items': [
                    {'type': 'top', 'name': 'Oversized Sweater', 'brand': 'Uniqlo', 'price': 49},
                    {'type': 'bottom', 'name': 'Joggers', 'brand': 'Everlane', 'price': 68},
                    {'type': 'shoes', 'name': 'Slip-On Sneakers', 'brand': 'Allbirds', 'price': 95},
                    {'type': 'bag', 'name': 'Backpack', 'brand': 'Away', 'price': 175},
                ]
            },
            {
                'title': 'Boho Festival',
                'description': 'Free-spirited and fun outfit perfect for music festivals or outdoor events.',
                'occasion': 'party',
                'season': 'summer',
                'style_tags': ['boho', 'festival', 'eclectic'],
                'color_palette': ['rust', 'cream', 'brown'],
                'items': [
                    {'type': 'dress', 'name': 'Embroidered Maxi Dress', 'brand': 'Free People', 'price': 168},
                    {'type': 'shoes', 'name': 'Gladiator Sandals', 'brand': 'Steve Madden', 'price': 79},
                    {'type': 'accessory', 'name': 'Fringe Bag', 'brand': 'Mango', 'price': 69},
                    {'type': 'jewelry', 'name': 'Layered Necklaces', 'brand': 'Etsy', 'price': 45},
                ]
            },
            {
                'title': 'Minimalist Monochrome',
                'description': 'Clean lines and neutral tones for a timeless, sophisticated look.',
                'occasion': 'work',
                'season': 'fall',
                'style_tags': ['minimalist', 'modern', 'clean'],
                'color_palette': ['black', 'white', 'gray'],
                'items': [
                    {'type': 'top', 'name': 'Turtleneck Sweater', 'brand': 'COS', 'price': 89},
                    {'type': 'bottom', 'name': 'Tailored Pants', 'brand': 'Arket', 'price': 79},
                    {'type': 'shoes', 'name': 'Leather Loafers', 'brand': 'Everlane', 'price': 168},
                    {'type': 'bag', 'name': 'Structured Tote', 'brand': 'Cuyana', 'price': 175},
                ]
            },
            {
                'title': 'Streetwear Edge',
                'description': 'Urban cool with a touch of attitude. Perfect for city exploring.',
                'occasion': 'casual',
                'season': 'fall',
                'style_tags': ['streetwear', 'urban', 'edgy'],
                'color_palette': ['black', 'olive', 'white'],
                'items': [
                    {'type': 'outerwear', 'name': 'Bomber Jacket', 'brand': 'Alpha Industries', 'price': 150},
                    {'type': 'top', 'name': 'Graphic Tee', 'brand': 'Urban Outfitters', 'price': 39},
                    {'type': 'bottom', 'name': 'Cargo Pants', 'brand': 'Dickies', 'price': 58},
                    {'type': 'shoes', 'name': 'High-Top Sneakers', 'brand': 'Converse', 'price': 85},
                ]
            },
        ]

        for i in range(count):
            template = random.choice(outfit_templates)
            user = random.choice(users)

            # Create outfit
            outfit = Outfit.objects.create(
                user=user,
                title=template['title'],
                description=template['description'],
                occasion=template['occasion'],
                season=template['season'],
                style_tags=template['style_tags'],
                color_palette=template['color_palette'],
                ai_generated=random.choice([True, False]),
                confidence_score=random.uniform(0.75, 0.99) if random.choice([True, False]) else None,
                is_public=random.choice([True, True, True, False]),  # 75% public
                likes_count=0,
                saves_count=0,
                views_count=random.randint(50, 5000),
                created_at=timezone.now() - timedelta(days=random.randint(0, 90))
            )

            # Create outfit items
            for item_data in template['items']:
                OutfitItem.objects.create(
                    outfit=outfit,
                    item_type=item_data['type'],
                    name=item_data['name'],
                    brand=item_data['brand'],
                    price=Decimal(str(item_data['price'])),
                    currency='USD',
                    size=random.choice(['XS', 'S', 'M', 'L', 'XL']),
                    color=random.choice(template['color_palette']),
                    material=random.choice(['Cotton', 'Linen', 'Silk', 'Wool', 'Polyester', 'Leather']),
                    purchase_url=f"https://example.com/product/{random.randint(1000, 9999)}",
                    retailer=item_data['brand'],
                    is_available=random.choice([True, True, True, False])  # 75% available
                )

            outfits.append(outfit)

        return outfits

    def seed_social_interactions(self, users, outfits):
        """Create likes and saves for outfits."""
        for outfit in outfits:
            # Random number of likes (0-50% of users)
            num_likes = random.randint(0, len(users) // 2)
            likers = random.sample(users, k=min(num_likes, len(users)))

            for liker in likers:
                if liker != outfit.user:  # Users don't like their own outfits
                    OutfitLike.objects.get_or_create(
                        user=liker,
                        outfit=outfit
                    )

            # Update likes count
            outfit.likes_count = OutfitLike.objects.filter(outfit=outfit).count()

            # Random number of saves (0-30% of users)
            num_saves = random.randint(0, len(users) // 3)
            savers = random.sample(users, k=min(num_saves, len(users)))

            collections = ['Summer Wardrobe', 'Work Outfits', 'Date Night', 'Inspiration', 'Fall Favorites']

            for saver in savers:
                if saver != outfit.user:  # Users don't save their own outfits
                    OutfitSave.objects.get_or_create(
                        user=saver,
                        outfit=outfit,
                        defaults={'collection_name': random.choice(collections)}
                    )

            # Update saves count
            outfit.saves_count = OutfitSave.objects.filter(outfit=outfit).count()
            outfit.save()

    def generate_bio(self, name):
        """Generate a realistic user bio."""
        bios = [
            f"Fashion enthusiast 👗 | Style is my passion | Based in {random.choice(['NYC', 'LA', 'London', 'Paris'])}",
            f"Personal stylist & fashion blogger ✨ Helping you find your style",
            f"Sustainable fashion advocate 🌱 | Vintage lover | Thrift finds",
            f"Minimalist wardrobe curator | Less is more 🤍",
            f"Street style photographer 📸 | Fashion week regular",
            f"DIY fashion & upcycling | Creating unique looks everyday",
            f"Plus size fashion inspiration 💕 | Style has no size",
            f"Luxury fashion on a budget | Smart shopping tips",
            f"Capsule wardrobe expert | Quality over quantity",
            f"Fashion student 🎓 | Exploring my personal style journey"
        ]
        return random.choice(bios)

    def seed_lookbooks(self, users, outfits, count):
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
        
        return lookbooks

    def seed_wardrobe_items(self, users, items_per_user):
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
        
        for user in users:
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

    def seed_social_posts(self, users, outfits, count):
        """Create social posts with comments, likes, and saves."""
        if not SOCIAL_APP_AVAILABLE:
            return []
        
        posts = []
        captions = [
            "Feeling confident in this outfit! ✨ #OOTD #Fashion",
            "Loving this new look! What do you think? 👗",
            "Perfect for a day out! #StyleInspiration",
            "Can't get enough of this combination! 💕",
            "This outfit makes me feel amazing! #Confidence",
            "Trying something new today! Thoughts? 🤔",
            "One of my favorite looks! #FashionWeek",
            "Casual but chic! #EverydayStyle",
            "This never goes out of style! #Classic",
            "Feeling the vibes! ✨ #GoodVibes",
            "New favorite outfit! #NewFavorites",
            "This is giving me life! 💃 #Fashionista",
            "Simple but elegant! #MinimalistStyle",
            "Love how this turned out! #OutfitOfTheDay",
            "This combo is everything! 🔥 #StyleGoals",
        ]
        
        hashtags_pool = [
            'OOTD', 'Fashion', 'Style', 'Outfit', 'Fashionista', 'FashionWeek',
            'StyleInspiration', 'FashionBlogger', 'StreetStyle', 'FashionStyle',
            'FashionAddict', 'FashionDiary', 'StyleGoals', 'FashionLover',
            'OutfitOfTheDay', 'FashionInspo', 'StyleOfTheDay', 'FashionDaily',
            'MinimalistStyle', 'CasualStyle', 'ChicStyle', 'ElegantStyle'
        ]
        
        locations = [
            ('New York, NY', 40.7128, -74.0060),
            ('Los Angeles, CA', 34.0522, -118.2437),
            ('London, UK', 51.5074, -0.1278),
            ('Paris, France', 48.8566, 2.3522),
            ('Tokyo, Japan', 35.6762, 139.6503),
            ('Milan, Italy', 45.4642, 9.1900),
            ('Berlin, Germany', 52.5200, 13.4050),
            ('Sydney, Australia', -33.8688, 151.2093),
        ]
        
        for i in range(count):
            user = random.choice(users)
            outfit = random.choice(outfits) if outfits else None
            
            # Generate caption
            caption = random.choice(captions)
            # Add random hashtags
            num_tags = random.randint(2, 5)
            tags = random.sample(hashtags_pool, k=num_tags)
            
            # Random location (50% chance)
            location_name = ''
            location_lat = None
            location_lng = None
            if random.choice([True, False]):
                loc_name, lat, lng = random.choice(locations)
                location_name = loc_name
                location_lat = lat
                location_lng = lng
            
            # Create post
            post = Post.objects.create(
                user=user,
                caption=caption,
                tags=tags,
                outfit=outfit,
                tagged_items=[],  # Empty for now, can be enhanced later
                location_name=location_name,
                location_lat=location_lat,
                location_lng=location_lng,
                privacy=random.choice(['public', 'public', 'public', 'friends']),  # 75% public
                likes_count=0,
                comments_count=0,
                shares_count=random.randint(0, 20),
                saves_count=0,
                views_count=random.randint(50, 5000),
                is_deleted=False,
                created_at=timezone.now() - timedelta(days=random.randint(0, 90))
            )
            
            # Add likes
            num_likes = random.randint(0, len(users) // 2)
            likers = random.sample(users, k=min(num_likes, len(users)))
            for liker in likers:
                if liker != user:
                    PostLike.objects.get_or_create(
                        user=liker,
                        post=post
                    )
            post.likes_count = PostLike.objects.filter(post=post).count()
            
            # Add saves
            num_saves = random.randint(0, len(users) // 3)
            savers = random.sample(users, k=min(num_saves, len(users)))
            for saver in savers:
                if saver != user:
                    PostSave.objects.get_or_create(
                        user=saver,
                        post=post
                    )
            post.saves_count = PostSave.objects.filter(post=post).count()
            
            # Add comments
            num_comments = random.randint(0, 10)
            commenters = random.sample(users, k=min(num_comments, len(users)))
            comment_texts = [
                "Love this! 😍",
                "So cute! Where did you get it?",
                "This is amazing! ✨",
                "You look great!",
                "Perfect styling! 👌",
                "This is goals! 🔥",
                "Beautiful outfit!",
                "I need this in my wardrobe!",
                "So inspiring! 💕",
                "Can't wait to try this!",
            ]
            
            for commenter in commenters:
                if commenter != user:
                    comment = Comment.objects.create(
                        post=post,
                        user=commenter,
                        content=random.choice(comment_texts),
                        likes_count=0,
                        is_deleted=False,
                        created_at=post.created_at + timedelta(minutes=random.randint(1, 1440))
                    )
                    
                    # Add some likes to comments
                    if random.choice([True, False]):
                        num_comment_likes = random.randint(0, 5)
                        comment_likers = random.sample(users, k=min(num_comment_likes, len(users)))
                        for liker in comment_likers:
                            if liker != commenter:
                                CommentLike.objects.get_or_create(
                                    user=liker,
                                    comment=comment
                                )
                        comment.likes_count = CommentLike.objects.filter(comment=comment).count()
                        comment.save()
            
            post.comments_count = Comment.objects.filter(post=post, is_deleted=False).count()
            post.save()
            
            posts.append(post)
        
        return posts
