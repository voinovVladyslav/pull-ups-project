from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TrainingGroundViewSet


app_name = 'training_ground'

router = DefaultRouter()
router.register('training-ground', TrainingGroundViewSet, 'training-ground')


urlpatterns = [
    path('', include(router.urls)),
]
