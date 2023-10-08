import logging

from user.models import User
from achievements.models import Achievement, AchievementType
from achievements.constants import ACHIEVEMENTS


logger = logging.getLogger('db')


def upsert_achievements(user: User, achievements: list = None):
    if not achievements:
        achievements = ACHIEVEMENTS
    checked_ids = []
    for achievement in achievements:
        achievement_type, created = AchievementType.objects.get_or_create(
            name=achievement['type']
        )
        obj, created = Achievement.objects.get_or_create(
            title=achievement['title'],
            description=achievement['description'],
            threshold=achievement['threshold'],
            type=achievement_type,
            user=user,
        )
        if created:
            logger.info(
                'Created achievement %s',
                achievement['title'],
                extra=dict(
                    type='achievements',
                    user=user,
                )
            )
        checked_ids.append(obj.id)

    excess_achievements = Achievement.objects.filter(
        user=user
    ).exclude(
        id__in=checked_ids
    )
    if excess_achievements:
        logger.info(
            'Deleting %s extra achievements',
            excess_achievements.count(),
            extra=dict(
                type='achievements',
                user=user,
            )
        )
        excess_achievements.delete()
