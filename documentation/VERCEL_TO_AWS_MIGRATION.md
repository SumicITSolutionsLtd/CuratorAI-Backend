# Vercel to AWS Migration Guide

This guide helps you migrate your CuratorAI backend from Vercel to AWS App Runner.

## Prerequisites

- ✅ AWS Account with admin access
- ✅ Domain `curatorai.net` in Route 53
- ✅ Neon PostgreSQL database (already have)
- ✅ AWS CLI installed and configured
- ✅ Docker installed

## Quick Migration Steps

### Step 1: Export Vercel Environment Variables

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Copy all your environment variables
3. Or use Vercel CLI:
   ```bash
   vercel env pull .env.vercel
   ```

### Step 2: Create AWS Infrastructure

**Using Terraform (Recommended):**

```bash
cd infrastructure/terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
terraform init
terraform plan
terraform apply
```

This creates:
- ✅ ECR repository
- ✅ S3 bucket for static/media files
- ✅ IAM roles
- ✅ S3 access keys (save these!)

**What's NOT created:**
- ❌ RDS database (using Neon instead)

### Step 3: Prepare Environment Variables for AWS

Your Neon database URL should look like:
```
postgresql://user:password@ep-xxxxx.us-east-1.aws.neon.tech/neondb?sslmode=require
```

**Key changes from Vercel to AWS:**

| Vercel | AWS |
|--------|-----|
| `ALLOWED_HOSTS=curator-ai-backend.vercel.app,*.vercel.app` | `ALLOWED_HOSTS=api.curatorai.net,curatorai.net` |
| Same `DATABASE_URL` (Neon) | Same `DATABASE_URL` (Neon) |
| No S3 needed | `USE_S3=True` + S3 credentials |

### Step 4: Build and Push Docker Image

**Windows:**
```cmd
scripts\deploy-to-aws.bat
```

**Linux/Mac:**
```bash
chmod +x scripts/deploy-to-aws.sh
./scripts/deploy-to-aws.sh
```

### Step 5: Create App Runner Service

1. Go to **AWS App Runner** console
2. Click **Create service**
3. **Source:**
   - Source type: **Container registry**
   - Provider: **Amazon ECR**
   - Container image URI: Select `curator-backend:latest`
   - Deployment trigger: **Manual** (or **Automatic** after CI/CD setup)

4. **Service settings:**
   - Service name: `curator-backend`
   - Virtual CPU: **1 vCPU**
   - Memory: **2 GB**
   - Port: **8000**

5. **Environment variables:** Add all from your Vercel setup:
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
   
   # Google OAuth (from your .env)
   GOOGLE_OAUTH_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
   GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
   
   # AWS S3 (from Terraform output)
   USE_S3=True
   AWS_STORAGE_BUCKET_NAME=<from-terraform-output>
   AWS_S3_REGION_NAME=us-east-1
   AWS_ACCESS_KEY_ID=<from-terraform-output>
   AWS_SECRET_ACCESS_KEY=<from-terraform-output>
   
   # Email (if you have it)
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=<your-email>
   EMAIL_HOST_PASSWORD=<your-password>
   ```

6. **Instance role:** Select `AppRunnerCuratorBackendRole` (from Terraform)

7. Click **Create & deploy**

### Step 6: Configure Custom Domain

1. In App Runner service → **Custom domains**
2. Click **Add domain**
3. Enter: `api.curatorai.net`
4. Go to Route 53 → Add CNAME record:
   - Name: `api`
   - Type: **CNAME**
   - Value: `<app-runner-url>.awsapprunner.com`
   - TTL: 300
5. Wait for SSL certificate (5-10 minutes)

### Step 7: Setup GitHub Actions CI/CD

1. **Create IAM Role for GitHub Actions:**

   Go to IAM → Roles → Create role:
   - Trusted entity: **Web identity**
   - Identity provider: **GitHub**
   - Audience: `sts.amazonaws.com`
   - Condition: `StringEquals` → `token.actions.githubusercontent.com:aud` = `sts.amazonaws.com`
   - Condition: `StringLike` → `token.actions.githubusercontent.com:sub` = `repo:YOUR_USERNAME/YOUR_REPO:*`

   Attach policies:
   - `AmazonEC2ContainerRegistryFullAccess`
   - `AppRunnerFullAccess`

   Note the Role ARN

2. **Add GitHub Secrets:**

   Go to GitHub → Repository → Settings → Secrets and variables → Actions

   Add:
   - `AWS_ROLE_ARN`: Your IAM role ARN
   - `AWS_REGION`: `us-east-1`

3. **Test CI/CD:**

   Push to `main` branch:
   ```bash
   git add .
   git commit -m "Setup AWS deployment"
   git push origin main
   ```

   Check GitHub Actions tab for deployment status.

### Step 8: Verify Deployment

1. **Check service status:**
   - AWS App Runner console → Service should be "Running"

2. **Test API:**
   ```bash
   curl https://api.curatorai.net/api/health/
   ```

3. **Check logs:**
   - App Runner console → Logs tab

4. **Test admin panel:**
   - Visit: `https://api.curatorai.net/admin/`

