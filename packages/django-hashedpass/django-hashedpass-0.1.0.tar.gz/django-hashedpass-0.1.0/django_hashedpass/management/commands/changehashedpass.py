'''Change a user's hashed password.'''

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Change a user's hashed password"

    def add_arguments(self, parser):
        parser.add_argument('username',
                            help='The user')
        parser.add_argument('hashed_password',
                            help='The new hashed password for the user')

    def handle(self, *args, **options):
        username = options['username']
        hashed_password = options['hashed_password']

        # Get user instance based on the username.
        UserModel = get_user_model()
        try:
            # Note: the username field is not guaranteed to be 'username'.
            user = UserModel.objects.get(**{UserModel.USERNAME_FIELD: username})
        except UserModel.DoesNotExist:
            raise CommandError('"{}" is not a known username.'.format(username))

        # Change the hashed password.
        user.password = hashed_password
        user.save()
        self.stdout.write(
            self.style.SUCCESS('Successfully changed the hashed password for "{}".'
                               .format(username)))
