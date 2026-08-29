"""PostgreSQL operations for reminders.

This is Remi's main service layer. Routes and assistant tools call these
functions instead of touching SQL directly.
"""

from types import SimpleNamespace

import api.log as log
from api.constants import MAIN_REMINDERS_TABLE
from api.database import get_PG_connection
from api.exceptions import DatabaseUnavailable, InvalidReminderDate, ReminderNotFound
from api.services_redis import redisDelete, redisGet, redisSet

logger = log.ger(__name__, "DEBUG", file_name="api")

# February allows 29 here because reminders are month/day based, not year based.
MONTH_DAYS = {
    1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31,
}

MONTH_NAMES = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December",
}


def cache_key(reminder_id: int) -> str:
    """Return the Redis key used for a single reminder lookup."""

    return f"get_by_id:{reminder_id}"


def validate_date(day: int, month: int) -> None:
    """Reject dates such as April 31 before they reach the database."""

    if day > MONTH_DAYS[month]:
        raise InvalidReminderDate(
            f"{MONTH_NAMES[month]} does not have {day} days."
        )


def _reminder_data(reminder_id, day, month, text, created_at) -> dict:
    """Convert a raw database row into Remi's public reminder shape."""

    return {
        "reminder_id": reminder_id,
        "day": day,
        "month": month,
        "month_name": MONTH_NAMES[month],
        "text": text,
        "created_at": created_at,
    }


def _connection():
    """Open PostgreSQL and translate connection failures into project errors."""

    try:
        return get_PG_connection()
    except Exception as exc:
        logger.exception("Database connection failed.")
        raise DatabaseUnavailable("The database is unavailable.") from exc


def create(*, day: int, month: int, text: str):
    """Create a reminder and return a small response object for API/tool layers."""

    validate_date(day, month)
    conn = _connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO {MAIN_REMINDERS_TABLE} (day, month, text)
                VALUES (%s, %s, %s)
                RETURNING id, created_at
                """,
                (day, month, text),
            )
            reminder_id, created_at = cursor.fetchone()
        conn.commit()
    except Exception as exc:
        conn.rollback()
        logger.exception("Reminder creation failed.")
        raise DatabaseUnavailable("Could not create the reminder.") from exc
    finally:
        conn.close()

    reminder = _reminder_data(reminder_id, day, month, text, created_at)
    return SimpleNamespace(
        code=1,
        message=f'Reminder "{text}" created with id {reminder_id}.',
        reminder=reminder,
    )


def get_by_id(reminder_id: int):
    """Get one reminder by id, using Redis as a soft cache when available."""

    query = cache_key(reminder_id)
    cached = redisGet(query)
    if cached:
        return cached

    conn = _connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT day, month, text, created_at
                FROM {MAIN_REMINDERS_TABLE}
                WHERE id = %s
                """,
                (reminder_id,),
            )
            row = cursor.fetchone()
    except Exception as exc:
        logger.exception("Getting reminder failed.")
        raise DatabaseUnavailable("Could not retrieve the reminder.") from exc
    finally:
        conn.close()

    if row is None:
        raise ReminderNotFound(f"Reminder with id {reminder_id} not found.")

    reminder = _reminder_data(reminder_id, *row)
    response = SimpleNamespace(
        code=1,
        message=f"Reminder with id {reminder_id} found.",
        reminder=reminder,
    )
    redisSet(query=query, response=response)
    return response


def get(
    day: int | None = None,
    month: int | None = None,
    text: str | None = None,
):
    """List reminders, optionally filtered by day, month or text."""

    conn = _connection()
    try:
        query = f"""
            SELECT id, day, month, text, created_at
            FROM {MAIN_REMINDERS_TABLE}
            WHERE 1=1
        """
        params = []

        if day is not None:
            query += " AND day = %s"
            params.append(day)
        if month is not None:
            query += " AND month = %s"
            params.append(month)
        if text is not None:
            query += " AND text ILIKE %s"
            params.append(f"%{text}%")

        query += " ORDER BY month, day, id"
        with conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
    except Exception as exc:
        logger.exception("Getting reminders failed.")
        raise DatabaseUnavailable("Could not retrieve reminders.") from exc
    finally:
        conn.close()

    reminders = [_reminder_data(*row) for row in rows]
    return SimpleNamespace(
        code=1,
        message=f"{len(reminders)} reminder(s) found.",
        reminders=reminders,
    )


def update(
    reminder_id: int,
    *,
    day: int | None = None,
    month: int | None = None,
    text: str | None = None,
):
    """Update any reminder field while preserving values not provided."""

    if day is None and month is None and text is None:
        raise ValueError("At least one field must be provided.")

    conn = _connection()
    try:
        with conn.cursor() as cursor:
            # Read the existing row first so partial updates can keep old values
            # and date validation can check the final day/month pair.
            cursor.execute(
                f"""
                SELECT day, month, text
                FROM {MAIN_REMINDERS_TABLE}
                WHERE id = %s
                """,
                (reminder_id,),
            )
            current = cursor.fetchone()
            if current is None:
                raise ReminderNotFound(
                    f"Reminder with id {reminder_id} not found."
                )

            new_day = day if day is not None else current[0]
            new_month = month if month is not None else current[1]
            new_text = text if text is not None else current[2]
            validate_date(new_day, new_month)

            cursor.execute(
                f"""
                UPDATE {MAIN_REMINDERS_TABLE}
                SET day = %s, month = %s, text = %s
                WHERE id = %s
                RETURNING created_at
                """,
                (new_day, new_month, new_text, reminder_id),
            )
            created_at = cursor.fetchone()[0]
        conn.commit()
    except (ReminderNotFound, InvalidReminderDate):
        conn.rollback()
        raise
    except Exception as exc:
        conn.rollback()
        logger.exception("Updating reminder failed.")
        raise DatabaseUnavailable("Could not update the reminder.") from exc
    finally:
        conn.close()

    # The cached single-reminder response is now stale.
    redisDelete(cache_key(reminder_id))
    reminder = _reminder_data(
        reminder_id, new_day, new_month, new_text, created_at
    )
    return SimpleNamespace(
        code=1,
        message=f"Reminder with id {reminder_id} updated.",
        reminder=reminder,
    )


def delete(reminder_id: int):
    """Delete a reminder and return the deleted data."""

    conn = _connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                f"""
                DELETE FROM {MAIN_REMINDERS_TABLE}
                WHERE id = %s
                RETURNING day, month, text, created_at
                """,
                (reminder_id,),
            )
            row = cursor.fetchone()
        if row is None:
            conn.rollback()
            raise ReminderNotFound(f"Reminder with id {reminder_id} not found.")
        conn.commit()
    except ReminderNotFound:
        raise
    except Exception as exc:
        conn.rollback()
        logger.exception("Deleting reminder failed.")
        raise DatabaseUnavailable("Could not delete the reminder.") from exc
    finally:
        conn.close()

    redisDelete(cache_key(reminder_id))
    reminder = _reminder_data(reminder_id, *row)
    return SimpleNamespace(
        code=1,
        message=f"Reminder with id {reminder_id} deleted.",
        reminder=reminder,
    )
