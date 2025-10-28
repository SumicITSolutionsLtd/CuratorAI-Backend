# CuratorAI Backend Setup Guide

Complete guide to set up your Django backend from scratch - optimized for **Command Prompt (CMD)**.

## Prerequisites

- ✅ Python 3.12+ installed
- Command Prompt (CMD) - preferred for Windows
- PostgreSQL (optional - we'll use SQLite for quick start)
- Redis (optional - for Celery tasks)

## 🚀 Quick Start (5 Minutes)

This guide will get you up and running with Django using SQLite for quick learning!

## Step 1: Activate Virtual Environment

Open **Command Prompt** (not PowerShell) in the `backend` folder:

```cmd
:: Navigate to backend folder
cd D:\Projects\OnGoing\Sumic\Curator\backend

:: Activate virtual environment
.venv\Scripts\activate.bat
```

You should see `(.venv)` in your terminal prompt.

**Note**: If you're in PowerShell and it's not working, switch to Command Prompt:
- Press `Win + R`, type `cmd`, press Enter
- Navigate to your project folder

## Step 2: Install Dependencies

```cmd
:: Upgrade pip first
python -m pip install --upgrade pip

:: Install all requirements
pip install -r requirements/development.txt

:: Install additional required packages
pip install requests cryptography
```

This will install:
- **Django 5.0.7** - The web framework
- **Django REST Framework** - For building APIs
- **django-allauth** - For authentication (email, Google, Facebook)
- **djangorestframework-simplejwt** - For JWT tokens
- **Celery** - For background tasks
- **And many more** - Check `requirements/development.txt` for full list

## Step 3: Database Setup (Choose One Option)

### ⭐ Option A: Use SQLite (Recommended for Beginners)

**This is the fastest way to get started!** SQLite is a file-based database, no installation needed.

**Already configured in your project!** The file `backend/curator/settings/development.py` is set up to use SQLite.

Your database will be created automatically in Step 4 as `backend/db.sqlite3`.

**Pros**: 
- Zero setup, works immediately
- Perfect for learning and development
- No separate database server needed

**Cons**: 
- Not suitable for production
- Limited concurrent access
- Switch to PostgreSQL before deploying

### Option B: Use Docker (Easy, Production-like)

```cmd
:: Start PostgreSQL and Redis in Docker
docker-compose up -d db redis
```

Then edit `backend/curator/settings/development.py` to use PostgreSQL (comment out SQLite config).

### Option C: Install PostgreSQL Locally

1. Download PostgreSQL: https://www.postgresql.org/download/windows/
2. Install with default settings (remember the password!)
3. Create database using pgAdmin or command line:

```sql
CREATE DATABASE curator_db;
CREATE USER curator_user WITH PASSWORD 'curator_pass';
GRANT ALL PRIVILEGES ON DATABASE curator_db TO curator_user;
```

Then update `backend/curator/settings/development.py` with your database credentials.

## Step 4: Create Migrations & Set Up Database

```cmd
:: First, create a static folder to avoid warnings
mkdir static

:: Generate migrations for the accounts app (if not already done)
python manage.py makemigrations accounts

:: Apply all migrations (create database tables)
python manage.py migrate
```

You should see output like:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying accounts.0001_initial... OK
  Applying account.0001_initial... OK
  Applying authtoken.0001_initial... OK
  ...
```

**What just happened?**
- Django created the `db.sqlite3` file (your database)
- All tables were created (users, auth tokens, sessions, etc.)
- Your app is now ready to store data!

## Step 5: Create Superuser (Admin Account)

```cmd
python manage.py createsuperuser
```

Enter:
- **Email**: admin@curator.com (or your choice)
- **Username**: admin
- **Password**: (your choice, min 8 characters)

**This account lets you:**
- Access the Django Admin panel
- Manage users, data, and content
- Test authentication features

## Step 6: Run Development Server

```cmd
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**🎉 Success!** Your Django server is now running!

## Step 7: Test the API

Open your browser and visit these URLs:

### 🎯 Essential URLs

1. **Admin Panel**: http://127.0.0.1:8000/admin/
   - Login with your superuser credentials
   - Manage users, data, and all models
   - Great for debugging and testing

2. **Swagger UI (Interactive API Docs)**: http://127.0.0.1:8000/api/schema/swagger-ui/
   - Test API endpoints directly in browser
   - See all available endpoints
   - Try out authentication, registration, etc.

3. **ReDoc (Beautiful API Documentation)**: http://127.0.0.1:8000/api/schema/redoc/
   - Clean, readable API documentation
   - Perfect for sharing with frontend team

4. **OpenAPI Schema**: http://127.0.0.1:8000/api/schema/
   - Raw API schema in JSON format
   - Import into Postman or other tools

### 🔗 API Endpoints Available

- **Authentication**: 
  - Register: `POST /api/v1/auth/register/`
  - Login: `POST /api/v1/auth/login/`
  - Logout: `POST /api/v1/auth/logout/`
  - Get User: `GET /api/v1/auth/user/`

- **Outfits**: 
  - List/Create: `GET/POST /api/v1/outfits/`
  - Detail: `GET/PUT/DELETE /api/v1/outfits/{id}/`

## Step 8: Test API with curl (Optional)

If you want to test from Command Prompt:

```cmd
:: Test user registration
curl -X POST http://127.0.0.1:8000/api/v1/auth/register/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"username\":\"testuser\",\"password\":\"Test123456\",\"password2\":\"Test123456\"}"
```

**Easier way**: Use the Swagger UI interface in your browser - it's much more user-friendly!

## ⚠️ Common Issues & Solutions

### Issue: "Python was not found"
**Solution**: 
- Use `py` command instead: `py --version`
- Or add Python to PATH and restart Command Prompt
- Restart your computer if just installed Python

### Issue: "Virtual environment not activating"
**Solution**:
```cmd
:: Make sure you're in Command Prompt (not PowerShell)
:: Use activate.bat (not Activate.ps1)
.venv\Scripts\activate.bat
```

### Issue: "No module named 'requests'" or "No module named 'cryptography'"
**Solution**:
```cmd
:: Install missing packages
pip install requests cryptography
```

### Issue: "No module named 'rest_framework.authtoken'"
**Solution**: This is already fixed in the project, but if you see it:
- Check that `'rest_framework.authtoken'` is in `INSTALLED_APPS` in `backend/curator/settings/base.py`

### Issue: "ModuleNotFoundError: No module named 'apps.wardrobe'"
**Solution**: These apps aren't created yet. They're commented out in `urls.py` for now.

### Issue: "Port 8000 already in use"
**Solution**: 
```cmd
:: Find what's using port 8000
netstat -ano | findstr :8000

:: Kill the process (replace PID with actual number)
taskkill /PID <PID_NUMBER> /F
```

### Issue: "staticfiles.W004 directory does not exist"
**Solution**:
```cmd
:: Create the static directory
mkdir static
```

### Issue: "No migrations to apply" or migration errors
**Solution**:
```cmd
:: Create fresh migrations
python manage.py makemigrations accounts

:: If database is corrupted, delete and recreate
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## 🚀 Next Steps

### 1. Explore Django Admin

Go to http://127.0.0.1:8000/admin/ and login with your superuser credentials.

**What you can do:**
- View and edit users
- Manage user profiles and style preferences
- Create test data
- See all your models in action

**Pro tip**: The admin is auto-generated from your models! Every field in your models appears here.

### 2. Test the API with Swagger UI

1. Go to http://127.0.0.1:8000/api/schema/swagger-ui/
2. Try the `/api/v1/auth/register/` endpoint
3. Register a test user
4. Try the `/api/v1/auth/login/` endpoint
5. Copy the JWT token and use "Authorize" button to authenticate

### 3. Create the Remaining Apps (When Ready)

The project has placeholder apps commented out. Create them when you're ready:

```cmd
:: Create remaining Django apps
python manage.py startapp wardrobe apps/wardrobe
python manage.py startapp posts apps/posts
python manage.py startapp recommendations apps/recommendations
python manage.py startapp search apps/search
python manage.py startapp lookbooks apps/lookbooks
```

Then uncomment them in:
- `backend/curator/settings/base.py` (INSTALLED_APPS)
- `backend/curator/urls.py` (URL patterns)

### 4. Start Celery (For Background Tasks - Optional)

Open a **new** Command Prompt window:

```cmd
:: Navigate and activate virtual environment
cd D:\Projects\OnGoing\Sumic\Curator\backend
.venv\Scripts\activate.bat

:: Start Celery worker
celery -A curator worker -l info
```

**What is Celery?**
- Runs background tasks (sending emails, processing images, etc.)
- Requires Redis (use Docker or install separately)
- Not needed for basic API testing

## 🔄 Daily Development Workflow

Every time you start working:

```cmd
:: 1. Open Command Prompt and navigate to backend folder
cd D:\Projects\OnGoing\Sumic\Curator\backend

:: 2. Activate virtual environment (ALWAYS DO THIS FIRST!)
.venv\Scripts\activate.bat

:: 3. Start the development server
python manage.py runserver

:: Server is now running at http://127.0.0.1:8000/
:: Press CTRL+BREAK to stop the server
```

### Common Django Commands

```cmd
:: ===== DATABASE =====
:: Create migrations after changing models
python manage.py makemigrations

:: Apply migrations to database
python manage.py migrate

:: Reset database (delete and recreate)
del db.sqlite3
python manage.py migrate

:: ===== USER MANAGEMENT =====
:: Create admin user
python manage.py createsuperuser

:: Change user password
python manage.py changepassword <username>

:: ===== SERVER =====
:: Run development server
python manage.py runserver

:: Run on different port
python manage.py runserver 8080

:: Run on all network interfaces (accessible from other devices)
python manage.py runserver 0.0.0.0:8000

:: ===== APP CREATION =====
:: Create a new Django app
python manage.py startapp app_name

:: Create app in apps directory
python manage.py startapp app_name apps/app_name

:: ===== SHELL =====
:: Open Django shell (interactive Python with Django loaded)
python manage.py shell

:: ===== TESTING =====
:: Run all tests
pytest

:: Run tests with coverage
pytest --cov

:: Run specific test file
pytest apps/accounts/tests/test_models.py

:: ===== UTILITIES =====
:: Check for problems
python manage.py check

:: Show all available commands
python manage.py help

:: Show SQL for migrations
python manage.py sqlmigrate accounts 0001
```

## 📊 Project Status

### ✅ What's Working

- ✅ **Django 5.0.7** project structure set up
- ✅ **SQLite database** configured and migrated
- ✅ **User authentication** with JWT tokens
- ✅ **User accounts app** with:
  - Custom User model (email-based login)
  - User profiles (gender, location, body measurements)
  - Style preferences (colors, brands, budget)
  - Social following system
- ✅ **Outfits app** with:
  - Outfit model (images, descriptions, occasions)
  - Outfit items (wardrobe pieces in outfits)
  - Likes and saves functionality
- ✅ **Django Admin Panel** - fully functional
- ✅ **API Documentation** - Swagger UI and ReDoc
- ✅ **REST API** with DRF
- ✅ **Authentication methods**:
  - Email/password registration and login
  - Social auth ready (Google, Facebook)
  - JWT token authentication

### 🔄 To Be Created (When Needed)

- ⏳ Wardrobe app (personal clothing items)
- ⏳ Posts app (social feed, outfit sharing)
- ⏳ Recommendations app (AI-powered suggestions)
- ⏳ Search app (outfit and user search)
- ⏳ Lookbooks app (curated outfit collections)
- ⏳ ML service integration (outfit analysis, virtual try-on)

## 📚 Learning Resources for Django Beginners

### 🎓 Official Documentation

1. **Django Official Tutorial** (Start Here!)
   - https://docs.djangoproject.com/en/5.0/intro/tutorial01/
   - 7-part tutorial that teaches Django fundamentals
   - Build a polling app step-by-step
   - **Estimated time**: 3-4 hours

2. **Django Documentation**
   - https://docs.djangoproject.com/en/5.0/
   - Comprehensive reference for everything Django
   - Topics: Models, Views, Templates, Forms, Authentication

3. **Django REST Framework (DRF)**
   - https://www.django-rest-framework.org/
   - **Quickstart**: https://www.django-rest-framework.org/tutorial/quickstart/
   - Learn to build APIs with Django
   - Serializers, ViewSets, Authentication

### 🎥 Video Tutorials

1. **Corey Schafer's Django Tutorial** (YouTube)
   - https://youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p
   - Comprehensive 17-part series
   - Very beginner-friendly
   - Covers models, views, templates, authentication

2. **Dennis Ivy - Django REST Framework**
   - https://youtube.com/watch?v=B38aDwUpcFc
   - Modern API development with DRF
   - Token authentication, serializers

3. **Traversy Media - Django Crash Course**
   - https://youtube.com/watch?v=e1IyzVyrLSU
   - Quick overview in 1 hour
   - Good for getting started fast

### 📖 Free Courses

1. **Django for Beginners** (Book + Website)
   - https://djangoforbeginners.com/
   - Written by William S. Vincent
   - Covers Django basics thoroughly

2. **MDN Django Tutorial**
   - https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django
   - Mozilla's comprehensive Django guide
   - Build a library catalog app

### 🔑 Key Concepts to Learn

#### 1. **Django Models** (Database Layer)
```python
# Define your data structure
class User(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
```
- **Learn**: Field types, relationships (ForeignKey, ManyToMany), migrations
- **Docs**: https://docs.djangoproject.com/en/5.0/topics/db/models/

#### 2. **Django Views** (Business Logic)
```python
# Handle requests and return responses
def my_view(request):
    data = Model.objects.all()
    return JsonResponse({'data': data})
```
- **Learn**: Function-based views, class-based views, generic views
- **Docs**: https://docs.djangoproject.com/en/5.0/topics/http/views/

#### 3. **Django URLs** (Routing)
```python
# Map URLs to views
urlpatterns = [
    path('api/users/', UserListView.as_view()),
]
```
- **Learn**: URL patterns, path converters, includes
- **Docs**: https://docs.djangoproject.com/en/5.0/topics/http/urls/

#### 4. **DRF Serializers** (Data Validation & Formatting)
```python
# Convert models to JSON and validate input
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']
```
- **Learn**: ModelSerializer, validation, nested serializers
- **Docs**: https://www.django-rest-framework.org/api-guide/serializers/

#### 5. **Authentication & Permissions**
```python
# Protect your API endpoints
class MyView(APIView):
    permission_classes = [IsAuthenticated]
```
- **Learn**: JWT tokens, session auth, permissions
- **Docs**: https://www.django-rest-framework.org/api-guide/authentication/

### 🛠️ Useful Tools

1. **DB Browser for SQLite**
   - https://sqlitebrowser.org/
   - Visual database viewer
   - See your data, run queries

2. **Postman**
   - https://www.postman.com/downloads/
   - Test API endpoints
   - Alternative to curl

3. **Django Debug Toolbar**
   - Already installed in your project!
   - Shows SQL queries, performance info
   - Visible when DEBUG=True

4. **Django Extensions**
   - Already installed!
   - Adds useful management commands
   - `python manage.py shell_plus` - enhanced shell

### 📝 Cheat Sheets

1. **Django Cheat Sheet**
   - https://github.com/lucrae/django-cheat-sheet
   - Quick reference for common tasks

2. **DRF Cheat Sheet**
   - https://www.cdrf.co/
   - Class-based view reference

### 🤝 Community & Help

1. **Django Discord**
   - https://discord.gg/xcRH6mN4fa
   - Active community for questions

2. **r/django (Reddit)**
   - https://reddit.com/r/django
   - Django discussions and help

3. **Stack Overflow**
   - Tag: `[django]` or `[django-rest-framework]`
   - Search before asking!

### 💡 Tips for Beginners

1. **Start Small**: Don't try to learn everything at once
2. **Follow the Tutorial**: Complete the official Django tutorial first
3. **Read the Docs**: Django has excellent documentation
4. **Use the Shell**: `python manage.py shell` - test code interactively
5. **Check the Admin**: Great way to verify your models work
6. **Learn SQL Basics**: Understanding databases helps A LOT
7. **Use Git**: Commit often, experiment fearlessly
8. **Test Your Code**: Write tests as you go
9. **Ask Questions**: Django community is very helpful
10. **Build Projects**: Best way to learn is by doing!

### 🎯 Recommended Learning Path

**Week 1: Django Basics**
1. Complete Django official tutorial (Parts 1-7)
2. Understand models, views, URLs, templates
3. Learn about migrations and the admin panel

**Week 2: Django REST Framework**
1. Complete DRF quickstart
2. Learn about serializers and viewsets
3. Understand authentication and permissions

**Week 3: Build Your Own API**
1. Start with a simple API (Todo app, Notes app)
2. Add authentication
3. Test with Postman/Swagger

**Week 4: Dive into CuratorAI**
1. Study the existing models
2. Create the remaining apps
3. Build new features

---

## 🎉 You're All Set!

Your Django backend is running and ready for development. Start with the Django tutorial, explore the admin panel, and gradually build features.

**Remember**: 
- ✅ Virtual environment: `.venv\Scripts\activate.bat`
- ✅ Start server: `python manage.py runserver`
- ✅ Admin panel: http://127.0.0.1:8000/admin/
- ✅ API docs: http://127.0.0.1:8000/api/schema/swagger-ui/

**Need Help?** Check the Common Issues section above or ask in the Django community!

Happy coding! 🚀

