'''Generates a hashed password from a given plaintext password.'''

from getpass import getpass
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generate a hashed password from a plaintext password.'

    def add_arguments(self, parser):
        parser.add_argument('--password',
                            action='store',
                            required=False,
                            help='The plaintext password')

    def handle(self, *args, **options):
        password = options.get('password')

        # If no password was given in the command line arguments, ask the user.
        if password is None:
            while True:
                password = getpass('Password: ')
                password_confirm = getpass('Password (again): ')

                if password == password_confirm:
                    self.stdout.write(make_password(password))
                    break
                else:
                    self.stderr.write(
                        self.style.ERROR('Passwords do not match. Try again.'))
        else:
            self.stdout.write(make_password(password))
