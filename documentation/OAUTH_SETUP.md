# 🔐 OAuth Authentication Setup Guide

This guide explains how to set up Google and Facebook OAuth authentication for CuratorAI.

---

## 📋 Overview

The application supports OAuth authentication via:
- **Google OAuth 2.0**
- **Facebook OAuth 2.0**

Users can sign in using their Google or Facebook accounts, and the system will automatically create a user account if one doesn't exist.

---

## 🔧 Setup Instructions

### 1. Google OAuth Setup

#### Step 1: Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to **APIs & Services** → **Credentials**
4. Click **Create Credentials** → **OAuth client ID**
5. If prompted, configure the OAuth consent screen:
   - Choose **External** (unless you have a Google Workspace)
   - Fill in app name, user support email, developer contact
   - Add scopes: `email`, `profile`
   - Add test users (if in testing mode)
6. Create OAuth client ID:
   - Application type: **Web application**
   - Name: `CuratorAI Backend`
   - Authorized JavaScript origins:
     - `http://localhost:8000` (for local development)
     - `https://curator-ai-backend.vercel.app` (for production)
     - `https://your-frontend-domain.com` (if applicable)
   - Authorized redirect URIs:
     - `http://localhost:8000/accounts/google/login/callback/` (for local)
     - `https://curator-ai-backend.vercel.app/accounts/google/login/callback/` (for production)
7. Copy the **Client ID** and **Client Secret**

#### Step 2: Add Environment Variables

Add these to your `.env` file (local) and Vercel environment variables:

```bash
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
```

**For Vercel:**
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add both variables for **Production**, **Preview**, and **Development**
3. Redeploy after adding

---

### 2. Facebook OAuth Setup

#### Step 1: Create Facebook App

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Click **My Apps** → **Create App**
3. Choose app type: **Consumer** or **Business**
4. Fill in app details:
   - App Name: `CuratorAI`
   - App Contact Email: your email
   - Business Account: (optional)
5. After creation, go to **Settings** → **Basic**
6. Add **App Domains**:
   - `localhost` (for development)
   - `curator-ai-backend.vercel.app` (for production)
   - Your frontend domain (if applicable)
7. Add **Privacy Policy URL** and **Terms of Service URL** (required for production)
8. Click **Add Platform** → **Website**
   - Site URL: `https://curator-ai-backend.vercel.app` (or your domain)

#### Step 2: Configure Facebook Login

1. In Facebook App Dashboard, go to **Products** → **Facebook Login** → **Settings**
2. Add **Valid OAuth Redirect URIs**:
   - `http://localhost:8000/accounts/facebook/login/callback/` (for local)
   - `https://curator-ai-backend.vercel.app/accounts/facebook/login/callback/` (for production)
3. Save changes

#### Step 3: Get App Credentials

1. Go to **Settings** → **Basic**
2. Copy **App ID** and **App Secret**
3. Note: App Secret is hidden by default, click **Show** to reveal it

#### Step 4: Add Environment Variables

Add these to your `.env` file (local) and Vercel environment variables:

```bash
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret
```

**For Vercel:**
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add both variables for **Production**, **Preview**, and **Development**
3. Redeploy after adding

---

## 🚀 API Usage

### Google OAuth Login

**Endpoint:** `POST /api/v1/auth/oauth/google/`

**Request:**
```json
{
  "access_token": "ya29.a0AfH6SMBx..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Google authentication successful",
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@gmail.com",
      "username": "user",
      "first_name": "John",
      "last_name": "Doe",
      "is_verified": true
    },
    "tokens": {
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
      "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    },
    "is_new_user": true
  }
}
```

### Facebook OAuth Login

**Endpoint:** `POST /api/v1/auth/oauth/facebook/`

**Request:**
```json
{
  "access_token": "EAAx..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Facebook authentication successful",
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@facebook.com",
      "username": "john_doe",
      "first_name": "John",
      "last_name": "Doe",
      "is_verified": false
    },
    "tokens": {
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
      "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    },
    "is_new_user": true
  }
}
```

---

## 📱 Frontend Integration

### Example: React/Next.js

