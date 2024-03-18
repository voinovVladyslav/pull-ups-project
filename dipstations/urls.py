from rest_framework_nested import routers
from django.urls import path, include

from .views import DipStationViewSet


app_name = 'dipstations'

router = routers.DefaultRouter()
router.register('dipstations', DipStationViewSet, 'dipstations')

urlpatterns = [
    path('', include(router.urls)),
]
