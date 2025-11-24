# 🚨 Vercel Production Issues - Quick Fix Guide

**Issues:** 400 Bad Request, 500 errors, CORS not enabled

---

## ⚡ Quick Fix (5 minutes)

### Step 1: Go to Vercel Dashboard

1. Visit: https://vercel.com/dashboard
2. Select your project: `backend` (or `curator-ai-backend`)
3. Go to: **Settings** → **Environment Variables**

### Step 2: Add These REQUIRED Environment Variables

**Copy and paste these EXACTLY into Vercel:**

```bash
DJANGO_SECRET_KEY=django-insecure-replace-this-with-a-random-50-character-string
DJANGO_SETTINGS_MODULE=curator.settings.production
DJANGO_DEBUG=False
CORS_ALLOW_ALL_ORIGINS=True
```

**⚠️ IMPORTANT:** Generate a real secret key! Run this locally:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and use it as `DJANGO_SECRET_KEY`.

### Step 3: Add Optional (But Recommended) Variables

```bash
ALLOWED_HOSTS=backend-zeta-henna-62.vercel.app,*.vercel.app
CORS_ALLOWED_ORIGINS=https://curator-ai-phi.vercel.app
```

**Note:** `ALLOWED_HOSTS` is optional because the code now uses `VERCEL_URL` automatically. But if you want to be explicit, add your actual backend domain.

### Step 4: Select Environments

For each variable:
- ✅ Check **Production**
- ✅ Check **Preview**  
- ✅ Check **Development**

### Step 5: Save and Redeploy

1. Click **Save** for each variable
2. Go to **Deployments** tab
3. Click **⋯** (three dots) on latest deployment
4. Click **Redeploy**

**Wait 2-3 minutes for deployment to complete.**

---

## ✅ Verify It Works

### Test 1: Root Endpoint

```bash
curl https://backend-zeta-henna-62.vercel.app/
```

**Expected:** JSON response (not 400 error)

### Test 2: Admin Panel

Visit: `https://backend-zeta-henna-62.vercel.app/admin/`

**Expected:** Login page (not 500 error)

### Test 3: CORS (from Frontend)

The frontend at `https://curator-ai-phi.vercel.app/` should now be able to make API requests without CORS errors.

---

## 🐛 If Still Getting Errors

### Error: Still 400 Bad Request

**Cause:** `DJANGO_SECRET_KEY` not set or invalid

**Fix:**
1. Generate a new secret key (see Step 2 above)
2. Update `DJANGO_SECRET_KEY` in Vercel
3. Redeploy

### Error: Still 500 on Admin

**Cause:** Database not migrated

**Fix:** This is expected on Vercel if you're using SQLite (ephemeral). For production, you need:
1. Set up PostgreSQL database (Neon, Supabase, etc.)
2. Add `DATABASE_URL` environment variable
3. Run migrations (Vercel will do this automatically if configured)

### Error: CORS Still Not Working

**Cause:** `CORS_ALLOW_ALL_ORIGINS` not set to `True`

**Fix:**
1. Double-check `CORS_ALLOW_ALL_ORIGINS=True` is set in Vercel
2. Make sure you selected all environments (Production, Preview, Development)
3. Redeploy

---

## 📋 Complete Environment Variables List

For reference, here are ALL possible environment variables:

```bash
# REQUIRED (Minimum 4 variables)
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=curator.settings.production
DJANGO_DEBUG=False
CORS_ALLOW_ALL_ORIGINS=True

# OPTIONAL (But Recommended)
ALLOWED_HOSTS=backend-zeta-henna-62.vercel.app
CORS_ALLOWED_ORIGINS=https://curator-ai-phi.vercel.app
DATABASE_URL=postgresql://user:pass@host:5432/dbname
JWT_ACCESS_TOKEN_LIFETIME=15
JWT_REFRESH_TOKEN_LIFETIME=10080
```

---

## 🎯 Summary

**The 3 main issues were:**

1. ❌ **Missing `DJANGO_SECRET_KEY`** → Causes 400 Bad Request
2. ❌ **CORS not enabled** → Frontend can't make requests
3. ❌ **ALLOWED_HOSTS mismatch** → Fixed by using VERCEL_URL automatically

**The fix:**
- ✅ Set `DJANGO_SECRET_KEY` (REQUIRED)
- ✅ Set `CORS_ALLOW_ALL_ORIGINS=True` (REQUIRED)
- ✅ Code now handles Vercel domains automatically

---

**Last Updated:** November 24, 2025