```javascript
// Google OAuth
const handleGoogleLogin = async () => {
  try {
    // Get Google access token using Google Sign-In SDK
    const response = await window.gapi.auth2.getAuthInstance().signIn();
    const accessToken = response.getAuthResponse().access_token;
    
    // Send to backend
    const res = await fetch('https://curator-ai-backend.vercel.app/api/v1/auth/oauth/google/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ access_token: accessToken }),
    });
    
    const data = await res.json();
    if (data.success) {
      // Store tokens
      localStorage.setItem('access_token', data.data.tokens.access);
      localStorage.setItem('refresh_token', data.data.tokens.refresh);
      // Redirect or update UI
    }
  } catch (error) {
    console.error('Google login failed:', error);
  }
};

// Facebook OAuth
const handleFacebookLogin = async () => {
  try {
    // Get Facebook access token using Facebook SDK
    window.FB.login((response) => {
      if (response.authResponse) {
        const accessToken = response.authResponse.accessToken;
        
        // Send to backend
        fetch('https://curator-ai-backend.vercel.app/api/v1/auth/oauth/facebook/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ access_token: accessToken }),
        })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            // Store tokens
            localStorage.setItem('access_token', data.data.tokens.access);
            localStorage.setItem('refresh_token', data.data.tokens.refresh);
            // Redirect or update UI
          }
        });
      }
    }, { scope: 'email,public_profile' });
  } catch (error) {
    console.error('Facebook login failed:', error);
  }
};
```

---

## 🔍 Testing

### Test Google OAuth Locally

1. Start your Django server: `python manage.py runserver`
2. Use a tool like Postman or curl:

```bash
curl -X POST http://localhost:8000/api/v1/auth/oauth/google/ \
  -H "Content-Type: application/json" \
  -d '{"access_token": "YOUR_GOOGLE_ACCESS_TOKEN"}'
```

### Test Facebook OAuth Locally

```bash
curl -X POST http://localhost:8000/api/v1/auth/oauth/facebook/ \
  -H "Content-Type: application/json" \
  -d '{"access_token": "YOUR_FACEBOOK_ACCESS_TOKEN"}'
```

**Note:** To get access tokens for testing:
- **Google**: Use [Google OAuth Playground](https://developers.google.com/oauthplayground/)
- **Facebook**: Use [Facebook Graph API Explorer](https://developers.facebook.com/tools/explorer/)

---

## ⚠️ Important Notes

1. **Email Verification**: 
   - Google users are automatically marked as verified
   - Facebook users may need email verification separately

2. **Username Generation**:
   - If email is available, username is derived from email
   - If not, a unique username is generated

3. **Account Linking**:
   - If a user with the same email exists, the OAuth account is linked
   - Users can link multiple OAuth providers to the same account

4. **Security**:
   - Always use HTTPS in production
   - Keep OAuth secrets secure (never commit to git)
   - Regularly rotate OAuth credentials

5. **Facebook Email**:
   - Some Facebook users may not have email addresses
   - The system creates a placeholder email in such cases
   - Users should be prompted to add an email later

---

## 🐛 Troubleshooting

### Google OAuth Issues

**Error: "Invalid Google token"**
- Check that the access token is valid and not expired
- Verify `GOOGLE_OAUTH_CLIENT_ID` is set correctly
- Ensure redirect URIs match exactly

**Error: "redirect_uri_mismatch"**
- Add the exact callback URL to Google Console
- Check for trailing slashes and protocol (http vs https)

### Facebook OAuth Issues

**Error: "Invalid Facebook token"**
- Verify `FACEBOOK_APP_ID` and `FACEBOOK_APP_SECRET` are correct
- Check that the app is not in development mode restrictions
- Ensure redirect URIs are added in Facebook App settings

**Error: "Email not provided"**
- Some Facebook users don't have email addresses
- The system handles this by creating a placeholder email
- Users should add an email address later

---

## 📚 Additional Resources

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Facebook Login Documentation](https://developers.facebook.com/docs/facebook-login/)
- [Django Allauth Documentation](https://django-allauth.readthedocs.io/)

---

## ✅ Checklist

- [ ] Google OAuth credentials created
- [ ] Facebook App created
- [ ] Environment variables added to `.env` (local)
- [ ] Environment variables added to Vercel
- [ ] Redirect URIs configured in both providers
- [ ] OAuth endpoints tested locally
- [ ] OAuth endpoints tested in production
- [ ] Frontend integration completed
- [ ] Error handling implemented

---

**Need help?** Contact the development team or check the API documentation at `/api/schema/swagger-ui/`

