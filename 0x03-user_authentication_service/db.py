#!/usr/bin/env python3

"""
DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Saves user to database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **filters) -> User:
        """ Find use based on provided filters
        """
        for k in filters.keys():
            if not hasattr(User, k):
                raise InvalidRequestError

        user = self._session.query(User).filter_by(**filters).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **values) -> None:
        """ Update the user in the user_id
        """
        user = None
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            return

        for k, v in values.items():
            if k not in user.__dict__:
                raise ValueError
            setattr(user, k, v)
        self._session.add(user)
        self._session.commit()
