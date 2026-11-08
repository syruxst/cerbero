"""
Cerbero - Configuración de logging.

Logger central `cerbero`. En verboso usa RichHandler si está disponible.
Siempre escribe a stderr para no contaminar la salida de wordlists
(que puede ir a stdout en modo pipe).
"""
from __future__ import annotations

import logging
import sys

LOGGER_NAME = "cerbero"


def setup_logging(verbosity: int = 0) -> logging.Logger:
    """
    Configura y devuelve el logger de la aplicación.

    Args:
        verbosity: 0 = WARNING, 1 = INFO, 2+ = DEBUG.

    Returns:
        Logger configurado.
    """
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    logger.handlers.clear()

    handler: logging.Handler
    try:
        from rich.logging import RichHandler

        handler = RichHandler(
            console=None,
            show_time=True,
            show_path=False,
            rich_tracebacks=True,
            markup=True,
        )
        handler.setFormatter(logging.Formatter("%(message)s", datefmt="[%X]"))
    except Exception:  # pragma: no cover
        handler = logging.StreamHandler(stream=sys.stderr)
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)-7s %(message)s", datefmt="%H:%M:%S")
        )

    handler.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def get_logger() -> logging.Logger:
    """Devuelve el logger de la aplicación (ya configurado o por defecto)."""
    return logging.getLogger(LOGGER_NAME)
