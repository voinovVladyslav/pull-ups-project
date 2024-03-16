from django.contrib import admin

from .models import PullUpBars


@admin.register(PullUpBars)
class BarsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'location',
    )
    search_fields = (
        'id',
        'title',
    )
