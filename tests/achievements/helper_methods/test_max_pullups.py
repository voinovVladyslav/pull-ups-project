import pytest

from model_bakery.baker import make

from bars.models import Bars
from counter.models import PullUpCounter

from achievements.helpers.check.query import get_max_pullups


@pytest.mark.parametrize(
    'reps',
    [
        (0),
        (21),
        (31),
        (44),
        (102),
    ],
)
def test_getting_max_pullups(db, create_user, reps):
    user = create_user()
    bar = make(Bars)
    make(PullUpCounter, user=user, bar=bar, reps=reps)
    assert get_max_pullups(user) == reps


def test_using_max_pullups_on_user_without_pullups_return_0(db, create_user):
    user = create_user()
    assert get_max_pullups(user) == 0
