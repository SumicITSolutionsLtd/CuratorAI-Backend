"""
Views for notifications app.
"""
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Notification, NotificationPreference
from .serializers import NotificationSerializer, NotificationPreferenceSerializer


class NotificationListView(generics.ListAPIView):
    """
    List user notifications with filtering.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get notifications",
        description="List user notifications with optional filtering",
        tags=["Notifications"],
        parameters=[
            OpenApiParameter(name='type', description='Filter by notification type', required=False, type=str),
            OpenApiParameter(name='is_read', description='Filter by read status', required=False, type=bool),
        ]
    )
    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user)
        
        # Apply filters
        notification_type = self.request.query_params.get('type')
        if notification_type:
            queryset = queryset.filter(type=notification_type)
        
        is_read = self.request.query_params.get('is_read')
        if is_read is not None:
            is_read_bool = is_read.lower() == 'true'
            queryset = queryset.filter(is_read=is_read_bool)
        
        return queryset


class UnreadCountView(views.APIView):
    """
    Get unread notification count.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get unread count",
        description="Get count of unread notifications by type",
        tags=["Notifications"]
    )
    def get(self, request, user_id):
        # Ensure user can only get their own unread count
        if request.user.id != user_id:
            return Response({
                'success': False,
                'message': 'Unauthorized'
            }, status=status.HTTP_403_FORBIDDEN)
        
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        total_count = notifications.count()
        
        # Count by type
        by_type = {}
        for notification_type, _ in Notification.TYPE_CHOICES:
            count = notifications.filter(type=notification_type).count()
            if count > 0:
                by_type[notification_type] = count
        
        return Response({
            'count': total_count,
            'by_type': by_type
        }, status=status.HTTP_200_OK)


class MarkNotificationReadView(views.APIView):
    """
    Mark a notification as read.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Mark notification as read",
        description="Mark a single notification as read",
        tags=["Notifications"]
    )
    def patch(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
        except Notification.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Notification not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        
        return Response({
            'id': str(notification.id),
            'is_read': True,
            'read_at': notification.read_at
        }, status=status.HTTP_200_OK)


class MarkAllReadView(views.APIView):
    """
    Mark all notifications as read.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Mark all as read",
        description="Mark all user notifications as read",
        tags=["Notifications"]
    )
    def patch(self, request, user_id):
        # Ensure user can only mark their own notifications
        if request.user.id != user_id:
            return Response({
                'success': False,
                'message': 'Unauthorized'
            }, status=status.HTTP_403_FORBIDDEN)
        
        count = Notification.objects.filter(user=request.user, is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return Response({
            'message': 'All notifications marked as read',
            'count': count
        }, status=status.HTTP_200_OK)


class DeleteNotificationView(generics.DestroyAPIView):
    """
    Delete a notification.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Delete notification",
        description="Delete a notification",
        tags=["Notifications"]
    )
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationPreferencesView(generics.RetrieveUpdateAPIView):
    """
    Get or update notification preferences.
    """
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get notification preferences",
        description="Get user's notification preferences",
        tags=["Notifications"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="Update notification preferences",
        description="Update user's notification preferences",
        tags=["Notifications"]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    def get_object(self):
        user_id = self.kwargs.get('user_id')
        
        # Ensure user can only access their own preferences
        if self.request.user.id != user_id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('You can only access your own preferences')
        
        # Get or create preferences
        preferences, _ = NotificationPreference.objects.get_or_create(user=self.request.user)
        return preferences

