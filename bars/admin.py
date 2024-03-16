from django.contrib import admin

from .models import Bars


@admin.register(Bars)
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
