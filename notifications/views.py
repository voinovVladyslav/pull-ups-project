from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from utils.pagination import StandartResultPagination

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated,]
    pagination_class = StandartResultPagination
