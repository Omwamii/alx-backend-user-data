#!/usr/bin/env python3
""" Module with BasicAUth class"""
from api.v1.auth.auth import Auth
import base64
from flask import request


class BasicAuth(Auth):
    """ BasicAuth class """
    def extract_base64_authorization_header(self, authorization_header: str)\
            -> str:
        """ returns base64 part of auth header """
        header = authorization_header
        if not header:
            return None
        if not isinstance(header, str):
            return None
        if not header.startswith('Basic '):
            return None
        return header[len('Basic '):]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """ returns the decoded value of a Base64 string """
        header = base64_authorization_header
        if not header:
            return None
        if not isinstance(header, str):
            return None
        try:
            is_base64 = base64.b64encode(base64.b64decode(header)) == header
        except Exception:
            return None
        else:
            return base64.b64decode(header).decode("utf-8")

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ Return the user email & password from base64 decoded value """
        header = decoded_base64_authorization_header
        if not header:
            return (None, None)
        if not isinstance(header, str):
            return (None, None)
        if ":" not in header:
            return (None, None)
        data = header.split(":")
        email, passwd = data[0], data[1]
        return (email, passwd)
