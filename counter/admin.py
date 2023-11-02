from django.contrib import admin

from core.filters import UserFilter, BarFilter
from .models import PullUpCounter


@admin.register(PullUpCounter)
class PullUpCounterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'reps',
        'user',
        'bar',
        'created_at',
    )

    list_filter = (
        UserFilter,
        BarFilter,
    )
