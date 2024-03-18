from rest_framework_nested import routers
from django.urls import path, include

from counter.views import PullUpCounterViewSet
from . import views


app_name = 'pullupbars'

router = routers.DefaultRouter()
router.register('pullupbars', views.PullUpBarsViewSet, 'pullupbars')

pullupbars_counter_router = routers.NestedSimpleRouter(
    router, 'pullupbars', lookup='pullupbar'
)
pullupbars_counter_router.register(
    'counter', PullUpCounterViewSet, 'pullupbars-counter'
)

urlpatterns = [
    path('', include(pullupbars_counter_router.urls)),
]
