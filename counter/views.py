from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from core.pagination import StandartResultPagination
from pullupbars.models import PullUpBars
from dipstations.models import DipStations
from achievements.helpers.check import check_user_achievements
from .models import PullUpCounter, DipCounter
from .serializers import PullUpCounterSerializer, DipCounterSerializer


class PullUpCounterViewSet(ModelViewSet):
    queryset = PullUpCounter.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = StandartResultPagination
    serializer_class = PullUpCounterSerializer

    def get_queryset(self):
        return PullUpCounter.objects.filter(
            pullupbar=self.kwargs['pullupbar_pk'], user=self.request.user
        ).order_by('-id')

    def perform_create(self, serializer):
        bar = PullUpBars.objects.filter(id=self.kwargs['pullupbar_pk']).first()
        if not bar:
            raise ValidationError({'pullupbar_id': 'bars does not exists'})
        serializer.save(user=self.request.user, pullupbar=bar)
        check_user_achievements(self.request.user)


class DipCounterViewSet(ModelViewSet):
    queryset = DipCounter.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = StandartResultPagination
    serializer_class = DipCounterSerializer

    def get_queryset(self):
        return DipCounter.objects.filter(
            dipstation=self.kwargs['dipstation_pk'], user=self.request.user
        ).order_by('-id')

    def perform_create(self, serializer):
        station = DipStations.objects.filter(
            id=self.kwargs['dipstation_pk']
        ).first()
        if not station:
            raise ValidationError({
                'dipstation_id': 'stations does not exists'
            })
        serializer.save(user=self.request.user, dipstation=station)
