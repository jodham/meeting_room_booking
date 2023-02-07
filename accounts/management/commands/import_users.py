import csv
import os

from django.core.management.base import BaseCommand
from room_booking_app.models import User


class Command(BaseCommand):
    help = 'import new users to database'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str, help='The directory containing the CSV file')
        parser.add_argument('filename', type=str, help='The name of the CSV file to import')

    def handle(self, *args, **kwargs):
        # Main logic for the command
        filename = kwargs['filename']
        file_path = os.path.join(kwargs['directory'], filename)
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                data = {key: value for key, value in zip(headers, row)}
                email = data.get('email')
                username = data.get('username')
                if email:
                    user, created = User.objects.get_or_create(email=email)
                elif username:
                    user, created = User.objects.get_or_create(username=username)
                else:
                    # No email or username provided, skip the user
                    continue
                if created:
                    # New user, set password and other fields
                    user.set_password(data.get('password'))
                    user.save()
