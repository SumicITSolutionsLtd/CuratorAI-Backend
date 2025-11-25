# 🔐 Google OAuth Flow - Complete Explanation

**Understanding how Google OAuth registration and authentication works**

---

## ✅ Yes, Users Can Register with Google OAuth!

**The backend automatically handles registration!** When a user signs in with Google for the first time, the system:

1. ✅ **Creates a new user account** automatically
2. ✅ **Links the Google account** to the user
3. ✅ **Returns JWT tokens** for authentication
4. ✅ **Sets user as verified** (Google emails are verified)
5. ✅ **Creates user profile** and style preferences

**No separate registration step needed!** The OAuth endpoint handles both registration and login.

---

## 🔄 How Google OAuth Works

### The Flow:

```
1. User clicks "Sign in with Google" on frontend
   ↓
2. Frontend redirects to Google OAuth consent screen
   ↓
3. User signs in with Google account
   ↓
4. Google redirects back with authorization code
   ↓
5. Frontend exchanges code for access token
   ↓
6. Frontend sends access token to your backend API
   ↓
7. Backend verifies token with Google
   ↓
8. Backend creates/authenticates user
   ↓
9. Backend returns JWT tokens
```

---

## 🎯 Key Concepts

### ❌ You DON'T Need a Google ID First!

**Common Misconception:** "I need a Google ID to get an access token"

**Reality:** The access token comes from Google's OAuth flow, not from a pre-existing Google ID. The flow works like this:

1. **User clicks "Sign in with Google"** → Google shows consent screen
2. **User signs in** → Google returns authorization code
3. **Frontend exchanges code** → Gets access token
4. **Frontend sends token to backend** → Backend verifies and creates user

### 🔑 What is an Access Token?

An **access token** is a temporary credential that:
- Proves the user authenticated with Google
- Allows your backend to fetch user info from Google
- Expires after 1 hour
- Is obtained through Google's OAuth flow

### 🆔 What is a Google ID?

A **Google ID** is:
- The user's unique identifier in Google's system
- Retrieved by your backend using the access token
- Used to link the Google account to your user account
- Not something you need beforehand!

---

## 📱 Frontend Integration - How to Get Access Token

### Method 1: Google Sign-In JavaScript SDK (Recommended)

```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://accounts.google.com/gsi/client" async defer></script>
</head>
<body>
    <div id="g_id_onload"
         data-client_id="YOUR_GOOGLE_OAUTH_CLIENT_ID"
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
            // response.credential is an ID token, not access token
            // For access token, use Google Sign-In JavaScript SDK
            console.log("ID Token:", response.credential);
            
            // Get access token using Google Sign-In SDK
            getAccessToken();
        }
        
        function getAccessToken() {
            gapi.load('auth2', function() {
                gapi.auth2.init({
                    client_id: 'YOUR_GOOGLE_OAUTH_CLIENT_ID'
                }).then(function() {
                    var authInstance = gapi.auth2.getAuthInstance();
                    authInstance.signIn({
                        scope: 'profile email'
                    }).then(function(googleUser) {
                        var accessToken = googleUser.getAuthResponse().access_token;
                        console.log("Access Token:", accessToken);
                        
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
                    
                    // Check if new user
                    if (data.data.is_new_user) {
                        console.log("New user registered!");
                    } else {
                        console.log("Existing user logged in!");
                    }
                    
                    // Redirect to dashboard
                    window.location.href = '/dashboard';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    </script>
</body>
</html>
```

### Method 2: React/Next.js Example

```jsx
import { useEffect } from 'react';

function GoogleSignInButton() {
    useEffect(() => {
        // Load Google Sign-In SDK
        const script = document.createElement('script');
        script.src = 'https://accounts.google.com/gsi/client';
        script.async = true;
        script.defer = true;
        document.body.appendChild(script);
        
        script.onload = () => {
            window.google.accounts.id.initialize({
                client_id: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID,
                callback: handleCredentialResponse,
            });
        };
        
        return () => {
            document.body.removeChild(script);
        };
    }, []);
    
    const handleCredentialResponse = async (response) => {
        // Get access token
        const accessToken = await getGoogleAccessToken();
        
        // Send to backend
        const res = await fetch('https://curator-ai-backend.vercel.app/api/v1/auth/oauth/google/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                access_token: accessToken
            })
        });
        
        const data = await res.json();
        
        if (data.success) {
            // Store tokens
            localStorage.setItem('access_token', data.data.tokens.access);
            localStorage.setItem('refresh_token', data.data.tokens.refresh);
            
            // Handle new user vs existing user
            if (data.data.is_new_user) {
                // Show welcome message
                alert('Welcome to CuratorAI!');
            }
            
            // Redirect
            window.location.href = '/dashboard';
        }
    };
    
    const getGoogleAccessToken = () => {
        return new Promise((resolve) => {
            window.gapi.load('auth2', () => {
                window.gapi.auth2.init({
                    client_id: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID
                }).then(() => {
                    const authInstance = window.gapi.auth2.getAuthInstance();
                    authInstance.signIn({
                        scope: 'profile email'
                    }).then((googleUser) => {
                        const accessToken = googleUser.getAuthResponse().access_token;
                        resolve(accessToken);
                    });
                });
            });
        });
    };
    
    return (
        <div 
            id="g_id_signin"
            className="g_id_signin"
            data-type="standard"
            data-theme="outline"
            data-size="large"
            data-text="sign_in_with"
            data-shape="rectangular"
        />
    );
}
```

