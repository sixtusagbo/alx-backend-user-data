#!/usr/bin/env python3
"""
Basic Authentication module for the API
"""
import base64
from api.v1.auth.auth import Auth
import binascii


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

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """Return the decoded value of a base64 string"""
        if base64_authorization_header is None or not isinstance(
            base64_authorization_header, str
        ):
            return None
        try:
            base64_bytes = base64.b64decode(base64_authorization_header)
            return base64_bytes.decode("utf-8")
        except binascii.Error as e:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Return user email and password"""
        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
            or ":" not in decoded_base64_authorization_header
        ):
            return (None, None)
        email, password = decoded_base64_authorization_header.split(":")
        return (email, password)
