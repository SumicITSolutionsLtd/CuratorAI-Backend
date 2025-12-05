# AWS Migration Checklist

Use this checklist to track your migration from Vercel to AWS App Runner.

## Prerequisites

- [ ] AWS Account with admin access
- [ ] Domain `curatorai.net` in Route 53 (or your domain)
- [ ] Neon PostgreSQL database (already configured) 
- [ ] AWS CLI installed and configured
- [ ] Docker installed locally
- [ ] GitHub repository access

## Phase 1: Infrastructure Setup

### Terraform Infrastructure

- [ ] Navigate to `infrastructure/terraform` directory
- [ ] Copy `terraform.tfvars.example` to `terraform.tfvars`
- [ ] Edit `terraform.tfvars` with your values:
  - [ ] `aws_region = "us-east-1"`
  - [ ] `environment = "production"`
  - [ ] `bucket_name = "curatorai-static-media"`
- [ ] Run `terraform init`
- [ ] Run `terraform plan` (review changes)
- [ ] Run `terraform apply` (create infrastructure)
- [ ] **Save Terraform outputs:**
  - [ ] `s3_bucket_name`
  - [ ] `s3_access_key_id`
  - [ ] `s3_secret_access_key`
  - [ ] `ecr_repository_url`
  - [ ] `app_runner_role_arn`

## Phase 2: Environment Variables

### Export from Vercel

- [ ] Go to Vercel Dashboard → Project → Settings → Environment Variables
- [ ] Copy all environment variables
- [ ] Or use CLI: `vercel env pull .env.vercel`

### Migrate to AWS Format

- [ ] Update `ALLOWED_HOSTS`:
  - [ ] From: `curator-ai-backend.vercel.app,*.vercel.app`
  - [ ] To: `api.curatorai.net,curatorai.net`
- [ ] Keep `DATABASE_URL` (same Neon URL)
- [ ] Update `CORS_ALLOWED_ORIGINS`:
  - [ ] Add `https://curatorai.net` if not present
- [ ] Add S3 configuration:
  - [ ] `USE_S3=True`
  - [ ] `AWS_STORAGE_BUCKET_NAME=<from-terraform>`
  - [ ] `AWS_S3_REGION_NAME=us-east-1`
  - [ ] `AWS_ACCESS_KEY_ID=<from-terraform>`
  - [ ] `AWS_SECRET_ACCESS_KEY=<from-terraform>`

## Phase 3: Docker & ECR

### Build and Push Image

- [ ] Test Docker build locally: `docker build -t curator-backend .`
- [ ] Tag image: `docker tag curator-backend:latest <ecr-url>/curator-backend:latest`
- [ ] Login to ECR: `aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ecr-url>`
- [ ] Push image: `docker push <ecr-url>/curator-backend:latest`
- [ ] Verify image in ECR console

## Phase 4: App Runner Service

### Create Service

- [ ] Go to AWS App Runner console
- [ ] Click "Create service"
- [ ] Configure source:
  - [ ] Provider: **Amazon ECR**
  - [ ] Container image URI: Select `curator-backend:latest`
  - [ ] Deployment trigger: **Manual** (or **Automatic** after CI/CD)
- [ ] Configure service:
  - [ ] Service name: `curator-backend`
  - [ ] Virtual CPU: **1 vCPU**
  - [ ] Memory: **2 GB**
  - [ ] Port: **8000**
- [ ] Add environment variables (all from Phase 2)
- [ ] Set instance role: `AppRunnerCuratorBackendRole` (from Terraform)
- [ ] Click "Create & deploy"
- [ ] Wait for service to be "Running" (5-10 minutes)

## Phase 5: Domain Configuration

### Custom Domain

- [ ] In App Runner → Custom domains → Add domain
- [ ] Enter: `api.curatorai.net`
- [ ] Copy the provided CNAME value
- [ ] Go to Route 53 → Hosted zones → `curatorai.net`
- [ ] Create CNAME record:
  - [ ] Name: `api`
  - [ ] Type: **CNAME**
  - [ ] Value: `<app-runner-url>.awsapprunner.com`
  - [ ] TTL: **300**
- [ ] Wait for SSL certificate (5-10 minutes)
- [ ] Verify domain status shows "Active"

## Phase 6: CI/CD Setup

### Add GitHub Identity Provider (Required First)

