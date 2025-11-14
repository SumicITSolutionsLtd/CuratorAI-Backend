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
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            OutfitSave.objects.all().delete()
            OutfitLike.objects.all().delete()
            OutfitItem.objects.all().delete()
            Outfit.objects.all().delete()
            UserFollowing.objects.all().delete()
            StylePreference.objects.all().delete()
            UserProfile.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('Cleared existing data'))

        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # Seed users
        users = self.seed_users(options['users'])
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users'))

        # Seed outfits
        outfits = self.seed_outfits(users, options['outfits'])
        self.stdout.write(self.style.SUCCESS(f'Created {len(outfits)} outfits'))

        # Seed social interactions
        self.seed_social_interactions(users, outfits)
        self.stdout.write(self.style.SUCCESS('Created social interactions'))

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

            # Create user
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password='testpass123',
                first_name=data['first_name'],
                last_name=data['last_name'],
                is_verified=random.choice([True, True, True, False]),  # 75% verified
                bio=self.generate_bio(data['first_name'])
            )

            # Create profile
            city, country = random.choice(cities)
            gender = random.choice(['M', 'F', 'O'])

            UserProfile.objects.create(
                user=user,
                gender=gender,
                date_of_birth=datetime.now().date() - timedelta(days=random.randint(7300, 14600)),  # 20-40 years old
                country=country,
                city=city,
                body_type=random.choice(['slim', 'athletic', 'average', 'curvy', 'plus']),
                height=random.randint(155, 190),
                weight=random.randint(50, 100),
                top_size=random.choice(['XS', 'S', 'M', 'L', 'XL']),
                bottom_size=random.choice(['26', '28', '30', '32', '34', '36']),
                shoe_size=random.choice(['7', '8', '9', '10', '11']),
                dress_size=random.choice(['0', '2', '4', '6', '8', '10', '12'])
            )

            # Create style preferences
            StylePreference.objects.create(
                user=user,
                preferred_styles=random.sample(style_options, k=random.randint(2, 5)),
                preferred_colors=random.sample(color_options, k=random.randint(3, 7)),
                preferred_brands=random.sample(brand_options, k=random.randint(2, 6)),
                preferred_patterns=['solid', 'stripes', 'floral', 'geometric', 'abstract'][:random.randint(1, 3)],
                budget_min=Decimal(random.choice([0, 50, 100, 200])),
                budget_max=Decimal(random.choice([500, 1000, 2000, 5000])),
                currency='USD',
                occasions=random.sample(['work', 'casual', 'formal', 'party', 'sport', 'date'], k=random.randint(2, 4)),
                prefer_sustainable=random.choice([True, False]),
                prefer_secondhand=random.choice([True, False]),
                fit_preference=random.choice(['loose', 'regular', 'tight', 'oversized', 'fitted'])
            )

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
