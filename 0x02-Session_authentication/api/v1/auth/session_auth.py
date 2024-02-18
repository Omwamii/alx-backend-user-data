#!/usr/bin/env python3
""" Module with SessionAUth class """
from api.v1.auth.auth import Auth
import uuid
from models.user import User
from flask import request
# from typing import TypeVar


class SessionAuth(Auth):
    """ Session Authentication class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a session ID for a user_id """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        sesh_id = str(uuid.uuid4())
        self.user_id_by_session_id[sesh_id] = user_id
        return sesh_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a session ID """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns a User instance based on a cookie value """
        sesh_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(sesh_id)
        user = User.get(id=user_id)
        return user

    def destroy_session(self, request=None):
        """ deletes a user session (logout) """
        if request is None:
            return False
        sesh_id = self.session_cookie(request)
        if sesh_id is None:
            return False
        if self.user_id_for_session_id(sesh_id) is None:
            return False
        del self.user_id_by_session_id[sesh_id]
        return True
