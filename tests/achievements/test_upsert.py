from achievements.constants import ACHIEVEMENTS
from achievements.helpers.upsert import upsert_achievements


def test_upsert_fill_all_achiements(db, create_user):
    user = create_user()
    assert user.achievements.count() == 0
    upsert_achievements(user)
    assert user.achievements.count() == len(ACHIEVEMENTS)


def test_upsert_remove_excess_achievements(db, create_user):
    user = create_user()
    upsert_achievements(user)
    assert user.achievements.count() == len(ACHIEVEMENTS)
    achievements = ACHIEVEMENTS[:5]
    upsert_achievements(user, achievements)
    assert user.achievements.count() == len(achievements)


def test_upsert_create_not_done_achievements(db, create_user):
    user = create_user()
    upsert_achievements(user)
    for achievement in user.achievements.iterator():
        assert achievement.done is False
