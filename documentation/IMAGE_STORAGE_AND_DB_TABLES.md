# Image Storage & Database Tables Guide

## 📸 Image Storage in Database

### How Images Are Stored

**Django ImageField:**
- ❌ **NOT stored directly in database** (images are binary files, too large for DB)
- ✅ **Stored in filesystem** (local `media/` folder or cloud storage like S3)
- ✅ **Database stores only the file path** (e.g., `"outfits/outfit_123.jpg"`)

**URLField (External Images):**
- ✅ **Stored in database as text** (URL string)
- ✅ Used for external image URLs (e.g., Unsplash, CDN)
- ✅ Examples: `main_image_url`, `avatar_url`, `cover_image_url`, `image_url`

### Current Setup

**Local Development:**
```python
MEDIA_ROOT = BASE_DIR / 'media'  # Images stored in project/media/
MEDIA_URL = 'media/'              # URL prefix for accessing images
```

**Production (Vercel/Cloud):**
- Currently configured for **AWS S3** (but `USE_S3 = False` by default)
- When enabled, images upload to S3 bucket
- Database stores S3 URL path

**Image Storage Options:**

1. **Local Filesystem** (Current - Development)
   - Images saved to `media/` folder
   - ❌ Not suitable for production (Vercel has ephemeral filesystem)
   - ✅ Good for development/testing

2. **AWS S3** (Recommended for Production)
   - Images uploaded to S3 bucket
   - ✅ Persistent storage
   - ✅ CDN support
   - ✅ Scalable
   - Configured but disabled (`USE_S3 = False`)

3. **External URLs** (Current - Production)
   - Store image URLs in database (`*_image_url` fields)
   - ✅ No storage costs
   - ✅ Fast (CDN)
   - ✅ Used by seeding script (Unsplash URLs)

### Image Fields in Models

**All models support BOTH:**
- `ImageField` - For file uploads (stored in filesystem/S3)
- `URLField` - For external URLs (stored in database as text)

**Priority in API Responses:**
- Serializers return `*_image_url` first (if set)
- Falls back to `ImageField` URL if `image_url` is empty
- This ensures frontend always gets working URLs

### Image Upload Endpoints

✅ **Working Image Upload Endpoints:**

1. **Wardrobe Items:**
   ```
   POST /api/v1/wardrobe/items/<id>/images/
   Content-Type: multipart/form-data
   Body: { image: <file>, is_primary: true/false }
   ```

2. **Social Posts:**
   ```
   POST /api/v1/social/posts/
   Content-Type: multipart/form-data
   Body: { caption: "...", images: [<file1>, <file2>, ...] }
   ```

3. **Outfits:**
   ```
   POST /api/v1/outfits/
   Content-Type: multipart/form-data
   Body: { title: "...", main_image: <file>, ... }
   ```

4. **Lookbooks:**
   ```
   POST /api/v1/lookbooks/create/
   Content-Type: multipart/form-data
   Body: { title: "...", cover_image: <file>, ... }
   ```

5. **User Avatars:**
   ```
   PATCH /api/v1/auth/me/
   Content-Type: multipart/form-data
   Body: { avatar: <file>, ... }
   ```

## 📊 Database Tables Status

### ✅ All Required Tables Exist

**Social Feed Tables:**
- ✅ `posts` - Main post table
- ✅ `post_images` - Post images (1-10 per post)
- ✅ `post_likes` - Post likes
- ✅ `post_saves` - Saved posts
- ✅ `comments` - Post comments
- ✅ `comment_likes` - Comment likes

**Outfits Tables:**
- ✅ `outfits` - Main outfit table
- ✅ `outfit_items` - Outfit items
- ✅ `outfit_likes` - Outfit likes
- ✅ `outfit_saves` - Saved outfits

**Lookbooks Tables:**
- ✅ `lookbooks` - Main lookbook table
- ✅ `lookbook_outfits` - Outfits in lookbooks
- ✅ `lookbook_likes` - Lookbook likes

**Wardrobe Tables:**
- ✅ `wardrobes` - User wardrobes
- ✅ `wardrobe_items` - Wardrobe items
- ✅ `wardrobe_item_images` - Additional item images
- ✅ `wardrobe_item_attributes` - Custom attributes
- ✅ `wardrobe_item_wear_logs` - Wear tracking

**Cart Tables:**
- ✅ `shopping_carts` - User carts
- ✅ `cart_items` - Cart items
- ✅ `promo_codes` - Promo codes

**Account Tables:**
- ✅ `users` - User accounts
- ✅ `user_profiles` - User profiles
- ✅ `style_preferences` - Style preferences
- ✅ `follows` - User follows

**Other Tables:**
- ✅ `notifications` - User notifications
- ✅ `notification_preferences` - Notification settings

### Verify Tables in Database

Run this to check all tables:
```bash
venv\Scripts\python.exe scripts/migrate_production.py
```

This will:
1. Connect to your database
2. List all required tables
3. Show which exist and which are missing
4. Run migrations if needed

## 🔧 Enabling S3 Storage (Production)

To enable S3 storage for production:

1. **Set Environment Variables in Vercel:**
   ```
   USE_S3=True
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   AWS_STORAGE_BUCKET_NAME=your_bucket
   AWS_S3_REGION_NAME=us-east-1
   ```

2. **Settings will automatically:**
   - Use S3 for file storage
   - Store images in S3 bucket
   - Database stores S3 URLs

## 📝 Summary

**Images in Database:**
- ❌ Image files are NOT stored in database (too large)
- ✅ Image file paths/URLs ARE stored in database
- ✅ External image URLs (URLField) stored as text in database
- ✅ File uploads stored in filesystem or S3

**Database Tables:**
- ✅ All social feed tables exist
- ✅ All outfit tables exist
- ✅ All lookbook tables exist
- ✅ All wardrobe tables exist
- ✅ All cart tables exist
- ✅ All account tables exist

**Current Image Strategy:**
- Development: Local filesystem (`media/` folder)
- Production: External URLs (Unsplash) stored in database
- Future: S3 storage for uploaded images

