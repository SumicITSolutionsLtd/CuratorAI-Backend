# CuratorAI API Endpoints - Wireframe Mapping

## ✅ Already Implemented Endpoints

### Authentication & User Management
| Wireframe | Endpoint | Status | Notes |
|-----------|----------|--------|-------|
| Sign Up (Step 1-3) | `POST /api/v1/auth/register/` | ✅ Complete | Includes profile setup in one call |
| Login | `POST /api/v1/auth/login/` | ✅ Complete | Email/password + OAuth stubs |
| Logout | `POST /api/v1/auth/logout/` | ✅ Complete | Blacklists refresh token |
| Refresh Token | `POST /api/v1/auth/refresh/` | ✅ Complete | JWT refresh |
| Get Current User | `GET /api/v1/auth/me/` | ✅ Complete | Profile with preferences |
| Update Profile | `PUT /api/v1/auth/me/` | ✅ Complete | Profile + style preferences |
| Get User by ID | `GET /api/v1/auth/users/<id>/` | ✅ Complete | Public profile view |
| Follow User | `POST /api/v1/auth/users/<id>/follow/` | ✅ Complete | Social following |
| Unfollow User | `DELETE /api/v1/auth/users/<id>/follow/` | ✅ Complete | Remove follow |
| Get Followers | `GET /api/v1/auth/users/<id>/followers/` | ✅ Complete | List followers |
| Get Following | `GET /api/v1/auth/users/<id>/following/` | ✅ Complete | List following |

### Outfit Management
| Wireframe | Endpoint | Status | Notes |
|-----------|----------|--------|-------|
| Home Feed | `GET /api/v1/outfits/` | ✅ Complete | Paginated with filters |
| Outfit Detail | `GET /api/v1/outfits/<id>/` | ✅ Complete | Full details + items |
| Create Outfit | `POST /api/v1/outfits/` | ✅ Complete | With items in one call |
| Update Outfit | `PUT /api/v1/outfits/<id>/` | ✅ Complete | Owner only |
| Delete Outfit | `DELETE /api/v1/outfits/<id>/` | ✅ Complete | Owner only |
| Like Outfit | `POST /api/v1/outfits/<id>/like/` | ✅ Complete | Toggle like |
| Save Outfit | `POST /api/v1/outfits/<id>/save/` | ✅ Complete | Save to collection |
| User Outfits | `GET /api/v1/outfits/user/<user_id>/` | ✅ Complete | User's public outfits |

## 🔄 Needs Implementation

### Password Reset Flow
| Wireframe | Endpoint | Status | Notes |
|-----------|----------|--------|-------|
| Request Reset | `POST /api/v1/auth/password-reset/` | ❌ Missing | Send reset email |
| Verify Reset Token | `GET /api/v1/auth/password-reset/<token>/` | ❌ Missing | Validate token |
| Reset Password | `POST /api/v1/auth/password-reset/<token>/` | ❌ Missing | Set new password |
| Email Verification | `POST /api/v1/auth/verify-email/` | ❌ Missing | Send verification code |
| Verify Code | `POST /api/v1/auth/verify-email/confirm/` | ❌ Missing | Confirm 6-digit code |

### Recommendations & Filters
| Wireframe | Endpoint | Status | Notes |
|-----------|----------|--------|-------|
| Get Recommendations | `GET /api/v1/recommendations/` | ❌ Missing | AI-powered personalized |
| Filter Recommendations | `GET /api/v1/recommendations/?occasion=&budget=...` | ❌ Missing | Advanced filters |
| Recommendation Feedback | `POST /api/v1/recommendations/<id>/feedback/` | ❌ Missing | Like/dislike for ML |
| Generate Recommendations | `POST /api/v1/recommendations/generate/` | ❌ Missing | On-demand generation |

### Visual Search
| Wireframe | Endpoint | Status | Notes |
|-----------|----------|--------|-------|
| Upload Image Search | `POST /api/v1/search/visual/` | ❌ Missing | Upload image, get similar |
| Processing Status | `GET /api/v1/search/visual/<id>/status/` | ❌ Missing | Check processing progress |
| Search Results | `GET /api/v1/search/visual/<id>/results/` | ❌ Missing | Get results with similarity |
| Similar Items | `GET /api/v1/search/similar/<outfit_id>/` | ❌ Missing | Find similar to existing |
| Recent Searches | `GET /api/v1/search/history/` | ❌ Missing | User's search history |

