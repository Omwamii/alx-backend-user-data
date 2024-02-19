#!/usr/bin/env python3
from flask import request
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class implementation """
    def create_session(self, user_id=None):
        """ (overload) Create and store new instance of UserSession
            & return session ID
        """
        sesh_id = super().create_session(user_id)
        user_sesh_obj = UserSession(user_id=user_id, session_id=sesh_id)
        user_sesh_obj.save()
        return sesh_id

    def user_id_for_session_id(self, session_id=None):
        """ (overload) request UserSession from database based on session ID
            returns user id of the stored object
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None):
        """ Delete UserSession based on session ID from request"""
        session_id = self.session_cookie(request)  # get session id for req
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
