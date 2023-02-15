#!/usr/bin/env python3

"""
Flask app
"""

from auth import Auth
from flask import Flask, abort, jsonify, redirect, request
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """ Flask home route
    """
    return jsonify(message="Bienvenue")


@app.route("/users", methods=["POST"])
def register_user():
    """ Register user endpoint
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or password is None:
        return

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": "<registered email>",
                        "message": "user created"})
    except ValueError:
        return jsonify(message="email already registered"), 400


@app.route("/sessions", methods=["POST"])
def login():
    """ Logs in a user
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or password is None:
        return

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = None
    try:
        session_id = AUTH.create_session(email)
    except NoResultFound:
        abort(401)

    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp


@app.route("/sessions", methods=["DELETE"])
def logout():
    """ Logs out the current user
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
