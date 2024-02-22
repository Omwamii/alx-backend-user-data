#!/usr/bin/env python3
""" Basic Flask App for Auth """
from flask import Flask, jsonify, request, abort
from auth import Auth

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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5000")
