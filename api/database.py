"""Database connection helpers.

The service layer imports these functions instead of creating PostgreSQL or
Redis clients directly. That keeps connection details in one small file.
"""

import psycopg2
import redis

import api.log as log
from api.settings import settings

logger = log.ger(__name__, "DEBUG", file_name="api")


def get_PG_connection():
    """Open a PostgreSQL connection using the values from `.env`."""

    logger.debug("Accessing PostgreSQL connection.")

    return psycopg2.connect(
        host=settings.POSTGRES_HOST,
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        port=settings.POSTGRES_PORT,
    )


def get_RD_connection(db: int = 0):
    """Open a Redis connection.

    `db` is the Redis database number. The project uses database 0 by default.
    `decode_responses=True` returns strings instead of bytes, which keeps the
    cache code easier to read.
    """

    logger.debug("Accessing Redis connection.")

    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=db,
        decode_responses=True,
    )
