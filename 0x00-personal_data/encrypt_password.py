#!/usr/bin/env python3
"""This module encrypts passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Return a salted, hashed password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)
