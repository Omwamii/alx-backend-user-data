#!/usr/bin/env python3
""" Module with 'filter_datum' method """
import re
from typing import List


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
                         field+'='+redaction+separation, message)
    return message
