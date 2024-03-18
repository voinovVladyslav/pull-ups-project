from django.contrib import admin

from .models import PullUpBars


@admin.register(PullUpBars)
class BarsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'training_ground',
    )
    search_fields = (
        'id',
        'title',
    )
    readonly_fields = (
        'id',
    )
