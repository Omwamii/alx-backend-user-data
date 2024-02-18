#!/usr/bin/env python3
""" Module of authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv as env


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def handle_auth():
    """ Handles all routes for session authentication """
    email = request.form.get('email')
    if email is None:
        return jsonify({'error': "email missing"}), 400
    passwd = request.form.get('password')
    if passwd is None:
        return jsonify({'error': "password missing"}), 400
    user = User.search({'email': email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if not user.is_valid_password(passwd):
        return jsonify({"error": "wrong password"}), 401

    # create session ID for user id
    from api.v1.app import auth
    sesh_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(env('SESSION_NAME'), sesh_id)
    return response