### Wardrobe Management
| Wireframe | Endpoint | Status | Notes |
|-----------|----------|--------|-------|
| List Wardrobe Items | `GET /api/v1/wardrobe/items/` | ❌ Missing | User's wardrobe |
| Add Item | `POST /api/v1/wardrobe/items/` | ❌ Missing | Add clothing item |
| Update Item | `PUT /api/v1/wardrobe/items/<id>/` | ❌ Missing | Edit item details |
| Delete Item | `DELETE /api/v1/wardrobe/items/<id>/` | ❌ Missing | Remove from wardrobe |
| Item Detail | `GET /api/v1/wardrobe/items/<id>/` | ❌ Missing | Full item info |
| Wardrobe Summary | `GET /api/v1/wardrobe/summary/` | ❌ Missing | Stats: item count, categories |
| Wardrobe Analytics | `GET /api/v1/wardrobe/analytics/` | ❌ Missing | Most worn, color distribution |
| Create Outfit Canvas | `POST /api/v1/wardrobe/outfits/` | ❌ Missing | Create from wardrobe items |

### Social Feed & Posts
| Wireframe | Endpoint | Status | Notes |
|-----------|----------|--------|-------|
| Get Feed | `GET /api/v1/posts/` | ❌ Missing | Personalized social feed |
| Create Post | `POST /api/v1/posts/` | ❌ Missing | Share outfit post |
| Post Detail | `GET /api/v1/posts/<id>/` | ❌ Missing | Full post with comments |
| Update Post | `PUT /api/v1/posts/<id>/` | ❌ Missing | Edit post |
| Delete Post | `DELETE /api/v1/posts/<id>/` | ❌ Missing | Remove post |
| Like Post | `POST /api/v1/posts/<id>/like/` | ❌ Missing | Toggle like |
| Comment on Post | `POST /api/v1/posts/<id>/comments/` | ❌ Missing | Add comment |
| Share Post | `POST /api/v1/posts/<id>/share/` | ❌ Missing | Share to external platforms |
| Save Post | `POST /api/v1/posts/<id>/save/` | ❌ Missing | Save to collections |
| Trending Posts | `GET /api/v1/posts/trending/` | ❌ Missing | Popular posts |
| Following Feed | `GET /api/v1/posts/following/` | ❌ Missing | Posts from followed users |

### Lookbooks (Shoppable)
| Wireframe | Endpoint | Status | Notes |
|-----------|----------|--------|-------|
| List Lookbooks | `GET /api/v1/lookbooks/` | ❌ Missing | Featured & trending |
| Lookbook Detail | `GET /api/v1/lookbooks/<id>/` | ❌ Missing | Full lookbook with outfits |
| Create Lookbook | `POST /api/v1/lookbooks/` | ❌ Missing | Admin/creator only |
| Update Lookbook | `PUT /api/v1/lookbooks/<id>/` | ❌ Missing | Edit lookbook |
| Delete Lookbook | `DELETE /api/v1/lookbooks/<id>/` | ❌ Missing | Remove lookbook |
| Like Lookbook | `POST /api/v1/lookbooks/<id>/like/` | ❌ Missing | Toggle like |
| Lookbook by Category | `GET /api/v1/lookbooks/?category=summer` | ❌ Missing | Filter by season/occasion |
| Add to Cart (All Items) | `POST /api/v1/lookbooks/<id>/cart/` | ❌ Missing | Add all items to cart |

### Shopping Cart & Checkout
| Wireframe | Endpoint | Status | Notes |
|-----------|----------|--------|-------|
| Get Cart | `GET /api/v1/cart/` | ❌ Missing | User's shopping cart |
| Add to Cart | `POST /api/v1/cart/items/` | ❌ Missing | Add product |
| Update Cart Item | `PUT /api/v1/cart/items/<id>/` | ❌ Missing | Change quantity/size |
| Remove from Cart | `DELETE /api/v1/cart/items/<id>/` | ❌ Missing | Remove item |
| Apply Promo Code | `POST /api/v1/cart/promo/` | ❌ Missing | Apply discount |
| Get Cart Summary | `GET /api/v1/cart/summary/` | ❌ Missing | Totals, shipping, tax |
| Checkout | `POST /api/v1/checkout/` | ❌ Missing | Process order (redirects to retailers) |

