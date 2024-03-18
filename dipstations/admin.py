from django.contrib import admin

from .models import DipStation


@admin.register(DipStation)
class DipStationAdmin(admin.ModelAdmin):
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
