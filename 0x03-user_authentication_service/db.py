#!/usr/bin/env python3

"""
DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        """ Save user to database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

    def find_user_by(self, **filters) -> User:
        """ Find use based on provided filters
        """
        user = self._session.query(User).filter_by(**filters).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **values) -> None:
        """ Update the user in the user_id
        """
        user = self.find_user_by(id=user_id)
        for k, v in values.items():
            if k not in user.__dict__:
                raise ValueError
            setattr(user, k, v)
        self._session.add(user)
        self._session.commit()
