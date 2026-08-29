"""FastAPI application entrypoint for Remi."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

import api.log as log
import api.setup.setup as setup
from .routes.reminders import router as reminders_router

logger = log.ger(__name__, "DEBUG", file_name="api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Prepare storage on startup and log shutdown.

    This is where Remi makes sure PostgreSQL, Redis and the reminders table are
    reachable before serving requests.
    """

    logger.info("Starting up.")
    setup.main()

    yield

    logger.info("Shutting down.")


app = FastAPI(
    title="Reminders API",
    description="API for managing reminders and memos",
    version="0.2.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    """Health endpoint used to check that the API is alive."""

    logger.info("root endpoint accessed")
    return {
        "message": "API running.",
        "docs": "Find documentation at /docs",
    }


app.include_router(reminders_router)
logger.debug("API configured.")
