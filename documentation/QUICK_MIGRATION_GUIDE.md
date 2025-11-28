# Quick Migration Guide - Fix Missing Tables

Your production database exists but is missing `lookbooks` and `wardrobes` tables. Here's how to fix it:

## 🚀 Quick Fix (Choose One Method)

### Method 1: Run Locally Against Production DB (Fastest)

```bash
# 1. Activate virtual environment
venv\Scripts\activate.bat

# 2. Get your production DATABASE_URL from Vercel
#    Go to: Vercel Dashboard → Your Project → Settings → Environment Variables
#    Copy the DATABASE_URL value

# 3. Set it temporarily (Windows CMD)
set DATABASE_URL=your_production_database_url_here

# 4. Run migrations
python manage.py migrate lookbooks wardrobe

# 5. Verify it worked
python manage.py showmigrations lookbooks wardrobe
```

### Method 2: Use the Migration Script

```bash
# 1. Activate virtual environment
venv\Scripts\activate.bat

# 2. Set DATABASE_URL
set DATABASE_URL=your_production_database_url_here

# 3. Run the script (it will check and migrate automatically)
python scripts/migrate_production.py
```

### Method 3: Via Vercel CLI

```bash
# 1. Install Vercel CLI if not installed
npm i -g vercel

# 2. Login to Vercel
vercel login

# 3. Link your project
vercel link

# 4. Pull environment variables
vercel env pull .env.local

# 5. Run migrations
python manage.py migrate lookbooks wardrobe
```

## ✅ What Gets Created

- `lookbooks` table
- `lookbook_outfits` table
- `lookbook_likes` table
- `wardrobes` table
- `wardrobe_items` table
- `wardrobe_item_images` table
- `wardrobe_item_attributes` table
- `wardrobe_item_wear_logs` table
- All necessary indexes

## 🔍 Verify It Worked

After running migrations, test the endpoints:

1. Go to your test dashboard: `https://your-app.vercel.app/test-dashboard/`
2. Test `GET /api/v1/lookbooks/` - should return `[]` (empty list) instead of 500 error
3. Test `GET /api/v1/wardrobe/items/` - should return `[]` instead of 500 error

## ⚠️ Important Notes

- ✅ **Safe**: These migrations only CREATE tables, they don't modify existing data
- ✅ **Idempotent**: Safe to run multiple times
- ✅ **No downtime**: Won't affect existing endpoints
- ⚠️ **Backup first**: Always good practice (though not required for CREATE TABLE)

## 🐛 Troubleshooting

**Error: "could not connect"**
- Check DATABASE_URL is correct
- Ensure database is accessible from your IP

**Error: "relation already exists"**
- Tables already exist, you're good! ✅

**Error: "permission denied"**
- Database user needs CREATE TABLE permission

## 📝 Next Steps

After migrations complete:
1. Test endpoints in the dashboard
2. The 500 errors should be gone
3. You can start adding data to lookbooks and wardrobe

