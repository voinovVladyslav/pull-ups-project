from django.core.management.base import BaseCommand

from achievements.helpers.upsert import upsert_achievements


class Command(BaseCommand):
    def handle(self, *args, **options):
        upsert_achievements()
