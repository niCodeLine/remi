"""Create the PostgreSQL tables needed by Remi."""

from api.constants import MAIN_REMINDERS_TABLE
from api.database import get_PG_connection
import api.log as log

logger = log.ger(__name__, "DEBUG", file_name="api")


# Table definitions are kept in a dictionary so more tables can be added later
# without changing the loop in `create_tables()`.
TABLES = {
    MAIN_REMINDERS_TABLE:
        """
        id SERIAL PRIMARY KEY,

        user_id INTEGER DEFAULT 1,

        day INTEGER NOT NULL CHECK(day BETWEEN 1 AND 31),
        month INTEGER NOT NULL CHECK(month BETWEEN 1 AND 12),

        text TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT NOW()
        """,
}


def create_tables():
    """Create all declared tables if they do not already exist."""

    conn = get_PG_connection()
    cursor = conn.cursor()  # type: ignore

    try:
        for tableName, tableDefinition in TABLES.items():
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {tableName} (
                {tableDefinition}
                )
                """
            )
            logger.info(f'Table "{tableName}" ready.')

        conn.commit()  # type: ignore
        logger.info("Tables committed to database.")
    except Exception as exc:
        logger.exception(f"Create table failed: {exc}")
        raise
    finally:
        cursor.close()
        conn.close()  # type: ignore


if __name__ == "__main__":
    create_tables()
