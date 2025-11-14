"""
Serializers for notifications app.
"""
from rest_framework import serializers
from apps.accounts.models import User
from .models import Notification, NotificationPreference


class ActorSerializer(serializers.ModelSerializer):
    """Minimal serializer for actor in notifications."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar']
        read_only_fields = ['id', 'username', 'avatar']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications."""
    actor = ActorSerializer(read_only=True)
    
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

