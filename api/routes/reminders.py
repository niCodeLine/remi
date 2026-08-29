"""HTTP routes for Remi reminders."""

from fastapi import APIRouter, HTTPException, Query, status

import api.log as log
import api.services_db as services_db
from api.exceptions import DatabaseUnavailable, InvalidReminderDate, ReminderNotFound
from api.schemas import CreateReminder, UpdateReminder

logger = log.ger(__name__, "DEBUG", file_name="api")

router = APIRouter(prefix="/reminders", tags=["reminders"])


def _response(response, collection: bool = False) -> dict:
    """Convert service responses into the public JSON shape."""

    key = "reminders" if collection else "reminder"
    return {
        "message": response.message,
        key: getattr(response, key),
    }


def _http_error(exc: Exception) -> HTTPException:
    """Translate project exceptions into HTTP errors that clients understand."""

    if isinstance(exc, InvalidReminderDate):
        return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc))
    if isinstance(exc, ReminderNotFound):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    if isinstance(exc, DatabaseUnavailable):
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        )
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Unexpected server error.",
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_reminder_endpoint(reminder: CreateReminder):
    """Create a reminder from an HTTP request body."""

    try:
        return _response(
            services_db.create(
                text=reminder.text,
                day=reminder.day,
                month=reminder.month,
            )
        )
    except Exception as exc:
        raise _http_error(exc) from exc


@router.get("/{reminder_id}")
def get_reminder_by_id_endpoint(reminder_id: int):
    """Get one reminder by id."""

    try:
        return _response(services_db.get_by_id(reminder_id))
    except Exception as exc:
        raise _http_error(exc) from exc


@router.get("/")
def get_reminders_endpoint(
    day: int | None = Query(None, ge=1, le=31),
    month: int | None = Query(None, ge=1, le=12),
    text: str | None = Query(None, min_length=1, max_length=100),
):
    """List reminders with optional query-string filters."""

    try:
        return _response(
            services_db.get(day=day, month=month, text=text),
            collection=True,
        )
    except Exception as exc:
        raise _http_error(exc) from exc


@router.patch("/{reminder_id}")
def update_reminder_endpoint(reminder_id: int, reminder: UpdateReminder):
    """Partially update a reminder."""

    changes = reminder.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="At least one field must be provided.",
        )
    try:
        return _response(services_db.update(reminder_id, **changes))
    except Exception as exc:
        raise _http_error(exc) from exc


@router.delete("/{reminder_id}")
def delete_reminder_endpoint(reminder_id: int):
    """Delete a reminder by id."""

    try:
        return _response(services_db.delete(reminder_id))
    except Exception as exc:
        raise _http_error(exc) from exc
