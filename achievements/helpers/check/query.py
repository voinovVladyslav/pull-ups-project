from django.utils import timezone
from django.db.models import Sum

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
