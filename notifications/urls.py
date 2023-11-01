from django.urls import path

from .views import NotificationApiView


app_name = 'notifications'


urlpatterns = [
    path(
        'notifications',
        NotificationApiView.as_view(),
        name='notifications-list',
    )
]
