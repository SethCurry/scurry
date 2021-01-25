import logging
import sys
import structlog
from structlog.stdlib import LoggerFactory

logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.DEBUG,
)

structlog.configure(logger_factory=LoggerFactory())


def get_logger(name: str):
    return structlog.get_logger(name)
