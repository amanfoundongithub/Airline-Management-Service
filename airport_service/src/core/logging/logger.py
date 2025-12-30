from datetime import datetime
from typing   import Any


class Logger:
    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[41m",  # Red background
    }

    RESET = "\033[0m"

    def __init__(self, name: str, level: str = "INFO"):
        self.name = name
        self.level = level

    def _log(self, level: str, message: str, **kwargs: Any) -> None:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        color = self.COLORS.get(level, "")

        extra = ""
        if kwargs:
            extra = " | " + " ".join(f"{k}={v}" for k, v in kwargs.items())

        print(
            f"{color}{timestamp} | {level:<8} | {self.name} | {message}{extra}{self.RESET}"
        )

    def debug(self, message: str, **kwargs: Any) -> None:
        self._log("DEBUG", message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        self._log("INFO", message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        self._log("WARNING", message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        self._log("ERROR", message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        self._log("CRITICAL", message, **kwargs)