### Method 3: Using Google OAuth 2.0 Playground (For Testing)

See `GOOGLE_OAUTH_TEST_TOKENS.md` for detailed instructions on using OAuth Playground to get test tokens.

---

## 🔍 How Your Backend Handles It

### Step-by-Step Backend Process:

1. **Receives access token** from frontend
   ```json
   {
     "access_token": "ya29.a0AfH6SMBx..."
   }
   ```

2. **Verifies token with Google**
   ```python
   # Backend calls Google API
   GET https://www.googleapis.com/oauth2/v2/userinfo
   Headers: Authorization: Bearer {access_token}
   ```

3. **Gets user info from Google**
   ```json
   {
     "id": "123456789",
     "email": "user@gmail.com",
     "given_name": "John",
     "family_name": "Doe",
     "picture": "https://..."
   }
   ```

4. **Checks if user exists**
   - If Google ID exists → Login existing user
   - If email exists → Link Google account to existing user
   - If neither exists → **Create new user** (automatic registration!)

5. **Returns JWT tokens**
   ```json
   {
     "success": true,
     "data": {
       "user": {...},
       "tokens": {
         "access": "eyJ0eXAi...",
         "refresh": "eyJ0eXAi..."
       },
       "is_new_user": true  // or false
     }
   }
   ```

---

## 📋 Complete Example Flow

### Frontend Code:

```javascript
// 1. User clicks "Sign in with Google"
function handleGoogleSignIn() {
    // 2. Initialize Google Sign-In
    gapi.load('auth2', () => {
        gapi.auth2.init({
            client_id: 'YOUR_GOOGLE_CLIENT_ID'
        }).then(() => {
            // 3. Show Google sign-in popup
            gapi.auth2.getAuthInstance().signIn({
                scope: 'profile email'
            }).then((googleUser) => {
                // 4. Get access token
                const accessToken = googleUser.getAuthResponse().access_token;
                
                // 5. Send to your backend
                fetch('/api/v1/auth/oauth/google/', {
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
                    // 6. Handle response
                    if (data.success) {
                        if (data.data.is_new_user) {
                            console.log('New user registered!');
                        } else {
                            console.log('Existing user logged in!');
                        }
                        
                        // Store tokens
                        localStorage.setItem('access_token', data.data.tokens.access);
                        localStorage.setItem('refresh_token', data.data.tokens.refresh);
                        
                        // Redirect
                        window.location.href = '/dashboard';
                    }
                });
            });
        });
    });
}
```

### Backend Response:

```json
{
  "success": true,
  "message": "Google authentication successful",
  "data": {
    "user": {
      "id": "uuid-here",
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
    "is_new_user": true  // true = registered, false = logged in
  }
}
```

---

## 🎯 Summary

### ✅ Registration is Automatic!

- **First time:** User signs in with Google → Backend creates account → Returns `is_new_user: true`
- **Subsequent times:** User signs in with Google → Backend finds account → Returns `is_new_user: false`

### 🔑 Getting Access Token

1. **Frontend uses Google Sign-In SDK**
2. **User authenticates with Google**
3. **Google returns access token**
4. **Frontend sends token to backend**
5. **Backend handles everything else!**

### ❌ You DON'T Need:

- ❌ Pre-existing Google ID
- ❌ Separate registration endpoint
- ❌ Manual user creation
- ❌ Email verification (Google emails are verified)

### ✅ You DO Need:

- ✅ Google OAuth Client ID (from Google Cloud Console)
- ✅ Google OAuth Client Secret (from Google Cloud Console)
- ✅ Frontend integration with Google Sign-In SDK
- ✅ Backend endpoint configured (already done!)

---

## 📚 Additional Resources

- **Google Sign-In Documentation:** https://developers.google.com/identity/sign-in/web
- **OAuth 2.0 Flow:** https://developers.google.com/identity/protocols/oauth2
- **Test Tokens Guide:** See `GOOGLE_OAUTH_TEST_TOKENS.md`

---

**Last Updated:** November 24, 2025

