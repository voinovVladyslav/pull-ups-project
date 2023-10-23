from django.urls import path

from user import views


app_name = 'user'


urlpatterns = [
    path('user/create/', views.CreateUserView.as_view(), name='create'),
    path('user/token/', views.AuthTokenView.as_view(), name='token'),
    path('user/me/', views.UpdateUserView.as_view(), name='me'),
    path(
        'user/statistics/',
        views.UserStatisticsView.as_view(),
        name='stats',
    ),
]
