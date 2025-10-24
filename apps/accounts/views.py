"""
Views for accounts app - Authentication and User Management.
"""
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import User, UserFollowing
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

