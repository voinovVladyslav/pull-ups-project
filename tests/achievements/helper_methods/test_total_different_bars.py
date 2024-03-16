import pytest

from model_bakery.baker import make

from pullupbars.models import PullUpBars
from counter.models import PullUpCounter

from achievements.helpers.check.query import get_total_bars


@pytest.mark.parametrize(
    'different_bars',
    [
        (3),
        (5),
        (25),
        (40),
        (50),
        (100),
        (130),
    ],
)
def test_many_different_bars(db, create_user, different_bars):
    user = create_user()
    bars = make(PullUpBars, different_bars)
    for bar in bars:
        make(PullUpCounter, reps=5, pullupbar=bar, user=user)
    assert get_total_bars(user) == different_bars


def test_no_pullups_return_0(db, create_user):
    user = create_user()
    assert get_total_bars(user) == 0


def test_0_reps_not_included(db, create_user):
    user = create_user()
    bars = make(PullUpBars, 5)
    for bar in bars:
        make(PullUpCounter, reps=0, pullupbar=bar, user=user)

    assert get_total_bars(user) == 0
