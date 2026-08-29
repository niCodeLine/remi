"""Pydantic request schemas for Remi's API."""

from pydantic import BaseModel, Field


class ReminderFields(BaseModel):
    """Fields required to create a reminder."""

    text: str = Field(min_length=1, max_length=100)
    day: int = Field(ge=1, le=31)
    month: int = Field(ge=1, le=12)


class CreateReminder(ReminderFields):
    """Create body. Kept separate so it can grow later if needed."""

    pass


class UpdateReminder(BaseModel):
    """Patch body where every field is optional."""

    text: str | None = Field(default=None, min_length=1, max_length=100)
    day: int | None = Field(default=None, ge=1, le=31)
    month: int | None = Field(default=None, ge=1, le=12)
