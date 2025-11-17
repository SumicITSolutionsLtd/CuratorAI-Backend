# 🔧 Adding DATABASE_URL to Vercel

## Quick Steps

### 1. Get Your Database URL

You mentioned you have a Neon database. The connection string should look like:
```
postgresql://neondb_owner:password@ep-wandering-smoke-ah247j6v-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### 2. Add to Vercel Dashboard

1. Go to: https://vercel.com/dashboard
2. Select your project: `curator-ai-backend` (or `backend`)
3. Go to: **Settings** → **Environment Variables**
4. Click: **Add New**
5. Add:
   - **Name**: `DATABASE_URL`
   - **Value**: Your full PostgreSQL connection string
   - **Environments**: Select **Production**, **Preview**, and **Development**
6. Click: **Save**

### 3. Pull Environment Variables Again

```bash
vercel env pull .env.local --environment=production
```

### 4. Verify DATABASE_URL is Set

```bash
# Windows (CMD)
type .env.local | findstr DATABASE_URL

# Windows (PowerShell)  
Select-String -Path .env.local -Pattern "DATABASE_URL"
```

---

## Alternative: Add Manually to .env.local (Temporary)

If you want to test locally without adding to Vercel first:

1. Open `.env.local` in a text editor
2. Add this line:
   ```
   DATABASE_URL=postgresql://neondb_owner:your-password@ep-wandering-smoke-ah247j6v-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require
   ```
3. Replace `your-password` with your actual password

**Note:** This is only for local testing. You still need to add it to Vercel for production!

