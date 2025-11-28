# Social Feed Tables Explanation

## 📊 How Social Feed Works

**Important:** There is **NO separate "feeds" table**. The social feed is **dynamically generated** from existing tables.

### Tables Used by Social Feed

The `/api/v1/social/feed/` endpoint uses these tables:

1. **`posts`** - Main table for all social posts
   - This is the PRIMARY table for social feed
   - Contains all post data (caption, privacy, metrics, etc.)

2. **`user_following`** - User follow relationships
   - Required for "following" feed type
   - Links users who follow each other
   - Table name: `user_following` (in accounts app)

3. **`post_images`** - Images for posts
   - Linked to posts via foreign key

4. **`post_likes`** - Post likes
   - Used for engagement metrics

5. **`post_saves`** - Saved posts
   - Used for engagement metrics

6. **`comments`** - Post comments
   - Used for engagement metrics

### Feed Types

The social feed endpoint supports 3 feed types:

1. **Following Feed** (`type=following`)
   - Queries `posts` table
   - Filters by users in `user_following` table
   - Shows posts from users you follow

2. **Trending Feed** (`type=trending`)
   - Queries `posts` table
   - Orders by `likes_count` and `created_at`
   - Shows most popular posts

3. **Discover Feed** (`type=discover`)
   - Queries `posts` table
   - Shows all public posts (excluding your own)

### CRUD Operations for Social Feed

**The feed itself is READ-ONLY** (no CRUD on feed). CRUD operations are on the underlying tables:

#### **Posts CRUD:**
- ✅ **CREATE**: `POST /api/v1/social/posts/` → Creates record in `posts` table
- ✅ **READ**: `GET /api/v1/social/feed/` → Reads from `posts` table
- ✅ **READ**: `GET /api/v1/social/posts/<id>/` → Reads single post from `posts` table
- ✅ **UPDATE**: `PATCH /api/v1/social/posts/<id>/update/` → Updates `posts` table
- ✅ **DELETE**: `DELETE /api/v1/social/posts/<id>/delete/` → Soft deletes in `posts` table

#### **Post Images CRUD:**
- ✅ **CREATE**: Included in `POST /api/v1/social/posts/` → Creates records in `post_images` table
- ✅ **READ**: Included in post responses → Reads from `post_images` table

#### **Post Likes/Saves CRUD:**
- ✅ **CREATE**: `POST /api/v1/social/posts/<id>/like/` → Creates record in `post_likes` table
- ✅ **DELETE**: `POST /api/v1/social/posts/<id>/like/` (toggle) → Deletes from `post_likes` table
- ✅ **CREATE**: `POST /api/v1/social/posts/<id>/save/` → Creates record in `post_saves` table
- ✅ **DELETE**: `DELETE /api/v1/social/posts/<id>/save/` → Deletes from `post_saves` table

#### **Comments CRUD:**
- ✅ **CREATE**: `POST /api/v1/social/posts/<id>/comments/add/` → Creates record in `comments` table
- ✅ **READ**: `GET /api/v1/social/posts/<id>/comments/` → Reads from `comments` table
- ✅ **UPDATE**: `PATCH /api/v1/social/comments/<id>/update/` → Updates `comments` table
- ✅ **DELETE**: `DELETE /api/v1/social/comments/<id>/delete/` → Soft deletes in `comments` table

#### **Following CRUD:**
- ✅ **CREATE**: `POST /api/v1/auth/users/<id>/follow/` → Creates record in `user_following` table
- ✅ **DELETE**: `DELETE /api/v1/auth/users/<id>/follow/` → Deletes from `user_following` table
- ✅ **READ**: `GET /api/v1/auth/users/<id>/followers/` → Reads from `user_following` table
- ✅ **READ**: `GET /api/v1/auth/users/<id>/following/` → Reads from `user_following` table

## ✅ All Required Tables

### Social Feed Tables:
- ✅ `posts` - **Main feed table** (all posts)
- ✅ `post_images` - Post images
- ✅ `post_likes` - Post likes
- ✅ `post_saves` - Saved posts
- ✅ `comments` - Post comments
- ✅ `comment_likes` - Comment likes
- ✅ `user_following` - **Required for following feed** (in accounts app)

### Verification

Run the migration script to verify all tables:
```bash
venv\Scripts\python.exe scripts/migrate_production.py
```

This will check if `user_following` table exists (it should, as it's part of accounts app migrations).

## 🔍 Why No Separate "Feeds" Table?

**Design Decision:**
- Feeds are **dynamic** - they change based on:
  - Who you follow (changes over time)
  - Post popularity (changes over time)
  - New posts (added constantly)
  
- Storing feeds in a separate table would require:
  - Constant updates when new posts are created
  - Constant updates when follow relationships change
  - Complex synchronization logic
  - Storage overhead

**Better Approach:**
- Query `posts` table dynamically
- Filter by `user_following` relationships
- Order by engagement metrics
- Fast with proper indexes (already added)

## 📝 Summary

✅ **All social feed tables exist:**
- `posts` - Main feed data
- `user_following` - Follow relationships (for following feed)
- `post_images`, `post_likes`, `post_saves`, `comments`, `comment_likes` - Supporting tables

✅ **All CRUD operations work:**
- Posts: Create, Read, Update, Delete
- Post Images: Create, Read
- Post Likes/Saves: Create, Delete (toggle)
- Comments: Create, Read, Update, Delete
- Following: Create, Read, Delete

✅ **Feed is dynamically generated** from `posts` table with proper filtering and ordering.

