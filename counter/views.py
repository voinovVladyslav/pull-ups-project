from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from utils.pagination import StandartResultPagination
from bars.models import Bars
from .models import PullUpCounter
from .serializers import PullUpCounterSerializer


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
class PullUpCounterViewSet(ModelViewSet):
    queryset = PullUpCounter.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = StandartResultPagination
    serializer_class = PullUpCounterSerializer

    def get_queryset(self):
        return PullUpCounter.objects.filter(
            bar=self.kwargs['bar_pk'], user=self.request.user
        ).order_by('-id')

    def perform_create(self, serializer):
        bar = Bars.objects.filter(id=self.kwargs['bar_pk']).first()
        if not bar:
            raise ValidationError({'bar_id': 'bars does not exists'})
        serializer.save(user=self.request.user, bar=bar)
