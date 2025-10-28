# CuratorAI Backend - Complete API Documentation
## Production-Ready Endpoint Specification

**Version:** 1.0.0
**Base URL:** `http://localhost:8000/api/v1` (Development)
**Base URL:** `https://api.curatorai.com/api/v1` (Production)
**Authentication:** JWT Bearer Token
**Date Generated:** 2025-10-28

---

## Table of Contents

1. [Authentication](#1-authentication)
2. [User Management](#2-user-management)
3. [Wardrobe Management](#3-wardrobe-management)
4. [Outfit Management](#4-outfit-management)
5. [Outfit Recommendations](#5-outfit-recommendations)
6. [Visual Search](#6-visual-search)
7. [Social Feed & Posts](#7-social-feed--posts)
8. [Lookbooks](#8-lookbooks)
9. [Shopping Cart](#9-shopping-cart)
10. [Notifications](#10-notifications)
11. [Admin Dashboard](#11-admin-dashboard)
12. [WebSocket Events](#12-websocket-events)
13. [Data Models](#13-data-models)
14. [Error Handling](#14-error-handling)
15. [Rate Limiting](#15-rate-limiting)

---

## Overview

### Current Implementation Status

| Module | Status | Endpoints Implemented | Total Endpoints | Completion |
|--------|--------|----------------------|----------------|------------|
| Authentication | ✅ Complete | 11/11 | 11 | 100% |
| User Management | ✅ Complete | 8/8 | 8 | 100% |
| Outfit Management | ✅ Complete | 9/9 | 9 | 100% |
| Wardrobe Management | ❌ Not Started | 0/8 | 8 | 0% |
| Recommendations | ❌ Not Started | 0/4 | 4 | 0% |
| Visual Search | ❌ Not Started | 0/5 | 5 | 0% |
| Social Feed | ❌ Not Started | 0/11 | 11 | 0% |
| Lookbooks | ❌ Not Started | 0/8 | 8 | 0% |
| Shopping Cart | ❌ Not Started | 0/8 | 8 | 0% |
| Notifications | ❌ Not Started | 0/6 | 6 | 0% |
| Admin Dashboard | ❌ Not Started | 0/8 | 8 | 0% |
| **TOTAL** | **19% Complete** | **28/86** | **86** | **33%** |

---

## Authentication

All requests (except registration and login) require a JWT token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Token Lifecycle
- **Access Token Lifetime:** 15 minutes
- **Refresh Token Lifetime:** 7 days
- **Rotation:** New refresh token issued on each refresh
- **Blacklisting:** Tokens blacklisted on logout

---

## 1. Authentication

### 1.1 Register New User

**Status:** ✅ Implemented

```http
POST /api/v1/auth/register/
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "agreeToTerms": true
}
```

**Response:** `201 Created`
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "avatar": null,
    "bio": "",
    "is_verified": false,
    "created_at": "2025-10-28T10:00:00Z",
    "profile": {
      "gender": null,
      "date_of_birth": null,
      "country": null,
      "body_type": null,
      "height": null,
      "top_size": null,
      "bottom_size": null,
      "shoe_size": null
    },
    "preferences": {
      "preferred_styles": [],
      "preferred_colors": [],
      "preferred_brands": [],
      "budget_min": 0,
      "budget_max": 10000,
      "currency": "USD",
      "occasions": []
    }
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**Validation:**
- Email must be unique and valid format
- Password minimum 8 characters
- Username 3-30 characters, alphanumeric + underscore
- agreeToTerms must be true

**Errors:**
- `400 Bad Request` - Validation errors
- `409 Conflict` - Email or username already exists

---

### 1.2 Login

**Status:** ✅ Implemented

```http
POST /api/v1/auth/login/
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "avatar": "https://cdn.curatorai.com/avatars/...",
    "bio": "Fashion enthusiast",
    "is_verified": true,
    "created_at": "2025-10-28T10:00:00Z",
    "profile": { /* ... */ },
    "preferences": { /* ... */ }
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**Errors:**
- `401 Unauthorized` - Invalid credentials
- `403 Forbidden` - Account suspended/banned

---

### 1.3 OAuth Login (Google/Facebook)

**Status:** ⚠️ Partially Implemented (needs testing)

```http
POST /api/v1/auth/oauth/{provider}/
Content-Type: application/json
```

**Path Parameters:**
- `provider`: `google` | `facebook`

**Request Body:**
```json
{
  "token": "google-oauth-token-here"
}
```

**Response:** `200 OK`
```json
{
  "user": { /* user object */ },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "is_new_user": true
}
```

**Errors:**
- `400 Bad Request` - Invalid OAuth token
- `401 Unauthorized` - OAuth provider verification failed

---

### 1.4 Refresh Token

**Status:** ✅ Implemented

```http
POST /api/v1/auth/refresh/
Content-Type: application/json
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access_token_expiration": "2025-10-28T10:15:00Z"
}
```

**Errors:**
- `401 Unauthorized` - Invalid or expired refresh token
- `403 Forbidden` - Token blacklisted

---

### 1.5 Logout

**Status:** ✅ Implemented

```http
POST /api/v1/auth/logout/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "message": "Successfully logged out"
}
```

**Notes:**
- Blacklists the refresh token
- Access token remains valid until expiration (15 min)

---

### 1.6 Get Current User

**Status:** ✅ Implemented

```http
GET /api/v1/auth/me/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "avatar": "https://cdn.curatorai.com/avatars/...",
  "bio": "Fashion enthusiast",
  "is_verified": true,
  "created_at": "2025-10-28T10:00:00Z",
  "updated_at": "2025-10-28T12:00:00Z",
  "profile": {
    "gender": "M",
    "date_of_birth": "1990-01-15",
    "phone_number": "+1234567890",
    "country": "US",
    "city": "New York",
    "body_type": "athletic",
    "height": 175,
    "weight": 70,
    "top_size": "M",
    "bottom_size": "32",
    "shoe_size": "10",
    "dress_size": null
  },
  "preferences": {
    "preferred_styles": ["casual", "street", "minimal"],
    "preferred_colors": ["black", "white", "navy", "gray"],
    "preferred_brands": ["Nike", "Adidas", "Uniqlo"],
    "preferred_patterns": ["solid", "stripes"],
    "budget_min": 50,
    "budget_max": 500,
    "currency": "USD",
    "occasions": ["casual", "work", "sport"],
    "prefer_sustainable": true,
    "prefer_secondhand": false,
    "fit_preference": "regular"
  },
  "stats": {
    "followers_count": 245,
    "following_count": 180,
    "outfits_count": 32,
    "posts_count": 18,
    "wardrobe_items_count": 87
  }
}
```

---

### 1.7 Update Current User

**Status:** ✅ Implemented

```http
PUT /api/v1/auth/me/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body (all fields optional):**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe_updated",
  "bio": "Updated bio",
  "profile": {
    "gender": "M",
    "date_of_birth": "1990-01-15",
    "phone_number": "+1234567890",
    "country": "US",
    "city": "New York",
    "body_type": "athletic",
    "height": 175,
    "weight": 70,
    "top_size": "M",
    "bottom_size": "32",
    "shoe_size": "10"
  },
  "preferences": {
    "preferred_styles": ["casual", "street"],
    "preferred_colors": ["black", "white"],
    "budget_min": 50,
    "budget_max": 500,
    "currency": "USD",
    "occasions": ["casual", "work"],
    "prefer_sustainable": true
  }
}
```

**Response:** `200 OK`
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "username": "johndoe_updated",
  /* ... updated user data ... */
}
```

**Errors:**
- `400 Bad Request` - Validation errors
- `409 Conflict` - Username already taken

---

### 1.8 Request Password Reset

**Status:** ❌ Not Implemented

```http
POST /api/v1/auth/password-reset/request/
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:** `200 OK`
```json
{
  "message": "If an account exists with this email, a reset code has been sent",
  "code_expires_in": 900
}
```

**Implementation Notes:**
- Send 6-digit verification code via email
- Code expires in 15 minutes
- Rate limit: 3 requests per hour per email
- Always return 200 (don't reveal if email exists)

---

### 1.9 Confirm Password Reset

**Status:** ❌ Not Implemented

```http
POST /api/v1/auth/password-reset/confirm/
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "code": "123456",
  "new_password": "NewSecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "message": "Password successfully reset"
}
```

**Errors:**
- `400 Bad Request` - Invalid code or expired
- `429 Too Many Requests` - Too many attempts

---

### 1.10 Request Email Verification

**Status:** ❌ Not Implemented

```http
POST /api/v1/auth/verify-email/request/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "message": "Verification code sent to your email",
  "code_expires_in": 900
}
```

---

### 1.11 Confirm Email Verification

**Status:** ❌ Not Implemented

```http
POST /api/v1/auth/verify-email/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "code": "123456"
}
```

**Response:** `200 OK`
```json
{
  "message": "Email successfully verified",
  "user": {
    "is_verified": true
  }
}
```

---

## 2. User Management

### 2.1 Get User Profile by ID

**Status:** ✅ Implemented

```http
GET /api/v1/users/{userId}/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "id": "uuid-string",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "avatar": "https://cdn.curatorai.com/avatars/...",
  "bio": "Fashion enthusiast",
  "is_verified": true,
  "created_at": "2025-10-28T10:00:00Z",
  "stats": {
    "followers_count": 245,
    "following_count": 180,
    "outfits_count": 32,
    "posts_count": 18
  },
  "is_following": false,
  "is_followed_by": false
}
```

**Privacy:**
- Email not exposed (only for own profile)
- Preferences not exposed (only for own profile)
- Profile visibility respects user privacy settings

---

### 2.2 Search Users

**Status:** ❌ Not Implemented

```http
GET /api/v1/users/search?q={query}&limit={limit}&offset={offset}
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `q` (required): Search query (username, full name)
- `limit` (optional): Results per page (default: 20, max: 50)
- `offset` (optional): Pagination offset (default: 0)

**Response:** `200 OK`
```json
{
  "count": 42,
  "next": "/api/v1/users/search?q=john&limit=20&offset=20",
  "previous": null,
  "results": [
    {
      "id": "uuid-string",
      "username": "johndoe",
      "full_name": "John Doe",
      "avatar": "https://cdn.curatorai.com/avatars/...",
      "bio": "Fashion enthusiast",
      "is_verified": true,
      "followers_count": 245,
      "is_following": false
    }
  ]
}
```

---

### 2.3 Follow User

**Status:** ✅ Implemented

```http
POST /api/v1/users/{userId}/follow/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "message": "Successfully followed user",
  "is_following": true
}
```

**Errors:**
- `400 Bad Request` - Cannot follow yourself
- `404 Not Found` - User not found

---

### 2.4 Unfollow User

**Status:** ✅ Implemented

```http
DELETE /api/v1/users/{userId}/follow/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "message": "Successfully unfollowed user",
  "is_following": false
}
```

---

### 2.5 Get User Followers

**Status:** ✅ Implemented

```http
GET /api/v1/users/{userId}/followers/?page={page}&limit={limit}
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Results per page (default: 20, max: 100)

**Response:** `200 OK`
```json
{
  "count": 245,
  "next": "/api/v1/users/{userId}/followers/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid-string",
      "username": "follower1",
      "full_name": "Jane Smith",
      "avatar": "https://cdn.curatorai.com/avatars/...",
      "is_verified": true,
      "is_following": false,
      "followed_at": "2025-10-20T14:30:00Z"
    }
  ]
}
```

---

### 2.6 Get User Following

**Status:** ✅ Implemented

```http
GET /api/v1/users/{userId}/following/?page={page}&limit={limit}
Authorization: Bearer {access_token}
```

**Response:** Same format as 2.5

---

### 2.7 Delete Account

**Status:** ❌ Not Implemented

```http
DELETE /api/v1/users/{userId}/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "password": "user_password",
  "confirmation": "DELETE MY ACCOUNT"
}
```

**Response:** `204 No Content`

**Implementation Notes:**
- Soft delete (mark as deleted, don't remove from database)
- Anonymize personal data
- Keep content but mark as [deleted user]
- Remove from public search results
- Can only delete own account

---

## 3. Wardrobe Management

**Status:** ❌ Module Not Implemented

### 3.1 Get User Wardrobe

```http
GET /api/v1/users/{userId}/wardrobe/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "id": "uuid-string",
  "user_id": "uuid-string",
  "total_items": 87,
  "categories": {
    "tops": 25,
    "bottoms": 18,
    "shoes": 12,
    "accessories": 15,
    "outerwear": 8,
    "dresses": 9
  },
  "created_at": "2025-10-28T10:00:00Z",
  "updated_at": "2025-10-28T15:00:00Z"
}
```

---

### 3.2 Get Wardrobe Items

```http
GET /api/v1/wardrobe/items?category={category}&color={color}&season={season}&page={page}
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `category` (optional): `top` | `bottom` | `shoes` | `accessory` | `outerwear` | `dress` | `bag`
- `color` (optional): Color filter
- `season` (optional): `spring` | `summer` | `fall` | `winter` | `all`
- `brand` (optional): Brand name
- `tags` (optional): Comma-separated tags
- `page` (optional): Page number
- `limit` (optional): Results per page (default: 20)

**Response:** `200 OK`
```json
{
  "count": 87,
  "next": "/api/v1/wardrobe/items?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid-string",
      "wardrobe_id": "uuid-string",
      "category": "top",
      "name": "White Cotton T-Shirt",
      "brand": "Uniqlo",
      "color": "white",
      "size": "M",
      "price": 19.99,
      "currency": "USD",
      "images": [
        "https://cdn.curatorai.com/wardrobe/items/...",
        "https://cdn.curatorai.com/wardrobe/items/..."
      ],
      "attributes": [
        {
          "key": "Material",
          "value": "100% Cotton"
        },
        {
          "key": "Fit",
          "value": "Regular"
        }
      ],
      "tags": ["casual", "summer", "basic"],
      "times_worn": 15,
      "purchase_link": "https://www.uniqlo.com/...",
      "purchase_date": "2024-06-15",
      "created_at": "2025-10-28T10:00:00Z",
      "updated_at": "2025-10-28T15:00:00Z"
    }
  ]
}
```

---

### 3.3 Get Single Wardrobe Item

```http
GET /api/v1/wardrobe/items/{itemId}/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "id": "uuid-string",
  "wardrobe_id": "uuid-string",
  "category": "top",
  "name": "White Cotton T-Shirt",
  /* ... all fields from 3.2 ... */
  "worn_dates": [
    "2025-10-20",
    "2025-10-18",
    "2025-10-15"
  ],
  "used_in_outfits": [
    {
      "id": "outfit-uuid",
      "name": "Casual Weekend",
      "thumbnail": "https://cdn.curatorai.com/..."
    }
  ]
}
```

---

### 3.4 Add Wardrobe Item

```http
POST /api/v1/wardrobe/items/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Request Body (FormData):**
```
category: "top"
name: "White Cotton T-Shirt"
brand: "Uniqlo"
color: "white"
size: "M"
price: 19.99
currency: "USD"
images: [File, File]  // Array of image files
attributes: '[{"key": "Material", "value": "100% Cotton"}]'  // JSON string
tags: '["casual", "summer"]'  // JSON string
purchase_link: "https://www.uniqlo.com/..."
purchase_date: "2024-06-15"
```

**Response:** `201 Created`
```json
{
  "id": "uuid-string",
  "wardrobe_id": "uuid-string",
  /* ... all item fields ... */
}
```

**Validation:**
- Images: Max 5 images, max 5MB each, formats: JPEG, PNG, WebP
- Name: Required, max 200 characters
- Category: Required, valid enum value
- Price: Optional, must be positive

---

### 3.5 Update Wardrobe Item

```http
PATCH /api/v1/wardrobe/items/{itemId}/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body (all fields optional):**
```json
{
  "name": "Updated Name",
  "color": "blue",
  "tags": ["casual", "summer", "favorite"],
  "notes": "My favorite shirt"
}
```

**Response:** `200 OK`
```json
{
  "id": "uuid-string",
  /* ... updated item data ... */
}
```

---

### 3.6 Delete Wardrobe Item

```http
DELETE /api/v1/wardrobe/items/{itemId}/
Authorization: Bearer {access_token}
```

**Response:** `204 No Content`

**Implementation Notes:**
- Soft delete recommended (keep history)
- Remove from active wardrobe but keep in outfit history
- Update wardrobe statistics

---

### 3.7 Upload Wardrobe Item Image

```http
POST /api/v1/wardrobe/items/{itemId}/images/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Request Body:**
```
image: [File]  // Single image file
is_primary: true  // Optional, default: false
```

**Response:** `201 Created`
```json
{
  "id": "image-uuid",
  "item_id": "item-uuid",
  "image_url": "https://cdn.curatorai.com/wardrobe/items/...",
  "is_primary": true,
  "created_at": "2025-10-28T15:00:00Z"
}
```

---

### 3.8 Mark Item as Worn

```http
POST /api/v1/wardrobe/items/{itemId}/worn/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "date": "2025-10-28",
  "outfit_id": "outfit-uuid"  // Optional
}
```

**Response:** `200 OK`
```json
{
  "message": "Item marked as worn",
  "times_worn": 16,
  "last_worn": "2025-10-28"
}
```

---

### 3.9 Get Wardrobe Statistics

```http
GET /api/v1/users/{userId}/wardrobe/stats/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "total_items": 87,
  "total_value": 4250.00,
  "currency": "USD",
  "categories": {
    "tops": 25,
    "bottoms": 18,
    "shoes": 12,
    "accessories": 15,
    "outerwear": 8,
    "dresses": 9
  },
  "colors": {
    "black": 18,
    "white": 15,
    "blue": 12,
    "gray": 10
  },
  "brands": {
    "Uniqlo": 12,
    "Zara": 8,
    "Nike": 6
  },
  "most_worn_items": [
    {
      "id": "item-uuid",
      "name": "White Cotton T-Shirt",
      "times_worn": 25,
      "image": "https://cdn.curatorai.com/..."
    }
  ],
  "least_worn_items": [
    {
      "id": "item-uuid",
      "name": "Fancy Dress",
      "times_worn": 1,
      "image": "https://cdn.curatorai.com/..."
    }
  ],
  "average_wear_per_item": 5.2,
  "items_never_worn": 12
}
```

---

## 4. Outfit Management

**Status:** ✅ Module Complete

### 4.1 List Outfits

**Status:** ✅ Implemented

```http
GET /api/v1/outfits/?occasion={occasion}&season={season}&search={query}&page={page}
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `occasion` (optional): `casual` | `work` | `formal` | `party` | `sport` | `date` | `travel`
- `season` (optional): `spring` | `summer` | `fall` | `winter` | `all`
- `search` (optional): Search in title/description
- `page` (optional): Page number (default: 1)
- `limit` (optional): Results per page (default: 20)

**Response:** `200 OK`
```json
{
  "count": 156,
  "next": "/api/v1/outfits/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid-string",
      "user": {
        "id": "user-uuid",
        "username": "johndoe",
        "avatar": "https://cdn.curatorai.com/..."
      },
      "title": "Summer Casual Vibes",
      "description": "Perfect for a weekend brunch",
      "main_image": "https://cdn.curatorai.com/outfits/...",
      "thumbnail": "https://cdn.curatorai.com/outfits/thumb/...",
      "occasion": "casual",
      "season": "summer",
      "style_tags": ["casual", "minimalist", "comfortable"],
      "color_palette": ["white", "beige", "denim"],
      "items": [
        {
          "id": "item-uuid",
          "item_type": "top",
          "name": "White Linen Shirt",
          "brand": "Uniqlo",
          "image": "https://cdn.curatorai.com/...",
          "price": 39.99,
          "currency": "USD",
          "purchase_url": "https://..."
        }
      ],
      "total_price": 189.99,
      "currency": "USD",
      "is_public": true,
      "likes_count": 45,
      "saves_count": 23,
      "views_count": 320,
      "is_liked": false,
      "is_saved": false,
      "created_at": "2025-10-28T10:00:00Z",
      "updated_at": "2025-10-28T15:00:00Z"
    }
  ]
}
```

---

### 4.2 Get Single Outfit

**Status:** ✅ Implemented

```http
GET /api/v1/outfits/{outfitId}/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "id": "uuid-string",
  "user": {
    "id": "user-uuid",
    "username": "johndoe",
    "full_name": "John Doe",
    "avatar": "https://cdn.curatorai.com/...",
    "is_following": false
  },
  "title": "Summer Casual Vibes",
  "description": "Perfect for a weekend brunch with friends...",
  "main_image": "https://cdn.curatorai.com/outfits/...",
  "thumbnail": "https://cdn.curatorai.com/outfits/thumb/...",
  "occasion": "casual",
  "season": "summer",
  "style_tags": ["casual", "minimalist", "comfortable"],
  "color_palette": ["white", "beige", "denim"],
  "items": [
    {
      "id": "item-uuid",
      "item_type": "top",
      "name": "White Linen Shirt",
      "brand": "Uniqlo",
      "image": "https://cdn.curatorai.com/...",
      "price": 39.99,
      "currency": "USD",
      "size": "M",
      "color": "white",
      "material": "100% Linen",
      "purchase_url": "https://www.uniqlo.com/...",
      "affiliate_link": "https://affiliate.link/...",
      "is_available": true
    }
  ],
  "total_price": 189.99,
  "currency": "USD",
  "ai_generated": false,
  "confidence_score": 0.92,
  "is_public": true,
  "likes_count": 45,
  "saves_count": 23,
  "views_count": 321,
  "is_liked": false,
  "is_saved": false,
  "created_at": "2025-10-28T10:00:00Z",
  "updated_at": "2025-10-28T15:00:00Z"
}
```

**Implementation Notes:**
- View count incremented on each GET request
- User can only see private outfits if they are the owner

---

### 4.3 Create Outfit

**Status:** ✅ Implemented

```http
POST /api/v1/outfits/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Request Body (FormData):**
```
title: "Summer Casual Vibes"
description: "Perfect for a weekend brunch"
occasion: "casual"
season: "summer"
style_tags: '["casual", "minimalist"]'  // JSON string
color_palette: '["white", "beige", "denim"]'  // JSON string
is_public: true
main_image: [File]  // Image file

items: '[
  {
    "item_type": "top",
    "name": "White Linen Shirt",
    "brand": "Uniqlo",
    "price": 39.99,
    "currency": "USD",
    "size": "M",
    "color": "white",
    "purchase_url": "https://...",
    "wardrobe_item_id": "item-uuid"  // Optional, if from wardrobe
  }
]'  // JSON string

