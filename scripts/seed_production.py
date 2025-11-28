"""
Script to seed the production database with sample data.
This script properly sets up Django and runs the seed_data command.
"""
import os
import sys
import django
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set up Django - use base settings (will use DATABASE_URL if set)
# Clear any existing DJANGO_SETTINGS_MODULE that might have issues
if 'DJANGO_SETTINGS_MODULE' in os.environ:
    del os.environ['DJANGO_SETTINGS_MODULE']

os.environ['DJANGO_SETTINGS_MODULE'] = 'curator.settings.base'
django.setup()

from django.core.management import execute_from_command_line

def main():
    """Run seed_data command with arguments."""
    print("=" * 60)
    print("🌱 Seeding Production Database")
    print("=" * 60)
    
    # Get command line arguments (skip script name)
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # Build command
    command = ['manage.py', 'seed_data'] + args
    
    print(f"\n📝 Running: python {' '.join(command)}")
    print()
    
    try:
        execute_from_command_line(['manage.py'] + ['seed_data'] + args)
        print("\n✅ Seeding completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Seeding failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

