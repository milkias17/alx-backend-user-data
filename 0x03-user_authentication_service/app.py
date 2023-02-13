#!/usr/bin/env python3

"""
Flask app
"""

from auth import Auth
from flask import Flask, jsonify, request

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

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": "<registered email>",
                        "message": "user created"})
    except ValueError:
        return jsonify(message="email already registered"), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
