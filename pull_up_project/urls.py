from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("admin/", admin.site.urls),

    # api documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    ),

    # api
    path('api/', include('user.urls')),
    path('api/', include('pullupbars.urls')),
    path('api/', include('dipstations.urls')),
    path('api/', include('achievements.urls')),
    path('api/', include('notifications.urls')),
    path('api/', include('training_ground.urls')),
]
