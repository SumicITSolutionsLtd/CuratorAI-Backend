# Installation Commands - Run These in Order

## Step 1: Navigate to Backend Folder
```powershell
cd "D:\Projects\On Going\Sumic\Curator\backend"
```

## Step 2: Activate Virtual Environment
```powershell
.venv\Scripts\Activate.ps1
```

**If you get an error**, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

## Step 3: Upgrade pip
```powershell
python -m pip install --upgrade pip
```

## Step 4: Install Dependencies
```powershell
pip install -r requirements/development.txt
```

This will take 2-5 minutes and install ~40 packages.

## Step 5: Run Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

## Step 6: Create Superuser
```powershell
python manage.py createsuperuser
```

Enter:
- **Email**: admin@curatorai.com
- **Username**: admin
- **Password**: (your choice - remember it!)

## Step 7: Start Server
```powershell
python manage.py runserver
```

## Step 8: Open Browser

Visit these URLs:
- http://localhost:8000/api/schema/swagger-ui/ (API Documentation)
- http://localhost:8000/admin/ (Admin Panel)
- http://localhost:8000/api/v1/auth/register/ (Test endpoint)

## Success! 🎉

You now have a running Django REST API!

---

## Next: Create Remaining App Models

The following apps need their models created:
- wardrobe
- posts  
- recommendations
- search
- lookbooks

I'll provide those files separately.

