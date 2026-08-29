"""Project logger helper.

Small projects often start with scattered `print()` calls. This helper keeps logs
consistent and avoids adding duplicate handlers when modules are imported more
than once.
"""

import logging


def ger(
    name: str = __name__,
    level: str = "INFO",
    console_logs: bool = True,
    file_logs: bool = True,
    file_name: str = "logs",
):
    """Configure and return a logger.

    `ger` is intentionally kept as the original helper name for compatibility
    with the rest of the project.
    """

    logger = logging.getLogger(name)

    # Avoid duplicate handlers when FastAPI reloads or modules are imported many
    # times during tests.
    if logger.handlers:
        return logger

    levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    log_level = levels.get(level.upper(), logging.INFO)
    logger.setLevel(log_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S | (%d/%m/%Y)",
    )

    if console_logs:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(log_level)
        logger.addHandler(console_handler)

    if file_logs:
        file_handler = logging.FileHandler(f"{file_name}.log", encoding="utf-8", mode="a")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)

    return logger
