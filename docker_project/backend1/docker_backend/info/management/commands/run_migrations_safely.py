# info/management/commands/run_migrations_safely.py

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection, transaction

class Command(BaseCommand):
    help = 'Run migrations safely with a database lock'

    def handle(self, *args, **options):
        lock_name = 'django_migration_lock'
        fake_flag = '--fake' if connection.introspection.table_names() else ''

        with connection.cursor() as cursor:
            # Try to acquire the lock
            cursor.execute(f"SELECT GET_LOCK('{lock_name}', 10)")
            locked = cursor.fetchone()[0]

            if not locked:
                self.stdout.write(self.style.ERROR('Failed to acquire migration lock. Another migration might be running.'))
                return

            try:
                self.stdout.write(self.style.SUCCESS('Acquired migration lock. Running migrations...'))
                call_command('migrate', *args, **options, fake_initial=True if fake_flag else None)
                self.stdout.write(self.style.SUCCESS('Migrations completed successfully.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error while running migrations: {e}'))
            finally:
                # Release the lock
                cursor.execute(f"SELECT RELEASE_LOCK('{lock_name}')")
                self.stdout.write(self.style.SUCCESS('Released migration lock.'))
