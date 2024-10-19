"""
Django command to wait for db service to be available
before starting app
"""
import time
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to wait for db"""

    def handle(self, *args, **options):
        """Entrypoint for command"""

        # write message to log
        self.stdout.write("Waiting for database...")
        # is db up?
        db_up = False
        # while db is not up, keep checking and waiting
        while db_up is False:
            try:
                # checks if default db is up
                self.check(databases=["default"])
                #  if db is up, set db_up to True
                db_up = True
            except (Psycopg2Error, OperationalError):
                # if db is not up due to Psycopg2Error or OperationalError,
                # write message to log
                self.stdout.write("Database unavailable, waiting 1 second...")
                #  wait for 1 second before retrying
                time.sleep(1)
        # write message to log once db is up
        self.stdout.write(self.style.SUCCESS("Database available!"))
