from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

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
