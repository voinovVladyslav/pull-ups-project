from django.db import models


class DipStations(models.Model):
    class Meta:
        verbose_name = 'Dip Station'
        verbose_name_plural = 'Dip Stations'

    title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'Dip station #{self.id}'
