# 🚀 Google OAuth Frontend Setup - Complete Guide

**Step-by-step guide to integrate Google OAuth in your frontend**

---

## 📋 Prerequisites

Before you can use Google OAuth in your frontend, you need:

1. ✅ **Google OAuth Client ID** (from Google Cloud Console)
2. ✅ **Google OAuth Client Secret** (for backend - already configured)
3. ✅ **Backend API endpoint** (already set up at `/api/v1/auth/oauth/google/`)

---

## 🔧 Step 1: Get Google OAuth Client ID

### Go to Google Cloud Console

1. Visit: **https://console.cloud.google.com/**
2. **Sign in** with your Google account
3. **Create a project** or select an existing one
   - Click the project dropdown at the top
   - Click "New Project"
   - Enter name: `CuratorAI`
   - Click "Create"

### Enable Google+ API

1. Go to **APIs & Services** → **Library**
2. Search for **"Google+ API"** or **"People API"**
3. Click on it and click **"Enable"**

### Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Choose **External** (unless you have Google Workspace)
3. Click **Create**
4. Fill in the form:
   - **App name:** `CuratorAI`
   - **User support email:** Your email
   - **Developer contact information:** Your email
   - Click **Save and Continue**
5. **Scopes** (Step 2):
   - Click **Add or Remove Scopes**
   - Select:
     - ✅ `.../auth/userinfo.email`
     - ✅ `.../auth/userinfo.profile`
   - Click **Update** → **Save and Continue**
6. **Test users** (Step 3):
   - Add test users if in testing mode
   - Click **Save and Continue**
7. **Summary** (Step 4):
   - Review and click **Back to Dashboard**

### Create OAuth Client ID

1. Go to **APIs & Services** → **Credentials**
2. Click **+ Create Credentials** → **OAuth client ID**
3. If prompted, configure consent screen (follow steps above)
4. **Application type:** Select **Web application**
5. **Name:** `CuratorAI Frontend`
6. **Authorized JavaScript origins:**
   - `http://localhost:3000` (for local development)
   - `http://localhost:5173` (for Vite dev server)
   - `https://curator-ai-phi.vercel.app` (your frontend domain)
   - `https://your-production-domain.com` (if different)
7. **Authorized redirect URIs:**
   - `http://localhost:3000` (for local)
   - `https://curator-ai-phi.vercel.app` (for production)
   - **Note:** These are for the frontend, not the backend callback
8. Click **Create**
9. **Copy the Client ID** - You'll need this for your frontend!

**Example Client ID format:**
```
123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com
```

---

## 💻 Step 2: Add Client ID to Frontend

### Option A: Environment Variables (Recommended)

**Create `.env.local` file in your frontend project:**

```bash
# .env.local
NEXT_PUBLIC_GOOGLE_CLIENT_ID=123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com
```

**Or for React/Vite:**

```bash
# .env
VITE_GOOGLE_CLIENT_ID=123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com
```

**Important:** 
- Use `NEXT_PUBLIC_` prefix for Next.js
- Use `VITE_` prefix for Vite
- These prefixes make the variable available in the browser

### Option B: Config File

**Create `config/google.js` or `config/google.ts`:**

```javascript
// config/google.js
export const GOOGLE_CLIENT_ID = '123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com';
```

---

## 🎨 Step 3: Implement Google Sign-In Button

### Method 1: Google Sign-In JavaScript SDK (Recommended)

**Add to your HTML/React component:**

```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://accounts.google.com/gsi/client" async defer></script>
</head>
<body>
    <!-- Google Sign-In Button -->
    <div id="g_id_onload"
         data-client_id="YOUR_GOOGLE_CLIENT_ID"
         data-callback="handleCredentialResponse"
         data-auto_select="false"
         data-cancel_on_tap_outside="true">
    </div>
    <div class="g_id_signin"
         data-type="standard"
         data-theme="outline"
         data-size="large"
         data-text="sign_in_with"
         data-shape="rectangular"
         data-logo_alignment="left">
    </div>

    <script>
        function handleCredentialResponse(response) {
            // This gives you an ID token, but we need access token
            // So we'll use the Google Sign-In SDK instead
            getAccessToken();
        }
        
        function getAccessToken() {
            // Load Google Sign-In SDK
            gapi.load('auth2', function() {
                gapi.auth2.init({
                    client_id: 'YOUR_GOOGLE_CLIENT_ID'
                }).then(function() {
                    var authInstance = gapi.auth2.getAuthInstance();
                    authInstance.signIn({
                        scope: 'profile email'
                    }).then(function(googleUser) {
                        var accessToken = googleUser.getAuthResponse().access_token;
                        
                        // Send to your backend
                        sendToBackend(accessToken);
                    });
                });
            });
        }
        
        function sendToBackend(accessToken) {
            fetch('https://curator-ai-backend.vercel.app/api/v1/auth/oauth/google/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    access_token: accessToken
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Store JWT tokens
                    localStorage.setItem('access_token', data.data.tokens.access);
                    localStorage.setItem('refresh_token', data.data.tokens.refresh);
                    
                    // Handle new user
                    if (data.data.is_new_user) {
                        alert('Welcome to CuratorAI!');
                    }
                    
                    // Redirect
                    window.location.href = '/dashboard';
                } else {
                    alert('Login failed: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
        }
    </script>
</body>
</html>
```

### Method 2: React Component

