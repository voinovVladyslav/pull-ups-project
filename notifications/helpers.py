from achievements.models import Achievement
from .models import Notification


def get_message_for_achievement(achievement: Achievement) -> str:
    return f'You just got achievement "{achievement.title}"'


def create_achievement_notification(user, achievement: Achievement) -> Notification:
    return Notification.objects.create(
        user=user,
        message=get_message_for_achievement(achievement),
        redirect_to='/achievements'
    )
