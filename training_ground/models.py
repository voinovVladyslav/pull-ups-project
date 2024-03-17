from django.db import models
from django.contrib.gis.db.models import PointField


class TrainingGround(models.Model):
    class Meta:
        verbose_name = 'Training Ground'
        verbose_name_plural = 'Training Grounds'

    location = PointField(
        srid=4326, serialize=True, geography=True
    )
    pullupbar = models.ForeignKey(
        'pullupbars.PullUpBars',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='training_grounds'
    )

    def __str__(self) -> str:
        return f'Training Ground #{self.id}'