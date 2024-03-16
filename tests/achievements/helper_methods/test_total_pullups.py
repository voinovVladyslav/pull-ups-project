import pytest

from model_bakery.baker import make

from pullupbars.models import PullUpBars
from counter.models import PullUpCounter

from achievements.helpers.check.query import get_total_pullups


@pytest.mark.parametrize(
    'reps_total',
    [
        (50),
        (4999),
        (8999),
        (17000),
    ],
)
def test_different_total_values(db, create_user, reps_total):
    user = create_user()
    bar = make(PullUpBars)
    make(PullUpCounter, reps=reps_total, pullupbar=bar, user=user)

    assert get_total_pullups(user) == reps_total


def test_user_without_pullups_return_0(db, create_user):
    user = create_user()
    assert get_total_pullups(user) == 0
