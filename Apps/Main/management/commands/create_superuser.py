import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    help = 'Create a superuser and add it to all groups'
    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            admin_username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
            admin_email = os.getenv('DJANGO_SUPERUSER_EMAIL')
            admin_password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')
            # Create the superuser
            user = User.objects.create_superuser(admin_username, admin_email, admin_password)
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
            # Get all groups
            groups = Group.objects.all()
            # Add the superuser to all groups
            user.groups.set(groups)
            self.stdout.write(self.style.SUCCESS('Superuser added to all groups'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))