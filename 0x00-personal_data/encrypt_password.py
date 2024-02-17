#!/usr/bin/env python3
"""
Module dealing with password hashing & validation
"""
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """ 
    Returns a hashed password
    Args:
        password (str): password to be hashed
    """
    b = password.encode()
    hashed = hashpw(b, bcrypt.gensalt())
    return hashed
