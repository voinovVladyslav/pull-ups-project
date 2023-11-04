from django.contrib import admin
from django.utils.safestring import mark_safe
from core.filters import UserFilter

from .models import Achievement, AchievementType, AchievementImage
from .helpers.image import link_image


@admin.register(Achievement)
class AchievementModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'user',
        'done',
        'has_image',
        'achieved_at',
    )

    raw_id_fields = (
        'user',
        'type',
        'image',
    )

    list_filter = (
        'done',
        'type',
        UserFilter,
    )
    actions = (
        'link_image',
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_image(self, obj):
        return obj.image is not None
    has_image.boolean = True

    def link_image(self, request, queryset):
        self.message_user(
            request,
            f'Run link_image for {queryset.count()} achievements'
        )
        for obj in queryset:
            link_image(obj)


@admin.register(AchievementType)
class AchievementTypeModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )


@admin.register(AchievementImage)
class AchievementImageModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'image_preview',
        'threshold',
        'type',
    )
    raw_id_fields = (
        'type',
    )
    search_fields = (
        'threshold',
        'type__name',
        'image_url',
    )

    def image_preview(self, obj):
        if not obj.image_url:
            return 'N/A'

        return mark_safe(
            f'<img src="{obj.image_url}" style="width: 150px"/>'
        )
