#!/usr/bin/env python3
"""Regex-ing"""
import re
from typing import List
import logging


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Returns the log message obfuscated"""
    for field in fields:
        pattern = r"{}=([^{}]+)".format(field, separator)
        message = re.sub(pattern, "{}={}".format(field, redaction), message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initalize formatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Fitered formatter"""
        unsafe_str = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, unsafe_str, self.SEPARATOR
        )
