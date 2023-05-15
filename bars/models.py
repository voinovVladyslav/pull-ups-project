from django.db import models
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
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90),
        ]
    )
    longitude = models.DecimalField(
        max_digits=11,
        decimal_places=9,
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180),
        ]
    )
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f'Pull bar #{self.id}'
