# 🌱 Seeding Production Database

Guide for seeding your production database on Vercel with sample data.

---

## 📋 Prerequisites

1. ✅ **Migrations completed** - Database tables must exist
2. ✅ **Vercel CLI installed** - For accessing production environment
3. ✅ **Database connected** - `DATABASE_URL` set in Vercel

---

## 🚀 Step-by-Step Guide

### Step 1: Install Vercel CLI (if not already installed)

```bash
npm i -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

### Step 3: Link to Your Project

```bash
vercel link
```

When prompted:
- **Set up this directory?** → `yes`
- **Which scope?** → Select your organization
- **Link to existing project?** → `yes`
- **What's your project's name?** → `curator-ai-backend` (or your project name)

### Step 4: Pull Production Environment Variables

```bash
vercel env pull .env.local
```

This downloads all environment variables from Vercel to `.env.local`.

### Step 5: Verify Database Connection

Check that `DATABASE_URL` is in your `.env.local`:

```bash
# Windows (CMD)
type .env.local | findstr DATABASE_URL

# Windows (PowerShell)
Select-String -Path .env.local -Pattern "DATABASE_URL"

# Linux/Mac
grep DATABASE_URL .env.local
```

### Step 6: Run Migrations (if not already done)

```bash
python manage.py migrate --settings=curator.settings.production
```

**Note:** This connects to your production database using credentials from `.env.local`.

### Step 7: Seed Production Database

**Option A: Seed with default amounts (20 users, 50 outfits)**
```bash
python manage.py seed_data --settings=curator.settings.production
```

**Option B: Seed with custom amounts**
```bash
python manage.py seed_data --users 50 --outfits 100 --settings=curator.settings.production
```

**Option C: Clear existing data first, then seed**
```bash
python manage.py seed_data --clear --users 50 --outfits 100 --settings=curator.settings.production
```

---

## ⚠️ Important Warnings

### ⚠️ **Production Data Warning**

- **`--clear` flag will DELETE all non-admin users and their data!**
- This includes:
  - All user accounts (except superusers)
  - All outfits
  - All user profiles
  - All social interactions (likes, saves, follows)

**Only use `--clear` if you want to start fresh!**

### ⚠️ **Admin Users**

- Admin/superuser accounts are **NOT deleted** by the `--clear` flag
- Your admin credentials remain safe

---

## 📊 What Gets Seeded

### Users (20 by default, or custom amount)
- Realistic names and emails
- User profiles with:
  - Location (city, country)
  - Body measurements
  - Clothing sizes
- Style preferences:
  - Preferred styles (minimalist, boho, etc.)
  - Preferred colors
  - Preferred brands
  - Budget ranges
- Following relationships (3-8 follows per user)

### Outfits (50 by default, or custom amount)
- Various outfit types:
  - Summer Brunch Look
  - Office Power Suit
  - Weekend Casual Vibes
  - Evening Elegance
  - Athleisure Chic
  - Date Night Ready
  - Travel Comfort
  - Boho Festival
  - Minimalist Monochrome
  - Streetwear Edge
- Outfit items with:
  - Brands (Zara, H&M, COS, etc.)
  - Prices
  - Purchase links
  - Sizes and colors

### Social Interactions
- Likes on outfits (0-50% of users per outfit)
- Saves to collections (0-30% of users per outfit)
- View counts (50-5000 per outfit)

---

## 🔍 Verify Seeding

### Check via Django Shell

```bash
python manage.py shell --settings=curator.settings.production
```

Then in the shell:
```python
from apps.accounts.models import User
from apps.outfits.models import Outfit

# Count users (excluding superusers)
print(f"Users: {User.objects.filter(is_superuser=False).count()}")

# Count outfits
print(f"Outfits: {Outfit.objects.count()}")

# Check a sample user
user = User.objects.filter(is_superuser=False).first()
if user:
    print(f"Sample user: {user.email}")
    print(f"  Profile: {hasattr(user, 'userprofile')}")
    print(f"  Style preferences: {hasattr(user, 'stylepreference')}")
    print(f"  Outfits: {user.outfit_set.count()}")
```

### Check via API

Visit your production API:
- **Swagger UI**: `https://curator-ai-backend.vercel.app/api/schema/swagger-ui/`
- **Users endpoint**: `https://curator-ai-backend.vercel.app/api/v1/auth/users/search/?q=`
- **Outfits endpoint**: `https://curator-ai-backend.vercel.app/api/v1/outfits/`

---

## 🛠️ Troubleshooting

### Error: "DATABASE_URL not found"

**Solution:**
```bash
# Make sure you've pulled environment variables
vercel env pull .env.local

# Verify the file exists and has DATABASE_URL
cat .env.local  # Linux/Mac
type .env.local  # Windows
```

### Error: "no such table: users"

**Solution:**
```bash
# Run migrations first
python manage.py migrate --settings=curator.settings.production
```

### Error: "UNIQUE constraint failed: users.email"

**Solution:**
- Users already exist. Use `--clear` to remove them first, or
- The seeder will skip existing users automatically

### Error: Connection timeout

**Solution:**
- Check your `DATABASE_URL` is correct
- Verify your database is accessible
- Check if your IP is whitelisted (for some database providers)

---

## 📝 Example Workflow

```bash
# 1. Pull environment variables
vercel env pull .env.local

# 2. Run migrations (if needed)
python manage.py migrate --settings=curator.settings.production

# 3. Seed with 50 users and 100 outfits
python manage.py seed_data --users 50 --outfits 100 --settings=curator.settings.production

# 4. Verify
python manage.py shell --settings=curator.settings.production
# Then run the Python commands above
```

---

## 🔄 Re-seeding

If you want to re-seed with fresh data:

```bash
# Clear and re-seed
python manage.py seed_data --clear --users 50 --outfits 100 --settings=curator.settings.production
```

**Warning:** This deletes all existing non-admin users and their data!

---

## ✅ Success Indicators

You'll know seeding worked when you see:

```
Starting database seeding...
Created 50 users
Created 100 outfits
Created social interactions
✅ Database seeding completed successfully!
```

---

## 📚 Related Commands

```bash
# Check migration status
python manage.py showmigrations --settings=curator.settings.production

# Create superuser (if needed)
python manage.py createsuperuser --settings=curator.settings.production

# Access Django shell
python manage.py shell --settings=curator.settings.production
```

---

**Need help?** Check the main setup guide or API documentation.

