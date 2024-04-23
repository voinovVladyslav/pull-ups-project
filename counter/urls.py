from django.urls import path

from .views import PullUpCounterListAPIView, DipCounterListAPIView


app_name = 'counter'

urlpatterns = [
    path(
        'counter/pullup/',
        PullUpCounterListAPIView.as_view(),
        name='pullup-list',
    ),
    path(
        'counter/dip/',
        DipCounterListAPIView.as_view(),
        name='dip-list',
    ),
]
