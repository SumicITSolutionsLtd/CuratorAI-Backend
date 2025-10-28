"""
Serializers for social app.
"""
from rest_framework import serializers
from apps.accounts.models import User
from .models import Post, PostImage, PostLike, PostSave, Comment, CommentLike


class PostImageSerializer(serializers.ModelSerializer):
    """Serializer for post images."""
    
    class Meta:
        model = PostImage
        fields = ['id', 'image', 'order', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user serializer for nested use."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', 'is_verified']


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
    
    class Meta:
        model = Post
        fields = [
            'id', 'user', 'caption', 'tags', 'outfit_id', 'tagged_items',
            'location_name', 'images', 'likes_count', 'comments_count', 
            'shares_count', 'saves_count', 'views_count', 'is_liked', 
            'is_saved', 'privacy', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'likes_count', 'comments_count', 'shares_count', 
            'saves_count', 'views_count', 'created_at', 'updated_at'
        ]
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostLike.objects.filter(user=request.user, post=obj).exists()
        return False
    
    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostSave.objects.filter(user=request.user, post=obj).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating posts."""
    
    class Meta:
        model = Post
        fields = ['caption', 'tags', 'outfit_id', 'tagged_items', 'location_name', 'location_lat', 'location_lng', 'privacy']

