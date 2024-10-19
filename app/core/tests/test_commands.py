"""
Test management commands
"""

# import patch from unittest to mock making management command
from unittest.mock import patch

# import OperationalError - when db has not started yet
from psycopg2 import OperationalError as Psycopg2Error

# import call_command to call the management command
from django.core.management import call_command

# import OperationalError - when db is not ready yet
from django.db.utils import OperationalError

# import SimpleTestCase test suites
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db when db is available"""
        # mock db is available by setting return_value to True
        patched_check.return_value = True

        # mock calling "wait_for_db" command
        call_command("wait_for_db")

        # assert "wait_for_db" calls check method once with "default" db
        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when getting OperationalError"""
        # mock side effect of check method to raise
        # Psycopg2Error 2 times, OperationalError 3 times, True once
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        print("test_wait_for_db_delay:: before calling wait_for_db")
        # mock calling "wait_for_db" command
        call_command("wait_for_db")
        print("test_wait_for_db_delay:: after calling wait_for_db")

        # assert that check method was called 6 times
        self.assertEqual(patched_check.call_count, 6)
        # assert that sleep method was called 5 times
        self.assertEqual(patched_sleep.call_count, 5)

        # assert that check method was called with "default" db each time
        patched_check.assert_called_with(databases=["default"])
