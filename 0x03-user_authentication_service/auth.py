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

    def get_user_from_session_id(self, session_id: str) -> str:
        """Finds corresponding user by session_id"""
        if session_id is None:
            return None
        try:
            found_user = self._db.find_user_by(session_id=session_id)
            return found_user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """ Updates user's session_id to None"""
        if user_id is None:
            return None
        try:
            found_user = self._db.find_user_by(id=user_id)
            self._db.update_user(found_user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ Finds user by email, updates user's reset_toke with UUID """
        try:
            found_user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(found_user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the user's password using the reset token.
        Raises ValueError if the reset token is invalid or user does not exist.
        """
        if not reset_token or not password:
            return None

        user = self._db.find_user_by(reset_token=reset_token)
        if user is None:
            raise ValueError

        self._db.update_user(
            user.id,
            hashed_password=_hash_password(password),
            reset_token=None
        )