item_images: [File, File, ...]  // Array of item image files
```

**Response:** `201 Created`
```json
{
  "id": "uuid-string",
  /* ... complete outfit data ... */
}
```

**Validation:**
- Title: Required, max 200 characters
- Items: At least 2 items required
- Main image: Required, max 10MB, formats: JPEG, PNG, WebP
- Total price: Auto-calculated from items

---

### 4.4 Update Outfit

**Status:** ✅ Implemented

```http
PATCH /api/v1/outfits/{outfitId}/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body (all fields optional):**
```json
{
  "title": "Updated Title",
  "description": "Updated description",
  "occasion": "work",
  "season": "fall",
  "is_public": false,
  "style_tags": ["professional", "modern"]
}
```

**Response:** `200 OK`
```json
{
  "id": "uuid-string",
  /* ... updated outfit data ... */
}
```

**Permissions:**
- Only owner can update outfit
- Cannot change items after creation (delete and recreate instead)

---

### 4.5 Delete Outfit

**Status:** ✅ Implemented

```http
DELETE /api/v1/outfits/{outfitId}/
Authorization: Bearer {access_token}
```

**Response:** `204 No Content`

**Permissions:**
- Only owner can delete outfit

---

### 4.6 Like/Unlike Outfit

**Status:** ✅ Implemented

