from django.utils import timezone
from django.db.models import Sum

from counter.models import PullUpCounter
from user.models import User


def get_total_pullups(user: User):
    return PullUpCounter.objects.filter(
        user=user
    ).aggregate(
        total_reps=Sum('reps')
    )['total_reps']
