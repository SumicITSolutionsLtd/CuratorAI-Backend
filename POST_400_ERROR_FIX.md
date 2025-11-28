# POST /api/v1/social/posts/ 400 Error Fix

## 🔍 Error Analysis

**Error:** `POST /api/v1/social/posts/ 400 (Bad Request)`

**Root Cause:**
The frontend is likely sending JSON data with `image_urls` field, but the serializer wasn't properly handling it. The serializer now supports both:
- `image_urls`: List of image URLs (for JSON requests)
- `images_data`: List of image files (for multipart/form-data)
- Legacy `images`: File uploads via multipart/form-data (backward compatibility)

## ✅ What Was Fixed

### 1. **PostCreateSerializer** (`apps/social/serializers.py`)
- ✅ Added `image_urls` field (list of URLs)
- ✅ Added `images_data` field (list of image files)
- ✅ Updated `create()` method to handle both file uploads and URLs
- ✅ Properly sets user from request context

### 2. **PostCreateView** (`apps/social/views.py`)
- ✅ Updated to pass request context to serializer
- ✅ Handles both JSON (with `image_urls`) and multipart/form-data (with `images`)
- ✅ Backward compatible with legacy `images` field

### 3. **ML Search Endpoint** (`apps/search/`)
- ✅ Created new `search` app
- ✅ Added `/ml/search/upload` endpoint (returns 501 Not Implemented)
- ✅ Added `/api/v1/search/visual/` endpoint (returns 501 Not Implemented)
- ✅ Prevents 404 errors, returns user-friendly message

## 📝 How to Use

### **JSON Request (with image URLs):**
```json
POST /api/v1/social/posts/
Content-Type: application/json
Authorization: Bearer <token>

{
  "caption": "Check out my new outfit!",
  "tags": ["fashion", "outfit"],
  "image_urls": [
    "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800",
    "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800"
  ],
  "privacy": "public"
}
```

### **Multipart Request (with file uploads):**
```javascript
const formData = new FormData();
formData.append('caption', 'Check out my new outfit!');
formData.append('tags', JSON.stringify(['fashion', 'outfit']));
formData.append('images', file1);
formData.append('images', file2);

fetch('/api/v1/social/posts/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
  },
  body: formData
});
```

### **Mixed (files + URLs):**
```json
{
  "caption": "My outfit",
  "images_data": [/* file objects */],
  "image_urls": ["https://example.com/image.jpg"]
}
```

## 🔧 Testing

Use the test dashboard to test the endpoint:
1. Go to `/test-dashboard/`
2. Select `POST /api/v1/social/posts/`
3. The example body will auto-populate with all fields
4. Add your `image_urls` array
5. Test the endpoint

## ✅ Status

- ✅ Serializer supports `image_urls` (JSON)
- ✅ Serializer supports `images_data` (multipart)
- ✅ View handles both request types
- ✅ Backward compatible with legacy `images` field
- ✅ ML search endpoint created (returns 501, not 404)

