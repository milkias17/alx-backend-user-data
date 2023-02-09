#!/usr/bin/env python3

"""
Session Based Authorization
"""

from uuid import uuid4

from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    Session Authorization class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Generates a unique session id and stores it
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns the user_id stored for the given session_id
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return SessionAuth.user_id_by_session_id.get(session_id)
