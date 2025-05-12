from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        # Your seed logic here
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))
