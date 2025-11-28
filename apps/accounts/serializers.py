"""
Serializers for accounts app.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
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
    avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'avatar', 'bio', 'is_verified', 'terms_and_conditions_accepted',
            'terms_accepted_at', 'profile', 'style_preference',
            'followers_count', 'following_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_verified', 'terms_accepted_at', 'created_at', 'updated_at']
    
    def get_avatar(self, obj):
        """Return avatar URL from avatar_url field or ImageField as fallback."""
        # Prioritize avatar_url field (external URL) over ImageField - ALWAYS
        if obj.avatar_url and obj.avatar_url.strip():
            return obj.avatar_url
        # Fallback to ImageField if avatar_url is not set or empty
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None
    
    def get_followers_count(self, obj):
        return obj.followers.count()
    
    def get_following_count(self, obj):
        return obj.following.count()


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    terms_and_conditions_accepted = serializers.BooleanField(required=True, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name', 'terms_and_conditions_accepted']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if not attrs.get('terms_and_conditions_accepted', False):
            raise serializers.ValidationError({"terms_and_conditions_accepted": "You must accept the terms and conditions to register."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        terms_accepted = validated_data.pop('terms_and_conditions_accepted')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            terms_and_conditions_accepted=terms_accepted,
            terms_accepted_at=timezone.now() if terms_accepted else None
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
        extra_kwargs = {
            'username': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'avatar': {'required': False},
            'bio': {'required': False},
        }
    
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


class StylePreferenceCompletionSerializer(serializers.Serializer):
    """Serializer for completing registration with style preferences."""
    # I shop for - single select
    shop_for = serializers.ChoiceField(
        choices=['Men', 'Women', 'Non-binary', 'Prefer not to say'],
        required=True,
        help_text="Shopping preference: Men, Women, Non-binary, or Prefer not to say"
    )
    
    # My style - multi-select
    styles = serializers.ListField(
        child=serializers.ChoiceField(choices=[
            'Casual', 'Formal', 'Streetwear', 'Bohemian', 
            'Minimalist', 'Vintage', 'Athletic', 'Trendy'
        ]),
        required=True,
        allow_empty=False,
        help_text="List of preferred styles (at least one required)"
    )
    
    # I dress for - multi-select
    dress_for = serializers.ListField(
        child=serializers.ChoiceField(choices=[
            'Work', 'Casual', 'Date Night', 'Party', 
            'Gym', 'Travel', 'Beach', 'Wedding'
        ]),
        required=True,
        allow_empty=False,
        help_text="List of occasions to dress for (at least one required)"
    )
    
    # My budget range - single select
    budget_range = serializers.ChoiceField(
        choices=['Budget-friendly ($)', 'Mid-range ($$)', 'Premium ($$$)', 'Luxury ($$$$)'],
        required=True,
        help_text="Budget range: Budget-friendly ($), Mid-range ($$), Premium ($$$), or Luxury ($$$$)"
    )
    
    def validate_styles(self, value):
        """Validate that at least one style is selected."""
        if not value or len(value) == 0:
            raise serializers.ValidationError("At least one style must be selected.")
        return value
    
    def validate_dress_for(self, value):
        """Validate that at least one occasion is selected."""
        if not value or len(value) == 0:
            raise serializers.ValidationError("At least one occasion must be selected.")
        return value

