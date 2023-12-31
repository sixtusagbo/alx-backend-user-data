#!/usr/bin/env python3
"""Basic Flask app"""
from os import abort
from flask import Flask, jsonify, redirect, request
from auth import Auth

app = Flask(__name__)
app.strict_slashes = False
AUTH = Auth()


@app.route("/")
def base():
    """Base route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Register a user"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """Log a user into the app"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        if AUTH.valid_login(email, password):
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", AUTH.create_session(email))
            return response
        else:
            abort(401)
    except Exception:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Log out"""
    session_id = request.cookies.get("session_id")

    try:
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        return redirect("/")
    except Exception:
        abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    """User profile"""
    session_id = request.cookies.get("session_id")
    try:
        user = AUTH.get_user_from_session_id(session_id)
        return jsonify({"email": user.email})
    except Exception:
        abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """Get reset password token"""
    email = request.form.get("email")

    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    except Exception:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """Update password end-point"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
