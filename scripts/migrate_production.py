"""
Script to run missing migrations on production database.
This will add the lookbooks and wardrobe tables without affecting existing data.
"""
import os
import sys
import django
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set up Django - use base settings (will use DATABASE_URL if set)
# Strip any whitespace from settings module and ensure it's set
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', '').strip()
if not settings_module or settings_module == '':
    settings_module = 'curator.settings.base'
os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
from django.conf import settings


def check_table_exists(table_name):
    """Check if a table exists in the database."""
    try:
        with connection.cursor() as cursor:
            if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = %s
                    );
                """, [table_name])
            else:
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name=?;
                """, [table_name])
            result = cursor.fetchone()
            return result[0] if result else False
    except Exception as e:
        print(f"Error checking table {table_name}: {e}")
        return False


def show_missing_tables():
    """Show which tables are missing."""
    required_tables = {
        'lookbooks': 'Lookbooks app',
        'wardrobes': 'Wardrobe app',
        'lookbook_outfits': 'Lookbooks app',
        'lookbook_likes': 'Lookbooks app',
        'wardrobe_items': 'Wardrobe app',
        'posts': 'Social app (Feed)',
        'post_images': 'Social app',
        'post_likes': 'Social app',
        'post_saves': 'Social app',
        'comments': 'Social app',
        'comment_likes': 'Social app',
        'user_following': 'Accounts app (Required for Social Feed)',
        'shopping_carts': 'Cart app',
        'cart_items': 'Cart app',
        'promo_codes': 'Cart app',
    }
    
    missing = []
    existing = []
    
    for table, app in required_tables.items():
        exists = check_table_exists(table)
        if exists:
            existing.append(table)
            print(f"✅ {table} exists")
        else:
            missing.append(table)
            print(f"❌ {table} missing ({app})")
    
    return missing, existing


def run_migrations():
    """Run migrations for lookbooks, wardrobe, social, and cart apps."""
    print("\n🔄 Running migrations for lookbooks, wardrobe, social, and cart apps...")
    try:
        # Run migrations for each app separately
        apps_to_migrate = ['accounts', 'lookbooks', 'outfits', 'wardrobe', 'social', 'cart']
        
        for app in apps_to_migrate:
            print(f"\n  Migrating {app}...")
            execute_from_command_line([
                'manage.py', 
                'migrate', 
                app,
                '--verbosity', 
                '2'
            ])
        
        print("\n✅ Migrations completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function."""
    print("=" * 60)
    print("🚀 CuratorAI Production Database Migration")
    print("=" * 60)
    
    # Show database info
    db = settings.DATABASES['default']
    print(f"\n📊 Database: {db.get('NAME', 'N/A')}")
    print(f"   Host: {db.get('HOST', 'N/A')}")
    
    # Check connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n⚠️  Please check your DATABASE_URL or database credentials.")
        return False
    
    # Check which tables are missing
    print("\n📋 Checking required tables...")
    missing, existing = show_missing_tables()
    
    if not missing:
        print("\n✅ All required tables already exist!")
        print("\n🔄 Running migrations to add new columns (image_url fields)...")
    else:
        print(f"\n⚠️  Found {len(missing)} missing table(s)")
        print("\n⚠️  WARNING: This will create new tables in your production database.")
        print("   Existing data will NOT be affected.")
    
    # Always run migrations to ensure all columns are up to date
    if run_migrations():
        # Verify tables were created
        print("\n📋 Verifying tables were created...")
        missing_after, existing_after = show_missing_tables()
        
        if not missing_after:
            print("\n✅ All tables created successfully!")
            return True
        else:
            print(f"\n⚠️  Some tables are still missing: {missing_after}")
            return False
    
    return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

