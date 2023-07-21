from rest_framework_nested import routers
from django.urls import path, include

from counter.views import PullUpCounterViewSet
from . import views


app_name = 'bars'

router = routers.DefaultRouter()
router.register('bars', views.BarsViewSet, 'bars')

bars_counter_router = routers.NestedSimpleRouter(router, 'bars', lookup='bar')
bars_counter_router.register('counter', PullUpCounterViewSet, 'bars-counter')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(bars_counter_router.urls)),
]
