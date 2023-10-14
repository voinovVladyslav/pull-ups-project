import logging

from django.utils import timezone

from achievements.models import Achievement, AchievementType
from counter.models import PullUpCounter
from user.models import User


logger = logging.getLogger('db')

ACHIEVEMENT_TYPE = 'diff'


def check_diff_achievements(user: User) -> None:
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

    today = timezone.now()
    start = today.replace(hour=0, minute=0, second=0, microsecond=0)

    achievements = Achievement.objects.filter(
        user=user, done=False, type=achievement_type
    ).order_by(
        'threshold'
    )

    diff_bars = PullUpCounter.objects.filter(
        user=user, reps__gte=1, created_at__gte=start
    ).distinct(
        'bar'
    ).count()

    for achievement in achievements:
        if achievement.threshold > diff_bars:
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
