from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TagViewSet


app_name = 'tag'

router = DefaultRouter()
router.register('tags', TagViewSet, 'tag')

urlpatterns = [
    path('', include(router.urls)),
]
