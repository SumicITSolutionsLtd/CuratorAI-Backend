# 🚀 Django Setup Guide - Complete Beginner's Guide

**Step-by-step guide to set up and run the CuratorAI Django backend**  
**Perfect for developers new to Django**

---

## 📋 Prerequisites

Before you start, make sure you have:

1. **Python 3.11 or higher** installed
   - **Windows:** Check using Python launcher:
     ```cmd
     py --version
     ```
 
   - Should show: `Python 3.11.x` or higher
   - If not installed: Download from https://www.python.org/downloads/
   - **⚠️ On Windows:** Use `py` command instead of `python` if `python` doesn't work

2. **pip** (Python package installer) - usually comes with Python
   - **Windows:** Check using:
     ```cmd
     py -m pip --version
     ```


3. **Git** (optional, if cloning from repository)

---

## ⚠️ IMPORTANT: Windows Users - Use `py` Command!

**If `python` command doesn't work on Windows**, use the `py` launcher instead:


- ✅ `py --version` (works on Windows)

- ✅ `py -m venv venv`

- ✅ `py -m pip install ...`

---

## 📁 Step 1: Navigate to Project Directory

Open your terminal/command prompt and navigate to the backend folder:

```bash
cd D:\Projects\OnGoing\Sumic\Curator\backend
```

**Windows Command Prompt (CMD):**
```cmd
cd D:\Projects\OnGoing\Sumic\Curator\backend
```

**Windows PowerShell:**
```powershell
cd D:\Projects\OnGoing\Sumic\Curator\backend
```

---

## 🐍 Step 2: Create Virtual Environment

**What is a virtual environment?**  
It's an isolated Python environment for your project. It keeps dependencies separate from other projects.

**Create virtual environment:**

**Windows (CMD) - Use `py` if `python` doesn't work:**
```cmd
py -m venv venv
```



**Linux/Mac:**
```bash
python3 -m venv venv
```

This creates a folder called `venv` in your project directory.

---

## ✅ Step 3: Activate Virtual Environment

**Important:** You MUST activate the virtual environment before installing packages or running Django commands!

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

**✅ Success indicator:** You should see `(venv)` at the start of your command prompt:
```
(venv) D:\Projects\OnGoing\Sumic\Curator\backend>
```

**⚠️ If you get an error in PowerShell:** Run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📦 Step 4: Install Dependencies

Install all required Python packages:

**Windows (CMD) - Use `py -m pip` if `pip` doesn't work:**
```cmd
py -m pip install -r requirements/development.txt
```

**Alternative (if `pip` is in PATH):**
```cmd
pip install -r requirements/development.txt
```

**What this does:**
- Installs Django 5.0.7
- Installs Django REST Framework
- Installs all other required packages (50+ packages)

**⏱️ This may take 2-5 minutes** - be patient!

**✅ Success:** You should see "Successfully installed..." messages.

---

## ⚙️ Step 5: Set Up Environment Variables (Optional for Development)

For **development**, Django will use default settings. However, you can create a `.env` file for custom configuration.

**Create `.env` file** (in the `backend` folder):

**Windows (Command Prompt):**
```cmd
copy NUL .env
```

**Windows (PowerShell):**
```powershell
New-Item -Path .env -ItemType File
```

**Linux/Mac:**
```bash
touch .env
```

**Add these minimum settings to `.env`:**

```env
# Django Secret Key (generate your own!)
DJANGO_SECRET_KEY=your-super-secret-key-change-this-to-random-50-chars

# Debug mode (True for development)
DJANGO_DEBUG=True

# Allowed hosts
ALLOWED_HOSTS=localhost,127.0.0.1

# Django Settings Module (uses development settings by default)
DJANGO_SETTINGS_MODULE=curator.settings.development
```

**Generate a secret key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as `DJANGO_SECRET_KEY` in your `.env` file.

