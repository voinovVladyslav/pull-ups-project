import logging
from datetime import timedelta

from django.utils import timezone

from achievements.models import Achievement, AchievementType
from counter.models import PullUpCounter
from user.models import User


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
    pullups = PullUpCounter.objects.filter(
        user=user, reps__gte=1
    ).order_by('-created_at')

    streak = 1
    current = pullups[0].created_at
    day_before = current - timedelta(days=1)

    for pullup in pullups:
        if pullup.created_at.date() == day_before.date():
            streak += 1
            current = day_before
            day_before = current - timedelta(days=1)
            continue

        if pullup.created_at.date() == current.date():
            continue
        break

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
