from datetime import datetime
import logging
import json

TAGS: set[str] = {
    "ERROR",
    "HTTPS",
    "WARNING",
    "LOG",
    "DEBUG",
    "CRITICAL",
    "INFO",
}


hour = datetime.now()

class Colors:
    grey = "\033[92m"
    yellow = "\x1b[33;20m"
    red = "\033[41m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

color = Colors()

class Formatter(logging.Formatter):
    format_ = "[%(asctime)s] [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: color.grey + format_ + color.reset,
        logging.INFO: color.grey + format_ + color.reset,
        logging.WARNING: color.yellow + format_ + color.reset,
        logging.ERROR: color.red + format_ + color.reset,
        logging.CRITICAL: color.bold_red + format_ + color.reset,
    }

    def __init__(self, fmt_keys: dict[str, str]):
        super().__init__()
        self.fmt_keys = fmt_keys or {}

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        self._style = logging.PercentStyle(log_fmt)
        self._fmt = self._style._fmt

        self.datefmt = "%H:%M:%S"
        return super().format(record)

    def formatterException(e):
        return e

class Logger:
    # class of the logger, use: logger = Logger()
    def print(self, tags: str, message: str) -> None:
        print(f"[{tags}] {message}")

    def warning(
            self,
            tags: str,
            message: str,
            extra: bool = False,
            stack_info: bool = False,
            stack_level: int = 1,
            *args: object
    ):
        print(tags, message, hour.now(), color.yellow, *args)

    def error(
            self,
            tags: str,
            message: str,
            extra: bool = False,
            stack_info: bool = False,
            stack_level: int = 1,
            *args: object
    ):
        print(tags, message, hour.now(), color.red, *args)

    def critical(
                self,
                tags: str,
                message: str,
                extra: bool = False,
                stack_info: bool = False,
                stack_level: int = 1,
                *args: object
        ):
            print(tags + "" + message + "" + hour.now() + color.bold_red, *args)

    def error(
                self,
                tags: str,
                message: str,
                extra: bool = False,
                stack_info: bool = False,
                stack_level: int = 1,
                *args: object
        ):
            print(tags, message, hour.now(), color.grey, *args)
