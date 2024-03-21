from django.contrib import admin

from core.filters import UserFilter, PullUpBarFilter, DipStationFilter
from .models import PullUpCounter, DipCounter


@admin.register(PullUpCounter)
class PullUpCounterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'reps',
        'user',
        'pullupbar',
        'created_at',
    )
    raw_id_fields = (
        'user',
        'pullupbar',
    )
    list_filter = (
        UserFilter,
        PullUpBarFilter,
    )

@admin.register(DipCounter)
class DipCounterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'reps',
        'user',
        'created_at',
    )
    raw_id_fields = (
        'user',
        'dipstation',
    )
    list_filter = (
        UserFilter,
        DipStationFilter,
    )
