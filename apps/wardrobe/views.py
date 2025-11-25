"""
Views for wardrobe app.
"""
from rest_framework import generics, status, views, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count, Avg
from django.db import models
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer, OpenApiTypes
from core.serializers import ValidationErrorResponse, UnauthorizedErrorResponse, NotFoundErrorResponse, ForbiddenErrorResponse
from .models import Wardrobe, WardrobeItem, WardrobeItemImage, WardrobeItemWearLog
from .serializers import (
    WardrobeSerializer,
    WardrobeItemSerializer,
    WardrobeItemCreateSerializer,
    WardrobeItemImageSerializer,
    WardrobeItemWearLogSerializer
)


class UserWardrobeView(generics.RetrieveAPIView):
    """
    Get user's wardrobe.
    """
    serializer_class = WardrobeSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get user wardrobe",
        description="Retrieve user's wardrobe with item counts",
        tags=["Wardrobe"],
        responses={
            200: inline_serializer(
                name='WardrobeResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': WardrobeSerializer(),
                }
            ),
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def get_object(self):
        user_id = self.kwargs.get('user_id')
        wardrobe, _ = Wardrobe.objects.get_or_create(user_id=user_id)
        return wardrobe


class WardrobeItemListView(generics.ListAPIView):
    """
    List wardrobe items with filtering.
    """
    serializer_class = WardrobeItemSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="List wardrobe items",
        description="List user's wardrobe items with optional filtering",
        tags=["Wardrobe"],
        parameters=[
            OpenApiParameter(name='category', description='Filter by category', required=False, type=str),
            OpenApiParameter(name='color', description='Filter by color', required=False, type=str),
            OpenApiParameter(name='season', description='Filter by season', required=False, type=str),
            OpenApiParameter(name='brand', description='Filter by brand', required=False, type=str),
            OpenApiParameter(name='tags', description='Filter by tags (comma-separated)', required=False, type=str),
            OpenApiParameter(name='page', description='Page number', required=False, type=int),
        ],
        responses={
            200: inline_serializer(
                name='WardrobeItemListResponse',
                fields={
                    'count': serializers.IntegerField(),
                    'next': serializers.URLField(allow_null=True),
                    'previous': serializers.URLField(allow_null=True),
                    'results': WardrobeItemSerializer(many=True),
                }
            ),
            401: UnauthorizedErrorResponse,
        }
    )
    def get_queryset(self):
        wardrobe, _ = Wardrobe.objects.get_or_create(user=self.request.user)
        queryset = WardrobeItem.objects.filter(wardrobe=wardrobe, is_deleted=False)
        
        # Apply filters
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        color = self.request.query_params.get('color')
        if color:
            queryset = queryset.filter(color__icontains=color)
        
        season = self.request.query_params.get('season')
        if season:
            queryset = queryset.filter(season=season)
        
        brand = self.request.query_params.get('brand')
        if brand:
            queryset = queryset.filter(brand__icontains=brand)
        
        tags = self.request.query_params.get('tags')
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            for tag in tag_list:
                queryset = queryset.filter(tags__contains=tag)
        
        return queryset


class WardrobeItemDetailView(generics.RetrieveAPIView):
    """
    Get single wardrobe item details.
    """
    serializer_class = WardrobeItemSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get wardrobe item",
        description="Retrieve detailed information about a wardrobe item",
        tags=["Wardrobe"],
        responses={
            200: inline_serializer(
                name='WardrobeItemDetailResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': WardrobeItemSerializer(),
                }
            ),
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def get_queryset(self):
        wardrobe, _ = Wardrobe.objects.get_or_create(user=self.request.user)
        return WardrobeItem.objects.filter(wardrobe=wardrobe, is_deleted=False)


class WardrobeItemCreateView(generics.CreateAPIView):
    """
    Add item to wardrobe.
    """
    serializer_class = WardrobeItemCreateSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Add wardrobe item",
        description="Add a new item to user's wardrobe",
        tags=["Wardrobe"],
        request=WardrobeItemCreateSerializer,
        responses={
            201: inline_serializer(
                name='WardrobeItemCreateResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': WardrobeItemSerializer(),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
        }
    )
    def perform_create(self, serializer):
        wardrobe, _ = Wardrobe.objects.get_or_create(user=self.request.user)
        serializer.save(wardrobe=wardrobe)


