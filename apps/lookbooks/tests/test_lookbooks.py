"""
Tests for lookbooks endpoints.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.lookbooks.models import Lookbook, LookbookLike

User = get_user_model()


@pytest.fixture
def api_client():
    """Create API client."""
    return APIClient()


@pytest.fixture
def user():
    """Create test user."""
    return User.objects.create_user(
        email='test@example.com',
        username='testuser',
        password='testpass123'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Create authenticated API client."""
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def lookbook(user):
    """Create a test lookbook."""
    return Lookbook.objects.create(
        creator=user,
        title='Test Lookbook',
        description='Test description',
        season='spring',
        occasion='casual',
        is_public=True
    )


@pytest.mark.django_db
class TestLookbookList:
    """Test lookbook list endpoint."""
    
    def test_get_lookbooks_success(self, authenticated_client, lookbook):
        """Test getting list of lookbooks."""
        url = '/api/v1/lookbooks/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 1
        assert len(response.data['results']) >= 1
    
    def test_get_lookbooks_filter_by_season(self, authenticated_client, lookbook):
        """Test filtering lookbooks by season."""
        url = '/api/v1/lookbooks/'
        response = authenticated_client.get(url, {'season': 'spring'})
        assert response.status_code == status.HTTP_200_OK
        assert all(item['season'] == 'spring' for item in response.data['results'])
    
    def test_get_lookbooks_filter_by_occasion(self, authenticated_client, lookbook):
        """Test filtering lookbooks by occasion."""
        url = '/api/v1/lookbooks/'
        response = authenticated_client.get(url, {'occasion': 'casual'})
        assert response.status_code == status.HTTP_200_OK
        assert all(item['occasion'] == 'casual' for item in response.data['results'])
    
    def test_get_lookbooks_unauthorized(self, api_client):
        """Test getting lookbooks without authentication."""
        url = '/api/v1/lookbooks/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestFeaturedLookbooks:
    """Test featured lookbooks endpoint."""
    
    def test_get_featured_lookbooks(self, authenticated_client, user):
        """Test getting featured lookbooks."""
        # Create featured lookbook
        Lookbook.objects.create(
            creator=user,
            title='Featured Lookbook',
            description='Featured description',
            season='summer',
            occasion='party',
            is_public=True,
            is_featured=True
        )
        
        url = '/api/v1/lookbooks/featured/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
        assert all(item['is_featured'] is True for item in response.data['results'])


@pytest.mark.django_db
class TestLookbookDetail:
    """Test lookbook detail endpoint."""
    
    def test_get_lookbook_detail(self, authenticated_client, lookbook):
        """Test getting lookbook details."""
        url = f'/api/v1/lookbooks/{lookbook.id}/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == lookbook.id
        assert response.data['title'] == lookbook.title
    
    def test_get_lookbook_detail_nonexistent(self, authenticated_client):
        """Test getting non-existent lookbook."""
        url = '/api/v1/lookbooks/99999/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_lookbook_detail_increments_views(self, authenticated_client, lookbook):
        """Test that viewing lookbook increments view count."""
        initial_views = lookbook.views_count
        url = f'/api/v1/lookbooks/{lookbook.id}/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        lookbook.refresh_from_db()
        assert lookbook.views_count == initial_views + 1


@pytest.mark.django_db
class TestLookbookCreate:
    """Test lookbook creation endpoint."""
    
    def test_create_lookbook_success(self, authenticated_client, user):
        """Test successful lookbook creation."""
        url = '/api/v1/lookbooks/create/'
        data = {
            'title': 'New Lookbook',
            'description': 'New description',
            'season': 'winter',
            'occasion': 'formal',
            'style': ['elegant', 'classic'],
            'tags': ['winter', 'formal'],
            'is_public': True,
            'outfit_ids': []
        }
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['data']['title'] == 'New Lookbook'
    
    def test_create_lookbook_unauthorized(self, api_client):
        """Test lookbook creation without authentication."""
        url = '/api/v1/lookbooks/create/'
        data = {'title': 'Test Lookbook'}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestLookbookLike:
    """Test lookbook like endpoint."""
    
    def test_like_lookbook_success(self, authenticated_client, user, lookbook):
        """Test successful lookbook like."""
        url = f'/api/v1/lookbooks/{lookbook.id}/like/'
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_liked'] is True
        assert response.data['likes_count'] == 1
    
    def test_unlike_lookbook(self, authenticated_client, user, lookbook):
        """Test unliking a lookbook."""
        # First like
        LookbookLike.objects.create(user=user, lookbook=lookbook)
        lookbook.likes_count = 1
        lookbook.save()
        
        url = f'/api/v1/lookbooks/{lookbook.id}/like/'
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_liked'] is False
        assert response.data['likes_count'] == 0
    
    def test_like_lookbook_nonexistent(self, authenticated_client):
        """Test liking non-existent lookbook."""
        url = '/api/v1/lookbooks/99999/like/'
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

