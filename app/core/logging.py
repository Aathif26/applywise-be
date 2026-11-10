"""Structured logging configuration."""

import logging
import sys
from typing import Any

from app.core.config import get_settings


class StructuredFormatter(logging.Formatter):
    """Emit log records as structured key=value lines.

    In production (DEBUG=False) the output is machine-friendly.  When DEBUG is
    enabled a more human-readable format is used instead.
    """

    def format(self, record: logging.LogRecord) -> str:
        level = record.levelname
        timestamp = self.formatTime(record, self.datefmt)
        logger = record.name
        message = record.getMessage()

        # Include exception info if present
        exc_text = ""
        if record.exc_info and record.exc_info[0] is not None:
            exc_text = f" | exception={self.formatException(record.exc_info)}"

        return (
            f"timestamp={timestamp} level={level} "
            f"logger={logger} message=\"{message}\"{exc_text}"
        )


def setup_logging() -> None:
    """Configure the root logger with structured output."""
    settings = get_settings()

    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredFormatter())

    root = logging.getLogger()
    root.setLevel(log_level)
    # Avoid duplicate handlers on repeated calls (e.g. tests)
    root.handlers.clear()
    root.addHandler(handler)

    # Quieten noisy third-party loggers
    for noisy in ("uvicorn.access", "sqlalchemy.engine"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger."""
    return logging.getLogger(name)

