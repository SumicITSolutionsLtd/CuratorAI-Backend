"""
URL patterns for notifications app.
"""
from django.urls import path
from .views import (
    NotificationListView,
    UnreadCountView,
    MarkNotificationReadView,
    MarkAllReadView,
    DeleteNotificationView,
    NotificationPreferencesView,
)

app_name = 'notifications'

urlpatterns = [
    # Notifications
    path('<int:user_id>/', NotificationListView.as_view(), name='notification-list'),
    path('<int:user_id>/unread-count/', UnreadCountView.as_view(), name='unread-count'),
    path('<int:notification_id>/read/', MarkNotificationReadView.as_view(), name='mark-read'),
    path('<int:user_id>/read-all/', MarkAllReadView.as_view(), name='mark-all-read'),
    path('<int:pk>/delete/', DeleteNotificationView.as_view(), name='delete-notification'),
    
    # Preferences
    path('<int:user_id>/preferences/', NotificationPreferencesView.as_view(), name='preferences'),
]

