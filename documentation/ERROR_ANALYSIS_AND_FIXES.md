# Error Analysis and Fixes

## 🔍 Error Breakdown

### 1. **Image 404 Errors** (Most Common)
```
Failed to load resource: the server responded with a status of 404
/media/posts/post_53_1_9331.jpg
/media/avatars/avatar_8_3111.jpg
```

**Root Cause:**
- Database has old records with `ImageField` paths (e.g., `posts/post_53_1_9331.jpg`)
- Files were saved to Vercel's **ephemeral filesystem** (deleted on each deployment)
- `_url` fields (`avatar_url`, `image_url`, etc.) are **empty** for old records
- Serializers fall back to `ImageField` URLs when `_url` is empty → 404 errors

**Why This Happens:**
1. Old seeding created records with `ImageField` files
2. Vercel's filesystem is **ephemeral** (files don't persist)
3. New `_url` fields were added but old records weren't updated
4. Frontend tries to load `/media/...` URLs that don't exist

**Solution:**
Run the seed script to populate `_url` fields for all existing records:
```bash
venv\Scripts\python.exe scripts/seed_with_images.py
```

This will:
- Update all users with `avatar_url`
- Update all outfits with `main_image_url`
- Update all outfit items with `image_url`
- Update all lookbooks with `cover_image_url`
- Update all wardrobe items with `primary_image_url`
- Update all post images with `image_url`

---

### 2. **401 Unauthorized - Cart Endpoint**
```
/api/v1/cart/34/:1 Failed to load resource: the server responded with a status of 401
```

**Root Cause:**
- Cart endpoints require authentication (`IsAuthenticated` permission)
- Frontend is calling `/api/v1/cart/34/` **without** a JWT token in the Authorization header
- Or the token is expired/invalid

**Why This Happens:**
- Frontend isn't sending the `Authorization: Bearer <token>` header
- User might not be logged in
- Token might have expired

**Solution:**
**Frontend Fix:**
```javascript
// Ensure all cart API calls include the auth token
fetch('/api/v1/cart/34/', {
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  }
})
```

**Backend Status:** ✅ Already correct - requires authentication

---

### 3. **404 Not Found - ML Search Endpoint**
```
/ml/search/upload:1 Failed to load resource: the server responded with a status of 404
```

**Root Cause:**
- Frontend is calling `/ml/search/upload`
- This endpoint **doesn't exist** in the backend
- The correct endpoint should be `/api/v1/search/visual/` (but it's not implemented yet)

**Why This Happens:**
- Frontend was built expecting a visual search endpoint
- Backend doesn't have this endpoint implemented
- Documentation shows it should exist at `/api/v1/search/visual/` but it's not in the codebase

**Solution Options:**

**Option A: Create the Endpoint (Recommended)**
Create a placeholder endpoint that returns a "not implemented" message:
```python
# apps/search/views.py (create new app)
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class VisualSearchView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        return Response({
            'success': False,
            'message': 'Visual search is not yet implemented. Coming soon!'
        }, status=status.HTTP_501_NOT_IMPLEMENTED)
```

**Option B: Update Frontend (Quick Fix)**
Remove or disable the visual search feature until backend is ready:
```javascript
// In frontend, catch the error gracefully
try {
  await fetch('/ml/search/upload', {...});
} catch (error) {
  console.log('Visual search not available yet');
  // Show user-friendly message
}
```

---

### 4. **Uncaught Promise Errors**
```
Uncaught (in promise) Object
```

**Root Cause:**
- These are **cascading errors** from the failed requests above
- When image loading fails (404), or API calls fail (401/404), JavaScript promises reject
- If errors aren't caught with `.catch()`, they become "Uncaught Promise" errors

**Why This Happens:**
- Frontend code doesn't have proper error handling for:
  - Image load failures
  - API request failures
  - Network errors

**Solution:**
Add proper error handling in frontend:
```javascript
// For image loading
<img 
  src={imageUrl} 
  onError={(e) => {
    e.target.src = '/placeholder-image.jpg'; // Fallback
    console.log('Image failed to load:', imageUrl);
  }}
/>

// For API calls
fetch('/api/v1/cart/34/', {...})
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
  })
  .catch(error => {
    console.error('API Error:', error);
    // Show user-friendly error message
  });
```

---

## 🛠️ Quick Fixes Summary

### **Immediate Actions:**

1. **Fix Image 404s** (Most Important):
   ```bash
   # Run this to populate _url fields for all existing records
   venv\Scripts\python.exe scripts/seed_with_images.py
   ```

2. **Fix Cart 401**:
   - Ensure frontend sends `Authorization: Bearer <token>` header
   - Check if user is logged in before calling cart endpoints

3. **Fix ML Search 404**:
   - Either create the endpoint (Option A above)
   - Or update frontend to handle missing endpoint gracefully (Option B)

4. **Fix Uncaught Promises**:
   - Add `.catch()` handlers to all `fetch()` calls
   - Add `onError` handlers to all `<img>` tags

---

## 📊 Priority Order

1. **HIGH**: Run `seed_with_images.py` to fix image 404s
2. **HIGH**: Fix cart authentication (frontend needs to send token)
3. **MEDIUM**: Create or disable ML search endpoint
4. **LOW**: Add error handling to prevent uncaught promises

---

## 🔄 Long-term Solutions

### **For Image Storage:**
- ✅ Already implemented: `_url` fields for external URLs
- ✅ Serializers prioritize `_url` over `ImageField`
- ⚠️ Need to: Update all existing records with `_url` values
- 💡 Future: Consider S3/Cloudinary for persistent image storage

### **For Authentication:**
- ✅ Backend already requires authentication
- ⚠️ Need to: Ensure frontend always sends tokens
- 💡 Future: Add token refresh logic

### **For Visual Search:**
- ⚠️ Not implemented yet
- 💡 Future: Integrate with ML service or implement basic image search

---

## ✅ Verification

After running `seed_with_images.py`, verify:
```sql
-- Check if _url fields are populated
SELECT COUNT(*) FROM users WHERE avatar_url IS NOT NULL AND avatar_url != '';
SELECT COUNT(*) FROM outfits WHERE main_image_url IS NOT NULL AND main_image_url != '';
SELECT COUNT(*) FROM post_images WHERE image_url IS NOT NULL AND image_url != '';
```

All counts should be > 0 for records that have images.

