from django.contrib import admin
from core.filters import UserFilter

from .models import Achievement, AchievementType


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
        'type',
    )

    list_filter = (
        'done',
        'type',
        UserFilter,
    )

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(AchievementType)
class AchievementTypeModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
