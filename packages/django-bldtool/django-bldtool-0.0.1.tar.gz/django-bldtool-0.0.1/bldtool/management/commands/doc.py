"""doc django-admin command handler and support"""
import contextlib
import os
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string

@contextlib.contextmanager
def cd(path):  #pylint: disable=invalid-name
    """Context manager for changing the current working directory"""

    new_path = os.path.expanduser(path)
    saved_path = os.getcwd()
    os.chdir(new_path)
    yield
    os.chdir(saved_path)

class Command(BaseCommand):
    """Command handler to make the documentation for the site."""
    help = "Build the documentation."

    def add_arguments(self, parser):
        parser.add_argument(
            '--init-dev',
            action='store_true',
            help='Create and initialize the doc-developer directory.'
        )
        parser.add_argument(
            '--init-user',
            action='store_true',
            help='Create and initialize the doc-user directory.'
        )

    def handle(self, *args, **options):
        if options['init_dev']:
            _init_doc('developer')
        if options['init_user']:
            _init_doc('user')

        _build_developer()
        _build_user()

def _init_doc(path):
    """Create the doc-{path} directory and set the index and config file."""
    if os.path.exists(f'doc-{path}'):
        raise CommandError(f'Directory doc-{path} already exists.')

    params = {
        'project': 'Demo Project Site',
        'author': 'Stefan Koch',
        'year': '2020',
    }
    conf = render_to_string("bldtool/sphinx_conf.py", params)
    gitignore = render_to_string("bldtool/sphinx_gitignore", params)
    index = render_to_string(f"bldtool/sphinx_{path}.rst", params)

    os.mkdir(f'doc-{path}')
    open(f'doc-{path}/conf.py', 'w').write(conf)
    open(f'doc-{path}/.gitignore', 'w').write(gitignore)
    open(f'doc-{path}/index.rst', 'w').write(index)

def _build_developer():
    """Build the developer documentation including the generated API documentation."""

    # don't do anything if the documentation does not exist.
    if not os.path.exists('doc-developer'):
        return

    # if the directory exist, make the documentation.
    with cd('doc-developer'):
        os.system('sphinx-apidoc -M -f -e -o apidoc ..')
        os.system('rm -rf build')
        os.system('sphinx-build  -q . build')

def _build_user():
    """Build the user level documentation."""
    # don't do anything if the documentation does not exist.
    if not os.path.exists('doc-user'):
        return

    with cd('doc-user'):
        os.system('sphinx-build  -q . build')
