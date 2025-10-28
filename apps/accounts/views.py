"""
Views for accounts app - Authentication and User Management.
"""
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
import random
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import User, UserFollowing, PasswordResetCode, EmailVerificationCode
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserUpdateSerializer,
    UserFollowingSerializer
)


class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    
    @extend_schema(
        summary="Register new user",
        description="Create a new user account with email and password",
        tags=["Authentication"]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'message': 'User registered successfully',
            'data': {
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(views.APIView):
    """
    User login endpoint.
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Login user",
        description="Authenticate user and return JWT tokens",
        tags=["Authentication"],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                }
            }
        }
    )
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({
                'success': False,
                'message': 'Email and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Authenticate user
        user = authenticate(username=email, password=password)
        
        if user is None:
            return Response({
                'success': False,
                'message': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'message': 'Login successful',
            'data': {
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
        }, status=status.HTTP_200_OK)


class LogoutView(views.APIView):
    """
    User logout endpoint.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Logout user",
        description="Blacklist refresh token",
        tags=["Authentication"]
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                'success': True,
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                'success': False,
                'message': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(generics.RetrieveUpdateAPIView):
    """
    Get or update current user profile.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer
    
    @extend_schema(
        summary="Get current user",
        description="Retrieve authenticated user's profile",
        tags=["Users"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="Update current user",
        description="Update authenticated user's profile",
        tags=["Users"]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class UserDetailView(generics.RetrieveAPIView):
    """
    Get user details by ID.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get user by ID",
        description="Retrieve user profile by user ID",
        tags=["Users"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class FollowUserView(views.APIView):
    """
    Follow/unfollow a user.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Follow user",
        description="Follow another user",
        tags=["Users"]
    )
    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if user_to_follow == request.user:
            return Response({
                'success': False,
                'message': 'Cannot follow yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already following
        if UserFollowing.objects.filter(follower=request.user, following=user_to_follow).exists():
            return Response({
                'success': False,
                'message': 'Already following this user'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create following relationship
        UserFollowing.objects.create(follower=request.user, following=user_to_follow)
        
        return Response({
            'success': True,
            'message': f'Now following {user_to_follow.username}'
        }, status=status.HTTP_201_CREATED)
    
    @extend_schema(
        summary="Unfollow user",
        description="Unfollow a user",
        tags=["Users"]
    )
    def delete(self, request, user_id):
        try:
            user_to_unfollow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            following = UserFollowing.objects.get(follower=request.user, following=user_to_unfollow)
            following.delete()
            
            return Response({
                'success': True,
                'message': f'Unfollowed {user_to_unfollow.username}'
            }, status=status.HTTP_200_OK)
        except UserFollowing.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Not following this user'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserFollowersView(generics.ListAPIView):
    """
    List user's followers.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return User.objects.filter(following__following_id=user_id)
    
    @extend_schema(
        summary="Get user followers",
        description="List all users following this user",
        tags=["Users"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserFollowingView(generics.ListAPIView):
    """
    List users that this user follows.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return User.objects.filter(followers__follower_id=user_id)
    
    @extend_schema(
        summary="Get user following",
        description="List all users that this user follows",
        tags=["Users"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RequestPasswordResetView(views.APIView):
    """
    Request password reset code.
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Request password reset",
        description="Send password reset code to user's email",
        tags=["Authentication"]
    )
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({
                'success': False,
                'message': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            
            # Generate 6-digit code
            code = str(random.randint(100000, 999999))
            
            # Create password reset code
            expires_at = timezone.now() + timedelta(minutes=15)
            PasswordResetCode.objects.create(
                user=user,
                code=code,
                expires_at=expires_at
            )
            
            # TODO: Send email with code (integrate with email service)
            # For now, we'll just return success
            
            return Response({
                'success': True,
                'message': 'If an account exists with this email, a reset code has been sent',
                'code_expires_in': 900  # 15 minutes in seconds
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            # Don't reveal if user exists
            return Response({
                'success': True,
                'message': 'If an account exists with this email, a reset code has been sent',
                'code_expires_in': 900
            }, status=status.HTTP_200_OK)


class ConfirmPasswordResetView(views.APIView):
    """
    Confirm password reset with code.
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Confirm password reset",
        description="Reset password using verification code",
        tags=["Authentication"]
    )
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        new_password = request.data.get('new_password')
        
        if not all([email, code, new_password]):
            return Response({
                'success': False,
                'message': 'Email, code, and new password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            
            # Find valid reset code
            reset_code = PasswordResetCode.objects.filter(
                user=user,
                code=code,
                is_used=False,
                expires_at__gt=timezone.now()
            ).first()
            
            if not reset_code:
                return Response({
                    'success': False,
                    'message': 'Invalid or expired reset code'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Reset password
            user.set_password(new_password)
            user.save()
            
            # Mark code as used
            reset_code.is_used = True
            reset_code.save()
            
            return Response({
                'success': True,
                'message': 'Password successfully reset'
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Invalid or expired reset code'
            }, status=status.HTTP_400_BAD_REQUEST)


class RequestEmailVerificationView(views.APIView):
    """
    Request email verification code.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Request email verification",
        description="Send verification code to user's email",
        tags=["Authentication"]
    )
    def post(self, request):
        user = request.user
        
        if user.is_verified:
            return Response({
                'success': False,
                'message': 'Email is already verified'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate 6-digit code
        code = str(random.randint(100000, 999999))
        
        # Create verification code
        expires_at = timezone.now() + timedelta(minutes=15)
        EmailVerificationCode.objects.create(
            user=user,
            code=code,
            expires_at=expires_at
        )
        
        # TODO: Send email with code
        
        return Response({
            'success': True,
            'message': 'Verification code sent to your email',
            'code_expires_in': 900
        }, status=status.HTTP_200_OK)


class ConfirmEmailVerificationView(views.APIView):
    """
    Confirm email verification with code.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Confirm email verification",
        description="Verify email using verification code",
        tags=["Authentication"]
    )
    def post(self, request):
        code = request.data.get('code')
        
        if not code:
            return Response({
                'success': False,
                'message': 'Verification code is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        
        # Find valid verification code
        verification_code = EmailVerificationCode.objects.filter(
            user=user,
            code=code,
            is_used=False,
            expires_at__gt=timezone.now()
        ).first()
        
        if not verification_code:
            return Response({
                'success': False,
                'message': 'Invalid or expired verification code'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Mark email as verified
        user.is_verified = True
        user.save()
        
        # Mark code as used
        verification_code.is_used = True
        verification_code.save()
        
        return Response({
            'success': True,
            'message': 'Email successfully verified',
            'user': {
                'is_verified': True
            }
        }, status=status.HTTP_200_OK)


class SearchUsersView(generics.ListAPIView):
    """
    Search users by username or name.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Search users",
        description="Search users by username, first name, or last name",
        tags=["Users"],
        parameters=[
            OpenApiParameter(name='q', description='Search query', required=True, type=str),
        ]
    )
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        
        if not query:
            return User.objects.none()
        
        return User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(id=self.request.user.id)[:50]  # Limit to 50 results


class DeleteAccountView(views.APIView):
    """
    Delete user account (soft delete).
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Delete account",
        description="Soft delete user account",
        tags=["Users"]
    )
    def delete(self, request):
        password = request.data.get('password')
        confirmation = request.data.get('confirmation')
        
        if not password or confirmation != 'DELETE MY ACCOUNT':
            return Response({
                'success': False,
                'message': 'Invalid confirmation'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify password
        user = authenticate(username=request.user.email, password=password)
        
        if user is None:
            return Response({
                'success': False,
                'message': 'Invalid password'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Soft delete: mark user as inactive and anonymize data
        user.is_active = False
        user.username = f'deleted_user_{user.id}'
        user.email = f'deleted_{user.id}@deleted.com'
        user.first_name = '[Deleted]'
        user.last_name = '[User]'
        user.bio = ''
        user.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

