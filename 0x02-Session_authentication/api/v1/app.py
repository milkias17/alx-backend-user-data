#!/usr/bin/env python3
"""
App.py
"""
from os import getenv

from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if getenv("AUTH_TYPE") == "basic_auth":
    auth = BasicAuth()
else:
    auth = Auth()


@app.before_request
def check_requires_auth():
    """
    filters requests that need authorization
    """
    requires_auth = auth.require_auth(
        request.path, ['/api/v1/status/',
                       '/api/v1/unauthorized/',
                       '/api/v1/forbidden/'])
    if not requires_auth:
        return None
    if not auth.authorization_header(request):
        abort(401)
    user = auth.current_user(request)
    if not user:
        abort(403)
    request.current_user = user


@app.errorhandler(404)
def not_found(e) -> str:
    """ Handle 404
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(e) -> str:
    """
        Handle 401
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(e) -> str:
    """
        Handle 403
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
