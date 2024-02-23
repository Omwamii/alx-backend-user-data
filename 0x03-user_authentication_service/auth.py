#!/usr/bin/env python3
""" Auth module """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
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
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a user """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pw = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pw)
            self._db._session.commit()
            return new_user
        else:
            # user already exists with the provided email
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """ Checks if password is valid for user's email (login)
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False  # user doesn't exist
        else:
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)

    def create_session(self, email: str) -> str:
        """ finds user with email & returns the session ID as string """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            sesh_id = _generate_uuid()
            self._db.update_user(user.id, session_id=sesh_id)
            return sesh_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ Returns a user object from session_id or None """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        else:
            return user

    def destroy_session(self, user_id: int) -> None:
        """ Destroy session & update user's session ID to none
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            return None  # user not found
        return None  # user's session deleted in db