```http
POST /api/v1/outfits/{outfitId}/like/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "message": "Outfit liked successfully",
  "is_liked": true,
  "likes_count": 46
}
```

**Implementation Notes:**
- Toggle behavior: If already liked, it unlikes
- Real-time notification sent to outfit owner
- Updates outfit likes_count

---

### 4.7 Save/Unsave Outfit

**Status:** ✅ Implemented

```http
POST /api/v1/outfits/{outfitId}/save/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body (optional):**
```json
{
  "collection_name": "Summer Favorites"
}
```

**Response:** `200 OK`
```json
{
  "message": "Outfit saved successfully",
  "is_saved": true,
  "saves_count": 24,
  "collection_name": "Summer Favorites"
}
```

**Implementation Notes:**
- Toggle behavior: If already saved, it unsaves
- Collection name is optional (defaults to "Saved")
- User can have multiple collections

---

### 4.8 Get User's Outfits

**Status:** ✅ Implemented

```http
GET /api/v1/outfits/user/{userId}/?page={page}&limit={limit}
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "count": 32,
  "next": "/api/v1/outfits/user/{userId}/?page=2",
  "previous": null,
  "results": [
    /* ... array of outfit objects ... */
  ]
}
```

**Privacy:**
- Only shows public outfits unless viewing own profile

---

### 4.9 Get Saved Outfits

**Status:** ❌ Not Implemented (backend has data, needs endpoint)

```http
GET /api/v1/users/{userId}/saved-outfits/?collection={collection}&page={page}
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `collection` (optional): Filter by collection name
- `page` (optional): Page number
- `limit` (optional): Results per page

**Response:** `200 OK`
```json
{
  "count": 28,
  "collections": ["Summer Favorites", "Work Outfits", "Date Night"],
  "results": [
    {
      "outfit": {
        /* ... outfit object ... */
      },
      "saved_at": "2025-10-28T15:00:00Z",
      "collection_name": "Summer Favorites"
    }
  ]
}
```

---

### 4.10 Provide Outfit Feedback

**Status:** ❌ Not Implemented

```http
POST /api/v1/outfits/{outfitId}/feedback/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "helpful": true,
  "feedback": "Love the color combination!"
}
```

**Response:** `201 Created`
```json
{
  "message": "Thank you for your feedback",
  "helpful_count": 42
}
```

---

## 5. Outfit Recommendations

**Status:** ❌ Module Not Implemented

### 5.1 Get Personalized Recommendations

```http
POST /api/v1/outfits/recommendations/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_id": "uuid-string",
  "filters": {
    "occasion": "casual",
    "season": "summer",
    "budget_max": 300,
    "style": ["minimalist", "casual"],
    "colors": ["white", "black", "gray"]
  },
  "page": 1,
  "limit": 10
}
```

**Response:** `200 OK`
```json
{
  "count": 45,
  "next": "/api/v1/outfits/recommendations/?page=2",
  "previous": null,
  "results": [
    {
      "id": "recommendation-uuid",
      "outfit": {
        /* ... complete outfit object ... */
      },
      "score": 0.95,
      "match_percentage": 95,
      "reasons": [
        "Matches your preferred style",
        "Within your budget range",
        "Perfect for casual occasions",
        "Uses colors from your preferences"
      ],
      "confidence": 0.92,
      "created_at": "2025-10-28T15:00:00Z"
    }
  ],
  "recommendation_context": {
    "based_on": "Your style preferences and wardrobe",
    "algorithm_version": "2.1.0",
    "generated_at": "2025-10-28T15:00:00Z"
  }
}
```

**Implementation Notes:**
- Uses ML recommendation service
- Considers user preferences, wardrobe, past likes/saves
- Real-time generation (may be slow, consider caching)
- Can filter recommendations by various criteria

---

### 5.2 Get Similar Outfits

**Status:** ❌ Not Implemented

```http
GET /api/v1/outfits/{outfitId}/similar/?limit={limit}
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `limit` (optional): Number of results (default: 10, max: 50)
- `similarity_threshold` (optional): Min similarity score 0-1 (default: 0.7)

**Response:** `200 OK`
```json
{
  "outfit_id": "uuid-string",
  "similar_outfits": [
    {
      "outfit": {
        /* ... outfit object ... */
      },
      "similarity_score": 0.92,
      "matching_attributes": [
        "Similar color palette",
        "Same occasion",
        "Similar style tags"
      ]
    }
  ]
}
```

**Implementation Notes:**
- Uses outfit embedding vectors for similarity search
- Consider caching results for popular outfits

---

### 5.3 Get Trending Outfits

**Status:** ❌ Not Implemented

```http
GET /api/v1/outfits/trending/?period={period}&limit={limit}
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `period` (optional): `day` | `week` | `month` (default: week)
- `limit` (optional): Number of results (default: 20)

**Response:** `200 OK`
```json
{
  "period": "week",
  "updated_at": "2025-10-28T15:00:00Z",
  "results": [
    {
      "outfit": {
        /* ... outfit object ... */
      },
      "trending_score": 0.95,
      "metrics": {
        "views_growth": 320,
        "likes_growth": 45,
        "saves_growth": 23
      }
    }
  ]
}
```

**Implementation Notes:**
- Calculate trending score based on:
  - Recent engagement (likes, saves, views)
  - Growth rate
  - Recency
- Update periodically via Celery task
- Cache results for performance

---

### 5.4 Get Daily Outfit Suggestion

**Status:** ❌ Not Implemented

```http
GET /api/v1/recommendations/daily/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "date": "2025-10-28",
  "outfit": {
    /* ... complete outfit object ... */
  },
  "reason": "Based on your schedule and weather forecast",
  "weather": {
    "temperature": 72,
    "condition": "sunny",
    "location": "New York"
  },
  "occasion_detected": "work"
}
```

**Implementation Notes:**
- One suggestion per day per user
- Consider weather API integration
- Consider user's calendar/schedule if available
- Cache daily suggestions

---

## 6. Visual Search

**Status:** ❌ Module Not Implemented
**ML Service URL:** Separate ML service (port 8001)

### 6.1 Visual Search by Image Upload

