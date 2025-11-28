# Migrating Production Database

This guide explains how to add the missing `lookbooks` and `wardrobe` tables to your existing production database.

## Overview

Your production database already exists with data, but the `lookbooks` and `wardrobes` tables are missing. This is because these apps were added later and their migrations haven't been run on production yet.

## Quick Fix

### Option 1: Using the Migration Script (Recommended)

```bash
# Make sure you're in the project directory
cd D:\Projects\OnGoing\Sumic\Curator\curator-backend

# Activate virtual environment
venv\Scripts\activate.bat

# Set production database URL (if not already set)
set DATABASE_URL=your_production_postgres_url

# Run the migration script
python scripts/migrate_production.py
```

### Option 2: Using Django Management Command

```bash
# Activate virtual environment
venv\Scripts\activate.bat

# Set production database URL
set DATABASE_URL=your_production_postgres_url

# Run migrations for specific apps
python manage.py migrate lookbooks wardrobe
```

### Option 3: For Vercel/Cloud Deployment

If you're deploying on Vercel or another cloud platform:

1. **Set DATABASE_URL in your platform's environment variables** (if not already set)

2. **Run migrations via Vercel CLI:**
   ```bash
   vercel env pull .env.local
   python manage.py migrate lookbooks wardrobe
   ```

3. **Or add a migration step to your build process** (see below)

## What Will Happen

The migrations will:
- ✅ Create the `lookbooks` table
- ✅ Create the `lookbook_outfits` table  
- ✅ Create the `lookbook_likes` table
- ✅ Create the `wardrobes` table
- ✅ Create the `wardrobe_items` table
- ✅ Create related tables (wardrobe_item_images, wardrobe_item_attributes, etc.)
- ✅ Create indexes for performance
- ✅ **NOT affect any existing data**

## Verification

After running migrations, verify the tables exist:

```bash
python manage.py dbshell
```

Then in PostgreSQL:
```sql
\dt lookbooks*
\dt wardrobe*
\q
```

Or use the migration script which will automatically verify.

## Troubleshooting

### Error: "relation already exists"

This means the tables already exist. You can safely ignore this or check if migrations were already applied:

```bash
python manage.py showmigrations lookbooks wardrobe
```

### Error: "could not connect to server"

1. Verify your `DATABASE_URL` is set correctly
2. Check that your production database is accessible
3. For cloud databases, ensure your IP is whitelisted (if required)

### Error: "permission denied"

Ensure your database user has CREATE TABLE permissions:

```sql
GRANT CREATE ON DATABASE your_db_name TO your_user;
```

### Error: "django.db.utils.ProgrammingError"

This usually means there's a conflict. Check:
1. Are migrations already partially applied?
2. Is there a schema mismatch?

You can check migration status:
```bash
python manage.py showmigrations
```

## For Vercel Deployments

### Automatic Migration on Deploy

Add this to your `vercel.json`:

```json
{
  "buildCommand": "python manage.py migrate && python manage.py collectstatic --noinput"
}
```

### Manual Migration via Vercel CLI

```bash
# Pull environment variables
vercel env pull .env.local

# Run migrations locally against production DB
python manage.py migrate lookbooks wardrobe

# Or use the script
python scripts/migrate_production.py
```

## Safety Notes

⚠️ **Important:**
- These migrations only CREATE tables - they don't modify existing data
- Always backup your database before running migrations (best practice)
- Test migrations on a staging environment first if possible
- The migrations are idempotent - safe to run multiple times

## After Migration

Once migrations are complete:

1. ✅ Test the endpoints:
   - `GET /api/v1/lookbooks/` should work
   - `GET /api/v1/wardrobe/items/` should work

2. ✅ Verify in test dashboard:
   - Try testing the lookbooks and wardrobe endpoints
   - They should return empty lists (no data yet) instead of 500 errors

3. ✅ Optional: Load sample data:
   ```bash
   python manage.py seed_data  # If you have a seed command
   ```

## Need Help?

If you encounter issues:
1. Check the error message in the test dashboard (it will show detailed tracebacks)
2. Verify database connection: `python scripts/migrate_production.py`
3. Check migration status: `python manage.py showmigrations`

