#!/usr/bin/env python3
"""Auth route module for the API
"""
from typing import List, TypeVar
from flask import request
from itsdangerous import exc


class Auth:
    """API Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if a route path requires auth"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        path = path if path[-1] == "/" else path + "/"
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Return current user for a request"""
        return None
