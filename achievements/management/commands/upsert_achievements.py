from django.core.management.base import BaseCommand

from achievements.helpers.upsert import upsert_achievements
from user.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            upsert_achievements(user)
