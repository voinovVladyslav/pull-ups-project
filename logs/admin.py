from django.contrib import admin
from django.utils.safestring import mark_safe
from admin_auto_filters.filters import AutocompleteFilter

from .models import LogRecord


class UserFilter(AutocompleteFilter):
    title = 'User'
    field_name = 'user'


@admin.register(LogRecord)
class LogRecordAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'level',
        'type',
        'msg',
        'bar',
        'user',
    )
    readonly_fields = (
        'created_at',
        'level',
        'type',
        'message',
        'trace',
        'bar',
        'user',
    )
    list_filter = (
        'type',
        'level__name',
        UserFilter,
    )
    search_fields = (
        'message',
    )
    ordering = (
        '-created_at',
    )
    date_hierarchy = "created_at"

    def msg(self, obj) -> str:
        message = obj.message[:100]
        return mark_safe(
            message.replace("\n", "<br>\n")
        )
