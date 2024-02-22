#!/usr/bin/env python3
""" Auth module """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """ returnes hashed password """
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pw


def _generate_uuid() -> str:
    """ Generate unique UUID """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ Init variables """
        self.__db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a user """
        try:
            self.__db.find_user_by(email=email)
        except NoResultFound:
            hashed_pw = _hash_password(password)
            new_user = self.__db.add_user(email, hashed_pw)
            return new_user
        else:
            # user already exists with the provided email
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """ Checks if password is valid for user's email (login)
        """
        try:
            user = self.__db.find_user_by(email=email)
        except Exception:
            return False  # user doesn't exist
        else:
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
