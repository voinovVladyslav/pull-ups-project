from django.contrib import admin
from admin_auto_filters.filters import AutocompleteFilter

from .models import Achievement


class UserFilter(AutocompleteFilter):
    field_name = 'user'
    title = 'User'


@admin.register(Achievement)
class AchievementModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'user',
        'done',
        'achieved_at',
    )

    raw_id_fields = (
        'user',
    )

    list_filter = (
        'done',
        UserFilter,
    )