```http
POST /api/v1/search/visual/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Request Body (FormData):**
```
image: [File]  // Image file to search
similarity_threshold: 0.7  // Optional, 0-1
remove_duplicates: true  // Optional
filters: '{
  "occasion": "casual",
  "price_max": 300,
  "season": "summer"
}'  // Optional JSON string
```

**Response:** `200 OK`
```json
{
  "search_id": "search-uuid",
  "query": {
    "image_url": "https://cdn.curatorai.com/searches/...",
    "uploaded_at": "2025-10-28T15:00:00Z"
  },
  "results": [
    {
      "id": "result-uuid",
      "outfit": {
        /* ... complete outfit object ... */
      },
      "similarity_score": 0.95,
      "match_percentage": 95,
      "matched_features": [
        "Color palette",
        "Style composition",
        "Item types"
      ],
      "matched_items": [
        {
          "query_item": "detected top in image",
          "matched_item": {
            "id": "item-uuid",
            "name": "White Linen Shirt",
            "similarity": 0.92
          }
        }
      ]
    }
  ],
  "total_results": 24,
  "processing_time_ms": 1250,
  "metadata": {
    "detected_items": [
      {
        "type": "top",
        "color": "white",
        "bounding_box": [0.2, 0.3, 0.6, 0.7]
      }
    ],
    "detected_styles": ["casual", "minimalist"],
    "dominant_colors": ["white", "beige", "blue"]
  }
}
```

**Implementation Notes:**
- Process image with ML service to extract features
- Compare against outfit database using embedding vectors
- Store search history for user
- Rate limit: 10 searches per minute per user
- Max image size: 10MB
- Supported formats: JPEG, PNG, WebP

---

### 6.2 Visual Search by URL

```http
POST /api/v1/search/visual/url/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "image_url": "https://example.com/fashion-image.jpg",
  "similarity_threshold": 0.7,
  "filters": {
    "occasion": "casual",
    "price_max": 300
  }
}
```

**Response:** `200 OK`
```json
{
  /* ... same as 6.1 ... */
}
```

---

### 6.3 Get Search Status

```http
GET /api/v1/search/status/{searchId}/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "search_id": "search-uuid",
  "status": "processing",
  "progress": 65,
  "message": "Analyzing image features...",
  "estimated_time_remaining_ms": 500,
  "started_at": "2025-10-28T15:00:00Z"
}
```

**Status Values:**
- `queued` - Search in queue
- `processing` - Currently processing
- `completed` - Search completed
- `failed` - Search failed

---

### 6.4 Get Search History

```http
GET /api/v1/search/recent/{userId}?limit={limit}
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `limit` (optional): Number of results (default: 20, max: 100)

**Response:** `200 OK`
```json
{
  "count": 45,
  "results": [
    {
      "id": "search-uuid",
      "image_url": "https://cdn.curatorai.com/searches/...",
      "thumbnail_url": "https://cdn.curatorai.com/searches/thumb/...",
      "results_count": 24,
      "timestamp": "2025-10-28T15:00:00Z"
    }
  ]
}
```

---

### 6.5 Delete Search History

```http
DELETE /api/v1/search/history/{userId}/
Authorization: Bearer {access_token}
```

**Response:** `204 No Content`

---

## 7. Social Feed & Posts

**Status:** ❌ Module Not Implemented

### 7.1 Get Social Feed

```http
POST /api/v1/social/feed/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "type": "following",
  "limit": 20,
  "offset": 0
}
```

**Feed Types:**
- `following` - Posts from users you follow
- `discover` - Recommended posts based on interests
- `trending` - Popular posts
- `nearby` - Posts from users in your area (if location enabled)

**Response:** `200 OK`
```json
{
  "count": 245,
  "next": "/api/v1/social/feed/?offset=20",
  "previous": null,
  "results": [
    {
      "id": "post-uuid",
      "user": {
        "id": "user-uuid",
        "username": "fashionista",
        "full_name": "Jane Doe",
        "avatar": "https://cdn.curatorai.com/...",
        "is_verified": true
      },
      "images": [
        "https://cdn.curatorai.com/posts/...",
        "https://cdn.curatorai.com/posts/..."
      ],
      "caption": "OOTD for today's brunch! 🌞☕",
      "tags": ["ootd", "casual", "weekend"],
      "tagged_items": [
        {
          "id": "item-uuid",
          "name": "White Linen Shirt",
          "brand": "Zara",
          "purchase_url": "https://..."
        }
      ],
      "outfit_id": "outfit-uuid",
      "likes": 342,
      "comments": 28,
      "shares": 15,
      "saves": 67,
      "is_liked": false,
      "is_saved": false,
      "privacy": "public",
      "created_at": "2025-10-28T10:00:00Z",
      "updated_at": "2025-10-28T10:00:00Z"
    }
  ]
}
```

---

### 7.2 Get Single Post

```http
GET /api/v1/social/posts/{postId}/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "id": "post-uuid",
  "user": {
    "id": "user-uuid",
    "username": "fashionista",
    "full_name": "Jane Doe",
    "avatar": "https://cdn.curatorai.com/...",
    "is_verified": true,
    "followers_count": 5420
  },
  "images": [
    "https://cdn.curatorai.com/posts/...",
    "https://cdn.curatorai.com/posts/..."
  ],
  "caption": "OOTD for today's brunch! 🌞☕",
  "tags": ["ootd", "casual", "weekend"],
  "tagged_items": [
    {
      "id": "item-uuid",
      "name": "White Linen Shirt",
      "brand": "Zara",
      "image": "https://cdn.curatorai.com/...",
      "price": 39.99,
      "currency": "USD",
      "purchase_url": "https://...",
      "position": {
        "x": 0.5,
        "y": 0.3
      }
    }
  ],
  "outfit": {
    "id": "outfit-uuid",
    "title": "Summer Casual",
    "thumbnail": "https://cdn.curatorai.com/..."
  },
  "likes": 342,
  "comments": 28,
  "shares": 15,
  "saves": 67,
  "views": 1420,
  "is_liked": false,
  "is_saved": false,
  "privacy": "public",
  "location": {
    "name": "New York, NY",
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "created_at": "2025-10-28T10:00:00Z",
  "updated_at": "2025-10-28T10:00:00Z"
}
```

---

### 7.3 Create Post

```http
POST /api/v1/social/posts/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Request Body (FormData):**
```
images: [File, File, ...]  // 1-10 images
caption: "OOTD for today's brunch! 🌞☕"
tags: '["ootd", "casual", "weekend"]'  // JSON string
tagged_items: '[
  {
    "wardrobe_item_id": "item-uuid",
    "position": {"x": 0.5, "y": 0.3}
  }
]'  // JSON string
outfit_id: "outfit-uuid"  // Optional
privacy: "public"  // public | friends | private
location: '{"name": "New York, NY", "latitude": 40.7128, "longitude": -74.0060}'  // Optional JSON
```

**Response:** `201 Created`
```json
{
  "id": "post-uuid",
  /* ... complete post object ... */
}
```

**Validation:**
- Images: 1-10 images required, max 10MB each
- Caption: Max 2200 characters
- Tags: Max 30 tags, max 50 characters each

---

### 7.4 Update Post

```http
PATCH /api/v1/social/posts/{postId}/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body (all fields optional):**
```json
{
  "caption": "Updated caption",
  "tags": ["updated", "tags"],
  "privacy": "friends"
}
```

**Response:** `200 OK`
```json
{
  "id": "post-uuid",
  /* ... updated post object ... */
}
```

**Permissions:**
- Only owner can update post
- Cannot change images after creation

---

### 7.5 Delete Post

```http
DELETE /api/v1/social/posts/{postId}/
Authorization: Bearer {access_token}
```

**Response:** `204 No Content`

**Permissions:**
- Only owner can delete post
- Soft delete recommended (keep for analytics)

---

### 7.6 Like/Unlike Post

```http
POST /api/v1/social/posts/{postId}/like/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "message": "Post liked successfully",
  "is_liked": true,
  "likes_count": 343
}
```

**Implementation Notes:**
- Toggle behavior: If already liked, it unlikes
- Real-time notification to post owner
- WebSocket event emitted

---

### 7.7 Save/Unsave Post

```http
POST /api/v1/social/posts/{postId}/save/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "message": "Post saved successfully",
  "is_saved": true,
  "saves_count": 68
}
```

---

### 7.8 Share Post

```http
POST /api/v1/social/posts/{postId}/share/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "platform": "internal",
  "message": "Check this out!"
}
```

**Platforms:**
- `internal` - Share within CuratorAI
- `instagram` - Share to Instagram (if integrated)
- `twitter` - Share to Twitter (if integrated)
- `facebook` - Share to Facebook (if integrated)

**Response:** `200 OK`
```json
{
  "message": "Post shared successfully",
  "shares_count": 16,
  "share_url": "https://curatorai.com/posts/{postId}"
}
```

---

### 7.9 Get Post Comments

