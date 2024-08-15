#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

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
        """Saves a user to the database"""
        newUser = User(email=email, hashed_password=hashed_password)
        self._session.add(newUser)
        self._session.commit()
        return newUser

    def find_user_by(self, **kwargs) -> User:
        """Returns first row of users table filtered by input arguments"""
        try:
            record = self._session.query(User).filter_by(**kwargs).first()

        if record is None:
                raise NoResultFound(f"No user found with criteria: {kwargs}")

        return record



    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates user's attributes"""
        user_record = self.find_user_by(id=user_id)

        if not user_record:
            raise ValueError(f"No user found with id: {user_id}")

        for key, value in kwargs.items():
            if hasattr(user_record, key):
                setattr(user_record, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}")

        self._session.commit()
        return None
