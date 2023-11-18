#!/usr/bin/env python3
"""Auth module"""
import uuid
from sqlalchemy.orm.exc import NoResultFound
from user import User
import bcrypt
from db import DB


def _hash_password(password: str) -> bytes:
    """Return a salted hash of the input password"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash


def _generate_uuid() -> str:
    """Return a new unique identifier"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Return the newly registered user"""
        if (
            email is None
            or not isinstance(email, str)
            or password is None
            or not isinstance(password, str)
        ):
            raise ValueError("email or password is missing")

        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(user.email))
        except NoResultFound:
            hashed = _hash_password(password)
            return self._db.add_user(email=email, hashed_password=hashed)

    def valid_login(self, email: str, password: str) -> bool:
        """Check if login details are valid"""
        try:
            user = self._db.find_user_by(email=email)
            pass_bytes = password.encode("utf-8")
            return bcrypt.checkpw(pass_bytes, user.hashed_password)
        except Exception:
            return False
