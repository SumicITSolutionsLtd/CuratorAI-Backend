"""
URL patterns for accounts app.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    CurrentUserView,
    UserDetailView,
    FollowUserView,
    UserFollowersView,
    UserFollowingView,
    RequestPasswordResetView,
    ConfirmPasswordResetView,
    RequestEmailVerificationView,
    ConfirmEmailVerificationView,
    SearchUsersView,
    DeleteAccountView,
    CompleteRegistrationView,
)
from .oauth_views import GoogleOAuthView, FacebookOAuthView

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('register/complete/', CompleteRegistrationView.as_view(), name='complete-registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # OAuth Authentication
    path('oauth/google/', GoogleOAuthView.as_view(), name='oauth-google'),
    path('oauth/facebook/', FacebookOAuthView.as_view(), name='oauth-facebook'),
    
    # Password Reset
    path('password-reset/request/', RequestPasswordResetView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', ConfirmPasswordResetView.as_view(), name='password-reset-confirm'),
    
    # Email Verification
    path('verify-email/request/', RequestEmailVerificationView.as_view(), name='email-verification-request'),
    path('verify-email/confirm/', ConfirmEmailVerificationView.as_view(), name='email-verification-confirm'),
    
    # User Profile
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/search/', SearchUsersView.as_view(), name='search-users'),
    
    # Following
    path('users/<int:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('users/<int:user_id>/followers/', UserFollowersView.as_view(), name='user-followers'),
    path('users/<int:user_id>/following/', UserFollowingView.as_view(), name='user-following'),
    
    # Account Management
    path('delete/', DeleteAccountView.as_view(), name='delete-account'),
]

