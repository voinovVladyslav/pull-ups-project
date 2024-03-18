from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from core.pagination import StandartResultPagination
from core.permissions import ReadOnly
from .models import DipStations
from .serializers import DipStationSerializer


class DipStationViewSet(ModelViewSet):
    queryset = DipStations.objects.all().order_by('-id')
    serializer_class = DipStationSerializer
    pagination_class = StandartResultPagination
    permission_classes = [IsAdminUser | ReadOnly]
