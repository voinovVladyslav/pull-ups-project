from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from utils.permissions import ReadOnly
from utils.pagination import StandartResultPagination
from .models import Tag
from .serializers import TagSerializer


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
class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser | ReadOnly]
    pagination_class = StandartResultPagination

    def get_queryset(self):
        return self.queryset.order_by('-id')
