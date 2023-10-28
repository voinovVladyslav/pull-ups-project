from django.contrib import admin
from admin_auto_filters.filters import AutocompleteFilter

from core.filters import UserFilter
from .models import PullUpCounter


class BarFilter(AutocompleteFilter):
    title = 'Pull Up Bar'
    field_name = 'bar'


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
