"""Startup setup for Remi.

The API calls `main()` during lifespan startup so the local database, table and
Redis connection are checked before requests arrive.
"""

import api.log as log
from ._create_tables import create_tables
from ._ensure_database import ensure_database
from ._ensure_redis import ensure_redis

logger = log.ger(__name__, "DEBUG", file_name="api")


def main():
    """Run all storage checks needed by the app."""

    logger.info("Executing initialization setup.")
    ensure_database()
    create_tables()
    ensure_redis()
    logger.info("Setup completed successfully.")


if __name__ == "__main__":
    main()
