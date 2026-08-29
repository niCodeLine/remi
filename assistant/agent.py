"""Google ADK assistant definition for Remi.

This file wires the assistant personality to the tool functions. The reminder
logic still lives in `api/services_db.py`.
"""

import warnings

from google.adk.agents.llm_agent import Agent

from assistant.tools import (
    create_reminder,
    date_now,
    delete_reminder,
    get_reminder_by_id,
    get_reminders,
)

warnings.filterwarnings("ignore", message=".*EXPERIMENTAL.*")


root_agent = Agent(
    name="Remi",
    model="gemini-2.5-flash",
    description="Create, save and get reminders.",
    instruction="""
    - You help creating and getting reminders.
    - You translate natural language into the specific parameters of the functions, and the other way around.
    - Talk in 1st person.
    - Respond in user's language.
    - Redact the reminders when retrieving, dont be literal, give id.
    """,
    tools=[date_now, get_reminder_by_id, get_reminders, delete_reminder, create_reminder],
)
