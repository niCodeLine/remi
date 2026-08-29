# Remi

> A small self-hosted reminders API.

Remi is the calm, simple version of the idea: save reminders, read them back,
and keep the backend small enough that you can understand every moving piece.

It uses FastAPI, PostgreSQL and Redis, without trying to become a whole product
before the basics are clear.

## The idea

```text
send reminder data  →  validate it  →  store it  →  read it later
```

That is it. No drama. No giant platform hidden behind a tiny example. Remi is
made to be a base you can actually study and reuse.

## Remi & Memo

Remi is the starting point. [Memo](https://github.com/niCodeLine/memos) is the
larger platform built from the same idea.

| Project | Shape | Good for |
| :--- | :--- | :--- |
| Remi | Small reminders API | Learning the API/database layer cleanly |
| [Memo](https://github.com/niCodeLine/memos) | Reminder platform | Workers, API keys, delivery attempts and channels |

```text
Remi = save reminders.
Memo = save reminders, protect access, watch due dates and dispatch messages.
```

## Versions

Remi keeps two useful paths:

- `main` — API plus a small optional assistant layer.
- `basic` — API, PostgreSQL and Redis only, without the assistant layer.

The `basic` branch is there on purpose. Sometimes you do not want the assistant
idea yet; you just want the database logic clean and quiet.

## What is inside

- REST API for reminder CRUD.
- PostgreSQL-backed storage.
- Optional Redis cache for repeated reads.
- Date validation for impossible month/day combinations.
- Small assistant layer that calls the same backend logic as the API.
- Docker Compose file for local PostgreSQL and Redis.
- Unit tests for routes and service behavior.

## Quick start

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Create a local environment file:

```bash
cp .env.example .env
```

Start PostgreSQL and Redis:

```bash
docker compose up -d
```

Run the API:

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

Open the docs:

```text
http://127.0.0.1:8000/docs
```

## Configuration

Default `.env.example` values match the included `docker-compose.yml`.

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

PostgreSQL is required. Redis is used as cache; the API is designed to keep
working from PostgreSQL if Redis is unavailable.

## API map

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Health check |
| `POST` | `/reminders/` | Create a reminder |
| `GET` | `/reminders/` | List or filter reminders |
| `GET` | `/reminders/{id}` | Get one reminder |
| `PATCH` | `/reminders/{id}` | Update a reminder |
| `DELETE` | `/reminders/{id}` | Delete a reminder |

Example:

```bash
curl -X POST "http://127.0.0.1:8000/reminders/" \
  -H "Content-Type: application/json" \
  -d '{"day": 14, "month": 4, "text": "Juanito birthday"}'
```

## Assistant layer

The assistant layer lives in `assistant/`.

`assistant/agent.py` defines Remi, and `assistant/tools.py` exposes the reminder
operations as assistant-callable tools. The assistant does not own the reminder
logic; it calls the same service layer used by the API.

That keeps the project useful in two ways:

- as a regular reminders API;
- as a small backend for a virtual assistant.

If you want the version without assistant code, use the `basic` branch.

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

assistant/
  agent.py             Optional virtual assistant definition
  tools.py             Assistant tool wrappers

tests/
  test_routes.py       API route tests
  test_services.py     Service-level tests
```

## Tests

```bash
python -m unittest discover -v
```

The tests mock database operations where needed, so they do not require a
running PostgreSQL or Redis instance.

## Where to go from here

Remi is deliberately small. If you want the bigger version of the idea, go to
[Memo](https://github.com/niCodeLine/memos), where the project grows into:

- Docker installation for the full application;
- background workers for due reminders;
- API keys for bots and assistant integrations;
- delivery channels such as webhook, Telegram, email or Alexa;
- AI-assisted urgency, category, channel and time suggestions.

Remi is the notebook. Memo is the workshop.
