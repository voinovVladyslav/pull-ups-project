from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from user.models import User
from achievements.helpers.check import check_user_achievements
from achievements.helpers.upsert import upsert_achievements


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'is_staff', 'last_login', 'created_at']
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'email',
                    'password',
                    'favorite_training_grounds',
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'last_login',
                    'created_at',
                )
            }
        ),
    )
    readonly_fields = ['last_login', 'created_at']
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'created_at',
                )
            }
        ),
    )
    actions = (
        'upsert_achievements',
        'check_achievements',
    )

    def upsert_achievements(self, request, queryset):
        for user in queryset:
            upsert_achievements(user)
        self.message_user(
            request,
            f'Successfully upsert achievements for {queryset.count()} users',
            level=messages.SUCCESS,
        )

    def check_achievements(self, request, queryset):
        for user in queryset:
            check_user_achievements(user)
        self.message_user(
            request,
            f'Successfully checked achievements for {queryset.count()} users',
            level=messages.SUCCESS,
        )
