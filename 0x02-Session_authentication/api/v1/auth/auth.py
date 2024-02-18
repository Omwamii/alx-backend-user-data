#!/usr/bin/env python3
""" Module with auth class """
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Authentication API management app
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False if authentication is not required for a path
        else return true
        """
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Check if header has authorization key
        return None if no """
        if request is None:
            return None
        header_key = request.headers.get('Authorization')
        if not header_key:
            return None
        return header_key

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None """
        return None

    def session_cookie(self, request=None) -> str:
        """ returns a cookie value from a request """
        if request is None:
            return None
        cookie_name = getenv('SESSION_NAME')
        cookie = request.cookies.get(cookie_name)