- [ ] Go to IAM → Identity providers → Add provider
- [ ] Provider type: **OpenID Connect**
- [ ] Provider URL: `https://token.actions.githubusercontent.com`
- [ ] Audience: `sts.amazonaws.com`
- [ ] Click "Add provider"
- [ ] Verify GitHub appears in identity providers list

### IAM Role for GitHub Actions

- [ ] Go to IAM → Roles → Create role
- [ ] Trusted entity type: **Web identity**
- [ ] Identity provider: Select **GitHub** (should now appear)
- [ ] Audience: `sts.amazonaws.com`
- [ ] Click "Next"
- [ ] Add conditions:
  - [ ] Condition 1: `StringEquals` → `token.actions.githubusercontent.com:aud` = `sts.amazonaws.com`
  - [ ] Condition 2: `StringLike` → `token.actions.githubusercontent.com:sub` = `repo:YOUR_USERNAME/YOUR_REPO:*`
    (Replace with your actual GitHub username and repo name)
- [ ] Click "Next"
- [ ] Attach policies:
  - [ ] `AmazonEC2ContainerRegistryFullAccess`
  - [ ] `AppRunnerFullAccess`
- [ ] Click "Next"
- [ ] Role name: `GitHubActionsDeployRole` (or your preferred name)
- [ ] Click "Create role"
- [ ] **Copy the Role ARN** (you'll need it for GitHub Secrets)

### GitHub Secrets

- [ ] Go to GitHub → Repository → Settings → Secrets and variables → Actions
- [ ] Add secret: `AWS_ROLE_ARN` = Your IAM role ARN
- [ ] Add secret: `AWS_REGION` = `us-east-1`
- [ ] Verify secrets are saved

### Test CI/CD

- [ ] Make a small change to code
- [ ] Commit and push to `main` branch
- [ ] Check GitHub Actions tab
- [ ] Verify workflow runs successfully
- [ ] Check App Runner console for new deployment

## Phase 7: Verification

### API Testing

- [ ] Test health endpoint: `curl https://api.curatorai.net/api/health/`
- [ ] Test API root: `curl https://api.curatorai.net/`
- [ ] Test authentication endpoints
- [ ] Test image upload (verify S3 URLs)
- [ ] Check App Runner logs for errors

### Frontend Updates

- [ ] Update frontend API URL to `https://api.curatorai.net`
- [ ] Update OAuth redirect URLs in Google Console
- [ ] Update OAuth redirect URLs in Facebook Console
- [ ] Test frontend authentication flow
- [ ] Test image uploads from frontend

## Phase 8: Monitoring

### Setup Monitoring (Optional)

- [ ] Set up CloudWatch alarms for App Runner
- [ ] Monitor S3 bucket usage
- [ ] Set up error notifications
- [ ] Monitor database connections (Neon)
- [ ] Check logs regularly for first 24-48 hours

## Phase 9: Cleanup (Optional)

### Decommission Vercel

- [ ] Verify AWS deployment is stable (24-48 hours)
- [ ] Update all external references to new URL
- [ ] Backup Vercel environment variables (already done)
- [ ] Delete Vercel project (optional)
- [ ] Update documentation with new URLs

## Troubleshooting Checklist

If issues occur:

- [ ] Check App Runner logs in AWS console
- [ ] Verify environment variables are set correctly
- [ ] Check Docker image builds successfully
- [ ] Verify database connection (Neon)
- [ ] Check S3 bucket permissions
- [ ] Verify IAM role has correct permissions
- [ ] Check Route 53 DNS propagation
- [ ] Verify SSL certificate is active
- [ ] Check CORS settings
- [ ] Review GitHub Actions workflow logs

## Success Criteria

- [ ] App Runner service is "Running"
- [ ] Custom domain is "Active"
- [ ] API endpoints respond correctly
- [ ] Images upload to S3 successfully
- [ ] Frontend can authenticate
- [ ] CI/CD deploys automatically on push
- [ ] No errors in App Runner logs
- [ ] All tests pass

## Notes

- Keep Vercel deployment running during migration for rollback
- Test thoroughly before decommissioning Vercel
- Monitor costs in AWS console
- Estimated monthly cost: ~$26-51/month

---

**Related Documentation:**
- [AWS Setup Guide](./AWS_SETUP_WITH_NEON.md)
- [Vercel to AWS Migration](./VERCEL_TO_AWS_MIGRATION.md)

