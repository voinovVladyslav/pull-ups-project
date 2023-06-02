from decimal import Decimal

from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
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


def get_ref_point_from_query_data(value: str) -> Point | None:
    try:
        longitude, latitude = value.split(';')
        return Point((Decimal(longitude), Decimal(latitude)), srid=4326)
    except Exception:
        return


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'page',
                OpenApiTypes.INT,
                description='Page number',
            ),
            OpenApiParameter(
                'ref_point',
                OpenApiTypes.STR,
                description='Coordinates in format "longitude;latitude"',
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
        queryset = self.queryset
        ref_point_raw = self.request.query_params.get('ref_point')
        if ref_point_raw:
            ref_point = get_ref_point_from_query_data(ref_point_raw)
            if ref_point:
                return queryset.annotate(
                    distance=Distance("location", ref_point)
                ).order_by(
                    "distance"
                )
        return queryset.order_by('-id')
