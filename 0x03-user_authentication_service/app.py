#!/usr/bin/env python3
""" Basic Flask App for Auth """
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def index():
    """ Index route """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """ endpoint to register users """
    email = str(request.form.get('email'))
    passw = str(request.form.get('password'))
    try:
        AUTH.register_user(email, passw)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({"email": f"{email}", "message": "user created"})


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """ Login """
    email = str(request.form.get('email'))
    passw = str(request.form.get('password'))
    if not AUTH.valid_login(email, passw):
        abort(401)
    sesh_id = AUTH.create_session(email)
    response = jsonify({"email": f"{email}", "message": "logged in"})
    response.set_cookie('session_id', sesh_id)
    return response


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """ Logout """
    sesh_id = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(sesh_id)
    if not user or not sesh_id:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", strict_slashes=False)
def profile() -> str:
    """ return user's email based on session cookie """
    sesh_id = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(sesh_id)
    if not user:
        abort(403)
    return jsonify({"email": "<user email>"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5000")
