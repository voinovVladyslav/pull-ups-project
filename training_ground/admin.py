from django.contrib import admin

from .models import TrainingGround


@admin.register(TrainingGround)
class TrainingGroundAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'location',
        'pullupbar',
        'dipstation',
    )
    search_fields = (
        'id',
    )
    raw_id_fields = (
        'pullupbar',
        'dipstation',
    )
