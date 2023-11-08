"""Auth route module for the API
"""
from typing import List, TypeVar
from flask import request


class Auth(object):
    """API Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if a route path requires auth"""
        return False

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Return current user for a request"""
        return None