## Environment Variables Comparison

### Vercel → AWS Mapping

| Variable | Vercel Value | AWS Value | Notes |
|----------|-------------|-----------|-------|
| `ALLOWED_HOSTS` | `curator-ai-backend.vercel.app,*.vercel.app` | `api.curatorai.net,curatorai.net` | Update for AWS domain |
| `DATABASE_URL` | Neon URL | Same Neon URL | No change needed |
| `CORS_ALLOWED_ORIGINS` | Frontend URLs | Same + `https://curatorai.net` | Add new domain |
| `USE_S3` | Not set | `True` | Enable for AWS |
| `AWS_*` | Not set | From Terraform | New for AWS |

## Migration Checklist

- [ ] Export Vercel environment variables
- [ ] Run Terraform to create infrastructure
- [ ] Save S3 access keys from Terraform output
- [ ] Build and push Docker image
- [ ] Create App Runner service
- [ ] Configure all environment variables
- [ ] Add custom domain `api.curatorai.net`
- [ ] Create CNAME in Route 53
- [ ] Wait for SSL certificate
- [ ] Test API endpoints
- [ ] Setup GitHub Actions CI/CD
- [ ] Test automatic deployment
- [ ] Update frontend to use new API URL
- [ ] Update OAuth redirect URLs
- [ ] Monitor for 24 hours
- [ ] Decommission Vercel (optional)

## Troubleshooting

### Service Won't Start

- Check App Runner logs
- Verify environment variables are set
- Check Docker image builds successfully
- Verify database connection (Neon)

### Domain Not Working

- Verify CNAME record in Route 53
- Wait for DNS propagation (up to 48 hours)
- Check App Runner custom domain status

### Database Connection Issues

- Verify Neon database is accessible
- Check `DATABASE_URL` format
- Ensure Neon allows connections from AWS IPs

### Static Files Not Loading

- Verify S3 bucket exists
- Check IAM role has S3 permissions
- Verify `USE_S3=True` is set
- Check S3 bucket policy

## Cost Comparison

**Vercel:**
- Free tier: Limited
- Pro: $20/month

**AWS (Estimated):**
- App Runner: ~$25-50/month
- S3: ~$0.25/month
- Route 53: ~$0.50/month
- **Total: ~$26-51/month**

## Rollback Plan

If issues occur:
1. Keep Vercel deployment running
2. Update Route 53 CNAME back to Vercel
3. Fix issues in AWS
4. Switch back when ready

## Next Steps

1. ✅ Complete migration
2. ✅ Monitor for 24-48 hours
3. ✅ Update frontend URLs
4. ✅ Update OAuth redirect URLs
5. ✅ Set up monitoring and alerts
6. ✅ Configure backups (if needed)

## Support

- Full AWS Guide: `AWS_DEPLOYMENT_GUIDE.md`
- Quick Start: `AWS_QUICK_START.md`
- Checklist: `AWS_MIGRATION_CHECKLIST.md`

