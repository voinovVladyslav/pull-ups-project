from django.db import models


class Notification(models.Model):
    message = models.TextField()
    unread = models.BooleanField(
        default=True
    )
    redirect_to = models.CharField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
