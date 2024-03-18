from django.db import models


class BaseCounter(models.Model):
    class Meta:
        abstract = True

    reps = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PullUpCounter(BaseCounter):
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='pullup_counter',
    )
    pullupbar = models.ForeignKey(
        'pullupbars.PullUpBars',
        on_delete=models.CASCADE,
        related_name='pullup_counter',
    )


class DipCounter(BaseCounter):
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='dip_counter',
    )
    dipstation = models.ForeignKey(
        'dipstations.DipStations',
        on_delete=models.CASCADE,
        related_name='dip_counter',
    )
