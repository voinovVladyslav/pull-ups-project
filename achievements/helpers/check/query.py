from datetime import timedelta

from django.utils import timezone
from django.db.models import Sum, Max

from counter.models import PullUpCounter
from user.models import User


def get_total_pullups(user: User) -> int:
    return PullUpCounter.objects.filter(
        user=user
    ).aggregate(
        total_reps=Sum('reps')
    )['total_reps']


def get_total_bars(user: User) -> int:
    return PullUpCounter.objects.filter(
        user=user,
        reps__gte=1,
    ).distinct(
        'bar'
    ).count()


def get_total_different_bars_used_today(user: User) -> int:
    today = timezone.now()
    start = today.replace(hour=0, minute=0, second=0, microsecond=0)

    return PullUpCounter.objects.filter(
        user=user, reps__gte=1, created_at__gte=start
    ).distinct(
        'bar'
    ).count()


def get_current_pullup_streak(user: User) -> int:
    pullups = PullUpCounter.objects.filter(
        user=user, reps__gte=1
    ).order_by('-created_at')

    result = 1
    current = pullups[0].created_at
    day_before = current - timedelta(days=1)

    for pullup in pullups:
        if pullup.created_at.date() == current.date():
            continue

        if pullup.created_at.date() == day_before.date():
            result += 1
            current = day_before
            day_before = current - timedelta(days=1)
            continue
        break

    return result


def get_max_pullups(user: User) -> int:
    return PullUpCounter.objects.filter(user=user).aggregate(
        Max('reps')
    )['reps__max']
