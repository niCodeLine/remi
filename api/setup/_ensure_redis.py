"""Check that Redis is reachable during startup."""

import redis

import api.log as log
from api.settings import settings

logger = log.ger(__name__, "DEBUG", file_name="api")


def ensure_redis():
    """Ping Redis so startup fails loudly when the configured cache is down."""

    logger.debug("Checking Redis...")

    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
    )

    try:
        if redis_client.ping():
            logger.info("Redis server running.")
    except Exception as exc:
        logger.exception(f"ensure_redis failed: {exc}")
        raise
