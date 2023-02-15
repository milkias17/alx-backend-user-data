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


@app.route("/profile")
def profile():
    """
    Profile page api route that returns a json paylod with the user's email
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    return jsonify(email=user.email)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """
    Gives the password reset token
    """
    email = request.form.get("email")
    if not email:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify(email=email, reset_token=reset_token)
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """
    Updates the users password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    if not email or not reset_token or not new_password:
        abort(403)

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify(email=email, message="Password updated")
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
