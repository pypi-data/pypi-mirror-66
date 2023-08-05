"""Command handler for lint on the whole project."""
import glob
import os
import subprocess
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    """Command handler for lint on the whole project."""
    help = 'Runs lint on all the source code of the project.'

    def handle(self, *args, **options):
        modules = [o for o in os.listdir('.')
                   if os.path.isdir(o) and os.path.exists(o+'/__init__.py')]
        pylint_ret = subprocess.call([
            'pylint',
            f'--rcfile={os.path.dirname(__file__)}/../../config/pylintrc',
            '-rn'] + modules)

        modules = [o for o in os.listdir('.')
                   if os.path.isdir(o) and os.path.exists(o+'/react/')]
        tslint_ret = 0
        for mod in modules:
            tslint_ret |= subprocess.call([
                f'{mod}/react/node_modules/.bin/tslint',
                '-c', f'{mod}/react/tslint.json',
            ] + glob.glob(f'{mod}/react/src/**/*.tsx', recursive=True))

        if pylint_ret or tslint_ret:
            raise CommandError("Code not lint clean")