```http
GET /api/v1/social/posts/{postId}/comments?page={page}&limit={limit}
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Results per page (default: 20)
- `sort` (optional): `recent` | `popular` (default: recent)

**Response:** `200 OK`
```json
{
  "count": 28,
  "next": "/api/v1/social/posts/{postId}/comments?page=2",
  "previous": null,
  "results": [
    {
      "id": "comment-uuid",
      "post_id": "post-uuid",
      "user": {
        "id": "user-uuid",
        "username": "commenter",
        "full_name": "John Smith",
        "avatar": "https://cdn.curatorai.com/...",
        "is_verified": false
      },
      "content": "Love this outfit! Where did you get the shirt?",
      "likes": 12,
      "is_liked": false,
      "parent_comment_id": null,
      "replies_count": 3,
      "replies": [
        {
          "id": "reply-uuid",
          "user": {
            "id": "user-uuid",
            "username": "fashionista",
            "full_name": "Jane Doe",
            "avatar": "https://cdn.curatorai.com/..."
          },
          "content": "@commenter It's from Zara!",
          "likes": 5,
          "is_liked": false,
          "created_at": "2025-10-28T10:15:00Z"
        }
      ],
      "created_at": "2025-10-28T10:10:00Z",
      "updated_at": "2025-10-28T10:10:00Z"
    }
  ]
}
```

---

### 7.10 Add Comment

```http
POST /api/v1/social/posts/{postId}/comments/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "content": "Love this outfit!",
  "parent_comment_id": null
}
```

**Response:** `201 Created`
```json
{
  "id": "comment-uuid",
  "post_id": "post-uuid",
  "user": {
    /* ... current user data ... */
  },
  "content": "Love this outfit!",
  "likes": 0,
  "is_liked": false,
  "parent_comment_id": null,
  "replies_count": 0,
  "created_at": "2025-10-28T10:10:00Z"
}
```

**Validation:**
- Content: Required, max 500 characters
- parent_comment_id: Must exist if provided

---

### 7.11 Update Comment

```http
PATCH /api/v1/social/comments/{commentId}/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "content": "Updated comment text"
}
```

**Response:** `200 OK`
```json
{
  "id": "comment-uuid",
  /* ... updated comment object ... */
}
```

**Permissions:**
- Only owner can update comment
- 15-minute edit window

---

### 7.12 Delete Comment

```http
DELETE /api/v1/social/comments/{commentId}/
Authorization: Bearer {access_token}
```

**Response:** `204 No Content`

**Permissions:**
- Owner can delete own comment
- Post owner can delete any comment on their post
- Moderators/admins can delete any comment

---

### 7.13 Like/Unlike Comment

```http
POST /api/v1/social/comments/{commentId}/like/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "message": "Comment liked successfully",
  "is_liked": true,
  "likes_count": 13
}
```

---

## 8. Lookbooks

**Status:** ❌ Module Not Implemented

### 8.1 Get Lookbooks

```http
GET /api/v1/lookbooks?page={page}&limit={limit}&featured={featured}
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `page` (optional): Page number
- `limit` (optional): Results per page (default: 20)
- `season` (optional): `spring` | `summer` | `fall` | `winter`
- `occasion` (optional): Occasion filter
- `price_min` (optional): Min price
- `price_max` (optional): Max price
- `style` (optional): Comma-separated styles
- `featured` (optional): Boolean, show only featured

**Response:** `200 OK`
```json
{
  "count": 45,
  "next": "/api/v1/lookbooks?page=2",
  "previous": null,
  "results": [
    {
      "id": "lookbook-uuid",
      "creator": {
        "id": "user-uuid",
        "username": "stylist",
        "full_name": "Jane Stylist",
        "avatar": "https://cdn.curatorai.com/...",
        "is_verified": true
      },
      "title": "Summer Essentials 2025",
      "description": "Must-have pieces for your summer wardrobe",
      "cover_image": "https://cdn.curatorai.com/lookbooks/...",
      "outfits_count": 12,
      "outfits": [
        {
          "id": "outfit-uuid",
          "thumbnail": "https://cdn.curatorai.com/...",
          "title": "Beach Day Outfit"
        }
      ],
      "price_range": {
        "min": 50,
        "max": 500,
        "currency": "USD"
      },
      "total_value": 2400,
      "season": "summer",
      "occasion": "casual",
      "style": ["casual", "beachy", "relaxed"],
      "tags": ["summer", "beach", "vacation"],
      "likes": 542,
      "views": 3420,
      "comments": 45,
      "is_public": true,
      "is_featured": true,
      "created_at": "2025-06-01T10:00:00Z",
      "updated_at": "2025-10-28T15:00:00Z"
    }
  ]
}
```

---

### 8.2 Get Featured Lookbooks

```http
GET /api/v1/lookbooks/featured?limit={limit}
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `limit` (optional): Number of results (default: 10, max: 20)

**Response:** `200 OK`
```json
{
  "count": 5,
  "results": [
    /* ... array of lookbook objects ... */
  ]
}
```

---

### 8.3 Get Single Lookbook

```http
GET /api/v1/lookbooks/{lookbookId}/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "id": "lookbook-uuid",
  "creator": {
    "id": "user-uuid",
    "username": "stylist",
    "full_name": "Jane Stylist",
    "avatar": "https://cdn.curatorai.com/...",
    "is_verified": true,
    "followers_count": 12500
  },
  "title": "Summer Essentials 2025",
  "description": "Must-have pieces for your summer wardrobe...",
  "cover_image": "https://cdn.curatorai.com/lookbooks/...",
  "outfits": [
    {
      "id": "outfit-uuid",
      "title": "Beach Day Outfit",
      "description": "Perfect for a day at the beach",
      "images": ["https://cdn.curatorai.com/..."],
      "items": [
        {
          "id": "item-uuid",
          "name": "Linen Beach Shirt",
          "brand": "Zara",
          "price": 49.99,
          "currency": "USD",
          "image": "https://cdn.curatorai.com/...",
          "purchase_url": "https://...",
          "is_available": true
        }
      ],
      "total_price": 189.99,
      "currency": "USD"
    }
  ],
  "price_range": {
    "min": 50,
    "max": 500,
    "currency": "USD",
    "average": 200
  },
  "total_value": 2400,
  "season": "summer",
  "occasion": "casual",
  "style": ["casual", "beachy", "relaxed"],
  "tags": ["summer", "beach", "vacation"],
  "likes": 542,
  "views": 3421,
  "comments": 45,
  "is_public": true,
  "is_featured": true,
  "is_liked": false,
  "created_at": "2025-06-01T10:00:00Z",
  "updated_at": "2025-10-28T15:00:00Z"
}
```

---

### 8.4 Create Lookbook

```http
POST /api/v1/lookbooks/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Request Body (FormData):**
```
title: "Summer Essentials 2025"
description: "Must-have pieces for your summer wardrobe"
cover_image: [File]  // Image file
outfit_ids: '["outfit-uuid-1", "outfit-uuid-2"]'  // JSON string array
season: "summer"
occasion: "casual"
style: '["casual", "beachy", "relaxed"]'  // JSON string
tags: '["summer", "beach", "vacation"]'  // JSON string
is_public: true
```

**Response:** `201 Created`
```json
{
  "id": "lookbook-uuid",
  /* ... complete lookbook object ... */
}
```

**Validation:**
- Title: Required, max 200 characters
- Description: Max 2000 characters
- Outfits: At least 3 outfits required
- Cover image: Required, max 10MB

---

### 8.5 Update Lookbook

```http
PATCH /api/v1/lookbooks/{lookbookId}/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body (all fields optional):**
```json
{
  "title": "Updated Title",
  "description": "Updated description",
  "outfit_ids": ["outfit-uuid-1", "outfit-uuid-2", "outfit-uuid-3"],
  "is_public": true,
  "tags": ["updated", "tags"]
}
```

**Response:** `200 OK`
```json
{
  "id": "lookbook-uuid",
  /* ... updated lookbook object ... */
}
```

**Permissions:**
- Only creator can update lookbook

---

### 8.6 Delete Lookbook

```http
DELETE /api/v1/lookbooks/{lookbookId}/
Authorization: Bearer {access_token}
```

**Response:** `204 No Content`

**Permissions:**
- Only creator can delete lookbook

---

### 8.7 Like/Unlike Lookbook

```http
POST /api/v1/lookbooks/{lookbookId}/like/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "message": "Lookbook liked successfully",
  "is_liked": true,
  "likes_count": 543
}
```

---

### 8.8 Get Lookbook Comments

```http
GET /api/v1/lookbooks/{lookbookId}/comments?page={page}&limit={limit}
Authorization: Bearer {access_token}
```

**Response:** Same format as post comments (7.9)

---

## 9. Shopping Cart

**Status:** ❌ Module Not Implemented

### 9.1 Get Cart

```http
GET /api/v1/cart/{userId}/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "id": "cart-uuid",
  "user_id": "user-uuid",
  "items": [
    {
      "id": "cart-item-uuid",
      "outfit_item_id": "item-uuid",
      "name": "White Linen Shirt",
      "brand": "Zara",
      "price": 39.99,
      "size": "M",
      "color": "white",
      "quantity": 1,
      "image_url": "https://cdn.curatorai.com/...",
      "product_url": "https://www.zara.com/...",
      "in_stock": true,
      "added_at": "2025-10-28T14:00:00Z"
    }
  ],
  "item_count": 5,
  "subtotal": 299.95,
  "shipping": 10.00,
  "tax": 26.99,
  "discount": 0,
  "total": 336.94,
  "currency": "USD",
  "promo_code": null,
  "updated_at": "2025-10-28T15:00:00Z"
}
```

---

### 9.2 Add Item to Cart

```http
POST /api/v1/cart/{userId}/items/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "outfit_item_id": "item-uuid",
  "size": "M",
  "quantity": 1
}
```

**Response:** `201 Created`
```json
{
  "id": "cart-uuid",
  "items": [
    /* ... updated cart items ... */
  ],
  "item_count": 6,
  "total": 376.93,
  "currency": "USD"
}
```

**Validation:**
- outfit_item_id: Must exist and be available for purchase
- quantity: Min 1, max 10

---

### 9.3 Update Cart Item Quantity

```http
PATCH /api/v1/cart/{userId}/items/{itemId}/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "quantity": 2
}
```

**Response:** `200 OK`
```json
{
  "id": "cart-uuid",
  /* ... updated cart ... */
}
```

---

### 9.4 Remove Item from Cart

```http
DELETE /api/v1/cart/{userId}/items/{itemId}/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "message": "Item removed from cart",
  "cart": {
    /* ... updated cart ... */
  }
}
```

---

### 9.5 Apply Promo Code

```http
POST /api/v1/cart/{userId}/promo/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "code": "SUMMER25"
}
```

**Response:** `200 OK`
```json
{
  "message": "Promo code applied successfully",
  "promo_code": "SUMMER25",
  "discount": 59.99,
  "discount_percentage": 20,
  "cart": {
    "subtotal": 299.95,
    "shipping": 10.00,
    "tax": 21.60,
    "discount": 59.99,
    "total": 271.56,
    "currency": "USD"
  }
}
```

**Errors:**
- `400 Bad Request` - Invalid or expired promo code
- `409 Conflict` - Code not applicable to cart items

---

### 9.6 Remove Promo Code

```http
DELETE /api/v1/cart/{userId}/promo/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "message": "Promo code removed",
  "cart": {
    /* ... updated cart without discount ... */
  }
}
```

---

### 9.7 Clear Cart

```http
DELETE /api/v1/cart/{userId}/
Authorization: Bearer {access_token}
```

**Response:** `204 No Content`

---

### 9.8 Calculate Shipping

```http
POST /api/v1/cart/shipping/calculate/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "address": {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "country": "US"
  },
  "items": [
    {
      "item_id": "item-uuid",
      "quantity": 1
    }
  ]
}
```

**Response:** `200 OK`
```json
{
  "shipping_methods": [
    {
      "id": "standard",
      "name": "Standard Shipping",
      "price": 10.00,
      "currency": "USD",
      "estimated_days": 5-7
    },
    {
      "id": "express",
      "name": "Express Shipping",
      "price": 25.00,
      "currency": "USD",
      "estimated_days": 2-3
    }
  ],
  "recommended": "standard"
}
```

---

### 9.9 Get Shipping Methods

```http
GET /api/v1/cart/shipping-methods/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "methods": [
    {
      "id": "standard",
      "name": "Standard Shipping",
      "base_price": 10.00,
      "currency": "USD",
      "estimated_days": "5-7",
      "available_countries": ["US", "CA", "UK"]
    },
    {
      "id": "express",
      "name": "Express Shipping",
      "base_price": 25.00,
      "currency": "USD",
      "estimated_days": "2-3",
      "available_countries": ["US", "CA"]
    }
  ]
}
```

---

## 10. Notifications

**Status:** ❌ Module Not Implemented

### 10.1 Get Notifications

```http
GET /api/v1/notifications/{userId}?type={type}&isRead={isRead}&limit={limit}&offset={offset}
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `type` (optional): `like` | `comment` | `follow` | `recommendation` | `sale` | `system` | `promo`
- `isRead` (optional): Boolean filter
- `limit` (optional): Results per page (default: 20)
- `offset` (optional): Pagination offset

