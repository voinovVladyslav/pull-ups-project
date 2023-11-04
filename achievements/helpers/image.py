from achievements.models import Achievement, AchievementImage


def link_image(achievement: Achievement) -> bool:
    try:
        image = AchievementImage.objects.get(
            threshold=achievement.threshold,
            type=achievement.type,
        )
        achievement.image = image
        achievement.save()
        return True
    except AchievementImage.DoesNotExist:
        return False
