#!/usr/bin/env python3
"""Regex-ing"""
import re
from typing import List
import logging
from mysql.connector.connection import MySQLConnection
from os import getenv
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Returns the log message obfuscated"""
    for field in fields:
        pattern = r"{}=([^{}]+)".format(field, separator)
        message = re.sub(pattern, "{}={}".format(field, redaction), message)
    return message


def get_logger() -> logging.Logger:
    """Return a `logging.Logger` object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handler)
    logger.propagate = False

    return logger


def get_db() -> MySQLConnection:
    """Returns a connector to the database"""
    username = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = getenv("PERSONAL_DATA_DB_NAME", "my_db")

    connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=db_name,
    )

    return connection


def main() -> None:
    """Display db rows in a filtered format"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        message = (
            "name={};email={};phone={};ssn={};password={};ip={};"
            "last_login={};user_agent={};".format(*row)
        )
        logger.info(message)
    cursor.close()
    db.close()


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


if __name__ == "__main__":
    main()
