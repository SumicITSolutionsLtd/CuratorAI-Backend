# 🚀 Vercel Deployment Guide for CuratorAI Backend

**Complete guide to deploy Django backend on Vercel**  
**Date:** October 29, 2025  
**Status:** Production Ready

---

## 📋 Table of Contents

1. [Why You Got 404 Error](#why-you-got-404-error)
2. [Vercel Configuration Files](#vercel-configuration-files)
3. [Environment Variables Setup](#environment-variables-setup)
4. [Deployment Steps](#deployment-steps)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

---

## ❌ Why You Got 404 Error

### The Problem

Unlike Laravel (which uses `.htaccess`), **Django on Vercel requires specific configuration files** to work properly.

**What was missing:**
- ✅ `vercel.json` - Tells Vercel how to deploy Django
- ✅ `build_files.sh` - Build script for dependencies
- ✅ Root URL route - Django had no route at `/`
- ✅ Proper WSGI configuration for serverless

**Now fixed!** All necessary files have been created.

---

## 📁 Vercel Configuration Files

### 1. `vercel.json`

Located at: `backend/vercel.json`

This tells Vercel how to deploy your Django app.

### 2. `build_files.sh`

Located at: `backend/build_files.sh`

**What it does:**
- Installs Python dependencies
- Collects static files
- Runs database migrations

### 3. `requirements.txt`

Located at: `backend/requirements.txt`

Links to your production requirements.

---

## 🔐 Environment Variables Setup

### Required Environment Variables

You need to configure these in **Vercel Dashboard → Settings → Environment Variables**:

#### 1. **Django Secret Key** (REQUIRED)
```
DJANGO_SECRET_KEY=your-super-secret-key-here-change-this-in-production
```

Generate a new one:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 2. **Django Settings Module** (REQUIRED)
```
DJANGO_SETTINGS_MODULE=curator.settings.production
```

#### 3. **Debug Mode** (REQUIRED - Set to False for production)
```
DJANGO_DEBUG=False
```

#### 4. **Allowed Hosts** (REQUIRED)
```
ALLOWED_HOSTS=curator-ai-backend.vercel.app,*.vercel.app
```

#### 5. **Database URL** (Optional - for PostgreSQL)
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

If you don't set this, it will use SQLite (ephemeral on Vercel).

#### 6. **CORS Origins** (For frontend)
```
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```
Or for testing:
```
CORS_ALLOW_ALL_ORIGINS=True
```

#### 7. **JWT Settings** (Optional)
```
JWT_ACCESS_TOKEN_LIFETIME=15
JWT_REFRESH_TOKEN_LIFETIME=10080
```

---

## 🚀 Deployment Steps

### Step 1: Set Environment Variables in Vercel

1. Go to **Vercel Dashboard**: https://vercel.com/dashboard
2. Select your project: `curator-ai-backend`
3. Go to **Settings** → **Environment Variables**
4. Add the 4 REQUIRED variables above
5. Select "Production, Preview, Development" for each
6. Click **Save**

### Step 2: Push Code to GitHub

```bash
cd backend
git add .
git commit -m "Add Vercel configuration and fix 404 error"
git push origin main
```

**Vercel will auto-deploy!**

### Step 3: Wait for Deploy (2-3 minutes)

Watch in Vercel Dashboard → Deployments

---

## ✅ Testing

### 1. Test Root URL

```bash
curl https://curator-ai-backend.vercel.app/
```

**Expected Response:**
```json
{
  "message": "Welcome to CuratorAI API",
  "version": "1.0.0",
  "status": "operational",
  "documentation": {
    "swagger": "https://curator-ai-backend.vercel.app/api/schema/swagger-ui/"
  }
}
```

### 2. Test API Documentation

Visit in browser:
- **Swagger UI**: https://curator-ai-backend.vercel.app/api/schema/swagger-ui/
- **ReDoc**: https://curator-ai-backend.vercel.app/api/schema/redoc/

### 3. Test Authentication Endpoint

```bash
curl -X POST https://curator-ai-backend.vercel.app/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User"
  }'
```

---

## 🐛 Troubleshooting

### Issue 1: Still Getting 404

**Cause:** Environment variables not set

**Solution:**
1. Go to Vercel Dashboard → Settings → Environment Variables
2. Add `DJANGO_SETTINGS_MODULE=curator.settings.production`
3. Add `DJANGO_SECRET_KEY=your-secret-key`
4. Redeploy

### Issue 2: "Internal Server Error" (500)

**Cause:** Database migration not run or environment variables missing

**Solution:**
1. Check Vercel build logs (Dashboard → Deployments → View Function Logs)
2. Ensure `build_files.sh` ran successfully
3. Check environment variables are set correctly

### Issue 3: "Bad Request" (400)

**Cause:** ALLOWED_HOSTS not configured

**Solution:**
```
ALLOWED_HOSTS=curator-ai-backend.vercel.app,*.vercel.app
```

### Issue 4: CORS Errors

**Cause:** Frontend domain not in CORS_ALLOWED_ORIGINS

**Solution:**
```
CORS_ALLOWED_ORIGINS=https://your-frontend.com,http://localhost:3000
```

---

## 📊 Vercel Build Logs

### View Build Logs:

1. Go to Vercel Dashboard
2. Click on your project
3. Go to **Deployments**
4. Click on latest deployment
5. Click **View Function Logs**

### Common Log Messages:

✅ **Good:**
```
Installing dependencies...
Collecting static files...
Migrations complete
Build successful
```

❌ **Bad:**
```
ModuleNotFoundError: No module named 'apps.accounts'
```
**Solution:** Ensure `INSTALLED_APPS` includes all apps

---

## 🎯 Vercel Limitations to Know

### 1. **Ephemeral File System**
- Files uploaded during runtime are lost on next deploy
- **Solution:** Use AWS S3 or Cloudinary for media files

### 2. **10-Second Execution Limit**
- Functions timeout after 10 seconds (free tier)
- **Solution:** Upgrade to Pro for 60-second limit

### 3. **Database Persistence**
- SQLite database is ephemeral on Vercel
- **Solution:** Use PostgreSQL (Neon, Supabase, or Vercel Postgres)

---

## 🗄️ Recommended: Use PostgreSQL

For production, use a persistent database:

### Option 1: Neon (Free Tier)
1. Sign up at https://neon.tech
2. Create database
3. Copy connection string
4. Add to Vercel: `DATABASE_URL=postgresql://...`

### Option 2: Supabase (Free Tier)
1. Sign up at https://supabase.com
2. Create project
3. Copy PostgreSQL connection string
4. Add to Vercel environment variables

---

## 📝 Deployment Checklist

Before going live:

- [ ] Set `DEBUG=False`
- [ ] Set strong `DJANGO_SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up persistent database (PostgreSQL)
- [ ] Configure CORS for frontend domain
- [ ] Test all API endpoints
- [ ] Check Swagger documentation works

---

## ✅ Summary

**What was done:**
1. ✅ Created `vercel.json` configuration
2. ✅ Created `build_files.sh` build script
3. ✅ Updated `wsgi.py` for Vercel
4. ✅ Added root URL route (no more 404)
5. ✅ Updated production settings

**Next steps:**
1. Configure environment variables in Vercel Dashboard
2. Push code to GitHub (auto-deploys)
3. Test the API
4. Set up persistent PostgreSQL database (recommended)

---

**Your API will now work! 🎉**

**Last Updated:** October 29, 2025  
**Status:** Ready for Deployment

