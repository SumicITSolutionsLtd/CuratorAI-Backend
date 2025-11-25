"""
Views for lookbooks app.
"""
from rest_framework import generics, status, views, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer, OpenApiTypes
from core.serializers import ValidationErrorResponse, UnauthorizedErrorResponse, NotFoundErrorResponse, ForbiddenErrorResponse
from .models import Lookbook, LookbookLike
from .serializers import LookbookSerializer, LookbookCreateSerializer


class LookbookListView(generics.ListAPIView):
    """
    List lookbooks with filtering.
    """
    serializer_class = LookbookSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="List lookbooks",
        description="List lookbooks with optional filtering",
        tags=["Lookbooks"],
        parameters=[
            OpenApiParameter(name='season', description='Filter by season', required=False, type=str),
            OpenApiParameter(name='occasion', description='Filter by occasion', required=False, type=str),
            OpenApiParameter(name='featured', description='Show only featured', required=False, type=bool),
            OpenApiParameter(name='page', description='Page number', required=False, type=int),
        ],
        responses={
            200: inline_serializer(
                name='LookbookListResponse',
                fields={
                    'count': serializers.IntegerField(),
                    'next': serializers.URLField(allow_null=True),
                    'previous': serializers.URLField(allow_null=True),
                    'results': LookbookSerializer(many=True),
                }
            ),
            401: UnauthorizedErrorResponse,
        }
    )
    def get_queryset(self):
        queryset = Lookbook.objects.filter(is_public=True)
        
        # Apply filters
        season = self.request.query_params.get('season')
        if season:
            queryset = queryset.filter(season=season)
        
        occasion = self.request.query_params.get('occasion')
        if occasion:
            queryset = queryset.filter(occasion=occasion)
        
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset


class FeaturedLookbooksView(generics.ListAPIView):
    """
    Get featured lookbooks.
    """
    serializer_class = LookbookSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get featured lookbooks",
        description="Get list of featured lookbooks",
        tags=["Lookbooks"],
        responses={
            200: inline_serializer(
                name='FeaturedLookbooksResponse',
                fields={
                    'count': serializers.IntegerField(),
                    'results': LookbookSerializer(many=True),
                }
            ),
            401: UnauthorizedErrorResponse,
        }
    )
    def get_queryset(self):
        return Lookbook.objects.filter(is_public=True, is_featured=True)[:10]


class LookbookDetailView(generics.RetrieveAPIView):
    """
    Get single lookbook details.
    """
    serializer_class = LookbookSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get lookbook",
        description="Get detailed information about a lookbook",
        tags=["Lookbooks"],
        responses={
            200: LookbookSerializer,
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def get_queryset(self):
        return Lookbook.objects.filter(is_public=True)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Increment view count
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class LookbookCreateView(generics.CreateAPIView):
    """
    Create a new lookbook.
    """
    serializer_class = LookbookCreateSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Create lookbook",
        description="Create a new lookbook with curated outfits",
        tags=["Lookbooks"],
        request=LookbookCreateSerializer,
        responses={
            201: inline_serializer(
                name='LookbookCreateResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': LookbookSerializer(),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
        }
    )
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class LookbookUpdateView(generics.UpdateAPIView):
    """
    Update a lookbook.
    """
    serializer_class = LookbookSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Update lookbook",
        description="Update lookbook details",
        tags=["Lookbooks"],
        request=LookbookSerializer,
        responses={
            200: inline_serializer(
                name='LookbookUpdateResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': LookbookSerializer(),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
            403: ForbiddenErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def get_queryset(self):
        return Lookbook.objects.filter(creator=self.request.user)


class LookbookDeleteView(generics.DestroyAPIView):
    """
    Delete a lookbook.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Delete lookbook",
        description="Delete a lookbook",
        tags=["Lookbooks"],
        responses={
            204: OpenApiTypes.NONE,
            401: UnauthorizedErrorResponse,
            403: ForbiddenErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def get_queryset(self):
        return Lookbook.objects.filter(creator=self.request.user)


class LikeLookbookView(views.APIView):
    """
    Like/unlike a lookbook.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Like/unlike lookbook",
        description="Toggle like on a lookbook",
        tags=["Lookbooks"],
        responses={
            200: inline_serializer(
                name='LikeLookbookResponse',
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
    def post(self, request, lookbook_id):
        lookbook = get_object_or_404(Lookbook, id=lookbook_id)
        
        # Check if already liked
        like = LookbookLike.objects.filter(user=request.user, lookbook=lookbook).first()
        
        if like:
            # Unlike
            like.delete()
            lookbook.likes_count = max(0, lookbook.likes_count - 1)
            lookbook.save(update_fields=['likes_count'])
            
            return Response({
                'success': True,
                'message': 'Lookbook unliked',
                'is_liked': False,
                'likes_count': lookbook.likes_count
            }, status=status.HTTP_200_OK)
        else:
            # Like
            LookbookLike.objects.create(user=request.user, lookbook=lookbook)
            lookbook.likes_count += 1
            lookbook.save(update_fields=['likes_count'])
            
            return Response({
                'success': True,
                'message': 'Lookbook liked successfully',
                'is_liked': True,
                'likes_count': lookbook.likes_count
            }, status=status.HTTP_200_OK)


class LookbookCommentsView(views.APIView):
    """
    Get lookbook comments (placeholder for future implementation).
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get lookbook comments",
        description="Get comments on a lookbook",
        tags=["Lookbooks"],
        responses={
            200: inline_serializer(
                name='LookbookCommentsResponse',
                fields={
                    'count': serializers.IntegerField(),
                    'results': serializers.ListField(),
                }
            ),
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def get(self, request, lookbook_id):
        # For now, return empty list
        # Can be implemented similarly to post comments
        return Response({
            'count': 0,
            'results': []
        }, status=status.HTTP_200_OK)

