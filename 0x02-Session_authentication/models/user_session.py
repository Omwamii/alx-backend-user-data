#!/usr/bin/env python3
""" Module with UserSession class """
from models.base import Base


class UserSession(Base):
    """ Implement session storage in DB """
    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize vars """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
