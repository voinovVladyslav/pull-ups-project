import logging

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .serializers import AchievementSerializer
from .models import Achievement


logger = logging.getLogger('db')


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
        ).order_by('type', 'threshold')

    @action(
        methods=['POST'], detail=True,
        url_name='reset-single', url_path='reset-single'
    )
    def reset_achievement(self, request, pk=None):
        achievement = Achievement.objects.get(pk=pk)
        achievement.done = False
        achievement.save()
        logger.info(
            'user %s reset achievement %s',
            self.request.user.email, achievement.title,
            extra=dict(
                type='achievement_reset',
                user=self.request.user,
            )
        )
        return Response()

    @action(
        methods=['POST'], detail=False,
        url_name='reset-all', url_path='reset-all'
    )
    def reset_achievements(self, request):
        self.request.user.achievements.update(done=False)
        logger.info(
            'user %s reset all achievements',
            self.request.user.email,
            extra=dict(
                type='achievement_reset',
                user=self.request.user,
            )
        )
        return Response()
