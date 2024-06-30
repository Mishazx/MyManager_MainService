from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('group_names', nargs='+', type=str)
    def handle(self, *args, **options):
        group_names = options['group_names']
        for group_name in group_names:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f'Group {group_name} created successfully')
            else:
                self.stdout.write(f'Group {group_name} already exists')