"""
Script to set up PostgreSQL database and run migrations.
This script helps configure and migrate the database for CuratorAI.
"""
import os
import sys
import django
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'curator.settings.base')
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
from django.conf import settings


def check_database_connection():
    """Check if database connection is working."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("✅ Database connection successful!")
                return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def show_database_info():
    """Show current database configuration."""
    db = settings.DATABASES['default']
    print("\n📊 Current Database Configuration:")
    print(f"   Engine: {db['ENGINE']}")
    print(f"   Name: {db.get('NAME', 'N/A')}")
    print(f"   Host: {db.get('HOST', 'N/A')}")
    print(f"   Port: {db.get('PORT', 'N/A')}")
    print(f"   User: {db.get('USER', 'N/A')}")
    print()


def run_migrations():
    """Run all pending migrations."""
    print("\n🔄 Running migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--verbosity', '2'])
        print("\n✅ Migrations completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        return False


def show_tables():
    """Show all tables in the database."""
    try:
        with connection.cursor() as cursor:
            if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """)
            else:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            
            tables = cursor.fetchall()
            if tables:
                print("\n📋 Database Tables:")
                for table in tables:
                    print(f"   - {table[0]}")
            else:
                print("\n⚠️  No tables found in database.")
    except Exception as e:
        print(f"\n❌ Error listing tables: {e}")


def main():
    """Main function."""
    print("=" * 60)
    print("🚀 CuratorAI PostgreSQL Setup")
    print("=" * 60)
    
    show_database_info()
    
    # Check connection
    if not check_database_connection():
        print("\n⚠️  Please configure your database connection first.")
        print("\n📝 To configure PostgreSQL, set these environment variables:")
        print("   - DATABASE_URL (recommended): postgresql://user:password@host:port/dbname")
        print("   OR set individually:")
        print("   - DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT")
        print("\n💡 Example DATABASE_URL:")
        print("   postgresql://curator_user:your_password@localhost:5432/curator_db")
        return False
    
    # Run migrations
    if not run_migrations():
        return False
    
    # Show tables
    show_tables()
    
    print("\n" + "=" * 60)
    print("✅ Setup complete! Your database is ready.")
    print("=" * 60)
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

