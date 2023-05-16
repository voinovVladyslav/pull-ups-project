from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views


app_name = 'bars'

router = DefaultRouter()
router.register('bars', views.BarsViewSet, 'bars')

urlpatterns = [
    path('', include(router.urls))
]
