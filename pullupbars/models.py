from django.db import models


class PullUpBars(models.Model):
    class Meta:
        verbose_name = 'Pull Up Bars'
        verbose_name_plural = 'Pull Up Bars'

    title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'Pull bar #{self.id}'
