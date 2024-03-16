from django.contrib import admin
from django.utils.safestring import mark_safe

from core.filters import UserFilter, PullUpBarFilter
from .models import LogRecord


@admin.register(LogRecord)
class LogRecordAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'level',
        'type',
        'msg',
        'pullupbar',
        'user',
    )
    readonly_fields = (
        'created_at',
        'level',
        'type',
        'message',
        'trace',
        'pullupbar',
        'user',
    )
    list_filter = (
        'type',
        'level__name',
        UserFilter,
        PullUpBarFilter,
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
