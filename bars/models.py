from django.db import models
from django.contrib.gis.db.models import PointField


class Bars(models.Model):
    class Meta:
        verbose_name = 'Pull Up Bars'
        verbose_name_plural = 'Pull Up Bars'

    title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    # x - longitude y - latitude
    location = PointField(
        null=True, blank=True, srid=4326, serialize=True, geography=True
    )
    tags = models.ManyToManyField('tag.Tag', blank=True)

    def __str__(self):
        return f'Pull bar #{self.id}'
