import logging
from decimal import Decimal

from django.forms.models import model_to_dict
from django.db.models import OuterRef, Exists
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from core.pagination import StandartResultPagination
from core.permissions import ReadOnly
from user.models import User
from .models import PullUpBars
from .serializers import BarsSerializer


logger = logging.getLogger('db')


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
    queryset = PullUpBars.objects.all()
    serializer_class = BarsSerializer
    pagination_class = StandartResultPagination
    permission_classes = [IsAdminUser | ReadOnly]

    def get_queryset(self):
        queryset = self.queryset

        if self.request.user.is_authenticated:
            queryset = queryset.annotate(
                is_favorite=Exists(
                    User.favorite_pullupbars.through.objects.filter(
                        user_id=self.request.user.id,
                        pullupbars_id=OuterRef('pk'),
                    )
                )
            )

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

    def perform_destroy(self, instance):
        instance.delete()
        logger.info(
            'Deleted bars: %s',
            model_to_dict(instance),
            extra=dict(type='bars_delete', user=self.request.user)
        )

    def perform_update(self, serializer):
        bars = serializer.save()
        logger.info(
            'Updated bars: %s',
            model_to_dict(bars),
            extra=dict(
                type='bars_update', pullupbar=bars, user=self.request.user
            )
        )

    @action(
        methods=['GET'], detail=False,
        url_name='favorites', url_path='favorites',
        permission_classes=[IsAuthenticated]
    )
    def list_favorites(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(user__id=request.user.id)
        serializer = self.get_serializer(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=['POST'], detail=False,
        url_name='favorites-add', url_path='favorites/add',
        permission_classes=[IsAuthenticated]
    )
    def favorite_add(self, request, *args, **kwargs):
        bar_id = request.data.get('bar_id', None)
        if not bar_id:
            raise ValidationError({'bar_id': 'this field is required'})
        try:
            bar = PullUpBars.objects.get(id=bar_id)
            request.user.favorite_pullupbars.add(bar)
            return Response(status=200)
        except Exception:
            raise ValidationError({'bar_id': 'Object does not exists'})

    @action(
        methods=['POST'], detail=False,
        url_name='favorites-remove', url_path='favorites/remove',
        permission_classes=[IsAuthenticated]
    )
    def favorite_remove(self, request, *args, **kwargs):
        bar_id = request.data.get('bar_id', None)
        if not bar_id:
            raise ValidationError({'bar_id': 'this field is required'})
        try:
            bar = PullUpBars.objects.get(id=bar_id)
            request.user.favorite_pullupbars.remove(bar)
            return Response(status=200)
        except Exception:
            raise ValidationError({'bar_id': 'Object does not exists'})