class WardrobeItemUpdateView(generics.UpdateAPIView):
    """
    Update wardrobe item.
    """
    serializer_class = WardrobeItemSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Update wardrobe item",
        description="Update a wardrobe item's information",
        tags=["Wardrobe"],
        request=WardrobeItemSerializer,
        responses={
            200: inline_serializer(
                name='WardrobeItemUpdateResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'data': WardrobeItemSerializer(),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def get_queryset(self):
        wardrobe, _ = Wardrobe.objects.get_or_create(user=self.request.user)
        return WardrobeItem.objects.filter(wardrobe=wardrobe, is_deleted=False)


class WardrobeItemDeleteView(generics.DestroyAPIView):
    """
    Delete wardrobe item (soft delete).
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Delete wardrobe item",
        description="Soft delete a wardrobe item",
        tags=["Wardrobe"],
        responses={
            204: OpenApiTypes.NONE,
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def get_queryset(self):
        wardrobe, _ = Wardrobe.objects.get_or_create(user=self.request.user)
        return WardrobeItem.objects.filter(wardrobe=wardrobe, is_deleted=False)
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.is_deleted = True
        instance.save()


class WardrobeItemImageUploadView(views.APIView):
    """
    Upload image to wardrobe item.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Upload item image",
        description="Upload an image for a wardrobe item",
        tags=["Wardrobe"],
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'image': {'type': 'string', 'format': 'binary'},
                    'is_primary': {'type': 'boolean', 'default': False},
                },
                'required': ['image']
            }
        },
        responses={
            201: inline_serializer(
                name='WardrobeItemImageResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'data': WardrobeItemImageSerializer(),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def post(self, request, item_id):
        wardrobe, _ = Wardrobe.objects.get_or_create(user=request.user)
        item = get_object_or_404(WardrobeItem, id=item_id, wardrobe=wardrobe, is_deleted=False)
        
        image = request.FILES.get('image')
        is_primary = request.data.get('is_primary', 'false').lower() == 'true'
        
        if not image:
            return Response({
                'success': False,
                'message': 'Image is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # If setting as primary, unset other primary images
        if is_primary:
            WardrobeItemImage.objects.filter(item=item, is_primary=True).update(is_primary=False)
            item.primary_image = image
            item.save()
        
        # Create image record
        item_image = WardrobeItemImage.objects.create(
            item=item,
            image=image,
            is_primary=is_primary
        )
        
        serializer = WardrobeItemImageSerializer(item_image)
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class MarkItemAsWornView(views.APIView):
    """
    Mark item as worn on a specific date.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Mark item as worn",
        description="Log that an item was worn on a specific date",
        tags=["Wardrobe"],
        request=inline_serializer(
            name='MarkWornRequest',
            fields={
                'date': serializers.DateField(required=False),
                'outfit_id': serializers.IntegerField(required=False, allow_null=True),
            }
        ),
        responses={
            200: inline_serializer(
                name='MarkWornResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'times_worn': serializers.IntegerField(),
                    'last_worn': serializers.DateField(),
                }
            ),
            400: ValidationErrorResponse,
            401: UnauthorizedErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def post(self, request, item_id):
        wardrobe, _ = Wardrobe.objects.get_or_create(user=request.user)
        item = get_object_or_404(WardrobeItem, id=item_id, wardrobe=wardrobe, is_deleted=False)
        
        worn_date = request.data.get('date', timezone.now().date())
        outfit_id = request.data.get('outfit_id')
        
        # Create wear log
        WardrobeItemWearLog.objects.create(
            item=item,
            worn_date=worn_date,
            outfit_id=outfit_id
        )
        
        # Update item statistics
        item.times_worn += 1
        item.last_worn_date = worn_date
        item.save()
        
        return Response({
            'success': True,
            'message': 'Item marked as worn',
            'times_worn': item.times_worn,
            'last_worn': item.last_worn_date
        }, status=status.HTTP_200_OK)


class WardrobeStatisticsView(views.APIView):
    """
    Get wardrobe statistics.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get wardrobe statistics",
        description="Get detailed statistics about user's wardrobe",
        tags=["Wardrobe"],
        responses={
            200: inline_serializer(
                name='WardrobeStatisticsResponse',
                fields={
                    'total_items': serializers.IntegerField(),
                    'total_value': serializers.FloatField(),
                    'currency': serializers.CharField(),
                    'categories': serializers.DictField(),
                    'colors': serializers.DictField(),
                    'brands': serializers.DictField(),
                    'most_worn_items': serializers.ListField(),
                    'least_worn_items': serializers.ListField(),
                    'average_wear_per_item': serializers.FloatField(),
                    'items_never_worn': serializers.IntegerField(),
                }
            ),
            401: UnauthorizedErrorResponse,
            403: ForbiddenErrorResponse,
            404: NotFoundErrorResponse,
        }
    )
    def get(self, request, user_id):
        wardrobe, _ = Wardrobe.objects.get_or_create(user_id=user_id)
        items = WardrobeItem.objects.filter(wardrobe=wardrobe, is_deleted=False)
        
        # Calculate statistics
        total_items = items.count()
        total_value = sum(item.price for item in items if item.price)
        
        # Category breakdown
        categories = {}
        for category_code, category_name in WardrobeItem.CATEGORY_CHOICES:
            count = items.filter(category=category_code).count()
            if count > 0:
                categories[category_code] = count
        
        # Color breakdown
        colors = {}
        for item in items:
            if item.color:
                color = item.color.lower()
                colors[color] = colors.get(color, 0) + 1
        
        # Brand breakdown
        brands = {}
        for item in items.filter(brand__isnull=False).exclude(brand=''):
            brand = item.brand
            brands[brand] = brands.get(brand, 0) + 1
        
        # Most worn items
        most_worn = items.order_by('-times_worn')[:5]
        most_worn_data = [{
            'id': str(item.id),
            'name': item.name,
            'times_worn': item.times_worn,
            'image': request.build_absolute_uri(item.primary_image.url) if item.primary_image else None
        } for item in most_worn if item.times_worn > 0]
        
        # Least worn items
        least_worn = items.filter(times_worn__gt=0).order_by('times_worn')[:5]
        least_worn_data = [{
            'id': str(item.id),
            'name': item.name,
            'times_worn': item.times_worn,
            'image': request.build_absolute_uri(item.primary_image.url) if item.primary_image else None
        } for item in least_worn]
        
        # Never worn items
        items_never_worn = items.filter(times_worn=0).count()
        
        # Average wear per item
        avg_wear = items.aggregate(avg=models.Avg('times_worn'))['avg'] or 0
        
        return Response({
            'total_items': total_items,
            'total_value': float(total_value) if total_value else 0,
            'currency': 'USD',  # TODO: Use user's preferred currency
            'categories': categories,
            'colors': dict(sorted(colors.items(), key=lambda x: x[1], reverse=True)[:10]),
            'brands': dict(sorted(brands.items(), key=lambda x: x[1], reverse=True)[:10]),
            'most_worn_items': most_worn_data,
            'least_worn_items': least_worn_data,
            'average_wear_per_item': round(avg_wear, 1),
            'items_never_worn': items_never_worn
        }, status=status.HTTP_200_OK)