### Virtual Try-On
| Wireframe | Endpoint | Status | Notes |
|-----------|----------|--------|-------|
| Start Try-On Session | `POST /api/v1/try-on/session/` | ❌ Missing | Initialize AR session |
| Upload Body Photo | `POST /api/v1/try-on/calibrate/` | ❌ Missing | Get measurements |
| Apply Garment | `POST /api/v1/try-on/apply/` | ❌ Missing | Overlay clothing |
| Capture Try-On | `POST /api/v1/try-on/capture/` | ❌ Missing | Save AR photo |
| Try-On History | `GET /api/v1/try-on/history/` | ❌ Missing | Past try-ons |

### Notifications
| Wireframe | Endpoint | Status | Notes |
|-----------|----------|--------|-------|
| Get Notifications | `GET /api/v1/notifications/` | ❌ Missing | All notifications |
| Mark as Read | `PUT /api/v1/notifications/<id>/read/` | ❌ Missing | Mark read |
| Mark All Read | `POST /api/v1/notifications/read-all/` | ❌ Missing | Bulk read |
| Notification Settings | `GET /api/v1/notifications/settings/` | ❌ Missing | User preferences |
| Update Settings | `PUT /api/v1/notifications/settings/` | ❌ Missing | Change preferences |

### Admin Dashboard
| Wireframe | Endpoint | Status | Notes |
|-----------|----------|--------|-------|
| Dashboard Stats | `GET /api/v1/admin/dashboard/` | ❌ Missing | Overview metrics |
| User Management | `GET /api/v1/admin/users/` | ❌ Missing | List all users |
| Suspend User | `PATCH /api/v1/admin/users/<id>/status/` | ❌ Missing | Ban/suspend |
| Content Moderation Queue | `GET /api/v1/admin/moderation/` | ❌ Missing | Flagged content |
| Approve/Reject Content | `POST /api/v1/admin/moderation/<id>/action/` | ❌ Missing | Moderate content |
| Analytics | `GET /api/v1/admin/analytics/` | ❌ Missing | Business metrics |
| Export Data | `GET /api/v1/admin/export/` | ❌ Missing | CSV/JSON export |
| System Logs | `GET /api/v1/admin/logs/` | ❌ Missing | Activity logs |

### Settings & API Keys
| Wireframe | Endpoint | Status | Notes |
|-----------|----------|--------|-------|
| Get Settings | `GET /api/v1/settings/` | ❌ Missing | User settings |
| Update Settings | `PUT /api/v1/settings/` | ❌ Missing | Notifications, privacy |
| Generate API Key | `POST /api/v1/settings/api-keys/` | ❌ Missing | Developer keys |
| List API Keys | `GET /api/v1/settings/api-keys/` | ❌ Missing | User's keys |
| Revoke API Key | `DELETE /api/v1/settings/api-keys/<id>/` | ❌ Missing | Delete key |
| API Usage Stats | `GET /api/v1/settings/api-keys/<id>/usage/` | ❌ Missing | Usage metrics |

## 📊 Summary

**Total Endpoints Required**: 107
**Implemented**: 20 (19%)
**Missing**: 87 (81%)

### Priority Breakdown

**High Priority (MVP Core)**: 45 endpoints
- ✅ Auth & Profile: 11/11 (100%)
- ✅ Outfits: 8/8 (100%)
- ❌ Recommendations: 0/4
- ❌ Visual Search: 0/5
- ❌ Wardrobe: 0/8
- ❌ Social Feed: 0/11
- ❌ Lookbooks: 0/8

**Medium Priority**: 28 endpoints
- ❌ Shopping Cart: 0/7
- ❌ Notifications: 0/5
- ❌ Admin Basic: 0/8
- ❌ Settings: 0/8

**Low Priority (Phase 2)**: 34 endpoints
- ❌ Virtual Try-On: 0/5
- ❌ Advanced Admin: 0/8
- ❌ Password Reset: 0/5
- ❌ Email Verification: 0/2
- ❌ Advanced Analytics: 0/14

## 🎯 Next Steps

1. **Complete remaining models** (wardrobe, posts, lookbooks, recommendations, search)
2. **Implement high-priority endpoints** for MVP completion
3. **Add ML service integration stubs** for recommendations and visual search
4. **Build admin endpoints** for content moderation
5. **Add real-time features** (notifications via WebSockets)

## 🔗 API Documentation

All implemented endpoints are documented at:
- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **ReDoc**: http://localhost:8000/api/schema/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

---

**Last Updated**: October 23, 2025  
**Status**: Core auth & outfits complete, remaining apps in progress

