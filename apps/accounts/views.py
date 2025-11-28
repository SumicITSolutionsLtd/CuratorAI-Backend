"""
Views for accounts app - Authentication and User Management.
"""
from rest_framework import generics, status, views, serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
import random
from drf_spectacular.utils import (
    extend_schema, 
    OpenApiParameter, 
    inline_serializer,
    OpenApiTypes
)
from .models import User, UserProfile, StylePreference, UserFollowing, PasswordResetCode, EmailVerificationCode
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserUpdateSerializer,
    UserFollowingSerializer,
    StylePreferenceCompletionSerializer
)
from core.serializers import (
    ValidationErrorResponse,
    UnauthorizedErrorResponse,
    NotFoundErrorResponse,
    ConflictErrorResponse,
)
from decimal import Decimal


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
        tags=["Authentication"],
        request=UserRegisterSerializer,
        responses={
            201: inline_serializer(
                name='RegisterResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': inline_serializer(
                        name='RegisterData',
                        fields={
                            'user': UserSerializer(),
                            'tokens': inline_serializer(
                                name='Tokens',
                                fields={
                                    'refresh': serializers.CharField(),
                                    'access': serializers.CharField(),
                                }
                            ),
                        }
                    ),
                }
            ),
            400: ValidationErrorResponse,
        }
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
        request=inline_serializer(
            name='LoginRequest',
            fields={
                'email': serializers.EmailField(required=True),
                'password': serializers.CharField(required=True, write_only=True),
            }
        ),
        responses={
            200: inline_serializer(
                name='LoginResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': inline_serializer(
                        name='LoginData',
                        fields={
                            'user': UserSerializer(),
                            'tokens': inline_serializer(
                                name='Tokens',
                                fields={
                                    'refresh': serializers.CharField(),
                                    'access': serializers.CharField(),
                                }
                            ),
                        }
                    ),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
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
        tags=["Authentication"],
        request=inline_serializer(
            name='LogoutRequest',
            fields={
                'refresh_token': serializers.CharField(required=True),
            }
        ),
        responses={
            200: inline_serializer(
                name='LogoutResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
        }
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
        tags=["Users"],
        responses={
            200: inline_serializer(
                name='CurrentUserResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': UserSerializer(),
                }
            ),
            401: UnauthorizedErrorResponse,
        }
    )
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'User retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Update current user",
        description="Update authenticated user's profile",
        tags=["Users"],
        request=UserUpdateSerializer,
        responses={
            200: inline_serializer(
                name='UpdateUserResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': UserSerializer(),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
        }
    )
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance.refresh_from_db()
        
        return Response({
            'success': True,
            'message': 'User updated successfully',
            'data': UserSerializer(instance).data
        }, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)


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
        tags=["Users"],
        responses={
            200: inline_serializer(
                name='UserDetailResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': UserSerializer(),
                }
            ),
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
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
        tags=["Users"],
        responses={
            201: inline_serializer(
                name='FollowUserResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
            409: ConflictErrorResponse,
        }
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
        tags=["Users"],
        responses={
            200: inline_serializer(
                name='UnfollowUserResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
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
        tags=["Users"],
        responses={
            200: inline_serializer(
                name='UserFollowersResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': UserSerializer(many=True),
                }
            ),
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
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
        tags=["Users"],
        responses={
            200: inline_serializer(
                name='UserFollowingResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': UserSerializer(many=True),
                }
            ),
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
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
        tags=["Authentication"],
        request=inline_serializer(
            name='PasswordResetRequest',
            fields={
                'email': serializers.EmailField(required=True),
            }
        ),
        responses={
            200: inline_serializer(
                name='PasswordResetRequestResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'code_expires_in': serializers.IntegerField(),
                }
            ),
            400: ValidationErrorResponse,
        }
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
        tags=["Authentication"],
        request=inline_serializer(
            name='ConfirmPasswordResetRequest',
            fields={
                'email': serializers.EmailField(required=True),
                'code': serializers.CharField(required=True, max_length=6),
                'new_password': serializers.CharField(required=True, write_only=True),
            }
        ),
        responses={
            200: inline_serializer(
                name='ConfirmPasswordResetResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                }
            ),
            400: ValidationErrorResponse,
        }
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
        tags=["Authentication"],
        responses={
            200: inline_serializer(
                name='EmailVerificationRequestResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'code_expires_in': serializers.IntegerField(),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
        }
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
        tags=["Authentication"],
        request=inline_serializer(
            name='ConfirmEmailVerificationRequest',
            fields={
                'code': serializers.CharField(required=True, max_length=6),
            }
        ),
        responses={
            200: inline_serializer(
                name='ConfirmEmailVerificationResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'user': inline_serializer(
                        name='UserVerificationStatus',
                        fields={
                            'is_verified': serializers.BooleanField(),
                        }
                    ),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
        }
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
        ],
        responses={
            200: inline_serializer(
                name='SearchUsersResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': UserSerializer(many=True),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
        }
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
        tags=["Users"],
        request=inline_serializer(
            name='DeleteAccountRequest',
            fields={
                'password': serializers.CharField(required=True, write_only=True),
                'confirmation': serializers.CharField(required=True),
            }
        ),
        responses={
            204: OpenApiTypes.NONE,
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
        }
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


class CompleteRegistrationView(views.APIView):
    """
    Complete registration by setting up user style preferences.
    
    Note: This endpoint requires authentication. After registration, users receive
    JWT tokens which should be used to authenticate this request. This is the
    second step in the registration flow (after initial account creation).
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Complete registration",
        description="Complete user registration by setting up style preferences (shop for, styles, dress for, budget)",
        tags=["Authentication"],
        request=StylePreferenceCompletionSerializer,
        responses={
            200: inline_serializer(
                name='CompleteRegistrationResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': inline_serializer(
                        name='CompleteRegistrationData',
                        fields={
                            'user': UserSerializer(),
                        }
                    ),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
        }
    )
    def post(self, request):
        serializer = StylePreferenceCompletionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        validated_data = serializer.validated_data
        
        # Map shop_for to gender in UserProfile
        shop_for_mapping = {
            'Men': 'M',
            'Women': 'F',
            'Non-binary': 'O',
            'Prefer not to say': 'N'
        }
        gender = shop_for_mapping.get(validated_data['shop_for'])
        
        # Update user profile
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.gender = gender
        profile.save()
        
        # Update style preferences
        style_pref, _ = StylePreference.objects.get_or_create(user=user)
        
        # Set preferred styles
        style_pref.preferred_styles = validated_data['styles']
        
        # Set occasions (dress_for)
        style_pref.occasions = validated_data['dress_for']
        
        # Map budget_range to budget_min and budget_max
        budget_mapping = {
            'Budget-friendly ($)': {'min': Decimal('0'), 'max': Decimal('100')},
            'Mid-range ($$)': {'min': Decimal('100'), 'max': Decimal('500')},
            'Premium ($$$)': {'min': Decimal('500'), 'max': Decimal('2000')},
            'Luxury ($$$$)': {'min': Decimal('2000'), 'max': Decimal('10000')}
        }
        budget = budget_mapping.get(validated_data['budget_range'], {'min': Decimal('0'), 'max': Decimal('1000')})
        style_pref.budget_min = budget['min']
        style_pref.budget_max = budget['max']
        
        style_pref.save()
        
        return Response({
            'success': True,
            'message': 'Registration completed successfully',
            'data': {
                'user': UserSerializer(user).data
            }
        }, status=status.HTTP_200_OK)

