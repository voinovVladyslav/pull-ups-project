from datetime import timedelta

import pytest
from django.utils import timezone
from model_bakery.baker import make

from tests.user.fixtures import create_user, user_email, user_password

from user.models import User
from bars.models import Bars
from counter.models import PullUpCounter

from achievements.helpers.check.query import get_current_pullup_streak


def test_current_streak_for_6_day_streak(db, create_user):
    user = create_user()
    bar = make(Bars)
    number_of_days = 6
    now = timezone.now()
    starting_point = now - timedelta(days=number_of_days)

    for _ in range(number_of_days):
        counter = make(PullUpCounter, bar=bar, user=user, reps=10)
        counter.created_at = starting_point
        counter.save()
        starting_point = starting_point + timedelta(days=1)

    assert number_of_days == get_current_pullup_streak(user)


def test_current_streak_return_0_when_no_pullups(db, create_user):
    user = create_user()
    assert get_current_pullup_streak(user) == 0


def test_count_only_pullups_with_1_rep_and_more(db, create_user):
    user = create_user()
    bar = make(Bars)
    number_of_days = 6
    now = timezone.now()
    starting_point = now - timedelta(days=number_of_days)

    for _ in range(number_of_days):
        counter = make(PullUpCounter, bar=bar, user=user, reps=0)
        counter.created_at = starting_point
        counter.save()
        starting_point = starting_point + timedelta(days=1)

    assert get_current_pullup_streak(user) == 0


def test_one_day_missing_resets_streak(db, create_user):
    user = create_user()

    bar = make(Bars)
    number_of_days = 10
    now = timezone.now()
    starting_point = now - timedelta(days=number_of_days)

    for i in range(number_of_days):

        if i == 5:
            # streak at the end is 4
            starting_point = starting_point + timedelta(days=1)
            continue

        counter = make(PullUpCounter, bar=bar, user=user, reps=10)
        counter.created_at = starting_point
        counter.save()
        starting_point = starting_point + timedelta(days=1)

    assert get_current_pullup_streak(user) == 4
