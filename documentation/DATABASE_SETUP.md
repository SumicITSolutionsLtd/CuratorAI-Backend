# Database Setup Guide for CuratorAI

This guide will help you set up PostgreSQL database for CuratorAI and run migrations.

## Prerequisites

1. PostgreSQL installed and running (local or cloud)
2. Database credentials (host, port, database name, username, password)

## Option 1: Using DATABASE_URL (Recommended)

The easiest way is to use a `DATABASE_URL` environment variable.

### Format
```
postgresql://username:password@host:port/database_name
```

### Examples

**Local PostgreSQL:**
```bash
export DATABASE_URL="postgresql://curator_user:your_password@localhost:5432/curator_db"
```

**Cloud PostgreSQL (e.g., Vercel Postgres, Supabase, AWS RDS):**
```bash
export DATABASE_URL="postgresql://user:pass@host.region.rds.amazonaws.com:5432/dbname"
```

**For Vercel Postgres:**
```bash
export DATABASE_URL="postgres://default:password@ep-xxx.region.aws.neon.tech:5432/verceldb"
```

### Windows (Command Prompt)
```cmd
set DATABASE_URL=postgresql://curator_user:your_password@localhost:5432/curator_db
```

### Windows (PowerShell)
```powershell
$env:DATABASE_URL="postgresql://curator_user:your_password@localhost:5432/curator_db"
```

## Option 2: Using Individual Environment Variables

If you prefer to set variables individually:

```bash
export DB_NAME=curator_db
export DB_USER=curator_user
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
```

## Setting Up the Database

### Step 1: Create the Database

If the database doesn't exist, create it:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE curator_db;

# Create user (optional)
CREATE USER curator_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE curator_db TO curator_user;

# Exit
\q
```

### Step 2: Configure Environment Variables

Create a `.env` file in the project root (or set environment variables):

```env
# Database Configuration
DATABASE_URL=postgresql://curator_user:your_password@localhost:5432/curator_db

# Or use individual variables:
# DB_NAME=curator_db
# DB_USER=curator_user
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=5432
```

### Step 3: Run Migrations

**Using the setup script (recommended):**
```bash
python scripts/setup_postgres.py
```

**Or manually:**
```bash
python manage.py migrate
```

### Step 4: Verify Setup

Check that tables were created:

```bash
python manage.py dbshell
```

Then in the PostgreSQL shell:
```sql
\dt  -- List all tables
\q   -- Exit
```

Or use the setup script which will show all tables automatically.

## Cloud Database Providers

### Vercel Postgres

1. Go to your Vercel project dashboard
2. Navigate to Storage → Create Database → Postgres
3. Copy the `POSTGRES_URL` connection string
4. Set it as `DATABASE_URL` in your environment variables

### Supabase

1. Go to your Supabase project
2. Navigate to Settings → Database
3. Copy the connection string under "Connection string" → "URI"
4. Set it as `DATABASE_URL`

### AWS RDS

1. Create an RDS PostgreSQL instance
2. Get the endpoint from RDS console
3. Format: `postgresql://username:password@endpoint:5432/dbname`
4. Set as `DATABASE_URL`

### Railway

1. Create a PostgreSQL service in Railway
2. Copy the `DATABASE_URL` from the service variables
3. Use it directly

## Troubleshooting

### Error: "relation does not exist"

This means migrations haven't been run. Run:
```bash
python manage.py migrate
```

### Error: "could not connect to server"

1. Check PostgreSQL is running: `pg_isready` or `psql -U postgres`
2. Verify host, port, and credentials
3. Check firewall settings for cloud databases
4. Ensure database exists

### Error: "password authentication failed"

1. Verify username and password
2. Check PostgreSQL authentication settings (`pg_hba.conf`)
3. For cloud databases, ensure credentials are correct

### Error: "database does not exist"

Create the database first:
```sql
CREATE DATABASE curator_db;
```

## Verifying Tables

After migrations, you should see these tables:

- `accounts_*` (users, profiles, etc.)
- `outfits_*`
- `lookbooks` and related tables
- `wardrobes` and related tables
- `social_*`
- `notifications_*`
- `cart_*`
- `django_migrations` (tracks applied migrations)

## Next Steps

Once the database is set up:

1. Create a superuser: `python manage.py createsuperuser`
2. Load sample data (if available): `python manage.py seed_data`
3. Test the API endpoints using the test dashboard

## Production Deployment

For production (e.g., Vercel):

1. Set `DATABASE_URL` in your deployment platform's environment variables
2. The app will automatically use it (see `curator/settings/production.py`)
3. Migrations should run automatically on deployment, or run them manually

## Security Notes

⚠️ **Never commit `.env` files or database credentials to version control!**

- Add `.env` to `.gitignore`
- Use environment variables in your deployment platform
- Use strong passwords for production databases
- Enable SSL connections for cloud databases when possible

