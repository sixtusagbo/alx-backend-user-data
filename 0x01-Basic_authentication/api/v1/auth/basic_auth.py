#!/usr/bin/env python3
"""
Basic Authentication module for the API
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """API Basic Authentication"""

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """Extract Base 64 authorization header"""
        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
            or authorization_header[:6] != "Basic "
        ):
            return None
        else:
            return authorization_header[6:]
