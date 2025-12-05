# AWS Setup with Neon Database

This is a simplified setup guide since you're using Neon database (no RDS needed).

## Architecture

```
┌─────────────┐
│   Route 53  │ (curatorai.net)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ App Runner  │ (Django Backend)
└──────┬──────┘
       │
       ├──► Neon PostgreSQL (External)
       └──► S3 (Static/Media Files)
```

## What You Need

1. ✅ **ECR Repository** - For Docker images
2. ✅ **S3 Bucket** - For static/media files
3. ✅ **IAM Roles** - For App Runner permissions
4. ✅ **App Runner Service** - Your Django app
5. ❌ **RDS** - NOT needed (using Neon)

## Quick Setup

### Step 1: Create Infrastructure (Terraform)

```bash
cd infrastructure/terraform

# Use simplified Terraform (no RDS)
cp main-simplified.tf main.tf.backup
# main-simplified.tf is already configured for Neon

cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars:
# - aws_region = "us-east-1"
# - environment = "production"
# - bucket_name = "curatorai-static-media"

terraform init
terraform plan
terraform apply
```

**Save the outputs:**
- `s3_bucket_name`
- `s3_access_key_id`
- `s3_secret_access_key`
- `ecr_repository_url`
- `app_runner_role_arn`

### Step 2: Migrate Environment Variables

**Option A: Use Migration Script**

```bash
# Get Vercel env vars
vercel env pull .env.vercel

# Migrate to AWS format
# Windows:
scripts\migrate-env-to-aws.bat .env.vercel

# Linux/Mac:
chmod +x scripts/migrate-env-to-aws.sh
./scripts/migrate-env-to-aws.sh .env.vercel
```

**Option B: Manual Migration**

Copy from Vercel and update:

| Variable | Vercel | AWS |
|----------|--------|-----|
| `ALLOWED_HOSTS` | `curator-ai-backend.vercel.app,*.vercel.app` | `api.curatorai.net,curatorai.net` |
| `DATABASE_URL` | Your Neon URL | Same Neon URL |
| `CORS_ALLOWED_ORIGINS` | Your frontend URLs | Same + `https://curatorai.net` |
| `USE_S3` | Not set | `True` |
| `AWS_*` | Not set | From Terraform output |

### Step 3: Build and Push Docker Image

```bash
# Windows
scripts\deploy-to-aws.bat

# Linux/Mac
./scripts/deploy-to-aws.sh
```

### Step 4: Create App Runner Service

1. Go to **AWS App Runner** console
2. Click **Create service**
3. Configure:
   - **Source:** ECR → `curator-backend:latest`
   - **Service name:** `curator-backend`
   - **CPU:** 1 vCPU
   - **Memory:** 2 GB
   - **Port:** 8000
   - **Environment variables:** Copy from `.env.aws` (or use migration script output)
   - **Instance role:** `AppRunnerCuratorBackendRole`
4. Click **Create & deploy**

### Step 5: Configure Domain

1. App Runner → Custom domains → Add `api.curatorai.net`
2. Route 53 → Add CNAME:
   - Name: `api`
   - Value: `<app-runner-url>.awsapprunner.com`
3. Wait for SSL (5-10 min)

### Step 6: Setup GitHub Actions

1. **Add GitHub as Identity Provider (Required First):** 
   
   Go to IAM → Identity providers → Add provider:
   - **Provider type:** OpenID Connect
   - **Provider URL:** `https://token.actions.githubusercontent.com`
   - **Audience:** `sts.amazonaws.com`
   - Click **Add provider**

2. **Create IAM Role for GitHub:**
   
   Go to IAM → Roles → Create role:
   - **Trusted entity type:** Web identity
   - **Identity provider:** Select **GitHub** (from Step 1)
   - **Audience:** `sts.amazonaws.com`
   
   **Add conditions:**
   - Condition 1: `StringEquals` → `token.actions.githubusercontent.com:aud` = `sts.amazonaws.com`
   - Condition 2: `StringLike` → `token.actions.githubusercontent.com:sub` = `repo:YOUR_USERNAME/YOUR_REPO:*`
     (Replace `YOUR_USERNAME` and `YOUR_REPO` with your actual GitHub username and repository name)
   
   **Attach policies:**
   - `AmazonEC2ContainerRegistryFullAccess`
   - `AppRunnerFullAccess`
   
   **Name:** `GitHubActionsDeployRole`
   - **Copy the Role ARN** (you'll need it for GitHub Secrets)

3. **Add GitHub Secrets:**
   
   Go to GitHub → Repository → Settings → Secrets and variables → Actions
   
   Add secrets:
   - `AWS_ROLE_ARN`: Your IAM role ARN (from Step 2)
   - `AWS_REGION`: `us-east-1`

4. **Test:**
   ```bash
   git push origin main
   ```
   
   Check GitHub Actions tab for deployment status.

## Environment Variables Template

```bash
# Django Core
DJANGO_SECRET_KEY=<from-vercel>
DJANGO_SETTINGS_MODULE=curator.settings.production
DJANGO_DEBUG=False
ALLOWED_HOSTS=api.curatorai.net,curatorai.net,localhost,127.0.0.1

# Database (Neon - same as Vercel)
DATABASE_URL=<your-neon-url>

# CORS
CORS_ALLOWED_ORIGINS=https://curatorai.net,https://www.curatorai.net,http://localhost:3000
CORS_ALLOW_ALL_ORIGINS=False

# JWT
JWT_ACCESS_TOKEN_LIFETIME=15
JWT_REFRESH_TOKEN_LIFETIME=10080

# Google OAuth
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret

# AWS S3 (from Terraform)
USE_S3=True
AWS_STORAGE_BUCKET_NAME=<terraform-output>
AWS_S3_REGION_NAME=us-east-1
AWS_ACCESS_KEY_ID=<terraform-output>
AWS_SECRET_ACCESS_KEY=<terraform-output>

# Email (if you have it)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=<your-email>
EMAIL_HOST_PASSWORD=<your-password>
```

## Cost Estimate

**Monthly:**
- App Runner: ~$25-50
- S3: ~$0.25
- Route 53: ~$0.50
- **Total: ~$26-51/month**

**No RDS costs** (using Neon free tier)

## Troubleshooting

### Database Connection

Neon should work from AWS App Runner. If issues:
1. Check Neon dashboard → Connection settings
2. Verify `DATABASE_URL` format
3. Ensure Neon allows connections from AWS IPs

### S3 Access

1. Verify IAM role has S3 permissions
2. Check S3 bucket policy
3. Verify access keys from Terraform output

## Next Steps

1. ✅ Complete setup
2. ✅ Test API endpoints
3. ✅ Update frontend URLs
4. ✅ Monitor for 24 hours
5. ✅ Decommission Vercel (optional)

