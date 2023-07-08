import logging
import traceback


class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        from .models import LogRecordLevel, LogRecord, LogRecordType
        from user.models import User
        from bars.models import Bars
        log_record = LogRecord()

        if hasattr(record, "type"):
            log_record_type, _ = LogRecordType.objects.get_or_create(
                name=record.type
            )
            log_record.type = log_record_type

        log_record_level, _ = LogRecordLevel.objects.get_or_create(
            name=record.levelname
        )
        log_record.level = log_record_level

        if hasattr(record, 'user'):
            if isinstance(record.user, User):
                user = record.user
            else:
                user = User.objects.filter(
                    id=record.user
                ).first()

            if user:
                log_record.user = user

        if hasattr(record, 'bar'):
            if isinstance(record.bar, Bars):
                bar = record.bar
            else:
                bar = Bars.objects.filter(
                    id=record.bar
                ).first()
            if bar:
                log_record.bar = bar

        log_record.message = record.getMessage()

        if record.exc_info:
            log_record.trace = traceback.format_exc()

        log_record.save()
