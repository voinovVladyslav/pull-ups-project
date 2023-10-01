from django.db import models


class Achievement(models.Model):
    title = models.CharField(
        max_length=255,
    )
    description = models.TextField()
    done = models.BooleanField(
        default=False
    )
    achieved_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='achievements'
    )

    def __str__(self) -> str:
        return f'{self.title} ({self.user.email})'
