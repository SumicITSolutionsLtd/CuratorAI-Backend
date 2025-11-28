"""
Serializers for social app.
"""
from rest_framework import serializers
from apps.accounts.models import User
from .models import Post, PostImage, PostLike, PostSave, Comment, CommentLike


class PostImageSerializer(serializers.ModelSerializer):
    """Serializer for post images."""
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = PostImage
        fields = ['id', 'image', 'order', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_image(self, obj):
        """Return image URL from image_url field or ImageField as fallback."""
        try:
            # Prioritize image_url field (external URL) over ImageField - ALWAYS
            if obj.image_url and obj.image_url.strip():
                return obj.image_url
            # Fallback to ImageField if image_url is not set or empty
            if obj.image:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.image.url)
                return obj.image.url
        except Exception:
            pass
        return None


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user serializer for nested use."""
    avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', 'avatar_url', 'is_verified']
    
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


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments."""
    user = UserBasicSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post_id', 'user', 'content', 'parent_comment_id', 
            'likes_count', 'is_liked', 'replies_count', 'replies',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'post_id', 'created_at', 'updated_at']
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return CommentLike.objects.filter(user=request.user, comment=obj).exists()
        return False
    
    def get_replies_count(self, obj):
        return obj.replies.filter(is_deleted=False).count()
    
    def get_replies(self, obj):
        # Only show first 3 replies
        replies = obj.replies.filter(is_deleted=False)[:3]
        return CommentSerializer(replies, many=True, context=self.context).data


class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts."""
    user = UserBasicSerializer(read_only=True)
    images = PostImageSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    outfit_id = serializers.IntegerField(source='outfit.id', read_only=True, allow_null=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'user', 'caption', 'tags', 'outfit', 'outfit_id', 'tagged_items',
            'location_name', 'images', 'likes_count', 'comments_count', 
            'shares_count', 'saves_count', 'views_count', 'is_liked', 
            'is_saved', 'privacy', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'likes_count', 'comments_count', 'shares_count', 
            'saves_count', 'views_count', 'created_at', 'updated_at'
        ]
    
    def get_is_liked(self, obj):
        try:
            request = self.context.get('request')
            if request and request.user and request.user.is_authenticated:
                return PostLike.objects.filter(user=request.user, post=obj).exists()
        except Exception:
            pass
        return False
    
    def get_is_saved(self, obj):
        try:
            request = self.context.get('request')
            if request and request.user and request.user.is_authenticated:
                return PostSave.objects.filter(user=request.user, post=obj).exists()
        except Exception:
            pass
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating posts."""
    images_data = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        help_text="List of image files to upload"
    )
    image_urls = serializers.ListField(
        child=serializers.URLField(),
        write_only=True,
        required=False,
        help_text="List of external image URLs"
    )
    outfit_id = serializers.IntegerField(write_only=True, required=False, allow_null=True, help_text="Outfit ID (alternative to outfit)")
    
    class Meta:
        model = Post
        fields = ['caption', 'tags', 'outfit', 'outfit_id', 'tagged_items', 'location_name', 'location_lat', 'location_lng', 'privacy', 'images_data', 'image_urls']
        extra_kwargs = {
            'caption': {'required': True, 'allow_blank': True},  # Allow blank to pass through to validation
            'tags': {'required': False},
            'outfit': {'required': False, 'allow_null': True},
            'tagged_items': {'required': False},
            'location_name': {'required': False, 'allow_blank': True},
            'location_lat': {'required': False, 'allow_null': True},
            'location_lng': {'required': False, 'allow_null': True},
            'privacy': {'required': False},
        }
    
    def validate_caption(self, value):
        """Validate caption is not blank."""
        # Handle None, empty string, or whitespace-only strings
        if value is None:
            raise serializers.ValidationError("Caption is required.")
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise serializers.ValidationError("Caption cannot be blank. Please provide a caption for your post.")
        return value
    
    def validate(self, data):
        """Set defaults for optional fields."""
        # Ensure caption is present and not blank (double-check in case validate_caption wasn't called)
        caption = data.get('caption')
        if caption is None:
            raise serializers.ValidationError({'caption': 'Caption is required.'})
        if isinstance(caption, str) and not caption.strip():
            raise serializers.ValidationError({'caption': 'Caption cannot be blank. Please provide a caption for your post.'})
        
        # Strip caption if it's a string
        if isinstance(caption, str):
            data['caption'] = caption.strip()
        
        # Handle outfit_id -> outfit conversion (support both field names)
        outfit_id = data.pop('outfit_id', None)
        if outfit_id is not None and 'outfit' not in data:
            from apps.outfits.models import Outfit
            try:
                outfit = Outfit.objects.get(pk=outfit_id)
                data['outfit'] = outfit
            except Outfit.DoesNotExist:
                raise serializers.ValidationError({'outfit_id': f'Outfit with id {outfit_id} does not exist.'})
        
        if 'tags' not in data or not data.get('tags'):
            data['tags'] = []
        if 'tagged_items' not in data or not data.get('tagged_items'):
            data['tagged_items'] = []
        if 'privacy' not in data or not data.get('privacy'):
            data['privacy'] = 'public'
        return data
    
    def create(self, validated_data):
        """Create post and handle images."""
        try:
            # Extract image data
            images_data = validated_data.pop('images_data', []) or []
            image_urls = validated_data.pop('image_urls', []) or []
            
            # Get user from request context (set by view)
            request = self.context.get('request')
            if not request or not request.user or not request.user.is_authenticated:
                raise serializers.ValidationError("User is required to create a post. Please ensure you are authenticated.")
            
            user = request.user
            
            # Create the post
            post = Post.objects.create(user=user, **validated_data)
            
            # Handle file uploads (from images_data field)
            if images_data:
                for idx, image_file in enumerate(images_data):
                    if image_file:  # Check if file is not None
                        PostImage.objects.create(post=post, image=image_file, order=idx)
            
            # Handle URL-based images (from image_urls field)
            if image_urls:
                for idx, image_url in enumerate(image_urls):
                    if image_url and image_url.strip():  # Check if URL is not empty
                        PostImage.objects.create(post=post, image_url=image_url, order=idx + len(images_data))
            
            return post
        except serializers.ValidationError:
            # Re-raise validation errors as-is
            raise
        except Exception as e:
            # Log the error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error creating post: {str(e)}", exc_info=True)
            raise serializers.ValidationError(f"Error creating post: {str(e)}")

