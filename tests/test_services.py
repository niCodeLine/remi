from unittest import TestCase
import os

os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_DB", "reminders")
os.environ.setdefault("POSTGRES_USER", "reminders_user")
os.environ.setdefault("POSTGRES_PASSWORD", "reminders_password")
os.environ.setdefault("REDIS_HOST", "localhost")

from api.exceptions import InvalidReminderDate
from api.services_db import validate_date


class DateValidationTests(TestCase):
    def test_valid_date_is_accepted(self):
        validate_date(day=30, month=4)

    def test_april_31_is_rejected(self):
        with self.assertRaises(InvalidReminderDate):
            validate_date(day=31, month=4)

    def test_february_30_is_rejected(self):
        with self.assertRaises(InvalidReminderDate):
            validate_date(day=30, month=2)
