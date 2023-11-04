import pytest
from model_bakery.baker import make

from tests.user.fixtures import create_user, user_email, user_password

from achievements.models import (
    AchievementType, AchievementImage, Achievement
)
from achievements.constants import ACHIEVEMENTS
from achievements.helpers.upsert import upsert_achievements


def test_link_image_if_found_by_type_and_threshold(db, create_user):
    achievement_raw = ACHIEVEMENTS[0]
    achievement_type = AchievementType.objects.create(
        name=achievement_raw['type']
    )
    image = make(
        AchievementImage,
        type=achievement_type,
        threshold=achievement_raw['threshold'],
    )
    user = create_user()
    upsert_achievements(user)
    achievement: Achievement = user.achievements.filter(
        type=achievement_type, threshold=achievement_raw['threshold']
    ).first()
    assert achievement.image == image