**Response:** `200 OK`
```json
{
  "count": 142,
  "unread_count": 8,
  "next": "/api/v1/notifications/{userId}?offset=20",
  "previous": null,
  "results": [
    {
      "id": "notification-uuid",
      "user_id": "user-uuid",
      "type": "like",
      "title": "New Like",
      "message": "johndoe liked your post",
      "image_url": "https://cdn.curatorai.com/...",
      "action_url": "/posts/post-uuid",
      "actor": {
        "id": "actor-uuid",
        "username": "johndoe",
        "avatar": "https://cdn.curatorai.com/..."
      },
      "is_read": false,
      "created_at": "2025-10-28T14:30:00Z"
    },
    {
      "id": "notification-uuid-2",
      "user_id": "user-uuid",
      "type": "recommendation",
      "title": "New Outfit Recommendations",
      "message": "We found 5 new outfit recommendations for you!",
      "image_url": "https://cdn.curatorai.com/...",
      "action_url": "/recommendations",
      "actor": null,
      "is_read": false,
      "created_at": "2025-10-28T13:00:00Z"
    }
  ]
}
```

---

### 10.2 Get Unread Count

```http
GET /api/v1/notifications/{userId}/unread-count/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "count": 8,
  "by_type": {
    "like": 3,
    "comment": 2,
    "follow": 1,
    "recommendation": 2
  }
}
```

---

### 10.3 Mark Notification as Read

```http
PATCH /api/v1/notifications/{notificationId}/read/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "id": "notification-uuid",
  "is_read": true,
  "read_at": "2025-10-28T15:00:00Z"
}
```

---

### 10.4 Mark All as Read

```http
PATCH /api/v1/notifications/{userId}/read-all/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "message": "All notifications marked as read",
  "count": 8
}
```

---

### 10.5 Delete Notification

```http
DELETE /api/v1/notifications/{notificationId}/
Authorization: Bearer {access_token}
```

**Response:** `204 No Content`

---

### 10.6 Get Notification Preferences

```http
GET /api/v1/notifications/{userId}/preferences/
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "user_id": "user-uuid",
  "email_notifications": {
    "likes": true,
    "comments": true,
    "follows": true,
    "recommendations": false,
    "marketing": false,
    "digest": "weekly"
  },
  "push_notifications": {
    "likes": true,
    "comments": true,
    "follows": true,
    "recommendations": true,
    "marketing": false
  },
  "in_app_notifications": {
    "likes": true,
    "comments": true,
    "follows": true,
    "recommendations": true,
    "system": true
  },
  "do_not_disturb": {
    "enabled": false,
    "start_time": "22:00",
    "end_time": "08:00"
  }
}
```

---

### 10.7 Update Notification Preferences

```http
PATCH /api/v1/notifications/{userId}/preferences/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body (all fields optional):**
```json
{
  "email_notifications": {
    "likes": false,
    "comments": true,
    "digest": "daily"
  },
  "push_notifications": {
    "recommendations": false
  },
  "do_not_disturb": {
    "enabled": true,
    "start_time": "23:00",
    "end_time": "07:00"
  }
}
```

**Response:** `200 OK`
```json
{
  /* ... updated preferences ... */
}
```

---

## 11. Admin Dashboard

**Status:** ❌ Module Not Implemented
**Permissions:** Admin or Moderator role required

### 11.1 Get Dashboard Statistics

```http
GET /api/v1/admin/dashboard/stats/
Authorization: Bearer {access_token}
X-Admin-Role: admin
```

**Response:** `200 OK`
```json
{
  "overview": {
    "total_users": 15420,
    "total_outfits": 45320,
    "total_posts": 23150,
    "total_reports": 42,
    "pending_reports": 12
  },
  "growth": {
    "users": {
      "count": 15420,
      "growth_percentage": 12.5,
      "trend": "up",
      "period": "month"
    },
    "outfits": {
      "count": 45320,
      "growth_percentage": 8.3,
      "trend": "up",
      "period": "month"
    },
    "revenue": {
      "amount": 125420.50,
      "currency": "USD",
      "growth_percentage": 15.2,
      "trend": "up",
      "period": "month"
    }
  },
  "engagement": {
    "daily_active_users": 3420,
    "avg_session_duration_minutes": 18.5,
    "avg_outfits_per_user": 2.9,
    "avg_posts_per_user": 1.5
  },
  "conversion": {
    "signup_to_outfit": 0.68,
    "outfit_to_purchase": 0.12,
    "overall_conversion_rate": 0.082
  }
}
```

---

### 11.2 Get Analytics Data

```http
GET /api/v1/admin/analytics?period={period}&metric={metric}
Authorization: Bearer {access_token}
X-Admin-Role: admin
```

**Query Parameters:**
- `period` (optional): `day` | `week` | `month` | `year` (default: month)
- `metric` (optional): `users` | `outfits` | `posts` | `revenue` | `engagement` | `all` (default: all)
- `start_date` (optional): ISO 8601 date
- `end_date` (optional): ISO 8601 date

**Response:** `200 OK`
```json
{
  "period": "month",
  "start_date": "2025-10-01",
  "end_date": "2025-10-31",
  "metrics": {
    "users": {
      "total": 15420,
      "new": 1720,
      "active": 8420,
      "churned": 120,
      "retention_rate": 0.93
    },
    "content": {
      "outfits_created": 3820,
      "posts_created": 1950,
      "comments": 8420,
      "likes": 42150
    },
    "revenue": {
      "total": 125420.50,
      "currency": "USD",
      "transactions": 1520,
      "avg_order_value": 82.51,
      "refunds": 2340.00
    },
    "engagement": {
      "daily_active_users": 3420,
      "weekly_active_users": 8420,
      "monthly_active_users": 12150,
      "avg_session_duration_minutes": 18.5,
      "bounce_rate": 0.32
    }
  },
  "charts": {
    "users_over_time": [
      {"date": "2025-10-01", "count": 13700},
      {"date": "2025-10-08", "count": 14200},
      {"date": "2025-10-15", "count": 14850},
      {"date": "2025-10-22", "count": 15150},
      {"date": "2025-10-29", "count": 15420}
    ],
    "revenue_over_time": [
      {"date": "2025-10-01", "amount": 28420.50},
      {"date": "2025-10-08", "amount": 32150.00},
      {"date": "2025-10-15", "amount": 29800.00},
      {"date": "2025-10-22", "amount": 35050.00}
    ]
  }
}
```

---

### 11.3 Get Users (Admin View)

```http
GET /api/v1/admin/users?role={role}&status={status}&search={query}&limit={limit}&offset={offset}
Authorization: Bearer {access_token}
X-Admin-Role: admin
```

**Query Parameters:**
- `role` (optional): `user` | `admin` | `moderator`
- `status` (optional): `active` | `suspended` | `banned`
- `search` (optional): Search by username, email, name
- `limit` (optional): Results per page (default: 50)
- `offset` (optional): Pagination offset

**Response:** `200 OK`
```json
{
  "count": 15420,
  "next": "/api/v1/admin/users?offset=50",
  "previous": null,
  "results": [
    {
      "id": "user-uuid",
      "email": "user@example.com",
      "username": "johndoe",
      "full_name": "John Doe",
      "avatar": "https://cdn.curatorai.com/...",
      "role": "user",
      "status": "active",
      "is_verified": true,
      "created_at": "2025-01-15T10:00:00Z",
      "last_login": "2025-10-28T14:00:00Z",
      "stats": {
        "outfits_count": 32,
        "posts_count": 18,
        "followers_count": 245,
        "following_count": 180
      },
      "flags": {
        "reported_count": 0,
        "warnings_count": 0,
        "is_suspicious": false
      }
    }
  ]
}
```

---

### 11.4 Update User Role

```http
PATCH /api/v1/admin/users/{userId}/role/
Authorization: Bearer {access_token}
X-Admin-Role: admin
Content-Type: application/json
```

**Request Body:**
```json
{
  "role": "moderator",
  "reason": "Promoted to moderator for excellent community contributions"
}
```

**Roles:**
- `user` - Regular user
- `moderator` - Can moderate content
- `admin` - Full admin access

**Response:** `200 OK`
```json
{
  "user_id": "user-uuid",
  "role": "moderator",
  "updated_by": "admin-uuid",
  "updated_at": "2025-10-28T15:00:00Z",
  "reason": "Promoted to moderator for excellent community contributions"
}
```

**Permissions:**
- Only admins can change roles
- Cannot demote yourself
- Audit log created

---

### 11.5 Update User Status

```http
PATCH /api/v1/admin/users/{userId}/status/
Authorization: Bearer {access_token}
X-Admin-Role: admin
Content-Type: application/json
```

**Request Body:**
```json
{
  "status": "suspended",
  "reason": "Violation of community guidelines",
  "duration_days": 7,
  "notify_user": true
}
```

**Status Values:**
- `active` - Normal user
- `suspended` - Temporarily suspended (read-only)
- `banned` - Permanently banned

**Response:** `200 OK`
```json
{
  "user_id": "user-uuid",
  "status": "suspended",
  "reason": "Violation of community guidelines",
  "suspended_until": "2025-11-04T15:00:00Z",
  "updated_by": "admin-uuid",
  "updated_at": "2025-10-28T15:00:00Z",
  "notification_sent": true
}
```

**Implementation Notes:**
- User receives email notification
- All active sessions terminated
- Audit log created
- User can appeal via support

---

### 11.6 Get Content Reports

```http
GET /api/v1/admin/reports?status={status}&type={type}&priority={priority}&page={page}
Authorization: Bearer {access_token}
X-Admin-Role: moderator
```

**Query Parameters:**
- `status` (optional): `pending` | `reviewed` | `resolved` | `dismissed`
- `type` (optional): `post` | `comment` | `user` | `outfit`
- `priority` (optional): `low` | `medium` | `high`
- `page` (optional): Page number
- `limit` (optional): Results per page (default: 20)

**Response:** `200 OK`
```json
{
  "count": 42,
  "pending_count": 12,
  "next": "/api/v1/admin/reports?page=2",
  "previous": null,
  "results": [
    {
      "id": "report-uuid",
      "content_type": "post",
      "content_id": "post-uuid",
      "content": {
        "id": "post-uuid",
        "author": {
          "id": "user-uuid",
          "username": "reported_user",
          "avatar": "https://cdn.curatorai.com/..."
        },
        "preview": "Post caption text...",
        "image_url": "https://cdn.curatorai.com/..."
      },
      "reported_by": [
        {
          "id": "reporter-uuid",
          "username": "reporter1",
          "reported_at": "2025-10-28T10:00:00Z",
          "reason": "inappropriate",
          "details": "Offensive language"
        }
      ],
      "report_count": 5,
      "reason": "inappropriate",
      "priority": "high",
      "status": "pending",
      "assigned_to": null,
      "created_at": "2025-10-28T10:00:00Z",
      "updated_at": "2025-10-28T10:00:00Z"
    }
  ]
}
```

**Report Reasons:**
- `inappropriate` - Inappropriate content
- `spam` - Spam or misleading
- `harassment` - Harassment or bullying
- `copyright` - Copyright violation
- `other` - Other reasons

---

### 11.7 Moderate Content

```http
POST /api/v1/admin/moderate/
Authorization: Bearer {access_token}
X-Admin-Role: moderator
Content-Type: application/json
```

**Request Body:**
```json
{
  "action": "remove_content",
  "content_type": "post",
  "content_id": "post-uuid",
  "report_id": "report-uuid",
  "reason": "Violation of community guidelines",
  "notify_user": true,
  "apply_penalty": true,
  "penalty_type": "warning",
  "notes": "First offense, issued warning"
}
```

**Actions:**
- `dismiss` - Dismiss report (no violation)
- `remove_content` - Remove content
- `edit_content` - Edit/censor content
- `warn_user` - Issue warning to user
- `suspend_user` - Suspend user
- `ban_user` - Ban user

**Penalty Types:**
- `warning` - Warning only
- `suspension_1day` - 1 day suspension
- `suspension_7days` - 7 day suspension
- `suspension_30days` - 30 day suspension
- `ban` - Permanent ban

**Response:** `200 OK`
```json
{
  "action": "remove_content",
  "content_type": "post",
  "content_id": "post-uuid",
  "status": "completed",
  "user_notified": true,
  "penalty_applied": {
    "type": "warning",
    "user_id": "user-uuid",
    "warnings_count": 1
  },
  "moderator": "moderator-uuid",
  "timestamp": "2025-10-28T15:00:00Z",
  "report_id": "report-uuid",
  "report_status": "resolved"
}
```

**Implementation Notes:**
- All moderation actions logged
- User receives notification
- Content soft-deleted (recoverable)
- Escalation system for repeat offenders

---

### 11.8 Export Data

```http
GET /api/v1/admin/export?type={type}&format={format}&start_date={date}&end_date={date}
Authorization: Bearer {access_token}
X-Admin-Role: admin
```

**Query Parameters:**
- `type` (required): `users` | `outfits` | `posts` | `analytics` | `reports`
- `format` (optional): `csv` | `json` | `xlsx` (default: csv)
- `start_date` (optional): ISO 8601 date
- `end_date` (optional): ISO 8601 date

**Response:** `200 OK`
```
Content-Type: text/csv (or application/json, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet)
Content-Disposition: attachment; filename="users_export_2025-10-28.csv"

