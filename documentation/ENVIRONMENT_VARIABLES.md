# ⚙️ Environment Variables Configuration

**Complete guide for configuring environment variables in Vercel**

---

## 🔐 Required Environment Variables for Vercel

### How to Add Environment Variables:

1. Go to **Vercel Dashboard**: https://vercel.com/dashboard
2. Select project: `curator-ai-backend`
3. Go to **Settings** → **Environment Variables**
4. Add each variable below
5. Select environments: **Production, Preview, Development**
6. Click **Save**
7. **Redeploy** for changes to take effect

---

## 📋 Minimum Required Variables

**These 4 variables are REQUIRED to make it work:**

```bash
1. DJANGO_SECRET_KEY=your-secret-key-here
2. DJANGO_SETTINGS_MODULE=curator.settings.production
3. DJANGO_DEBUG=False
4. ALLOWED_HOSTS=curator-ai-backend.vercel.app,*.vercel.app
```

---

## 📝 All Environment Variables

### 1. Django Core Settings (REQUIRED)

```bash
# Django Secret Key
DJANGO_SECRET_KEY=your-super-secret-key-change-this-to-random-50-chars

# Django Settings Module
DJANGO_SETTINGS_MODULE=curator.settings.production

# Debug Mode (False for production)
DJANGO_DEBUG=False
```

**Generate Secret Key:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Allowed Hosts (REQUIRED)

```bash
# Add your Vercel domain
ALLOWED_HOSTS=curator-ai-backend.vercel.app,*.vercel.app,localhost,127.0.0.1
```

### 3. Database Configuration (Optional but Recommended)

```bash
# PostgreSQL Database URL (Recommended for production)
DATABASE_URL=postgresql://username:password@host:5432/database_name

# If not set, will use SQLite (ephemeral on Vercel)
```

**Options for PostgreSQL:**
- **Neon:** https://neon.tech (free tier)
- **Supabase:** https://supabase.com (free tier)
- **Railway:** https://railway.app (free tier)
- **Vercel Postgres:** Built-in

### 4. CORS Configuration (REQUIRED for Frontend)

```bash
# Allow all origins (for testing)
CORS_ALLOW_ALL_ORIGINS=True

# Or specify specific origins (recommended for production)
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
```

### 5. JWT Token Settings (Optional)

```bash
# JWT Access Token Lifetime (in minutes)
JWT_ACCESS_TOKEN_LIFETIME=15

# JWT Refresh Token Lifetime (in minutes - 7 days = 10080)
JWT_REFRESH_TOKEN_LIFETIME=10080
```

### 6. Email Configuration (Optional)

```bash
# Email Backend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
```

**For Gmail:**
1. Enable 2-factor authentication
2. Generate app-specific password
3. Use that password (not your regular password)

### 7. AWS S3 Configuration (Optional - for file uploads)

```bash
# AWS Credentials
USE_S3=True
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

---

## 🔄 After Adding Variables

### IMPORTANT: Redeploy!

Environment variables are only applied on deploy. After adding variables:

**Option 1: Redeploy via Dashboard**
1. Go to Vercel Dashboard → Deployments
2. Click on latest deployment
3. Click "Redeploy"

**Option 2: Redeploy via Git Push**
```bash
git commit --allow-empty -m "Trigger redeploy"
git push
```

---

## ✅ Verify Environment Variables

### Check if variables are set:

1. Go to Vercel Dashboard → Settings → Environment Variables
2. You should see all variables listed
3. They should show as "Set" (value hidden for security)

### Test in deployment:

Visit: https://curator-ai-backend.vercel.app/

**Should show:**
```json
{
  "message": "Welcome to CuratorAI API",
  "status": "operational"
}
```

**NOT 404 error!**

---

## 📝 Complete Example

Here's a complete working configuration:

```bash
# Core Django Settings
DJANGO_SECRET_KEY=django-insecure-w+jb#3g8&d%2v@x5n*e7f-h+j=k9m2p4q6r8s0t1u3v5w7y9
DJANGO_SETTINGS_MODULE=curator.settings.production
DJANGO_DEBUG=False
ALLOWED_HOSTS=curator-ai-backend.vercel.app,*.vercel.app

# CORS for Frontend
CORS_ALLOWED_ORIGINS=https://curator-ai-frontend.vercel.app,http://localhost:3000

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=15
JWT_REFRESH_TOKEN_LIFETIME=10080

# Database (using Neon free tier)
DATABASE_URL=postgresql://user:pass@host.neon.tech/curatorai?sslmode=require
```

---

**After configuring these variables, your 404 error will be fixed!** ✅

---

**Last Updated:** October 29, 2025

