"""
Script to create migrations for social app and run them.
"""
import os
import sys
import django
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set up Django - use base settings (will use DATABASE_URL if set)
os.environ['DJANGO_SETTINGS_MODULE'] = 'curator.settings.base'
django.setup()

from django.core.management import execute_from_command_line

def main():
    """Create migrations and run them."""
    print("=" * 60)
    print("🚀 Creating Social App Migrations")
    print("=" * 60)
    
    # Create migrations
    print("\n📝 Creating migrations for social app...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations', 'social'])
        print("✅ Migrations created successfully!")
    except Exception as e:
        print(f"❌ Failed to create migrations: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Run migrations
    print("\n🔄 Running migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', 'social', '--verbosity', '2'])
        print("✅ Migrations applied successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to run migrations: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

