from django.contrib import admin

from core.filters import UserFilter
from .models import Notification


@admin.register(Notification)
class NotificationModelAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'truncated_message',
        'unread',
        'has_redirect_link',
        'user',
    )
    raw_id_fields = (
        'user',
    )
    search_fields = (
        'id',
        'redirect_to',
        'message',
    )
    list_filter = (
        'unread',
        UserFilter
    )
    ordering = ('-created_at',)

    def has_redirect_link(self, obj) -> bool:
        return bool(obj.redirect_to)
    has_redirect_link.boolean = True

    def truncated_message(self, obj) -> str:
        return obj.message[:100]
    truncated_message.short_description = 'Message'
