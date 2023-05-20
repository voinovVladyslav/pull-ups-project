from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from utils.pagination import StandartResultPagination
from utils.permissions import ReadOnly
from .models import Bars
from .serializers import BarsSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'page',
                OpenApiTypes.INT,
                description='Page number',
            ),
        ]
    )
)
class BarsViewSet(viewsets.ModelViewSet):
    queryset = Bars.objects.all()
    serializer_class = BarsSerializer
    pagination_class = StandartResultPagination
    permission_classes = [IsAdminUser | ReadOnly]

    def get_queryset(self):
        return self.queryset.order_by('-id')
