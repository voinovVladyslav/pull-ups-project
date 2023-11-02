import logging

from django.utils import timezone

from achievements.models import Achievement, AchievementType
from notifications.models import Notification
from notifications.helpers import get_message_for_achievement
from user.models import User
from .query import get_total_bars


logger = logging.getLogger('db')

ACHIEVEMENT_TYPE = 'totaldiff'


def check_totaldiff_achievements(user: User) -> None:
    achievement_type = AchievementType.objects.filter(
        name=ACHIEVEMENT_TYPE
    ).first()
    if not achievement_type:
        logger.warning(
            'Trying to check achievement with non-existing type: %s',
            ACHIEVEMENT_TYPE,
            extra=dict(
                type='achievement_check',
                user=user,
            )
        )
        return

    achievements = Achievement.objects.filter(
        user=user, done=False, type=achievement_type
    ).order_by(
        'threshold'
    )
    total_diff_bars = get_total_bars(user)
    for achievement in achievements:
        if achievement.threshold > total_diff_bars:
            break

        achievement.achieved_at = timezone.now()
        achievement.done = True
        achievement.save()
        Notification.objects.create(
            message=get_message_for_achievement(achievement),
            user=user,
        )
        logger.info(
            'User %s got achievement: %s',
            user.email, achievement.title,
            extra=dict(
                type='achievement_check',
                user=user,
            )
        )
