"""
Serializers for accounts app.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile, StylePreference, UserFollowing


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""
    
    class Meta:
        model = UserProfile
        exclude = ['id', 'user', 'created_at', 'updated_at']


class StylePreferenceSerializer(serializers.ModelSerializer):
    """Serializer for StylePreference model."""
    
    class Meta:
        model = StylePreference
        exclude = ['id', 'user', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    profile = UserProfileSerializer(read_only=True)
    style_preference = StylePreferenceSerializer(read_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'avatar', 'bio', 'is_verified', 'profile', 'style_preference',
            'followers_count', 'following_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_verified', 'created_at', 'updated_at']
    
    def get_followers_count(self, obj):
        return obj.followers.count()
    
    def get_following_count(self, obj):
        return obj.following.count()


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Create related profile and style preference
        UserProfile.objects.create(user=user)
        StylePreference.objects.create(user=user)
        
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user information."""
    profile = UserProfileSerializer(required=False)
    style_preference = StylePreferenceSerializer(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'avatar', 'bio', 'profile', 'style_preference']
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        style_preference_data = validated_data.pop('style_preference', None)
        
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update profile if provided
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        # Update style preference if provided
        if style_preference_data:
            style_pref = instance.style_preference
            for attr, value in style_preference_data.items():
                setattr(style_pref, attr, value)
            style_pref.save()
        
        return instance


class UserFollowingSerializer(serializers.ModelSerializer):
    """Serializer for following relationships."""
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)
    
    class Meta:
        model = UserFollowing
        fields = ['id', 'follower', 'following', 'created_at']

