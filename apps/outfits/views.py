"""
Views for outfits app.
"""
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from core.permissions import IsOwnerOrReadOnly
from .models import Outfit, OutfitLike, OutfitSave
from .serializers import OutfitSerializer, OutfitCreateSerializer


class OutfitListCreateView(generics.ListCreateAPIView):
    """
    List all public outfits or create a new outfit.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OutfitCreateSerializer
        return OutfitSerializer
    
    def get_queryset(self):
        queryset = Outfit.objects.filter(is_public=True)
        
        # Filter by occasion
        occasion = self.request.query_params.get('occasion')
        if occasion:
            queryset = queryset.filter(occasion=occasion)
        
        # Filter by season
        season = self.request.query_params.get('season')
        if season:
            queryset = queryset.filter(season=season)
        
        # Search by title or description
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset.select_related('user').prefetch_related('items')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @extend_schema(
        summary="List outfits",
        description="Get paginated list of public outfits with optional filters",
        tags=["Outfits"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create outfit",
        description="Create a new outfit with items",
        tags=["Outfits"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class OutfitDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete an outfit.
    """
    queryset = Outfit.objects.all()
    serializer_class = OutfitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Get outfit details",
        description="Retrieve detailed information about a specific outfit",
        tags=["Outfits"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="Update outfit",
        description="Update outfit details (owner only)",
        tags=["Outfits"]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @extend_schema(
        summary="Delete outfit",
        description="Delete an outfit (owner only)",
        tags=["Outfits"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class OutfitLikeView(views.APIView):
    """
    Like or unlike an outfit.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Like outfit",
        description="Like or unlike an outfit",
        tags=["Outfits"]
    )
    def post(self, request, pk):
        try:
            outfit = Outfit.objects.get(pk=pk)
        except Outfit.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Outfit not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if already liked
        like, created = OutfitLike.objects.get_or_create(
            user=request.user,
            outfit=outfit
        )
        
        if created:
            # Increment likes count
            outfit.likes_count += 1
            outfit.save(update_fields=['likes_count'])
            message = 'Outfit liked'
        else:
            # Unlike
            like.delete()
            outfit.likes_count = max(0, outfit.likes_count - 1)
            outfit.save(update_fields=['likes_count'])
            message = 'Outfit unliked'
        
        return Response({
            'success': True,
            'message': message,
            'likes_count': outfit.likes_count
        }, status=status.HTTP_200_OK)


class OutfitSaveView(views.APIView):
    """
    Save or unsave an outfit.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Save outfit",
        description="Save or unsave an outfit to user's collection",
        tags=["Outfits"]
    )
    def post(self, request, pk):
        try:
            outfit = Outfit.objects.get(pk=pk)
        except Outfit.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Outfit not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        collection_name = request.data.get('collection_name', '')
        
        # Check if already saved
        save, created = OutfitSave.objects.get_or_create(
            user=request.user,
            outfit=outfit,
            defaults={'collection_name': collection_name}
        )
        
        if created:
            # Increment saves count
            outfit.saves_count += 1
            outfit.save(update_fields=['saves_count'])
            message = 'Outfit saved'
        else:
            # Unsave
            save.delete()
            outfit.saves_count = max(0, outfit.saves_count - 1)
            outfit.save(update_fields=['saves_count'])
            message = 'Outfit removed from saved'
        
        return Response({
            'success': True,
            'message': message,
            'saves_count': outfit.saves_count
        }, status=status.HTTP_200_OK)


class UserOutfitsView(generics.ListAPIView):
    """
    List outfits created by a specific user.
    """
    serializer_class = OutfitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Outfit.objects.filter(user_id=user_id, is_public=True).select_related('user').prefetch_related('items')
    
    @extend_schema(
        summary="Get user outfits",
        description="List all public outfits by a specific user",
        tags=["Outfits"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

