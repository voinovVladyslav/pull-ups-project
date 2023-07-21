from django.db import models


class BaseCounter(models.Model):
    class Meta:
        abstract = True

    reps = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PullUpCounter(BaseCounter):
    user = models.ForeignKey(
        'user.User', on_delete=models.CASCADE, related_name='pullup_counter'
    )
    bar = models.ForeignKey(
        'bars.Bars', on_delete=models.CASCADE, related_name='pullup_counter'
    )
