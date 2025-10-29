# 🎓 Django Backend Guide for Beginners

**Complete guide to understanding the CuratorAI Django backend**  
**For developers new to Django but familiar with Python**

---

## 📋 Table of Contents

1. [Django Architecture Overview](#django-architecture-overview)
2. [Project Structure](#project-structure)
3. [How Django Works](#how-django-works)
4. [Models - Database Layer](#models---database-layer)
5. [Serializers - Data Conversion](#serializers---data-conversion)
6. [Views - Business Logic](#views---business-logic)
7. [URLs - Routing](#urls---routing)
8. [Authentication - JWT](#authentication---jwt)
9. [Database Operations](#database-operations)
10. [Making Changes](#making-changes)
11. [Debugging Guide](#debugging-guide)

---

## 🏗️ Django Architecture Overview

### MTV Pattern (Model-Template-View)

Django uses MTV, but for APIs we adapt it to **Model-Serializer-View**:

```
Request → URLs → View → Serializer → Model → Database
                  ↓
Response ← JSON ← Serializer ← QuerySet ← Database
```

**Flow Example:** User registers
1. **Request:** POST to `/api/v1/auth/register/` with JSON data
2. **URL Router:** Maps to `RegisterView`
3. **View:** Validates data using `UserSerializer`
4. **Serializer:** Converts JSON to Python objects
5. **Model:** Saves user to database
6. **Response:** Returns user data + JWT tokens as JSON

---

## 📁 Project Structure

```
backend/
├── apps/                    # All Django apps
│   ├── accounts/           # User authentication
│   │   ├── models.py      # User, Profile models
│   │   ├── serializers.py # JSON ↔ Python conversion
│   │   ├── views.py       # Business logic
│   │   └── urls.py        # Route definitions
│   ├── outfits/           # Outfit management
│   ├── wardrobe/          # Wardrobe items
│   ├── notifications/     # Notifications
│   ├── cart/              # Shopping cart
│   ├── social/            # Social feed
│   └── lookbooks/         # Lookbooks
├── core/                   # Shared utilities
├── curator/               # Project configuration
│   ├── settings/
│   │   ├── base.py       # Common settings
│   │   ├── development.py # Dev settings
│   │   └── production.py  # Prod settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI server entry point
└── manage.py             # Django management commands
```

---

## 🔄 How Django Works

### 1. **Request Lifecycle**

```python
# User makes request
POST /api/v1/auth/login/
{
  "email": "user@example.com",
  "password": "password123"
}

# Django processes:
# 1. URLs: Find matching route
# 2. View: Execute LoginView
# 3. Serializer: Validate input
# 4. Model: Check user exists
# 5. Response: Return tokens
```

### 2. **Django Apps**

Each app is a self-contained module:
- **accounts**: User management
- **outfits**: Outfit CRUD
- **wardrobe**: Wardrobe items
- etc.

**Why separate apps?**
- Modularity
- Reusability
- Easier testing
- Clear separation of concerns

---

## 📊 Models - Database Layer

### What are Models?

Models define your database schema using Python classes.

**Example: User Model**

```python
class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

**This creates a database table:**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    bio TEXT,
    avatar VARCHAR(255),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP
);
```

### Field Types

```python
# Text fields
CharField(max_length=100)      # Short text (255 chars max)
TextField()                     # Long text (unlimited)
EmailField()                    # Email validation

# Numbers
IntegerField()                  # Integers
DecimalField(max_digits=10, decimal_places=2)  # Money, precise decimals
FloatField()                    # Floating point

# Dates
DateField()                     # Date only
DateTimeField()                 # Date + time
DateTimeField(auto_now_add=True)  # Set on creation
DateTimeField(auto_now=True)    # Update on every save

# Boolean
BooleanField(default=False)     # True/False

# Files
ImageField(upload_to='images/') # Images
FileField(upload_to='files/')   # Any file

# Relationships
ForeignKey(User, on_delete=models.CASCADE)  # One-to-many
ManyToManyField(Tag)            # Many-to-many
OneToOneField(Profile)          # One-to-one

# JSON
JSONField(default=dict)         # Store JSON data
```

### Relationships

**One-to-Many (ForeignKey):**
```python
class Outfit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # One user can have many outfits
```

**Many-to-Many:**
```python
class Outfit(models.Model):
    tags = models.ManyToManyField(Tag)
    # One outfit can have many tags
    # One tag can be on many outfits
```

---

## 🔄 Serializers - Data Conversion

### What are Serializers?

Serializers convert between Python objects and JSON (and vice versa).

**Example:**

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']
        read_only_fields = ['id']
```

**What it does:**

```python
# Python object → JSON (serialization)
user = User.objects.get(id=1)
serializer = UserSerializer(user)
serializer.data  # → {'id': 1, 'email': 'user@example.com', ...}

# JSON → Python object (deserialization)
data = {'email': 'new@example.com', 'username': 'newuser'}
serializer = UserSerializer(data=data)
if serializer.is_valid():
    user = serializer.save()  # Creates User object
```

### Validation

```python
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    def validate_email(self, value):
        """Custom email validation"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate(self, data):
        """Validate multiple fields together"""
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords don't match")
        return data
```

---

## 🎯 Views - Business Logic

### What are Views?

Views handle business logic and return responses.

### Types of Views

**1. APIView (Custom logic):**

```python
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

**2. Generic Views (Built-in functionality):**

```python
class OutfitListView(generics.ListCreateAPIView):
    queryset = Outfit.objects.all()
    serializer_class = OutfitSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter outfits for current user
        return Outfit.objects.filter(user=self.request.user)
```

**3. ViewSets (All CRUD in one):**

```python
class OutfitViewSet(viewsets.ModelViewSet):
    queryset = Outfit.objects.all()
    serializer_class = OutfitSerializer
    # Automatically provides: list, create, retrieve, update, destroy
```

### Common Generic Views

```python
# List all + Create
ListCreateAPIView

# Retrieve one
RetrieveAPIView

# Update one
UpdateAPIView

# Delete one
DestroyAPIView

# Retrieve + Update + Delete
RetrieveUpdateDestroyAPIView
```

---

## 🛣️ URLs - Routing

### How URLs Work

URLs map HTTP requests to views.

```python
# apps/accounts/urls.py
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]

# curator/urls.py (main)
urlpatterns = [
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/outfits/', include('apps.outfits.urls')),
]
```

**Result:**
- `POST /api/v1/auth/register/` → `RegisterView`
- `POST /api/v1/auth/login/` → `LoginView`
- `GET /api/v1/auth/users/123/` → `UserDetailView` (pk=123)

### URL Parameters

```python
# Path parameters
path('users/<int:user_id>/', view)  # /users/123/
path('posts/<uuid:post_id>/', view)  # /posts/abc-123-def/

# Query parameters (in view)
def get(self, request):
    search = request.query_params.get('search')  # ?search=test
    page = request.query_params.get('page', 1)    # ?page=2
```

---

## 🔐 Authentication - JWT

### How JWT Works

```python
# User logs in
POST /api/v1/auth/login/
{
  "email": "user@example.com",
  "password": "password123"
}

# Response includes tokens
{
  "access": "eyJ0eXAiOiJKV1...",  # Short-lived (15 min)
  "refresh": "eyJ0eXAiOiJKV1...", # Long-lived (7 days)
  "user": {...}
}

# Future requests include access token
GET /api/v1/outfits/
Authorization: Bearer eyJ0eXAiOiJKV1...
```

### Protected Views

```python
from rest_framework.permissions import IsAuthenticated

class OutfitListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # request.user is automatically available
        outfits = Outfit.objects.filter(user=request.user)
        serializer = OutfitSerializer(outfits, many=True)
        return Response(serializer.data)
```

---

## 💾 Database Operations

### QuerySets

QuerySets are lazy - they don't hit the database until you use them.

```python
# Get all
users = User.objects.all()

# Filter
active_users = User.objects.filter(is_active=True)
verified = User.objects.filter(is_verified=True, is_active=True)

# Get one
user = User.objects.get(id=1)  # Raises error if not found
user = User.objects.filter(email='test@example.com').first()  # Returns None if not found

# Exclude
non_verified = User.objects.exclude(is_verified=True)

# Order
recent_users = User.objects.order_by('-created_at')  # - for descending

# Count
user_count = User.objects.count()

# Exists
has_users = User.objects.filter(email='test@example.com').exists()

# Create
user = User.objects.create(
    email='new@example.com',
    username='newuser'
)

# Update
User.objects.filter(id=1).update(is_verified=True)

# Delete
User.objects.filter(id=1).delete()
```

### Field Lookups

```python
# Exact match
User.objects.filter(username='john')
User.objects.filter(username__exact='john')  # Same

# Case-insensitive
User.objects.filter(username__iexact='JOHN')

# Contains
User.objects.filter(username__contains='jo')
User.objects.filter(username__icontains='JO')  # Case-insensitive

# Starts with / Ends with
User.objects.filter(email__startswith='user')
User.objects.filter(email__endswith='@gmail.com')

# Greater than / Less than
User.objects.filter(age__gt=18)   # Greater than
User.objects.filter(age__gte=18)  # Greater than or equal
User.objects.filter(age__lt=65)   # Less than
User.objects.filter(age__lte=65)  # Less than or equal

# In list
User.objects.filter(id__in=[1, 2, 3, 4, 5])

# Date ranges
from datetime.datetime import datetime, timedelta
yesterday = datetime.now() - timedelta(days=1)
User.objects.filter(created_at__gte=yesterday)

# Null checks
User.objects.filter(bio__isnull=True)
User.objects.filter(bio__isnull=False)
```

### Relationships

```python
# Forward relationship (ForeignKey)
outfit = Outfit.objects.get(id=1)
user = outfit.user  # Get the user who created this outfit

# Reverse relationship
user = User.objects.get(id=1)
outfits = user.outfit_set.all()  # Get all outfits by this user

# With related_name
class Outfit(models.Model):
    user = models.ForeignKey(User, related_name='outfits', on_delete=models.CASCADE)

user.outfits.all()  # Cleaner!

# Many-to-many
outfit.tags.add(tag)         # Add a tag
outfit.tags.remove(tag)      # Remove a tag
outfit.tags.all()            # Get all tags
outfit.tags.clear()          # Remove all tags
```

### Optimization

```python
# select_related (for ForeignKey - single JOIN)
outfits = Outfit.objects.select_related('user').all()
# SQL: SELECT * FROM outfits JOIN users ...

# prefetch_related (for Many-to-many - separate queries)
outfits = Outfit.objects.prefetch_related('tags').all()
# SQL: SELECT * FROM outfits; SELECT * FROM tags WHERE ...

# only / defer
users = User.objects.only('id', 'email')  # Only fetch these fields
users = User.objects.defer('bio')         # Fetch all except these
```

---

## 🔧 Making Changes

### Adding a New Field to a Model

```python
# 1. Add field to model
class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)  # New field

# 2. Create migration
python manage.py makemigrations

# 3. Apply migration
python manage.py migrate

# 4. Update serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [..., 'phone_number']  # Add here
```

### Adding a New Endpoint

```python
# 1. Create view (apps/accounts/views.py)
class UpdatePhoneView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        user.phone_number = request.data.get('phone_number')
        user.save()
        return Response({'message': 'Phone updated'})

# 2. Add URL (apps/accounts/urls.py)
urlpatterns = [
    ...,
    path('update-phone/', UpdatePhoneView.as_view(), name='update-phone'),
]

# 3. Test
curl -X POST http://localhost:8000/api/v1/auth/update-phone/ \
  -H "Authorization: Bearer <token>" \
  -d '{"phone_number": "1234567890"}'
```

### Adding a New App

```python
# 1. Create app
python manage.py startapp myapp apps/myapp

# 2. Register in settings
INSTALLED_APPS = [
    ...,
    'apps.myapp',
]

# 3. Create models
class MyModel(models.Model):
    name = models.CharField(max_length=100)

# 4. Create migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create serializers, views, URLs
# 6. Include URLs in main urls.py
path('api/v1/myapp/', include('apps.myapp.urls')),
```

---

## 🐛 Debugging Guide

### Common Issues

**1. "No module named 'apps.xxx'"**
```python
# Solution: Check INSTALLED_APPS in settings.py
INSTALLED_APPS = [
    'apps.accounts',
    'apps.outfits',
    # Add your app here
]
```

**2. "Relation does not exist"**
```bash
# Solution: Run migrations
python manage.py makemigrations
python manage.py migrate
```

**3. "Authentication credentials were not provided"**
```python
# Solution: Add JWT token to request
headers = {
    'Authorization': f'Bearer {access_token}'
}
```

**4. "User matching query does not exist"**
```python
# Solution: Use .first() or try/except
user = User.objects.filter(email=email).first()
if not user:
    return Response({'error': 'User not found'}, status=404)
```

### Debugging Tips

```python
# 1. Print to console
print(f"User: {user}")
print(f"Request data: {request.data}")

# 2. Use Django shell
python manage.py shell
>>> from apps.accounts.models import User
>>> User.objects.all()

# 3. Check SQL queries
from django.db import connection
print(connection.queries)

# 4. Use Django Debug Toolbar (in development)
# Shows SQL queries, templates, signals, etc.

# 5. Use logging
import logging
logger = logging.getLogger(__name__)
logger.info(f"User {user.id} logged in")
logger.error(f"Error occurred: {error}")
```

### Testing Endpoints

```bash
# Using curl
curl -X GET http://localhost:8000/api/v1/auth/me/ \
  -H "Authorization: Bearer <token>"

# Using Python requests
import requests
response = requests.get(
    'http://localhost:8000/api/v1/auth/me/',
    headers={'Authorization': f'Bearer {token}'}
)
print(response.json())

# Using Swagger UI
# Go to http://localhost:8000/api/schema/swagger-ui/
# Click on endpoint → Try it out → Execute
```

---

## 📚 Key Concepts Summary

### 1. Models = Database Tables
- Define structure with Python classes
- Django creates SQL automatically

### 2. Serializers = JSON ↔ Python
- Convert data between formats
- Handle validation

### 3. Views = Business Logic
- Process requests
- Return responses

### 4. URLs = Routing
- Map URLs to views

### 5. Migrations = Database Changes
- Track schema changes
- Apply changes safely

---

## 🎯 Next Steps

1. **Explore the code**: Start with a simple app like `accounts`
2. **Make small changes**: Add a field, create an endpoint
3. **Test everything**: Use Swagger UI or curl
4. **Read Django docs**: https://docs.djangoproject.com/
5. **Read DRF docs**: https://www.django-rest-framework.org/

---

**You're ready to work with Django!** 🎉

---

**Last Updated:** October 29, 2025  
**Author:** Created for CuratorAI Backend Team

