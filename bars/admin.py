from django.contrib import admin

from .models import Address, Bars


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'country',
        'city',
        'street',
        'number',
        'postal_code'
    )
    search_fields = (
        'coutry',
        'city',
        'street',
        'postal_code',
    )


@admin.register(Bars)
class BarsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'location',
        'address',
    )
    search_fields = (
        'id',
        'title',
    )