**⚠️ Note:** If you skip this step, Django will use default values for development (that's okay too!).

---

## 🗄️ Step 6: Set Up Database (Run Migrations)

**What are migrations?**  
Migrations are Django's way of creating and updating database tables based on your models.

**Run migrations:**

**Windows (CMD) - After activating venv:**
```cmd
python manage.py migrate
```

**Note:** Once you activate the virtual environment, `python` command should work inside `venv`.

**What this does:**
- Creates the SQLite database file (`db.sqlite3`) if it doesn't exist
- Creates all database tables (User, Outfit, Wardrobe, etc.)
- Applies all existing migrations

**✅ Success:** You should see:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, ...
Running migrations:
  Applying accounts.0001_initial... OK
  Applying outfits.0001_initial... OK
  ...
```

**First time:** This may take 30-60 seconds as it creates many tables.

---

## 👤 Step 7: Create Superuser (Admin Account)

**What is a superuser?**  
A superuser is an admin account that can access Django admin panel at `/admin/`.

**Create superuser:**

```bash
python manage.py createsuperuser
```

**You'll be prompted to enter:**
1. **Username:** (e.g., `admin` or your name)
2. **Email address:** (e.g., `admin@example.com`) - optional, press Enter to skip
3. **Password:** (enter a password - it won't show as you type)
4. **Password (again):** (confirm password)

**✅ Success:** You should see "Superuser created successfully."

**Example:**
```
Username: admin
Email address: admin@example.com
Password: ********
Password (again): ********
Superuser created successfully.
```

---

## 🚀 Step 8: Start Development Server

**Start the Django development server:**
venv\Scripts\activate.bat


```bash
python manage.py runserver
```

or 

venv\Scripts\python.exe manage.py runserver


**✅ Success:** You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**🎉 Server is running!** Keep this terminal window open.

---

## ✅ Step 9: Test the Setup

Open your web browser and visit these URLs:

### 1. **Home Page / API Root**
```
http://localhost:8000/
```
or
```
http://127.0.0.1:8000/
```

**Expected:** Should show a JSON response or welcome message.

### 2. **Django Admin Panel**
```
http://localhost:8000/admin/
```

**Login with:**
- Username: (the one you created in Step 7)
- Password: (the password you set)

**Expected:** You should see the Django admin dashboard with models like:
- Users
- Groups
- Accounts
- Outfits
- Wardrobe
- etc.

### 3. **API Documentation (Swagger UI)**
```
http://localhost:8000/api/schema/swagger-ui/
```

**Expected:** Interactive API documentation where you can:
- See all API endpoints
- Test endpoints directly
- View request/response examples

### 4. **Test an API Endpoint**
```
http://localhost:8000/api/v1/auth/register/
```

**Expected:** Should show API endpoint documentation or a response.

---

## 🧪 Step 10: Test Registration (Optional)

You can test creating a user via the API:

**Using Swagger UI (Recommended):**
1. Go to: http://localhost:8000/api/schema/swagger-ui/
2. Find `POST /api/v1/auth/register/`
3. Click "Try it out"
4. Enter test data:
   ```json
   {
     "email": "test@example.com",
     "username": "testuser",
     "password": "testpass123",
     "password2": "testpass123"
   }
   ```
5. Click "Execute"
6. Should return user data and JWT tokens!

**Using curl (Command Line):**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"username\":\"testuser\",\"password\":\"testpass123\",\"password2\":\"testpass123\"}"
```

**Using PowerShell (Windows):**
```powershell
Invoke-WebRequest -Uri http://localhost:8000/api/v1/auth/register/ -Method POST -ContentType "application/json" -Body '{"email":"test@example.com","username":"testuser","password":"testpass123","password2":"testpass123"}'
```

---

## 🛑 Stopping the Server

To stop the development server:
- Press `CTRL + C` in the terminal where the server is running
- Or close the terminal window

---

## 📝 Daily Workflow

Once everything is set up, here's your daily workflow:

### Starting Work:

1. **Navigate to project:**
   ```bash
   cd D:\Projects\OnGoing\Sumic\Curator\backend
   ```

2. **Activate virtual environment:**
   ```cmd
   venv\Scripts\activate.bat
   ```

3. **Start server:**
   ```bash
   python manage.py runserver
   ```

### After Making Model Changes:

1. **Create migrations:**
   ```bash
   python manage.py makemigrations
   ```

2. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

---

## 🐛 Common Issues & Solutions

### Issue 1: "python: command not found" or "python: unrecognized command"

**Solution:**
- **This is COMMON on Windows!** Use `py` launcher instead:
  ```cmd
  py --version              # Check Python version
  py -m venv venv           # Create virtual environment
  py -m pip install ...     # Install packages (before venv activation)
  ```
- After activating virtual environment (`venv\Scripts\activate.bat`), `python` should work
- **If `python` still doesn't work after activating venv** (Windows Store app alias issue):
  - **Quick fix:** Use the full path to venv's Python:
    ```cmd
    venv\Scripts\python.exe manage.py runserver
    venv\Scripts\python.exe manage.py migrate
    ```
  - **Permanent fix:** Disable Windows Store app execution aliases:
    1. Open **Settings** → **Apps** → **Advanced app settings** → **App execution aliases**
    2. Turn OFF the toggles for `python.exe` and `python3.exe`
    3. Restart your terminal and try `python` again
- If `py` also doesn't work, Python may not be installed - download from https://www.python.org/downloads/

### Issue 2: "pip: command not found"

**Solution:**
- **On Windows, use:** `py -m pip install ...`
- Install pip: `py -m ensurepip --upgrade`
- Or use: `py -m pip install ...` (always works on Windows)

### Issue 3: "ModuleNotFoundError: No module named 'django'"

**Solution:**
- Make sure virtual environment is activated (see `(venv)` prefix)
- Reinstall dependencies: `python -m pip install -r requirements/development.txt`

### Issue 3b: "ModuleNotFoundError: No module named 'requests'" or "ModuleNotFoundError: No module named 'cryptography'"

**Solution:**
- These are dependencies required by `django-allauth` for OAuth providers
- Install missing modules:
  ```cmd
  python -m pip install requests cryptography
  ```
- Or reinstall all dependencies:
  ```cmd
  python -m pip install -r requirements/development.txt
  ```

### Issue 4: "django.db.utils.OperationalError: no such table"

**Solution:**
- Run migrations: `python manage.py migrate`

### Issue 5: "Port 8000 is already in use"

**Solution:**
- Another process is using port 8000
- Stop other Django servers or use a different port:
  ```bash
  python manage.py runserver 8001
  ```
- Then access: `http://localhost:8001/`

### Issue 6: "Permission denied" when activating virtual environment (Windows)

**Solution (PowerShell):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Solution (CMD):**
- Use `venv\Scripts\activate.bat` instead of `activate.ps1`

### Issue 7: Migrations show "No changes detected"

**Solution:**
- This is normal if you haven't changed any models
- If you did change models, check:
  1. App is in `INSTALLED_APPS` in `curator/settings/base.py`
  2. Model is saved properly
  3. Try: `python manage.py makemigrations <app_name>`

### Issue 8: "Invalid SECRET_KEY"

**Solution:**
- Create/update `.env` file with `DJANGO_SECRET_KEY`
- Generate new key: 
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

---

## 📚 Useful Django Commands

### Database Commands:
```cmd
# Run migrations (after activating venv)
python manage.py migrate

# Create migrations (after changing models)
python manage.py makemigrations

# Show migration status
python manage.py showmigrations

# Create superuser
python manage.py createsuperuser

# Access Django shell (Python REPL with Django)
python manage.py shell
```

**Note:** Use `python` (not `py`) AFTER activating virtual environment!

### Server Commands:
```cmd
# Start server (default port 8000) - after activating venv
python manage.py runserver

# Start on specific port
python manage.py runserver 8001

# Start on specific IP and port
python manage.py runserver 0.0.0.0:8000
```

**Note:** Use `python` (not `py`) AFTER activating virtual environment!

### Utility Commands:
```cmd
# Check for issues (after activating venv)
python manage.py check

# Collect static files
python manage.py collectstatic

# Open Django shell
python manage.py shell
```

**Note:** Use `python` (not `py`) AFTER activating virtual environment!

---

## 🎓 Understanding the Project Structure

```
backend/
├── apps/                    # All Django apps
│   ├── accounts/           # User authentication
│   ├── outfits/            # Outfit management
│   ├── wardrobe/           # Wardrobe items
│   ├── notifications/      # Notifications
│   ├── cart/               # Shopping cart
│   ├── social/             # Social feed
│   └── lookbooks/          # Lookbooks
├── curator/                # Project settings
│   ├── settings/
│   │   ├── base.py         # Common settings
│   │   ├── development.py  # Development settings (active)
│   │   └── production.py   # Production settings
│   └── urls.py             # Main URL routing
├── core/                   # Shared utilities
├── db.sqlite3              # SQLite database (created after migrate)
├── manage.py               # Django management script
├── requirements/           # Dependency files
│   ├── base.txt           # Base dependencies
│   └── development.txt    # Development dependencies
└── venv/                   # Virtual environment (created by you)
```

---

## 🔗 Useful Links

- **API Documentation (Swagger):** http://localhost:8000/api/schema/swagger-ui/
- **Django Admin:** http://localhost:8000/admin/
- **API Base URL:** http://localhost:8000/api/v1/

---

## ✅ Setup Checklist

- [ ] Python 3.11+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements/development.txt`)
- [ ] Environment variables set up (optional)
- [ ] Migrations run (`python manage.py migrate`)
- [ ] Superuser created (`python manage.py createsuperuser`)
- [ ] Server running (`python manage.py runserver`)
- [ ] Can access http://localhost:8000/
- [ ] Can access http://localhost:8000/admin/
- [ ] Can access http://localhost:8000/api/schema/swagger-ui/

---

## 🎉 You're Ready!

If you've completed all steps and can access the URLs above, **congratulations!** Your Django backend is set up and ready for development.

**Next Steps:**
1. Explore the API using Swagger UI
2. Read the [Django Backend Guide](DJANGO_BACKEND_GUIDE.md) to understand how Django works
3. Start building features!

---

## 📞 Need Help?

If you encounter issues not covered here:
1. Check the [Django Backend Guide](DJANGO_BACKEND_GUIDE.md) for Django concepts
2. Check the [Implementation Summary](IMPLEMENTATION_SUMMARY.md) for what's been built
3. Check Django documentation: https://docs.djangoproject.com/

---

**Last Updated:** October 29, 2025  
**Version:** 1.0.0

