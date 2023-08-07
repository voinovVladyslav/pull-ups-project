from django.db import models
from django.contrib.gis.db.models import PointField
from django.core.validators import MinValueValidator, MaxValueValidator


class Address(models.Model):
    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    country = models.CharField(
        max_length=128,
    )
    city = models.CharField(
        max_length=256,
    )
    street = models.CharField(
        max_length=256
    )
    number = models.CharField(
        max_length=32,
    )
    postal_code = models.CharField(
        max_length=32,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.street} {self.number}'


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
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    tags = models.ManyToManyField('tag.Tag', blank=True)

    def __str__(self):
        return f'Pull bar #{self.id}'
