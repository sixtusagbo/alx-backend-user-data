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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
