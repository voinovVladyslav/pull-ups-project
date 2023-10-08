from django.db import models


class AchievementType(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
    )

    def __str__(self) -> str:
        return self.name


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
    threshold = models.PositiveIntegerField()
    type = models.ForeignKey(
        AchievementType,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='achievements'
    )

    def __str__(self) -> str:
        return f'{self.title} ({self.user.email})'
