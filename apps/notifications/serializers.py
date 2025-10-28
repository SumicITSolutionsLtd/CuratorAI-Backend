"""
Serializers for notifications app.
"""
from rest_framework import serializers
from apps.accounts.serializers import UserSerializer
from .models import Notification, NotificationPreference


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications."""
    actor = UserSerializer(read_only=True, fields=['id', 'username', 'avatar'])
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user_id', 'type', 'title', 'message', 'image_url', 
            'action_url', 'actor', 'is_read', 'read_at', 'created_at'
        ]
        read_only_fields = ['id', 'user_id', 'created_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for notification preferences."""
    
    class Meta:
        model = NotificationPreference
        exclude = ['id', 'user', 'created_at', 'updated_at']

