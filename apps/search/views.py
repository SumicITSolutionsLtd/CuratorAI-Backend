"""
Views for search app (visual search, etc.)
"""
from rest_framework import views, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, inline_serializer
from core.serializers import UnauthorizedErrorResponse


class VisualSearchUploadView(views.APIView):
    """
    Visual search by image upload.
    Placeholder endpoint - returns not implemented message.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Visual search by image upload",
        description="Search for similar outfits by uploading an image. Currently not implemented.",
        tags=["Search"],
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'image': {'type': 'string', 'format': 'binary'},
                }
            }
        },
        responses={
            501: inline_serializer(
                name='VisualSearchNotImplementedResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                }
            ),
            401: UnauthorizedErrorResponse,
        }
    )
    def post(self, request):
        """Handle visual search upload - placeholder."""
        return Response({
            'success': False,
            'message': 'Visual search is not yet implemented. This feature will be available soon!'
        }, status=status.HTTP_501_NOT_IMPLEMENTED)


class VisualSearchURLView(views.APIView):
    """
    Visual search by image URL.
    Placeholder endpoint - returns not implemented message.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Visual search by image URL",
        description="Search for similar outfits by providing an image URL. Currently not implemented.",
        tags=["Search"],
        request=inline_serializer(
            name='VisualSearchURLRequest',
            fields={
                'image_url': serializers.URLField(),
            }
        ),
        responses={
            501: inline_serializer(
                name='VisualSearchNotImplementedResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                }
            ),
            401: UnauthorizedErrorResponse,
        }
    )
    def post(self, request):
        """Handle visual search by URL - placeholder."""
        return Response({
            'success': False,
            'message': 'Visual search is not yet implemented. This feature will be available soon!'
        }, status=status.HTTP_501_NOT_IMPLEMENTED)

