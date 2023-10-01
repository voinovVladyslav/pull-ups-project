from django.core.management.base import BaseCommand

from achievements.constants import ACHIEVEMENTS


class Command(BaseCommand):
    def handle(self, *args, **options):
        checked_ids = []
        all_good = True
        for achievement in ACHIEVEMENTS:
            if achievement['id'] in checked_ids:
                print(f'ID {achievement["id"]} got dublicates')
                all_good = False
                continue
            checked_ids.append(achievement['id'])

        if all_good:
            print('All good')
