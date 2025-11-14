#!/usr/bin/env python
"""
Script to set up database on Vercel (run migrations and create admin user).
This can be run locally using Vercel CLI or as a one-time setup script.

Usage:
    vercel env pull .env.local
    python scripts/setup_vercel_db.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'curator.settings.production')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model

User = get_user_model()

def main():
    print("=" * 60)
    print("Setting up Vercel Database")
    print("=" * 60)
    
    # Run migrations
    print("\n1. Running migrations...")
    try:
        call_command('migrate', verbosity=2, interactive=False)
        print("✅ Migrations completed successfully!")
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False
    
    # Check if admin user exists
    print("\n2. Checking for admin user...")
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@curator.ai')
    admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
    
    if User.objects.filter(username=admin_username).exists():
        print(f"✅ Admin user '{admin_username}' already exists!")
        return True
    
    # Create admin user
    print(f"\n3. Creating admin user '{admin_username}'...")
    admin_password = os.environ.get('ADMIN_PASSWORD')
    
    if not admin_password:
        print("⚠️  ADMIN_PASSWORD not set in environment variables.")
        print("   Creating admin user with default password: 'admin123'")
        print("   ⚠️  CHANGE THIS PASSWORD IMMEDIATELY!")
        admin_password = 'admin123'
    
    try:
        User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password
        )
        print(f"✅ Admin user '{admin_username}' created successfully!")
        print(f"   Email: {admin_email}")
        print(f"   Username: {admin_username}")
        if admin_password == 'admin123':
            print(f"   Password: {admin_password} (CHANGE THIS!)")
        else:
            print(f"   Password: [Set via ADMIN_PASSWORD]")
        return True
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

