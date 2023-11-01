from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.pagination import StandartResultPagination
from .models import Notification
from .serializers import NotificationSerializer


class NotificationApiView(ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandartResultPagination

    def get_queryset(self):
        qs = self.queryset
        return qs.filter(user=self.request.user).order_by('-created_at')

    def mark_read(self, request):
        qs = self.get_queryset()
        qs.update(unread=False)
        return Response(status=200)


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
