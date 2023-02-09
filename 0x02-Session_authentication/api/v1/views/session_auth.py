#!/usr/bin/env python3
"""
Api routes for all session based authentication tasks
"""

from os import getenv

from api.v1.views import app_views
from flask import jsonify, request
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login():
    """
    Logs in a user from a form submission
    """
    user_email = request.form.get('email')
    user_password = request.form.get('password')

    if not user_email:
        return jsonify({"error": "email missing"}), 400
    if not user_password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": user_email})

    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(user_password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    resp = jsonify(user.to_json())
    resp.set_cookie(getenv("SESSION_NAME"), session_id)
    return resp
