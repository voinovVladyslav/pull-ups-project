from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from core.pagination import StandartResultPagination
from core.permissions import ReadOnly
from .models import PullUpBars
from .serializers import PullUpBarsSerializer


class PullUpBarsViewSet(viewsets.ModelViewSet):
    queryset = PullUpBars.objects.all().order_by('-id')
    serializer_class = PullUpBarsSerializer
    pagination_class = StandartResultPagination
    permission_classes = [IsAdminUser | ReadOnly]
