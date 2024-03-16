from django.contrib import admin

from core.filters import UserFilter, PullUpBarFilter
from .models import PullUpCounter


@admin.register(PullUpCounter)
class PullUpCounterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'reps',
        'user',
        'pullupbar',
        'created_at',
    )

    list_filter = (
        UserFilter,
        PullUpBarFilter,
    )
