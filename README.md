# Reminders API Base

Reminders API Base is a small FastAPI backend for saving and managing personal
reminders. It is designed as the foundation for future assistants, bots and
automations.

The goal of this branch is intentionally modest: provide a clean API layer and
database access layer that can store reminders reliably. Notification workers,
users, API keys, delivery channels and assistant/AI behavior are planned as
future extensions, not as part of this API-only version.

## What this project demonstrates

- FastAPI REST API design.
- PostgreSQL integration as the source of truth.
- Redis integration as optional read cache.
- Pydantic request validation.
- Basic CRUD operations.
- Clear error handling for invalid dates, missing reminders and database
  failures.
- Unit tests that run without requiring PostgreSQL or Redis.

## Current scope

This version can:

- create reminders;
- list reminders;
- search reminders by day, month or text;
- retrieve one reminder by ID;
- update a reminder;
- delete a reminder;
- validate impossible dates, such as April 31;
- expose those operations through HTTP endpoints;

This version does not yet:

- send notifications;
- run background workers;
- mark reminders as sent;
- support users or profiles;
- authenticate bots with API keys;
- choose delivery channels;
- integrate directly with Telegram, email, webhooks or Alexa.
- include a virtual assistant layer.

Those features belong to the next project built on top of this base.

## Architecture

```text
Client / bot / future assistant
        ↓
FastAPI routes
        ↓
Reminder service layer
        ↓
PostgreSQL
        ↓
Redis cache, optional
```

PostgreSQL is the main database. Redis is only used as a cache. If Redis is not
available, the API should still use PostgreSQL.

## Project structure

```text
api/
  main.py              FastAPI application setup
  routes/reminders.py  HTTP endpoints
  services_db.py       PostgreSQL reminder operations
  services_redis.py    Redis cache helpers
  schemas.py           Request validation models
  exceptions.py        Project-specific errors
  setup/               Database/table setup helpers

tests/
  test_routes.py       API route tests
  test_services.py     Service-level tests
```

## Requirements

- Python 3.10+
- PostgreSQL
- Redis

Redis is recommended but treated as optional cache. PostgreSQL is required.

## Setup

Create a virtual environment if you want one:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your local `.env` file:

```bash
cp .env.example .env
```

Default values in `.env.example` match the included `docker-compose.yml`.

## Running PostgreSQL and Redis with Docker

If you have Docker installed, you can start PostgreSQL and Redis with:

```bash
docker compose up -d
```

This starts:

- PostgreSQL on port `5432`;
- Redis on port `6379`.

Then run the API locally:

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

The API documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

## Running without Docker

Start PostgreSQL and Redis manually, then make sure your `.env` values match
your local database configuration.

Example `.env`:

```text
POSTGRES_HOST=localhost
POSTGRES_DB=reminders
POSTGRES_USER=reminders_user
POSTGRES_PASSWORD=reminders_password
POSTGRES_PORT=5432

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
```

Then run:

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

## API endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/` | Health check |
| POST | `/reminders/` | Create a reminder |
| GET | `/reminders/` | List or filter reminders |
| GET | `/reminders/{id}` | Get one reminder |
| PATCH | `/reminders/{id}` | Update a reminder |
| DELETE | `/reminders/{id}` | Delete a reminder |

Example:

```bash
curl -X POST "http://127.0.0.1:8000/reminders/" \
  -H "Content-Type: application/json" \
  -d '{"day": 14, "month": 4, "text": "Juanito birthday"}'
```

## Tests

Run:

```bash
python -m unittest discover -v
```

The tests mock database operations where needed, so they do not require a
running PostgreSQL or Redis instance.

## Future direction

This repository is the base. A larger project can build on top of it with:

- Docker installation for the full application;
- workers that send due reminders;
- users, profiles and one local admin;
- API keys for bots and assistant integrations;
- delivery channels such as Telegram, email, webhooks or Alexa;
- AI features such as urgency classification, channel selection and suggested
  reminder times.

See [docs/NEXT_PROJECT.md](docs/NEXT_PROJECT.md) for the proposed expansion.
