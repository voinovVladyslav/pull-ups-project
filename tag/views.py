import logging
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from core.permissions import ReadOnly
from core.pagination import StandartResultPagination
from .models import Tag
from .serializers import TagSerializer


logger = logging.getLogger('db')


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

    def create(self, request, *args, **kwargs):
        logger.info(
            'Create tag',
            extra=dict(type='tags_create', user=request.user)
        )
        return super().create(request, *args, **kwargs)

    def destroy(self, request, pk=None, *args, **kwargs):
        logger.info(
            'Deleted tag: id=%s',
            pk,
            extra=dict(type='tags_delete', user=request.user)
        )
        return super().destroy(request, *args, **kwargs)
