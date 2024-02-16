#!/usr/bin/env python3
""" Module with BasicAUth class"""
from api.v1.auth.auth import Auth
import base64
from flask import request
from models.user import User
from typing import TypeVar


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

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ Returns the User instance based on email & passwd """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for u in users:
                if u.is_valid_password(user_pwd):
                    return u
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User instance based on a received request
        """
        Auth_header = self.authorization_header(request)
        if Auth_header is not None:
            token = self.extract_base64_authorization_header(Auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, pword = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, pword)
        return
