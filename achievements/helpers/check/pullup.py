import logging

from django.db.models import Max
from django.utils import timezone

from achievements.models import Achievement, AchievementType
from counter.models import PullUpCounter
from user.models import User


logger = logging.getLogger('db')

ACHIEVEMENT_TYPE = 'pullup'


def check_pullup_achievements(user: User) -> None:
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
    max_pullups = PullUpCounter.objects.filter(user=user).aggregate(
        Max('reps')
    )['reps__max']
    for achievement in achievements:
        if achievement.threshold > max_pullups:
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
