#!/usr/bin/env python3

from flask import Flask, jsonify, request, abort
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def home():
    """GET /home
    Return:
        -JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def new_user() -> str:
    """POST /users
    Registers new user with email and password, checks
    if user is already registered
    Return:
        -JSON payload
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        new_user = AUTH.register_user(email, password)
        if new_user is not None:
            return jsonify({
                "email": new_user.email,
                "message": "user created"
            })
    except ValueError:
        return jsonify({
            "message": "email already registered"
        }), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """POST /sessions
    Creates new user session and stores as cookie
    Return:
        -JSON payload
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({
        "email": email,
        "message": "logged in"
    })
    response.set_cookie("session_id", session_id)
    return response
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
