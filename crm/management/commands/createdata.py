from django.core.management.base import BaseCommand
from fixtures import create_test_data

class Command(BaseCommand):
    help = 'Creates test data for the CRM system'

    def handle(self, *args, **options):
        create_test_data()
        self.stdout.write(self.style.SUCCESS('Successfully created test data'))