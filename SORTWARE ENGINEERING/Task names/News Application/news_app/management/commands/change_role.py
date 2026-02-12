"""
Management command to change user roles directly
Usage: python manage.py change_role <username> <role>
Example: python manage.py change_role chris JOURNALIST
"""
from django.core.management.base import BaseCommand
from news_app.models import CustomUser


class Command(BaseCommand):
    help = 'Change a user role directly'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user')
        parser.add_argument('role', type=str, choices=['READER', 'EDITOR', 'JOURNALIST'], help='New role')

    def handle(self, *args, **options):
        username = options['username']
        new_role = options['role']
        
        try:
            user = CustomUser.objects.get(username=username)
            old_role = user.role
            
            # Change role using raw SQL to bypass everything
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE news_app_customuser SET role = %s WHERE id = %s",
                    [new_role, user.id]
                )
            
            # Refresh and assign groups
            user.refresh_from_db()
            user._assign_to_group()
            
            groups = list(user.groups.values_list('name', flat=True))
            
            self.stdout.write(self.style.SUCCESS(
                f'✅ Successfully changed {username} role from {old_role} to {new_role}'
            ))
            self.stdout.write(f'   Groups: {", ".join(groups)}')
            
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ User "{username}" not found'))
