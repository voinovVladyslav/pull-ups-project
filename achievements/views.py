from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .serializers import AchievementSerializer
from .models import Achievement


class AchievementViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user,
        )

    @action(
        methods=['POST'], detail=True,
        url_name='reset-single', url_path='reset'
    )
    def reset_achievement(self, request, pk=None):
        achievement = Achievement.objects.get(pk=pk)
        achievement.done = False
        achievement.save()
        return Response()

    @action(
        methods=['POST'], detail=False,
        url_name='reset-all', url_path='reset'
    )
    def reset_achievements(self, request):
        self.request.user.achievements.update(done=False)
        return Response()