<file content>
```

**Implementation Notes:**
- Async processing for large exports
- Email download link when ready
- Files expire after 24 hours
- Rate limit: 5 exports per hour per admin

---

## 12. WebSocket Events

**Status:** ❌ Not Implemented

**Connection:**
```javascript
const socket = io('ws://localhost:8000', {
  auth: {
    token: accessToken
  }
});
```

### 12.1 Client Events (Emit)

**Join User Room:**
```javascript
socket.emit('join', {
  room: `user_${userId}`
});
```

**Leave User Room:**
```javascript
socket.emit('leave', {
  room: `user_${userId}`
});
```

**Typing Indicator (Comments):**
```javascript
socket.emit('typing', {
  post_id: 'post-uuid',
  is_typing: true
});
```

---

### 12.2 Server Events (Listen)

**New Notification:**
```javascript
socket.on('notification', (data) => {
  // data = {
  //   id: 'notification-uuid',
  //   type: 'like',
  //   title: 'New Like',
  //   message: 'johndoe liked your post',
  //   action_url: '/posts/post-uuid',
  //   created_at: '2025-10-28T15:00:00Z'
  // }
});
```

**New Recommendation:**
```javascript
socket.on('new_recommendation', (data) => {
  // data = {
  //   count: 5,
  //   message: 'We found 5 new outfit recommendations for you!'
  // }
});
```

**Post Liked:**
```javascript
socket.on('post_liked', (data) => {
  // data = {
  //   post_id: 'post-uuid',
  //   likes_count: 46,
  //   liked_by: {
  //     id: 'user-uuid',
  //     username: 'johndoe'
  //   }
  // }
});
```

**New Comment:**
```javascript
socket.on('new_comment', (data) => {
  // data = {
  //   post_id: 'post-uuid',
  //   comment: {
  //     id: 'comment-uuid',
  //     user: { ... },
  //     content: 'Great outfit!',
  //     created_at: '2025-10-28T15:00:00Z'
  //   }
  // }
});
```

**New Follower:**
```javascript
socket.on('new_follower', (data) => {
  // data = {
  //   follower: {
  //     id: 'user-uuid',
  //     username: 'newfollower',
  //     avatar: 'https://...'
  //   }
  // }
});
```

**Processing Complete (ML):**
```javascript
socket.on('processing_complete', (data) => {
  // data = {
  //   job_id: 'job-uuid',
  //   type: 'visual_search' | 'recommendation' | 'outfit_analysis',
  //   status: 'completed',
  //   result_url: '/api/v1/search/results/job-uuid'
  // }
});
```

**Typing Indicator:**
```javascript
socket.on('user_typing', (data) => {
  // data = {
  //   post_id: 'post-uuid',
  //   user: {
  //     id: 'user-uuid',
  //     username: 'johndoe'
  //   },
  //   is_typing: true
  // }
});
```

---

## 13. Data Models

### 13.1 User Model

```typescript
{
  id: string;  // UUID
  email: string;  // Unique
  username: string;  // Unique, 3-30 chars
  first_name: string;
  last_name: string;
  avatar: string | null;  // URL
  bio: string;  // Max 500 chars
  is_verified: boolean;
  role: 'user' | 'admin' | 'moderator';
  profile: UserProfile;
  preferences: UserPreferences;
  created_at: string;  // ISO 8601
  updated_at: string;  // ISO 8601
}
```

### 13.2 User Profile

```typescript
{
  gender: 'M' | 'F' | 'O' | 'N' | null;
  date_of_birth: string | null;  // YYYY-MM-DD
  phone_number: string | null;
  country: string | null;  // ISO 3166-1 alpha-2
  city: string | null;
  timezone: string | null;
  body_type: 'slim' | 'athletic' | 'average' | 'curvy' | 'plus' | null;
  height: number | null;  // cm
  weight: number | null;  // kg
  top_size: string | null;
  bottom_size: string | null;
  shoe_size: string | null;
  dress_size: string | null;
}
```

### 13.3 User Preferences

```typescript
{
  preferred_styles: string[];  // ['casual', 'formal', 'street', ...]
  preferred_colors: string[];
  preferred_brands: string[];
  preferred_patterns: string[];
  budget_min: number;
  budget_max: number;
  currency: string;  // ISO 4217
  occasions: string[];
  prefer_sustainable: boolean;
  prefer_secondhand: boolean;
  fit_preference: 'tight' | 'regular' | 'loose' | null;
}
```

### 13.4 Outfit Model

```typescript
{
  id: string;  // UUID
  user_id: string;
  user: {
    id: string;
    username: string;
    avatar: string;
  };
  title: string;  // Max 200 chars
  description: string | null;
  main_image: string;  // URL
  thumbnail: string;  // URL
  occasion: 'casual' | 'work' | 'formal' | 'party' | 'sport' | 'date' | 'travel';
  season: 'spring' | 'summer' | 'fall' | 'winter' | 'all';
  style_tags: string[];
  color_palette: string[];
  items: OutfitItem[];
  total_price: number;
  currency: string;
  ai_generated: boolean;
  confidence_score: number;  // 0-1
  is_public: boolean;
  likes_count: number;
  saves_count: number;
  views_count: number;
  is_liked: boolean;
  is_saved: boolean;
  created_at: string;
  updated_at: string;
}
```

### 13.5 Outfit Item

```typescript
{
  id: string;
  outfit_id: string;
  item_type: 'top' | 'bottom' | 'dress' | 'outerwear' | 'shoes' | 'accessory' | 'bag' | 'jewelry';
  name: string;
  brand: string | null;
  image: string;  // URL
  price: number | null;
  currency: string;
  size: string | null;
  color: string | null;
  material: string | null;
  purchase_url: string | null;
  affiliate_link: string | null;
  retailer: string | null;
  is_available: boolean;
  product_id: string | null;
}
```

### 13.6 Wardrobe Item

```typescript
{
  id: string;
  wardrobe_id: string;
  category: 'top' | 'bottom' | 'shoes' | 'accessory' | 'outerwear' | 'dress' | 'bag';
  name: string;
  brand: string | null;
  color: string;
  size: string | null;
  price: number | null;
  currency: string;
  images: string[];  // URLs
  attributes: Array<{
    key: string;
    value: string;
  }>;
  tags: string[];
  times_worn: number;
  purchase_link: string | null;
  purchase_date: string | null;  // YYYY-MM-DD
  created_at: string;
  updated_at: string;
}
```

### 13.7 Social Post

```typescript
{
  id: string;
  user_id: string;
  user: {
    id: string;
    username: string;
    full_name: string;
    avatar: string;
    is_verified: boolean;
  };
  images: string[];  // URLs
  caption: string;  // Max 2200 chars
  tags: string[];
  tagged_items: Array<{
    id: string;
    name: string;
    brand: string;
    image: string;
    purchase_url: string;
    position: {
      x: number;  // 0-1
      y: number;  // 0-1
    };
  }>;
  outfit_id: string | null;
  likes: number;
  comments: number;
  shares: number;
  saves: number;
  views: number;
  is_liked: boolean;
  is_saved: boolean;
  privacy: 'public' | 'friends' | 'private';
  location: {
    name: string;
    latitude: number;
    longitude: number;
  } | null;
  created_at: string;
  updated_at: string;
}
```

### 13.8 Comment

```typescript
{
  id: string;
  post_id: string;
  user_id: string;
  user: {
    id: string;
    username: string;
    full_name: string;
    avatar: string;
  };
  content: string;  // Max 500 chars
  likes: number;
  is_liked: boolean;
  parent_comment_id: string | null;
  replies_count: number;
  replies: Comment[];  // Nested comments
  created_at: string;
  updated_at: string;
}
```

### 13.9 Notification

```typescript
{
  id: string;
  user_id: string;
  type: 'like' | 'comment' | 'follow' | 'recommendation' | 'sale' | 'system' | 'promo';
  title: string;
  message: string;
  image_url: string | null;
  action_url: string | null;
  actor: {
    id: string;
    username: string;
    avatar: string;
  } | null;
  is_read: boolean;
  created_at: string;
}
```

### 13.10 Cart

```typescript
{
  id: string;
  user_id: string;
  items: CartItem[];
  item_count: number;
  subtotal: number;
  shipping: number;
  tax: number;
  discount: number;
  total: number;
  currency: string;
  promo_code: string | null;
  updated_at: string;
}
```

### 13.11 Cart Item

```typescript
{
  id: string;
  cart_id: string;
  outfit_item_id: string;
  name: string;
  brand: string;
  price: number;
  size: string | null;
  color: string;
  quantity: number;
  image_url: string;
  product_url: string | null;
  in_stock: boolean;
  added_at: string;
}
```

---

## 14. Error Handling

### Error Response Format

All API errors follow this consistent format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": ["Specific validation error"]
    },
    "timestamp": "2025-10-28T15:00:00Z",
    "request_id": "req-uuid"
  }
}
```

