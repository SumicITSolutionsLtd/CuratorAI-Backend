"""
Tests for social feed endpoints.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.social.models import Post, PostImage, PostLike, PostSave
from apps.accounts.models import UserFollowing

User = get_user_model()


@pytest.fixture
def api_client():
    """Create API client."""
    return APIClient()


@pytest.fixture
def user1():
    """Create first test user."""
    return User.objects.create_user(
        email='user1@example.com',
        username='user1',
        password='testpass123'
    )


@pytest.fixture
def user2():
    """Create second test user."""
    return User.objects.create_user(
        email='user2@example.com',
        username='user2',
        password='testpass123'
    )


@pytest.fixture
def authenticated_client(api_client, user1):
    """Create authenticated API client."""
    refresh = RefreshToken.for_user(user1)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def post(user2):
    """Create a test post."""
    return Post.objects.create(
        user=user2,
        caption='Test post caption',
        privacy='public'
    )


@pytest.mark.django_db
class TestSocialFeed:
    """Test social feed endpoint."""
    
    def test_get_feed_following_empty(self, authenticated_client, user1):
        """Test feed when user follows no one."""
        url = '/api/v1/social/feed/'
        response = authenticated_client.get(url, {'type': 'following'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0
    
    def test_get_feed_following_with_posts(self, authenticated_client, user1, user2, post):
        """Test feed with posts from followed users."""
        # Create following relationship
        UserFollowing.objects.create(follower=user1, following=user2)
        
        url = '/api/v1/social/feed/'
        response = authenticated_client.get(url, {'type': 'following'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 1
    
    def test_get_feed_discover(self, authenticated_client, user1, post):
        """Test discover feed."""
        url = '/api/v1/social/feed/'
        response = authenticated_client.get(url, {'type': 'discover'})
        assert response.status_code == status.HTTP_200_OK
        # Should exclude user's own posts
        assert all(item['user']['id'] != user1.id for item in response.data['results'])
    
    def test_get_feed_trending(self, authenticated_client, post):
        """Test trending feed."""
        url = '/api/v1/social/feed/'
        response = authenticated_client.get(url, {'type': 'trending'})
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
    
    def test_get_feed_unauthorized(self, api_client):
        """Test feed access without authentication."""
        url = '/api/v1/social/feed/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPostDetail:
    """Test post detail endpoint."""
    
    def test_get_post_detail(self, authenticated_client, post):
        """Test getting post details."""
        url = f'/api/v1/social/posts/{post.id}/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == post.id
        assert response.data['caption'] == post.caption
    
    def test_get_post_detail_nonexistent(self, authenticated_client):
        """Test getting non-existent post."""
        url = '/api/v1/social/posts/99999/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_post_detail_increments_views(self, authenticated_client, post):
        """Test that viewing post increments view count."""
        initial_views = post.views_count
        url = f'/api/v1/social/posts/{post.id}/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        post.refresh_from_db()
        assert post.views_count == initial_views + 1


@pytest.mark.django_db
class TestPostCreate:
    """Test post creation endpoint."""
    
    def test_create_post_success(self, authenticated_client, user1):
        """Test successful post creation."""
        url = '/api/v1/social/posts/'
        data = {
            'caption': 'New post caption',
            'tags': ['fashion', 'style'],
            'privacy': 'public'
        }
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['data']['caption'] == 'New post caption'
    
    def test_create_post_unauthorized(self, api_client):
        """Test post creation without authentication."""
        url = '/api/v1/social/posts/'
        data = {'caption': 'Test post'}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPostLike:
    """Test post like endpoint."""
    
    def test_like_post_success(self, authenticated_client, user1, post):
        """Test successful post like."""
        url = f'/api/v1/social/posts/{post.id}/like/'
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_liked'] is True
        assert response.data['likes_count'] == 1
    
    def test_unlike_post(self, authenticated_client, user1, post):
        """Test unliking a post."""
        # First like
        PostLike.objects.create(user=user1, post=post)
        post.likes_count = 1
        post.save()
        
        url = f'/api/v1/social/posts/{post.id}/like/'
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_liked'] is False
        assert response.data['likes_count'] == 0
    
    def test_like_post_nonexistent(self, authenticated_client):
        """Test liking non-existent post."""
        url = '/api/v1/social/posts/99999/like/'
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestPostSave:
    """Test post save endpoint."""
    
    def test_save_post_success(self, authenticated_client, user1, post):
        """Test successful post save."""
        url = f'/api/v1/social/posts/{post.id}/save/'
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_saved'] is True
        assert response.data['saves_count'] == 1
    
    def test_unsave_post(self, authenticated_client, user1, post):
        """Test unsaving a post."""
        # First save
        PostSave.objects.create(user=user1, post=post)
        post.saves_count = 1
        post.save()
        
        url = f'/api/v1/social/posts/{post.id}/save/'
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_saved'] is False
        assert response.data['saves_count'] == 0

