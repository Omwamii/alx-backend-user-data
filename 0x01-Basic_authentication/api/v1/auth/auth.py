#!/usr/bin/env python3
""" Module with auth class """
from flask import request
from Typing import List, TypeVar


class Auth:
    """ Authentication API management app
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False """
        return False

    def authorization_header(self, request=None) -> str:
        """ returns None """
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None """
        return request
