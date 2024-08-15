#!/usr/bin/env python3

from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4


def _hash_password(password: str) -> str:
    """Returns salted hashed password as bytestring"""
    return hashpw(password.encode("utf-8"), gensalt())


def _generate_uuid() -> str:
    """Returns string representation of a new UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers new user if email does not exist in db"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Implements credential validation"""
        try:
            user_found = self._db.find_user_by(email=email)
            return checkpw(
                    password.encode("utf-8"),
                    user_found.hashed_password
                    )

        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Finds user corresponding to email,
        generates a new UUID and store it in the database
        as the user's session_id
        """
        try:
            user_found = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user_found.id, session_id=session_id)
        return session_id
