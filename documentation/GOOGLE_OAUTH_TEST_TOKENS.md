# 🔑 How to Get Google OAuth Tokens for Testing

**Quick guide to get Google OAuth access tokens to test your API**

---

## 🚀 Method 1: Google OAuth Playground (Easiest for Testing)

### Step 1: Go to Google OAuth Playground

Visit: **https://developers.google.com/oauthplayground/**

### Step 2: Configure OAuth Playground

1. **Click the gear icon (⚙️)** in the top right
2. **Check "Use your own OAuth credentials"**
3. **Enter your credentials:**
   - **OAuth Client ID**: Your `GOOGLE_OAUTH_CLIENT_ID`
   - **OAuth Client secret**: Your `GOOGLE_OAUTH_CLIENT_SECRET`
4. **Click "Close"**

### Step 3: Select Scopes

In the left panel, find and select these scopes:
- ✅ `https://www.googleapis.com/auth/userinfo.email`
- ✅ `https://www.googleapis.com/auth/userinfo.profile`

### Step 4: Authorize APIs

1. Click **"Authorize APIs"** button
2. Sign in with your Google account
3. Click **"Allow"** to grant permissions
4. You'll be redirected back to the playground

### Step 5: Exchange Authorization Code for Tokens

1. Click **"Exchange authorization code for tokens"** button
2. You'll see the **Access token** (starts with `ya29.`)

### Step 6: Copy the Access Token

Copy the **Access token** - this is what you'll use to test your API!

**Example token format:**
```
ya29.a0AfH6SMBx... (long string)
```

---

## 🧪 Method 2: Using Google Sign-In Button (Frontend Testing)

If you want to test from a frontend:

### Step 1: Add Google Sign-In Button

```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://accounts.google.com/gsi/client" async defer></script>
</head>
<body>
    <div id="g_id_onload"
         data-client_id="YOUR_GOOGLE_OAUTH_CLIENT_ID"
         data-callback="handleCredentialResponse">
    </div>
    <div class="g_id_signin" data-type="standard"></div>

    <script>
        function handleCredentialResponse(response) {
            // response.credential is the JWT token
            // For OAuth access token, use Google Sign-In JavaScript SDK instead
            console.log("JWT Token:", response.credential);
        }
    </script>
</body>
</html>
```

### Step 2: Get Access Token Using Google Sign-In SDK

```html
<script src="https://apis.google.com/js/api.js"></script>
<script>
    function onLoad() {
        gapi.load('auth2', function() {
            gapi.auth2.init({
                client_id: 'YOUR_GOOGLE_OAUTH_CLIENT_ID'
            }).then(function() {
                var authInstance = gapi.auth2.getAuthInstance();
                authInstance.signIn().then(function(googleUser) {
                    var accessToken = googleUser.getAuthResponse().access_token;
                    console.log("Access Token:", accessToken);
                    // Use this token to test your API
                });
            });
        });
    }
</script>
```

---

## 🧪 Method 3: Using curl/Postman (Command Line Testing)

### Step 1: Get Token from OAuth Playground

Use Method 1 above to get an access token.

### Step 2: Test Your API Endpoint

**Local Testing:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/oauth/google/ \
  -H "Content-Type: application/json" \
  -d '{"access_token": "ya29.a0AfH6SMBx..."}'
```

**Production Testing:**
```bash
curl -X POST https://curator-ai-backend.vercel.app/api/v1/auth/oauth/google/ \
  -H "Content-Type: application/json" \
  -d '{"access_token": "ya29.a0AfH6SMBx..."}'
```

### Step 3: Expected Response

```json
{
  "success": true,
  "message": "Google authentication successful",
  "data": {
    "user": {
      "id": "uuid-here",
      "email": "your-email@gmail.com",
      "username": "your-email",
      "first_name": "Your",
      "last_name": "Name",
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

---

## 📋 Prerequisites

Before you can get OAuth tokens, you need:

### 1. Google OAuth Credentials

If you don't have them yet:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project or select existing one
3. Go to **APIs & Services** → **Credentials**
4. Click **Create Credentials** → **OAuth client ID**
5. Configure OAuth consent screen (if first time):
   - Choose **External**
   - Fill in app name, email
   - Add scopes: `email`, `profile`
6. Create OAuth client:
   - Type: **Web application**
   - Name: `CuratorAI Test`
   - Authorized redirect URIs:
     - `https://developers.google.com/oauthplayground` (for OAuth Playground)
     - `http://localhost:8000/accounts/google/login/callback/` (for local)
     - `https://curator-ai-backend.vercel.app/accounts/google/login/callback/` (for production)
7. Copy **Client ID** and **Client Secret**

### 2. Set Environment Variables

**Local (.env file):**
```bash
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
```

**Vercel (Environment Variables):**
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add both variables
3. Select: Production, Preview, Development
4. Redeploy

---

## ⚠️ Important Notes

1. **Token Expiration:**
   - Access tokens expire after 1 hour
   - Get a new token when it expires

2. **OAuth Playground Redirect URI:**
   - Make sure `https://developers.google.com/oauthplayground` is added to your authorized redirect URIs in Google Console

3. **Testing Scopes:**
   - Always use `email` and `profile` scopes
   - These are required for user authentication

4. **Security:**
   - Never share your Client Secret publicly
   - Don't commit tokens to git
   - Use environment variables for credentials

---

## 🐛 Troubleshooting

### Error: "Invalid Google token"

**Causes:**
- Token expired (get a new one)
- Wrong token type (need access token, not ID token)
- Client ID/Secret mismatch

**Fix:**
- Get a fresh token from OAuth Playground
- Verify `GOOGLE_OAUTH_CLIENT_ID` matches the one used to get the token

### Error: "redirect_uri_mismatch"

**Cause:** Redirect URI not added to Google Console

**Fix:**
- Add `https://developers.google.com/oauthplayground` to authorized redirect URIs
- Make sure there are no trailing slashes

### Error: "Access blocked: This app's request is invalid"

**Cause:** OAuth consent screen not configured

**Fix:**
- Go to Google Cloud Console → APIs & Services → OAuth consent screen
- Complete the setup (app name, email, scopes)

---

## 📚 Quick Reference

**OAuth Playground:** https://developers.google.com/oauthplayground/

**Your API Endpoint:**
- Local: `http://localhost:8000/api/v1/auth/oauth/google/`
- Production: `https://curator-ai-backend.vercel.app/api/v1/auth/oauth/google/`

**Required Scopes:**
- `https://www.googleapis.com/auth/userinfo.email`
- `https://www.googleapis.com/auth/userinfo.profile`

**Token Format:**
- Starts with: `ya29.`
- Length: ~200+ characters
- Expires: 1 hour

---

**Last Updated:** November 24, 2025

