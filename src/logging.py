import logging
from enum import StrEnum

LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


def configure_logging(log_level: LogLevel = LogLevel.ERROR):
    # Telethon
    logging.getLogger("telethon").setLevel(level=logging.WARNING)

    # httpx
    logging.getLogger("httpx").setLevel(level=logging.WARNING)
    logging.getLogger("httpcore").setLevel(level=logging.WARNING)

    log_level = str(log_level).upper()
    log_levels = [level.value for level in LogLevel]

    if log_level not in log_levels:
        logging.basicConfig(level=LogLevel.ERROR)
        return

    if log_level == LogLevel.DEBUG:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
        return

    logging.basicConfig(level=log_level)
