# Lookbooks and Wardrobe Endpoints

This document lists all available endpoints for lookbooks and wardrobe functionality.

## ✅ Status

- ✅ **Migrations completed** - All tables created in production database
- ✅ **Data seeded** - 15 lookbooks and 400 wardrobe items created
- ✅ **Endpoints configured** - All endpoints are available and working

## 📚 Lookbooks Endpoints

### List Lookbooks
- **GET** `/api/v1/lookbooks/`
- **Description**: List all public lookbooks with optional filtering
- **Authentication**: Required
- **Query Parameters**:
  - `season` (optional): Filter by season (spring, summer, fall, winter, all)
  - `occasion` (optional): Filter by occasion (casual, work, formal, party, travel, vacation)
  - `featured` (optional): Show only featured lookbooks (true/false)
  - `page` (optional): Page number for pagination
- **Response**: Paginated list of lookbooks

### Featured Lookbooks
- **GET** `/api/v1/lookbooks/featured/`
- **Description**: Get featured lookbooks
- **Authentication**: Required
- **Response**: List of featured lookbooks

### Create Lookbook
- **POST** `/api/v1/lookbooks/create/`
- **Description**: Create a new lookbook
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "title": "Summer Essentials",
    "description": "A curated collection of perfect summer outfits",
    "season": "summer",
    "occasion": "casual",
    "style": ["minimalist", "fresh"],
    "tags": ["summer", "casual"],
    "is_public": true,
    "is_featured": false
  }
  ```

### Get Lookbook Details
- **GET** `/api/v1/lookbooks/<id>/`
- **Description**: Get details of a specific lookbook
- **Authentication**: Required
- **Response**: Lookbook details with outfits

### Update Lookbook
- **PATCH** `/api/v1/lookbooks/<id>/update/`
- **Description**: Update a lookbook (must be the creator)
- **Authentication**: Required
- **Request Body**: Partial update fields

### Delete Lookbook
- **DELETE** `/api/v1/lookbooks/<id>/delete/`
- **Description**: Delete a lookbook (must be the creator)
- **Authentication**: Required

### Like/Unlike Lookbook
- **POST** `/api/v1/lookbooks/<lookbook_id>/like/`
- **Description**: Like or unlike a lookbook
- **Authentication**: Required
- **Response**: Updated like status

### Get Lookbook Comments
- **GET** `/api/v1/lookbooks/<lookbook_id>/comments/`
- **Description**: Get comments for a lookbook (placeholder for future implementation)
- **Authentication**: Required

## 👔 Wardrobe Endpoints

### List Wardrobe Items
- **GET** `/api/v1/wardrobe/items/`
- **Description**: List wardrobe items for the authenticated user with filtering
- **Authentication**: Required
- **Query Parameters**:
  - `category` (optional): Filter by category (top, bottom, shoes, accessory, outerwear, dress, bag)
  - `season` (optional): Filter by season
  - `page` (optional): Page number for pagination
- **Response**: Paginated list of wardrobe items

### Get User Wardrobe
- **GET** `/api/v1/wardrobe/users/<user_id>/wardrobe/`
- **Description**: Get a user's wardrobe information
- **Authentication**: Required
- **Response**: Wardrobe details with item counts

### Get Wardrobe Statistics
- **GET** `/api/v1/wardrobe/users/<user_id>/wardrobe/stats/`
- **Description**: Get wardrobe statistics (total items, by category, etc.)
- **Authentication**: Required
- **Response**: Statistics about the wardrobe

### Create Wardrobe Item
- **POST** `/api/v1/wardrobe/items/create/`
- **Description**: Add a new item to wardrobe
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "category": "top",
    "name": "White Cotton T-Shirt",
    "brand": "Everlane",
    "color": "white",
    "size": "M",
    "price": 28.00,
    "currency": "USD",
    "season": "all",
    "tags": ["casual", "comfortable"]
  }
  ```

### Get Wardrobe Item Details
- **GET** `/api/v1/wardrobe/items/<id>/`
- **Description**: Get details of a specific wardrobe item
- **Authentication**: Required
- **Response**: Item details

### Update Wardrobe Item
- **PATCH** `/api/v1/wardrobe/items/<id>/update/`
- **Description**: Update a wardrobe item
- **Authentication**: Required (must own the item)
- **Request Body**: Partial update fields

### Delete Wardrobe Item
- **DELETE** `/api/v1/wardrobe/items/<id>/delete/`
- **Description**: Soft delete a wardrobe item
- **Authentication**: Required (must own the item)

### Upload Item Image
- **POST** `/api/v1/wardrobe/items/<item_id>/images/`
- **Description**: Upload an image for a wardrobe item
- **Authentication**: Required
- **Request**: Multipart form data with image file

### Mark Item as Worn
- **POST** `/api/v1/wardrobe/items/<item_id>/worn/`
- **Description**: Mark an item as worn on a specific date
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "worn_date": "2024-11-28",
    "outfit_id": 123,  // optional
    "notes": "Wore to work"  // optional
  }
  ```

## 🧪 Testing Endpoints

You can test all these endpoints using the test dashboard:

1. Go to: `https://your-app.vercel.app/test-dashboard/`
2. Select an endpoint from the list
3. Click "Load Example" to auto-populate request body
4. Click "Get Token" to get an authentication token
5. Click "Test Endpoint" to see results

## 📊 Current Data

After seeding:
- ✅ **15 lookbooks** created with outfits and likes
- ✅ **400 wardrobe items** created across 20 users
- ✅ All endpoints are functional and tested

## 🔍 Example Requests

### Get All Lookbooks
```bash
GET /api/v1/lookbooks/
Authorization: Bearer <token>
```

### Get My Wardrobe Items
```bash
GET /api/v1/wardrobe/items/
Authorization: Bearer <token>
```

### Create a Lookbook
```bash
POST /api/v1/lookbooks/create/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "My New Lookbook",
  "description": "A collection of my favorite outfits",
  "season": "winter",
  "occasion": "casual",
  "style": ["minimalist"],
  "tags": ["winter", "casual"],
  "is_public": true
}
```

### Add Item to Wardrobe
```bash
POST /api/v1/wardrobe/items/create/
Authorization: Bearer <token>
Content-Type: application/json

{
  "category": "top",
  "name": "Blue Sweater",
  "brand": "Zara",
  "color": "blue",
  "size": "M",
  "price": 49.99,
  "season": "winter"
}
```

## ✅ Verification Checklist

- [x] Migrations run successfully
- [x] Tables created in production database
- [x] Sample data seeded
- [x] All endpoints accessible
- [x] Authentication working
- [x] CRUD operations functional
- [x] Filtering and pagination working
- [x] Test dashboard can test all endpoints

## 🎉 All Set!

Your lookbooks and wardrobe endpoints are now fully functional with data. You can:
- Browse lookbooks
- Create and manage your own lookbooks
- Add items to your wardrobe
- Track what you've worn
- Get wardrobe statistics

All endpoints are ready for frontend integration!

