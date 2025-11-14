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
from pathlib import Path

# Load environment variables from .env.local if it exists
env_file = Path(__file__).parent.parent / '.env.local'
if env_file.exists():
    print(f"Loading environment variables from {env_file}")
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                # Remove quotes if present
                value = value.strip('"').strip("'")
                os.environ[key.strip()] = value

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
    
    # Check if DATABASE_URL is set
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("\n❌ ERROR: DATABASE_URL not found in environment variables!")
        print("   Make sure you've run: vercel env pull .env.local")
        print("   And that .env.local file exists in the project root.")
        return False
    
    # Mask password in output
    if '@' in database_url:
        masked_url = database_url.split('@')[0].split(':')[:-1]
        masked_url.append('***')
        masked_url.append('@' + database_url.split('@')[1])
        print(f"\n✓ DATABASE_URL found: {'@'.join(masked_url)}")
    else:
        print(f"\n✓ DATABASE_URL found")
    
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

