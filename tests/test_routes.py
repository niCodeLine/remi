from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch
import os

os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_DB", "reminders")
os.environ.setdefault("POSTGRES_USER", "reminders_user")
os.environ.setdefault("POSTGRES_PASSWORD", "reminders_password")
os.environ.setdefault("REDIS_HOST", "localhost")

from fastapi.testclient import TestClient

from api.exceptions import ReminderNotFound
from api.main import app


class ReminderRouteTests(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("api.routes.reminders.services_db.create")
    def test_create_returns_201(self, create):
        create.return_value = SimpleNamespace(
            message="Reminder created.",
            reminder={
                "reminder_id": 1,
                "day": 14,
                "month": 4,
                "month_name": "April",
                "text": "Birthday",
                "created_at": "2026-06-28T12:00:00",
            },
        )

        response = self.client.post(
            "/reminders/",
            json={"day": 14, "month": 4, "text": "Birthday"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["reminder"]["reminder_id"], 1)

    @patch("api.routes.reminders.services_db.get_by_id")
    def test_missing_reminder_returns_404(self, get_by_id):
        get_by_id.side_effect = ReminderNotFound(
            "Reminder with id 99 not found."
        )

        response = self.client.get("/reminders/99")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["detail"],
            "Reminder with id 99 not found.",
        )

    def test_invalid_request_body_returns_422(self):
        response = self.client.post(
            "/reminders/",
            json={"day": 32, "month": 4, "text": ""},
        )

        self.assertEqual(response.status_code, 422)

    def test_empty_patch_returns_422(self):
        response = self.client.patch("/reminders/1", json={})

        self.assertEqual(response.status_code, 422)

    @patch("api.routes.reminders.services_db.get")
    def test_empty_collection_is_successful(self, get_reminders):
        get_reminders.return_value = SimpleNamespace(
            message="0 reminder(s) found.",
            reminders=[],
        )

        response = self.client.get("/reminders/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["reminders"], [])
