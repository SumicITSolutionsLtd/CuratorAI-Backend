# Vercel Deployment Setup Guide

## Current Status

✅ **Build is working!** The deployment succeeds and static files are collected.

❌ **Runtime Issues:**
- Admin panel returns 500 error
- API endpoints return 500 error
- Database not configured

## Issues Fixed

1. ✅ **GitHub Workflow** - Updated Python versions from 3.7/3.8/3.9 to 3.11/3.12
2. ✅ **Build Process** - Static files now collect to correct directory
3. ✅ **Database Configuration** - Settings updated for Vercel environment

## Required Setup Steps

### 1. Set Up Database

**Option A: Use Vercel Postgres (Recommended)**
1. Go to Vercel Dashboard → Your Project → Storage
2. Click "Create Database" → Select "Postgres"
3. Copy the `POSTGRES_URL` connection string
4. Add it as `DATABASE_URL` environment variable in Vercel

**Option B: Use External PostgreSQL**
1. Set up PostgreSQL database (e.g., Supabase, Railway, Neon)
2. Get connection string (format: `postgresql://user:password@host:port/dbname`)
3. Add as `DATABASE_URL` environment variable in Vercel

**Option C: Use SQLite (Not Recommended for Production)**
- SQLite will work but data resets on each deployment
- Only use for testing

### 2. Set Environment Variables in Vercel

Go to: **Vercel Dashboard → Your Project → Settings → Environment Variables**

Add these variables:

```bash
# Required
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=curator.settings.production
DJANGO_ENVIRONMENT=production
DJANGO_DEBUG=False
ALLOWED_HOSTS=curator-ai-backend.vercel.app,*.vercel.app

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://user:password@host:port/dbname

# Admin User (optional - for auto-creation)
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@curator.ai
ADMIN_PASSWORD=your-secure-password-here
```

### 3. Run Migrations

After setting `DATABASE_URL`, you need to run migrations. Options:

**Option A: Using Vercel CLI (Recommended)**
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Link to your project
vercel link

# Pull environment variables
vercel env pull .env.local

# Run migrations locally (will connect to Vercel database)
python manage.py migrate --settings=curator.settings.production

# Create admin user
python manage.py createsuperuser --settings=curator.settings.production
```

**Option B: Using Setup Script**
```bash
# Pull environment variables
vercel env pull .env.local

# Run setup script
python scripts/setup_vercel_db.py
```

**Option C: Using Django Shell via Vercel CLI**
```bash
vercel env pull .env.local
python manage.py shell --settings=curator.settings.production
```

Then in the shell:
```python
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', 'admin@curator.ai', 'your-password')
```

### 4. Verify Setup

1. **Check Admin Panel:**
   - Visit: `https://curator-ai-backend.vercel.app/admin/`
   - Should show login page (not 500 error)
   - Login with admin credentials

2. **Check API:**
   - Visit: `https://curator-ai-backend.vercel.app/api/schema/swagger-ui/`
   - Should show Swagger UI
   - Test an endpoint

3. **Check Runtime Logs:**
   - Go to Vercel Dashboard → Your Project → Logs
   - Look for any errors

## Troubleshooting

### 500 Error on Admin Panel

**Cause:** Database not configured or migrations not run

**Solution:**
1. Check if `DATABASE_URL` is set in Vercel environment variables
2. Run migrations (see Step 3 above)
3. Check runtime logs for specific error messages

### Database Connection Errors

**Check:**
1. `DATABASE_URL` format is correct
2. Database is accessible from Vercel's IP ranges
3. Database credentials are correct

### Admin User Not Created

**Solution:**
1. Use `python manage.py createsuperuser` locally with Vercel env vars
2. Or use the setup script: `python scripts/setup_vercel_db.py`
3. Or create via Django shell

## Current Database Status

Based on your production settings:
- If `DATABASE_URL` is set → Uses PostgreSQL
- If `DATABASE_URL` is NOT set → Uses SQLite at `/tmp/db.sqlite3` (ephemeral)

**⚠️ Important:** SQLite on Vercel is ephemeral - data resets on each deployment. Use PostgreSQL for production!

## Next Steps

1. ✅ Set up PostgreSQL database (Vercel Postgres or external)
2. ✅ Add `DATABASE_URL` to Vercel environment variables
3. ✅ Run migrations
4. ✅ Create admin user
5. ✅ Test admin panel and API endpoints

## Admin Credentials

**Default (if using setup script without ADMIN_PASSWORD):**
- Username: `admin`
- Email: `admin@curator.ai`
- Password: `admin123` ⚠️ **CHANGE THIS IMMEDIATELY!**

**Custom:**
Set `ADMIN_USERNAME`, `ADMIN_EMAIL`, and `ADMIN_PASSWORD` environment variables before running setup script.

