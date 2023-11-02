from django.urls import path

from .views import NotificationApiView, MarkAsReadNotificationApiView


app_name = 'notifications'


urlpatterns = [
    path(
        'notifications',
        NotificationApiView.as_view(),
        name='notifications-list',
    ),
    path(
        'notifications/mark-read/',
        MarkAsReadNotificationApiView.as_view(),
        name='mark-read'
    )
]
