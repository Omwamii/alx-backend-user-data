#!/usr/bin/env python3
""" Module with 'filter_datum' method """
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ uses regex to replace occurences of strings to obfuscate
    Args:
        fields: list of strings indicating fields to be obfuscated
        redaction: what field will be obfuscated to
        message: log line to obfuscate
        separator: character separating the fields
    """
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initialize variables """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        redact the message of LogRecord instance
        Args:
        record (logging.LogRecord): LogRecord instance containing message
        Return:
            formatted string
        """
        message = super(RedactingFormatter, self).format(record)
        redacted = filter_datum(self.fields, self.REDACTION,
                                message, self.SEPARATOR)
        return redacted
