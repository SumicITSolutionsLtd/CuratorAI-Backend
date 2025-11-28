"""
Views for social app - Posts, Feed, Comments.
"""
from rest_framework import generics, status, views, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer, OpenApiTypes
from core.serializers import ValidationErrorResponse, UnauthorizedErrorResponse, NotFoundErrorResponse, ForbiddenErrorResponse
from .models import Post, PostImage, PostLike, PostSave, Comment, CommentLike
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer, PostImageSerializer


class SocialFeedView(generics.ListAPIView):
    """
    Get social feed (posts from following users or discover feed).
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get social feed",
        description="Get posts feed (following, discover, or trending)",
        tags=["Social Feed"],
        parameters=[
            OpenApiParameter(name='type', description='Feed type: following, discover, trending', required=False, type=str),
            OpenApiParameter(name='page', description='Page number', required=False, type=int),
        ],
        responses={
            200: inline_serializer(
                name='SocialFeedResponse',
                fields={
                    'count': serializers.IntegerField(),
                    'next': serializers.URLField(allow_null=True),
                    'previous': serializers.URLField(allow_null=True),
                    'results': PostSerializer(many=True),
                }
            ),
            401: UnauthorizedErrorResponse,
        }
    )
    def get_queryset(self):
        feed_type = self.request.query_params.get('type', 'following')
        user = self.request.user
        
        try:
            if feed_type == 'following':
                # Posts from users the current user follows
                following_users = list(user.following.values_list('following_id', flat=True))
                if following_users:
                    queryset = Post.objects.filter(
                        user_id__in=following_users,
                        is_deleted=False,
                        privacy='public'
                    )
                else:
                    # Return empty queryset if user doesn't follow anyone
                    queryset = Post.objects.none()
            elif feed_type == 'trending':
                # Posts with high engagement
                queryset = Post.objects.filter(
                    is_deleted=False,
                    privacy='public'
                ).order_by('-likes_count', '-created_at')
            elif feed_type == 'forYou' or feed_type == 'foryou':
                # "For You" feed - mix of all public posts including user's own posts
                # This is similar to discover but includes the user's own posts
                queryset = Post.objects.filter(
                    is_deleted=False,
                    privacy='public'
                )
            else:  # discover
                # All public posts (excluding user's own posts)
                queryset = Post.objects.filter(
                    is_deleted=False,
                    privacy='public'
                ).exclude(user=user)
        except Exception as e:
            # Log the error and fallback to empty queryset
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in get_queryset: {str(e)}", exc_info=True)
            queryset = Post.objects.none()
        
        return queryset.order_by('-created_at')


class PostDetailView(generics.RetrieveAPIView):
    """
    Get single post details.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get post",
        description="Get detailed information about a post",
        tags=["Social Feed"],
        responses={
            200: PostSerializer,
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def get_queryset(self):
        return Post.objects.filter(is_deleted=False)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Increment view count
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PostCreateView(generics.CreateAPIView):
    """
    Create a new post.
    """
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Create post",
        description="Create a new social post",
        tags=["Social Feed"],
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'caption': {'type': 'string'},
                    'tags': {'type': 'string'},
                    'outfit_id': {'type': 'integer'},
                    'location_name': {'type': 'string'},
                    'privacy': {'type': 'string', 'enum': ['public', 'private', 'followers']},
                    'images': {'type': 'array', 'items': {'type': 'string', 'format': 'binary'}},
                }
            }
        },
        responses={
            201: inline_serializer(
                name='PostCreateResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': PostSerializer(),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
        }
    )
    def create(self, request, *args, **kwargs):
        import logging
        import traceback
        logger = logging.getLogger(__name__)
        
        try:
            # Log incoming request data for debugging
            logger.info(f"Creating post with data: {dict(request.data)}")
            
            serializer = self.get_serializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            
            # Create post - user is obtained from request context in serializer.create()
            # The serializer will handle images_data and image_urls
            try:
                post = serializer.save()
                logger.info(f"Post created successfully with ID: {post.id}")
            except Exception as create_error:
                error_traceback = traceback.format_exc()
                logger.error(f"Error in serializer.save(): {str(create_error)}")
                logger.error(f"Full traceback:\n{error_traceback}")
                raise
            
            # Handle legacy multipart/form-data image uploads (if images_data/image_urls not provided)
            # This supports the old 'images' field name for backward compatibility
            try:
                if not post.images.exists():
                    images = request.FILES.getlist('images')
                    for idx, image in enumerate(images[:10]):  # Max 10 images
                        if image:  # Check if file is not None
                            PostImage.objects.create(post=post, image=image, order=idx)
            except Exception as img_upload_error:
                logger.warning(f"Error handling legacy image uploads: {str(img_upload_error)}")
                # Don't fail the entire request if legacy image upload fails
            
            # Return wrapped response - refresh from DB to ensure all relationships are loaded
            post.refresh_from_db()
            
            # Try to serialize the post with proper error handling
            try:
                # Use select_related to prefetch user and outfit to avoid N+1 queries
                post = Post.objects.select_related('user', 'outfit').prefetch_related('images').get(pk=post.pk)
                serializer_data = PostSerializer(post, context={'request': request}).data
            except Exception as serialization_error:
                # Log serialization error with full traceback
                error_traceback = traceback.format_exc()
                logger.error(f"Error serializing post response: {str(serialization_error)}")
                logger.error(f"Full traceback:\n{error_traceback}")
                
                # Return a simplified response if serialization fails
                try:
                    serializer_data = {
                        'id': post.id,
                        'caption': getattr(post, 'caption', ''),
                        'tags': getattr(post, 'tags', []),
                        'privacy': getattr(post, 'privacy', 'public'),
                        'created_at': post.created_at.isoformat() if hasattr(post, 'created_at') and post.created_at else None,
                        'updated_at': post.updated_at.isoformat() if hasattr(post, 'updated_at') and post.updated_at else None,
                    }
                    
                    # Try to add user info safely
                    try:
                        if post.user:
                            serializer_data['user'] = {
                                'id': post.user.id,
                                'username': getattr(post.user, 'username', ''),
                                'first_name': getattr(post.user, 'first_name', ''),
                                'last_name': getattr(post.user, 'last_name', ''),
                            }
                        else:
                            serializer_data['user'] = None
                    except Exception as user_error:
                        logger.error(f"Error serializing user: {str(user_error)}")
                        serializer_data['user'] = None
                    
                    # Try to add images safely
                    try:
                        images = []
                        for img in post.images.all()[:10]:  # Limit to 10 images
                            img_data = {
                                'id': img.id,
                                'order': getattr(img, 'order', 0),
                            }
                            # Try to get image URL
                            if hasattr(img, 'image_url') and img.image_url:
                                img_data['image'] = img.image_url
                            elif hasattr(img, 'image') and img.image:
                                try:
                                    img_data['image'] = request.build_absolute_uri(img.image.url) if request else img.image.url
                                except:
                                    img_data['image'] = None
                            else:
                                img_data['image'] = None
                            images.append(img_data)
                        serializer_data['images'] = images
                    except Exception as img_error:
                        logger.error(f"Error serializing images: {str(img_error)}")
                        serializer_data['images'] = []
                    
                    # Add other fields safely
                    serializer_data['likes_count'] = getattr(post, 'likes_count', 0)
                    serializer_data['comments_count'] = getattr(post, 'comments_count', 0)
                    serializer_data['saves_count'] = getattr(post, 'saves_count', 0)
                    serializer_data['views_count'] = getattr(post, 'views_count', 0)
                    serializer_data['is_liked'] = False
                    serializer_data['is_saved'] = False
                    serializer_data['outfit'] = None
                    serializer_data['outfit_id'] = post.outfit.id if hasattr(post, 'outfit') and post.outfit else None
                    
                except Exception as e:
                    logger.error(f"Error creating simplified response: {str(e)}", exc_info=True)
                    # Last resort - minimal response
                    serializer_data = {
                        'id': post.id,
                        'caption': getattr(post, 'caption', ''),
                    }
            
            return Response({
                'success': True,
                'message': 'Post created successfully',
                'data': serializer_data
            }, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            # Log validation errors
            error_traceback = traceback.format_exc()
            logger.error(f"Validation error creating post: {str(e)}")
            logger.error(f"Validation error details: {e.detail if hasattr(e, 'detail') else 'No details'}")
            logger.error(f"Full traceback:\n{error_traceback}")
            # Re-raise validation errors as-is (DRF will handle them)
            raise
        except Exception as e:
            # Log unexpected errors with full traceback
            error_traceback = traceback.format_exc()
            logger.error(f"Unexpected error creating post: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Full traceback:\n{error_traceback}")
            # Return a 500 error with details (include error message for debugging)
            return Response({
                'success': False,
                'message': f'An error occurred while creating the post: {str(e)}',
                'error': str(e),
                'error_type': type(e).__name__,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostUpdateView(generics.UpdateAPIView):
    """
    Update a post.
    """
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Update post",
        description="Update post caption, tags, or privacy",
        tags=["Social Feed"],
        request=PostCreateSerializer,
        responses={
            200: inline_serializer(
                name='PostUpdateResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': PostSerializer(),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
            403: ForbiddenErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user, is_deleted=False)


class PostDeleteView(generics.DestroyAPIView):
    """
    Delete a post (soft delete).
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Delete post",
        description="Soft delete a post",
        tags=["Social Feed"],
        responses={
            204: OpenApiTypes.NONE,
            401: UnauthorizedErrorResponse,
            403: ForbiddenErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user, is_deleted=False)
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class LikePostView(views.APIView):
    """
    Like/unlike a post.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Like/unlike post",
        description="Toggle like on a post",
        tags=["Social Feed"],
        responses={
            200: inline_serializer(
                name='LikePostResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'is_liked': serializers.BooleanField(),
                    'likes_count': serializers.IntegerField(),
                }
            ),
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, is_deleted=False)
        
        # Check if already liked
        like = PostLike.objects.filter(user=request.user, post=post).first()
        
        if like:
            # Unlike
            like.delete()
            post.likes_count = max(0, post.likes_count - 1)
            post.save(update_fields=['likes_count'])
            
            return Response({
                'success': True,
                'message': 'Post unliked',
                'is_liked': False,
                'likes_count': post.likes_count
            }, status=status.HTTP_200_OK)
        else:
            # Like
            PostLike.objects.create(user=request.user, post=post)
            post.likes_count += 1
            post.save(update_fields=['likes_count'])
            
            return Response({
                'success': True,
                'message': 'Post liked successfully',
                'is_liked': True,
                'likes_count': post.likes_count
            }, status=status.HTTP_200_OK)


class SavePostView(views.APIView):
    """
    Save/unsave a post.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Save/unsave post",
        description="Toggle save on a post",
        tags=["Social Feed"],
        responses={
            200: inline_serializer(
                name='SavePostResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'is_saved': serializers.BooleanField(),
                    'saves_count': serializers.IntegerField(),
                }
            ),
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, is_deleted=False)
        
        # Check if already saved
        save = PostSave.objects.filter(user=request.user, post=post).first()
        
        if save:
            # Unsave
            save.delete()
            post.saves_count = max(0, post.saves_count - 1)
            post.save(update_fields=['saves_count'])
            
            return Response({
                'success': True,
                'message': 'Post unsaved',
                'is_saved': False,
                'saves_count': post.saves_count
            }, status=status.HTTP_200_OK)
        else:
            # Save
            PostSave.objects.create(user=request.user, post=post)
            post.saves_count += 1
            post.save(update_fields=['saves_count'])
            
            return Response({
                'success': True,
                'message': 'Post saved successfully',
                'is_saved': True,
                'saves_count': post.saves_count
            }, status=status.HTTP_200_OK)


class SharePostView(views.APIView):
    """
    Share a post.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Share post",
        description="Share a post (increment share count)",
        tags=["Social Feed"],
        responses={
            200: inline_serializer(
                name='SharePostResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'shares_count': serializers.IntegerField(),
                    'share_url': serializers.URLField(),
                }
            ),
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, is_deleted=False)
        
        # Increment share count
        post.shares_count += 1
        post.save(update_fields=['shares_count'])
        
        return Response({
            'success': True,
            'message': 'Post shared successfully',
            'shares_count': post.shares_count,
            'share_url': f'https://curatorai.com/posts/{post.id}'
        }, status=status.HTTP_200_OK)


class PostCommentsView(generics.ListAPIView):
    """
    Get post comments.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get post comments",
        description="List comments on a post",
        tags=["Social Feed"],
        parameters=[
            OpenApiParameter(name='sort', description='Sort by: recent or popular', required=False, type=str),
            OpenApiParameter(name='page', description='Page number', required=False, type=int),
        ],
        responses={
            200: inline_serializer(
                name='PostCommentsResponse',
                fields={
                    'count': serializers.IntegerField(),
                    'next': serializers.URLField(allow_null=True),
                    'previous': serializers.URLField(allow_null=True),
                    'results': CommentSerializer(many=True),
                }
            ),
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        queryset = Comment.objects.filter(post_id=post_id, parent_comment=None, is_deleted=False)
        
        sort_by = self.request.query_params.get('sort', 'recent')
        if sort_by == 'popular':
            queryset = queryset.order_by('-likes_count', '-created_at')
        
        return queryset


class AddCommentView(views.APIView):
    """
    Add comment to post.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Add comment",
        description="Add a comment to a post",
        tags=["Social Feed"],
        request=inline_serializer(
            name='AddCommentRequest',
            fields={
                'content': serializers.CharField(required=True, max_length=500),
                'parent_comment_id': serializers.IntegerField(required=False, allow_null=True),
            }
        ),
        responses={
            201: inline_serializer(
                name='AddCommentResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'data': CommentSerializer(),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, is_deleted=False)
        
        content = request.data.get('content')
        parent_comment_id = request.data.get('parent_comment_id')
        
        if not content or len(content) > 500:
            return Response({
                'success': False,
                'message': 'Content is required and must be less than 500 characters'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create comment
        comment = Comment.objects.create(
            post=post,
            user=request.user,
            content=content,
            parent_comment_id=parent_comment_id
        )
        
        # Update post comment count
        post.comments_count += 1
        post.save(update_fields=['comments_count'])
        
        serializer = CommentSerializer(comment, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class UpdateCommentView(generics.UpdateAPIView):
    """
    Update a comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Update comment",
        description="Update comment content",
        tags=["Social Feed"],
        request=inline_serializer(
            name='UpdateCommentRequest',
            fields={
                'content': serializers.CharField(required=True, max_length=500),
            }
        ),
        responses={
            200: inline_serializer(
                name='UpdateCommentResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': CommentSerializer(),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
            403: ForbiddenErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user, is_deleted=False)


class DeleteCommentView(generics.DestroyAPIView):
    """
    Delete a comment.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Delete comment",
        description="Delete a comment (soft delete)",
        tags=["Social Feed"],
        responses={
            204: OpenApiTypes.NONE,
            401: UnauthorizedErrorResponse,
            403: ForbiddenErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def get_queryset(self):
        # User can delete their own comments
        # Post owner can delete any comment on their posts
        user_comments = Comment.objects.filter(user=self.request.user, is_deleted=False)
        post_owner_comments = Comment.objects.filter(post__user=self.request.user, is_deleted=False)
        return user_comments | post_owner_comments
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        
        # Update post comment count
        post = instance.post
        post.comments_count = max(0, post.comments_count - 1)
        post.save(update_fields=['comments_count'])


class LikeCommentView(views.APIView):
    """
    Like/unlike a comment.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Like/unlike comment",
        description="Toggle like on a comment",
        tags=["Social Feed"],
        responses={
            200: inline_serializer(
                name='LikeCommentResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'is_liked': serializers.BooleanField(),
                    'likes_count': serializers.IntegerField(),
                }
            ),
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, is_deleted=False)
        
        # Check if already liked
        like = CommentLike.objects.filter(user=request.user, comment=comment).first()
        
        if like:
            # Unlike
            like.delete()
            comment.likes_count = max(0, comment.likes_count - 1)
            comment.save(update_fields=['likes_count'])
            
            return Response({
                'success': True,
                'message': 'Comment unliked',
                'is_liked': False,
                'likes_count': comment.likes_count
            }, status=status.HTTP_200_OK)
        else:
            # Like
            CommentLike.objects.create(user=request.user, comment=comment)
            comment.likes_count += 1
            comment.save(update_fields=['likes_count'])
            
            return Response({
                'success': True,
                'message': 'Comment liked successfully',
                'is_liked': True,
                'likes_count': comment.likes_count
            }, status=status.HTTP_200_OK)

