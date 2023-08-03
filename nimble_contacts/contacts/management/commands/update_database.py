from django.core.management.base import BaseCommand
from contacts.utils import manual_update


class Command(BaseCommand):
    help = 'Update the database after starting the server for the first time.'

    def handle(self, *args, **options):
        print("Updating the database...")
        last_update = manual_update()
        print(f"Updating is done. Last update: {last_update}")
