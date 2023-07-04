import uuid
from django.db import models


class LogRecordType(models.Model):
    """
    Model of the log record type.
    """
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class LogRecordLevel(models.Model):
    """
    Type of the log record level.
    """
    name = models.CharField(max_length=32, unique=True)

    def __str__(self) -> str:
        return self.name


class LogRecord(models.Model):
    """
    Model of the log record.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    level = models.ForeignKey(LogRecordLevel, on_delete=models.CASCADE)
    type = models.ForeignKey(
        LogRecordType,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    message = models.TextField()
    trace = models.TextField(
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.message
