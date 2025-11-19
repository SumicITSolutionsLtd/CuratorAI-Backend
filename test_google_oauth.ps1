# Test Google OAuth Endpoint
# Replace YOUR_ACCESS_TOKEN with your actual Google access token

$accessToken = "YOUR_ACCESS_TOKEN"
$body = @{
    access_token = $accessToken
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/oauth/google/" -Method Post -Body $body -ContentType "application/json"

$response | ConvertTo-Json -Depth 10

