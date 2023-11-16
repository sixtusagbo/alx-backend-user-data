#!/usr/bin/env python3
"""Auth route module for the API
"""
from typing import List, TypeVar
from flask import request
from itsdangerous import exc
import os


class Auth:
    """API Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if a route path requires auth"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for excluded_path in excluded_paths:
            if path.rstrip("/") == excluded_path.rstrip("/"):
                return False
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        if request is None or request.headers.get("Authorization") is None:
            return None
        else:
            return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """Return current user for a request"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME")
        return request.cookies.get(session_name)