### HTTP Status Codes

| Code | Description | Usage |
|------|-------------|-------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST (resource created) |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation errors, malformed request |
| 401 | Unauthorized | Missing or invalid authentication token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource conflict (duplicate, constraint violation) |
| 422 | Unprocessable Entity | Semantic errors in request |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Service temporarily unavailable |

### Common Error Codes

**Authentication Errors:**
- `AUTH_INVALID_TOKEN` - Invalid or expired token
- `AUTH_TOKEN_EXPIRED` - Token expired, use refresh token
- `AUTH_INVALID_CREDENTIALS` - Invalid email/password
- `AUTH_ACCOUNT_SUSPENDED` - Account suspended
- `AUTH_ACCOUNT_BANNED` - Account banned
- `AUTH_EMAIL_NOT_VERIFIED` - Email verification required

**Validation Errors:**
- `VALIDATION_ERROR` - General validation error
- `VALIDATION_REQUIRED_FIELD` - Required field missing
- `VALIDATION_INVALID_FORMAT` - Invalid field format
- `VALIDATION_MIN_LENGTH` - Value too short
- `VALIDATION_MAX_LENGTH` - Value too long
- `VALIDATION_INVALID_ENUM` - Invalid enum value

**Resource Errors:**
- `RESOURCE_NOT_FOUND` - Resource not found
- `RESOURCE_ALREADY_EXISTS` - Resource already exists
- `RESOURCE_CONFLICT` - Resource conflict

**Permission Errors:**
- `PERMISSION_DENIED` - Insufficient permissions
- `PERMISSION_OWNER_ONLY` - Only owner can perform this action

**Rate Limit Errors:**
- `RATE_LIMIT_EXCEEDED` - Rate limit exceeded

**File Upload Errors:**
- `FILE_TOO_LARGE` - File exceeds size limit
- `FILE_INVALID_TYPE` - Invalid file type
- `FILE_UPLOAD_FAILED` - File upload failed

**ML Service Errors:**
- `ML_SERVICE_UNAVAILABLE` - ML service unavailable
- `ML_PROCESSING_FAILED` - ML processing failed
- `ML_INVALID_IMAGE` - Invalid image for processing

### Example Error Responses

**Validation Error:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "email": ["This field is required"],
      "password": ["Password must be at least 8 characters"]
    },
    "timestamp": "2025-10-28T15:00:00Z",
    "request_id": "req-uuid"
  }
}
```

**Authentication Error:**
```json
{
  "error": {
    "code": "AUTH_TOKEN_EXPIRED",
    "message": "Access token has expired",
    "details": {
      "expired_at": "2025-10-28T14:45:00Z",
      "action": "Use refresh token to get new access token"
    },
    "timestamp": "2025-10-28T15:00:00Z",
    "request_id": "req-uuid"
  }
}
```

**Rate Limit Error:**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded",
    "details": {
      "limit": 100,
      "window": "1 hour",
      "retry_after": 3600,
      "reset_at": "2025-10-28T16:00:00Z"
    },
    "timestamp": "2025-10-28T15:00:00Z",
    "request_id": "req-uuid"
  }
}
```

---

## 15. Rate Limiting

### Rate Limit Headers

All responses include rate limit information:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1635436800
```

### Rate Limit Tiers

**Anonymous Users:**
- 10 requests per minute
- 100 requests per hour

**Authenticated Users:**
- 60 requests per minute
- 1000 requests per hour

**Premium Users:**
- 120 requests per minute
- 5000 requests per hour

**Admin/Moderator:**
- 300 requests per minute
- 10000 requests per hour

### Endpoint-Specific Limits

**Visual Search:**
- 10 searches per minute
- 100 searches per day

**File Uploads:**
- 20 uploads per hour
- 100MB total per day

**Password Reset:**
- 3 requests per hour per email

**Email Verification:**
- 5 requests per hour per user

**Social Actions (like, save, etc):**
- 100 actions per minute

---

## Appendix A: Implementation Priority

### Phase 1 - Critical (Week 1-2)
1. ✅ Authentication (COMPLETE)
2. ✅ User Management (COMPLETE)
3. ✅ Outfit Management (COMPLETE)
4. ❌ Password Reset & Email Verification
5. ❌ Wardrobe Management

### Phase 2 - Core Features (Week 3-4)
6. ❌ Social Feed & Posts
7. ❌ Notifications (basic)
8. ❌ Shopping Cart
9. ❌ Image Upload to S3

### Phase 3 - Advanced Features (Week 5-6)
10. ❌ Outfit Recommendations (ML)
11. ❌ Visual Search (ML)
12. ❌ Lookbooks
13. ❌ WebSocket (real-time)

### Phase 4 - Admin & Polish (Week 7-8)
14. ❌ Admin Dashboard
15. ❌ Content Moderation
16. ❌ Analytics
17. ❌ Testing & Optimization

---

## Appendix B: Environment Variables

```bash
# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_SETTINGS_MODULE=curator.settings.production
DEBUG=False
ALLOWED_HOSTS=api.curatorai.com,localhost

# Database
DB_NAME=curatorai_db
DB_USER=curatorai_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# JWT
JWT_ACCESS_TOKEN_LIFETIME=15  # minutes
JWT_REFRESH_TOKEN_LIFETIME=10080  # 7 days in minutes

# AWS S3
USE_S3=True
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=curatorai-media
AWS_S3_REGION_NAME=us-east-1

# ML Services
ML_RECOMMENDATION_SERVICE_URL=http://ml-service:8000
ML_VISUAL_SEARCH_SERVICE_URL=http://ml-service:8001

# Email
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@curatorai.com

# OAuth
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret

# Monitoring
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id

# CORS
CORS_ALLOWED_ORIGINS=https://curatorai.com,https://www.curatorai.com

# CDN
CDN_URL=https://cdn.curatorai.com
```

---

## Appendix C: Testing Guide

### Example API Calls (cURL)

**Register:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

**Get Current User:**
```bash
curl http://localhost:8000/api/v1/auth/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**List Outfits:**
```bash
curl "http://localhost:8000/api/v1/outfits/?occasion=casual&season=summer" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

**End of Documentation**

For questions or support, contact: dev@curatorai.com