```jsx
// components/GoogleSignIn.jsx
import { useEffect } from 'react';

export default function GoogleSignIn() {
    useEffect(() => {
        // Load Google Sign-In SDK
        const script = document.createElement('script');
        script.src = 'https://apis.google.com/js/api.js';
        script.async = true;
        script.defer = true;
        document.body.appendChild(script);
        
        script.onload = () => {
            window.gapi.load('auth2', () => {
                window.gapi.auth2.init({
                    client_id: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || 
                               process.env.VITE_GOOGLE_CLIENT_ID
                });
            });
        };
        
        return () => {
            if (document.body.contains(script)) {
                document.body.removeChild(script);
            }
        };
    }, []);
    
    const handleGoogleSignIn = () => {
        const authInstance = window.gapi.auth2.getAuthInstance();
        
        authInstance.signIn({
            scope: 'profile email'
        }).then((googleUser) => {
            const accessToken = googleUser.getAuthResponse().access_token;
            
            // Send to backend
            fetch('https://curator-ai-backend.vercel.app/api/v1/auth/oauth/google/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    access_token: accessToken
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    localStorage.setItem('access_token', data.data.tokens.access);
                    localStorage.setItem('refresh_token', data.data.tokens.refresh);
                    
                    if (data.data.is_new_user) {
                        // Show welcome message
                        console.log('New user registered!');
                    }
                    
                    // Redirect or update state
                    window.location.href = '/dashboard';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }).catch(error => {
            console.error('Sign-in error:', error);
        });
    };
    
    return (
        <button 
            onClick={handleGoogleSignIn}
            className="google-sign-in-button"
        >
            <img src="/google-icon.svg" alt="Google" />
            Sign in with Google
        </button>
    );
}
```

### Method 3: Next.js with TypeScript

```tsx
// components/GoogleSignIn.tsx
'use client';

import { useEffect, useState } from 'react';

declare global {
    interface Window {
        gapi: any;
    }
}

export default function GoogleSignIn() {
    const [isLoaded, setIsLoaded] = useState(false);
    
    useEffect(() => {
        // Load Google Sign-In SDK
        const script = document.createElement('script');
        script.src = 'https://apis.google.com/js/api.js';
        script.async = true;
        script.defer = true;
        document.body.appendChild(script);
        
        script.onload = () => {
            window.gapi.load('auth2', () => {
                window.gapi.auth2.init({
                    client_id: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID!
                }).then(() => {
                    setIsLoaded(true);
                });
            });
        };
        
        return () => {
            if (document.body.contains(script)) {
                document.body.removeChild(script);
            }
        };
    }, []);
    
    const handleSignIn = async () => {
        if (!isLoaded) return;
        
        try {
            const authInstance = window.gapi.auth2.getAuthInstance();
            const googleUser = await authInstance.signIn({
                scope: 'profile email'
            });
            
            const accessToken = googleUser.getAuthResponse().access_token;
            
            const response = await fetch(
                'https://curator-ai-backend.vercel.app/api/v1/auth/oauth/google/',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        access_token: accessToken
                    })
                }
            );
            
            const data = await response.json();
            
            if (data.success) {
                localStorage.setItem('access_token', data.data.tokens.access);
                localStorage.setItem('refresh_token', data.data.tokens.refresh);
                
                // Handle redirect
                window.location.href = '/dashboard';
            }
        } catch (error) {
            console.error('Sign-in error:', error);
        }
    };
    
    return (
        <button
            onClick={handleSignIn}
            disabled={!isLoaded}
            className="px-4 py-2 bg-white border border-gray-300 rounded-lg flex items-center gap-2 hover:bg-gray-50"
        >
            <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Sign in with Google
        </button>
    );
}
```

---

## 🔐 Step 4: Backend Configuration (Already Done!)

Your backend is already configured! Just make sure these environment variables are set:

**In Vercel (Backend):**
```bash
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
```

**Note:** The backend uses the Client Secret to verify tokens, but the frontend only needs the Client ID.

---

## ✅ Complete Flow Summary

1. **Get Client ID** from Google Cloud Console
2. **Add Client ID** to frontend environment variables
3. **Load Google Sign-In SDK** in your frontend
4. **User clicks "Sign in with Google"**
5. **Google shows consent screen**
6. **User signs in**
7. **Frontend gets access token**
8. **Frontend sends token to backend** (`/api/v1/auth/oauth/google/`)
9. **Backend verifies token and creates/logs in user**
10. **Backend returns JWT tokens**
11. **Frontend stores tokens and redirects**

---

## 🎯 Quick Checklist

- [ ] Google Cloud Console project created
- [ ] OAuth consent screen configured
- [ ] OAuth Client ID created (Web application)
- [ ] Authorized JavaScript origins added
- [ ] Client ID added to frontend `.env`
- [ ] Google Sign-In SDK loaded in frontend
- [ ] Sign-in button implemented
- [ ] Access token sent to backend API
- [ ] JWT tokens stored in localStorage
- [ ] User redirected after successful login

---

## 🐛 Common Issues

### Error: "Invalid client_id"

**Cause:** Client ID not set or incorrect

**Fix:**
- Check environment variable is set correctly
- Make sure you're using the Client ID (not Client Secret)
- Verify the Client ID format: `xxx.apps.googleusercontent.com`

### Error: "redirect_uri_mismatch"

**Cause:** Frontend URL not in authorized origins

**Fix:**
- Add your frontend URL to "Authorized JavaScript origins" in Google Console
- Make sure protocol matches (http vs https)
- No trailing slashes

### Error: "Access blocked: This app's request is invalid"

**Cause:** OAuth consent screen not configured

**Fix:**
- Complete OAuth consent screen setup in Google Console
- Add test users if in testing mode

---

## 📚 Resources

- **Google Sign-In Documentation:** https://developers.google.com/identity/sign-in/web
- **Google Cloud Console:** https://console.cloud.google.com/
- **OAuth 2.0 Guide:** https://developers.google.com/identity/protocols/oauth2

---

**Last Updated:** November 24, 2025

