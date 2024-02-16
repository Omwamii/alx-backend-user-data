#!/usr/bin/env python3
""" Module with auth class """
from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication API management app
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        # add tolerance for routes not ending with '/'
        if not path.endswith('/'):
            path += '/'
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ returns None """
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None """
        return request
