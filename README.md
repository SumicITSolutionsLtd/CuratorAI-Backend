# CuratorAI Backend - Django REST API

AI-powered fashion recommendation platform backend built with Django and Django REST Framework.

## Tech Stack

- **Framework**: Django 5.0 + Django REST Framework
- **Database**: PostgreSQL 15+
- **Cache**: Redis 7.0
- **Task Queue**: Celery
- **Storage**: AWS S3 (via django-storages)
- **Auth**: JWT (djangorestframework-simplejwt)

## Quick Start

### 1. Install Python 3.11+

Make sure Python is installed and added to PATH.

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements/development.txt
```

### 4. Environment Setup

```bash
copy .env.example .env
```

Edit `.env` and update values as needed.

### 5. Run with Docker (Recommended)

```bash
docker-compose up -d
```

This starts PostgreSQL, Redis, and the Django app.

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
python manage.py runserver
```

API will be available at `http://localhost:8000/api/v1/`

## Project Structure

```
backend/
├── curator/           # Main Django project
├── apps/             # Django apps
│   ├── accounts/     # Authentication & profiles
│   ├── outfits/      # Outfit management
│   ├── wardrobe/     # Personal wardrobe
│   ├── posts/        # Social feed
│   ├── recommendations/  # AI recommendations
│   ├── search/       # Visual search
│   └── lookbooks/    # Shoppable lookbooks
├── core/             # Shared utilities
└── ml_services/      # ML integration layer
```

## API Documentation

- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **ReDoc**: http://localhost:8000/api/schema/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## Admin Panel

Django admin available at: http://localhost:8000/admin/

## Testing

```bash
pytest
pytest --cov
```

## Key Endpoints

### Authentication
- POST `/api/v1/auth/register/` - Register new user
- POST `/api/v1/auth/login/` - Login (get JWT tokens)
- POST `/api/v1/auth/refresh/` - Refresh access token
- GET `/api/v1/auth/me/` - Get current user profile

### Outfits
- GET `/api/v1/outfits/` - List outfits
- POST `/api/v1/outfits/` - Create outfit
- GET `/api/v1/outfits/{id}/` - Get outfit details

### Recommendations
- GET `/api/v1/recommendations/` - Get personalized recommendations

### Visual Search
- POST `/api/v1/search/visual/` - Upload image for visual search

### Wardrobe
- GET `/api/v1/wardrobe/items/` - List wardrobe items
- POST `/api/v1/wardrobe/items/` - Add item to wardrobe

### Posts (Social Feed)
- GET `/api/v1/posts/` - Get social feed
- POST `/api/v1/posts/` - Create post

## License

Proprietary - K&O Curator Technologies Group Ltd.

