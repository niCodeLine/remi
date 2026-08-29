# Remi Basic

> The API-only version of Remi.

This branch keeps Remi at its simplest: a reminders API, PostgreSQL storage and
Redis cache helpers. No assistant layer, no workers, no notification platform.
Just the backend base.

It exists because sometimes the small version is the useful one. If you want to
study the service logic, reuse the database layer, or start a different project
from a clean API, this is the branch to open.

## The idea

```text
HTTP request  →  validate reminder  →  save in PostgreSQL  →  read it later
```

That is the whole shape. The code is intentionally direct so the moving pieces
are easy to follow.

## Remi, Remi Basic & Memo

| Project | Shape | Good for |
| :--- | :--- | :--- |
| Remi `basic` | API and database only | Studying or reusing the backend core |
| Remi `main` | API plus optional assistant layer | Connecting the same backend logic to an assistant |
| [Memo](https://github.com/niCodeLine/memos) | Full reminder platform | Workers, API keys, delivery attempts and channels |

```text
Remi Basic = store reminders.
Remi main  = store reminders and expose them to an assistant.
Memo       = store reminders, protect access, watch due dates and dispatch them.
```

## What is inside

- FastAPI routes for reminder CRUD.
- PostgreSQL as the source of truth.
- Redis helpers for lightweight caching.
- Validation for impossible day/month combinations.
- Small service layer separated from the HTTP routes.
- Docker Compose file for local PostgreSQL and Redis.
- Unit tests that mock external services where needed.

## Quick start

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Create your local environment file:

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

The default `.env.example` values match the included `docker-compose.yml`.

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

PostgreSQL is required. Redis is optional in spirit: it helps with caching, but
the reminder data belongs to PostgreSQL.

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

## Tests

```bash
python -m unittest discover -v
```

The tests mock database operations where needed, so they do not require a
running PostgreSQL or Redis instance.

## Where to go next

Use this branch if you want the quiet base.

Use `main` if you want the assistant-facing version of Remi.

Use [Memo](https://github.com/niCodeLine/memos) if you want the larger platform
with API keys, workers, retries and delivery channels.

Small base first. Bigger ideas later.
