#!/usr/bin/env python3
"""Implements session authentication with database as storage"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session authentication with database as storage"""

    def create_session(self, user_id=None):
        """Create and store a new instance of `UserSession` and
        returns the session id
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return the User ID by requesting `UserSession` in
        the database based on `session_id`
        """
        # Inherit the expiration features
        user_id = super().user_id_for_session_id(session_id)
        if user_id is None:
            return None

        # Request `UserSession` in database (mocked with file here)
        # See views module __init__.py for UserSession load call
        try:
            sessions = UserSession.search({"session_id": session_id})
            if len(sessions) == 0:
                return None
            session: UserSession = sessions[0]
            return session.user_id
        except Exception:
            return None

    def destroy_session(self, request=None):
        """Destroys the `UserSession` based on the Session ID from
        the request cookie"""
        # Inherit some destroy logic
        destroyed = super().destroy_session(request)
        if not destroyed:
            return False

        session_id = self.session_cookie(request)
        # Delete the `UserSession` from the database (mocked with file here)
        try:
            sessions = UserSession.search({"session_id": session_id})
            if len(sessions) == 0:
                return None
            session: UserSession = sessions[0]
            session.remove()
            return True
        except Exception:
            return False
