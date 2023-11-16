#!/usr/bin/env python3
"""This module implements session authentication with expiration
for session id"""
from datetime import datetime, timedelta
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session auth with expiration"""

    def __init__(self) -> None:
        """Initialize an instance of this class"""
        super().__init__()
        duration = os.getenv("SESSION_DURATION", 0)

        try:
            self.session_duration = int(duration)
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session id for a user id"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return a user id based on a session id"""
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_id is None or session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict['user_id']

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        session_duration = timedelta(seconds=self.session_duration)
        session_expiration_time = created_at + session_duration

        if session_expiration_time < datetime.now():
            return None

        return session_dict['user_id']
