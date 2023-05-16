from rest_framework import viewsets
from .models import Bars
from .serializers import BarsSerializer


class BarsViewSet(viewsets.ModelViewSet):
    queryset = Bars.objects.all()
    serializer_class = BarsSerializer
