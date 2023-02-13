#!/usr/bin/env python3
"""
Auth module
"""
from uuid import uuid4

import bcrypt
from db import DB
from sqlalchemy.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """ Hash given password
    """
    return bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ Generate a unique identifier
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Class constructor
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Regiser a new user to database
        """
        found = True
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            found = False

        if found:
            raise ValueError(f"User {email} already exists")

        return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """ Checks if the given credentials are valid
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode("UTF-8"),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ Returns a session_id for a user
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
