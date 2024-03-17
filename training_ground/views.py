from decimal import Decimal

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
)

from core.pagination import StandartResultPagination
from core.permissions import ReadOnly
from .models import TrainingGround
from .serializers import TrainingGroundSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='ref_point',
                type=str,
                description='Coordinates in format "longitude;latitude"',
            ),
        ]
    )
)
class TrainingGroundViewSet(viewsets.ModelViewSet):
    queryset = TrainingGround.objects.all()
    serializer_class = TrainingGroundSerializer
    pagination_class = StandartResultPagination
    permission_classes = [IsAdminUser | ReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-id')
        if self.request.user.is_authenticated:
            qs = self.annotate_favorites(qs)
        return qs

    @staticmethod
    def annotate_favorites(qs):
        return qs

    def apply_query_params(self, qs, params: dict):
        ref_point = self.get_ref_point(params.get('ref_point'))
        if ref_point:
            qs = qs.annotate(
                distance=Distance('location', ref_point)
            ).order_by(
                'distance'
            )
        return qs

    @staticmethod
    def get_ref_point(value: str) -> Point | None:
        try:
            longitude, latitude = value.split(';')
            return Point((Decimal(longitude), Decimal(latitude)), srid=4326)
        except Exception:
            return

    @action(
        methods=['POST'],
        detail=True,
        url_name='favorites-add',
        url_path='favorites/add',
        permission_classes=[IsAuthenticated],
        serializer_class=None,
    )
    def favorite_add(self, request, pk=None, *args, **kwargs):
        tg = self.get_object()
        request.user.favorite_training_grounds.add(tg)
        return Response(
            {'message': 'Successfully added to favorites'}, status=200
        )

    @action(
        methods=['POST'],
        detail=True,
        url_name='favorites-remove',
        url_path='favorites/remove',
        permission_classes=[IsAuthenticated],
        serializer_class=None,
    )
    def favorite_remove(self, request, pk=None, *args, **kwargs):
        tg = self.get_object()
        request.user.favorite_training_grounds.remove(tg)
        return Response(
            {'message': 'Successfully removed from favorites'}, status=200
        )