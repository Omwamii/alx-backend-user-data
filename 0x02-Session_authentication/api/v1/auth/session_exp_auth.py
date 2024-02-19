#!/usr/bin/env python3
""" Module with SessionExpAuth class """
from api.v1.auth.session_auth import SessionAuth
from os import getenv as env
from datetime import datetime as time, timedelta


class SessionExpAuth(SessionAuth):
    """ Session class implementation with Expiry time """
    user_id_by_session_id = {}

    def __init__(self):
        """ Initialize vars, overload __init__ """
        super().__init__()
        try:
            self.session_duration = int(env('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ create session ID for user """
        sesh_id = super().create_session(user_id)
        if not sesh_id:
            return None
        session_dictionary = {'user_id': user_id, 'created_at': time.now()}
        self.user_id_by_session_id[sesh_id] = session_dictionary
        return sesh_id

    def user_id_for_session_id(self, session_id=None):
        """ Get a user from session ID """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id.get(session_id)['user_id']
        sesh_t = self.user_id_by_session_id[session_id].get('created_at')
        if not sesh_t:
            return None
        if sesh_t + timedelta(seconds=self.session_duration) < time.now():
            # session expired
            return None
        return self.user_id_by_session_id.get(session_id)['user_id']
