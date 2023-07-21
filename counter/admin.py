from django.contrib import admin
from .models import PullUpCounter

from admin_auto_filters.filters import AutocompleteFilter


class UserFilter(AutocompleteFilter):
    title = 'User'
    field_name = 'user'


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
