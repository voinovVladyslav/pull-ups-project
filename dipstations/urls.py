from rest_framework_nested import routers
from django.urls import path, include

from dipstations.views import DipStationViewSet
from .views import DipStationViewSet


app_name = 'dipstations'

router = routers.DefaultRouter()
router.register('dipstations', DipStationViewSet, 'dipstations')

dipstation_counter_router = routers.NestedSimpleRouter(
    router, 'dipstations', lookup='dipstation'
)
dipstation_counter_router.register(
    'counter', DipStationViewSet, 'dipstations-counter',
)

urlpatterns = [
    path('', include(dipstation_counter_router.urls)),
]
