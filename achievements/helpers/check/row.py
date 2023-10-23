import logging

from django.utils import timezone

from achievements.models import Achievement, AchievementType
from user.models import User

from .query import get_current_pullup_streak


logger = logging.getLogger('db')

ACHIEVEMENT_TYPE = 'row'


def check_row_achievements(user: User) -> None:
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
    streak = get_current_pullup_streak(user)

    for achievement in achievements:
        if achievement.threshold > streak:
            break

        achievement.achieved_at = timezone.now()
        achievement.done = True
        achievement.save()
        logger.info(
            'User %s got achievement: %s',
            user.email, achievement.title,
            extra=dict(
                type='achievement_check',
                user=user,
            )
        )
