from django.contrib import admin

from .models import DipStations


@admin.register(DipStations)
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
