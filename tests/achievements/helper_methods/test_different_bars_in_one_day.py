from datetime import datetime

import pytest

from django.utils.timezone import make_aware
from model_bakery.baker import make

from bars.models import Bars
from counter.models import PullUpCounter

from achievements.helpers.check.query import (
    get_total_different_bars_used_today,
)


@pytest.mark.parametrize(
    'diff_bars',
    [
        (2),
        (6),
        (11),
    ],
)
def test_different_bars_in_one_day_helper(db, diff_bars, create_user):
    user = create_user()
    bars = make(Bars, diff_bars)
    for bar in bars:
        make(PullUpCounter, reps=5, bar=bar, user=user)

    res = get_total_different_bars_used_today(user)
    assert diff_bars == res


def test_count_only_pullups_from_same_day(db, create_user):
    user = create_user()
    bars = make(Bars, 4)
    dates = [
        make_aware(datetime(2023, 9, 11)),
        make_aware(datetime(2023, 9, 12)),
        make_aware(datetime(2023, 9, 13)),
        make_aware(datetime.now()),
    ]
    for bar, date in zip(bars, dates):
        counter = make(PullUpCounter, reps=10, bar=bar, user=user)
        counter.created_at = date
        counter.save()

    res = get_total_different_bars_used_today(user)
    assert res == 1
