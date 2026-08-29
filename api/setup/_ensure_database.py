"""Create the application database when it is missing."""

import psycopg2

import api.log as log
from api.settings import settings

logger = log.ger(__name__, "DEBUG", file_name="api")


def ensure_database():
    """Connect to the default `postgres` DB and create Remi's DB if needed."""

    database_name = settings.POSTGRES_DB
    logger.debug(f"Checking database {database_name}...")

    conn = psycopg2.connect(
        host=settings.POSTGRES_HOST,
        database="postgres",
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        port=settings.POSTGRES_PORT,
    )

    conn.autocommit = True
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT 1
            FROM pg_database
            WHERE datname = %s
            """,
            (database_name,),
        )

        exists = cursor.fetchone()
        if exists:
            logger.info(f'Database "{database_name}" already exists.')
        else:
            cursor.execute(f"CREATE DATABASE {database_name}")
            logger.info(f'Database "{database_name}" created.')

        logger.debug("Database check completed.")
    except Exception as exc:
        logger.exception(f"ensure_database failed: {exc}")
        raise
    finally:
        cursor.close()
        conn.close()
