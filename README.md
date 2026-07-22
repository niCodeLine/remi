# Reminders API Base

Self-hosted reminders API built for quick capture and local storage. FastAPI,
PostgreSQL and Redis, without the assistant layer.

This branch keeps only the backend base: HTTP endpoints, database access and a
small cache layer. It is meant to stay simple enough to reuse from bots,
assistants, workers or other projects later.

## Versions

- `main` — API + optional assistant layer.
- `basic` — API, PostgreSQL and Redis only.

## Features

- Quick reminder capture through a REST API.
- PostgreSQL-backed storage.
- Optional Redis cache for repeated reads.
- Basic CRUD operations for reminders.
- Date validation for impossible month/day combinations.
- Docker Compose file for local PostgreSQL and Redis.
- Unit tests for routes and service behavior.

## Quick Start

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Create a local environment file:

```bash
cp .env.example .env
```

Start PostgreSQL and Redis with Docker:

```bash
docker compose up -d
```

Run the API:

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

Open:

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

## API

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

## Structure

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

## Tests

```bash
python -m unittest discover -v
```

The tests mock database operations where needed, so they do not require a
running PostgreSQL or Redis instance.

## Roadmap

This branch is the basic layer. A larger reminder platform can build on top of
it with:

- an assistant layer;
- Docker installation for the full application;
- background workers for due reminders;
- users, profiles and a local admin;
- API keys for bots and integrations;
- delivery channels such as Telegram, email, webhooks or Alexa;
- AI-assisted urgency, channel and time suggestions.

See [docs/NEXT_PROJECT.md](docs/NEXT_PROJECT.md) for the possible expansion.

