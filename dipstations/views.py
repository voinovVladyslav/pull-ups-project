from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from core.pagination import StandartResultPagination
from core.permissions import ReadOnly
from .models import DipStation
from .serializers import DipStationSerializer


class DipStationViewSet(ModelViewSet):
    queryset = DipStation.objects.all()
    serializer_class = DipStationSerializer
    pagination_class = StandartResultPagination
    permission_classes = [IsAdminUser | ReadOnly]
