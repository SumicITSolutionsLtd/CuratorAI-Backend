"""
Tests for authentication endpoints.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture
def api_client():
    """Create API client."""
    return APIClient()


@pytest.fixture
def user():
    """Create a test user."""
    from apps.accounts.models import UserProfile, StylePreference
    
    user = User.objects.create_user(
        email='test@example.com',
        username='testuser',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )
    # Create related profile and style preference (same as registration)
    UserProfile.objects.create(user=user)
    StylePreference.objects.create(user=user)
    return user


@pytest.fixture
def authenticated_client(api_client, user):
    """Create authenticated API client."""
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.mark.django_db
class TestRegistration:
    """Test user registration endpoint."""
    
    def test_register_success(self, api_client):
        """Test successful user registration."""
        url = '/api/v1/auth/register/'
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'securepass123',
            'password2': 'securepass123',
            'first_name': 'New',
            'last_name': 'User',
            'terms_and_conditions_accepted': True
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'data' in response.data
        assert 'tokens' in response.data['data']
        assert 'access' in response.data['data']['tokens']
        assert 'refresh' in response.data['data']['tokens']
    
    def test_register_duplicate_email(self, api_client, user):
        """Test registration with duplicate email."""
        url = '/api/v1/auth/register/'
        data = {
            'email': user.email,
            'username': 'differentuser',
            'password': 'securepass123',
            'password2': 'securepass123',
            'first_name': 'New',
            'last_name': 'User',
            'terms_and_conditions_accepted': True
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_register_invalid_data(self, api_client):
        """Test registration with invalid data."""
        url = '/api/v1/auth/register/'
        data = {
            'email': 'invalid-email',
            'username': '',
            'password': '123'  # Too short
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogin:
    """Test user login endpoint."""
    
    def test_login_success(self, api_client, user):
        """Test successful login."""
        url = '/api/v1/auth/login/'
        data = {
            'email': user.email,
            'password': 'testpass123'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'data' in response.data
        assert 'tokens' in response.data['data']
        assert 'access' in response.data['data']['tokens']
        assert 'refresh' in response.data['data']['tokens']
    
    def test_login_invalid_credentials(self, api_client, user):
        """Test login with invalid credentials."""
        url = '/api/v1/auth/login/'
        data = {
            'email': user.email,
            'password': 'wrongpassword'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_nonexistent_user(self, api_client):
        """Test login with non-existent user."""
        url = '/api/v1/auth/login/'
        data = {
            'email': 'nonexistent@example.com',
            'password': 'password123'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCurrentUser:
    """Test current user endpoint."""
    
    def test_get_current_user(self, authenticated_client, user):
        """Test getting current user profile."""
        url = '/api/v1/auth/me/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'data' in response.data
        assert response.data['data']['email'] == user.email
        assert response.data['data']['username'] == user.username
    
    def test_update_current_user(self, authenticated_client, user):
        """Test updating current user profile."""
        url = '/api/v1/auth/me/'
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'bio': 'Updated bio'
        }
        response = authenticated_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'data' in response.data
        user.refresh_from_db()
        assert user.first_name == 'Updated'
        assert response.data['data']['first_name'] == 'Updated'
    
    def test_get_current_user_unauthorized(self, api_client):
        """Test getting current user without authentication."""
        url = '/api/v1/auth/me/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestTokenRefresh:
    """Test token refresh endpoint."""
    
    def test_refresh_token_success(self, api_client, user):
        """Test successful token refresh."""
        refresh = RefreshToken.for_user(user)
        url = '/api/v1/auth/refresh/'
        data = {'refresh': str(refresh)}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
    
    def test_refresh_token_invalid(self, api_client):
        """Test refresh with invalid token."""
        url = '/api/v1/auth/refresh/'
        data = {'refresh': 'invalid_token'}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestGoogleOAuth:
    """Test Google OAuth endpoint."""
    
    def test_google_oauth_missing_token(self, api_client):
        """Test Google OAuth without token."""
        url = '/api/v1/auth/oauth/google/'
        response = api_client.post(url, {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_google_oauth_invalid_token(self, api_client):
        """Test Google OAuth with invalid token."""
        url = '/api/v1/auth/oauth/google/'
        data = {'access_token': 'invalid_token_12345'}
        response = api_client.post(url, data, format='json')
        # Should return 401 for invalid token
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_400_BAD_REQUEST]
    
    @pytest.mark.skip(reason="Requires valid Google token for testing")
    def test_google_oauth_valid_token(self, api_client):
        """Test Google OAuth with valid token."""
        # This test requires a valid Google OAuth token
        # Should be tested manually or with mocked Google API
        pass

