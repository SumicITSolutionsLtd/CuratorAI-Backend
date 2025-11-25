# OpenAPI Schema Implementation Guide

## ✅ Completed Implementation

### 1. Enhanced Exception Handler (`core/exceptions.py`)
- Comprehensive error handling with proper error codes
- Consistent error response format
- Request ID tracking
- Support for all HTTP status codes (400, 401, 403, 404, 409, 429, 500, 503)

### 2. Error Response Serializers (`core/serializers.py`)
- `ValidationErrorResponse` - 400 errors
- `UnauthorizedErrorResponse` - 401 errors
- `NotFoundErrorResponse` - 404 errors
- `ForbiddenErrorResponse` - 403 errors
- `ConflictErrorResponse` - 409 errors
- `ServerErrorResponse` - 500 errors

### 3. SPECTACULAR_SETTINGS Configuration
- Enhanced settings in `curator/settings/base.py`
- Swagger UI and ReDoc configurations
- JWT Bearer authentication schema
- Component splitting enabled

### 4. Apps with Complete OpenAPI Schemas
- ✅ **accounts** - All authentication and user management endpoints
- ✅ **outfits** - All outfit CRUD and interaction endpoints
- ✅ **wardrobe** - All wardrobe management endpoints
- ✅ **oauth_views** - Google and Facebook OAuth endpoints

### 5. Apps Remaining (Follow Same Pattern)
- ⏳ **notifications** - Notification management
- ⏳ **cart** - Shopping cart operations
- ⏳ **social** - Social feed and posts
- ⏳ **lookbooks** - Lookbook management

---

## 📋 Pattern for Adding Schemas

### Step 1: Import Required Modules

```python
from rest_framework import serializers
from drf_spectacular.utils import (
    extend_schema, 
    OpenApiParameter, 
    inline_serializer,
    OpenApiTypes
)
from core.serializers import (
    ValidationErrorResponse,
    UnauthorizedErrorResponse,
    NotFoundErrorResponse,
    ForbiddenErrorResponse,
    ConflictErrorResponse,
)
```

### Step 2: Add @extend_schema Decorator

#### For GET (List) Endpoints:
```python
@extend_schema(
    summary="List items",
    description="Get paginated list of items",
    tags=["Items"],
    parameters=[
        OpenApiParameter(name='page', description='Page number', required=False, type=int),
        OpenApiParameter(name='search', description='Search query', required=False, type=str),
    ],
    responses={
        200: inline_serializer(
            name='ItemListResponse',
            fields={
                'count': serializers.IntegerField(),
                'next': serializers.URLField(allow_null=True),
                'previous': serializers.URLField(allow_null=True),
                'results': ItemSerializer(many=True),
            }
        ),
        401: UnauthorizedErrorResponse,
    }
)
def get(self, request, *args, **kwargs):
    return super().get(request, *args, **kwargs)
```

#### For GET (Detail) Endpoints:
```python
@extend_schema(
    summary="Get item details",
    description="Retrieve detailed information about an item",
    tags=["Items"],
    responses={
        200: inline_serializer(
            name='ItemDetailResponse',
            fields={
                'success': serializers.BooleanField(),
                'message': serializers.CharField(),
                'data': ItemSerializer(),
            }
        ),
        401: UnauthorizedErrorResponse,
        404: NotFoundErrorResponse,
    }
)
def get(self, request, *args, **kwargs):
    return super().get(request, *args, **kwargs)
```

#### For POST (Create) Endpoints:
```python
@extend_schema(
    summary="Create item",
    description="Create a new item",
    tags=["Items"],
    request=ItemCreateSerializer,
    responses={
        201: inline_serializer(
            name='ItemCreateResponse',
            fields={
                'success': serializers.BooleanField(),
                'message': serializers.CharField(),
                'data': ItemSerializer(),
            }
        ),
        400: ValidationErrorResponse,
        401: UnauthorizedErrorResponse,
    }
)
def post(self, request, *args, **kwargs):
    return super().post(request, *args, **kwargs)
```

#### For PUT/PATCH (Update) Endpoints:
```python
@extend_schema(
    summary="Update item",
    description="Update item details",
    tags=["Items"],
    request=ItemUpdateSerializer,
    responses={
        200: inline_serializer(
            name='ItemUpdateResponse',
            fields={
                'success': serializers.BooleanField(),
                'message': serializers.CharField(),
                'data': ItemSerializer(),
            }
        ),
        400: ValidationErrorResponse,
        401: UnauthorizedErrorResponse,
        403: ForbiddenErrorResponse,
        404: NotFoundErrorResponse,
    }
)
def put(self, request, *args, **kwargs):
    return super().put(request, *args, **kwargs)
```

