from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from core.pagination import StandartResultPagination
from .models import Notification
from .serializers import NotificationSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'page',
                OpenApiTypes.INT,
                description='Page number',
            ),
            OpenApiParameter(
                'unread',
                OpenApiTypes.BOOL,
                description='Filter by unread status',
            ),
        ]
    )
)
class NotificationApiView(ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandartResultPagination

    def get_queryset(self):
        qs = self.queryset
        qs = qs.filter(user=self.request.user)

        unread_filter = self.request.query_params.get('unread', None)
        if unread_filter in ['True', 'False']:
            qs = qs.filter(unread=unread_filter)

        return qs.order_by('-created_at')


class MarkAsReadNotificationApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        result = Notification.objects.filter(
            user=request.user, unread=True
        ).update(
            unread=False
        )
        return Response(
            {'marked_as_read': result}, status=status.HTTP_200_OK
        )
