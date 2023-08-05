"""Command handler for test coverage on the whole project."""
import json
import os
import subprocess
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    """Command handler for coverage on the whole project."""
    help = 'Runs coverage on all the (python) source code of the project.'

    def handle(self, *args, **options):
        # Make sure all the tests pass.
        subprocess.call(['coverage', 'erase'])
        ret = subprocess.call([
            'coverage', 'run',
            f'--rcfile={os.path.dirname(__file__)}/../../config/coveragerc',
            '--source=.',
            'manage.py', 'test',
        ])
        if ret:
            raise CommandError("Code not Tests did not pass.")

        # if there were no errors, show the results and look for coverage.
        subprocess.call([
            'coverage', 'html',
        ])
        subprocess.call(['coverage', 'report'])
        data = json.loads(
            subprocess.run(['coverage', 'json', '-o', '-'],
                           capture_output=True, check=True).stdout)
        if data['totals']['missing_lines'] > 0:
            raise CommandError("Code not 100% coverage")
