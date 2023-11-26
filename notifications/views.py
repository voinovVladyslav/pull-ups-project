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
    get=extend_schema(
        parameters=[
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

        unread_filter = self.get_unread_filter(self.request)
        if unread_filter:
            qs = qs.filter(unread=unread_filter)

        return qs.order_by('-created_at')

    def paginate_queryset(self, queryset):
        if self.get_unread_filter(self.request) is not None:
            return None
        return super().paginate_queryset(queryset)

    @staticmethod
    def get_unread_filter(request):
        result = request.query_params.get('unread', None)

        if not result:
            return None

        if result in ['True', 'False']:
            return result

        return None


class MarkAsReadNotificationApiView(APIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        result = Notification.objects.filter(
            user=self.request.user, unread=True
        ).update(
            unread=False
        )
        return Response(
            {'marked_as_read': result}, status=status.HTTP_200_OK
        )
