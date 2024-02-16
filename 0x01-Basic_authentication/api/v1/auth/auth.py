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
        for ex_path in excluded_paths:
            if ex_path.endswith("*"):
                ex_l = len(ex_path.split("*")[0])
                if path[:ex_l] == ex_path:
                    return False
            elif ex_path == path:
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
