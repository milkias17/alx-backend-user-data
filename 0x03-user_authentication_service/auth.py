#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from sqlalchemy.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """ Hash given password
    """
    return bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())


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
