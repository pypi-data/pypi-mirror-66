"""Command handler for all QC checks on the project."""
from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Command handler for all qc checks on the project."""
    help = 'Runs lint and test coverage on the project.'

    def handle(self, *args, **options):
        call_command('lint')
        call_command('coverage')
