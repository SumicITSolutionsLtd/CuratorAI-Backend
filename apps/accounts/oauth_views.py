"""
OAuth authentication views for Google and Facebook.
"""
import requests
from rest_framework import status, views, serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from allauth.socialaccount.models import SocialAccount
from drf_spectacular.utils import extend_schema, inline_serializer
from .serializers import UserSerializer
from .models import UserProfile, StylePreference
from core.serializers import ValidationErrorResponse, UnauthorizedErrorResponse

User = get_user_model()


class GoogleOAuthView(views.APIView):
    """
    Google OAuth authentication endpoint.
    Accepts Google ID token and creates/authenticates user.
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Google OAuth login",
        description="Authenticate with Google OAuth token. Returns JWT tokens.",
        tags=["Authentication"],
        request=inline_serializer(
            name='GoogleOAuthRequest',
            fields={
                'access_token': serializers.CharField(required=True, help_text='Google OAuth ID token (JWT) or access token'),
            }
        ),
        responses={
            200: inline_serializer(
                name='GoogleOAuthResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': inline_serializer(
                        name='GoogleOAuthData',
                        fields={
                            'user': UserSerializer(),
                            'tokens': inline_serializer(
                                name='Tokens',
                                fields={
                                    'refresh': serializers.CharField(),
                                    'access': serializers.CharField(),
                                }
                            ),
                            'is_new_user': serializers.BooleanField(),
                        }
                    ),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
        }
    )
    def post(self, request):
        access_token = request.data.get('access_token')
        
        if not access_token:
            return Response({
                'success': False,
                'message': 'Google access token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Verify token with Google
            google_user_info = self._verify_google_token(access_token)
            
            if not google_user_info:
                return Response({
                    'success': False,
                    'message': 'Invalid Google token'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Get or create user
            user, is_new_user = self._get_or_create_user_from_google(google_user_info)
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'success': True,
                'message': 'Google authentication successful',
                'data': {
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    },
                    'is_new_user': is_new_user
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Authentication failed: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def _verify_google_token(self, token):
        """
        Verify Google token (ID token or access token) and get user info.
        Supports both Google ID tokens (JWT) and access tokens.
        """
        import base64
        import json
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            # Check if token is a JWT (ID token) by checking if it has 3 parts separated by dots
            # JWT format: header.payload.signature
            if token.count('.') == 2:
                # This looks like an ID token (JWT)
                return self._verify_google_id_token(token)
            else:
                # This looks like an access token
                return self._verify_google_access_token(token)
        except Exception as e:
            logger.error(f'Unexpected error verifying Google token: {str(e)}')
            return None
    
    def _verify_google_id_token(self, id_token):
        """
        Verify Google ID token (JWT) and extract user info.
        Uses Google's tokeninfo endpoint to verify the ID token.
        """
        import requests
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            # Verify ID token with Google's tokeninfo endpoint
            response = requests.get(
                'https://oauth2.googleapis.com/tokeninfo',
                params={'id_token': id_token},
                timeout=10
            )
            
            if response.status_code == 200:
                token_info = response.json()
                
                # Verify the token is for our client
                # Try to get from SOCIALACCOUNT_PROVIDERS first, then from direct settings
                google_client_id = (
                    getattr(settings, 'SOCIALACCOUNT_PROVIDERS', {})
                    .get('google', {})
                    .get('APP', {})
                    .get('client_id')
                ) or getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID', None)
                
                if google_client_id:
                    aud = token_info.get('aud')
                    if aud != google_client_id:
                        logger.warning(f'Token audience mismatch: expected {google_client_id}, got {aud}')
                        return None
                
                # Extract user info from token
                user_info = {
                    'id': token_info.get('sub'),  # Google user ID
                    'email': token_info.get('email'),
                    'email_verified': token_info.get('email_verified', False),
                    'given_name': token_info.get('given_name', ''),
                    'family_name': token_info.get('family_name', ''),
                    'name': token_info.get('name', ''),
                    'picture': token_info.get('picture', ''),
                }
                
                # Ensure we have required fields
                if not user_info.get('id') or not user_info.get('email'):
                    logger.error('ID token missing required fields (sub or email)')
                    return None
                
                return user_info
            else:
                logger.error(f'Google tokeninfo endpoint returned status {response.status_code}: {response.text}')
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f'Google ID token verification error: {str(e)}')
            return None
        except Exception as e:
            logger.error(f'Unexpected error verifying Google ID token: {str(e)}')
            return None
    
    def _verify_google_access_token(self, access_token):
        """Verify Google access token and get user info."""
        import requests
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            # First try v2 API
            response = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f'Bearer {access_token}'},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            
            # If v2 fails, try v3 API
            response = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={'Authorization': f'Bearer {access_token}'},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            
            logger.warning('Failed to verify Google access token with userinfo endpoints')
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f'Google access token verification error: {str(e)}')
            return None
        except Exception as e:
            logger.error(f'Unexpected error verifying Google access token: {str(e)}')
            return None
    
    def _get_or_create_user_from_google(self, google_user_info):
        """Get or create user from Google user info."""
        email = google_user_info.get('email')
        google_id = google_user_info.get('id')
        first_name = google_user_info.get('given_name', '')
        last_name = google_user_info.get('family_name', '')
        picture = google_user_info.get('picture', '')
        
        if not email:
            raise ValueError('Email not provided by Google')
        
        # Try to find existing social account
        try:
            social_account = SocialAccount.objects.get(
                provider='google',
                uid=google_id
            )
            user = social_account.user
            is_new_user = False
        except SocialAccount.DoesNotExist:
            # Try to find user by email
            try:
                user = User.objects.get(email=email)
                # Link Google account to existing user
                SocialAccount.objects.create(
                    user=user,
                    provider='google',
                    uid=google_id,
                    extra_data=google_user_info
                )
                is_new_user = False
            except User.DoesNotExist:
                # Create new user
                username = email.split('@')[0]
                # Ensure username is unique
                base_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = User.objects.create_user(
                    email=email,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    is_verified=True,  # Google emails are verified
                    terms_and_conditions_accepted=True,  # OAuth users implicitly accept terms
                    terms_accepted_at=timezone.now()
                )
                
                # Create related profile and style preference (same as regular registration)
                UserProfile.objects.create(user=user)
                StylePreference.objects.create(user=user)
                
                # Create social account
                SocialAccount.objects.create(
                    user=user,
                    provider='google',
                    uid=google_id,
                    extra_data=google_user_info
                )
                
                # Set avatar if available
                if picture:
                    # TODO: Download and save avatar image
                    pass
                
                is_new_user = True
        
        return user, is_new_user


class FacebookOAuthView(views.APIView):
    """
    Facebook OAuth authentication endpoint.
    Accepts Facebook access token and creates/authenticates user.
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Facebook OAuth login",
        description="Authenticate with Facebook OAuth token. Returns JWT tokens.",
        tags=["Authentication"],
        request=inline_serializer(
            name='FacebookOAuthRequest',
            fields={
                'access_token': serializers.CharField(required=True, help_text='Facebook OAuth access token'),
            }
        ),
        responses={
            200: inline_serializer(
                name='FacebookOAuthResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': inline_serializer(
                        name='FacebookOAuthData',
                        fields={
                            'user': UserSerializer(),
                            'tokens': inline_serializer(
                                name='Tokens',
                                fields={
                                    'refresh': serializers.CharField(),
                                    'access': serializers.CharField(),
                                }
                            ),
                            'is_new_user': serializers.BooleanField(),
                        }
                    ),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
        }
    )
    def post(self, request):
        access_token = request.data.get('access_token')
        
        if not access_token:
            return Response({
                'success': False,
                'message': 'Facebook access token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Verify token with Facebook
            facebook_user_info = self._verify_facebook_token(access_token)
            
            if not facebook_user_info:
                return Response({
                    'success': False,
                    'message': 'Invalid Facebook token'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Get or create user
            user, is_new_user = self._get_or_create_user_from_facebook(facebook_user_info, access_token)
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'success': True,
                'message': 'Facebook authentication successful',
                'data': {
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    },
                    'is_new_user': is_new_user
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Authentication failed: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def _verify_facebook_token(self, access_token):
        """Verify Facebook access token and get user info."""
        try:
            # Get app ID from settings
            app_id = getattr(settings, 'SOCIALACCOUNT_PROVIDERS', {}).get('facebook', {}).get('APP', {}).get('client_id')
            app_secret = getattr(settings, 'SOCIALACCOUNT_PROVIDERS', {}).get('facebook', {}).get('APP', {}).get('secret')
            
            # First, verify the token
            verify_response = requests.get(
                f'https://graph.facebook.com/debug_token',
                params={
                    'input_token': access_token,
                    'access_token': f'{app_id}|{app_secret}'
                },
                timeout=10
            )
            
            if verify_response.status_code != 200:
                return None
            
            verify_data = verify_response.json()
            if not verify_data.get('data', {}).get('is_valid'):
                return None
            
            # Get user info
            response = requests.get(
                'https://graph.facebook.com/me',
                params={
                    'access_token': access_token,
                    'fields': 'id,name,email,first_name,last_name,picture.type(large)'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                # Get picture URL
                picture_data = user_data.get('picture', {}).get('data', {})
                user_data['picture'] = picture_data.get('url', '')
                return user_data
            return None
        except Exception:
            return None
    
    def _get_or_create_user_from_facebook(self, facebook_user_info, access_token):
        """Get or create user from Facebook user info."""
        email = facebook_user_info.get('email')
        facebook_id = facebook_user_info.get('id')
        name = facebook_user_info.get('name', '')
        first_name = facebook_user_info.get('first_name', '')
        last_name = facebook_user_info.get('last_name', '')
        picture = facebook_user_info.get('picture', '')
        
        # If no email, use Facebook ID as identifier
        if not email:
            # Try to get email with additional permission
            # For now, create a placeholder email
            email = f"facebook_{facebook_id}@facebook.temp"
        
        # Try to find existing social account
        try:
            social_account = SocialAccount.objects.get(
                provider='facebook',
                uid=facebook_id
            )
            user = social_account.user
            is_new_user = False
        except SocialAccount.DoesNotExist:
            # Try to find user by email (if real email)
            if email and not email.endswith('@facebook.temp'):
                try:
                    user = User.objects.get(email=email)
                    # Link Facebook account to existing user
                    SocialAccount.objects.create(
                        user=user,
                        provider='facebook',
                        uid=facebook_id,
                        extra_data=facebook_user_info
                    )
                    is_new_user = False
                except User.DoesNotExist:
                    user = None
            else:
                user = None
            
            if not user:
                # Create new user
                if first_name and last_name:
                    username = f"{first_name.lower()}{last_name.lower()}"
                elif name:
                    username = name.lower().replace(' ', '')
                else:
                    username = f"facebook_user_{facebook_id[:8]}"
                
                # Ensure username is unique
                base_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                # If no real email, we'll need to handle it differently
                # For now, create with placeholder
                user = User.objects.create_user(
                    email=email if email and not email.endswith('@facebook.temp') else f"user_{facebook_id}@curator.ai",
                    username=username,
                    first_name=first_name or name.split()[0] if name else '',
                    last_name=last_name or ' '.join(name.split()[1:]) if name and len(name.split()) > 1 else '',
                    is_verified=False,  # Facebook emails may not be verified
                    terms_and_conditions_accepted=True,  # OAuth users implicitly accept terms
                    terms_accepted_at=timezone.now()
                )
                
                # Create related profile and style preference (same as regular registration)
                UserProfile.objects.create(user=user)
                StylePreference.objects.create(user=user)
                
                # Create social account
                SocialAccount.objects.create(
                    user=user,
                    provider='facebook',
                    uid=facebook_id,
                    extra_data=facebook_user_info
                )
                
                # Set avatar if available
                if picture:
                    # TODO: Download and save avatar image
                    pass
                
                is_new_user = True
        
        return user, is_new_user

