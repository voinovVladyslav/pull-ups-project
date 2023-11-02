from achievements.models import Achievement


def get_message_for_achievement(achievement: Achievement) -> str:
    return f'You just got achievement "{achievement.title}"'
