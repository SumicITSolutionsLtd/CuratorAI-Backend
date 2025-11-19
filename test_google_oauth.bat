@echo off
echo Testing Google OAuth endpoint...
echo.
echo Replace YOUR_ACCESS_TOKEN with your actual Google access token from OAuth Playground
echo.
curl -X POST http://localhost:8000/api/v1/auth/oauth/google/ -H "Content-Type: application/json" -d "{\"access_token\": \"YOUR_ACCESS_TOKEN\"}"
echo.
pause

