# app/core/log_config.py

import logging
from logging.config import dictConfig
import atexit

from app.core.app_config import settings


class HTMLFormatter(logging.Formatter):
    def format(self, record):
        log_entry = super().format(record)
        return f"<tr><td>{record.asctime}</td><td>{record.name}</td><td>{record.levelname}</td><td>{log_entry}</td></tr>"

    @staticmethod
    def formatHeader():
        return """
        <html>
        <head>
            <style>
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid black; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                tr:nth-child(even) { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
        <table>
            <tr><th>Time</th><th>Logger</th><th>Level</th><th>Message</th></tr>
        """

    @staticmethod
    def formatFooter():
        return """
        </table>
        </body>
        </html>
        """


LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "html": {
            "()": HTMLFormatter,
            "format": "%(asctime)s %(message)s",
        },
    },
    "handlers": {
        "html_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "log.html",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "html",
            "level": logging.DEBUG if settings.DEBUG else logging.INFO,
        },
    },
    "loggers": {
        "": {
            "handlers": ["html_file"],
            "level": logging.DEBUG if settings.DEBUG else logging.INFO,
            "propagate": True,
        },
    },
}


def configure_logging():
    dictConfig(LOG_CONFIG)

    # Add header to the log file
    with open("log.html", "w") as log_file:
        log_file.write(HTMLFormatter.formatHeader())

    # Ensure footer is added when the application exits
    @atexit.register
    def add_footer():
        with open("log.html", "a") as log_file:
            log_file.write(HTMLFormatter.formatFooter())