#### For DELETE Endpoints:
```python
@extend_schema(
    summary="Delete item",
    description="Delete an item",
    tags=["Items"],
    responses={
        204: OpenApiTypes.NONE,
        401: UnauthorizedErrorResponse,
        403: ForbiddenErrorResponse,
        404: NotFoundErrorResponse,
    }
)
def delete(self, request, *args, **kwargs):
    return super().delete(request, *args, **kwargs)
```

#### For Custom Action Endpoints:
```python
@extend_schema(
    summary="Custom action",
    description="Perform custom action on item",
    tags=["Items"],
    request=inline_serializer(
        name='CustomActionRequest',
        fields={
            'field1': serializers.CharField(required=True),
            'field2': serializers.IntegerField(required=False),
        }
    ),
    responses={
        200: inline_serializer(
            name='CustomActionResponse',
            fields={
                'success': serializers.BooleanField(),
                'message': serializers.CharField(),
                'data': serializers.DictField(),
            }
        ),
        400: ValidationErrorResponse,
        401: UnauthorizedErrorResponse,
        404: NotFoundErrorResponse,
    }
)
def post(self, request, pk):
    # Implementation
    pass
```

#### For File Upload Endpoints:
```python
@extend_schema(
    summary="Upload file",
    description="Upload a file",
    tags=["Items"],
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'file': {'type': 'string', 'format': 'binary'},
                'description': {'type': 'string'},
            },
            'required': ['file']
        }
    },
    responses={
        201: inline_serializer(
            name='FileUploadResponse',
            fields={
                'success': serializers.BooleanField(),
                'data': FileSerializer(),
            }
        ),
        400: ValidationErrorResponse,
        401: UnauthorizedErrorResponse,
    }
)
def post(self, request):
    # Implementation
    pass
```

---

## 🔍 Common Error Response Codes

| Status Code | Error Response | Use Case |
|------------|----------------|----------|
| 400 | `ValidationErrorResponse` | Invalid input, validation errors |
| 401 | `UnauthorizedErrorResponse` | Missing/invalid authentication |
| 403 | `ForbiddenErrorResponse` | Insufficient permissions |
| 404 | `NotFoundErrorResponse` | Resource not found |
| 409 | `ConflictErrorResponse` | Resource conflict (duplicate, etc.) |
| 429 | `ValidationErrorResponse` | Rate limit exceeded |
| 500 | `ServerErrorResponse` | Internal server error |

---

## 📝 Checklist for Each View

- [ ] Import required modules
- [ ] Add `@extend_schema` decorator with:
  - [ ] `summary` - Brief description
  - [ ] `description` - Detailed description
  - [ ] `tags` - API grouping
  - [ ] `request` - Request body schema (if applicable)
  - [ ] `parameters` - Query parameters (if applicable)
  - [ ] `responses` - All possible response codes with schemas
- [ ] Include error responses for all possible error cases
- [ ] Use appropriate serializers for success responses
- [ ] Test schema generation at `/api/schema/`

---

## 🚀 Testing the Schema

1. **View Schema JSON:**
   ```
   GET /api/schema/
   ```

2. **View Swagger UI:**
   ```
   GET /api/schema/swagger-ui/
   ```

3. **View ReDoc:**
   ```
   GET /api/schema/redoc/
   ```

4. **Generate TypeScript Types (Frontend):**
   ```bash
   npx openapi-typescript https://your-api-url/api/schema/ -o ./src/types/api.ts
   ```

---

## 📚 Examples

See completed implementations in:
- `apps/accounts/views.py` - Authentication endpoints
- `apps/outfits/views.py` - Outfit management
- `apps/wardrobe/views.py` - Wardrobe management
- `apps/accounts/oauth_views.py` - OAuth endpoints

---

## 🎯 Next Steps

1. Complete remaining apps (notifications, cart, social, lookbooks)
2. Test all endpoints in Swagger UI
3. Generate TypeScript types on frontend
4. Update frontend to use generated types
5. Add examples to schema (optional but recommended)

---

## 📖 Resources

- [drf-spectacular Documentation](https://drf-spectacular.readthedocs.io/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [DRF Serializers](https://www.django-rest-framework.org/api-guide/serializers/)

